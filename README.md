# 🇮🇳 Bharat YatraBot

Bharat YatraBot is a friendly, knowledgeable India-centric conversational travel assistant. Built with the **Agno** agent framework, **Azure OpenAI**, and **SerpAPI**, it specializes in helping users plan their travels across India—whether it's exploring heritage sites, booking flights and hotels, or building complete travel itineraries.

---

## 🌟 Features

- **Conversational Travel Assistant**: Ask natural language questions about travel in India.
- **Flight & Hotel Search**: Discover flights and hotels with live data, presenting prices in INR (₹).
- **Places & Destinations Exploration**: Find tourist attractions, beaches, hill stations, and cultural experiences.
- **Itinerary Building**: Generate customized travel itineraries based on selected flights, hotels, and places of interest.
- **Context Aware**: Remembers user preferences (budget, cabin class, preferred airlines) and previous interactions.
- **RESTful API**: Fast and robust API built with FastAPI for interacting with the travel agent.

---

## 🏗️ Architecture & Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) for the web API backend.
- **Agent Framework**: [Agno](https://github.com/agno/agno) for orchestrating the AI agent, memory, and tools.
- **LLM Provider**: **Azure OpenAI** (e.g., `gpt-4o-mini`).
- **Search Provider**: **SerpAPI** (Google Flights, Google Hotels, Google Maps).
- **Database**: **SQLite** for persisting agent sessions and chat history.

---

## 📂 Project Structure

```text
D:/Travel Agent/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuration & Environment loading
│   ├── schemas.py          # Pydantic schemas for data validation
│   ├── database.py         # SQLite memory management
│   ├── client.py           # SerpAPI HTTP client wrappers
│   ├── agent.py            # Agno Agent configuration and instructions
│   ├── chat.py             # Chat execution logic
│   └── tools/              # Specialized agent tools
│       ├── __init__.py
│       ├── flights.py      # Google Flights tool
│       ├── hotels.py       # Google Hotels tool
│       ├── places.py       # Google Maps and Travel Explore tools
│       └── itinerary.py    # Itinerary builder tool
├── main.py                 # Main FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables example
└── travel_agent.ipynb      # Original experimental notebook
```

---

## 🚀 Setup & Installation

**1. Clone the repository and navigate to the project directory:**
```bash
git clone <repository_url>
cd "Travel Agent"
```

**2. Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables:**
Copy the `.env.example` file to `.env` and populate it with your actual API keys.
```bash
cp .env.example .env
```
Ensure the following variables are configured in `.env`:
- `AZURE_OPENAI_DEPLOYMENT`: Your Azure OpenAI deployment name (e.g., `gpt-4o-mini`).
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key.
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint.
- `AZURE_OPENAI_API_VERSION`: The API version (e.g., `2024-12-01-preview`).
- `SERPAPI_API_KEY`: Your SerpAPI key for live web data.
- `SQLITE_DB_PATH`: Path for the SQLite database (default: `travel_agent.db`).

---

## 💻 Running the Application

Start the FastAPI application using Uvicorn:
```bash
python main.py
```
The server will start at `http://0.0.0.0:8000`. You can also view the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

---

## 🔌 API Endpoints

### 1. Create a New Session
Initializes a new chat session and returns a unique `session_id`.

**Request:**
```http
GET /session/new
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0"
}
```

### 2. Chat
Send a message to the Bharat YatraBot and get a response.

**Request:**
```http
POST /chat
Content-Type: application/json

{
  "session_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "message": "Plan a 3-day trip to Jaipur from Delhi."
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "response": "Here is a wonderful 3-day itinerary for your trip to Jaipur..."
}
```

---

## 🤖 Agent Capabilities

Bharat YatraBot is equipped with the following toolsets:
- **Flight Search:** Converts city names to IATA codes (e.g., DEL, BOM, BLR) and fetches real-time flight options.
- **Hotel Search:** Finds accommodations and detailed hotel information.
- **Destination Exploration:** Suggests cheap getaways and explores attractions based on Google Maps data.
- **Itinerary Generation:** Compiles a comprehensive itinerary integrating all user preferences and selected bookings.

*Namaste! Enjoy building and traveling with Bharat YatraBot.*
