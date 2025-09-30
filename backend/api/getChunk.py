from services.embedding import get_embedding_function
from langchain_chroma import Chroma
from config import CHROMA_PATH
from fastapi import APIRouter
import traceback

# ROUTER TRẢ VỀ CÁC CHUNK
router = APIRouter(tags=["Get Chunks"])
@router.get("/chunks")
def get_chunks():
    try:
        embedding_function = get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function
        )
        data = db._collection.get(include=["documents", "metadatas"])

        chunks = []
        for i in range(len(data["ids"])):
            chunks.append({
                "id": data["ids"][i],
                "document": data["documents"][i],
                "metadata": data["metadatas"][i]
            })

        return {"chunks": chunks}
    except Exception:
        error_message = traceback.format_exc()
        print("Error:", error_message)
        return {"error": "Failed to fetch chunks."}