import os
import json
from typing import Dict, Any

from fastapi import FastAPI, HTTPException

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

from working_classes import *


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_TIME_OUT = int(os.getenv("OLLAMA_TIME_OUT", "120"))


api = FastAPI(title="Ollama Backend")


chat_histories: Dict[str, InMemoryChatMessageHistory] = {}


llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=1.0,
    timeout=OLLAMA_TIME_OUT,
)

prompt = ChatPromptTemplate(
    [("system","You are AI-agent helper. Yout must anwer on Russian"), 
     ("human", "{message}")])



@api.get("/health")
async def health():
    return {
        "status": "ok",
        "ollama_base_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL,
    }



@api.post("/chat", response_model=ChatResponse)
async def post_message(request: ChatRequest):
    try:
        chain = prompt | llm | StrOutputParser()
        response = await chain.ainvoke(
            {"message":request.message}
        )

        return {
            "message": response,
            "model":OLLAMA_MODEL
        }
    except:
        return {
            "message" : "Error:200",
            "model":OLLAMA_MODEL
        }


