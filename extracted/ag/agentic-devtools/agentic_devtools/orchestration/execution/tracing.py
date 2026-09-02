"""Tracing infrastructure — event schema and default emitter.

Provides the ``TraceEvent`` dataclass, a ``redact_sensitive_keys()``
utility, and a ``LoggingTraceEmitter`` that writes JSON to Python's
``logging`` module at DEBUG level.  Emit failures are swallowed with a
stderr warning — they never propagate into node execution.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Any

from .types import JSONValue

logger = logging.getLogger("agentic_devtools.orchestration.execution.tracing")

# ---------------------------------------------------------------------------
# Default redaction blocklist
# ---------------------------------------------------------------------------

_DEFAULT_BLOCKLIST: frozenset[str] = frozenset(
    {
        "token",
        "secret",
        "password",
        "api_key",
        "apikey",
        "pat",
        "authorization",
        "auth",
        "credential",
        "credentials",
    }
)


# ---------------------------------------------------------------------------
# TraceEvent dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TraceEvent:
    """A single trace event emitted during node execution.

    Attributes:
        timestamp: Epoch seconds (``time.time()``) when the event was created.
        node_name: Name of the emitting node.
        operation_type: ``"reasoning"`` or ``"tool_invocation"``.
        model_id: LLM model identifier (empty string for tool events).
        tool_name: Tool name (empty string for reasoning events).
        input_summary: Truncated/redacted input description.
        output_summary: Truncated/redacted output description.
        duration_ms: Wall-clock duration in milliseconds.
        success: Whether the operation succeeded.
        usage: Token-usage metadata (empty mapping when unavailable).
    """

    timestamp: float
    node_name: str
    operation_type: str
    model_id: str = ""
    tool_name: str = ""
    input_summary: str = ""
    output_summary: str = ""
    duration_ms: float = 0.0
    success: bool = True
    usage: dict[str, JSONValue] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Redaction utility
# ---------------------------------------------------------------------------


def _redact_list_item(item: Any, *, blocklist: frozenset[str]) -> Any:  # noqa: ANN401
    """Recursively redact a single list element."""
    if isinstance(item, dict):
        return redact_sensitive_keys(item, blocklist=blocklist)
    if isinstance(item, list):
        return [_redact_list_item(i, blocklist=blocklist) for i in item]
    return item


def redact_sensitive_keys(
    data: dict[str, Any],
    *,
    blocklist: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Return a redacted copy of *data* with sensitive values replaced.

    Keys whose lower-cased name appears in *blocklist* (default:
    ``_DEFAULT_BLOCKLIST``) have their values replaced with
    ``"[REDACTED]"``.  Redaction recurses into nested dicts and lists
    (including lists-of-lists) so deeply nested sensitive keys are also
    caught.
    """
    effective = blocklist if blocklist is not None else _DEFAULT_BLOCKLIST
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in effective:
            result[key] = "[REDACTED]"
        elif isinstance(value, dict):
            result[key] = redact_sensitive_keys(value, blocklist=effective)
        elif isinstance(value, list):
            result[key] = [_redact_list_item(item, blocklist=effective) for item in value]
        else:
            result[key] = value
    return result


# ---------------------------------------------------------------------------
# LoggingTraceEmitter — default TraceEmitter implementation
# ---------------------------------------------------------------------------


class LoggingTraceEmitter:
    """Emits ``TraceEvent`` instances as JSON via Python's ``logging`` module.

    Emission failures are caught and reported to *stderr* with metadata
    (node name and operation type only — no payload) so they can be
    diagnosed without leaking sensitive data.
    """

    def emit(self, event: TraceEvent) -> None:
        """Emit *event* as a JSON-formatted DEBUG log entry."""
        try:
            payload: dict[str, JSONValue] = {
                "timestamp": event.timestamp,
                "node_name": event.node_name,
                "operation_type": event.operation_type,
                "model_id": event.model_id,
                "tool_name": event.tool_name,
                "input_summary": event.input_summary,
                "output_summary": event.output_summary,
                "duration_ms": event.duration_ms,
                "success": event.success,
                "usage": event.usage,
            }
            logger.debug(json.dumps(payload, default=str))
        except Exception as exc:  # noqa: BLE001
            exc_type = type(exc).__name__
            print(
                f"[TraceEmitter] emit failed for node={event.node_name} op={event.operation_type}: {exc_type}",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Helper — create a trace event with auto-timestamp
# ---------------------------------------------------------------------------


def make_trace_event(
    *,
    node_name: str,
    operation_type: str,
    model_id: str = "",
    tool_name: str = "",
    input_summary: str = "",
    output_summary: str = "",
    duration_ms: float = 0.0,
    success: bool = True,
    usage: dict[str, JSONValue] | None = None,
) -> TraceEvent:
    """Convenience factory that auto-sets ``timestamp`` to ``time.time()``."""
    return TraceEvent(
        timestamp=time.time(),
        node_name=node_name,
        operation_type=operation_type,
        model_id=model_id,
        tool_name=tool_name,
        input_summary=input_summary,
        output_summary=output_summary,
        duration_ms=duration_ms,
        success=success,
        usage=usage or {},
    )
