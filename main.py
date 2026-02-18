import asyncio
import os
from dotenv import load_dotenv

from src.api.polymarket_client import PolyClient
from src.api.news_provider import NewsProvider
from src.brain.llm_factory import Brain
from src.strategy.probability_engine import find_best_proposals
from src.utils.database import DatabaseManager
from src.strategy.kelly_criterion import KellyCalculator

# Load API keys from the .env file
load_dotenv()

async def process_market(market, news_provider, brain, db_manager):
    """Process a single market: fetch news, analyze, and find opportunities."""
    try:
        print(f"Analyzing: {market.question}...")
        context = await news_provider.get_context_for_question(market.question)
        analysis = await brain.analyze_market(market, context)
        await db_manager.save_prediction(market, analysis)
        proposal = find_best_proposals(market, analysis)
        
        return proposal
    except Exception as e:
        print(f"Error while processing market {market.id}: {e}")
        return None

async def main():
    # Wallet config
    MY_BANKROLL = 50 # USDC
    kelly = KellyCalculator()
    
    # Initialize clients
    db_manager = DatabaseManager()
    await db_manager.initialize()
    poly_client = PolyClient()
    news_provider = NewsProvider()
    brain = Brain(model_name="gpt-4o")

    print("Starting the scan.\n")
    
    # 1. Fetch active markets (e.g. 10 most popular)
    markets = await poly_client.get_active_markets(limit=15)
    
    if not markets:
        print("No active markets found.")
        return

    # 2. Process markets
    tasks = [process_market(m, news_provider, brain, db_manager) for m in markets]
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
            suggested_bet = kelly.calculate_bet_amount(
                bankroll=MY_BANKROLL, 
                price=opt['market_price'], 
                estimated_prob=opt['ai_probability']
                )
            
            print(f"\n  MARKET: {opt['question']}")
            print(f"    Market price: {opt['market_price']:.2f}")
            print(f"    AI estimate:  {opt['ai_probability']:.2f}")
            print(f"    EDGE: {opt['edge']*100:.1f}%")
            print(f"    Suggested bet: {suggested_bet}")
            print(f"    Reasoning: {opt['reasoning']}...")
            print("\n" + "-" * 30)

    print("\nScan completed.")

if __name__ == "__main__":
    asyncio.run(main())