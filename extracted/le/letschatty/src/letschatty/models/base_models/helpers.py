from datetime import datetime

def _normalize_precision(dt: datetime) -> datetime:
    """Normalize datetime to millisecond precision"""
    return dt.replace(microsecond=(dt.microsecond // 1000) * 1000)
    