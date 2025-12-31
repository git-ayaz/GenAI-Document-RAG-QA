import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Multi-Doc RAG Chatbot", layout="centered")
st.title("📄 Multi-Document RAG Chatbot")

# ---------- SESSION STATE ----------

if "documents" not in st.session_state:
    st.session_state.documents = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- UPLOAD ----------

st.subheader("Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file:
    files = {"file": uploaded_file}
    res = requests.post(f"{BACKEND_URL}/upload", files=files)

    if res.status_code == 200:
        data = res.json()
        if data["filename"] not in st.session_state.documents:
            st.session_state.documents.append(data["filename"])
        st.success("PDF uploaded and indexed")
    else:
        st.error("Upload failed")

# ---------- CHAT ----------

if st.session_state.documents:
    st.subheader("Select Document")

    selected_doc = st.selectbox(
        "Choose document",
        st.session_state.documents
    )

    question = st.text_input("Ask a question")

    if st.button("Ask") and question:
        payload = {
            "question": question,
            "selected_doc": selected_doc,
            "chat_history": st.session_state.chat_history
        }

        res = requests.post(
            f"{BACKEND_URL}/ask",
            json=payload
        )

        if res.status_code == 200:
            answer = res.json()["answer"]

            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

        else:
            st.error("Failed to get answer")

# ---------- DISPLAY CHAT ----------

if st.session_state.chat_history:
    st.divider()
    st.subheader("Conversation")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")
