"""Pipecat span dict → :class:`KytteError`."""

from __future__ import annotations

from aigie.tracing.error_conversion_base import to_kytte_error as _to_kytte_error
from aigie.tracing.errors import KytteError


def _classify_source(span: dict, _error_type: str | None) -> str:
    span_type = (span.get("type") or "").lower()
    if span_type == "llm":
        return "model"
    if span_type == "tool":
        # STT/TTS are provider model calls wearing a tool span, because
        # OpenInference has no audio span kind; a function call is a real tool.
        modality = (span.get("metadata") or {}).get("modality")
        return "model" if modality in ("stt", "tts") else "tool"
    if span_type == "chain":
        return "node"
    return "framework"


def to_kytte_error(span: dict) -> KytteError | None:
    """Convert a Pipecat span dict into a :class:`KytteError`, or ``None``."""
    return _to_kytte_error(span, _classify_source)
