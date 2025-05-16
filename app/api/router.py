# app/api/router.py
from fastapi import APIRouter

from app.api.endpoints import documents, health

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])


@api_router.get("/documents/{document_id}/content")
async def get_document_content(document_id: str):
    from app.db.firebase import get_document_content

    return await get_document_content(document_id)
