from __future__ import annotations

from typing import Any

SCRAPE_DATA_TYPES = frozenset({"fetch_results", "scraped_pages"})
MAX_LOG_STRING_LEN = 100


def is_scrape_data_log(payload: dict[str, Any]) -> bool:
    event_type = payload.get("type") or payload.get("response_type")
    return event_type in SCRAPE_DATA_TYPES


def truncate_strings_for_log(value: Any, *, max_len: int = MAX_LOG_STRING_LEN) -> Any:
    if isinstance(value, str):
        if len(value) <= max_len:
            return value
        omitted = len(value) - max_len
        return f"{value[:max_len]}…[truncated {omitted} chars]"
    if isinstance(value, dict):
        return {key: truncate_strings_for_log(item, max_len=max_len) for key, item in value.items()}
    if isinstance(value, list):
        return [truncate_strings_for_log(item, max_len=max_len) for item in value]
    return value
