from sentence_transformers import CrossEncoder
from app.config import RERANKER_MODEL_NAME

class RerankerModel:
    def __init__(self):
        self.model = CrossEncoder(RERANKER_MODEL_NAME)

    def rerank(self, query, candidate_texts):
        pairs = [(query, text) for text in candidate_texts]
        return self.model.predict(pairs)