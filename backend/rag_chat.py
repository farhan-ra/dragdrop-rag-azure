from backend.config import settings
from backend.pdf_loader import pdf_collection, embed_texts
from openai import AzureOpenAI

class ChromaRAGChat:
    def __init__(self, top_k=5):
        self.top_k = top_k
        self.client = AzureOpenAI(
            api_key=settings.OPEN_AI_KEY,
            api_version="2024-05-01-preview",
            azure_endpoint=settings.OPEN_AI_ENDPOINT
        )

    def retrieve_context(self, query: str) -> str:
        query_embedding = embed_texts([query])[0]
        results = pdf_collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )
        docs = [d for batch in results["documents"] for d in batch]
        return "\n".join(docs)

    def chat(self, user_message: str, system_prompt: str = None) -> str:
        context = self.retrieve_context(user_message)
        system_prompt = system_prompt or f"You are {settings.ASSISTANT_NAME}, an AI assistant that answers based on uploaded PDFs."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {user_message}\n\nContext:\n{context}"}
        ]

        response = self.client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
