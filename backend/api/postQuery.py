from services.rag import query_rag
from pydantic import BaseModel
from fastapi import APIRouter
import traceback

class QueryRequest(BaseModel):
    query_text: str

# # ROUTER TRẢ VỀ CÂU TRẢ LỜI
router = APIRouter(tags=["Get Answer For Query"])
@router.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        result = query_rag(request.query_text)
        return result
    except Exception:
        error_message = traceback.format_exc()
        print("Error:", error_message)
        return {"error": "An error occurred while processing your request."}