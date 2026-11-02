"""Tracing functionality for Logscope."""

from functools import wraps
import sys
import os
import threading
import inspect
from datetime import datetime
from typing import Optional

from logscope.database import LogscopeDatabase
from logscope.utils import format_timestamp_with_milliseconds

_local = threading.local()

PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))

SKIP_MODULES = {
    os.path.join(PACKAGE_DIR, 'logscope', 'tracing.py'),
    os.path.join(PACKAGE_DIR, 'logscope', 'database.py'),
    os.path.join(PACKAGE_DIR, 'logscope', 'handlers.py'),
    os.path.join(PACKAGE_DIR, 'logscope', 'core.py'),
}

def should_trace_frame(frame) -> bool:
    """
    Determine if a frame should be traced.
    
    Args:
        frame: The stack frame to check
        
    Returns:
        bool: True if the frame should be traced, False otherwise
    """
    filename = os.path.abspath(frame.f_code.co_filename)
    return filename not in SKIP_MODULES

def trace_function(frame, event, arg) -> Optional[callable]:
    """
    Trace function that captures function calls and line events.
    """
    if not hasattr(_local, "db") or _local.db is None:
        return None

    # Skip frames from the logging library itself
    if not should_trace_frame(frame):
        return trace_function

    # Get source context
    try:
        context_lines, _ = inspect.findsource(frame)
        source_line = context_lines[frame.f_lineno - 1].strip()
    except Exception:
        source_line = "<source not available>"

    # Create appropriate message based on event type
    if event == "call":
        message = f"Function call: {frame.f_code.co_name}"
    elif event == "return":
        message = f"Function return: {frame.f_code.co_name} -> {repr(arg)}"
    elif event == "exception":
        exc_type, exc_value, _ = arg
        message = f"Exception in function: {exc_type.__name__}: {exc_value}"
    else:
        message = f"Event {event} in function {frame.f_code.co_name}"

    # Write directly to database
    _local.db.write_log({
        'timestamp': format_timestamp_with_milliseconds({'created': datetime.now().timestamp()}),
        'message': message,
        'filename': frame.f_code.co_filename,
        'lineno': frame.f_lineno,
        'source': source_line,
        'function': frame.f_code.co_name,
        'event_type': event
    })

    return trace_function

def start_tracing(db_path='logscope.db'):
    """Start tracing with the given database path."""
    _local.db = LogscopeDatabase(db_path)
    sys.settrace(trace_function)

def stop_tracing():
    """Stop the tracing process for the current thread."""
    sys.settrace(None)
    if hasattr(_local, "db"):
        _local.db.close()
        _local.db = None

def trace(func=None, *, db_path='logscope.db'):
    """
    Decorator to trace the execution of a function.
    """
    if func is None:
        return lambda f: trace(f, db_path=db_path)

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_tracing(db_path)
        try:
            return func(*args, **kwargs)
        finally:
            stop_tracing()

    return wrapper