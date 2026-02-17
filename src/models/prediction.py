from pydantic import BaseModel, Field
from typing import List

class MarketAnalysis(BaseModel):
    probability: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    key_factors: List[str] = Field(default_factory=list)
    counter_argument: str
    reasoning: str