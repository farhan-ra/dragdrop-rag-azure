import os
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.pdf_loader import add_pdf_to_index
from backend.rag_chat import ChromaRAGChat
from backend.config import settings

app = FastAPI(title=settings.ASSISTANT_NAME)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")
chat_engine = ChromaRAGChat()

@app.get("/chat", response_class=HTMLResponse)
async def serve_chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "assistant_name": settings.ASSISTANT_NAME})

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    chunks = add_pdf_to_index(temp_path, file.filename)
    os.remove(temp_path)
    return {"status": "success", "chunks_added": chunks}

@app.post("/chat_message")
async def chat_message(message: str = Form(...)):
    reply = chat_engine.chat(message)
    return {"reply": reply}
