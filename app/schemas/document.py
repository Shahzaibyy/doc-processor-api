# app/schemas/document.py
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TableData(BaseModel):
    index: str
    data: List[Dict[str, str]]


class Paragraph(BaseModel):
    text: str
    index: str
    is_heading: str


class Header(BaseModel):
    level: str
    text: str
    index: str


class Page(BaseModel):
    page_number: str
    content: str


class DocumentMetadata(BaseModel):
    original_filename: str
    processed_at: str
    document_type: str
    file_size: str
    total_pages: str
    total_paragraphs: str
    total_headers: str
    total_tables: str


class ContentPreview(BaseModel):
    first_page_content: str
    headers: List[str]
    first_paragraphs: List[str]


class StorageInfo(BaseModel):
    storage_url: str
    chunks: Dict[str, int]


class DocumentProcessResponse(BaseModel):
    status: str
    message: str
    document_id: str
    storage_url: str
    summary: Dict[str, int]
    content_preview: ContentPreview


class HealthCheckResponse(BaseModel):
    status: str
    service: str
    version: str


class DocumentChunk(BaseModel):
    document_id: str
    chunk_index: str
    type: str
    content: List[Dict[str, Any]]
    total_chunks: str
    created_at: Optional[datetime] = None


# Add these utility models if needed
class ChunkMetadata(BaseModel):
    chunk_index: str
    total_chunks: str
    document_id: str
    type: str


class DocumentContent(BaseModel):
    paragraphs: List[Paragraph]
    headers: List[Header]
    pages: List[Page]
    tables: List[TableData]
