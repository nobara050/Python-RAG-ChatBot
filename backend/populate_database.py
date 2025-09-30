from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.embedding import get_embedding_function
from langchain.schema.document import Document
from config import CHROMA_PATH, DATA_PATH
from langchain_chroma import Chroma
import argparse
import shutil
import os
# ======================================================
# CHẠY BẰNG PYTHON: python populate_database.py --reset
# --reset: xóa db trước khi chạy (optional)
# ======================================================

# 1. LOAD DOC TỪ THƯ MỤC
def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

# 2. TÁCH DOC THÀNH CÁC CHUNK
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
        separators=[
            "\n\n", 
            "\n",       
            ".", "?", "!", ";", ":",  
            " ",       
            ""          
        ]
    )
    return text_splitter.split_documents(documents)

# 3. THÊM CHUNK VÀO CHROMA DB
def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )

    # Tính ID cho từng chunk
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Lấy ID hiện có trong DB
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Lọc ra các chunk mới chưa có trong DB
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    
    else:
        print("No new documents to add")
    
    print("Completed ✅")

# ===========================================================================
# Tính ID cho từng chunk
def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

def main():
    # KIỂM TRA CỜ ĐỂ XÓA DB
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("Clearing Database")
        clear_database()

    # CHẠY TOÀN BỘ LUỒNG
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
