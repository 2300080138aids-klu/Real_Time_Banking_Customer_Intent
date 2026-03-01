import numpy as np
import faiss

from app.models.embedding_model import EmbeddingModel
from app.config import FAISS_INDEX_PATH
from app.data.intent_prototypes import INTENT_PROTOTYPES


def build_faiss_index():
    embedder = EmbeddingModel()

    intent_names = list(INTENT_PROTOTYPES.keys())
    descriptions = list(INTENT_PROTOTYPES.values())

    embeddings = embedder.encode(descriptions)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)

    print("Prototype-based FAISS index built successfully.")


if __name__ == "__main__":
    build_faiss_index()