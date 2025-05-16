# app/db/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from app.core.config import settings
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("doc_processor")


def initialize_firebase():
    """
    Initialize Firebase app with the provided credentials.
    This should be called only once during application startup.
    """
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
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


def save_document(document_id: str, data: Dict[str, Any]):
    """Save document metadata to Firestore"""
    try:
        db = get_firestore_client()
        doc_ref = db.collection(settings.FIREBASE_COLLECTION_NAME).document(document_id)

        # Add timestamp
        data["created_at"] = firestore.SERVER_TIMESTAMP

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
        data["created_at"] = firestore.SERVER_TIMESTAMP

        chunk_ref = db.collection("document_chunks").document(chunk_id)
        chunk_ref.set(data)
        logger.info(f"Document chunk saved with ID: {chunk_id}")
    except Exception as e:
        logger.error(f"Error saving chunk to Firestore: {e}")
        raise
