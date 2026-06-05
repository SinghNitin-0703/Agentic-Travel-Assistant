import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4-mini")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your-azure-api-key-here")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-endpoint.cognitiveservices.azure.com/")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

# SerpAPI Configuration
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "your-serpapi-key-here")
SERPAPI_BASE_URL = os.getenv("SERPAPI_BASE_URL", "https://serpapi.com/search.json")

# SQLite Configuration
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "travel_agent.db")

# Also set as env vars for libraries that need them
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
os.environ["AZURE_OPENAI_DEPLOYMENT"] = AZURE_OPENAI_DEPLOYMENT
os.environ["AZURE_OPENAI_API_VERSION"] = AZURE_OPENAI_API_VERSION
