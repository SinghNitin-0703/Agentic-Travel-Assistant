import httpx
from app.config import SERPAPI_BASE_URL, SERPAPI_API_KEY

async def serpapi_request(params: dict) -> dict:
    """Make an async request to SerpAPI with common defaults."""
    params["api_key"] = SERPAPI_API_KEY
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.get(SERPAPI_BASE_URL, params=params)
    resp.raise_for_status()
    return resp.json()
