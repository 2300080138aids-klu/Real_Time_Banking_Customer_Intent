import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data")
TRAIN_PATH = os.path.join(DATA_PATH, "train.csv")
FAISS_INDEX_PATH = os.path.join(DATA_PATH, "faiss.index")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

TOP_K = 5
DOMAIN_SIMILARITY_THRESHOLD = 0.40
CONFIDENCE_THRESHOLD = 0.85