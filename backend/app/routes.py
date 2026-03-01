from pydantic import BaseModel
from fastapi import APIRouter
from app.models.intent_pipeline import IntentPipeline

router = APIRouter(tags=["Intent Detection Engine"])

pipeline = IntentPipeline()


class QueryRequest(BaseModel):
    query: str


class PredictionResponse(BaseModel):
    intent: str
    confidence: float
    risk_level: str
    handling_stage: str


@router.post("/predict", response_model=PredictionResponse)
def predict(request: QueryRequest):
    return pipeline.predict(request.query)