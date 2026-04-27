"""Best-effort redacted diagnostics error log.

This is intentionally separate from ``services.audit``. Diagnostics entries are
short-lived support artifacts with cheap append semantics, not tamper-evident
governance records.
"""

from __future__ import annotations

import json
import logging
import re
import stat
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s,;}]+"),
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._\-]+"),
)
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_SENSITIVE_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "bearer",
    "content",
    "input",
    "arguments",
    "args",
    "output",
    "password",
    "prompt",
    "raw_messages",
    "raw_tokens",
    "response",
    "secret",
    "token_text",
    "tool_arguments",
    "tool_input",
    "tool_output",
}

_SUCCESS_STOP_REASONS = {"completed", "done", "stop", "end_turn", "length", "max_tokens"}
_ERROR_STOP_HINTS = (
    "block",
    "cancel",
    "compaction",
    "context_length",
    "dlp",
    "error",
    "exception",
    "failed",
    "filter",
    "internal",
    "timeout",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _json_line_size(entry: dict[str, Any]) -> int:
    return len(json.dumps(entry, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) + 1


def _sanitize_string(value: str, *, max_chars: int = 512) -> str:
    text = _CONTROL_RE.sub(" ", value)
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub("[redacted]", text)
    text = " ".join(text.split())
    if len(text) > max_chars:
        return text[: max_chars - 1] + "..."
    return text


def _safe_key(key: Any) -> str:
    return _sanitize_string(str(key), max_chars=96)


def _redact_value(key: str, value: Any, *, depth: int = 0) -> Any:
    if depth > 8:
        return "[truncated]"
    lowered = key.lower().replace("-", "_")
    if lowered in _SENSITIVE_KEYS or lowered.endswith("_content"):
        if isinstance(value, str):
            return {"redacted": True, "chars": len(value)}
        if isinstance(value, list | tuple | set | dict):
            return {"redacted": True, "type": type(value).__name__}
        return "[redacted]"
    if isinstance(value, str):
        return _sanitize_string(value)
    if isinstance(value, dict):
        return {_safe_key(k): _redact_value(str(k), v, depth=depth + 1) for k, v in value.items()}
    if isinstance(value, list | tuple | set):
        return [_redact_value(key, item, depth=depth + 1) for item in list(value)[:200]]
    if isinstance(value, bool | int | float) or value is None:
        return value
    return _sanitize_string(str(value), max_chars=160)


def normalize_summary_for_log(summary: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative redacted copy suitable for diagnostics JSONL."""
    redacted = _redact_value("summary", summary)
    return redacted if isinstance(redacted, dict) else {}


def should_log_summary(summary: dict[str, Any], *, log_successful_debug_turns: bool = False) -> bool:
    """Classify terminal debug summaries for failure-only diagnostics logging."""
    if log_successful_debug_turns:
        return True
    if not isinstance(summary, dict):
        return False
    if summary.get("errors"):
        return True
    stop_reason = str(summary.get("stop_reason") or "").lower()
    if stop_reason and stop_reason not in _SUCCESS_STOP_REASONS:
        return any(hint in stop_reason for hint in _ERROR_STOP_HINTS)
    for event in summary.get("runtime_events") or []:
        kind = str(event.get("kind") if isinstance(event, dict) else event).lower()
        if kind in {"cancelled", "dlp_blocked", "output_filter_blocked"}:
            return True
        if "failed" in kind or "error" in kind or "blocked" in kind:
            return True
    for tool in summary.get("tools") or []:
        if isinstance(tool, dict) and str(tool.get("status") or "").lower() in {"error", "failed", "blocked"}:
            return True
    if summary.get("active_tools") and stop_reason in {"cancelled", "timeout", "internal_error"}:
        return True
    return False


@dataclass
class DiagnosticsWriteResult:
    written: bool
    path: Path | None = None
    reason: str = ""


class DiagnosticsLogWriter:
    """Append redacted diagnostics entries with bounded filesystem impact."""

    def __init__(
        self,
        log_dir: Path,
        *,
        enabled: bool = True,
        log_successful_debug_turns: bool = False,
        redact_content: bool = True,
        retention_days: int = 14,
        rotate_size_bytes: int = 1_048_576,
        max_entry_bytes: int = 32_768,
        max_log_dir_bytes: int = 10_485_760,
    ) -> None:
        self.log_dir = log_dir
        self.enabled = enabled
        self.log_successful_debug_turns = log_successful_debug_turns
        self.redact_content = redact_content
        self.retention_days = retention_days
        self.rotate_size_bytes = rotate_size_bytes
        self.max_entry_bytes = max_entry_bytes
        self.max_log_dir_bytes = max_log_dir_bytes
        self.disabled_reason = ""
        self._warned = False
        self._last_cleanup = 0.0

        if self.enabled:
            try:
                self.log_dir.mkdir(parents=True, exist_ok=True)
                try:
                    self.log_dir.chmod(stat.S_IRWXU)
                except OSError:
                    pass
            except OSError as exc:
                self.enabled = False
                self.disabled_reason = f"unwritable diagnostics log directory: {exc}"
                self._warn_once(self.disabled_reason)

    @property
    def active_path(self) -> Path:
        return self._log_path()

    def _log_path(self, date_str: str | None = None) -> Path:
        if date_str is None:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self.log_dir / f"diagnostics-{date_str}.jsonl"

    def write_summary(
        self,
        summary: dict[str, Any],
        *,
        interface: str,
        conversation_id: str = "",
        request_id: str = "",
        turn_id: str = "",
    ) -> DiagnosticsWriteResult:
        """Persist one terminal debug summary if configured and classified loggable."""
        if not self.enabled:
            return DiagnosticsWriteResult(False, reason=self.disabled_reason or "disabled")
        if not should_log_summary(summary, log_successful_debug_turns=self.log_successful_debug_turns):
            return DiagnosticsWriteResult(False, reason="not_loggable")

        try:
            self._maybe_cleanup()
            self._maybe_rotate()
            safe_summary = normalize_summary_for_log(summary) if self.redact_content else dict(summary)
            entry = {
                "version": 1,
                "timestamp": _utc_now(),
                "interface": _sanitize_string(interface, max_chars=32),
                "conversation_id": _sanitize_string(conversation_id, max_chars=120),
                "request_id": _sanitize_string(request_id, max_chars=120),
                "turn_id": _sanitize_string(turn_id, max_chars=120),
                "stop_reason": safe_summary.get("stop_reason"),
                "final_phase": safe_summary.get("final_phase"),
                "model": safe_summary.get("model"),
                "usage": safe_summary.get("usage"),
                "retries": safe_summary.get("retries"),
                "active_tools": safe_summary.get("active_tools"),
                "runtime_events": safe_summary.get("runtime_events"),
                "errors": safe_summary.get("errors"),
                "summary": safe_summary,
                "redaction": {
                    "raw_prompts": "omitted",
                    "raw_tokens": "omitted",
                    "raw_tool_arguments": "omitted",
                    "raw_tool_output": "omitted",
                    "raw_messages": "omitted",
                },
            }
            entry = self._fit_entry(entry)
            line = json.dumps(entry, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
            path = self._log_path()
            with open(path, "ab") as handle:
                if fcntl is not None:
                    fcntl.flock(handle, fcntl.LOCK_EX)
                try:
                    handle.write(line)
                    handle.flush()
                finally:
                    if fcntl is not None:
                        fcntl.flock(handle, fcntl.LOCK_UN)
            try:
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            except OSError:
                pass
            return DiagnosticsWriteResult(True, path=path)
        except OSError as exc:
            self.disabled_reason = f"diagnostics log write failed: {exc}"
            self.enabled = False
            self._warn_once(self.disabled_reason)
            return DiagnosticsWriteResult(False, path=self._log_path(), reason=self.disabled_reason)
        except Exception as exc:
            self.disabled_reason = f"diagnostics log skipped: {exc}"
            self._warn_once(self.disabled_reason)
            return DiagnosticsWriteResult(False, path=self._log_path(), reason=self.disabled_reason)

    def _fit_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        if _json_line_size(entry) <= self.max_entry_bytes:
            return entry
        fitted = dict(entry)
        summary = dict(fitted.get("summary") or {})
        summary["phases"] = list(summary.get("phases") or [])[:10]
        summary["tools"] = list(summary.get("tools") or [])[:10]
        summary["runtime_events"] = list(summary.get("runtime_events") or [])[:10]
        summary["retries"] = list(summary.get("retries") or [])[:5]
        summary["errors"] = list(summary.get("errors") or [])[:5]
        summary["diagnostics_truncated"] = True
        fitted["summary"] = summary
        fitted["runtime_events"] = summary.get("runtime_events")
        fitted["retries"] = summary.get("retries")
        fitted["errors"] = summary.get("errors")
        if _json_line_size(fitted) <= self.max_entry_bytes:
            return fitted
        for key in ("phases", "tools", "runtime_events", "retries"):
            summary.pop(key, None)
        summary["diagnostics_truncated"] = True
        fitted["summary"] = summary
        fitted["runtime_events"] = []
        fitted["retries"] = []
        fitted["active_tools"] = []
        if _json_line_size(fitted) <= self.max_entry_bytes:
            return fitted
        return {
            "version": 1,
            "timestamp": fitted["timestamp"],
            "interface": fitted["interface"],
            "conversation_id": fitted["conversation_id"],
            "request_id": fitted["request_id"],
            "turn_id": fitted["turn_id"],
            "stop_reason": fitted.get("stop_reason"),
            "final_phase": fitted.get("final_phase"),
            "model": fitted.get("model"),
            "errors": fitted.get("errors") or [],
            "summary": {"diagnostics_truncated": True},
            "redaction": fitted["redaction"],
        }

    def _maybe_rotate(self) -> None:
        path = self._log_path()
        try:
            if path.exists() and path.stat().st_size >= self.rotate_size_bytes:
                rotated = path.with_name(f"{path.stem}.{int(time.time() * 1000)}{path.suffix}")
                path.rename(rotated)
        except OSError as exc:
            self._warn_once(f"diagnostics log rotation skipped: {exc}")

    def _maybe_cleanup(self) -> None:
        now = time.time()
        if now - self._last_cleanup < 60:
            return
        self._last_cleanup = now
        self.purge_old_logs()
        self.enforce_directory_size()

    def purge_old_logs(self) -> int:
        if not self.enabled or self.retention_days <= 0:
            return 0
        cutoff = time.time() - (self.retention_days * 86400)
        deleted = 0
        try:
            for path in self.log_dir.glob("diagnostics-*.jsonl*"):
                try:
                    if path.stat().st_mtime < cutoff:
                        path.unlink()
                        deleted += 1
                except OSError:
                    pass
        except OSError:
            pass
        return deleted

    def enforce_directory_size(self) -> int:
        if not self.enabled or self.max_log_dir_bytes <= 0:
            return 0
        try:
            files = [p for p in self.log_dir.glob("diagnostics-*.jsonl*") if p.is_file()]
            sizes = [(p, p.stat().st_size, p.stat().st_mtime) for p in files]
        except OSError:
            return 0
        total = sum(size for _, size, _ in sizes)
        deleted = 0
        for path, size, _mtime in sorted(sizes, key=lambda item: item[2]):
            if total <= self.max_log_dir_bytes:
                break
            try:
                path.unlink()
                total -= size
                deleted += 1
            except OSError:
                pass
        return deleted

    def _warn_once(self, message: str) -> None:
        if self._warned:
            return
        self._warned = True
        logger.warning("%s", message)


def create_diagnostics_log_writer(config: Any) -> DiagnosticsLogWriter:
    """Factory for app/CLI diagnostics logging."""
    cfg = getattr(config, "diagnostics", None)
    if cfg is None:
        return DiagnosticsLogWriter(Path.home() / ".anteroom" / "diagnostics", enabled=False)
    enabled = getattr(cfg, "error_log_enabled", True)
    if not isinstance(enabled, bool):
        return DiagnosticsLogWriter(Path.home() / ".anteroom" / "diagnostics", enabled=False)
    raw_log_path = getattr(cfg, "log_path", "")
    data_dir = getattr(getattr(config, "app", None), "data_dir", "")
    if raw_log_path:
        log_dir = (
            Path(raw_log_path).expanduser()
            if isinstance(raw_log_path, str)
            else Path.home() / ".anteroom" / "diagnostics"
        )
    elif isinstance(data_dir, Path):
        log_dir = data_dir / "diagnostics"
    elif isinstance(data_dir, str) and data_dir:
        log_dir = Path(data_dir).expanduser() / "diagnostics"
    else:
        return DiagnosticsLogWriter(Path.home() / ".anteroom" / "diagnostics", enabled=False)
    return DiagnosticsLogWriter(
        log_dir,
        enabled=enabled,
        log_successful_debug_turns=bool(getattr(cfg, "log_successful_debug_turns", False)),
        redact_content=bool(getattr(cfg, "redact_content", True)),
        retention_days=int(getattr(cfg, "retention_days", 14)),
        rotate_size_bytes=int(getattr(cfg, "rotate_size_bytes", 1_048_576)),
        max_entry_bytes=int(getattr(cfg, "max_entry_bytes", 32_768)),
        max_log_dir_bytes=int(getattr(cfg, "max_log_dir_bytes", 10_485_760)),
    )
