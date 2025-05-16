# app/api/endpoints/health.py
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.document import HealthCheckResponse

router = APIRouter()


@router.get("", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API is functioning properly.
    Returns status information about the service.
    """
    return {
        "status": "healthy",
        "service": "document-processor",
        "version": settings.VERSION,
    }
