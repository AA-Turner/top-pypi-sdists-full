"""Best-effort API transport trace dumping."""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API_TRACE_DIR_ENV = "CORTEX_CODE_AGENT_SDK_API_TRACE_DIR"
_trace_sink_sequence = 0
_REDACTED = "[REDACTED]"
_SENSITIVE_KEY_RE = re.compile(
    r"(authorization|credential|password|secret|token|sessiontoken|session[_-]?token)",
    re.IGNORECASE,
)
_STRING_REDACTIONS = (
    (
        re.compile(r'(Snowflake\s+Token=)"[^"]*"', re.IGNORECASE),
        r'\1"' + _REDACTED + '"',
    ),
    (
        re.compile(r"(\bAuthorization\s*[:=]\s*)(Bearer\s+)?[^\s,\n}]+", re.IGNORECASE),
        rf"\1\2{_REDACTED}",
    ),
    (
        re.compile(
            r'("?(?:access[_-]?token|refresh[_-]?token|session[_-]?token|token|'
            r'password|secret|credential|authorization)"?\s*[:=]\s*)("[^"]*"|[^\s,}&]+)',
            re.IGNORECASE,
        ),
        r'\1"' + _REDACTED + '"',
    ),
)


class _ApiTraceSink:
    def __init__(self, directory: str):
        global _trace_sink_sequence
        _trace_sink_sequence += 1
        self._directory = Path(directory)
        self._sequence = 0
        self._prefix = f"{int(time.time() * 1000)}-{os.getpid()}-{_trace_sink_sequence}"

    def write_json(self, label: str, data: Mapping[str, Any]) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        }
        self._write_file(
            label, "json", json.dumps(_redact_trace_value(payload), indent=2)
        )

    def write_text(self, label: str, extension: str, data: str) -> None:
        self._write_file(label, extension, _redact_trace_string(data))

    def _write_file(self, label: str, extension: str, data: str) -> None:
        try:
            self._directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            os.chmod(self._directory, 0o700)
            self._sequence += 1
            safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "-", label)
            path = (
                self._directory
                / f"{self._prefix}-{self._sequence:04d}-{safe_label}.{extension}"
            )
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                file.write(data)
            os.chmod(path, 0o600)
        except Exception:
            # API tracing is diagnostic-only and should never change SDK behavior.
            return


def _create_api_trace_sink(env: Mapping[str, str]) -> _ApiTraceSink | None:
    directory = env.get(API_TRACE_DIR_ENV)
    return _ApiTraceSink(directory) if directory else None


def _redact_trace_value(value: Any, key: str | None = None) -> Any:
    if key is not None and _SENSITIVE_KEY_RE.search(key):
        return _REDACTED
    if isinstance(value, Mapping):
        return {
            str(child_key): _redact_trace_value(child_value, str(child_key))
            for child_key, child_value in value.items()
        }
    if isinstance(value, list):
        return [_redact_trace_value(item) for item in value]
    if isinstance(value, str):
        return _redact_trace_string(value)
    return value


def _redact_trace_string(value: str) -> str:
    redacted = value
    for pattern, replacement in _STRING_REDACTIONS:
        redacted = pattern.sub(replacement, redacted)
    return redacted
