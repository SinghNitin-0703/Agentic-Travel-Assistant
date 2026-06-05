from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import uvicorn
from contextlib import asynccontextmanager

from app.database import init_database
from app.chat import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Async Database...")
    await init_database()
    yield
    print("Shutting down...")

app = FastAPI(title="Bharat YatraBot API", lifespan=lifespan)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Process chat asynchronously
    response_text = await chat(request.session_id, request.message)
    
    return ChatResponse(
        session_id=request.session_id,
        response=response_text
    )

@app.get("/session/new")
async def create_new_session():
    return {"session_id": str(uuid.uuid4())}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
