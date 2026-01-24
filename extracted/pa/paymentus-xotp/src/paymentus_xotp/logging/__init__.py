"""
Logging utilities for the XOTP SDK.
"""
import logging
from enum import Enum
from typing import Protocol, Optional, Any, List, Dict, Union

__all__ = [
    "LogLevel",
    "MaskingLevel",
    "Logger"
]

class LogLevel(Enum):
    """Log levels for SDK logging"""
    SILENT = 0
    MINIMAL = 1
    NORMAL = 2
    VERBOSE = 3
    
    def to_python_level(self) -> int:
        """Convert SDK log level to Python logging level"""
        mapping = {
            LogLevel.SILENT: logging.CRITICAL + 10,  # Higher than CRITICAL
            LogLevel.MINIMAL: logging.INFO,
            LogLevel.NORMAL: logging.DEBUG,
            LogLevel.VERBOSE: logging.DEBUG
        }
        return mapping.get(self, logging.INFO)


class MaskingLevel(Enum):
    """Masking levels for sensitive data"""
    NONE = 0
    PCI_ONLY = 1
    ALL_PII = 2


class Logger:
    """Default implementation of the Logger interface that uses Python's logging module."""
    
    def __init__(self, level: LogLevel = LogLevel.NORMAL):
        """
        Initialize a new DefaultLogger.
        
        Args:
            level: The initial log level to use. Defaults to NORMAL.
        """
        self.logger = logging.getLogger("paymentus.xotp.sdk")
        self.level: LogLevel = level
        
        python_level = level.to_python_level()
        self.logger.setLevel(python_level)

        # Ensure we have a clean set of handlers to avoid duplicates.
        self.logger.handlers.clear()

        # Add a new, correctly-leveled handler.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(python_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
    def info(self, message: str, *args: Any) -> None:
        """Log an informational message"""
        if args:
            self.logger.info(message, *args)
        else:
            self.logger.info(message)
    
    def error(self, message: str, *args: Any) -> None:
        """Log an error message"""
        if args:
            self.logger.error(message, *args)
        else:
            self.logger.error(message)
    
    def warn(self, message: str, *args: Any) -> None:
        """Log a warning message"""
        if args:
            self.logger.warning(message, *args)
        else:
            self.logger.warning(message)
    
    def debug(self, message: str, *args: Any) -> None:
        """Log a debug message"""
        if args:
            self.logger.debug(message, *args)
        else:
            self.logger.debug(message)