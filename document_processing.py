import os
import openai
from fastapi import HTTPException
from vector_database import VectorDatabase
from PyPDF2 import PdfReader
import docx

# Initialize ChromaDB client
vector_db = VectorDatabase()

# Read the content of the file
def read_file_content(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".txt":
        with open(file_path, "r") as file:
            return file.read()
    elif file_ext == ".pdf":
        return read_pdf_content(file_path)
    elif file_ext == ".doc":
        return read_doc_content(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

# Read PDF content
def read_pdf_content(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Read Word document content
def read_doc_content(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Create embeddings using OpenAI
def create_embeddings(content: str) -> list:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(
        input=[content], model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Process document, create embeddings and store them
def process_document(file_path: str, file_name: str) -> str:
    content = read_file_content(file_path)
    embedding = create_embeddings(content)
    
    # Assign a unique asset ID
    asset_id = f"asset_{hash(file_name)}"
    
    # Store in vector database
    vector_db.store_embedding(asset_id, embedding, {"file_name": file_name})
    
    return asset_id