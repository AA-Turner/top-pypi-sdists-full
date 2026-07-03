"""Strands span dict → :class:`KytteError`."""

from __future__ import annotations

from aigie.tracing.error_conversion_base import to_kytte_error as _to_kytte_error
from aigie.tracing.errors import KytteError


def _classify_source(span: dict, _error_type: str | None) -> str:
    span_type = (span.get("type") or "").lower()
    if span_type == "tool":
        return "tool"
    if span_type == "llm":
        return "model"
    if span_type == "subgraph_workflow":
        return "node"
    return "framework"


def to_kytte_error(span: dict) -> KytteError | None:
    """Convert a Strands span dict into a :class:`KytteError`, or ``None``."""
    return _to_kytte_error(span, _classify_source)
