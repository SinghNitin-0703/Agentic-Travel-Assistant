import aiosqlite
import json
from datetime import datetime
from app.config import SQLITE_DB_PATH

async def init_database():
    """Create the sessions table if it doesn't exist."""
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id   TEXT PRIMARY KEY,
                user_id      TEXT DEFAULT 'default_user',
                preferences  TEXT DEFAULT '{}',
                history      TEXT DEFAULT '[]',
                itinerary    TEXT DEFAULT '{}',
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def create_session(session_id: str, user_id: str = "default_user") -> dict:
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO sessions (session_id, user_id, preferences, history, itinerary)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_id, json.dumps({}), json.dumps([]), json.dumps({})))
        await db.commit()
    return {"session_id": session_id, "user_id": user_id, "preferences": {}, "history": [], "itinerary": {}}

async def load_session(session_id: str) -> dict:
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM sessions WHERE session_id = ?;", (session_id,)) as cursor:
            row = await cursor.fetchone()

    if row is None:
        return await create_session(session_id)

    return {
        "session_id": row["session_id"],
        "user_id": row["user_id"],
        "preferences": json.loads(row["preferences"]) if isinstance(row["preferences"], str) else row["preferences"],
        "history": json.loads(row["history"]) if isinstance(row["history"], str) else row["history"],
        "itinerary": json.loads(row["itinerary"]) if isinstance(row["itinerary"], str) else row["itinerary"],
    }

async def save_session(session_id: str, data: dict) -> None:
    async with aiosqlite.connect(SQLITE_DB_PATH) as db:
        await db.execute("""
            UPDATE sessions
            SET preferences = ?,
                history     = ?,
                itinerary   = ?,
                updated_at  = CURRENT_TIMESTAMP
            WHERE session_id = ?;
        """, (
            json.dumps(data.get("preferences", {})),
            json.dumps(data.get("history", [])),
            json.dumps(data.get("itinerary", {})),
            session_id,
        ))
        await db.commit()

async def update_preferences(session_id: str, prefs: dict) -> None:
    session = await load_session(session_id)
    session["preferences"].update(prefs)
    await save_session(session_id, session)

async def append_message(session_id: str, role: str, content: str) -> None:
    session = await load_session(session_id)
    session["history"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })
    await save_session(session_id, session)
