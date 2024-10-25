import os
from fastapi import UploadFile

from ..haystack.haystack import RAG
from ..core.config import Settings
import json
import re
import logging

logger = logging.getLogger(__name__)
settings = Settings()
rag = RAG()

class Service:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)
        logger.info(f"Saving file {file.filename} to {file_path}")
        with open(file_path, "wb+") as f:
            f.write(await file.read())
        logger.info("File saved successfully.")
        logger.info(f"Upload Directory: {self.upload_dir}")
        # List all files in the upload directory  
        file_contents = ""  
        for file_name in os.listdir(self.upload_dir):  
            file_path = os.path.join(self.upload_dir, file_name)  # Full path of the file  
            if os.path.isfile(file_path):  # Ensure it's a file  
                logger.info(f"Reading file: {file_name}")  
                file_contents += await read_file_content(file_path) + "\n"  # Accumulate contents
        json_string = re.sub(r'[\n\r\t]', '', file_contents)
        data = json.loads(json_string)
        rag.embedding(data)
    
    async def ask_question(self, question: str) -> str:
        answer = rag.get_answer(question)
        logger.info("Question processed successfully.")
        return answer

async def read_file_content(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
