# README.md
# Document Processing API

A FastAPI middleware service that processes Word documents (.docx files), extracts data, and stores it in Firebase Firestore.

## Features

- Upload Word documents via REST API
- Extract text, tables, and structure from documents
- Store processed data in Firebase Firestore
- Integrated with existing Next.js frontend and FastAPI backend

## Setup Instructions

### Prerequisites

- Python 3.8+
- Firebase project with Firestore database
- Firebase service account credentials

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up Firebase credentials:
   ```
   export FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
   ```

### Running the API

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

Build and run the Docker container:

```bash
docker build -t document-processor-api .
docker run -p 8000:8000 -e FIREBASE_CREDENTIALS_PATH=/app/credentials.json -v /path/to/credentials.json:/app/credentials.json document-processor-api
```

## API Usage

### Upload Document

**Endpoint:** `POST /api/upload-document`

**Content-Type:** `multipart/form-data`

**Request:**
- `file`: Word document (.docx)

**Response:**
```json
{
  "status": "success",
  "message": "Document processed successfully",
  "document_id": "uuid-string",
  "summary": {
    "paragraphs_count": 15,
    "tables_count": 2,
    "headers_count": 5
  }
}
```

### Health Check

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "document-processor"
}
```

## Integration with Existing System

This API is designed to work as a middleware service alongside your existing FastAPI backend and Next.js frontend. You can call this API from your frontend to upload documents, and the extracted data will be stored in the same Firestore database that your main application uses.

## Customization

To customize the data extraction logic, modify the `extract_data_from_docx()` function in `app.py`. This function can be extended to extract specific information based on your document format and requirements.
