import asyncio
from src.api.polymarket_client import PolyClient
from src.api.news_provider import NewsProvider
from src.brain.llm_factory import Brain


async def main() -> None:
    poly_client = PolyClient()
    news_provider = NewsProvider()
    brain = Brain()

    active_markets = await poly_client.get_active_markets()
    sample_market = active_markets[0]

    context = await news_provider.get_context_for_question(question=sample_market.question)
    market_analysys = await brain.analyze_market(sample_market, context)

    print(f"Propability: {market_analysys.probability}")
    print(f"Reasoning: {market_analysys.reasoning}")
    print(f"Confidence: {market_analysys.confidence}")


if __name__ == "__main__":
    asyncio.run(main())