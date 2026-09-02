"""Audit logging for tool invocations (FR-005).

Emits structured JSON audit entries to the
``agentic_devtools.orchestration.tools.audit`` logger at INFO level.
Each entry captures tool name, inputs, outputs, timing, and status.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import time
from typing import Any

from agentic_devtools.orchestration.execution.tracing import redact_sensitive_keys

logger = logging.getLogger("agentic_devtools.orchestration.tools.audit")


@dataclasses.dataclass(frozen=True)
class AuditEntry:
    """Schema for a single audit log record.

    Attributes:
        timestamp: ISO-8601 formatted timestamp.
        tool_name: Name of the invoked tool.
        input_summary: Redacted input parameters.
        output_summary: Truncated output description.
        duration_ms: Execution duration in milliseconds.
        status: One of ``"success"``, ``"error"``, ``"timeout"``,
            ``"dry_run_skipped"``, ``"validation_error"``,
            ``"precondition_not_met"``, ``"skipped_duplicate"``.
        error_type: Error category (None on success).
        error_message: Error details (None on success).
        correlation_id: Links to the current execution context.
    """

    timestamp: str
    tool_name: str
    input_summary: dict[str, Any]
    output_summary: str
    duration_ms: float
    status: str
    error_type: str | None = None
    error_message: str | None = None
    correlation_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        return dataclasses.asdict(self)


def _truncate(text: str, max_length: int) -> str:
    """Truncate *text* to *max_length* characters."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def _redact_output(value: Any) -> Any:
    """Recursively redact sensitive keys from tool output summaries."""
    if isinstance(value, dict):
        return redact_sensitive_keys(value)
    if isinstance(value, list):
        return [_redact_output(item) for item in value]
    return value


def _truncate_string_values(value: Any, max_str_length: int) -> Any:
    """Recursively truncate long string values in *value* before serialisation.

    This avoids allocating a huge JSON string just to discard most of it
    afterwards (e.g. when a filesystem_read_file tool returns megabytes of
    file content).  Only the *values* of dicts / list items are truncated;
    dict keys are left intact.
    """
    if isinstance(value, str):
        return _truncate(value, max_str_length)
    if isinstance(value, dict):
        return {k: _truncate_string_values(v, max_str_length) for k, v in value.items()}
    if isinstance(value, list):
        return [_truncate_string_values(item, max_str_length) for item in value]
    return value


def emit_audit_log(
    *,
    tool_name: str,
    inputs: dict[str, Any],
    output: Any,
    duration_ms: float,
    status: str,
    error_type: str | None = None,
    error_message: str | None = None,
    correlation_id: str = "",
    max_output_summary_length: int = 500,
) -> AuditEntry:
    """Emit a structured audit log entry.

    Returns the ``AuditEntry`` for testing purposes.
    """
    from datetime import datetime, timezone

    redacted_inputs = redact_sensitive_keys(inputs) if isinstance(inputs, dict) else inputs
    truncated_inputs = _truncate_string_values(redacted_inputs, max_output_summary_length)

    redacted_output = _redact_output(output)
    # Pre-truncate long string values *before* json.dumps so that tools
    # returning large payloads (e.g. filesystem_read_file) do not cause
    # expensive full serialisation followed by immediate discard.
    truncated_output = _truncate_string_values(redacted_output, max_output_summary_length)
    output_str = json.dumps(truncated_output, default=str) if truncated_output is not None else ""
    # Final safety net: the serialised JSON itself may still exceed the limit
    # if there are many fields, so truncate the string as well.
    output_summary = _truncate(output_str, max_output_summary_length)

    entry = AuditEntry(
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        tool_name=tool_name,
        input_summary=truncated_inputs,
        output_summary=output_summary,
        duration_ms=duration_ms,
        status=status,
        error_type=error_type,
        error_message=error_message,
        correlation_id=correlation_id,
    )

    logger.info(json.dumps(entry.to_dict(), default=str))
    return entry


def get_timestamp() -> float:
    """Return current time in seconds (for duration measurement)."""
    return time.time()
