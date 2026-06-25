"""Shared span-dict → :class:`KytteError` conversion for callback integrations.

LangGraph and LangChain produce the same wire-shape span dicts, so the severity
rules + the probing body are shared here. ``source`` attribution differs per
framework, so each passes its own ``classify_source`` (its enricher only sees
its own framework's spans — emitters are per-adapter).
"""

from __future__ import annotations

import re
from collections.abc import Callable

from aigie.tracing.errors import KytteError

# HTTP-ish status codes (429, 4xx, 5xx) are matched as standalone tokens via
# ``\b`` so they don't spuriously match digits embedded in UUIDs / request ids /
# token counts. A GraphInterrupt's error message embeds a random ``id=<uuid>``;
# a bare-substring "403"/"503" check would flip severity at random whenever the
# UUID happened to contain those digits.
_TRANSIENT_HIGH = re.compile(
    r"\b(?:429|5\d\d)\b"
    r"|rate[_ ]?limit|resource_exhausted|quota|timed?\s*out|timeout"
    r"|deadline_exceeded|internal_server_error|service unavailable",
    re.IGNORECASE,
)
_PERMANENT_HIGH = re.compile(
    r"\b(?:401|403)\b|unauthorized|forbidden|invalid[_ ]?api[_ ]?key|authentication",
    re.IGNORECASE,
)
_PERMANENT_MEDIUM = re.compile(
    r"\b(?:400|404)\b|validation|invalid[_ ]?input|parsing|not[_ ]?found",
    re.IGNORECASE,
)


def classify_severity_transient(message: str) -> tuple[str, bool]:
    """Map an error message to ``(severity, is_transient)``."""
    if _TRANSIENT_HIGH.search(message):
        return "high", True
    if _PERMANENT_HIGH.search(message):
        return "high", False
    if _PERMANENT_MEDIUM.search(message):
        return "medium", False
    return "medium", False


def to_kytte_error(
    span: dict, classify_source: Callable[[dict, str | None], str]
) -> KytteError | None:
    """Convert a callback-integration span dict into a :class:`KytteError`.

    Returns ``None`` when the span has no error signals. Error fields aren't
    reliably at the top level, so we probe ``metadata`` and ``output`` too.
    ``classify_source`` is the framework's source-attribution function.
    """
    metadata: dict = span.get("metadata") or {}
    raw_output = span.get("output")
    output: dict = raw_output if isinstance(raw_output, dict) else {}

    error_field = span.get("error") or output.get("error") or metadata.get("error")
    if isinstance(error_field, dict):
        # metadata.error may already be the canonical KytteError blob from a
        # previous enrichment pass — don't recurse, treat as no raw error.
        error_field = None
    error_message = span.get("error_message") or metadata.get("status_message") or error_field
    error_type = span.get("error_type") or metadata.get("error_type") or output.get("error_type")
    status = span.get("status")

    if status != "error" and not error_field and not error_message:
        return None

    message = error_message or error_field or ""
    if not message and error_type:
        # Some real spans (e.g. GeneratorExit, CancelledError) carry no message
        # at all — surface the type string so downstream UIs always have
        # something non-empty to render.
        message = error_type
    raw = error_field if (error_field and error_field != message) else None

    source = classify_source(span, error_type)
    severity, is_transient = classify_severity_transient(message)

    return KytteError(
        type=error_type or "unknown",
        message=message,
        severity=severity,
        is_transient=is_transient,
        source=source,
        raw=raw,
    )
