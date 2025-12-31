from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
import shutil

from rag import ingest_pdf, ask_question

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class AskRequest(BaseModel):
    question: str
    selected_doc: str
    chat_history: List[dict]


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ingest_pdf(path)
    return {"message": "PDF processed", "filename": file.filename}


@app.post("/ask")
async def ask(req: AskRequest):
    answer = ask_question(
        question=req.question,
        chat_history=req.chat_history,
        selected_doc=req.selected_doc
    )
    return {"answer": answer}
