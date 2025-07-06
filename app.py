import streamlit as st
import pandas as pd
from model import generate_final_response

st.set_page_config(page_title="NyayaMate - Legal Assistant", layout="wide")

st.title("⚖️ NyayaMate: Your Indian Legal Assistant")
st.markdown("Enter your grievance or query in plain English (e.g., *'My neighbor threatens me every day'*):")

user_query = st.text_input("📝 Type your issue below")

if st.button("🔍 Analyze"):
    with st.spinner("Analyzing relevant BNS sections..."):
        result = generate_final_response(user_query)
        st.session_state.result = result

# Display the result only if available
if "result" in st.session_state:
    result = st.session_state.result
    st.markdown("## 🧠 Summary ")
    st.markdown(result["summary"])

    # 3. Ask what user wants next
    st.subheader("🔍 What would you like to explore next?")
    option = st.selectbox(
        "Choose one:",
        (
            "📌 Mapped IPC Sections",
            "📘 BNS Section Descriptions",
            "🧑‍⚖️ Legal Advice",
            "📂 Case History (Links)"
        )
    )

    if st.button("Show Selected Section"):
        if option == "📌 Mapped IPC Sections":
            st.markdown("### 📌 Mapped IPC Sections")
            st.text(result["ipc_mapping"])

        elif option == "📘 BNS Section Descriptions":
            st.markdown("### 📘 BNS Section Descriptions")
            st.markdown(result["bns_descriptions"])

        elif option == "🧑‍⚖️ Legal Advice":
            st.markdown("### 🧑‍⚖️ Legal Advice")
            st.markdown(result["advice"])

        elif option == "📂 Case History (Links)":
            st.markdown("### 📂 Case History (Links)")
            st.markdown(result["case_links"])
