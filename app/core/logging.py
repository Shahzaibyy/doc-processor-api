# app/core/logging.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import settings


def setup_logging():
    """
    Set up logging configuration for the application.
    Returns a logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Set up log file path
    log_file = log_dir / "app.log"

    # Configure log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler with rotation
            RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=5, encoding="utf8"  # 10MB
            ),
        ],
    )

    # Create and return logger
    logger = logging.getLogger("doc_processor")

    # Set third-party loggers to WARNING level
    for logger_name in ("uvicorn", "uvicorn.access", "fastapi"):
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    return logger
