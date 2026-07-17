"""LangGraph failure → :class:`KytteError`.

Severity rules + probing body are shared (``error_conversion_base``); this file
owns LangGraph's ``source`` attribution, inferred from span name prefixes and
the ``langgraph_node`` metadata marker.
"""

from __future__ import annotations

from aigie.integrations.langgraph.control_flow import is_control_flow_error_type
from aigie.tracing.error_conversion_base import to_kytte_error as _to_kytte_error
from aigie.tracing.errors import KytteError


def _classify_source(span: dict, error_type: str | None) -> str:
    name = (span.get("name") or "").lower()
    metadata = span.get("metadata") or {}
    if name.startswith("tool:") or (error_type and "tool" in error_type.lower()):
        return "tool"
    if name.startswith("node:") or (error_type and "node" in error_type.lower()):
        return "node"
    if metadata.get("langgraph_node"):
        return "node"
    if metadata.get("provider"):
        return "model"
    return "framework"


def to_kytte_error(span: dict) -> KytteError | None:
    """Convert a LangGraph span dict into a :class:`KytteError`, or ``None``."""
    metadata = span.get("metadata") or {}
    error_type = span.get("error_type") or metadata.get("error_type")
    if is_control_flow_error_type(error_type):
        return None
    return _to_kytte_error(span, _classify_source)
