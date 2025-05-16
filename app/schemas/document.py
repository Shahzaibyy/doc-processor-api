# app/schemas/document.py
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TableData(BaseModel):
    index: int
    data: List[List[str]]


class Paragraph(BaseModel):
    text: str
    index: int
    is_heading: bool = False


class Header(BaseModel):
    level: int
    text: str
    index: int


class ExtractedDocumentData(BaseModel):
    paragraphs: List[Paragraph] = []
    tables: List[TableData] = []
    headers: List[Header] = []


class DocumentMetadata(BaseModel):
    original_filename: str
    processed_at: datetime = Field(default_factory=datetime.now)
    document_type: str = "word"
    file_size: Optional[int] = None
    additional_info: Optional[Dict[str, Any]] = None


class ProcessedDocument(BaseModel):
    document_id: str
    content: ExtractedDocumentData
    metadata: DocumentMetadata


class DocumentProcessResponse(BaseModel):
    status: str
    message: str
    document_id: str
    summary: Dict[str, int]


class HealthCheckResponse(BaseModel):
    status: str
    service: str
    version: str
