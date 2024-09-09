from vector_database import VectorDatabase
import asyncio

class ChatService:
    def __init__(self):
        self.chats = {}
        self.vector_db = VectorDatabase()

    def start_chat(self, asset_id: str) -> str:
        if not self.vector_db.collection.get(ids=[asset_id]):
            raise ValueError("Invalid asset ID")
        
        thread_id = f"chat_{len(self.chats) + 1}"
        self.chats[thread_id] = {"asset_id": asset_id, "messages": []}
        return thread_id

    async def send_message(self, thread_id: str, message: str) -> str:
        if thread_id not in self.chats:
            raise ValueError("Invalid chat thread ID")

        # Simulate agent response (query embeddings here)
        await asyncio.sleep(1)  # Simulate async processing
        response = f"Response for '{message}' using asset {self.chats[thread_id]['asset_id']}"
        
        # Store message and response
        self.chats[thread_id]["messages"].append({"user": message, "agent": response})
        return response

    def get_chat_history(self, thread_id: str):
        if thread_id not in self.chats:
            raise ValueError("Invalid chat thread ID")
        return self.chats[thread_id]["messages"]
