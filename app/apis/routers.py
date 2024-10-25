from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.services import Service
from typing import Dict
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

service = Service()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
) -> Dict[str, str]:
    logger.info(f"Upload attempt for file: {file.filename}")
    try:
        await service.save_file(file)
        return {"message": "File uploaded successfully"}
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/question")
async def ask_question(question: str) -> Dict[str, str]:
    logger.info(f"Question: {question}")
    try:
        answer = await service.ask_question(question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error during question: {e}")
        raise HTTPException(status_code=400, detail=str(e))
