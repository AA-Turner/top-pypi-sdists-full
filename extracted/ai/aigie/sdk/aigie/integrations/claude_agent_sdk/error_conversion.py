"""Pure span -> KytteError mapping for the Claude Agent SDK integration.

Mirrors sdk/aigie/integrations/langgraph/error_conversion.py. Every
per-framework error rule lives here so the adapter and platform have one
source of truth.
"""

from __future__ import annotations

import re
from typing import Any

from aigie.tracing.errors import KytteError

_TRANSIENT_HIGH = re.compile(
    r"(rate[_ ]?limit|429|timed?\s*out|timeout|5\d\d|service unavailable|overloaded|RESOURCE_EXHAUSTED)",
    re.IGNORECASE,
)
_PERMANENT_HIGH = re.compile(
    r"(authentication|invalid[_ ]api[_ ]key|401|403)",
    re.IGNORECASE,
)
_PERMANENT_MEDIUM = re.compile(
    r"(invalid_request|validation|bad request|400|PARSING_ERROR)",
    re.IGNORECASE,
)


def _raw_message(span: dict[str, Any]) -> str | None:
    for k in ("error", "error_message"):
        v = span.get(k)
        if isinstance(v, str) and v.strip():
            return v
    meta = span.get("metadata") or {}
    msg = meta.get("status_message")
    if isinstance(msg, str) and msg.strip():
        return msg
    out = span.get("output") or {}
    if isinstance(out, dict):
        v = out.get("error")
        if isinstance(v, str) and v.strip():
            return v
    return None


def _classify(message: str) -> tuple[str, bool]:
    if _TRANSIENT_HIGH.search(message):
        return "high", True
    if _PERMANENT_HIGH.search(message):
        return "high", False
    if _PERMANENT_MEDIUM.search(message):
        return "medium", False
    return "medium", False


def _source(span: dict[str, Any]) -> str:
    name = (span.get("name") or "").lower()
    span_type = (span.get("type") or "").lower()
    if "tool" in name or span_type == "tool":
        return "tool"
    if "llm" in name or "llm" in span_type or "model" in name:
        return "model"
    if span_type == "agent" or "subagent" in name or "agent" in name:
        return "node"
    return "framework"


def to_kytte_error(span: dict[str, Any]) -> KytteError | None:
    message = _raw_message(span)
    if not message:
        return None
    severity, is_transient = _classify(message)
    return KytteError(
        type=span.get("error_type") or "claude_agent_sdk_error",
        message=message,
        severity=severity,
        is_transient=is_transient,
        source=_source(span),
    )
