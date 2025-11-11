# 🤖 Azure RAG Chatbot Template (with ChromaDB + FastAPI)

A **Retrieval-Augmented Generation (RAG)** chatbot built using **Azure OpenAI**, **FastAPI**, and **ChromaDB**, with an interactive web UI for chat and PDF upload.

This template allows you to:
- Upload PDFs dynamically 🗂️  
- Store and query them using **ChromaDB** as a vector database 🔍  
- Chat with the AI assistant that references uploaded content 💬  
- Easily extend the UI and backend for different assistant use cases 🎯  

---

## 🚀 Features

✅ **Azure OpenAI integration** for embeddings and chat completions  
✅ **Local vector storage** using ChromaDB  
✅ **Drag & Drop PDF upload** with automatic text extraction  
✅ **Clean FastAPI backend** with modular structure  
✅ **Responsive chat UI** with user/assistant bubbles  
✅ **Easily customizable assistant behavior**

---

## 🧩 Project Structure
azure-rag-chatbot/
│
├── app.py # Main FastAPI application
│
├── backend/
│ ├── config.py # Environment and settings
│ ├── pdf_loader.py # PDF parsing and ChromaDB indexing
│ ├── rag_chat.py # RAG chat logic using Azure OpenAI
│
├── frontend/
│ ├── templates/
│ │ └── chat.html # Web chat UI
│ └── static/
│ ├── css/
│ │ └── style.css # UI styling
│ └── js/
│ └── chat.js # Client-side interactivity
│
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md # You are here 😄

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/azure-rag-chatbot.git
cd azure-rag-chatbot
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
```bash
OPEN_AI_ENDPOINT=https://<your-azure-openai-endpoint>.openai.azure.com
OPEN_AI_KEY=<your-azure-openai-key>
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-ada-002
ASSISTANT_NAME=<your-assistant-name>
```

> ⚠️ Ensure your Azure OpenAI resource has both a chat model (e.g. gpt-4o-mini) and embedding model (e.g. text-embedding-ada-002 deployed.

---

## ▶️ Run the Application
Start the FastAPI server:
```bash
uvicorn app:app --reload
```
Then open in your browser:

👉 http://127.0.0.1:8000/chat

---

## 💬 Using the App
1. Upload PDFs
- Drag & drop a PDF or click the upload area.
- The app automatically extracts text, chunks it, embeds it with Azure OpenAI, and stores it in ChromaDB.

2. Ask Questions
- Type questions related to the uploaded documents.
- The chatbot retrieves the most relevant chunks from ChromaDB and answers using Azure OpenAI.

3. Enjoy the Conversation
- User and assistant messages appear as chat bubbles.
- You can extend this for any assistant persona.

---

## 🧠 How It Works
1. Upload PDF → Extract text → Create embeddings (Azure OpenAI) → Store in ChromaDB
2. User query → Embed query → Retrieve relevant chunks → Provide context to Azure OpenAI
3. Azure OpenAI → Generates response grounded in document context

---

## 🧰 Requirements
- Python 3.10+
- Azure OpenAI resource with deployed models
- (Optional) Git & Virtual Environment tools

---

## 🧪 Example Queries

After uploading a travel brochure PDF:
> User: What are the destinations offered by the travel agent?

> Assistant: The travel agency offers flights to Paris, Tokyo, and Sydney with full package deals including hotels and tours.

---

## 🔧 Customization

You can easily modify:
- `settings.ASSISTANT_NAME` → change assistant persona
- `system_prompt` in `rag_chat.py` → define tone and context
- Frontend UI → add your own branding or layout

---

## 🚀 Deployment

### Run in Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Containerize (Optional)
Create a simple Dockerfile:
```bash
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Then:
```bash
docker build -t azure-rag-chatbot .
docker run -p 8000:8000 azure-rag-chatbot
```
---

## 🧑‍💻 Author
Farhan Rahman