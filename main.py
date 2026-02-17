import asyncio
import os
from dotenv import load_dotenv

from src.api.polymarket_client import PolyClient
from src.api.news_provider import NewsProvider
from src.brain.llm_factory import Brain
from src.strategy.probability_engine import find_best_proposals

# Load API keys from the .env file
load_dotenv()

async def process_market(market, news_provider, brain):
    """Process a single market: fetch news, analyze, and find opportunities."""
    try:
        print(f"Analyzing: {market.question}...")
        context = await news_provider.get_context_for_question(market.question)
        analysis = await brain.analyze_market(market, context)
        proposal = find_best_proposals(market, analysis)
        
        return proposal
    except Exception as e:
        print(f"Error while processing market {market.id}: {e}")
        return None

async def main():
    # Initialize clients
    poly_client = PolyClient()
    news_provider = NewsProvider()
    brain = Brain(model_name="gpt-4o")

    print("Starting")
    
    # 1. Fetch active markets (e.g. 10 most popular)
    markets = await poly_client.get_active_markets(limit=10)
    
    if not markets:
        print("No active markets found.")
        return

    # 2. Process markets
    tasks = [process_market(m, news_provider, brain) for m in markets]
    results = await asyncio.gather(*tasks)

    # 3. Filter and display results
    opportunities = [r for r in results if r is not None]

    print("\n" + "="*50)
    print("OPPORTUNITY REPORT")
    print("="*50)

    if not opportunities:
        print("No strong opportunities meeting the criteria.")
    else:
        for opt in opportunities:
            print(f"\n  MARKET: {opt['question']}")
            print(f"    Market price: {opt['market_price']:.2f}")
            print(f"    AI estimate:  {opt['ai_probability']:.2f}")
            print(f"    EDGE: {opt['edge']*100:.1f}%")
            print(f"    Reasoning: {opt['reasoning'][:150]}...")
            print("-" * 30)

    print("\nScan completed.")

if __name__ == "__main__":
    asyncio.run(main())