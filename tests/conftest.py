# tests/conftest.py
import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app


@pytest.fixture
def client():
    """Return a TestClient instance for testing API endpoints."""
    return TestClient(app)


@pytest.fixture
def mock_docx_file():
    """Create a mock Word document file for testing."""
    file_content = b"mock word document content"
    return io.BytesIO(file_content)


@pytest.fixture(autouse=True)
def mock_firebase():
    """Mock Firebase initialization and Firestore operations."""
    with patch("app.db.firebase.initialize_firebase"), patch(
        "app.db.firebase.get_firestore_client"
    ), patch("app.db.firebase.save_document", return_value="test-document-id"):
        yield


@pytest.fixture
def mock_document_processor():
    """Mock document processor service."""
    with patch(
        "app.services.document_processor.DocumentProcessorService.process_document"
    ) as mock:
        mock.return_value = {
            "status": "success",
            "message": "Document processed successfully",
            "document_id": "test-document-id",
            "summary": {
                "paragraphs_count": 5,
                "tables_count": 2,
                "headers_count": 3,
                "total_words": 100,
                "table_words": 20,
            },
        }
        yield mock


@pytest.fixture
def mock_extract_data():
    """Mock document data extraction."""
    with patch("app.utils.document_parser.extract_data_from_docx") as mock:
        mock.return_value = {
            "paragraphs": [
                {"text": "Test paragraph 1", "index": 0, "is_heading": False},
                {"text": "Test header", "index": 1, "is_heading": True},
                {"text": "Test paragraph 2", "index": 2, "is_heading": False},
            ],
            "tables": [
                {"index": 0, "data": [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]}
            ],
            "headers": [{"level": 1, "text": "Test Header", "index": 1}],
        }
        yield mock
