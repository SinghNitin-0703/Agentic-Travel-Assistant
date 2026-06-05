# Bharat YatraBot

A modular conversational travel assistant built with the Agno agent framework, Azure OpenAI, and SerpAPI.

## Project Structure

```text
D:/Travel Agent/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration & Environment loading
│   ├── schemas.py          # Pydantic schemas for data validation
│   ├── database.py         # SQLite memory management
│   ├── client.py           # SerpAPI HTTP client
│   ├── agent.py            # Agno Agent configuration
│   ├── chat.py             # Chat loop and execution logic
│   └── tools/              # Specialized agent tools
│       ├── __init__.py
│       ├── flights.py      # Google Flights tool
│       ├── hotels.py       # Google Hotels tool
│       ├── places.py       # Google Maps and Travel Explore tools
│       └── itinerary.py    # Itinerary builder tool
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables example
└── travel_agent.ipynb      # Original experimental notebook
```

## Setup & Running

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your API keys (Azure OpenAI and SerpAPI).
   ```bash
   cp .env.example .env
   ```

3. **Run the App:**
   Start the interactive chat in the terminal:
   ```bash
   python main.py
   ```
