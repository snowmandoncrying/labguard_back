from fastapi import FastAPI
from fastapi_utilities import repeat_every
from app.api import manual_rag_router, manual_query_router, risk_analysis_router, manual_router
from app.api.voice_chat_router import router as voice_chat_router
from app.api.agent_chat_ws_router import router as agent_chat_ws_router
from app.api.manual_analyze_router import router as manual_analyze_router
from app.api.experiment_analysis_router import router as experiment_analysis_router
from app.api.user import router as user_router
from app.services.agent_chat_service import flush_all_chat_logs
from app.db import create_tables
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
@repeat_every(seconds=60, wait_first=True)
async def periodic_flush_chat_logs():
    """
    Periodically flush chat logs from Redis to the database.
    Waits for the first 60 seconds before running.
    """
    flush_all_chat_logs()

# @app.on_event("startup")
# def on_startup():
#     """
#     On application startup, import create_tables module to trigger table creation.
#     """
#     print("Initializing database tables...")
#     pass # create_tables 모듈을 import 하는 것만으로 테이블이 생성됩니다.

app.include_router(manual_rag_router.router)
app.include_router(manual_query_router.router)
app.include_router(risk_analysis_router.router)
app.include_router(voice_chat_router)
app.include_router(agent_chat_ws_router) 
app.include_router(manual_analyze_router)
app.include_router(experiment_analysis_router) 
app.include_router(user_router)
app.include_router(manual_router.router)