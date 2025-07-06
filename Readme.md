# ⚖️ NyayaMate: Your Indian Legal Assistant

NyayaMate is a next-gen AI-powered legal assistant designed specifically for Indian citizens. Unlike generic chatbots, NyayaMate uses a custom-trained Sentence Transformer model fine-tuned on real Indian legal data (including sections from the Bharatiya Nyaya Sanhita, 2023) to accurately match user grievances with relevant legal provisions.

With a sleek Streamlit interface and Google Gemini integration, it offers:

✨ Context-aware summaries of matched BNS sections in plain English

🔍 Accurate mapping to corresponding IPC sections using legal cross-reference data

🧠 Smart procedural advice tailored to the seriousness of the offense (serious vs. soft)

📚 Case law discovery from trusted Indian legal portals like Indian Kanoon, Bar & Bench, and LiveLaw

📘 Precise descriptions of each matched BNS section to help users understand the law clearly


## 📸 Screenshots

### 🧑‍⚖️ Landing Page
![Landing Page](./assets/Screenshot%202025-07-06%20174307.png)

### 🧠 Summary & Section Selection
![Summary](./assets/Screenshot%202025-07-06%20174533.png)

### 📘 BNS Descriptions Output
![BNS Descriptions](./assets/Screenshot%202025-07-06%20174601.png)

### 📚 Case History Output
![Case History](./assets/Screenshot%202025-07-06%20175528.png)
## 🚀 Features

- 🔎 Semantic search over BNS using MiniLM and FAISS
- 🧠 Summarization and legal advice via Google Gemini Pro (2.5 Flash)
- 📊 Dynamic section loading based on user selection (summary → then next action)
- 🌐 Real-time scraping of relevant case laws from trusted legal portals

## 🛠️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/PrajwalBagchi/NyayMate.git
   cd NyayMate

2. Create and activate a virtual environment:
   ```bash 
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   
4. Create a .env file in the root directory and add your Gemini API key:
   ```bash
    GEMINI_API_KEY=your_google_gemini_key_here

5. Run the app:
   ```bash
    streamlit run app/app.py

6. 📁 Project Structure
   ```bash
    NyayaMate/
    ├── app/
    │   ├── app.py              # Streamlit UI logic
    │   └── model.py            # Backend search, summarization, scraping
    ├── app/data/               # BNStoIPC.csv
    ├── app/embeddings/         # FAISS index + BNS Pickle
    ├── assets/                 # Screenshots for README
    ├── requirements.txt
    ├── .env                    # Your Gemini API key
    └── README.md

7. ✅ Notes

The app does not give legal verdicts. It only suggests relevant law sections and advice for informational purposes.

Built with ❤️ for legal accessibility and literacy in India.

🧑‍💻 Built by:
Prajwal Bagchi

Feel free to open issues or contribute!
