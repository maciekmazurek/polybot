import asyncio
from src.api.polymarket_client import PolyClient
from src.api.news_provider import NewsProvider
from src.brain.llm_factory import Brain
from src.strategy.probability_engine import find_best_proposals


async def main() -> None:
    poly_client = PolyClient()
    news_provider = NewsProvider()
    brain = Brain()

    active_markets = await poly_client.get_active_markets()
    proposals = []

    for market in active_markets:
        context = await news_provider.get_context_for_question(question=market.question)
        market_analysys = await brain.analyze_market(market, context)
        proposal = find_best_proposals(market, market_analysys)
        if proposal is not None:
            proposals.append(proposal)
        
    sorted(proposals, key=lambda x: x["edge"])
    

if __name__ == "__main__":
    asyncio.run(main())