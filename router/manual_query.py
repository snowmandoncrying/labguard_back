from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.manual_query import query_manual

router = APIRouter()

class QueryRequest(BaseModel):
    manual_id: str
    question: str
    top_k: int = 4

@router.post("/manual/query")
async def manual_query(request: QueryRequest):
    """
    저장된 매뉴얼에 대해 질문하고 답변을 받습니다.
    """
    try:
        result = await query_manual(request.manual_id, request.question, top_k=request.top_k)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 