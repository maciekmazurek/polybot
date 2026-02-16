import asyncio
from src.api.polymarket_client import PolyClient
from src.api.news_provider import NewsProvider


async def main() -> None:
    poly_client = PolyClient()
    news_provider = NewsProvider()

    active_markets = await poly_client.get_active_markets()
    sample_question = active_markets[0].question
    question_context = await news_provider.get_context_for_question(question=sample_question)

    print(question_context)


if __name__ == "__main__":
    asyncio.run(main())