"""Bridge the OpenAI Agents SDK tracing processor to Aigie spans."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from aigie.context_manager import enrich_span_fields, merge_metadata
from aigie.tracing.emitter import TraceEmitter
from aigie.tracing.llm_metadata import normalize_provider
from aigie.tracing.retention import is_retention_suppressed
from aigie.tracing.usage import llm_span_payload


def _time(value: str | None, fallback: datetime | None = None) -> datetime:
    if value:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return fallback or datetime.now(timezone.utc)


def _safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool, list, dict)):
        return value
    return str(value)


def _uuid_id(value: Any) -> str:
    """Map Agents SDK trace/span IDs to the UUID wire contract deterministically."""
    text = str(value)
    try:
        return str(UUID(text))
    except (ValueError, AttributeError):
        return str(uuid5(NAMESPACE_URL, f"aigie:openai-agents:{text}"))


def _model_provider(model: Any) -> str:
    """Infer the model provider while retaining OpenAI for unqualified model names."""
    value = str(model or "")
    prefix, separator, _ = value.partition("/")
    if not separator:
        return "openai"
    return normalize_provider(prefix) or "openai"


_MAX_CLOSED_TRACES = 128

_LLM_KINDS = frozenset({"generation", "response", "transcription", "speech"})

_SPAN_TYPES = {
    "generation": "llm",
    "response": "llm",
    "transcription": "llm",
    "speech": "llm",
    "function": "tool",
    "agent": "agent",
    "guardrail": "guardrail",
    "handoff": "chain",
    "task": "chain",
    "turn": "chain",
    "custom": "chain",
    "speech_group": "chain",
    "mcp_tools": "tool",
}


def _span_payload(exported: dict[str, Any], span: Any) -> tuple[str, dict[str, Any]]:
    """Flatten the exported span into a ``(kind, data)`` pair."""
    raw_data = exported.get("span_data")
    raw_data = raw_data if isinstance(raw_data, dict) else {}
    data = dict(raw_data)
    nested_data = raw_data.get("data")
    if isinstance(nested_data, dict):
        data.update(nested_data)
    if data.get("type") == "response" and data.get("model") is None:
        response = getattr(getattr(span, "span_data", None), "response", None)
        model = getattr(response, "model", None)
        if model:
            data["model"] = model
    kind = str(raw_data.get("type", "custom"))
    if kind == "custom" and data.get("sdk_span_type") in {"task", "turn"}:
        kind = str(data["sdk_span_type"])
    return kind, data


def _kind_metadata(kind: str, data: dict[str, Any]) -> dict[str, Any]:
    """Collect the metadata fields specific to one Agents SDK span kind."""
    keys: tuple[str, ...]
    if kind == "agent":
        keys = ("handoffs", "tools", "output_type")
    elif kind == "handoff":
        keys = ("from_agent", "to_agent")
    elif kind == "function":
        keys = ("mcp_data",)
    elif kind == "guardrail":
        return {} if data.get("triggered") is None else {"triggered": bool(data["triggered"])}
    elif kind in {"task", "turn"}:
        return {key: value for key, value in data.items() if key != "name"}
    else:
        return {}
    return {key: data[key] for key in keys if data.get(key) is not None}


def _span_io(kind: str, data: dict[str, Any], config: Any) -> tuple[Any, Any]:
    """Pick the input/output fields for a span kind, honoring the capture flags."""
    input_key, output_key = ("server", "result") if kind == "mcp_tools" else ("input", "output")
    return (
        data.get(input_key) if config.capture_inputs else None,
        data.get(output_key) if config.capture_outputs else None,
    )


def _span_name(kind: str, data: dict[str, Any]) -> str:
    if kind in {"task", "turn"}:
        return str(data.get("name") or kind)
    return str(data.get("name") or data.get("model") or kind)


class OpenAIAgentsProcessor:
    """A non-blocking ``agents`` ``TracingProcessor`` implementation."""

    def __init__(self, emitter: TraceEmitter, config: Any) -> None:
        self._emitter: TraceEmitter | None = emitter
        self._config = config
        self._traces: dict[str, tuple[datetime, Any]] = {}
        self._trace_io: dict[str, tuple[Any, Any]] = {}
        self._closed_traces: dict[str, tuple[datetime, Any, Any, Any]] = {}

    def configure(self, emitter: TraceEmitter, config: Any) -> None:
        """Rebind the processor when a new Aigie client is initialized."""
        self._emitter = emitter
        self._config = config
        self._traces.clear()
        self._trace_io.clear()
        self._closed_traces.clear()

    def detach(self) -> None:
        """Stop emitting without unregistering from the Agents SDK processor list.

        The Agents SDK exposes no removal API, so the processor stays subscribed
        and a later ``configure`` re-arms it instead of registering a duplicate.
        """
        self._emitter = None
        self._traces.clear()
        self._trace_io.clear()
        self._closed_traces.clear()

    def record_workflow_io(
        self, trace_id: str, input_value: Any = None, output_value: Any = None
    ) -> None:
        """Record Runner input/output supplied by the optional lifecycle hooks."""
        if self._emitter is None:
            return
        current_input, current_output = self._trace_io.get(trace_id, (None, None))
        self._trace_io[trace_id] = (
            current_input if current_input is not None else input_value,
            output_value if output_value is not None else current_output,
        )

    def on_trace_start(self, trace: Any) -> None:
        self._closed_traces.pop(trace.trace_id, None)
        self._traces[trace.trace_id] = (datetime.now(timezone.utc), trace)

    def on_trace_end(self, trace: Any) -> None:
        started, _ = self._traces.pop(trace.trace_id, (datetime.now(timezone.utc), trace))
        input_value, output_value = self._trace_io.get(trace.trace_id, (None, None))
        self._remember_closed(trace.trace_id, (started, trace, input_value, output_value))
        self._trace_io.pop(trace.trace_id, None)
        self._emit(
            span_id=_uuid_id(trace.trace_id),
            trace_id=_uuid_id(trace.trace_id),
            parent_id=None,
            name=getattr(trace, "name", None) or "Agent workflow",
            span_type="workflow",
            started=started,
            ended=datetime.now(timezone.utc),
            input=input_value if self._config.capture_inputs else None,
            output=output_value if self._config.capture_outputs else None,
            metadata=merge_metadata(
                getattr(trace, "metadata", None), {"framework": "openai_agents"}
            ),
        )

    def _remember_closed(self, trace_id: str, entry: tuple[datetime, Any, Any, Any]) -> None:
        """Retain a bounded window of finished traces for approval resumes."""
        self._closed_traces.pop(trace_id, None)
        self._closed_traces[trace_id] = entry
        while len(self._closed_traces) > _MAX_CLOSED_TRACES:
            self._closed_traces.pop(next(iter(self._closed_traces)))

    def mark_interrupted(self, trace_id: str, approvals: int) -> None:
        """Publish an approval pause for a completed, resumable SDK run."""
        closed = self._closed_traces.get(trace_id)
        if closed is None:
            return
        started, trace, input_value, output_value = closed
        self._trace_io[trace_id] = (input_value, output_value)
        self._emit(
            span_id=_uuid_id(trace_id),
            trace_id=_uuid_id(trace_id),
            parent_id=None,
            name=getattr(trace, "name", None) or "Agent workflow",
            span_type="workflow",
            started=started,
            ended=datetime.now(timezone.utc),
            input=input_value if self._config.capture_inputs else None,
            output=None,
            metadata=merge_metadata(
                getattr(trace, "metadata", None),
                {
                    "framework": "openai_agents",
                    "human_in_loop": True,
                    "pending_approvals": approvals,
                },
            ),
            status="paused",
        )

    def on_span_start(self, span: Any) -> None:
        return

    def on_span_end(self, span: Any) -> None:
        exported = span.export() or {}
        kind, data = _span_payload(exported, span)
        metadata = merge_metadata(
            exported.get("metadata"), {"framework": "openai_agents", "kind": kind}
        )
        extras: dict[str, Any] = {}
        if kind in _LLM_KINDS:
            usage_extras, usage_metadata = llm_span_payload(
                data.get("usage"), model_id=data.get("model")
            )
            extras.update(usage_extras)
            metadata.update(usage_metadata)
            metadata["provider"] = _model_provider(data.get("model"))
        metadata.update(_kind_metadata(kind, data))
        input_value, output_value = _span_io(kind, data, self._config)
        self._emit(
            span_id=_uuid_id(exported.get("id") or getattr(span, "span_id", "") or ""),
            trace_id=_uuid_id(exported.get("trace_id") or span.trace_id),
            parent_id=(
                _uuid_id(exported["parent_id"])
                if exported.get("parent_id")
                else _uuid_id(span.trace_id)
            ),
            name=_span_name(kind, data),
            span_type=_SPAN_TYPES.get(kind, "chain"),
            started=_time(exported.get("started_at")),
            ended=_time(exported.get("ended_at")),
            input=_safe(input_value),
            output=_safe(output_value),
            metadata=metadata,
            extras=extras,
            error=exported.get("error"),
        )

    def _emit(
        self,
        *,
        span_id: str,
        trace_id: str,
        parent_id: str | None,
        name: str,
        span_type: str,
        started: datetime,
        ended: datetime,
        input: Any,
        output: Any,
        metadata: dict[str, Any] | None,
        extras: dict[str, Any] | None = None,
        error: Any = None,
        status: str | None = None,
    ) -> None:
        if self._emitter is None:
            return
        if is_retention_suppressed() or getattr(self._config, "zero_retention", False):
            return
        duration_ns = max(1, int((ended - started).total_seconds() * 1_000_000_000))
        metadata, tags = enrich_span_fields(metadata)
        payload: dict[str, Any] = {
            "id": span_id,
            "trace_id": trace_id,
            "parent_id": parent_id,
            "name": name,
            "type": span_type,
            "status": status or ("error" if error else "success"),
            "start_time": started.isoformat(),
            "end_time": ended.isoformat(),
            "duration_ns": duration_ns,
            "input": input,
            "output": None if error else output,
            "metadata": metadata,
        }
        if tags:
            payload["tags"] = tags
        if extras:
            payload.update(extras)
        if error:
            message = str(error)
            payload.update(error=message, error_message=message, error_type=type(error).__name__)
        self._emitter.emit(payload)

    def shutdown(self) -> None:
        self._traces.clear()
        self._trace_io.clear()
        self._closed_traces.clear()

    def force_flush(self) -> None:
        return
