"""Utility functions for Logscope."""

import time
import inspect
import logging
from typing import Tuple

class CallingDetailsFilter(logging.Filter):
    """Filter that adds calling details to log records."""
    
    def filter(self, record):
        source, function, _, _ = get_calling_details(record)
        record.source = source
        record.function = function
        return True

def get_calling_details(record: logging.LogRecord) -> Tuple[str, str, str, int]:
    """
    Get the calling context details for a log record.
    
    Args:
        record: The log record to analyze
        
    Returns:
        Tuple of (source code context, function name, pathname, lineno)
    """
    frame = inspect.currentframe()
    while frame:
        frame = frame.f_back
        if frame and frame.f_lineno == record.lineno and frame.f_code.co_filename == record.pathname:
            frame = frame.f_back
            break
    if frame:
        frame_info = inspect.getframeinfo(frame)
        func_name = frame.f_code.co_name if frame.f_code.co_name != '<module>' else '<global>'
        return (
            frame_info.code_context[0].strip() if frame_info.code_context else "<unknown>",
            func_name,
            frame.f_code.co_filename,
            frame.f_lineno
        )
    else:
        return ("<unknown>", "<unknown>", record.pathname, record.lineno)

def format_timestamp_with_milliseconds(record: logging.LogRecord | dict) -> str:
    """
    Format a timestamp with millisecond precision.
    
    Args:
        record: Either a LogRecord object or a dictionary containing a 'created' key
        
    Returns:
        Formatted timestamp string
    """
    if isinstance(record, dict):
        timestamp = record['created']
    else:
        timestamp = record.created
        
    timestamp_sec = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    milliseconds = int((timestamp % 1) * 1000)
    return f"{timestamp_sec}.{milliseconds:03d}"