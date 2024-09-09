import chromadb
from chromadb.config import Settings

class VectorDatabase:
    def __init__(self):
        # Initialize ChromaDB client with default settings
        self.client = chromadb.Client(Settings())
        self.collection = self.client.get_or_create_collection("document_embeddings")

    def store_embedding(self, asset_id: str, embedding: list, metadata: dict):
        self.collection.add(
            documents=[embedding],
            metadatas=[metadata],
            ids=[asset_id]
        )

    def query_embeddings(self, embedding: list, top_k: int = 1):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
