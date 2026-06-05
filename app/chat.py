from app.database import load_session, append_message
from app.agent import get_agent

async def chat(session_id: str, user_message: str) -> str:
    """
    Process a user message through the Bharat YatraBot agent.
    """
    session = await load_session(session_id)
    await append_message(session_id, "user", user_message)

    print(f"\n📨 User Message: {user_message}")
    print("⏳ Agent processing... (watch for 🛠️  TOOL CALLED messages below)\n")

    agent = get_agent()
    response = await agent.arun(user_message, session_id=session_id)

    response_text = response.content if response.content else "I'm sorry, I couldn't process that request."

    await append_message(session_id, "assistant", response_text)

    return response_text
