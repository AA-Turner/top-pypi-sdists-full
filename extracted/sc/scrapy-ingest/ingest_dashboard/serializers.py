"""JSON-safe values for API responses."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal


def serialize_value(value):
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
