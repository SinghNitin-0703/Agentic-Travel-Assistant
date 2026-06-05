import aiosqlite
import json
from datetime import datetime
from app.config import SQLITE_DB_PATH

async def init_database():
    """Create the sessions table with default values if it doesn't exist."""
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id   TEXT PRIMARY KEY,
                preferences  TEXT DEFAULT '{}',
                history      TEXT DEFAULT '[]',
                itinerary    TEXT DEFAULT '{}',
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def create_session(session_id: str) -> dict:
    """Insert a new session using database defaults, ignoring if it already exists."""
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))
        await db.commit()
        
    return {"session_id": session_id, "preferences": {}, "history": [], "itinerary": {}}

def _parse_json(data):
    """Helper to safely parse JSON strings from the database."""
    return json.loads(data) if isinstance(data, str) else data

async def load_session(session_id: str) -> dict:
    """Fetch a session by ID. Creates a new one if it doesn't exist."""
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)) as cursor:
            row = await cursor.fetchone()

    if not row:
        return await create_session(session_id)

    return {
        "session_id": row["session_id"],
        "preferences": _parse_json(row["preferences"]),
        "history": _parse_json(row["history"]),
        "itinerary": _parse_json(row["itinerary"]),
    }

async def save_session(session_id: str, data: dict) -> None:
    """Update an existing session with new data."""
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("""
            UPDATE sessions
            SET preferences = ?, history = ?, itinerary = ?, updated_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
        """, (
            json.dumps(data.get("preferences", {})),
            json.dumps(data.get("history", [])),
            json.dumps(data.get("itinerary", {})),
            session_id
        ))
        await db.commit()

async def append_message(session_id: str, role: str, content: str) -> None:
    """Helper to quickly add a new chat message to a session's history."""
    session = await load_session(session_id)
    session["history"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })
    await save_session(session_id, session)
