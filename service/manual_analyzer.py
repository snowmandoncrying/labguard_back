import os
import shutil
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
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
        llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPENAI_API_KEY)
        question = "이 매뉴얼에서 나타나는 잠재적 위험요소와 주의사항을 요약해줘."
        # chunk별 요약
        chunk_summaries = []
        for chunk in split_docs:
            chunk_summary = llm.predict(f"{question}\n\n{chunk.page_content}")
            chunk_summaries.append(chunk_summary.strip())
        # chunk 요약을 다시 합쳐서 최종 요약
        final_input = f"{question}\n\n" + "\n".join(chunk_summaries)
        final_summary = llm.predict(final_input)
        return final_summary.strip()
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass 