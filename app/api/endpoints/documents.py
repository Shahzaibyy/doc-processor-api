# app/api/endpoints/documents.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

from app.core.config import settings
from app.services.document_processor import DocumentProcessorService
from app.schemas.document import DocumentProcessResponse

logger = logging.getLogger("doc_processor")
router = APIRouter()


@router.post("/upload", response_model=DocumentProcessResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF or DOCX) to be processed and stored in Firestore.

    The API extracts text, tables, and structure from the document and
    stores the extracted data in Firestore.

    Returns processing result with document ID and summary statistics.
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Only {', '.join(settings.ALLOWED_EXTENSIONS)} files are supported",
            )

        # Read file content
        file_content = await file.read()

        # Check file size
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {max_size_mb}MB",
            )

        # Process document
        result = await DocumentProcessorService.process_document(
            file_content=file_content, filename=file.filename
        )

        return result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        # Document processing errors
        logger.error(f"Document processing error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error in upload_document: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
