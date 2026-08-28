import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def setup_logging():

    # Create logs directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("expense_tracker")

    # Prevent duplicate handlers when Uvicorn reloads
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

   
    # File Handler

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)


    # Console Handler

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Don't propagate to root logger
    logger.propagate = False

    return logger