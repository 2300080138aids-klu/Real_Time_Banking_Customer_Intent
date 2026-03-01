import faiss
from app.config import FAISS_INDEX_PATH, TOP_K

class FAISSRetriever:
    def __init__(self):
        self.index = faiss.read_index(FAISS_INDEX_PATH)

    def search(self, query_embedding):
        distances, indices = self.index.search(query_embedding, TOP_K)
        return distances[0], indices[0]