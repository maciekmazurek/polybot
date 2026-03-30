# PolyBot

PolyBot is an asynchronous bot that scans Polymarket markets and looks for opportunities where the AI estimate differs from the market price.

## How the Bot Works

1. Fetches active markets from the Polymarket API.
2. For each market, fetches additional context from Tavily (news/search).
3. Sends the question plus context to GPT-4o, which returns a probability estimate.
4. Computes edge (`ai_probability - market_price`) and filters only meaningful proposals.
5. For selected opportunities, calculates a suggested bet size using Fractional Kelly.
6. Saves analyses in a local SQLite database (`data/bot_memory.db`).

## How to Run

### 1. Installation

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. `.env` Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key

# Runtime parameters
MARKETS_TO_ANALYZE=10
BANKROLL=50
```

### 3. Start

```bash
python main.py
```

After startup, the bot prints a report in the terminal and stores predictions in SQLite.

## Technologies Used

- Python 3
- `asyncio` (parallel market processing)
- `openai` (GPT-4o)
- `httpx` / `aiohttp` (asynchronous HTTP requests)
- `tavily` (context retrieval)
- `pydantic` (data models and validation)
- `aiosqlite` (local results database)
- `python-dotenv` (environment variables)