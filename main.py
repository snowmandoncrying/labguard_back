from fastapi import FastAPI
from router import manual_rag, manual_query, risk_analysis_router
from router.chat_ws_router import router as chat_ws_router
from router.voice_chat_router import router as voice_chat_router

app = FastAPI()

app.include_router(manual_rag.router)
app.include_router(manual_query.router)
app.include_router(risk_analysis_router.router)
app.include_router(chat_ws_router)
app.include_router(voice_chat_router) 