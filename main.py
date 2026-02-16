import asyncio
from src.api.polymarket_client import PolyClient


async def main() -> None:
    client = PolyClient()
    active_markets = await client.get_active_markets()

    for market in active_markets:
        print(market.description)


if __name__ == "__main__":
    asyncio.run(main())