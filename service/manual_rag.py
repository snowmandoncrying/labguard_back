import os
import uuid
import time
import re
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import pytesseract
from pdf2image import convert_from_path

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

CHROMA_DIR = "./chroma_db"
POPLER_PATH = r"C:\Users\201-13\Documents\poppler-24.08.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =====================
# 청크 필터링 함수 정의
# =====================
def filter_chunk(text: str) -> bool:
    """
    특수문자/수식/깨진 문자가 포함된 chunk를 필터링하는 함수.
    - 한글, 영어, 숫자, 공백, 일반적인 문장부호(.,;:!?()-[]/) 만 허용
    - 나머지 특수문자/수식/깨진 문자는 제외
    """
    # 허용 문자: 한글, 영문, 숫자, 공백, 일반 문장부호
    allowed_pattern = r'[^\uAC00-\uD7A3a-zA-Z0-9 .,;:!?()\[\]\-/]'  # 허용 외 문자
    # 특수문자/깨진문자/수식이 있으면 False
    if re.search(allowed_pattern, text):
        return False
    return True

async def embed_pdf_manual(file: UploadFile, manual_type: str = "UNKNOWN"):
    import tempfile, shutil
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    try:
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        # 1. manual_id 생성 (uuid)
        manual_id = str(uuid.uuid4())
        # 2. PyPDFLoader로 텍스트 추출 및 청킹
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        split_docs = splitter.split_documents(docs)
        # 3. 일반 chunk에 메타데이터 부여
        pdf_chunks = []
        for idx, doc in enumerate(split_docs):
            if not filter_chunk(doc.page_content):
                continue  # 특수문자/수식/깨진 문자가 포함된 청크는 저장하지 않음
            meta = {
                "manual_id": manual_id,
                "manual_type": manual_type,
                "page_num": doc.metadata.get("page", 1),
                "chunk_idx": idx,
                "source": "pdf",
                "filename": file.filename,
                "uploaded_at": int(time.time())
            }
            pdf_chunks.append(Document(page_content=doc.page_content, metadata=meta))
        # 4. OCR 추출 및 메타데이터 부여
        ocr_docs = []
        images = convert_from_path(temp_path, poppler_path=POPLER_PATH)
        existing_texts = set(doc.page_content.strip() for doc in split_docs)
        for idx, img in enumerate(images):
            ocr_text = pytesseract.image_to_string(img, lang='kor+eng').strip()
            if not ocr_text or ocr_text in existing_texts:
                continue
            if not filter_chunk(ocr_text):
                continue  # 특수문자/수식/깨진 문자가 포함된 청크는 저장하지 않음
            meta = {
                "manual_id": manual_id,
                "manual_type": manual_type,
                "page_num": idx + 1,
                "chunk_idx": idx,
                "source": "ocr",
                "filename": file.filename,
                "uploaded_at": int(time.time())
            }
            ocr_docs.append(Document(page_content=ocr_text, metadata=meta))
        # 5. 합치기 및 벡터DB 저장
        all_docs = pdf_chunks + ocr_docs
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(all_docs, embeddings, persist_directory=CHROMA_DIR)
        vectorstore.persist()
        return {
            "message": "PDF 임베딩 및 저장 완료",
            "manual_id": manual_id,
            "pdf_chunks": len(pdf_chunks),
            "ocr_chunks": len(ocr_docs),
            "total_chunks": len(all_docs)
        }
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass 