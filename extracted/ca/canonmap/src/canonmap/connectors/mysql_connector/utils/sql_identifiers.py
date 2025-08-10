# src/canonmap/connectors/mysql_connector/utils/sql_identifiers.py

from __future__ import annotations

def quote_identifier(name: str) -> str:
    cleaned = (name or "").strip()
    if not cleaned:
        raise ValueError(f"Invalid identifier: {name!r}")
    # Escape backticks by doubling them per MySQL rules
    escaped = cleaned.replace("`", "``")
    return f"`{escaped}`"


