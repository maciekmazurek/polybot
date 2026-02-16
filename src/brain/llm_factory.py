import openai
import os
from src.models.market import Market
from src.models.prediction import MarketAnalysis

class Brain:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def analyze_market(self, market: Market, context: str) -> MarketAnalysis:
        prompt = f"""
        Analizujesz rynek predykcyjny: "{market.question}"
        Oto najnowsze informacje: {context}
        
        Na podstawie faktów, oszacuj prawdopodobieństwo wyniku 'TAK' (YES).
        Zwróć odpowiedź w formacie JSON z polami: 
        probability (float 0-1), reasoning (str), confidence (float 0-1).
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        return MarketAnalysis.model_validate_json(response.choices[0].message.content)