"""Flatten nested item dicts for tabular export."""

from __future__ import annotations

import json
from typing import Any


def flatten_value(
    data: Any,
    prefix: str = "",
    *,
    sep: str = ".",
    max_depth: int = 10,
) -> dict[str, Any]:
    """Turn nested dicts/lists into a single-level mapping."""
    if max_depth <= 0:
        key = prefix or "value"
        return {key: _scalar(data)}

    if isinstance(data, dict):
        if not data:
            return {prefix: ""} if prefix else {}
        out: dict[str, Any] = {}
        for key, value in data.items():
            part = str(key)
            path = f"{prefix}{sep}{part}" if prefix else part
            out.update(flatten_value(value, path, sep=sep, max_depth=max_depth - 1))
        return out

    key = prefix or "value"
    if isinstance(data, (list, tuple)):
        return {key: json.dumps(data, ensure_ascii=False, default=str)}
    return {key: _scalar(data)}


def _scalar(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)
