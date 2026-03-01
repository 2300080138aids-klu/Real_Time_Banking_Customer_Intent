import numpy as np

from app.models.embedding_model import EmbeddingModel
from app.models.reranker_model import RerankerModel
from app.retrieval.faiss_index import FAISSRetriever
from app.config import DOMAIN_SIMILARITY_THRESHOLD
from app.utils.preprocessing import clean_text
from app.data.intent_prototypes import INTENT_PROTOTYPES


# ---------------- RISK CLASSIFICATION ----------------

CRITICAL_INTENTS = {
    "lost_or_stolen_card",
    "compromised_card",
    "lost_or_stolen_phone"
}

HIGH_RISK_INTENTS = {
    "transaction_charged_twice",
    "refund_not_showing_up",
    "receiving_money",
    "transfer_not_received_by_recipient",
    "declined_transfer",
    "extra_charge_on_statement"
}


class IntentPipeline:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.retriever = FAISSRetriever()
        self.reranker = RerankerModel()

        self.intent_names = list(INTENT_PROTOTYPES.keys())
        self.intent_descriptions = list(INTENT_PROTOTYPES.values())

    def classify_risk(self, intent: str, confidence: float):

        if intent in CRITICAL_INTENTS:
            return "CRITICAL", "HUMAN_IMMEDIATE"

        elif intent in HIGH_RISK_INTENTS:
            return "HIGH_RISK", "AI_TRIAGE_THEN_HUMAN"

        elif confidence < 0.40:
            return "UNCERTAIN", "HUMAN_UNCERTAIN"

        else:
            return "LOW_RISK", "AI_SELF_SERVICE"

    def predict(self, query: str):

        query = clean_text(query)
        query_embedding = self.embedder.encode([query])

        # -------- Domain Detection --------
        distances, indices = self.retriever.search(query_embedding)
        domain_score = float(distances[0])

        if domain_score < DOMAIN_SIMILARITY_THRESHOLD:
            return {
                "intent": "NO_INFORMATION_AVAILABLE",
                "confidence": 0.0,
                "risk_level": "OUT_OF_DOMAIN",
                "handling_stage": "NO_ACTION"
            }

        candidate_intents = [self.intent_names[i] for i in indices]
        candidate_descriptions = [self.intent_descriptions[i] for i in indices]

        # -------- Reranking --------
        rerank_scores = self.reranker.rerank(query, candidate_descriptions)
        rerank_scores = np.array(rerank_scores)

        # Softmax probability
        exp_scores = np.exp(rerank_scores)
        probabilities = exp_scores / np.sum(exp_scores)

        best_idx = int(np.argmax(probabilities))
        best_intent = candidate_intents[best_idx]
        confidence = float(probabilities[best_idx])

        # -------- Risk Classification --------
        risk_level, handling_stage = self.classify_risk(best_intent, confidence)

        return {
            "intent": best_intent,
            "confidence": confidence,
            "risk_level": risk_level,
            "handling_stage": handling_stage
        }