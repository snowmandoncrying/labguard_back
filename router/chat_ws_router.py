from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from service.chat_service import rag_chat_answer
from typing import List, Dict
import asyncio

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket 기반 RAG 챗봇 (친근하고 친구처럼, 문서에 있는 내용만 답변)
    - manual_id, question을 받아 벡터DB+LLM로 답변
    - 답변은 항상 친근하고 자연스럽게, 문서에 없는 내용은 "문서에서 확인할 수 없습니다."로 응답
    - 세션별로 history를 메모리에 저장해 멀티턴 대화 지원
    """
    await websocket.accept()
    history: List[Dict[str, str]] = []  # 세션별 대화 히스토리
    try:
        while True:
            data = await websocket.receive_json()
            # 예시: {"manual_id": "...", "question": "..."}
            manual_id = data.get("manual_id")
            question = data.get("question")
            if not manual_id or not question:
                await websocket.send_json({"error": "manual_id와 question을 모두 입력해야 합니다."})
                continue
            # RAG 파이프라인 호출 (친근한 말투, 문서 기반 답변)
            answer = await rag_chat_answer(manual_id, question, history)
            # 대화 히스토리 저장
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})
            # 답변 전송
            await websocket.send_json({
                "question": question,
                "answer": answer,
                "history": history[-10:]  # 최근 10턴만 반환
            })
    except WebSocketDisconnect:
        print("WebSocket 연결 종료")
    except Exception as e:
        await websocket.send_json({"error": f"서버 오류: {str(e)}"})

# 예시 메시지 포맷
"""
클라이언트 → 서버:
{
    "manual_id": "abc-123-xyz",
    "question": "화학물질 취급 시 주의사항은?"
}

서버 → 클라이언트:
{
    "question": "화학물질 취급 시 주의사항은?",
    "answer": "... (친근한 말투, 문서 기반 답변)",
    "history": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
}
""" 