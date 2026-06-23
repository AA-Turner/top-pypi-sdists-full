"""LangGraph-specific failure → :class:`KytteError` conversion.

Pure function. Takes a span payload (dict shape that hits the wire) and
returns the canonical :class:`KytteError`, or ``None`` if the span does
not look like a failure.

The conversion is intentionally simple: this is not a classifier with a
giant enum. It inspects a handful of existing span fields and chooses
``source``, ``severity``, and ``is_transient``. The ``type`` field stays
a free-form string (whatever the framework already produced).
"""

from __future__ import annotations

import re

from aigie.tracing.errors import KytteError

# HTTP-ish status codes (429, 4xx, 5xx) are matched as standalone tokens via
# ``\b`` so they don't spuriously match digits embedded in UUIDs / request ids /
# token counts. A GraphInterrupt's error message embeds a random ``id=<uuid>``;
# a bare-substring "403"/"503" check would flip an interrupt's severity at
# random whenever the UUID happened to contain those digits.
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


def to_kytte_error(span: dict) -> KytteError | None:
    """Convert a LangGraph span dict into a :class:`KytteError`.

    Returns ``None`` when the span has no error signals (caller should
    have already filtered, but we keep this defensive).

    LangGraph error spans on the wire don't reliably put error fields at
    the top level — the legacy callback duplicates them into
    ``metadata`` and ``output``. We probe both for robustness so
    realistic wire shapes still produce a useful classification.
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
        # Some real spans (e.g. GeneratorExit, CancelledError) carry no
        # message at all — surface the type string so downstream UIs
        # always have something non-empty to render.
        message = error_type
    raw = error_field if (error_field and error_field != message) else None

    source = _classify_source(span, error_type)
    severity, is_transient = _classify_severity_transient(message)

    return KytteError(
        type=error_type or "unknown",
        message=message,
        severity=severity,
        is_transient=is_transient,
        source=source,
        raw=raw,
    )


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


def _classify_severity_transient(message: str) -> tuple[str, bool]:
    if _TRANSIENT_HIGH.search(message):
        return "high", True
    if _PERMANENT_HIGH.search(message):
        return "high", False
    if _PERMANENT_MEDIUM.search(message):
        return "medium", False
    return "medium", False
