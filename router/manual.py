from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from service.manual_analyzer import analyze_manual_file

router = APIRouter()

@router.post("/analyze/manual")
async def analyze_manual(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    try:
        summary = await analyze_manual_file(file)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 