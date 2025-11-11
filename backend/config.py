import os
from dotenv import load_dotenv

load_dotenv()

# Central place for config and environment loading.

class Settings:
    OPEN_AI_ENDPOINT = os.getenv("OPEN_AI_ENDPOINT")
    OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
    CHAT_MODEL = os.getenv("CHAT_MODEL")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    SEARCH_URL = os.getenv("SEARCH_ENDPOINT")
    SEARCH_KEY = os.getenv("SEARCH_KEY")
    INDEX_NAME = os.getenv("INDEX_NAME")

settings = Settings()
