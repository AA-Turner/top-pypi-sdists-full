"""Fastino GLiNER2 hosted-API provider (information extraction, not chat)."""
from .errors import (
    FastinoAuthError,
    FastinoError,
    FastinoServerError,
    FastinoValidationError,
)
from .fastino_api import FastinoExtraction, parse_spans
from .models import ExtractedSpan, SpanExtractionResult

__all__ = [
    "ExtractedSpan",
    "FastinoAuthError",
    "FastinoError",
    "FastinoExtraction",
    "FastinoServerError",
    "FastinoValidationError",
    "SpanExtractionResult",
    "parse_spans",
]
