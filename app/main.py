# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
import logging

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.firebase import initialize_firebase

# Setup logging
logger = setup_logging()

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    initialize_firebase()
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    # Additional cleanup if needed
    logger.info("Application shutdown completed")

# For running directly with Python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

