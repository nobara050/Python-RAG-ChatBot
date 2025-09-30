from langchain.prompts import ChatPromptTemplate
from services.embedding import get_embedding_function
from config import PROMPT_TEMPLATE_PATH, CHROMA_PATH
from langchain_chroma import Chroma
from services.llm import llm_prompt
from pathlib import Path

# PROMPT TEMPLATE
PROMPT_TEMPLATE = Path(PROMPT_TEMPLATE_PATH).read_text(encoding="utf-8")

# LUỒNG RAG LẤY CÂU TRẢ LỜI
def query_rag(query_text: str):
    # Khởi tạo ChromaDB với embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 1. Tìm chunk phù hợp
    results = db.similarity_search_with_score(query_text, k=15)

    # Lấy nội dung top chunks
    top_chunks = [doc.page_content for doc, _ in results]
    context_text = "\n\n---\n\n".join(top_chunks)

    # 2. Tạo prompt hoàn chỉnh
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # 3. Gọi LLM trả lời
    response_text = llm_prompt(prompt)

    # Lấy nguồn tài liệu
    sources = [
        {
            "source": doc.metadata.get("source", None),
            "page": doc.metadata.get("page", None),
            "id": doc.metadata.get("id", None)
        }
        for doc, _ in results
    ]

    return {
        "prompt": prompt,
        "response": response_text,
        "sources": sources
    }

