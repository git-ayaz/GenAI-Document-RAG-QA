import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

VECTOR_DB_DIR = "vectorstore"

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

from dotenv import load_dotenv
load_dotenv(override=True)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Answer ONLY using the context below.

Context:
{context}

Question:
{question}

If the answer is not present, say you don't know.
"""
)


def ingest_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = os.path.basename(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    # ✅ Persistence is automatic now
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=VECTOR_DB_DIR
    )


def ask_question(question: str, chat_history: list, selected_doc: str):
    db = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embedding
    )

    retriever = db.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {"source": selected_doc}
        }
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    for msg in chat_history:
        if msg["role"] == "user":
            memory.chat_memory.add_user_message(msg["content"])
        else:
            memory.chat_memory.add_ai_message(msg["content"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa.invoke({"query": question})["result"]
