"""Bridge the OpenAI Agents SDK tracing processor to Aigie spans."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import NAMESPACE_URL, UUID, uuid5

from aigie.context_manager import enrich_span_fields, merge_metadata
from aigie.tracing.emitter import TraceEmitter
from aigie.tracing.execution_state import build_execution_plan
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

# _tallies is bounded on its own rather than by _closed_traces' eviction order,
# and reclaims only entries no path can reach — see _reclaim_unreachable_tally.
# The cap is the trigger to look for one, not a licence to drop whatever is
# oldest: an abandoned trace should not leak, but a live one must not be lost.
_MAX_LIVE_TALLIES = 1024

# A paused run is deliberately allowed to outlive _closed_traces, so it needs a
# bound of its own: an approval nobody ever resumes is otherwise remembered for
# the life of the process, and pins its tally too, since reclamation treats
# paused runs as reachable.
_MAX_PAUSED_TRACES = 128

# How long a finished run's counters stay resumable. Long enough to cover a
# human approval turnaround, short enough that abandoned runs do not accumulate
# for the life of the process.
_TALLY_RETENTION = timedelta(hours=1)

_LLM_KINDS = frozenset({"generation", "response", "transcription", "speech"})


@dataclass(slots=True)
class _RunTally:
    """Run-level counters behind the root's ``execution_plan``.

    The processor only ever sees span *ends*, so turns and tool calls are
    derived from span kinds. The lifecycle hooks in ``hooks.py`` would be the
    more direct seam but are opt-in, so counting there would report zero for
    every user who does not pass ``hooks=``.
    """

    turn_count: int = 0
    tool_call_count: int = 0
    errored: bool = False
    # Set when the run ends; the clock the retention bound reads. None while the
    # run is live, so an in-flight run is never a reclamation candidate.
    ended_at: datetime | None = None


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


def _plan(name: str, tally: _RunTally, status: str) -> dict[str, Any]:
    return build_execution_plan(
        agent=name,
        tool_calls=tally.tool_call_count,
        turn_count=tally.turn_count,
        status=status,
    )


class OpenAIAgentsProcessor:
    """A non-blocking ``agents`` ``TracingProcessor`` implementation."""

    def __init__(self, emitter: TraceEmitter, config: Any) -> None:
        self._emitter: TraceEmitter | None = emitter
        self._config = config
        self._traces: dict[str, tuple[datetime, Any]] = {}
        self._trace_io: dict[str, tuple[Any, Any]] = {}
        self._closed_traces: dict[str, tuple[datetime, Any, Any, Any]] = {}
        self._tallies: dict[str, _RunTally] = {}
        # Traces paused for approval. on_trace_start accepts any id, so a paused
        # run stays resumable after the closed cache has forgotten it — which
        # makes membership here part of what "reachable" means below.
        # Insertion-ordered so the oldest abandoned approval evicts first.
        self._paused: dict[str, None] = {}

    def configure(self, emitter: TraceEmitter, config: Any) -> None:
        """Rebind the processor when a new Aigie client is initialized."""
        self._emitter = emitter
        self._config = config
        self._traces.clear()
        self._trace_io.clear()
        self._closed_traces.clear()
        self._tallies.clear()
        self._paused.clear()

    def detach(self) -> None:
        """Stop emitting without unregistering from the Agents SDK processor list.

        The Agents SDK exposes no removal API, so the processor stays subscribed
        and a later ``configure`` re-arms it instead of registering a duplicate.
        """
        self._emitter = None
        self._traces.clear()
        self._trace_io.clear()
        self._closed_traces.clear()
        self._tallies.clear()
        self._paused.clear()

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
        self._paused.pop(trace.trace_id, None)  # the resume happened; _traces covers it now
        self._traces[trace.trace_id] = (datetime.now(timezone.utc), trace)
        # A resume reopens the same trace id: it is live again, so its counters
        # stop ageing toward reclamation.
        if (tally := self._tallies.get(trace.trace_id)) is not None:
            tally.ended_at = None

    def on_trace_end(self, trace: Any) -> None:
        started, _ = self._traces.pop(trace.trace_id, (datetime.now(timezone.utc), trace))
        input_value, output_value = self._trace_io.get(trace.trace_id, (None, None))
        # Left in _tallies rather than popped: a run that pauses for approval
        # resumes into this same trace, and its counters must survive the gap.
        tally = self._tallies.get(trace.trace_id) or _RunTally()
        tally.ended_at = datetime.now(timezone.utc)
        self._tallies[trace.trace_id] = tally
        name = getattr(trace, "name", None) or "Agent workflow"
        self._remember_closed(trace.trace_id, (started, trace, input_value, output_value))
        self._trace_io.pop(trace.trace_id, None)
        self._emit(
            span_id=_uuid_id(trace.trace_id),
            trace_id=_uuid_id(trace.trace_id),
            parent_id=None,
            name=name,
            span_type="workflow",
            started=started,
            ended=datetime.now(timezone.utc),
            input=input_value if self._config.capture_inputs else None,
            output=output_value if self._config.capture_outputs else None,
            metadata=merge_metadata(
                getattr(trace, "metadata", None),
                {
                    "framework": "openai_agents",
                    "execution_plan": _plan(name, tally, "error" if tally.errored else "success"),
                },
            ),
        )

    def _record_tally(self, trace_key: str, kind: str, error: Any) -> None:
        """Fold one finished child span into its run's counters."""
        tally = self._tallies.get(trace_key)
        if tally is None:
            if len(self._tallies) >= _MAX_LIVE_TALLIES:
                self._reclaim_unreachable_tally()
            # Popped in on_trace_end, and unbounded for the same reason _trace_io
            # is: any cap would have to guess whether a run is still accumulating,
            # and guessing wrong makes it finalize claiming it did no work.
            tally = self._tallies[trace_key] = _RunTally()
        span_type = _SPAN_TYPES.get(kind)
        if span_type == "llm":
            tally.turn_count += 1
        elif span_type == "tool" and kind != "mcp_tools":
            # An mcp_tools span is a server's tool *listing* (MCPListToolsSpanData),
            # not an invocation -- the IO mapping above reads it as server/result
            # for the same reason. Counting it reports a tool call on a run that
            # made none.
            tally.tool_call_count += 1
        if error:
            tally.errored = True

    def _reclaim_unreachable_tally(self) -> None:
        """Free tallies whose run ended long enough ago that no resume is coming.

        ``on_trace_end`` keeps a tally so an approval pause can resume into it,
        and that resume may arrive after the closed-trace entry is evicted — so
        the retention cannot be tied to those windows without losing pre-pause
        counters. It is bounded by time instead, the same way the pre-pause
        emit window is: past ``_TALLY_RETENTION`` the run is not coming back.

        Without this every real run leaks. A work-bearing tally used to be kept
        unconditionally, and every run has at least one LLM span, so nothing was
        ever freed once it aged out of the resume windows.
        """
        now = datetime.now(timezone.utc)
        for trace_id in list(self._tallies):
            if len(self._tallies) < _MAX_LIVE_TALLIES:
                return
            # _closed_traces included: mark_interrupted can still resume from it,
            # and a quiet process can hold an entry there for longer than the
            # retention window. Dropping the tally under a live closed entry is
            # the same lost-resume-state bug, reached by the clock instead.
            if (
                trace_id in self._traces
                or trace_id in self._paused
                or trace_id in self._closed_traces
            ):
                continue
            ended = self._tallies[trace_id].ended_at
            if ended is None or now - ended < _TALLY_RETENTION:
                continue
            self._tallies.pop(trace_id, None)

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
        name = getattr(trace, "name", None) or "Agent workflow"
        self._trace_io[trace_id] = (input_value, output_value)
        self._paused.pop(trace_id, None)
        self._paused[trace_id] = None
        while len(self._paused) > _MAX_PAUSED_TRACES:
            self._paused.pop(next(iter(self._paused)))
        tally = self._tallies.get(trace_id) or _RunTally()
        # The pause is activity: restart the retention clock from here, so an
        # approval is kept for a window measured from when it paused rather than
        # from when the run ended. Without this a run evicted from _paused by
        # later pauses -- a count-based bound, while retention is time-based --
        # loses its counters the moment those two axes disagree.
        tally.ended_at = datetime.now(timezone.utc)
        self._tallies[trace_id] = tally
        self._emit(
            span_id=_uuid_id(trace_id),
            trace_id=_uuid_id(trace_id),
            parent_id=None,
            name=name,
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
                    "execution_plan": _plan(name, tally, "paused"),
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
        raw_trace_id = exported.get("trace_id") or span.trace_id
        error = exported.get("error")
        self._record_tally(str(raw_trace_id), kind, error)
        input_value, output_value = _span_io(kind, data, self._config)
        self._emit(
            span_id=_uuid_id(exported.get("id") or getattr(span, "span_id", "") or ""),
            trace_id=_uuid_id(raw_trace_id),
            parent_id=(
                _uuid_id(exported["parent_id"])
                if exported.get("parent_id")
                else _uuid_id(raw_trace_id)
            ),
            name=_span_name(kind, data),
            span_type=_SPAN_TYPES.get(kind, "chain"),
            started=_time(exported.get("started_at")),
            ended=_time(exported.get("ended_at")),
            input=_safe(input_value),
            output=_safe(output_value),
            metadata=metadata,
            extras=extras,
            error=error,
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
        self._tallies.clear()
        self._paused.clear()

    def force_flush(self) -> None:
        return
