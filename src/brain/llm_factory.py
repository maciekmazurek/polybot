import json
import os
from openai import AsyncOpenAI
from src.models.market import Market
from src.models.prediction import MarketAnalysis
from .prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class Brain:
    def __init__(self, model_name="gpt-4o"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    async def analyze_market(self, market: Market, context: str) -> MarketAnalysis:
        user_prompt = USER_PROMPT_TEMPLATE.format(
            question=market.question,
            price=market.outcomes[0].price,
            market_pct=int(market.outcomes[0].price * 100),
            context=context
        )

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2  # Lower temperature = more stable 
        )

        raw_json = response.choices[0].message.content
        analysis_data = json.loads(raw_json)
            
        return MarketAnalysis(**analysis_data)