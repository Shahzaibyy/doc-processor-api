# app/services/document_processor.py
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List
import io
from PyPDF2 import PdfReader
from docx import Document

from app.schemas.document import (
    DocumentMetadata,
    ContentPreview,
    DocumentProcessResponse,
    DocumentChunk,
    Page,
    Header,
    Paragraph,
    TableData
)
from app.db.firebase import save_document, save_document_chunk, upload_to_storage

logger = logging.getLogger("doc_processor")

class DocumentProcessorService:
    """Service for processing document files and saving extracted data."""

    @staticmethod
    def _chunk_content(content: List[Dict], chunk_size: int = 100) -> List[List[Dict]]:
        """Split content into smaller chunks"""
        return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    @staticmethod
    def _flatten_table_data(table_data: List[List[str]]) -> List[Dict[str, Any]]:
        """Convert table data into Firestore-compatible format"""
        flattened_rows = []
        for row_idx, row in enumerate(table_data):
            row_dict = {
                "row_index": str(row_idx),
                "cells": [{"cell_index": str(i), "value": str(v)} for i, v in enumerate(row)]
            }
            flattened_rows.append(row_dict)
        return flattened_rows

    @staticmethod
    def _extract_data_from_pdf(file_content: bytes) -> Dict[str, Any]:
        """Extract text and structure from a PDF document."""
        pdf_reader = PdfReader(io.BytesIO(file_content))
        extracted_data = {
            "paragraphs": [],
            "tables": [],
            "headers": [],
            "pages": []
        }
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            paragraphs = text.split('\n\n')
            
            # Process paragraphs
            for i, para in enumerate(paragraphs):
                if para.strip():
                    # Simple heuristic for headers (all caps, short text)
                    is_heading = para.isupper() and len(para.split()) <= 3
                    if is_heading:
                        extracted_data["headers"].append({
                            "level": "1",
                            "text": para.strip(),
                            "index": str(i)
                        })
                    
                    extracted_data["paragraphs"].append({
                        "text": para.strip(),
                        "index": str(i),
                        "is_heading": is_heading
                    })
            
            # Add page information
            extracted_data["pages"].append({
                "page_number": str(page_num),
                "content": text
            })
        
        return extracted_data

    @staticmethod
    def _extract_data_from_docx(file_content: bytes) -> Dict[str, Any]:
        """Extract text and structure from a Word document."""
        doc = Document(io.BytesIO(file_content))
        
        paragraphs = []
        headers = []
        pages = []
        tables = []
        
        current_page_content = []
        current_page_number = 1
        char_count = 0
        chars_per_page = 3000

        # Process paragraphs and headers
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text:
                # Basic paragraph data
                para_data = {
                    "text": str(text),
                    "index": str(i),
                    "is_heading": "false"  # Store as string for consistency
                }

                # Check for heading
                if para.style.name.startswith('Heading'):
                    para_data["is_heading"] = "true"
                    try:
                        level = int(para.style.name.replace('Heading', '').strip())
                    except ValueError:
                        level = 1
                    
                    headers.append({
                        "text": str(text),
                        "level": str(level),
                        "index": str(i)
                    })

                paragraphs.append(para_data)

                # Page simulation
                current_page_content.append(text)
                char_count += len(text)

                if char_count >= chars_per_page:
                    pages.append({
                        "page_number": str(current_page_number),
                        "content": str("\n".join(current_page_content))
                    })
                    current_page_content = []
                    current_page_number += 1
                    char_count = 0

        # Add final page if content exists
        if current_page_content:
            pages.append({
                "page_number": str(current_page_number),
                "content": str("\n".join(current_page_content))
            })

        # Process tables with flattened structure
        for i, table in enumerate(doc.tables):
            rows_data = []
            for row_idx, row in enumerate(table.rows):
                cells = []
                for cell_idx, cell in enumerate(row.cells):
                    cells.append({
                        "cell_index": str(cell_idx),
                        "value": str(cell.text.strip())
                    })
                rows_data.append({
                    "row_index": str(row_idx),
                    "cells": cells
                })
            
            tables.append({
                "table_index": str(i),
                "rows": rows_data
            })

        return {
            "paragraphs": paragraphs,
            "headers": headers,
            "pages": pages,
            "tables": tables
        }

    @staticmethod
    async def process_document(file_content: bytes, filename: str) -> DocumentProcessResponse:
        """Process a document file, extract data, and save to Firebase"""
        try:
            logger.info(f"Processing document: {filename}")
            
            document_id = str(uuid.uuid4())
            file_extension = filename.lower().split('.')[-1]
            
            if file_extension != 'docx':
                raise ValueError(f"Unsupported file type: {file_extension}")

            # Upload to Firebase Storage
            storage_url = upload_to_storage(file_content, document_id, filename)

            # Extract content
            extracted_data = DocumentProcessorService._extract_data_from_docx(file_content)

            # Create base document metadata
            base_doc = {
                "document_id": document_id,
                "storage_url": storage_url,
                "metadata": {
                    "original_filename": str(filename),
                    "processed_at": datetime.now().isoformat(),
                    "file_size": str(len(file_content)),
                    "document_type": str(file_extension),
                    "total_pages": str(len(extracted_data["pages"])),
                    "total_paragraphs": str(len(extracted_data["paragraphs"])),
                    "total_headers": str(len(extracted_data["headers"])),
                    "total_tables": str(len(extracted_data["tables"]))
                },
                "content_summary": {
                    "first_page": extracted_data["pages"][0] if extracted_data["pages"] else {},
                    "headers": extracted_data["headers"][:10],
                    "first_paragraphs": extracted_data["paragraphs"][:5]
                }
            }

            # Save to Firestore
            save_document(document_id, base_doc)

            # Save content chunks
            for content_type, (content, chunk_size) in {
                "pages": (extracted_data["pages"], 50),
                "paragraphs": (extracted_data["paragraphs"], 100),
                "headers": (extracted_data["headers"], len(extracted_data["headers"])),
                "tables": (extracted_data["tables"], 10)
            }.items():
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i + chunk_size]
                    chunk_doc = DocumentChunk(
                        document_id=document_id,
                        chunk_index=str(i//chunk_size),
                        type=content_type,
                        content=chunk,
                        total_chunks=str((len(content) + chunk_size - 1) // chunk_size)
                    )
                    save_document_chunk(f"{document_id}_{content_type}_{i//chunk_size}", chunk_doc.model_dump())

            # Return response
            return DocumentProcessResponse(
                status="success",
                message="Document processed successfully",
                document_id=document_id,
                storage_url=storage_url,
                summary={
                    "pages_count": len(extracted_data["pages"]),
                    "paragraphs_count": len(extracted_data["paragraphs"]),
                    "tables_count": len(extracted_data["tables"]),
                    "headers_count": len(extracted_data["headers"])
                },
                content_preview=ContentPreview(
                    first_page_content=extracted_data["pages"][0]["content"] if extracted_data["pages"] else "",
                    headers=[h["text"] for h in extracted_data["headers"][:10]],
                    first_paragraphs=[p["text"] for p in extracted_data["paragraphs"][:5]]
                )
            )

        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise ValueError(f"Failed to process document: {str(e)}")
