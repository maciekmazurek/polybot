import aiosqlite
from datetime import datetime
from src.models.market import Market
from src.models.prediction import MarketAnalysis

class DatabaseManager:
    def __init__(self, db_path="data/bot_memory.db"):
        self.db_path = db_path

    async def initialize(self):
        """Tworzy tabele, jeśli jeszcze nie istnieją."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    market_id TEXT,
                    question TEXT,
                    market_price REAL,
                    ai_probability REAL,
                    confidence REAL,
                    edge REAL,
                    reasoning TEXT,
                    created_at TIMESTAMP,
                    final_result TEXT DEFAULT NULL -- 'YES', 'NO' lub NULL jeśli trwa
                )
            """)
            await db.commit()

    async def save_prediction(self, market: Market, analysis: MarketAnalysis):
        """Zapisuje nową analizę do bazy."""
        edge = analysis.probability - market.outcomes[0].price
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO predictions 
                   (market_id, question, market_price, ai_probability, confidence, edge, reasoning, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    market.id,
                    market.question,
                    market.outcomes[0].price,
                    analysis.probability,
                    analysis.confidence_score,
                    edge,
                    analysis.reasoning,
                    datetime.now().isoformat()
                )
            )
            await db.commit()