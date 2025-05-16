# app/db/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from app.core.config import settings

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
    """
    Get a Firestore client instance.
    Returns:
        firestore.Client: Firestore client instance
    """
    try:
        return firestore.client()
    except Exception as e:
        logger.error(f"Error getting Firestore client: {e}")
        raise


def save_document(document_id, data):
    """
    Save document data to Firestore.

    Args:
        document_id (str): Document ID
        data (dict): Document data to save

    Returns:
        str: Document ID of the saved document
    """
    try:
        db = get_firestore_client()
        collection_ref = db.collection(settings.FIREBASE_COLLECTION_NAME)
        doc_ref = collection_ref.document(document_id)
        doc_ref.set(data)
        logger.info(f"Document saved to Firestore with ID: {document_id}")
        return document_id
    except Exception as e:
        logger.error(f"Error saving document to Firestore: {e}")
        raise
