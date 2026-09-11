"""Narrowing the values a generated model may leave unset.

A leaf module: every entity parses the same handful of shapes, so the checks
live here rather than once per domain module.
"""

from __future__ import annotations

# Python internals
from datetime import datetime
from typing import Any


def text(value: Any) -> str | None:
    """Narrow one of the many strings the generated model may leave unset.

    Args:
        value: What the payload carries.

    Returns:
        The string, or ``None`` for anything else.
    """
    return value if isinstance(value, str) else None


def whole(value: Any) -> int | None:
    """Narrow a nullable counter the generated model may leave unset.

    Args:
        value: What the payload carries.

    Returns:
        The integer, or ``None`` for anything else.
    """
    return value if isinstance(value, int) else None


def moment(value: Any) -> datetime | None:
    """Narrow a nullable timestamp the generated model may leave unset.

    Args:
        value: What the payload carries.

    Returns:
        The datetime, or ``None`` for anything else.
    """
    return value if isinstance(value, datetime) else None


def seconds(value: Any) -> float | None:
    """Turn a millisecond duration into seconds, as the rest of this SDK reports.

    Args:
        value: What the payload carries.

    Returns:
        The duration in seconds, or ``None`` for anything unset.
    """
    return value / 1000 if isinstance(value, (int, float)) else None
