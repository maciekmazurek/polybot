import httpx
import json
import logging
from typing import List
from src.models.market import Market, MarketOutcome

logger = logging.getLogger(__name__)

class PolyClient:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
        self.timeout = httpx.Timeout(10.0)

    async def get_active_markets(self, limit: int = 20) -> List[Market]:
        """Fetch a list of active markets that meet liquidity criteria."""
        query_params = {
            "active": "true",
            "closed": "false",
            "limit": limit,
            "order": "volume",
            "ascending": "false"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/markets", params=query_params)
                response.raise_for_status()
                raw_data = response.json()
                
                return self._transform_data(raw_data)
            except Exception as e:
                logger.error(f"Error while fetching data from Polymarket: {e}")
                return []

    def _transform_data(self, raw_data: List[dict]) -> List[Market]:
        """Transform raw JSON into a list of `Market` objects."""
        refined_markets = []
        for item in raw_data:
            try:
                # Map API payload fields to our local model
                market = Market(
                    id=item.get("id"),
                    question=item.get("question"),
                    description=item.get("description"),
                    category=item.get("groupItemTitle", "General"),
                    end_date=item.get("endDate"),
                    volume=float(item.get("volume", 0)),
                    outcomes=[
                        MarketOutcome(
                            name=name, 
                            price=float(price)
                        )
                        for (name, price) in zip(json.loads(item.get("outcomes")), json.loads(item.get("outcomePrices")))
                    ]
                )
                refined_markets.append(market)
            except Exception as e:
                logger.warning(f"Skipped market {item.get('id')} due to a mapping error: {e}")
                continue
        
        return refined_markets