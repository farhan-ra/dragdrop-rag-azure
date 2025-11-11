import os
from pypdf import PdfReader
import chromadb
from backend.config import settings
from openai import AzureOpenAI

# Initialize Azure OpenAI client
azure_client = AzureOpenAI(
    api_key=settings.OPEN_AI_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=settings.OPEN_AI_ENDPOINT
)

# Initialize Chroma
chroma_client = chromadb.Client()
COLLECTION_NAME = "pdf_collection"

if COLLECTION_NAME in [c.name for c in chroma_client.list_collections()]:
    pdf_collection = chroma_client.get_collection(name=COLLECTION_NAME)
else:
    pdf_collection = chroma_client.create_collection(name=COLLECTION_NAME)


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from each page of a PDF."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generates embeddings using Azure OpenAI."""
    response = azure_client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]


def add_pdf_to_index(file_path: str, file_name: str):
    """Splits PDF into chunks and stores in Chroma with embeddings."""
    text = extract_text_from_pdf(file_path)
    chunk_size = 1000  # characters per chunk
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    embeddings = embed_texts(chunks)

    pdf_collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": file_name}] * len(chunks),
        ids=[f"{file_name}_{i}" for i in range(len(chunks))]
    )

    return len(chunks)
