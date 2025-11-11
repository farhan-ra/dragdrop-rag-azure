from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.rag_chat import router as chat_router
from frontend.frontend import router as frontend_router

app = FastAPI(title="Margie’s Travel Assistant", version="1.0")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include routers
app.include_router(chat_router)
app.include_router(frontend_router)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "RAG Chat"}
