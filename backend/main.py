from fastapi import FastAPI

# Import routers
from api.getChunk import router as getChunk_router
from api.postQuery import router as postQuery_router
from api.postSpeech import router as postSpeech_router

app = FastAPI(title="Chatbot RAG API")

# ROUTER
app.include_router(getChunk_router)
app.include_router(postQuery_router)
app.include_router(postSpeech_router)

# HOME
@app.get("/")
def root():
    return {"message": "API is running"}