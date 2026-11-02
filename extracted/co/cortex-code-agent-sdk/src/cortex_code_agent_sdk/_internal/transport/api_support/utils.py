"""Small shared helpers for direct Agent API transport."""

from __future__ import annotations

import json
from typing import Any


def _empty_usage() -> dict[str, int]:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_write_input_tokens": 0,
    }

def _add_usage(target: dict[str, int], usage: dict[str, int]) -> None:
    for key in target:
        target[key] += int(usage.get(key, 0))

def _parse_json_object(input_json: str) -> dict[str, Any]:
    if not input_json.strip():
        return {}
    try:
        value = json.loads(input_json)
    except json.JSONDecodeError:
        return {}
    return _as_record(value)

def _as_record(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
