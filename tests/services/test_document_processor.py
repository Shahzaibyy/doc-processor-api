# tests/api/test_documents.py
import pytest
from fastapi import status


def test_upload_document_success(client, mock_docx_file, mock_document_processor):
    """Test successful document upload."""
    # Create test file
    test_file = {
        "file": (
            "test_document.docx",
            mock_docx_file,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }

    # Make request
    response = client.post("/api/documents/upload", files=test_file)

    # Check response
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["document_id"] == "test-document-id"
    assert "summary" in response_data
    assert response_data["summary"]["paragraphs_count"] == 5
    assert response_data["summary"]["tables_count"] == 2

    # Ensure mock was called
    mock_document_processor.assert_called_once()


def test_upload_invalid_extension(client):
    """Test upload with invalid file extension."""
    # Create test file with wrong extension
    test_file = {"file": ("test_document.txt", b"test content", "text/plain")}

    # Make request
    response = client.post("/api/documents/upload", files=test_file)

    # Check response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only" in response.json()["detail"] and ".docx" in response.json()["detail"]


def test_document_processing_error(client, mock_docx_file, mock_document_processor):
    """Test error during document processing."""
    # Mock processor to raise an error
    mock_document_processor.side_effect = ValueError("Test processing error")

    # Create test file
    test_file = {
        "file": (
            "test_document.docx",
            mock_docx_file,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }

    # Make request
    response = client.post("/api/documents/upload", files=test_file)

    # Check response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Test processing error" in response.json()["detail"]


def test_upload_no_file(client):
    """Test upload with no file."""
    # Make request without file
    response = client.post("/api/documents/upload")

    # Check response
    assert response.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
