# app/db/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore, storage
import logging
from app.core.config import settings
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("doc_processor")


def initialize_firebase():
    """Initialize Firebase app with Storage and Firestore"""
    try:
        if not firebase_admin._apps:
            # Create a credential object from the settings
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
            
            # Initialize the app with storage bucket
            firebase_admin.initialize_app(cred, {
                'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
                'databaseURL': settings.FIREBASE_DATABASE_URL
            })
            
            # Test the connection
            db = firestore.client()
            bucket = storage.bucket()
            
            logger.info("Firebase initialized successfully")
        else:
            logger.info("Firebase already initialized")
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")
        raise


def get_firestore_client():
    """Get Firestore client instance"""
    try:
        return firestore.client()
    except Exception as e:
        logger.error(f"Error getting Firestore client: {e}")
        raise


def get_storage_bucket():
    """Get Storage bucket instance"""
    try:
        return storage.bucket()
    except Exception as e:
        logger.error(f"Error getting Storage bucket: {e}")
        raise


def upload_to_storage(file_content: bytes, document_id: str, filename: str) -> str:
    """Upload document to Firebase Storage"""
    try:
        bucket = get_storage_bucket()
        file_extension = filename.split('.')[-1].lower()
        storage_path = f"documents/{document_id}/original.{file_extension}"
        
        blob = bucket.blob(storage_path)
        blob.upload_from_string(
            file_content,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # Make the blob publicly accessible
        blob.make_public()
        
        return blob.public_url
    except Exception as e:
        logger.error(f"Error uploading to Storage: {e}")
        raise


def save_document(document_id: str, data: Dict[str, Any]):
    """Save document metadata to Firestore"""
    try:
        db = get_firestore_client()
        doc_ref = db.collection(settings.FIREBASE_COLLECTION_NAME).document(document_id)
        
        # Add timestamp
        data['created_at'] = firestore.SERVER_TIMESTAMP
        
        doc_ref.set(data)
        logger.info(f"Document metadata saved to Firestore with ID: {document_id}")
    except Exception as e:
        logger.error(f"Error saving to Firestore: {e}")
        raise


def save_document_chunk(chunk_id: str, data: Dict[str, Any]):
    """Save document chunk to Firestore"""
    try:
        db = get_firestore_client()
        
        # Add timestamp
        data['created_at'] = firestore.SERVER_TIMESTAMP
        
        chunk_ref = db.collection('document_chunks').document(chunk_id)
        chunk_ref.set(data)
        logger.info(f"Document chunk saved with ID: {chunk_id}")
    except Exception as e:
        logger.error(f"Error saving chunk to Firestore: {e}")
        raise
