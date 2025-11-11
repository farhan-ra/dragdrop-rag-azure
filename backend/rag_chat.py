from fastapi import APIRouter
from pydantic import BaseModel
from openai import AzureOpenAI
from backend.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=settings.OPEN_AI_ENDPOINT,
    api_key=settings.OPEN_AI_KEY
)

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(req: ChatRequest):
    """Handles chat messages and performs RAG search."""
    user_input = req.message.strip()
    if not user_input:
        return {"reply": "Please enter a valid message.", "sources": []}

    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": settings.SEARCH_URL,
                    "index_name": settings.INDEX_NAME,
                    "authentication": {
                        "type": "api_key",
                        "key": settings.SEARCH_KEY
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": settings.EMBEDDING_MODEL
                    },
                }
            }
        ]
    }

    messages = [
        {
            "role": "system",
            "content": "You are a Parks Victoria assistant that provides information on park planning and development."
        },
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=messages,
            extra_body=rag_params
        )
        msg = response.choices[0].message
        reply = msg.content or "No response generated."
        citations = []
        if hasattr(msg, "context") and msg.context:
            citations = msg.context.get("citations", [])
        return {"reply": reply, "sources": citations}

    except Exception as e:
        return {"reply": f"Error: {str(e)}", "sources": []}
