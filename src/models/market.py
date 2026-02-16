from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MarketOutcome(BaseModel):
    """Represents a single outcome (e.g., 'YES' or 'NO') and its price."""
    name: str
    price: float

class Market(BaseModel):
    """Primary market model for Polymarket."""
    id: str
    question: str
    description: Optional[str] = None
    category: str
    end_date: Optional[datetime] = None
    outcomes: List[MarketOutcome]
    volume: float = 0.0

    @property
    def price_diff(self) -> float:
        """Difference between outcome prices."""
        if len(self.outcomes) >= 2:
            return abs(self.outcomes[0].price - self.outcomes[1].price)
        return 0.0