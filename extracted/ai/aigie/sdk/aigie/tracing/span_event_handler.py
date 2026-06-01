"""In-flight span tracker and wire-shaper for tracing integrations.

Holds an in-memory dict of open spans keyed by framework-native run_id
so close_span can compute duration and reuse span_id/parent_id. Every
method shapes the wire payload and forwards it to ``TraceEmitter``;
emissions are skipped when the caller is inside a ``no_retention()``
scope. Integration lifecycles hold one of these via composition.

trace_id is sourced from ambient ``trace_state`` (set by the lifecycle)
and parent_id falls back to the ambient span stack when the framework
doesn't supply a parent_run_id we already track.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Literal

from aigie.buffer import EventType
from aigie.tracing.retention import is_retention_suppressed
from aigie.tracing.trace_state import (
    current_parent_span_id,
    current_trace_id,
    pop_span,
    push_span,
)

if TYPE_CHECKING:
    from aigie.tracing.config_base import FrameworkConfigBase
    from aigie.tracing.emitter import TraceEmitter


_FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "error_classification",
        "error_detection",
        "error_severity",
        "error_is_transient",
        "status_message",
    }
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _require_trace_id() -> str:
    trace_id = current_trace_id()
    if trace_id is None:
        raise RuntimeError(
            "open_span called without active ambient trace_state. "
            "Wrap in open_ambient(trace_id=...) / close_ambient(token)."
        )
    return trace_id


class SpanEventHandler:
    """In-flight span tracker and wire-shaper.

    Holds an in-memory registry of open spans keyed by framework-native
    run_id. Each lifecycle primitive shapes one wire payload and forwards
    it to ``TraceEmitter``. Integrations hold an instance via composition
    rather than inheriting from it.
    """

    def __init__(
        self,
        emitter: TraceEmitter,
        *,
        config: FrameworkConfigBase | None = None,
    ) -> None:
        self._emitter = emitter
        self._open: dict[str, dict[str, Any]] = {}
        self._config = config

    @property
    def zero_retention(self) -> bool:
        """True when this callback was constructed with a zero-retention config."""
        return bool(self._config and self._config.zero_retention)

    @property
    def emitter(self) -> TraceEmitter:
        return self._emitter

    def is_open(self, run_id: str) -> bool:
        return run_id in self._open

    def get_state(self, run_id: str) -> dict[str, Any] | None:
        """Return the open-span state dict for ``run_id``, or None.

        The returned dict is the live one — mutations are visible to subsequent
        close_span/fail_span emissions.
        """
        return self._open.get(run_id)

    def open_span(
        self,
        *,
        run_id: str,
        parent_run_id: str | None,
        name: str,
        span_type: str,
        input: Any,
        metadata: dict[str, Any] | None = None,
        extras: dict[str, Any] | None = None,
    ) -> str:
        trace_id = _require_trace_id()
        span_id = str(uuid.uuid4())
        if is_retention_suppressed():
            return span_id
        start_dt = _utcnow()
        start_time = start_dt.isoformat()
        clean_metadata = self._sanitize_metadata(metadata or {})

        # Parent priority:
        # 1. explicit framework-native parent_run_id resolved through _open
        # 2. ambient SpanStack top (handles "framework didn't tell us")
        # 3. None (root)
        parent_id: str | None = None
        if parent_run_id:
            parent_state = self._open.get(parent_run_id)
            if parent_state:
                parent_id = parent_state["id"]
        if parent_id is None:
            parent_id = current_parent_span_id()

        payload = {
            "id": span_id,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "name": name,
            "type": span_type,
            "input": input,
            "metadata": clean_metadata,
            "start_time": start_time,
            "created_at": start_time,
        }
        if extras:
            payload.update(extras)
        self._open[run_id] = {
            "id": span_id,
            "name": name,
            "type": span_type,
            "input": input,
            "metadata": clean_metadata,
            "start_dt": start_dt,
            "start_time": start_time,
            "parent_id": parent_id,
        }
        push_span(span_id)
        self._emitter.emit_raw_sync(EventType.SPAN_CREATE, payload)
        return span_id

    def get_span_metadata(self, run_id: str) -> dict[str, Any] | None:
        """Return the metadata dict for an open span, or None.

        Returned dict is the live one — mutations are visible to subsequent
        close_span/fail_span emissions. Use sparingly; prefer passing
        metadata_updates= through close_span/fail_span.
        """
        state = self._open.get(run_id)
        return state["metadata"] if state else None

    def close_span(
        self,
        *,
        run_id: str,
        output: Any,
        extras: dict[str, Any] | None = None,
        metadata_updates: dict[str, Any] | None = None,
    ) -> None:
        state = self._open.pop(run_id, None)
        if state is None:
            return
        if metadata_updates:
            state["metadata"].update(metadata_updates)
        if is_retention_suppressed():
            pop_span()
            return
        payload = self._finalize_payload(state, status="success")
        payload["output"] = self._strip_error_envelope(output)
        if extras:
            payload.update(extras)
        self._emitter.emit_raw_sync(EventType.SPAN_UPDATE, payload)
        pop_span()

    def fail_span(
        self,
        *,
        run_id: str,
        error: BaseException,
        metadata_updates: dict[str, Any] | None = None,
    ) -> None:
        """Close an open span with an error. ``metadata.error`` is populated by
        KytteErrorEnricher (post-hook); we do not duplicate it into metadata here.
        """
        state = self._open.pop(run_id, None)
        if state is None:
            return
        if metadata_updates:
            state["metadata"].update(metadata_updates)
        if is_retention_suppressed():
            pop_span()
            return
        err_str = str(error)
        payload = self._finalize_payload(state, status="error")
        payload["output"] = None
        payload["error"] = err_str
        payload["error_message"] = err_str
        payload["error_type"] = type(error).__name__
        self._emitter.emit_raw_sync(EventType.SPAN_UPDATE, payload)
        pop_span()

    def _finalize_payload(self, state: dict[str, Any], *, status: str) -> dict[str, Any]:
        end_dt = _utcnow()
        duration_ns = int((end_dt - state["start_dt"]).total_seconds() * 1_000_000_000) or 1
        return {
            "id": state["id"],
            "trace_id": current_trace_id(),
            "name": state["name"],
            "type": state["type"],
            "input": state["input"],
            "metadata": state["metadata"],
            "status": status,
            "start_time": state["start_time"],
            "end_time": end_dt.isoformat(),
            "duration_ns": duration_ns,
            "parent_id": state["parent_id"],
        }

    def pause_span(self, *, run_id: str) -> None:
        """Mark span as paused without removing it; expects later resume/close/fail."""
        state = self._open.get(run_id)
        if state is None:
            return
        if is_retention_suppressed():
            return
        payload = {
            "id": state["id"],
            "trace_id": current_trace_id(),
            "name": state["name"],
            "type": state["type"],
            "status": "paused",
        }
        self._emitter.emit_raw_sync(EventType.SPAN_UPDATE, payload)

    def close_pending_spans(self, *, status: Literal["paused"] = "paused") -> None:
        """Pause every open span. Used on framework pause/interrupt."""
        del status  # signature reserved; only paused is implemented
        for run_id in list(self._open):
            self.pause_span(run_id=run_id)

    def close_trace(self, *, status: str) -> None:
        trace_id = current_trace_id()
        if trace_id is None:
            return
        if is_retention_suppressed():
            return
        self._emitter.emit_raw_sync(EventType.TRACE_UPDATE, {"id": trace_id, "status": status})

    @staticmethod
    def _strip_error_envelope(output: Any) -> Any:
        if isinstance(output, dict) and output.get("status") == "error" and "error" in output:
            return None
        return output

    @staticmethod
    def _sanitize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in metadata.items() if k not in _FORBIDDEN_METADATA_KEYS}
