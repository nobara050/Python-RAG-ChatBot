from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY, EMBEDDING_MODEL

# HÀM EMBEDDING - DÙNG GOOGLE GENERATIVE AI
def get_embedding_function():
    return GoogleGenerativeAIEmbeddings(
        model= EMBEDDING_MODEL, 
        google_api_key=GOOGLE_API_KEY,
        transport="grpc" 
    )

# # HÀM EMBEDDING - DÙNG HUGGINGFACE

# from langchain_huggingface import HuggingFaceEmbeddings
# def get_embedding_function():
#     return HuggingFaceEmbeddings(
#         model_name="AITeamVN/Vietnamese_Embedding_v2"
#     )