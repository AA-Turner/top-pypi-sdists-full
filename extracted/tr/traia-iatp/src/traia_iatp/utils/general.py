"""General utility functions for traia_iatp package."""

import logging
from datetime import datetime
import pytz


def get_logger() -> logging.Logger:
    """Get a logger instance configured for the traia_iatp package.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def get_now_in_utc() -> datetime:
    """Get the current datetime in UTC timezone.
    
    Returns:
        datetime: Current UTC datetime
    """
    return datetime.now(tz=pytz.utc)


def is_empty(obj) -> bool:
    """Check if an object is empty.
    
    Args:
        obj: Object to check
        
    Returns:
        bool: True if object is None or has length 0
    """
    try:
        if obj is None:
            return True
        if len(obj) == 0:
            return True
    except TypeError:
        # Object doesn't have length (e.g., numbers, booleans)
        return obj is None
    return False


def not_empty(obj) -> bool:
    """Check if an object is not empty.
    
    Args:
        obj: Object to check
        
    Returns:
        bool: True if object is not None and has length > 0
    """
    return not is_empty(obj) 