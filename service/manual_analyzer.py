import os
import shutil
import tempfile
from fastapi import UploadFile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

async def analyze_manual_file(file: UploadFile) -> str:
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    try:
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        split_docs = splitter.split_documents(docs)
        llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)
        full_text = "\n".join([d.page_content for d in split_docs])
        question = "이 매뉴얼에서 나타나는 잠재적, 위험요소와 주의사항을 요약해줘."
        response = llm.predict(f"{question}\n\n{full_text}")
        return response.strip()
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass 