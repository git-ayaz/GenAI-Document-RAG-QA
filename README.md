# 📄 Multi-Document RAG Chatbot

A **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload **multiple PDF documents** and ask **context-aware questions** with **chat memory**.  
The system uses a **FastAPI backend**, **Streamlit frontend**, **ChromaDB** for vector storage, and **Groq LLMs** for fast inference.

---

## 🚀 Features

- 📂 Upload and index **multiple PDF documents**
- 🔍 Ask questions **specific to a selected document**
- 🧠 **Chat memory** for multi-turn conversations
- ⚡ Fast inference using **Groq LLM**
- 🧾 Context-grounded answers (no hallucination)
- 🖥️ Clean Streamlit UI
- 🔗 REST API powered by FastAPI

---

## 🛠️ Tech Stack

**Frontend**
- Streamlit

**Backend**
- FastAPI
- Uvicorn

**RAG Pipeline**
- LangChain
- ChromaDB (Vector Store)
- Sentence Transformers (Embeddings)

**LLM**
- Groq (ChatGroq)

---

## 📁 Project Structure

multi-doc-rag-chatbot/
│
├── backend/
│ ├── api.py # FastAPI endpoints
│ ├── rag.py # RAG logic (ingestion + retrieval)
│ ├── uploads/ # Uploaded PDFs
│ └── vectorstore/ # ChromaDB data
│
├── frontend/
│ └── app.py # Streamlit UI
│
├── requirements.txt
├── .env
└── README.md


---

## 🔐 Environment Setup

Create a `.env` file in the project root:

GROQ_API_KEY=your_groq_api_key_here

---

## 📦 Installation

### 1️⃣ Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate     # Linux / Mac
env\Scripts\activate        # Windows
```
### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Running the Application
Start Backend (FastAPI)
```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000
```

Start Frontend (Streamlit)
```bash
cd frontend
streamlit run app.py
```
Open: http://localhost:8501

## 💬 How It Works
Upload one or more PDF files
Documents are split into chunks and embedded
Embeddings are stored in ChromaDB
User selects a document and asks a question
Relevant chunks are retrieved
LLM generates an answer using retrieved context and chat history



