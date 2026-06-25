"""LangChain failure → :class:`KytteError`.

Severity rules + probing body are shared (``error_conversion_base``); this file
owns LangChain's ``source`` attribution, inferred from the span ``type``
(LangChain has no ``langgraph_node`` marker).
"""

from __future__ import annotations

from aigie.tracing.error_conversion_base import to_kytte_error as _to_kytte_error
from aigie.tracing.errors import KytteError


def _classify_source(span: dict, error_type: str | None) -> str:
    name = (span.get("name") or "").lower()
    span_type = (span.get("span_type") or span.get("type") or "").lower()
    metadata = span.get("metadata") or {}
    if (
        span_type == "tool"
        or name.startswith("tool:")
        or (error_type and "tool" in error_type.lower())
    ):
        return "tool"
    if span_type == "llm" or metadata.get("provider") or metadata.get("model"):
        return "model"
    if span_type in ("chain", "workflow"):
        return "node"
    return "framework"


def to_kytte_error(span: dict) -> KytteError | None:
    """Convert a LangChain span dict into a :class:`KytteError`, or ``None``."""
    return _to_kytte_error(span, _classify_source)
