# app/services/document_processor.py
import uuid
import logging
from datetime import datetime
from typing import Dict, Any

from app.utils.document_parser import (
    extract_data_from_docx,
    extract_document_statistics,
)
from app.db.firebase import save_document
from app.schemas.document import ProcessedDocument, DocumentMetadata

logger = logging.getLogger("doc_processor")


class DocumentProcessorService:
    """Service for processing document files and saving extracted data."""

    @staticmethod
    async def process_document(file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Process a document file, extract data, and save to Firestore.

        Args:
            file_content (bytes): Binary content of the document
            filename (str): Original filename

        Returns:
            Dict[str, Any]: Processing result with document ID and summary

        Raises:
            ValueError: If document processing fails
        """
        try:
            logger.info(f"Processing document: {filename}")

            # Extract data from document
            extracted_data = extract_data_from_docx(file_content)

            # Generate document ID
            document_id = str(uuid.uuid4())

            # Create document metadata
            metadata = DocumentMetadata(
                original_filename=filename,
                processed_at=datetime.now(),
                file_size=len(file_content),
            )

            # Create processed document
            processed_doc = {
                "document_id": document_id,
                "content": extracted_data,
                "metadata": metadata.dict(),
            }

            # Save to Firestore
            save_document(document_id, processed_doc)

            # Get document statistics
            stats = extract_document_statistics(extracted_data)

            # Return processing result
            return {
                "status": "success",
                "message": "Document processed successfully",
                "document_id": document_id,
                "summary": stats,
            }

        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise ValueError(f"Failed to process document: {str(e)}")
