from fastapi import FastAPI, UploadFile, File, HTTPException
from document_processing import process_document
from chat_service import ChatService
import os
import shutil

app = FastAPI()
chat_service = ChatService()

# Upload and process the document
@app.post("/api/documents/process")
async def upload_file(file: UploadFile):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        asset_id = process_document(file_location, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"asset_id": asset_id}

# Start a chat session
@app.post("/api/chat/start")
async def start_chat(asset_id: str):
    try:
        thread_id = chat_service.start_chat(asset_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"thread_id": thread_id}

# Send a message in a chat
@app.post("/api/chat/message")
async def send_message(thread_id: str, message: str):
    try:
        response = await chat_service.send_message(thread_id, message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"response": response}

# Get chat history
@app.get("/api/chat/history")
async def get_chat_history(thread_id: str):
    try:
        history = chat_service.get_chat_history(thread_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)