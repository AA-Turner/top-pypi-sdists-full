"""Logging utilities for MCP CLI."""

import logging
import os
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    
    RESET = '\033[0m'
    
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, 
                 use_colors: bool = True):
        """Initialize the formatter.
        
        Args:
            fmt: Format string
            datefmt: Date format string
            use_colors: Whether to use colors (default: True)
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and self._supports_color()
    
    @staticmethod
    def _supports_color() -> bool:
        """Check if the terminal supports color output."""
        # Check if stdout is a tty and not redirected
        if not hasattr(sys.stderr, 'isatty') or not sys.stderr.isatty():
            return False
        
        # Check for common environment variables that indicate color support
        if sys.platform == 'win32':
            # Windows terminal supports ANSI colors in Windows 10+
            return True
        
        # Check TERM environment variable
        term = os.getenv('TERM', '')
        if term == 'dumb':
            return False
        
        # Check for NO_COLOR env variable (https://no-color.org/)
        if os.getenv('NO_COLOR'):
            return False
        
        return True
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors if supported."""
        # Save original levelname
        levelname = record.levelname
        
        if self.use_colors and levelname in self.COLORS:
            # Add color to levelname
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
            
            # Color the entire message for ERROR and CRITICAL
            if levelname in ('ERROR', 'CRITICAL'):
                record.msg = f"{self.COLORS[levelname]}{record.msg}{self.RESET}"
        
        # Format the record
        formatted = super().format(record)
        
        # Restore original levelname
        record.levelname = levelname
        
        return formatted


def setup_colored_logging(handler: logging.Handler, fmt: str, datefmt: str) -> None:
    """Apply colored formatting to a logging handler.
    
    Args:
        handler: The logging handler to apply colored formatting to
        fmt: Format string for log messages
        datefmt: Date format string
    """
    formatter = ColoredFormatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)


def setup_logging(level: int = logging.WARNING) -> None:
    """Set up logging for the MCP CLI application.
    
    This function configures the root logger and various package loggers
    with appropriate levels and formats. It includes colored output support
    when running in a terminal.
    
    Args:
        level: Logging level for the application
    """
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stderr)
    
    # Configure format
    fmt = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    datefmt = '%H:%M:%S'
    
    # Apply colored formatting if supported
    setup_colored_logging(console_handler, fmt, datefmt)
    
    # Configure root logger
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    # Set mcp_cli to the requested level
    mcp_logger = logging.getLogger('mcp_cli')
    mcp_logger.setLevel(level)
    
    # Set httpx and httpcore to WARNING unless DEBUG is requested
    # This reduces noise from HTTP library internals
    http_level = level if level == logging.DEBUG else logging.WARNING
    for logger_name in ['httpx', 'httpcore', 'hpack', 'httpx_auth']:
        logger = logging.getLogger(logger_name)
        logger.setLevel(http_level)
    
    # Always suppress httpcore debug logs as they're too verbose
    logging.getLogger('httpcore').setLevel(logging.INFO)
    
    logging.getLogger('asyncio').setLevel(logging.INFO)