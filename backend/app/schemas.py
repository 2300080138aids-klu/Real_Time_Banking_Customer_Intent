from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    confidence: float
    candidates: List[str]
    escalate: bool