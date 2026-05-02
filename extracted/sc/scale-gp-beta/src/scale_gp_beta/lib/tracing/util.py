import os
import uuid
from typing import Optional
from datetime import datetime, timezone
from functools import cache

_tracing_disabled: Optional[bool] = None


def generate_trace_id() -> str:
    """
    Generate a unique trace ID.

    Returns:
        str: A unique trace ID.
    """
    return str(uuid.uuid4())


def generate_span_id() -> str:
    """
    Generate a unique span ID.

    Returns:
        str: A unique span ID.
    """
    return str(uuid.uuid4())


def iso_timestamp() -> str:
    """
    Generate an ISO 8601 timestamp.

    Returns:
        str: The current time in ISO 8601 format.
    """
    return datetime.now(timezone.utc).isoformat()


def configure(disabled: bool) -> None:
    """
    Programmatically enable or disable tracing.

    This setting takes precedence over the `DISABLE_SCALE_TRACING` environment
    variable.

    Args:
        disabled (bool): Set to True to disable tracing, False to enable.
    """
    global _tracing_disabled
    _tracing_disabled = disabled
    is_disabled.cache_clear()


@cache
def is_disabled() -> bool:
    """
    Check if tracing is disabled, with programmatic control taking precedence.

    Tracing is considered disabled if `configure(disabled=True)` has been called,
    or if the `DISABLE_SCALE_TRACING` environment variable is set.

    Returns:
        bool: True if tracing is disabled, otherwise False.
    """
    if _tracing_disabled is not None:
        return _tracing_disabled
    return os.getenv("DISABLE_SCALE_TRACING") is not None
