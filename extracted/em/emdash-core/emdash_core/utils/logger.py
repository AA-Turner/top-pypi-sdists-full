"""Logging configuration for EmDash.

Production mode (default): Minimal logs, only warnings and errors.
Debug mode (LOG_LEVEL=DEBUG): Full verbose logging with timestamps.
"""

import os
import sys
from loguru import logger


def _is_debug_mode() -> bool:
    """Check if debug logging is enabled."""
    level = os.environ.get("LOG_LEVEL", "WARNING").upper()
    return level in ("DEBUG", "TRACE")


def setup_logger():
    """Configure logger with appropriate level and format.

    In production mode (default), logs are minimal - only WARNING and above.
    In debug mode (LOG_LEVEL=DEBUG), full verbose logs are shown.
    """
    # Remove default handler
    logger.remove()

    # Get log level from environment
    log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()

    if _is_debug_mode():
        # Debug mode: full verbose format
        logger.add(
            sys.stderr,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
            colorize=True,
        )
    else:
        # Production mode: minimal format, only warnings and errors
        logger.add(
            sys.stderr,
            level=log_level,
            format="<level>{level: <8}</level> | <level>{message}</level>",
            colorize=True,
        )

    return logger


# Create a module-level logger instance
log = setup_logger()
