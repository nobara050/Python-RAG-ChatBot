from dotenv import load_dotenv
import os

load_dotenv()

# API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# PATHS
CHROMA_PATH = os.getenv("CHROMA_PATH")
DATA_PATH = os.getenv("DATA_PATH")

# MODEL
LLM_MODEL = os.getenv("LLM_MODEL") 
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# PROMPT
PROMPT_TEMPLATE_PATH = os.getenv("PROMPT_TEMPLATE_PATH")