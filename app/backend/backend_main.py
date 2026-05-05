import os
import json
from typing import Dict, Any

from fastapi import FastAPI, HTTPException

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

from working_classes import ChatRequest, ChatResponse, GuardDecision


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TIME_OUT = int(os.getenv("OLLAMA_TIME_OUT", "20"))


api = FastAPI(title="Ollama Backend")


chat_histories: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()

    return chat_histories[session_id]


llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=1.0,
    timeout=OLLAMA_TIME_OUT,
)


guardllm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.0,
    timeout=OLLAMA_TIME_OUT,
    format="json",
)



@api.get("/health")
async def health():
    return {
        "status": "ok",
        "ollama_base_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL,
    }



@api.post("/chat", response_model=ChatResponse)
async def post_message(request: ChatRequest):
    


@api.get("/chat/{session_id}/memory")
async def get_memory(session_id: str):
    history = get_session_history(session_id)

    return {
        "session_id": session_id,
        "messages": [
            {
                "type": message.type,
                "content": message.content,
            }
            for message in history.messages
        ]
    }