import httpx
import os


class NewsProvider:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.timeout = httpx.Timeout(10.0)

    async def get_context_for_question(self, question: str) -> str:
        """Fetches the most recent facts related to a market question."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": question,
                    "search_depth": "advanced",
                    "max_results": 5
                }
            )
            data = response.json()
            # Combine results into a single text block
            context = "\n".join([result['content'] for result in data.get('results', [])])
            return context