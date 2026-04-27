"""Lightweight diagnostic context for correlated debug logs."""

from __future__ import annotations

import contextvars
import logging
import re
import time
import uuid
from collections.abc import Mapping
from typing import Any

_MAX_TEXT = 160
_MAX_KEYS = 12
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_SECRET_KEY_RE = re.compile(r"(?i)(api[_-]?key|authorization|bearer|credential|password|secret|token)")
_SECRET_VALUE_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s,;}]+"),
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._\-]+"),
)
_LOG_RECORD_RESERVED = frozenset(logging.makeLogRecord({}).__dict__)

_diagnostic_context: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar(
    "anteroom_diagnostic_context",
    default={},
)


def new_turn_id(prefix: str = "turn") -> str:
    """Return a short opaque id suitable for correlating one user turn."""
    safe_prefix = re.sub(r"[^A-Za-z0-9_]", "_", prefix).strip("_") or "turn"
    return f"{safe_prefix}_{uuid.uuid4().hex[:12]}"


def set_diagnostic_context(**fields: Any) -> contextvars.Token[dict[str, Any]]:
    """Merge non-empty fields into the current diagnostic context."""
    current = dict(_diagnostic_context.get())
    for key, value in fields.items():
        if value is not None and value != "":
            current[key] = redact_value(value, key=key)
    return _diagnostic_context.set(current)


def reset_diagnostic_context(token: contextvars.Token[dict[str, Any]]) -> None:
    """Restore a context token returned by :func:`set_diagnostic_context`."""
    _diagnostic_context.reset(token)


def clear_diagnostic_context() -> contextvars.Token[dict[str, Any]]:
    """Clear diagnostic context for the current task."""
    return _diagnostic_context.set({})


def current_fields(**overrides: Any) -> dict[str, Any]:
    """Return current context fields plus sanitized overrides."""
    fields = dict(_diagnostic_context.get())
    for key, value in overrides.items():
        if value is not None:
            fields[key] = redact_value(value, key=key)
    return fields


def redact_value(value: Any, *, key: str | None = None) -> Any:
    """Return scalar-safe metadata for debug logging."""
    if key and _SECRET_KEY_RE.search(key):
        return "[redacted]"
    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        text = _CONTROL_RE.sub(" ", value)
        for pattern in _SECRET_VALUE_PATTERNS:
            text = pattern.sub("[redacted]", text)
        text = " ".join(text.split())
        if len(text) > _MAX_TEXT:
            text = text[: _MAX_TEXT - 1] + "..."
        return text
    if isinstance(value, Mapping):
        return shape_metadata(value)
    if isinstance(value, list | tuple | set | frozenset):
        return {"type": "array", "length": len(value)}
    return type(value).__name__


def shape_metadata(value: Any) -> dict[str, Any]:
    """Describe a value without exposing its raw contents."""
    if isinstance(value, Mapping):
        keys = sorted(str(redact_value(k)) for k in value.keys())
        return {"type": "object", "keys": keys[:_MAX_KEYS], "key_count": len(keys)}
    if isinstance(value, list | tuple | set | frozenset):
        return {"type": "array", "length": len(value)}
    if isinstance(value, str):
        return {"type": "string", "length": len(value)}
    if value is None:
        return {"type": "null"}
    return {"type": type(value).__name__}


def log_debug(logger: logging.Logger, event: str, /, **fields: Any) -> bool:
    """Emit a correlated debug event, avoiding field work unless DEBUG is enabled.

    Callable field values are evaluated only after the logger confirms DEBUG is
    active. This lets call sites pass cheap lambdas for shape metadata without
    doing serialization on normal runs.
    """
    if not logger.isEnabledFor(logging.DEBUG):
        return False

    started_at = fields.pop("_started_at", None)
    if started_at is not None and "elapsed_ms" not in fields:
        try:
            fields["elapsed_ms"] = round((time.monotonic() - float(started_at)) * 1000, 1)
        except (TypeError, ValueError):
            pass

    evaluated: dict[str, Any] = {}
    for key, value in fields.items():
        if callable(value):
            try:
                value = value()
            except Exception:
                value = "<field_error>"
        evaluated[key] = value

    payload = current_fields(event=event, **evaluated)
    extra = {_extra_key(key): value for key, value in payload.items()}
    logger.debug("%s %s", event, _format_fields(payload), extra=extra)
    return True


def _extra_key(key: str) -> str:
    return f"diag_{key}" if key in _LOG_RECORD_RESERVED else key


def _format_fields(fields: Mapping[str, Any]) -> str:
    parts: list[str] = []
    for key in sorted(fields):
        if key == "event":
            continue
        value = fields[key]
        if isinstance(value, dict):
            rendered = ",".join(f"{k}:{value[k]}" for k in sorted(value))
            parts.append(f"{key}={{{rendered}}}")
        else:
            parts.append(f"{key}={value!r}")
    return " ".join(parts)
