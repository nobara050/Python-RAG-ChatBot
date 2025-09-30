from config import GOOGLE_API_KEY, LLM_MODEL
from google import genai

# HÀM GỌI LLM - DÙNG GOOGLE GENERATIVE AI
def llm_prompt(prompt: str) -> str:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model=LLM_MODEL, 
        contents=prompt
    )
    return response.text