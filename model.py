import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = 'all-MiniLM-L6-v2'
bns_model = SentenceTransformer(MODEL_NAME)

df = pd.read_pickle("app/embeddings/bns.pkl")
index = faiss.read_index("app/embeddings/faiss_index.bin")

mapping_df = pd.read_csv("app/data/BNStoIPC.csv")

gemini = genai.GenerativeModel("gemini-2.5-flash")


def get_ipc_equivalents_with_description(bns_section_number):
    section_str = str(bns_section_number).strip()
    mapping_df['BNS Sections'] = mapping_df['BNS Sections'].astype(str).str.strip()
    matches = mapping_df[mapping_df['BNS Sections'] == section_str]
    if matches.empty:
        return []

    ipc_sections = matches['IPC Sections'].astype(str).values[0].split(',')
    ipc_sections = [s.strip() for s in ipc_sections]

    ipc_descriptions = []
    for ipc_sec in ipc_sections:
        desc_row = mapping_df[mapping_df['IPC Sections'].astype(str).str.strip() == ipc_sec]
        desc = desc_row.iloc[0].get('IPC Description', 'No description available.') if not desc_row.empty else 'No description available.'
        ipc_descriptions.append((ipc_sec, desc))

    return ipc_descriptions

def get_case_reference_links(section_text):
    try:
        base_url = "https://indiankanoon.org"
        query = section_text.replace(" ", "+")
        search_url = f"{base_url}/search/?formInput={query}"

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a in soup.select("div.result_title > a")[:3]:
            href = base_url + a['href']
            title = a.get_text(strip=True)
            if "docfragment" in href or "vs" in title.lower():
                links.append(f"{title} - {href}")

        return links if links else ["No relevant cases found on Indian Kanoon."]

    except Exception as e:
        return [f"Error fetching cases: {str(e)}"]

#
def generate_final_response(user_query, show_ipc_descriptions=False):
    all_bns_embeddings = bns_model.encode(df['Description'].tolist(), show_progress_bar=False)
    query_embedding = bns_model.encode([user_query])

    index_temp = faiss.IndexFlatL2(all_bns_embeddings.shape[1])
    index_temp.add(all_bns_embeddings)
    distances, indices = index_temp.search(np.array(query_embedding), k=5)
    results = df.iloc[indices[0]][['Section', 'Section _name', 'Description']].to_dict(orient='records')

    bns_for_summary = []
    ipc_mapping_output = ""
    bns_description_output = ""
    procedure_output = ""
    case_links_output = ""

    for r in results:
        sec_id = r['Section']
        bns_name = r['Section _name']
        bns_desc = r['Description']

        bns_for_summary.append(f"Section {sec_id}: {bns_name} - {bns_desc}")

        combined_prompt = f"""
        You're a legal assistant helping a citizen affected by Indian criminal law. Based on the following BNS sections, provide a **single combined legal procedure guide**.

        Here are the relevant sections:

        {chr(10).join([f"Section {r['Section']}: {r['Section _name']} - {r['Description']}" for r in results])}

        In your answer, do the following:
        1. Briefly analyze if the majority of these sections deal with **serious or softer offenses**.
        2. Provide ONE guide on how to file a police complaint (FIR) in India if needed.
        3. Optionally, if any section explicitly requires a different or urgent step, mention that separately.
        4. Mention relevant authorities (Police Station, Magistrate, etc.) and social media handles for awareness.

        Use bullet points or short paragraphs. Plain English only.
        """

        try:
            procedure_output = gemini.generate_content(combined_prompt).text.strip()
        except:
            procedure_output = "Legal procedure guidance unavailable."


        links = get_case_reference_links(f"{bns_name} {sec_id}")
        if links:
            case_links_output += f"Top Articles for Section {sec_id}:\n" + "\n".join(links) + "\n\n"

        ipc_mappings = get_ipc_equivalents_with_description(sec_id)
        if ipc_mappings:
            for ipc_sec, desc in ipc_mappings:
                ipc_mapping_output += f"BNS Section {sec_id} -> IPC Section {ipc_sec}\n"
                bns_description_output += f"Section {sec_id}: {bns_name} - {bns_desc[:200].strip()}...\n\n"
        else:
            ipc_mapping_output += f"BNS Section {sec_id} -> No direct IPC mapping found\n"

    try:
        joined_sections = "\n\n".join(bns_for_summary)
        prompt = (
            f"The following are Indian legal sections relevant to a user's situation:\n\n"
            f"{joined_sections}\n\n"
            "Summarize all of them briefly in one paragraph using plain English."
        )
        combined_summary = gemini.generate_content(prompt).text.strip()
    except Exception:
        combined_summary = "Summary unavailable."

    return {
        "summary": combined_summary,
        "ipc_mapping": ipc_mapping_output,
        "bns_descriptions": bns_description_output,
        "advice": procedure_output,
        "case_links": case_links_output
    }
