"""Opt-in per-turn debug diagnostics.

The collector consumes the shared ``AgentEvent`` stream and produces a small
redacted summary for CLI/web troubleshooting. It is not an audit log and does
not persist data.
"""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

_MAX_TEXT = 240
_MAX_EVENTS = 30
_MAX_TOOLS = 50
_MAX_RETRIES = 20
_MAX_PHASES = 40
_SNAPSHOT_EVENTS = 10
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s,;}]+"),
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._\-]+"),
)


def should_log_summary(summary: dict[str, Any], *, log_successful_debug_turns: bool = False) -> bool:
    """Return true when a terminal redacted summary should be persisted."""
    from .diagnostics_log import should_log_summary as _should_log_summary

    return _should_log_summary(summary, log_successful_debug_turns=log_successful_debug_turns)


def normalize_summary_for_log(summary: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative redacted copy suitable for diagnostics persistence."""
    from .diagnostics_log import normalize_summary_for_log as _normalize_summary_for_log

    return _normalize_summary_for_log(summary)


def _round_seconds(value: float | int | None) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 3)
    except (TypeError, ValueError):
        return None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sanitize_diagnostic_text(value: Any, *, max_chars: int = _MAX_TEXT) -> str:
    """Return short single-line diagnostic text with obvious secrets removed."""
    text = str(value or "")
    text = _CONTROL_RE.sub(" ", text)
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub("[redacted]", text)
    text = " ".join(text.split())
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "..."
    return text


def _sanitize_text(value: Any, *, max_chars: int = _MAX_TEXT) -> str:
    return sanitize_diagnostic_text(value, max_chars=max_chars)


def _safe_str_list(value: Any, *, max_items: int = 8) -> list[str]:
    if not isinstance(value, list | tuple | set):
        return []
    result: list[str] = []
    for item in value:
        safe = _sanitize_text(item, max_chars=80)
        if safe:
            result.append(safe)
        if len(result) >= max_items:
            break
    return result


def _safe_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _argument_shape(arguments: Any) -> dict[str, Any]:
    """Return argument metadata without raw values."""
    if isinstance(arguments, dict):
        keys = sorted(_sanitize_text(k, max_chars=64) for k in arguments.keys())
        return {"type": "object", "keys": keys[:12], "key_count": len(keys)}
    if isinstance(arguments, list):
        return {"type": "array", "length": len(arguments)}
    if arguments is None:
        return {"type": "null"}
    return {"type": type(arguments).__name__}


def _output_shape(output: Any) -> dict[str, Any]:
    """Return output metadata without raw output content."""
    if isinstance(output, dict):
        keys = sorted(_sanitize_text(k, max_chars=64) for k in output.keys() if not str(k).startswith("_"))
        shape: dict[str, Any] = {"type": "object", "keys": keys[:12], "key_count": len(keys)}
        for key in ("exit_code", "status", "error_code"):
            if key in output and not isinstance(output.get(key), dict | list):
                shape[key] = _sanitize_text(output.get(key), max_chars=80)
        if "error" in output:
            shape["has_error"] = True
        return shape
    if isinstance(output, list):
        return {"type": "array", "length": len(output)}
    if isinstance(output, str):
        return {"type": "string", "length": len(output)}
    if output is None:
        return {"type": "null"}
    return {"type": type(output).__name__}


@dataclass
class _PhaseRecord:
    phase: str
    started_at: float
    duration_seconds: float | None = None
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class _ToolRecord:
    id: str
    name: str
    started_at: float
    argument_shape: dict[str, Any]
    status: str = "running"
    duration_seconds: float | None = None
    output_shape: dict[str, Any] | None = None
    approval_decision: str | None = None
    hook_blocked: bool = False
    iteration: int | None = None
    timeout_seconds: float | None = None
    first_response_elapsed_seconds: float | None = None
    execution_elapsed_seconds: float | None = None


class DebugDiagnosticsCollector:
    """Collect a redacted per-turn diagnostic summary."""

    def __init__(
        self,
        *,
        provider: str | None = None,
        model: str | None = None,
        turn_id: str | None = None,
        request_id: str | None = None,
        interface: str | None = None,
        conversation_id: str | None = None,
        clock: Callable[[], float] | None = None,
        wall_clock: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or time.monotonic
        self._wall_clock = wall_clock or _utc_now
        self._start = self._clock()
        self._started_at = self._wall_clock()
        self._provider = provider or ""
        self._model = model or ""
        self._turn_id = _sanitize_text(turn_id, max_chars=120) if turn_id else None
        self._request_id = _sanitize_text(request_id, max_chars=120) if request_id else None
        self._interface = _sanitize_text(interface, max_chars=40) if interface else None
        self._conversation_id = _sanitize_text(conversation_id, max_chars=120) if conversation_id else None
        self._phases: list[_PhaseRecord] = []
        self._current_phase: _PhaseRecord | None = None
        self._tools: dict[str, _ToolRecord] = {}
        self._tool_order: list[str] = []
        self._retries: list[dict[str, Any]] = []
        self._runtime_events: list[dict[str, Any]] = []
        self._errors: list[dict[str, Any]] = []
        self._usage: dict[str, Any] = {}
        self._counters = {"tokens": 0, "token_chars": 0, "assistant_chars": 0}
        self._stop_reason = "running"
        self._finished = False
        self._ended_at: str | None = None
        self._end = self._start

    def observe(self, kind: str, data: dict[str, Any] | None = None) -> None:
        """Consume one agent event."""
        data = data or {}
        now = self._clock()

        if kind == "phase":
            self._start_phase(_sanitize_text(data.get("phase") or "unknown", max_chars=80), data, now)
        elif kind == "thinking":
            self._add_runtime_event("thinking", {})
        elif kind == "retrying":
            self._add_retry(data)
            self._start_phase("retrying", data, now)
        elif kind == "token":
            content = data.get("content", "")
            self._counters["tokens"] += 1
            self._counters["token_chars"] += len(content) if isinstance(content, str) else 0
            if self._current_phase is None or self._current_phase.phase in ("connecting", "waiting", "retrying"):
                self._start_phase("streaming", data, now)
        elif kind == "usage":
            self._usage = {
                key: data.get(key)
                for key in ("prompt_tokens", "completion_tokens", "total_tokens", "estimated", "model")
                if key in data
            }
        elif kind == "tool_call_start":
            self._start_tool(data, now)
        elif kind == "tool_call_end":
            self._finish_tool(data, now)
        elif kind == "assistant_message":
            content = data.get("content", "")
            self._counters["assistant_chars"] += len(content) if isinstance(content, str) else 0
        elif kind == "queued_message":
            self._add_runtime_event(
                "queued_message",
                {
                    "position": data.get("position"),
                    "queue_depth": data.get("queue_depth"),
                    "content_chars": len(data.get("content", "")) if isinstance(data.get("content"), str) else 0,
                },
            )
        elif kind in {
            "compaction",
            "dlp_blocked",
            "dlp_warning",
            "output_filter_blocked",
            "output_filter_warning",
            "injection_detected",
            "budget_warning",
            "workflow_pause",
            "auto_plan_suggest",
            "cancelled",
        }:
            self._add_runtime_event(kind, self._sanitize_runtime_payload(kind, data))
            if kind in {"dlp_blocked", "output_filter_blocked", "cancelled"}:
                self._stop_reason = kind
        elif kind == "error":
            self._stop_reason = _sanitize_text(data.get("code") or "error", max_chars=80)
            error = {
                "code": _sanitize_text(data.get("code") or "", max_chars=80),
                "message": _sanitize_text(
                    data.get("display_message") or data.get("message") or "error",
                    max_chars=160,
                ),
                "retryable": bool(data.get("retryable", False)),
            }
            for key in ("elapsed_seconds", "timeout_seconds"):
                if key in data:
                    error[key] = _round_seconds(data.get(key))
            for key in ("timeout_type", "error_type", "provider", "model", "iteration"):
                if key in data:
                    value = (
                        _safe_int(data.get(key)) if key == "iteration" else _sanitize_text(data.get(key), max_chars=120)
                    )
                    if value is not None and value != "":
                        error[key] = value
            self._errors.append(error)
        elif kind == "done":
            if self._stop_reason == "running":
                self._stop_reason = _sanitize_text(data.get("stop_reason") or "completed", max_chars=80)

    def finish(self, stop_reason: str | None = None) -> dict[str, Any]:
        """Return a finalized serializable summary."""
        if not self._finished:
            self._end = self._clock()
            self._ended_at = self._wall_clock()
            if self._current_phase and self._current_phase.duration_seconds is None:
                self._current_phase.duration_seconds = max(0.0, self._end - self._current_phase.started_at)
            for tool in self._tools.values():
                if tool.status == "running":
                    tool.duration_seconds = max(0.0, self._end - tool.started_at)
            self._finished = True
        if stop_reason and self._stop_reason == "running":
            self._stop_reason = _sanitize_text(stop_reason, max_chars=80)

        return {
            "version": 2,
            "turn_id": self._turn_id,
            "request_id": self._request_id or self._turn_id,
            "interface": self._interface,
            "conversation_id": self._conversation_id,
            "correlation": {
                "turn_id": self._turn_id,
                "request_id": self._request_id or self._turn_id,
                "interface": self._interface,
                "conversation_id": self._conversation_id,
            },
            "started_at": self._started_at,
            "ended_at": self._ended_at,
            "total_duration_seconds": _round_seconds(self._end - self._start),
            "stop_reason": self._stop_reason,
            "final_phase": self._current_phase.phase if self._current_phase else None,
            "model": {
                "provider": self._provider or None,
                "name": self._usage.get("model") or self._model or None,
            },
            "usage": dict(self._usage),
            "retries": self._retries[:_MAX_RETRIES],
            "phases": [
                {
                    "phase": phase.phase,
                    "duration_seconds": _round_seconds(phase.duration_seconds),
                    **phase.data,
                }
                for phase in self._phases[:_MAX_PHASES]
            ],
            "tools": [self._serialize_tool(self._tools[tid]) for tid in self._tool_order[:_MAX_TOOLS]],
            "active_tools": [self._serialize_tool(tool) for tool in self._tools.values() if tool.status == "running"][
                :8
            ],
            "runtime_events": self._runtime_events[:_MAX_EVENTS],
            "errors": self._errors[:8],
            "counters": dict(self._counters),
            "redaction": {
                "raw_tokens": "omitted",
                "raw_prompts": "omitted",
                "raw_tool_arguments": "omitted",
                "raw_tool_output": "omitted",
                "raw_messages": "omitted",
            },
        }

    def snapshot(self) -> dict[str, Any]:
        """Return a redacted live snapshot without finalizing the turn."""
        now = self._clock()
        current_phase = None
        if self._current_phase is not None:
            current_phase = {
                "phase": self._current_phase.phase,
                "age_seconds": _round_seconds(now - self._current_phase.started_at),
                **self._current_phase.data,
            }
        return {
            "version": 2,
            "turn_id": self._turn_id,
            "request_id": self._request_id or self._turn_id,
            "interface": self._interface,
            "conversation_id": self._conversation_id,
            "correlation": {
                "turn_id": self._turn_id,
                "request_id": self._request_id or self._turn_id,
                "interface": self._interface,
                "conversation_id": self._conversation_id,
            },
            "started_at": self._started_at,
            "age_seconds": _round_seconds(now - self._start),
            "stop_reason": self._stop_reason,
            "current_phase": current_phase,
            "model": {
                "provider": self._provider or None,
                "name": self._usage.get("model") or self._model or None,
            },
            "active_tools": [
                self._serialize_tool(tool, now=now) for tool in self._tools.values() if tool.status == "running"
            ][:8],
            "recent_events": self._runtime_events[-_SNAPSHOT_EVENTS:],
            "retries": self._retries[-5:],
            "errors": self._errors[-3:],
            "counters": dict(self._counters),
            "redaction": {
                "raw_tokens": "omitted",
                "raw_prompts": "omitted",
                "raw_tool_arguments": "omitted",
                "raw_tool_output": "omitted",
                "raw_messages": "omitted",
            },
        }

    def _start_phase(self, phase: str, data: dict[str, Any], now: float) -> None:
        if self._current_phase and self._current_phase.duration_seconds is None:
            self._current_phase.duration_seconds = max(0.0, now - self._current_phase.started_at)
        record = _PhaseRecord(phase=phase, started_at=now, data=self._phase_payload(data))
        self._phases.append(record)
        self._current_phase = record

    def _phase_payload(self, data: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key in (
            "attempt",
            "max_attempts",
            "iteration",
            "elapsed_seconds",
            "connect_elapsed_seconds",
            "first_response_elapsed_seconds",
            "timeout_seconds",
            "execution_elapsed_seconds",
            "tool_count",
            "estimated_tokens",
            "message_tokens",
            "system_prompt_tokens",
            "tool_schema_tokens",
            "token_threshold",
            "message_count",
            "message_threshold",
            "new_message_count",
            "messages_compacted",
            "tail_preserved",
            "dropped_messages",
            "dropped_groups",
            "attempts",
            "retries",
            "modified_count",
            "bytes_saved",
            "keep_recent_groups",
            "compact_chars",
            "preserve_tail",
            "summary_retry_drop_groups",
        ):
            if key in data:
                value = _round_seconds(data.get(key)) if key.endswith("seconds") else data.get(key)
                payload[key] = value
        if "reason" in data:
            payload["reason"] = _sanitize_text(data.get("reason"), max_chars=120)
        if "strategy" in data:
            payload["strategy"] = _sanitize_text(data.get("strategy"), max_chars=120)
        if "timeout_type" in data:
            payload["timeout_type"] = _sanitize_text(data.get("timeout_type"), max_chars=80)
        if "provider" in data:
            payload["provider"] = _sanitize_text(data.get("provider"), max_chars=80)
        if "model" in data:
            payload["model"] = _sanitize_text(data.get("model"), max_chars=120)
        if "reasons" in data:
            payload["reasons"] = _safe_str_list(data.get("reasons"))
        if "tool_names" in data:
            payload["tool_names"] = _safe_str_list(data.get("tool_names"))
        for key in ("in_memory_only", "no_op", "cancelled", "stale_eviction"):
            if key in data:
                value = _safe_bool(data.get(key))
                if value is not None:
                    payload[key] = value
        return payload

    def _start_tool(self, data: dict[str, Any], now: float) -> None:
        tool_id = _sanitize_text(data.get("id") or f"tool-{len(self._tool_order) + 1}", max_chars=120)
        record = _ToolRecord(
            id=tool_id,
            name=_sanitize_text(data.get("tool_name") or "tool", max_chars=120),
            started_at=now,
            argument_shape=_argument_shape(data.get("arguments")),
            iteration=_safe_int(data.get("iteration")),
            timeout_seconds=_round_seconds(data.get("timeout_seconds")),
            first_response_elapsed_seconds=_round_seconds(data.get("first_response_elapsed_seconds")),
        )
        self._tools[tool_id] = record
        self._tool_order.append(tool_id)
        self._start_phase("tool_exec", {"tool_count": len(self._tools)}, now)

    def _finish_tool(self, data: dict[str, Any], now: float) -> None:
        tool_id = _sanitize_text(data.get("id") or "", max_chars=120)
        record = self._tools.get(tool_id)
        if record is None:
            record = _ToolRecord(
                id=tool_id or f"tool-{len(self._tool_order) + 1}",
                name=_sanitize_text(data.get("tool_name") or "tool", max_chars=120),
                started_at=now,
                argument_shape={"type": "unknown"},
            )
            self._tools[record.id] = record
            self._tool_order.append(record.id)
        record.status = _sanitize_text(data.get("status") or "unknown", max_chars=80)
        record.duration_seconds = max(0.0, now - record.started_at)
        if "execution_elapsed_seconds" in data:
            record.execution_elapsed_seconds = _round_seconds(data.get("execution_elapsed_seconds"))
        if "timeout_seconds" in data:
            record.timeout_seconds = _round_seconds(data.get("timeout_seconds"))
        output = data.get("output")
        record.output_shape = _output_shape(output)
        if isinstance(output, dict):
            decision = output.get("_approval_decision")
            if decision:
                record.approval_decision = _sanitize_text(decision, max_chars=80)
            record.hook_blocked = bool(output.get("hook_blocked"))

    def _add_retry(self, data: dict[str, Any]) -> None:
        retry = {
            "attempt": data.get("attempt"),
            "max_attempts": data.get("max_attempts"),
            "delay_seconds": _round_seconds(data.get("delay")),
            "reason": _sanitize_text(data.get("reason"), max_chars=120),
        }
        if "elapsed_seconds" in data:
            retry["elapsed_seconds"] = _round_seconds(data.get("elapsed_seconds"))
        if "timeout_seconds" in data:
            retry["timeout_seconds"] = _round_seconds(data.get("timeout_seconds"))
        for key in ("timeout_type", "error_type", "provider", "model"):
            if key in data:
                value = _sanitize_text(data.get(key), max_chars=120)
                if value:
                    retry[key] = value
        if len(self._retries) < _MAX_RETRIES:
            self._retries.append(retry)

    def _add_runtime_event(self, kind: str, payload: dict[str, Any]) -> None:
        if len(self._runtime_events) >= _MAX_EVENTS:
            return
        self._runtime_events.append({"kind": kind, **payload})

    def _sanitize_runtime_payload(self, kind: str, data: dict[str, Any]) -> dict[str, Any]:
        if kind in {"dlp_blocked", "dlp_warning", "output_filter_blocked", "output_filter_warning"}:
            return {"rules": _safe_str_list(data.get("matches"))}
        if kind == "injection_detected":
            return {
                "tool_name": _sanitize_text(data.get("tool_name"), max_chars=120),
                "technique": _sanitize_text(data.get("technique"), max_chars=120),
                "confidence": data.get("confidence"),
                "action": _sanitize_text(data.get("action"), max_chars=40),
            }
        if kind == "budget_warning":
            return {
                "message": _sanitize_text(data.get("message"), max_chars=160),
                "label": _sanitize_text(data.get("label"), max_chars=80),
                "used": data.get("used"),
                "limit": data.get("limit"),
                "percent": data.get("percent"),
            }
        if kind == "workflow_pause":
            return {
                "tool_call_id": _sanitize_text(data.get("tool_call_id"), max_chars=120),
                "tool_name": _sanitize_text(data.get("tool_name"), max_chars=120),
                "reason": _sanitize_text(data.get("reason"), max_chars=120),
            }
        if kind == "auto_plan_suggest":
            return {"tool_calls": data.get("tool_calls")}
        if kind == "compaction":
            payload = self._phase_payload(data)
            if "new_message_count" in data and "message_count" in data:
                try:
                    payload["messages_compacted"] = max(0, int(data["message_count"]) - int(data["new_message_count"]))
                except (TypeError, ValueError):
                    pass
            return payload
        if kind == "cancelled":
            payload = {"reason": _sanitize_text(data.get("reason"), max_chars=120)}
            for key in ("elapsed_seconds", "iteration"):
                if key in data:
                    payload[key] = _round_seconds(data.get(key)) if key.endswith("seconds") else data.get(key)
            return payload
        return {}

    def _serialize_tool(self, tool: _ToolRecord, *, now: float | None = None) -> dict[str, Any]:
        duration = tool.duration_seconds
        if duration is None and now is not None:
            duration = max(0.0, now - tool.started_at)
        payload = {
            "id": tool.id,
            "name": tool.name,
            "status": tool.status,
            "duration_seconds": _round_seconds(duration),
            "argument_shape": tool.argument_shape,
        }
        if tool.iteration is not None:
            payload["iteration"] = tool.iteration
        if tool.timeout_seconds is not None:
            payload["timeout_seconds"] = _round_seconds(tool.timeout_seconds)
        if tool.first_response_elapsed_seconds is not None:
            payload["first_response_elapsed_seconds"] = _round_seconds(tool.first_response_elapsed_seconds)
        if tool.execution_elapsed_seconds is not None:
            payload["execution_elapsed_seconds"] = _round_seconds(tool.execution_elapsed_seconds)
        if tool.output_shape is not None:
            payload["output_shape"] = tool.output_shape
        if tool.approval_decision:
            payload["approval_decision"] = tool.approval_decision
        if tool.hook_blocked:
            payload["hook_blocked"] = True
        return payload
