from __future__ import annotations

from typing import Any

RAW_TRACE_KEY = "rawTrace"
LEGACY_RAW_TRACE_KEY = "externalTrace"


def raw_trace_key_of(payload: dict[str, Any]) -> str:
    if RAW_TRACE_KEY not in payload and LEGACY_RAW_TRACE_KEY in payload:
        return LEGACY_RAW_TRACE_KEY
    return RAW_TRACE_KEY


def raw_trace_of(payload: dict[str, Any]) -> Any:
    return payload.get(raw_trace_key_of(payload))
