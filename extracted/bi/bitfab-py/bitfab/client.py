"""Bitfab client for provider-based API calls."""

from __future__ import annotations

import asyncio
import contextlib
import enum
import functools
import inspect
import json
import logging
import os
import sys
import threading
import uuid
from collections.abc import Awaitable, Callable, Collection, Mapping, Sequence
from contextvars import ContextVar
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypedDict,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import ParamSpec

from bitfab import subtree
from bitfab.assertion_categories import AssertionCategoriesClient
from bitfab.baml import run_function_with_baml
from bitfab.commit_ref import CommitRef, current_commit_ref, start_commit_ref_resolution
from bitfab.constants import (
    DEFAULT_SERVICE_URL,
    REPLAY_API_KEY_ENV,
    _replay_context,
    _seed_context,
    _submit_origin,
)
from bitfab.datasets import DatasetsClient
from bitfab.db_snapshot import DbSnapshotRef, build_snapshot_ref
from bitfab.experiment_id import resolve_experiment_id
from bitfab.experiments import ExperimentsClient
from bitfab.graders import GradersClient
from bitfab.http import (
    ApiKeyInput,
    HttpClient,
    flush_traces,
)
from bitfab.labels import LabelsClient
from bitfab.mock_matching import MATCHER, VariantChain, extend_variant_chain
from bitfab.mock_override import (
    NO_MOCK_OVERRIDE,
    MockOverride,
    MockOverrideCtx,
    MockOverrideInput,
    MockOverrideResolver,
    MockSource,
    MockTarget,
    MockValue,
    NodeMatcher,
    SpanNodeMeta,
)
from bitfab.organization_members import OrganizationMembersClient
from bitfab.payload_budget import MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES
from bitfab.replay import (  # noqa: F401 - re-export
    _CODE_CHANGE_UNSET,
    _CONCURRENCY_UNSET,
    AdaptContext,
    CodeChangeFile,
    MockStrategy,
    ProcessLauncher,
    ReplayConcurrency,
    ReplayExperimentStart,
    ReplayItem,
    ReplayItemFinishProgress,
    ReplayItemStartProgress,
    ReplayProgress,
    ReplayResult,
    ReseedResult,
    _CodeChangeUnset,
    _ConcurrencyUnset,
    _deserialize_inputs,
    _in_replay_item,
    _in_seed_scope,
    _resolve_replay_fn,
)
from bitfab.replay import replay as _run_replay
from bitfab.replay_branch import DbBranchOptions, ReplayBranch
from bitfab.replay_interrupt import ReplayInterrupt
from bitfab.selective_replay import SelectiveReplayOptions, json_fingerprint
from bitfab.serialize import deserialize_value, serialize_value, to_json_safe
from bitfab.simulation_plan import (
    CONTENT_OFF_KEY,
    DECLARED_IN_CODE_FIELD,
    ROOT_TRACE_FUNCTION_KEY_FIELD,
    SimulationPlan,
)
from bitfab.span_origin import (
    FRAMEWORK_INSTRUMENTATIONS,
    SpanInstrumentation,
    make_span_origin,
)
from bitfab.thread_propagation import install as install_thread_propagation
from bitfab.timestamp import now_iso_timestamp
from bitfab.trace_metadata import (
    caller_trace_metadata,
    record_caller_trace_metadata,
    retire_trace_metadata,
)
from bitfab.traces import TracesClient
from bitfab.warn_once import warn_once

if TYPE_CHECKING:
    from bitfab.langgraph_integration import BitfabLangGraphIntegration

# Cap on the human-readable input/output JSON size sent to the server.
# Mirrors _MAX_SERIALIZED_BYTES in serialize.py, which is the whole-span budget:
# a single field may use all of it, and enforce_payload_budget trims the total
# once every field is in. Once either input or output crosses this threshold we
# replace it with a stub so the span still ships.
_MAX_HUMAN_PAYLOAD_BYTES = MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES

CAPTURE_ENABLED_ENV = "BITFAB_CAPTURE_ENABLED"
MAX_CAPTURED_SUBTREE_SPANS_ENV = "BITFAB_MAX_CAPTURED_SUBTREE_SPANS"

_TRUE_ENV_VALUES = frozenset({"1", "true", "yes"})
_FALSE_ENV_VALUES = frozenset({"0", "false", "no"})


def read_positive_int_env(name: str) -> int | None:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def read_boolean_env(name: str) -> bool | None:
    """Read a boolean environment variable, returning None when it is unset,
    empty, or spelled in a way we do not recognize, so the caller keeps its own
    default."""
    raw = os.environ.get(name)
    if raw is None:
        return None
    value = raw.strip().lower()
    if value == "":
        return None
    if value in _TRUE_ENV_VALUES:
        return True
    if value in _FALSE_ENV_VALUES:
        return False
    warn_once(
        f"unrecognized-boolean-env:{name}",
        f'{name}="{raw}" is not 0 or 1; ignoring it.',
    )
    return None


def _safe_type_name(value: Any) -> str:
    try:
        return type(value).__qualname__
    except Exception:
        return "unknown"


def _cap_payload_size(value: Any) -> Any:
    try:
        size = len(json.dumps(value, default=str))
    except Exception:
        return f"<unserializable: {_safe_type_name(value)} (json_dumps_failed)>"
    if size > _MAX_HUMAN_PAYLOAD_BYTES:
        return f"<unserializable: {_safe_type_name(value)} (too_large_{size}_bytes)>"
    return value


# Type variables for generic function signatures
P = ParamSpec("P")
T = TypeVar("T")

# Sentinel for register_mock_override's ordered form, so an explicit
# value=None (a legitimate flat override output) is distinguishable from
# "no value passed" (the single-arg object form).
_REGISTER_VALUE_UNSET: Any = object()

# Span types matching the backend enum
SpanType = Literal["llm", "agent", "function", "guardrail", "handoff", "custom"]
CaptureWhen = Literal["always", "nested"]
CaptureSurface = Literal["opt-in", "opt-out"]


# Context entry - each entry is a dict with multiple key-value pairs
ContextEntry = dict[str, Any]


# --- BAML Collector support for wrap_baml ---

_baml_collector_class: Any = None
_baml_collector_loaded: bool = False


def _rebuild_sequence(value: list[Any] | tuple[Any, ...], items: list[Any]) -> Any:
    if isinstance(value, list):
        return items
    if hasattr(value, "_make"):
        with contextlib.suppress(Exception):
            return type(value)._make(items)
    if type(value) is not tuple:
        with contextlib.suppress(Exception):
            return type(value)(items)
    return tuple(items)


def _load_baml_collector_class() -> Any:
    global _baml_collector_class, _baml_collector_loaded
    if _baml_collector_loaded:
        return _baml_collector_class
    try:
        from baml_py import Collector

        _baml_collector_class = Collector
    except ImportError:
        _baml_collector_class = None
    _baml_collector_loaded = True
    return _baml_collector_class


def _parse_http_body(raw_body: Any) -> dict[str, Any] | None:
    """Parse an HTTP body from a BAML Collector call into a dict.

    The body may be a plain ``str`` (older baml-py) or an ``HTTPBody`` object
    (baml-py >= 0.219) which exposes ``.json()`` / ``.text`` helpers.
    """
    if raw_body is None:
        return None
    # HTTPBody object - prefer .json() which returns a dict directly
    json_fn = getattr(raw_body, "json", None)
    if callable(json_fn):
        result = json_fn()
        return result if isinstance(result, dict) else None
    # Plain string fallback
    if isinstance(raw_body, str):
        parsed = json.loads(raw_body)
        return parsed if isinstance(parsed, dict) else None
    return None


def _extract_prompt_from_collector(collector: Any) -> str | None:
    try:
        last_log = collector.last
        if last_log is None:
            return None
        calls = getattr(last_log, "calls", []) or []
        selected_call = next(
            (c for c in calls if getattr(c, "selected", False)),
            calls[0] if calls else None,
        )
        if selected_call is None:
            return None
        http_request = getattr(selected_call, "http_request", None)
        if http_request is None:
            return None
        body = _parse_http_body(getattr(http_request, "body", None))
        if not isinstance(body, dict):
            return None
        messages = body.get("messages")
        if not isinstance(messages, list) or not messages:
            return None
        rendered = []
        for msg in messages:
            if isinstance(msg, dict) and "role" in msg:
                content = msg.get("content", "")
                rendered.append(
                    {
                        "role": msg["role"],
                        "content": content
                        if isinstance(content, str)
                        else json.dumps(content),
                    }
                )
        if rendered:
            return json.dumps(rendered)
        return None
    except Exception:
        return None


def _extract_context_from_collector(collector: Any) -> dict[str, Any] | None:
    try:
        last_log = collector.last
        calls = getattr(last_log, "calls", []) or [] if last_log else []
        selected_call = next(
            (c for c in calls if getattr(c, "selected", False)),
            calls[0] if calls else None,
        )
        usage = getattr(collector, "usage", None)

        context: dict[str, Any] = {}

        if selected_call is not None:
            provider = getattr(selected_call, "provider", None)
            if provider:
                context["provider"] = provider

            http_request = getattr(selected_call, "http_request", None)
            if http_request is not None:
                body = _parse_http_body(getattr(http_request, "body", None))
                if isinstance(body, dict) and isinstance(body.get("model"), str):
                    context["model"] = body["model"]

        call_usage = getattr(selected_call, "usage", None) if selected_call else None
        input_tokens = getattr(usage, "input_tokens", None) or getattr(
            call_usage, "input_tokens", None
        )
        output_tokens = getattr(usage, "output_tokens", None) or getattr(
            call_usage, "output_tokens", None
        )
        if input_tokens is not None:
            context["inputTokens"] = input_tokens
        if output_tokens is not None:
            context["outputTokens"] = output_tokens

        timing = getattr(last_log, "timing", None) if last_log else None
        duration_ms = getattr(timing, "duration_ms", None)
        if duration_ms is not None:
            context["durationMs"] = duration_ms

        return context if context else None
    except Exception:
        return None


class TraceLink(TypedDict, total=False):
    trace_id: str
    trace_function_key: str
    span_id: str


class SpanContext(TypedDict, total=False):
    """Context for tracking nested spans."""

    traceId: str
    spanId: str
    threadId: int
    contexts: list[ContextEntry]
    surface: CaptureSurface
    enclosingTrace: TraceLink
    variantChain: VariantChain
    spanName: str
    rootTraceFunctionKey: str
    instrumentation: SpanInstrumentation
    declaredNode: bool
    isRoot: bool


class MixedTracingError(RuntimeError):
    """Opt-in tracing (``span``) and opt-out tracing (``trace`` / ``node``)
    met in one call stack."""


_SURFACE_OF: dict[str, CaptureSurface] = {
    "span": "opt-in",
    "trace": "opt-out",
    "node": "opt-out",
}
_MIX_REMEDY = {
    "span": (
        "Inside a @trace subtree, configure a function with @node instead, "
        "or trace this workflow with @span only."
    ),
    "trace": (
        "Decorate the caller with @trace as well, or decorate this function with @span."
    ),
    "node": (
        "@node only takes effect beneath @trace. Decorate the caller with "
        "@trace, or decorate this function with @span."
    ),
}


def _mixed_tracing_error(entered: str, enclosing: str) -> MixedTracingError:
    return MixedTracingError(
        "Opt-in and opt-out tracing can't be mixed: "
        f"@{entered} ({_SURFACE_OF[entered]}) was entered inside a "
        f"@{enclosing} call ({_SURFACE_OF[enclosing]}). {_MIX_REMEDY[entered]}"
    )


def _enclosing_surface() -> CaptureSurface | None:
    stack = _span_stack.get()
    if not stack:
        return None
    return stack[-1].get("surface")


class TraceState(TypedDict, total=False):
    """State for tracking trace-level data."""

    traceId: str
    sessionId: str
    name: str
    contexts: list[ContextEntry]
    startedAt: str
    endedAt: str
    experimentId: str
    inputSourceTraceId: str
    replayAttempt: int
    dbSnapshotRef: DbSnapshotRef
    dropped: bool
    ingestionType: str
    traceFunctionKey: str


# Async-safe context variable for tracking nested spans
# Uses Python's contextvars which properly propagate through async/await chains
_span_stack: ContextVar[list[SpanContext]] = ContextVar(
    "bitfab_span_stack", default=None
)

# Global dict to track active trace states (trace_id -> TraceState)
_active_trace_states: dict[str, TraceState] = {}

_node_variant: ContextVar[tuple[Callable[..., Any], str | None] | None] = ContextVar(
    "bitfab_node_variant", default=None
)


def _missing_recording_error(
    trace_function_key: str,
    span_name: str,
    call_index: int,
    variant_chain: VariantChain,
) -> RuntimeError:
    message = (
        "Replay selected span "
        f"'{trace_function_key}:{span_name}' for mocking, but recorded occurrence "
        f"{call_index + 1} is unavailable. The real span was not executed."
    )
    if variant_chain:
        variants = ", ".join(
            f"variant '{variant}' of '{name}'" for name, variant in variant_chain
        )
        message += (
            f" The call ran beneath {variants}, and it only matches recordings "
            "beneath the same name and variant, so each variant must be computed "
            "from the call's arguments."
        )
    elif (_replay_context.get() or {}).get("mock_tree_has_variants"):
        message += (
            " The recording has variants but this call ran beneath none, so a "
            "node that stopped computing its variant, or computes a different "
            "one, no longer matches its recording. Compute each variant from "
            "the call's arguments."
        )
    return RuntimeError(message)


def _root_trace_function_key_of(payload: dict[str, Any]) -> str | None:
    captured = payload.get(ROOT_TRACE_FUNCTION_KEY_FIELD)
    trace_id = payload.get("traceId")
    own = payload.get("traceFunctionKey")
    return _resolve_root_trace_function_key(
        captured if isinstance(captured, str) else None,
        trace_id if isinstance(trace_id, str) else None,
        own if isinstance(own, str) else None,
    )


def _resolve_root_trace_function_key(
    captured: str | None, trace_id: str | None, own: str | None
) -> str | None:
    if captured is not None:
        return captured
    if trace_id is not None:
        trace_state = _active_trace_states.get(trace_id)
        root_key = trace_state.get("traceFunctionKey") if trace_state else None
        if isinstance(root_key, str):
            return root_key
    return own


def _get_span_stack() -> list[SpanContext]:
    """Get the current span stack from async context."""
    stack = _span_stack.get()
    if stack is None:
        stack = []
        _span_stack.set(stack)
    return stack


class ActiveSpanContext(TypedDict):
    trace_id: str
    span_id: str


def _active_span_context() -> ActiveSpanContext | None:
    stack = _get_span_stack()
    if not stack:
        return None
    current = stack[-1]
    session = subtree.current_session()
    if session is not None and session.trace_id == current["traceId"]:
        return {
            "trace_id": session.trace_id,
            "span_id": subtree.current_parent_span_id(session),
        }
    return {"trace_id": current["traceId"], "span_id": current["spanId"]}


class CurrentSpan:
    """Handle to the current active span, allowing context to be added."""

    def __init__(self, context: SpanContext) -> None:
        self._context = context

    @property
    def id(self) -> str:
        """The Bitfab ID for the current span."""
        return self._context["spanId"]

    @property
    def trace_id(self) -> str:
        """The trace ID for the current span."""
        return self._context["traceId"]

    def add_context(self, context: dict[str, Any]) -> None:
        """Add a context entry to this span.

        Each call adds one entry (the entire context dict) to the contexts array.

        Args:
            context: Dict with key-value pairs to add as one context entry
        """
        try:
            if not isinstance(context, dict):
                return

            existing: list[ContextEntry] = self._context.get("contexts", [])
            # Push the entire context object as one entry
            self._context["contexts"] = [*existing, context]
        except Exception:
            # Silently ignore - never crash the host app
            pass

    def set_prompt(self, prompt: str) -> None:
        """Set the prompt for this span.

        The prompt is stored in span_data.prompt. Calling multiple times
        overwrites the previous value.

        Args:
            prompt: The prompt string to store
        """
        try:
            if not isinstance(prompt, str):
                return
            self._context["prompt"] = prompt
        except Exception:
            # Silently ignore - never crash the host app
            pass


def _on_event_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


class CurrentTrace:
    """Handle to the current active trace, allowing trace-level context to be set."""

    def __init__(self, trace_id: str) -> None:
        self._trace_id = trace_id

    def _get_or_create_trace_state(self) -> TraceState:
        """Get existing trace state or create a new one."""
        trace_state = _active_trace_states.get(self._trace_id)
        if trace_state is None:
            trace_state = TraceState(
                traceId=self._trace_id,
                startedAt=now_iso_timestamp(),
            )
            _active_trace_states[self._trace_id] = trace_state
        return trace_state

    def set_session_id(self, session_id: str) -> None:
        """Set the session ID for this trace.

        Session ID is used to group traces from the same user session.
        This is stored as a database column.

        Args:
            session_id: The session ID to set
        """
        try:
            trace_state = self._get_or_create_trace_state()
            trace_state["sessionId"] = session_id
        except Exception:
            # Silently ignore - never crash the host app
            pass

    def set_name(self, name: str) -> None:
        """Set the name for this trace.

        The name is the title Bitfab shows for the trace and a field you can
        search and filter on. Use it for the case, ticket, or record the run
        is about. Stored as a database column. Unset, the trace is titled by
        its trace function key.

        Args:
            name: The name to set
        """
        if not isinstance(name, str) or not name:
            return
        try:
            trace_state = self._get_or_create_trace_state()
            trace_state["name"] = name
        except Exception:
            pass

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set metadata for this trace.

        Metadata is stored in the raw trace data. Subsequent calls merge with
        existing metadata, with later values taking precedence.

        Args:
            metadata: Dict of key-value pairs to store as trace metadata
        """
        try:
            if not isinstance(metadata, dict):
                return

            record_caller_trace_metadata(self._trace_id, metadata)
        except Exception:
            # Silently ignore - never crash the host app
            pass

    def add_context(self, context: dict[str, Any]) -> None:
        """Add a context entry to this trace.

        Each call adds one entry (the entire context dict) to the contexts array.

        Args:
            context: Dict with key-value pairs to add as one context entry
        """
        try:
            if not isinstance(context, dict):
                return

            trace_state = self._get_or_create_trace_state()
            existing: list[ContextEntry] = trace_state.get("contexts", [])
            # Push the entire context object as one entry
            trace_state["contexts"] = [*existing, context]
        except Exception:
            # Silently ignore - never crash the host app
            pass

    def drop(self) -> None:
        """Drop this trace.

        Flags the current in-flight trace. Once flagged, spans that complete
        afterward are not uploaded at all, and when the trace completes the
        completion request carries a top-level dropped: true so the server
        scrubs any payloads that already raced out and marks it dropped.

        Never throws into caller code.
        """
        try:
            trace_state = self._get_or_create_trace_state()
            trace_state["dropped"] = True
        except Exception:
            # Silently ignore - never crash the host app
            pass


def _validate_trace_id(trace_id: str) -> None:
    """Validate a canonical Bitfab trace ID."""
    if not _is_uuid(trace_id):
        raise ValueError("trace_id must be a valid Bitfab trace ID")


def _validate_span_id(id: str) -> None:
    """Validate a canonical Bitfab span ID."""
    if not _is_uuid(id):
        raise ValueError("id must be a valid Bitfab span ID")


def _is_uuid(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return str(uuid.UUID(value)) == value.lower()
    except ValueError:
        return False


class DetachedTrace:
    """A detached handle to a previously-created trace, looked up by its
    canonical Bitfab ID.

    Unlike ``get_current_trace()``, this handle is not tied to async context
    propagation - each method sends to the server immediately. Useful for
    adding context to a trace from a different process, request, or thread
    than the one that created it.

    Methods are blocking, like ``get_trace_span()``: each returns once the
    server has applied the change and raises if the server rejected it. They
    write whether or not capture is on.

    Example::

        trace = client.get_trace(trace_id)
        trace.add_context({"refund_status": "approved"})
        trace.set_metadata({"region": "us-west"})
    """

    def __init__(self, client: Bitfab, trace_id: str) -> None:
        self._client = client
        self._trace_id = trace_id

    @property
    def trace_id(self) -> str:
        """The canonical Bitfab trace ID this handle resolves."""
        return self._trace_id

    def add_context(self, context: dict[str, Any]) -> None:
        """Append a context entry. Server-side appends to the contexts array;
        existing entries are preserved.

        No-op when context is not a dict. Raises if the server rejects the
        update.
        """
        if not isinstance(context, dict):
            return
        self._client.http_client.patch_trace(
            self._trace_id, {"appendContexts": [context]}
        )

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Merge metadata into this trace. Server-side shallow-merges new
        keys into the existing metadata object; existing keys are preserved
        unless overwritten.

        No-op when metadata is not a dict. Raises if the server rejects the
        update.
        """
        if not isinstance(metadata, dict):
            return
        self._client.http_client.patch_trace(
            self._trace_id, {"mergeMetadata": metadata}
        )

    def set_session_id(self, session_id: str) -> None:
        """Set the sessionId for this trace. Replaces any existing sessionId.

        No-op when session_id is empty. Raises if the server rejects the
        update.
        """
        if not isinstance(session_id, str) or not session_id:
            return
        self._client.http_client.patch_trace(
            self._trace_id, {"setSessionId": session_id}
        )

    def set_name(self, name: str) -> None:
        """Set the name for this trace. Replaces any existing name.

        No-op when name is empty. Raises if the server rejects the update.
        """
        if not isinstance(name, str) or not name:
            return
        self._client.http_client.patch_trace(self._trace_id, {"setName": name})


class _NoOpCurrentSpan:
    """No-op span handle returned when outside a span context."""

    @property
    def id(self) -> str:
        """Return empty string when outside a span context."""
        return ""

    @property
    def trace_id(self) -> str:
        """Return empty string when outside a span context."""
        return ""

    def add_context(self, context: dict[str, Any]) -> None:
        pass

    def set_prompt(self, prompt: str) -> None:
        pass


class _NoOpCurrentTrace:
    """No-op trace handle returned when outside a span context."""

    def set_session_id(self, session_id: str) -> None:
        pass

    def set_name(self, name: str) -> None:
        pass

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        pass

    def add_context(self, context: dict[str, Any]) -> None:
        pass

    def drop(self) -> None:
        pass


_NO_OP_SPAN = _NoOpCurrentSpan()
_NO_OP_TRACE = _NoOpCurrentTrace()


def get_current_span() -> CurrentSpan | _NoOpCurrentSpan:
    """Get a handle to the current active span.

    Call this from inside a traced function (decorated with ``@span``) to get
    a span handle that allows setting metadata at runtime.

    Returns a no-op object if called outside of a span context (methods do nothing).
    """
    stack = _get_span_stack()
    if stack:
        return CurrentSpan(stack[-1])
    return _NO_OP_SPAN


def get_current_replay_branch() -> ReplayBranch | None:
    """Get the database branch the current replay item is running against.

    Call this from inside a function being replayed with
    ``client.replay(db_branch=...)`` and point your database client at
    ``branch.database_url`` so the replay reads the data as it was at trace
    time::

        branch = get_current_replay_branch()
        url = branch.database_url if branch else os.environ["DATABASE_URL"]

    Returns ``None`` outside a replay item, and for an item whose source trace
    carried no DB snapshot reference, so live request code takes the same path
    it always did.
    """
    ctx: dict[str, Any] | None = _replay_context.get()
    if not ctx:
        return None
    lease = ctx.get("db_branch_lease")
    if not lease:
        return None
    # Surface the Bitfab trace ID (what the customer sees in the dashboard),
    # not the external trace ID. Falling back to the external one keeps replays
    # from external sources working until that path is fully wired.
    trace_id = ctx.get("source_bitfab_trace_id") or ctx.get("input_source_trace_id")
    if not trace_id:
        return None
    return ReplayBranch(lease, trace_id, ctx)


def get_current_trace() -> CurrentTrace | _NoOpCurrentTrace:
    """Get a handle to the current active trace.

    Call this from inside a traced function (decorated with ``@span``) to get
    a trace handle that allows setting trace-level context at runtime.

    Returns a no-op object if called outside of a span context (methods do nothing).
    """
    stack = _get_span_stack()
    if stack:
        return CurrentTrace(stack[-1]["traceId"])
    return _NO_OP_TRACE


def _run_with_span_stack(stack: list[SpanContext], fn: Callable[[], T]) -> T:
    """Run a function with a new span stack context."""
    token = _span_stack.set(stack)
    try:
        return fn()
    finally:
        _span_stack.reset(token)


def _run_finalize(
    finalize: Callable[[Any], Any], output: Any
) -> tuple[Any, str | None]:
    """Apply a sync ``finalize`` to a span output. Returns ``(recorded, error)``.

    ``finalize`` turns a non-serializable value (a live stream) into a
    serializable view for the span output. It never affects the caller's
    return value. A throwing ``finalize`` records an error instead of
    crashing the host; an async ``finalize`` on a sync span is an error
    (use an async function instead).
    """
    try:
        finalized = finalize(output)
        if inspect.isawaitable(finalized):
            if inspect.iscoroutine(finalized):
                finalized.close()
            return None, (
                "finalize failed: async finalize is not supported on a sync span; "
                "use an async function"
            )
        return finalized, None
    except Exception as e:  # never crash the host app
        return None, f"finalize failed: {e}"


async def _run_finalize_async(
    finalize: Callable[[Any], Any], output: Any
) -> tuple[Any, str | None]:
    """Async counterpart of :func:`_run_finalize`; awaits an async ``finalize``."""
    try:
        finalized = finalize(output)
        if inspect.isawaitable(finalized):
            finalized = await finalized
        return finalized, None
    except Exception as e:  # never crash the host app
        return None, f"finalize failed: {e}"


logger = logging.getLogger(__name__)


def _function_span_name(fn: Any) -> str | None:
    qualname = getattr(fn, "__qualname__", None) or getattr(fn, "__name__", None)
    if not qualname:
        return None
    return subtree.qualified_span_name(qualname)


class AllowedEnvVars(TypedDict, total=False):
    """Allowed environment variables for LLM providers.

    Only these keys are permitted when passing environment variables
    to the Bitfab client for local BAML execution.

    Attributes:
        OPENAI_API_KEY: OpenAI API key for GPT models
    """

    OPENAI_API_KEY: str


SpanOccurrence = Union[Literal["first", "last"], int]


class CapturedSpan(TypedDict):
    id: str
    traceId: str
    parentSpanId: str | None
    name: str | None
    type: str
    input: Any
    output: Any
    contexts: list[dict[str, Any]]
    prompt: str | None
    metadata: dict[str, Any]
    metrics: dict[str, Any] | None
    errors: Any
    startedAt: str | None
    endedAt: str | None


_SEED_INSIDE_RUNNING_LOOP = (
    "seed_trace('{key}', ...) was called from inside a running event loop. It "
    "runs the function to completion on its own loop, so call it from "
    "synchronous code (a script or a management command), not from a coroutine."
)


def _event_loop_is_running() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


async def _await(value: Awaitable[Any]) -> Any:
    return await value


class Bitfab:
    """Client for making provider-based API calls via BAML."""

    def __init__(
        self,
        api_key: ApiKeyInput | None = None,
        service_url: str | None = None,
        env_vars: AllowedEnvVars | None = None,
        capture_enabled: bool | None = None,
        baml_client: Any = None,
        strict: bool = False,
        trace_across_threads: bool | None = None,
        max_captured_subtree_spans: int | None = None,
        simulation_plan: bool = True,
        enabled: bool | None = None,
    ):
        """Initialize the Bitfab client.

        Args:
            api_key: The API key for Bitfab API authentication. Resolved lazily,
                the first time a span needs it, not at construction. Accepts a
                string or a function returning the key (resolved at first use,
                so it survives env loaded after import). When omitted or empty,
                the SDK falls back to reading ``BITFAB_API_KEY`` from the
                environment at first use.
            service_url: The base URL for the Bitfab API (default: https://bitfab.ai)
            env_vars: Environment variables for LLM provider API keys (only OPENAI_API_KEY is supported)
            capture_enabled: Whether traced calls are captured. When False,
                decorated functions run without recording a span and nothing is
                sent, except inside a replay item or the one call ``seed_trace``
                runs, which always record their trace. None (default): read
                ``BITFAB_CAPTURE_ENABLED`` (0 or 1) at first use, and capture
                when it is unset.
            baml_client: The generated BAML client instance (e.g., ``b`` from baml_client). Used by wrap_baml() when no explicit client is passed.
            strict: When True, the first traced call with no resolvable API key
                raises instead of disabling tracing quietly. Off by default so a
                missing key never crashes the host app; turn it on in standalone
                scripts where an untraced run is a failure you want surfaced.
            trace_across_threads: Nest spans from worker threads and thread
                pools under the trace that submitted the work, so replay mocks
                fire there (see ``bitfab/thread_propagation.py``).
                True: on. False: off. None (default): on only when
                ``BITFAB_TRACE_ACROSS_THREADS=1`` is set, otherwise off.
                Process-global once installed; a later False never uninstalls.
            max_captured_subtree_spans: Cap on discovered calls sent with their
                inputs and outputs, for every ``trace()`` that does not pass
                its own. None (default): read
                ``BITFAB_MAX_CAPTURED_SUBTREE_SPANS``, then use 500. Declared
                nodes, nested trace roots, framework integration spans, and
                spans the loaded sim plan turned capture off for do not count,
                so they keep recording past it. Spans sent without inputs and
                outputs only because the sim plan could not be read still
                count. Past it, further discovered calls with capture on record
                nothing.
            simulation_plan: Read the organization's sim plan and apply its
                content-capture decisions (default: True). The first read starts
                here, and a root span entered while it is in flight waits for it,
                for at most the read timeout, once per client. False behaves
                exactly like ``BITFAB_DISABLE_SIM_PLAN``: no read, no wait,
                nothing held back, nothing stripped.
            enabled: Deprecated alias for ``capture_enabled``. Warns once.
        """
        if enabled is not None:
            warn_once(
                "deprecated-enabled-option",
                "Bitfab(enabled=...) is deprecated; pass capture_enabled=... instead.",
            )
            capture_enabled = (
                enabled if capture_enabled is None else capture_enabled and enabled
            )
        self._api_key_config = api_key
        # Cached only once a non-empty key is found, so an early resolve (before
        # env loaded) can't poison a later one.
        self._resolved_api_key: str | None = None
        self._api_key_warned = False
        self.service_url = service_url or DEFAULT_SERVICE_URL
        self.env_vars = env_vars or {}
        self._capture_enabled_in_code = capture_enabled
        self._capture_enabled_from_env: bool | None = None
        self._strict = strict
        self.baml_client = baml_client
        # The key is NOT read here. HttpClient gets a callable so the key is
        # resolved at send time, after any in-script load_dotenv() has run.
        self.http_client = HttpClient(
            api_key=self._resolve_api_key,
            service_url=self.service_url,
        )
        self._simulation_plan = SimulationPlan(
            self.http_client, simulation_plan, self._discard_external_span
        )
        self.http_client.external_span_sender = self._send_external_span
        self.http_client.external_trace_sender = self._send_external_trace
        self.http_client.release_held_external_spans = self._simulation_plan.release
        self.http_client.stop_simulation_plan = self._simulation_plan.stop
        self.datasets = DatasetsClient(self.http_client)
        self.assertion_categories = AssertionCategoriesClient(self.http_client)
        self.organization_members = OrganizationMembersClient(self.http_client)
        self.traces = TracesClient(self.http_client)
        self.labels = LabelsClient(self.http_client)
        self.graders = GradersClient(self.http_client)
        self.experiments = ExperimentsClient(self.http_client)
        # Overrides registered via register_mock_override(); applied to every
        # replay after any per-call mock_override (per-call wins). See replay().
        self._mock_overrides: list[MockOverride] = []
        self._max_captured_subtree_spans_in_code = max_captured_subtree_spans
        self._max_captured_subtree_spans_from_env: int | None = None
        self._max_captured_subtree_spans_env_read = False
        resolved_trace_across_threads = (
            trace_across_threads
            if trace_across_threads is not None
            else os.environ.get("BITFAB_TRACE_ACROSS_THREADS", "").strip().lower()
            in ("1", "true", "yes")
        )
        if resolved_trace_across_threads:
            install_thread_propagation()
        start_commit_ref_resolution()
        self._simulation_plan.refresh()

    def _send_external_span(
        self, payload: dict[str, Any], submit: Callable[[dict[str, Any]], None]
    ) -> None:
        try:
            self._simulation_plan.send(
                payload, _root_trace_function_key_of(payload), submit
            )
        except Exception as error:
            warn_once(
                "external-span-dropped",
                f"a span was dropped because the send step failed: {error}",
            )

    def _discard_external_span(self, payload: dict[str, Any]) -> bool:
        trace_id = payload.get("sourceTraceId")
        raw_span = payload.get("rawSpan")
        span_id = raw_span.get("id") if isinstance(raw_span, dict) else None
        if not isinstance(trace_id, str) or not isinstance(span_id, str):
            return False
        return self.http_client.trace_completion.abort(trace_id, span_id)

    def _send_external_trace(
        self, payload: dict[str, Any], submit: Callable[[dict[str, Any]], None]
    ) -> None:
        try:
            self._simulation_plan.send_trace(payload, submit)
        except Exception as error:
            warn_once(
                "external-trace-dropped",
                f"a trace was dropped because the send step failed: {error}",
            )

    def close(self, timeout: float = 30.0) -> bool:
        """Flush and permanently close this client's tracing resources.

        Args:
            timeout: Maximum total seconds to wait.

        Returns:
            True when pending requests and transports closed within the deadline.
        """
        return self.http_client.close(timeout)

    def __enter__(self) -> Bitfab:
        """Return this client for use as a context manager."""
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        """Close tracing resources when leaving a context manager."""
        self.close()

    def register_mock_override(
        self,
        match_or_override: Union[str, NodeMatcher, MockOverride, MockOverrideResolver],
        value: MockValue = _REGISTER_VALUE_UNSET,
    ) -> None:
        """Register a mock override applied to every subsequent replay.

        A mock override injects a custom value into the spans its ``match``
        predicate selects during replay (full replacement of that span's
        output), so downstream real code runs against the substituted value.
        The ``value`` is either a flat value injected directly, or a callable
        invoked with a :class:`~bitfab.mock_override.MockOverrideCtx`. See
        :class:`~bitfab.mock_override.MockOverride`.

        Supported forms:

        * object: ``register_mock_override(MockOverride(match, value))``
        * ordered: ``register_mock_override(match, value)``
        * keyed: ``register_mock_override(trace_function_key, override_or_resolver)``
        * global resolver: ``register_mock_override(resolver)``; route on
          ``ctx.node.trace_function_key`` and return ``NO_MOCK_OVERRIDE`` to
          decline the current span

        Registered overrides apply after any per-call ``mock_override`` passed
        to :meth:`replay` (per-call wins for the same span), and both take
        precedence over the base ``mock`` strategy. Registrations accumulate;
        call :meth:`clear_mock_overrides` to reset.
        """
        if isinstance(match_or_override, str):
            trace_function_key = match_or_override
            if isinstance(value, MockOverride):
                keyed_match = value.match
                self._mock_overrides.append(
                    MockOverride(
                        match=lambda node: (
                            node.trace_function_key == trace_function_key
                            and keyed_match(node)
                        ),
                        value=value.value,
                    )
                )
                return
            if callable(value):
                self._mock_overrides.append(
                    MockOverride(
                        match=lambda node: (
                            node.trace_function_key == trace_function_key
                        ),
                        value=value,
                    )
                )
                return
            raise ValueError(
                "register_mock_override(trace_function_key, override) requires "
                "a MockOverride or callable resolver."
            )
        if isinstance(match_or_override, MockOverride):
            if value is not _REGISTER_VALUE_UNSET:
                raise ValueError(
                    "register_mock_override takes either a MockOverride, or a "
                    "(match, value) pair, not both."
                )
            self._mock_overrides.append(match_or_override)
            return
        if value is _REGISTER_VALUE_UNSET and callable(match_or_override):
            self._mock_overrides.append(
                MockOverride(match=lambda _node: True, value=match_or_override)
            )
            return
        if value is _REGISTER_VALUE_UNSET:
            raise ValueError(
                "register_mock_override(match, value) requires a value as the "
                "second argument."
            )
        self._mock_overrides.append(MockOverride(match=match_or_override, value=value))

    def clear_mock_overrides(self) -> None:
        """Remove all overrides registered via :meth:`register_mock_override`."""
        self._mock_overrides = []

    def _resolve_api_key_without_raising(self) -> str | None:
        replay_key = os.environ.get(REPLAY_API_KEY_ENV)
        if replay_key and replay_key.strip():
            return replay_key
        if self._resolved_api_key is not None:
            return self._resolved_api_key
        from_config = (
            self._api_key_config()
            if callable(self._api_key_config)
            else self._api_key_config
        )
        candidate = (
            from_config
            if from_config and from_config.strip()
            else os.environ.get("BITFAB_API_KEY")
        )
        key = candidate if candidate and candidate.strip() else None
        if key:
            self._resolved_api_key = key
        return key

    def _resolve_api_key(self) -> str | None:
        """Resolve the API key lazily, the first time a span actually needs it.

        The key is intentionally NOT read at construction. A module that builds
        the client at import time (e.g. ``Bitfab(api_key=os.environ.get(...))``)
        runs before the entrypoint's ``load_dotenv()`` when imported early, so
        the key would be empty at construction even though it is set moments
        later. Resolving here (first decorated call / first request) reads it
        after env loading has run.

        Resolution order: the configured value (string, or function called
        while still unresolved), then a fallback read of ``BITFAB_API_KEY`` from
        the environment. Once a non-empty key is found it is cached.
        """
        key = self._resolve_api_key_without_raising()
        if key:
            return key
        if self._strict:
            raise RuntimeError(
                "Bitfab: no API key resolved. Set BITFAB_API_KEY or pass "
                "api_key to Bitfab(). If a script loads env with dotenv, load "
                "it before importing the module that constructs the client "
                "(e.g. `dotenv run -- python script.py`), or pass "
                "api_key=lambda: os.environ.get('BITFAB_API_KEY')."
            )
        if self._capture_configured() and not self._api_key_warned:
            self._api_key_warned = True
            logger.warning(
                "Bitfab: api_key is empty - tracing is disabled. "
                "Provide a valid API key to enable tracing."
            )
        return None

    def _awaits_first_simulation_plan_read(self) -> bool:
        try:
            if _get_span_stack() or subtree.current_session() is not None:
                return False
            self._simulation_plan.refresh()
            return self._simulation_plan.awaiting_first_read()
        except Exception:
            return False

    def _resolve_max_captured_subtree_spans(self, override: int | None) -> int:
        if override is not None:
            return override
        if self._max_captured_subtree_spans_in_code is not None:
            return self._max_captured_subtree_spans_in_code
        if not self._max_captured_subtree_spans_env_read:
            self._max_captured_subtree_spans_from_env = read_positive_int_env(
                MAX_CAPTURED_SUBTREE_SPANS_ENV
            )
            self._max_captured_subtree_spans_env_read = True
        if self._max_captured_subtree_spans_from_env is not None:
            return self._max_captured_subtree_spans_from_env
        return subtree.DEFAULT_MAX_CAPTURED_SUBTREE_SPANS

    def _capture_configured(self) -> bool:
        """The on/off intent behind capture: what the constructor was passed
        when it was passed one, otherwise ``BITFAB_CAPTURE_ENABLED``, otherwise
        on. Read at first use and cached, so a client built at import time
        still sees env a script loaded afterwards."""
        if self._capture_enabled_in_code is not None:
            return self._capture_enabled_in_code
        if self._capture_enabled_from_env is None:
            from_env = read_boolean_env(CAPTURE_ENABLED_ENV)
            self._capture_enabled_from_env = True if from_env is None else from_env
        return self._capture_enabled_from_env

    def _is_capture_enabled(self) -> bool:
        """Whether capture is on, decided lazily at call time (not frozen at
        construction). ``capture_enabled=False`` short-circuits without ever
        touching the key."""
        if not self._capture_configured():
            return False
        return self._resolve_api_key() is not None

    def _should_record(self) -> bool:
        """Whether a traced call records a span right now: capture is on, or
        the call runs inside a replay item or a ``seed_trace`` call, which
        record regardless of the capture flag. Either way a key must resolve."""
        if (
            not self._capture_configured()
            and not _in_replay_item()
            and not _in_seed_scope()
        ):
            return False
        return self._resolve_api_key() is not None

    def _prepare_framework_integration(self) -> None:
        if self._capture_configured() and self._strict:
            self._resolve_api_key()

    @property
    def capture_enabled(self) -> bool:
        """Effective capture state, evaluated lazily: on only when not
        explicitly disabled AND an API key resolves. Reading this resolves the
        key (and may emit the one-time empty-key warning) exactly as the first
        traced call would. Replay records inside its items, and ``seed_trace``
        records its one call, even when this is False."""
        return self._is_capture_enabled()

    @property
    def enabled(self) -> bool:
        """Deprecated alias for ``capture_enabled``."""
        warn_once(
            "deprecated-enabled-property",
            "Bitfab.enabled is deprecated; read capture_enabled instead.",
        )
        return self._is_capture_enabled()

    @property
    def api_key(self) -> str | None:
        """The configured API key (the function form is resolved on read).
        Reflects what was passed to ``Bitfab(...)``; the ``BITFAB_API_KEY``
        environment fallback applied during actual tracing is not surfaced
        here, and reading this never warns."""
        return (
            self._api_key_config()
            if callable(self._api_key_config)
            else self._api_key_config
        )

    def _fetch_function_version(self, method_name: str) -> dict:
        """Fetch the function with its current version and BAML prompt from the server.

        Args:
            method_name: The name of the method to fetch

        Returns:
            Function version data including BAML prompt and providers

        Raises:
            ValueError: If function not found or has no prompt
        """
        result = self.http_client.lookup_function(method_name)

        # Check if function was not found
        if result.get("id") is None:
            raise ValueError(
                f'Function "{method_name}" not found. Create it at: {self.service_url}/functions'
            )

        # Check if function has no prompt
        if not result.get("prompt"):
            func_id = result.get("id")
            raise ValueError(
                f'Function "{method_name}" has no prompt configured. '
                f"Add one at: {self.service_url}/functions/{func_id}"
            )

        return result

    def call(self, method_name: str, **kwargs: Any) -> Any:
        """Call a method with the given named arguments via BAML execution.

        Args:
            method_name: The name of the method to call
            **kwargs: Named arguments to pass to the method

        Returns:
            The result of the BAML function execution

        Raises:
            ValueError: If no prompt is found or other API errors
        """
        try:
            function_version = self._fetch_function_version(method_name)
            execution_result = asyncio.run(
                run_function_with_baml(
                    function_version["prompt"],
                    kwargs,
                    function_version["providers"],
                    self.env_vars,
                )
            )

            # Create trace for the local execution
            # Serialize the result to JSON string
            if isinstance(execution_result.result, str):
                result_str = execution_result.result
            elif hasattr(execution_result.result, "model_dump"):
                result_str = json.dumps(execution_result.result.model_dump())
            elif hasattr(execution_result.result, "dict"):
                result_str = json.dumps(execution_result.result.dict())
            elif isinstance(execution_result.result, (dict, list)):
                result_str = json.dumps(execution_result.result)
            else:
                result_str = str(execution_result.result)

            # Create trace in background (fire-and-forget)
            trace_payload: dict[str, Any] = {
                "result": result_str,
                "source": "python-sdk",
            }
            if kwargs:
                trace_payload["inputs"] = kwargs
            if execution_result.raw_collector is not None:
                trace_payload["rawCollector"] = execution_result.raw_collector

            if self._should_record():
                self.http_client.send_internal_trace(
                    function_version["id"],
                    trace_payload,
                )

            return execution_result.result
        except Exception as e:
            logger.error(f"Error during local execution: {e}")
            raise

    def get_openai_tracing_processor(self):
        """Get a tracing processor for OpenAI Agents SDK integration.

        The processor implements the TracingProcessor interface from the OpenAI
        Agents SDK and can be registered to automatically capture traces and
        spans from agent execution.

        Example:
            ```python
            from bitfab import Bitfab
            from agents import add_trace_processor

            bitfab = Bitfab(api_key="your-api-key")
            processor = bitfab.get_openai_tracing_processor()

            # Add Bitfab without replacing other tracing processors.
            add_trace_processor(processor)
            ```

        Returns:
            A BitfabOpenAITracingProcessor instance configured for this client.
            Constructing it does not require openai-agents; only registering it
            with ``add_trace_processor`` does.

        See:
            https://openai.github.io/openai-agents-python/ref/tracing/
        """
        from bitfab.tracing import BitfabOpenAITracingProcessor

        self._prepare_framework_integration()
        return BitfabOpenAITracingProcessor(
            api_key="",
            service_url=self.service_url,
            get_active_span_context=_active_span_context,
            _http_client=self.http_client,
            _should_record=self._should_record,
        )

    def get_openai_agent_handler(self, trace_function_key: str):
        """Get an OpenAI Agents SDK handler that records a replayable root span.

        The processor from :meth:`get_openai_tracing_processor` captures
        everything inside a run (LLM calls, tools, handoffs) but never sees the
        caller's input, so a processor-only run records an empty-input root and
        is not replayable. This handler's ``wrap_run`` is a drop-in for
        ``Runner.run`` that opens a ``@bitfab.span`` root carrying the input and
        final output; the processor's spans nest beneath it. Register the
        processor once at startup, then call ``await handler.wrap_run(agent,
        input)`` in place of ``await Runner.run(agent, input)``.

        Example::

            from agents import Agent, Runner, add_trace_processor

            add_trace_processor(client.get_openai_tracing_processor())
            handler = client.get_openai_agent_handler("research-topic")
            result = await handler.wrap_run(agent, "Find X")

        Args:
            trace_function_key: Groups traces under this key in Bitfab

        Returns:
            A BitfabOpenAIAgentHandler instance configured for this client
        """
        from bitfab.openai_agent_sdk import BitfabOpenAIAgentHandler

        return BitfabOpenAIAgentHandler(
            client=self,
            trace_function_key=trace_function_key,
            get_active_span_context=_active_span_context,
        )

    def get_langgraph_callback_handler(self, trace_function_key: str):
        """Get a LangGraph/LangChain callback handler for tracing.

        The handler implements LangChain's BaseCallbackHandler and captures
        graph node execution, LLM calls, and tool invocations as Bitfab spans.

        Example::

            from bitfab import Bitfab

            bitfab = Bitfab(api_key="your-api-key")
            handler = bitfab.get_langgraph_callback_handler("my-agent")

            result = agent.invoke(
                {"messages": [...]},
                config={"callbacks": [handler]},
            )

        Args:
            trace_function_key: Groups traces under this key in Bitfab

        Returns:
            A BitfabLangGraphCallbackHandler instance configured for this client

        Raises:
            ImportError: If langchain-core is not installed
        """
        from bitfab.langgraph import BitfabLangGraphCallbackHandler

        self._prepare_framework_integration()
        return BitfabLangGraphCallbackHandler(
            api_key="",
            trace_function_key=trace_function_key,
            service_url=self.service_url,
            get_active_span_context=_active_span_context,
            _http_client=self.http_client,
            _should_record=self._should_record,
        )

    def get_langchain_callback_handler(self, trace_function_key: str):
        """Get a LangChain callback handler for tracing.

        Alias of :meth:`get_langgraph_callback_handler`. LangChain chains and
        LangGraph graphs share the same callback system, so one handler
        serves both.

        Example::

            from bitfab import Bitfab

            bitfab = Bitfab(api_key="your-api-key")
            handler = bitfab.get_langchain_callback_handler("my-chain")

            result = chain.invoke(input, config={"callbacks": [handler]})

        Args:
            trace_function_key: Groups traces under this key in Bitfab

        Returns:
            A BitfabLangGraphCallbackHandler instance configured for this client

        Raises:
            ImportError: If langchain-core is not installed
        """
        return self.get_langgraph_callback_handler(trace_function_key)

    def get_langgraph_integration(
        self,
        trace_function_key: str,
        *,
        mock_tools_on_replay: bool | list[str] | tuple[str, ...] = True,
    ) -> BitfabLangGraphIntegration:
        """Get experimental LangGraph callbacks and ``ToolNode`` replay hooks.

        The returned integration combines native ``wrap_tool_call`` /
        ``awrap_tool_call`` hooks for replayable tool execution with
        ``create_invoker()`` / ``create_async_invoker()`` for a
        callback-configured replayable graph entry point. Lower-level callback
        and root wrappers remain available. This API may change before it is
        stable.
        """
        from bitfab.langgraph import BitfabLangGraphCallbackHandler
        from bitfab.langgraph_integration import BitfabLangGraphIntegration

        self._prepare_framework_integration()
        callback_handler = BitfabLangGraphCallbackHandler(
            api_key="",
            trace_function_key=trace_function_key,
            service_url=self.service_url,
            get_active_span_context=_active_span_context,
            capture_tools=False,
            _http_client=self.http_client,
            _should_record=self._should_record,
        )
        return BitfabLangGraphIntegration(
            client=self,
            trace_function_key=trace_function_key,
            callback_handler=callback_handler,
            mock_tools_on_replay=mock_tools_on_replay,
        )

    def get_claude_agent_handler(self, trace_function_key: str):
        """Get a Claude Agent SDK handler for tracing.

        The handler captures LLM turns, tool invocations, and subagent
        execution as Bitfab spans with proper parent-child hierarchy.

        Example::

            from bitfab import Bitfab
            from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

            bitfab = Bitfab(api_key="your-api-key")
            handler = bitfab.get_claude_agent_handler("my-agent")

            options = handler.instrument_options(
                ClaudeAgentOptions(model="claude-sonnet-4-5-...")
            )

            async with ClaudeSDKClient(options=options) as client:
                await client.query("Do something")
                async for message in handler.wrap_response(client.receive_response()):
                    ...

        Args:
            trace_function_key: Groups traces under this key in Bitfab

        Returns:
            A BitfabClaudeAgentHandler instance configured for this client

        Raises:
            ImportError: If claude-agent-sdk is not installed
        """
        from bitfab.claude_agent_sdk import BitfabClaudeAgentHandler

        self._prepare_framework_integration()
        return BitfabClaudeAgentHandler(
            api_key="",
            trace_function_key=trace_function_key,
            service_url=self.service_url,
            get_active_span_context=_active_span_context,
            _http_client=self.http_client,
            _should_record=self._should_record,
        )

    def seed_trace(
        self,
        trace_function_key: str,
        fn: Callable,
        *,
        args: Sequence[Any] = (),
        kwargs: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        session_id: str | None = None,
        name: str | None = None,
    ) -> str:
        """Run ``fn`` once and record the execution as an original trace.

        Capture stays off: this records exactly one call, with the same
        semantics capture-on would give it (root span, first-party subtree
        under the ``trace`` decorator's bounds, no mocking). The result is an
        original under ``trace_function_key``: ``replay`` selects it, and each
        replay of it links back as ``original_trace_id``. ``metadata`` is
        stored on the trace and handed to the replay's ``adapt_inputs`` hook
        as ``ctx["metadata"]``.

        ``fn`` is resolved exactly as ``replay`` resolves it: a decorated
        function records under its own key (which must match), and a plain
        callable is wrapped under ``trace_function_key`` here. The recorded
        input is the real call and the output is what the run produced. An
        exception is recorded on the root span, the trace still persists, and
        the exception is re-raised.

        Call from synchronous code. An ``async def`` ``fn`` runs to completion
        on a fresh event loop; calling from inside a running loop raises.

        Args:
            trace_function_key: The key ``replay`` will select this trace by.
            fn: The function to run once.
            args: Positional arguments for the call.
            kwargs: Keyword arguments for the call.
            metadata: Stored on the trace and passed to ``adapt_inputs`` as
                ``ctx["metadata"]``. Put the case's provenance here.
            session_id: Optional session ID, to group related cases.
            name: The trace's title, and a field you can search and filter
                on. Put the case's own label here (a ticket id, a dataset row
                name) so the seeded trace is findable by it. Defaults to the
                trace function key.

        Returns:
            The trace ID, usable with ``replay(trace_ids=[...])``.
        """
        target, _, _ = _resolve_replay_fn(self, fn, trace_function_key)
        call_args = tuple(args)
        call_kwargs = dict(kwargs or {})
        is_async = inspect.iscoroutinefunction(target) or inspect.iscoroutinefunction(
            inspect.unwrap(fn)
        )
        if is_async and _event_loop_is_running():
            raise RuntimeError(_SEED_INSIDE_RUNNING_LOOP.format(key=trace_function_key))

        trace_id = str(uuid.uuid4())
        # No dbSnapshotRef: a seeded trace carries no database pin.
        trace_state: TraceState = {
            "traceId": trace_id,
            "traceFunctionKey": trace_function_key,
            "startedAt": now_iso_timestamp(),
            "contexts": [],
            "ingestionType": "seeded",
        }
        if session_id is not None:
            trace_state["sessionId"] = session_id
        if name is not None:
            trace_state["name"] = name
        if metadata:
            record_caller_trace_metadata(trace_id, metadata)
        _active_trace_states[trace_id] = trace_state

        token = _seed_context.set({"trace_id": trace_id})
        try:
            result = target(*call_args, **call_kwargs)
            if inspect.isawaitable(result):
                if _event_loop_is_running():
                    if inspect.iscoroutine(result):
                        result.close()
                    raise RuntimeError(
                        _SEED_INSIDE_RUNNING_LOOP.format(key=trace_function_key)
                    )
                asyncio.run(_await(result))
        finally:
            _seed_context.reset(token)
            unrecorded = _active_trace_states.pop(trace_id, None)
            flush_traces(timeout=30.0)
            retire_trace_metadata(trace_id)
        if unrecorded is not None:
            raise RuntimeError(
                f"seed_trace recorded nothing for '{trace_function_key}': the call "
                "finished without a root span. Check that an API key resolves "
                "(BITFAB_API_KEY or api_key=), and that fn is a regular or async "
                "function rather than a generator."
            )
        return trace_id

    def reseed_trace(
        self,
        trace_function_key: str,
        fn: Callable,
        *,
        trace_id: str,
    ) -> ReseedResult:
        source = self.http_client.get_reseed_source(trace_id)
        source_key = source.get("traceFunctionKey")
        if source_key != trace_function_key:
            raise ValueError(
                f"Trace {trace_id} belongs to '{source_key}', not '{trace_function_key}'."
            )
        _, _, auto_wrapped = _resolve_replay_fn(self, fn, trace_function_key)
        args, kwargs = _deserialize_inputs(
            {
                "input": source.get("input"),
                "inputSerialized": source.get("inputSerialized"),
            },
            dict_input_as_positional=auto_wrapped,
        )
        run_trace_id = self.seed_trace(
            trace_function_key,
            fn,
            args=args,
            kwargs=kwargs,
            metadata=source.get("metadata") or None,
            session_id=source.get("sessionId"),
            name=source.get("name"),
        )
        adopted = self.http_client.reseed_trace(trace_id, run_trace_id)
        return {
            "trace_id": adopted["traceId"],
            "previous_run_trace_id": adopted["previousRunTraceId"],
        }

    def replay(
        self,
        fn_or_key: Union[Callable, str] | None = None,
        fn: Callable | None = None,
        *,
        limit: int | None = None,
        trace_ids: list[str] | None = None,
        name: str | None = None,
        notes: str | None = None,
        metadata: dict[str, str] | None = None,
        max_concurrency: int | _ConcurrencyUnset | None = _CONCURRENCY_UNSET,
        code_change_description: Union[str, _CodeChangeUnset, None] = (
            _CODE_CHANGE_UNSET
        ),
        code_change_files: Union[
            list[CodeChangeFile], _CodeChangeUnset, None
        ] = _CODE_CHANGE_UNSET,
        experiment_group_id: str | None = None,
        dataset_id: str | None = None,
        dataset_ids: list[str] | None = None,
        grader_ids: list[str] | None = None,
        only_with_assertions: bool = False,
        skip_assertion_judging: bool = False,
        judge_assertions: bool | None = None,
        mock: MockStrategy = "marked",
        mock_override: Union[MockOverrideInput, list[MockOverrideInput]] | None = None,
        experimental_selective_replay: SelectiveReplayOptions | None = None,
        adapt_inputs: Callable[
            [list[Any], dict[str, Any], AdaptContext], tuple[list[Any], dict[str, Any]]
        ]
        | None = None,
        db_branch: DbBranchOptions | bool | None = None,
        dry_run: bool = False,
        attempts: int | _ConcurrencyUnset = _CONCURRENCY_UNSET,
        concurrency: ReplayConcurrency | None = None,
        process_launcher: ProcessLauncher | None = None,
        on_item_start: Callable[[ReplayItemStartProgress], None] | None = None,
        on_item_finish: Callable[[ReplayItemFinishProgress], None] | None = None,
        on_progress: Callable[[ReplayProgress], None] | None = None,
        on_experiment_start: Callable[[ReplayExperimentStart], None] | None = None,
        resume: str | None = None,
        force: bool = False,
        on_interrupt: Callable[[ReplayInterrupt], None] | None = None,
    ) -> ReplayResult:
        """Replay historical traces through a function and create an experiment.

        Fetches the last N traces for the given trace function key, re-runs each
        through the provided function (wrapped with span decorator for tracing),
        and returns comparison data.

        Two call forms:

        * ``client.replay(decorated_fn, ...)``: the trace function key is read
          from the ``@span`` decorator on the function.
        * ``client.replay("key", fn, ...)``: explicit key with any plain
          callable. Use this for handler-instrumented workflows
          (LangGraph/LangChain, Claude Agent SDK, OpenAI Agents), which record
          traces under a key with no decorated root function in the app. The
          SDK wraps ``fn`` in a span under the key internally, and a recorded
          dict root input (e.g. a LangGraph state) is passed as a single
          positional argument, matching the TypeScript SDK. (A decorated
          ``fn`` keeps decorated-path kwargs semantics even when a matching
          key is also passed.)

        Args:
            fn_or_key: The decorated function to replay, or an explicit trace
                function key string (with the callable as the next argument).
            fn: The callable to replay when ``fn_or_key`` is a key string.
            limit: Maximum number of traces to replay (default: 5; maximum:
                5,000). Ignored when ``trace_ids`` or a dataset is passed
                because either source already determines how many traces
                replay. Supplying ``trace_ids`` also emits a warning.
            trace_ids: Optional list of trace IDs to replay (max 100)
            name: What this run is testing, in a few words, such as
                'baseline' or 'shorter system prompt'. Bitfab records the
                commit, branch, tree state, datasets, and who ran it with every
                experiment, so do not repeat them here.
            notes: Run conditions Bitfab cannot see on its own, such as an
                environment override or a forced feature flag. Kept on the
                experiment next to its name.
            metadata: Caller-owned tags on the experiment, such as which
                schedule launched it. Read back and filtered on through
                ``client.experiments``.
            max_concurrency: Maximum number of items to process in parallel.
                Set to 1 for sequential execution, or None for unlimited. Defaults to 10.
            code_change_description: Optional rationale for the code change being
                tested in this replay. Stored on the resulting experiment. When
                supplied without ``code_change_files``, this text is preserved
                while the SDK automatically captures the files. Pass ``None``
                when the replay should have no description; use
                ``code_change_files=None`` to suppress automatic file capture.
            code_change_files: Optional list of files edited as part of this code
                change. Each entry is ``{"path", "before", "after"}``. Omit
                this argument to capture automatically, or pass ``None`` to
                suppress file capture for this replay.
            experiment_group_id: Optional UUID that groups multiple replay runs
                into a single experiment batch.
            dataset_id: Optional UUID of the dataset this replay runs against.
                Mutually exclusive with ``dataset_ids``. Stored on the resulting
                experiment for durable dataset attribution; validated
                server-side against the org.
            dataset_ids: Optional dataset UUIDs this replay runs against, for
                benchmarking one function against several corpora in a single
                run. Mutually exclusive with ``dataset_id``. The run replays the
                union of their traces, graded by the union of their graders, and
                is attributed to every one of them.
            grader_ids: Optional list of grader UUIDs attached directly to this
                experiment (max 100). At completion they are graded as the union
                with the dataset's runnable graders. Use it to grade a single run
                with a check you don't want to add permanently. Each must be an
                active/live grader in the same org and trace function, or the
                server rejects the replay.
            only_with_assertions: Replay only the selected traces that carry at
                least one approved assertion. Narrows whatever ``limit``,
                ``trace_ids`` or ``dataset_ids`` chose, so a run that measures
                assertion outcomes doesn't pay to re-execute traces nothing can
                grade. With ``limit`` it selects the N most recent traces that
                HAVE approved assertions, rather than filtering the N most
                recent down to however few do. An assertion still awaiting
                review doesn't count, because a replay is only judged against
                assertions a person has approved.
            skip_assertion_judging: Don't judge approved assertions on each
                replay. Judging is on by default: every approved assertion is
                judged as its replay finishes and the verdict is saved as that
                assertion's agent label, and each judgement costs model calls.
            mock: Mock strategy for child spans during replay.
                ``"marked"`` (default) only mocks child spans declared with
                ``mock_on_replay=True`` on ``@client.span(...)``; ``"none"``
                runs everything real; ``"all"`` returns every matched recorded
                child span's historical output. A selected occurrence that is unavailable
                errors the item without executing the real child.
            mock_override: Optional selective override(s) layered on top of
                ``mock``: a :class:`~bitfab.mock_override.MockOverride`, global
                resolver, or list. A resolver routes on
                ``ctx.node.trace_function_key`` and may return
                ``NO_MOCK_OVERRIDE`` to continue to lower-priority overrides
                and the base strategy. Per-call overrides are tried before any
                registered via
                :meth:`register_mock_override`, and fire even under
                ``mock="none"``. The root span is never overridden.
            experimental_selective_replay: Opt-in must_run manifest. The
                server protects required subtrees and ancestors, combining them
                with each trace's assertions and recorded
                replay_reusable declarations. Requires mock="marked" without
                overrides and in-process replay. Item selective_replay reports
                execution coverage, not assertion verdicts.
            adapt_inputs: Optional hook to reshape recorded inputs onto the
                current signature when the function's shape changed since the
                traces were captured. Receives ``(args, kwargs, AdaptContext)``
                and returns the ``(args, kwargs)`` passed to ``fn``.
            db_branch: ``True`` to branch with the mirror project's own sizing,
                or a :class:`DbBranchOptions` mapping to tune how each branch
                is sized and warmed. ``False`` and omission leave branching
                off. The server resolves a per-trace branch from each source
                trace's ``db_snapshot_ref``; read it inside ``fn`` with
                :func:`get_current_replay_branch` (the SDK releases each branch
                after its item).
            attempts: How many times each source trace is replayed in this
                run (1 to 100, default 1). Superseded by ``concurrency``.
            concurrency: Optional :class:`ReplayConcurrency` carrying
                ``attempts``, ``max_concurrency`` and the ``primitive`` that
                runs them. Passing it alongside the ``attempts``/
                ``max_concurrency`` arguments is an error.
            on_item_finish: Optional callback invoked once per item as it
                finishes, always with that item and running totals (a
                :class:`ReplayItemFinishProgress`). It never receives a
                whole-run completion event. Use it to render replay progress,
                for example a terminal progress bar. A raising callback never
                crashes the run.
            on_progress: Deprecated compatibility callback. It receives the
                same per-item events plus its legacy item-less terminal
                ``"complete"`` event. Ignored when ``on_item_finish`` is also
                provided.
            on_item_start: Optional callback invoked when a worker begins each
                item. Pair it with ``on_item_finish`` to distinguish queued work
                from in-flight work. A raising callback never crashes the run.
            on_experiment_start: Optional callback invoked once, as soon as the
                server has created the experiment and before any item runs,
                with its ``experiment_id`` and ``experiment_url``. Use it to
                show the experiment link even if the run later fails. A raising
                callback never crashes the run.
            resume: Experiment ID of a replay that stopped before every item
                finished. Runs only the traces and attempts that did not
                finish, in the same experiment, and returns the finished ones
                with ``carried_over=True`` and no payloads. Passing
                ``trace_ids``, ``limit``, ``dataset_id``, ``dataset_ids``,
                ``attempts``, ``grader_ids``, ``only_with_assertions`` or
                ``dry_run`` with it is an error, because the experiment
                already fixed them. Database branching and its settings also
                come from the experiment, so ``db_branch`` is ignored.
            force: Resume even when the experiment had activity in the last
                two minutes or its code change differs from the one it started
                with. Only valid with ``resume``.
            on_interrupt: Optional callback invoked when SIGINT (Ctrl-C) or
                SIGTERM stops the run after the experiment started, once the
                experiment is marked interrupted. It receives
                ``experiment_id``, ``experiment_url`` and ``signal``
                (``"SIGINT"`` or ``"SIGTERM"``). When it is set, replay prints
                nothing itself. Without it, replay prints
                ``[replay] Experiment <id> interrupted.``. Either way the
                signal then goes on to any handler installed before the run,
                or ends the process as it normally would.

        Returns:
            ReplayResult with items (input, result, original_output, error),
            experiment_id, and experiment_url (``test_run_id`` and
            ``test_run_url`` are deprecated aliases carrying the same values)
        """
        if isinstance(fn_or_key, str):
            if fn is None:
                raise ValueError(
                    'replay("key", fn) requires a callable as the second argument.'
                )
            trace_function_key: str | None = fn_or_key
            replay_fn = fn
        elif fn_or_key is None:
            # Keyword-style legacy call: client.replay(fn=decorated_fn). The
            # first positional used to be named `fn`, so keep that spelling
            # working.
            if fn is None:
                raise ValueError(
                    "replay requires a function: replay(decorated_fn) or "
                    'replay("key", fn).'
                )
            trace_function_key = None
            replay_fn = fn
        else:
            if fn is not None:
                raise ValueError(
                    "Pass either replay(decorated_fn) or replay('key', fn), "
                    "not two callables."
                )
            trace_function_key = None
            replay_fn = fn_or_key
        return _run_replay(
            self,
            replay_fn,
            trace_function_key=trace_function_key,
            limit=limit,
            trace_ids=trace_ids,
            name=name,
            notes=notes,
            metadata=metadata,
            max_concurrency=max_concurrency,
            code_change_description=code_change_description,
            code_change_files=code_change_files,
            experiment_group_id=experiment_group_id,
            dataset_id=dataset_id,
            dataset_ids=dataset_ids,
            grader_ids=grader_ids,
            only_with_assertions=only_with_assertions,
            skip_assertion_judging=skip_assertion_judging,
            judge_assertions=judge_assertions,
            mock=mock,
            mock_override=mock_override,
            experimental_selective_replay=experimental_selective_replay,
            adapt_inputs=adapt_inputs,
            db_branch=db_branch,
            dry_run=dry_run,
            attempts=attempts,
            concurrency=concurrency,
            process_launcher=process_launcher,
            on_item_start=on_item_start,
            on_item_finish=on_item_finish,
            on_progress=on_progress,
            on_experiment_start=on_experiment_start,
            resume=resume,
            force=force,
            on_interrupt=on_interrupt,
        )

    def span(
        self,
        trace_function_key: str,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        capture_when: CaptureWhen = "always",
        test_run_id: str | None = None,
        mock_on_replay: bool = False,
        replay_reusable: bool = False,
        finalize: Callable[[Any], Any] | None = None,
        experiment_id: str | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Decorator to wrap a function and automatically create a span for its inputs and outputs.

        The wrapped function behaves identically to the original, but sends
        span data to Bitfab in the background after each call. Nested spans
        are automatically tracked through async context propagation.

        ``span`` is the opt-in tracing surface: only the functions you
        decorate are recorded. :meth:`trace` and :meth:`node` are the opt-out
        surface, where everything beneath one root is recorded unless
        excluded. The two are never mixed in one call stack: a ``span`` call
        entered beneath an active ``trace`` raises :class:`MixedTracingError`.

        Example usage:
            ```python
            client = Bitfab(api_key="your-api-key")


            @client.span("order-processing")
            def process_order(order_id: str, items: list[str]) -> dict:
                # ... process order
                return {"total": 100}


            # With explicit span name and type
            @client.span("safety-check", name="ContentValidator", type="guardrail")
            def check_content(content: str) -> dict:
                return {"safe": True}


            # Async functions work too
            @client.span("fetch-data")
            async def fetch_data(url: str) -> dict:
                # ... fetch data
                return {"data": "result"}


            # Nested spans work automatically
            @client.span("outer-operation", type="agent")
            def outer():
                inner()  # This span will be a child of outer-operation


            @client.span("inner-operation", type="function")
            def inner():
                pass
            ```

        Args:
            trace_function_key: A string identifier for grouping spans (e.g., 'order-processing', 'user-auth')
            name: The name of the span. Defaults to the function name if available, otherwise the trace_function_key.
            type: The type of span. Defaults to "custom". Options: llm, agent, function, guardrail, handoff, custom
            capture_when: Controls whether the span may start a new trace. ``"always"``
                captures every call. ``"nested"`` captures only when another Bitfab
                span is active and otherwise runs the function untraced. Unknown
                values warn once and default to ``"always"``.
            test_run_id: Deprecated alias for ``experiment_id``.
            replay_reusable: Experimental output-only reuse of this entire subtree.
                Requires lossless JSON inputs/output, no hidden mutable reads,
                input mutation, identity dependence, or effects needed later.
                Declare at capture and replay; include all relevant changes in
                must_run. Ordinary replay is unaffected. Not a safety mock.
            mock_on_replay: When True, replay will reuse this span's historical output instead of
                executing the wrapped function under the default ``mock="marked"`` replay
                strategy; ignored outside replay and under the ``mock="all"``/``mock="none"``
                strategies.
                Use this for child spans that are expensive (paid LLM/API calls), slow, or
                non-deterministic - the root function still runs real code, only the marked
                descendants return their recorded output. A selected occurrence that is
                unavailable errors the item without executing the real child. Async-generator
                spans cannot be mocked; selecting one errors before iteration.
            finalize: Optional callable that records a serializable view of a
                non-serializable result (a live stream) as the span output, while the
                raw return value is handed back to the caller unchanged. Use it to trace
                streaming functions.

                What ``finalize`` receives depends on the wrapped function:

                - **async generator** (``async def ... yield``): the list of yielded
                    values (the streamed chunks), collected as they pass through to the
                    caller. This is non-destructive - the caller still receives every
                    chunk. Pass a prebuilt helper like ``finalizers.openai_chunks`` or
                    ``finalizers.anthropic_events`` to assemble ``{text, usage, ...}``.
                - **async / sync function**: the return value. finalize is applied
                    inline before the span is recorded - on an async span it is
                    awaited, so a live single-consumer stream returned here is blocked
                    on and consumed before the call returns. Prefer an async generator
                    for streaming; reserve this form for plain return values or results
                    with non-destructive accessors.

                The caller's return value is always the raw result, unchanged. On an
                async generator the recorded view is assembled in ``finally`` after
                iteration, so the caller has already received every chunk and nothing
                blocks. ``finalize`` may be async on an async (or async-generator) span;
                it must be sync on a sync span. If it raises, the span records an error
                instead of crashing the host.
            experiment_id: Optional experiment ID that attributes the span to an
                experiment.

        Returns:
            A decorator that wraps functions to create spans for inputs and outputs

        Raises:
            ValueError: If ``experiment_id`` and ``test_run_id`` are both passed
                with different values.
        """
        return self._span_impl(
            trace_function_key,
            name=name,
            type=type,
            capture_when=capture_when,
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="Bitfab.span"
            ),
            mock_on_replay=mock_on_replay,
            replay_reusable=replay_reusable,
            finalize=finalize,
            surface="opt-in",
        )

    def _span_impl(
        self,
        trace_function_key: str,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        capture_when: CaptureWhen = "always",
        experiment_id: str | None = None,
        mock_on_replay: bool = False,
        replay_reusable: bool = False,
        finalize: Callable[[Any], Any] | None = None,
        surface: CaptureSurface | None,
        mirror_in_enclosing_traces: bool = False,
        instrumentation: SpanInstrumentation | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        span_type = type
        explicit_name = name
        resolved_instrumentation = (
            instrumentation
            if instrumentation is not None
            else ("trace" if surface == "opt-out" else "span")
        )
        self._simulation_plan.refresh()

        def decorator(fn: Callable[P, T]) -> Callable[P, T]:
            is_async = inspect.iscoroutinefunction(fn)
            is_async_gen = inspect.isasyncgenfunction(fn)
            monitored_code = getattr(fn, "__code__", None)
            function_name = fn.__name__ or None
            # Span name priority: explicit name > qualified function name > trace_function_key
            span_name = explicit_name or _function_span_name(fn) or trace_function_key
            # `options` is kept lightweight and serializable: it is attached to
            # the wrapped function as `_bitfab_options` for introspection. The
            # wrappers close over `finalize` directly rather than reading it
            # here, so a callable never ends up on that attribute.
            options = {
                "name": explicit_name,
                "type": span_type,
                "capture_when": capture_when,
                "experiment_id": experiment_id,
                "mock_on_replay": mock_on_replay,
                "replay_reusable": replay_reusable,
            }

            # Detect if the decorated function is an instance/class method
            # so we can strip self/cls from the recorded span inputs
            try:
                sig = inspect.signature(fn)
                first_param = next(iter(sig.parameters), None)
                _is_method = first_param in ("self", "cls")
            except (ValueError, TypeError):
                _is_method = False

            def _build_span_context(
                args: tuple[Any, ...], kwargs: dict[str, Any]
            ) -> tuple[list[SpanContext], dict[str, Any], bool] | None:
                """Build span context and base params for tracing.

                Returns:
                    Tuple of (new_stack, base_params, is_root_span)
                """
                pending_variant = _node_variant.get()
                variant = None
                if pending_variant is not None:
                    _node_variant.set(None)
                    if pending_variant[0] is fn:
                        variant = pending_variant[1]
                resolved_capture_when: CaptureWhen = "always"
                if capture_when in ("always", "nested"):
                    resolved_capture_when = capture_when
                else:
                    warn_once(
                        f"invalid-capture-when:{trace_function_key}",
                        f"unknown capture_when value {capture_when!r}; defaulting to "
                        '"always". Valid values: "always", "nested".',
                    )

                current_stack = _get_span_stack()
                parent_context = current_stack[-1] if current_stack else None
                if (
                    surface == "opt-in"
                    and parent_context is not None
                    and parent_context.get("surface") == "opt-out"
                ):
                    raise _mixed_tracing_error("span", "trace")
                if resolved_capture_when == "nested" and parent_context is None:
                    return None

                enclosing_session = (
                    subtree.current_session()
                    if surface == "opt-out" and parent_context is None
                    else None
                )
                replay_ctx = _replay_context.get()
                seed_ctx = _seed_context.get()
                if parent_context:
                    trace_id = parent_context["traceId"]
                elif enclosing_session is not None:
                    trace_id = str(uuid.uuid4())
                else:
                    trace_id = (
                        (replay_ctx.get("trace_id") if replay_ctx else None)
                        or (seed_ctx.get("trace_id") if seed_ctx else None)
                        or str(uuid.uuid4())
                    )
                span_id = str(uuid.uuid4())
                parent_span_id = parent_context["spanId"] if parent_context else None
                is_root_span = parent_span_id is None
                if is_root_span:
                    variant = None
                variant_chain = extend_variant_chain(
                    parent_context.get("variantChain", ()) if parent_context else (),
                    span_name,
                    variant,
                )

                executing_thread = threading.current_thread()
                runtime: dict[str, Any] = {
                    "thread_id": executing_thread.ident,
                    "thread_name": executing_thread.name,
                }
                if parent_context is not None:
                    parent_thread_id = parent_context.get("threadId")
                    if parent_thread_id is not None:
                        runtime["parent_thread_id"] = parent_thread_id
                submit_origin = _submit_origin.get()
                if submit_origin is not None:
                    runtime["submit_thread_id"] = submit_origin["thread_id"]
                    runtime["submit_thread_name"] = submit_origin["thread_name"]

                root_state_at_open = _active_trace_states.get(trace_id)
                new_context: SpanContext = {
                    "traceId": trace_id,
                    "spanId": span_id,
                    "threadId": executing_thread.ident or 0,
                    "spanName": span_name,
                    "rootTraceFunctionKey": (
                        root_state_at_open.get("traceFunctionKey", trace_function_key)
                        if root_state_at_open
                        else trace_function_key
                    ),
                    "instrumentation": resolved_instrumentation,
                    "declaredNode": mirror_in_enclosing_traces,
                    "isRoot": is_root_span,
                }
                if surface is not None:
                    new_context["surface"] = surface
                if variant_chain:
                    new_context["variantChain"] = variant_chain
                if enclosing_session is not None:
                    new_context["enclosingTrace"] = {
                        "trace_id": enclosing_session.trace_id,
                        "trace_function_key": enclosing_session.label,
                    }
                nearest_captured_ancestor_span_id = (
                    self._nearest_captured_ancestor_span_id(current_stack)
                )
                new_stack = [*current_stack, new_context]
                resolved_experiment_id = (
                    replay_ctx["experiment_id"] if replay_ctx else experiment_id
                )
                input_source_span_id = (
                    replay_ctx.get("input_source_span_id") if replay_ctx else None
                )
                input_source_trace_id = (
                    replay_ctx.get("input_source_trace_id") if replay_ctx else None
                )
                replay_attempt = (
                    replay_ctx.get("replay_attempt") if replay_ctx else None
                )

                started_at = now_iso_timestamp()
                if is_root_span:
                    self._simulation_plan.refresh()
                if is_root_span and trace_id not in _active_trace_states:
                    new_state = TraceState(
                        traceId=trace_id,
                        traceFunctionKey=trace_function_key,
                        startedAt=started_at,
                        dbSnapshotRef=build_snapshot_ref(started_at),
                    )
                    if resolved_experiment_id is not None:
                        new_state["experimentId"] = resolved_experiment_id
                    if input_source_trace_id is not None:
                        new_state["inputSourceTraceId"] = input_source_trace_id
                    if replay_attempt is not None:
                        new_state["replayAttempt"] = replay_attempt
                    _active_trace_states[trace_id] = new_state

                # Strip self/cls from recorded args for methods
                recorded_args = args[1:] if _is_method and args else args

                root_state = _active_trace_states.get(trace_id)
                root_trace_function_key = (
                    root_state.get("traceFunctionKey", trace_function_key)
                    if root_state
                    else trace_function_key
                )

                base_params = {
                    "trace_function_key": trace_function_key,
                    "root_trace_function_key": root_trace_function_key,
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "parent_span_id": parent_span_id,
                    "nearest_captured_ancestor_span_id": nearest_captured_ancestor_span_id,
                    "raw_args": recorded_args,
                    "raw_kwargs": kwargs,
                    "started_at": started_at,
                    "function_name": function_name,
                    "span_name": span_name,
                    "span_type": span_type,
                    "experiment_id": resolved_experiment_id,
                    "input_source_span_id": input_source_span_id,
                    "is_root_span": is_root_span,
                    "runtime": runtime,
                    "instrumentation": resolved_instrumentation,
                    "variant": variant,
                    "replay_reusable": replay_reusable,
                    "replay_json_safe": (replay_reusable or mock_on_replay)
                    and finalize is None
                    and not is_async_gen
                    and not inspect.isgeneratorfunction(fn),
                }

                self.http_client.trace_completion.start(trace_id, span_id)
                return new_stack, base_params, is_root_span

            def _get_ended_at() -> str:
                return now_iso_timestamp()

            def _safe_send_span(span_context: SpanContext, **send_kwargs: Any) -> None:
                try:
                    runtime_contexts: list[ContextEntry] = span_context.get(
                        "contexts", []
                    )
                    if runtime_contexts:
                        send_kwargs["contexts"] = runtime_contexts
                    runtime_prompt: str | None = span_context.get("prompt")
                    if runtime_prompt is not None:
                        send_kwargs["prompt"] = runtime_prompt
                    enclosing_trace = span_context.get("enclosingTrace")
                    if enclosing_trace is not None:
                        send_kwargs["enclosing_trace"] = enclosing_trace
                    self._send_span(
                        **send_kwargs, declared_node=mirror_in_enclosing_traces
                    )
                except Exception as error:
                    span_name = send_kwargs.get("span_name") or send_kwargs.get(
                        "trace_function_key"
                    )
                    warn_once(
                        f"span-send-failed:{span_name}",
                        f"span '{span_name}' was not sent ({_safe_type_name(error)}: {error}); its child spans will appear without a parent",
                    )
                finally:
                    self.http_client.trace_completion.end(
                        span_context["traceId"], span_context["spanId"]
                    )

            def _resolve_recorded_output(
                mock_entry: dict[str, Any],
                fetch_span_output: Callable[[str], Any] | None,
            ) -> Any:
                """Resolve a mock tree entry's ORIGINAL recorded output.

                Prefer an inline output when the (eager) tree carried one
                (``mock="all"``, or an older server that returns outputs
                regardless of ``includeOutputs``); only when the payload-free
                tree omitted it does this fetch lazily by ``externalSpanId``
                through the memoized ``fetch_span_output``. Absence of the
                ``output``/``outputMeta`` keys (not a ``None`` value) is what
                distinguishes "no inline output" from "recorded output is None".
                Both the base "marked"/"all" path and an override's
                ``get_original_output`` go through here, so the memoization means
                a span read twice fetches once.
                """
                has_inline = "output" in mock_entry or "outputMeta" in mock_entry
                if (
                    not has_inline
                    and fetch_span_output is not None
                    and mock_entry.get("externalSpanId")
                ):
                    return fetch_span_output(mock_entry["externalSpanId"])
                output = mock_entry.get("output")
                output_meta = mock_entry.get("outputMeta")
                if output_meta is not None:
                    # Fail open: a deserialization error falls back to the raw
                    # JSON output rather than aborting the mocked replay, matching
                    # the guard the base marked/all path has always applied.
                    with contextlib.suppress(Exception):
                        output = deserialize_value(
                            {"json": output, "meta": output_meta}
                        )
                return output

            def _plan_mock_replay(
                is_root_span: bool, variant: str | None, variant_chain: VariantChain
            ) -> tuple[Any, ...] | None:
                """Decide whether this child span is mocked, WITHOUT doing any
                blocking work.

                Advances the per-(key, name) call counter and runs the override
                match / base-strategy eligibility check, all synchronously. The
                counter advance MUST stay on the caller's thread (the event loop
                for async roots): replay runs sibling spans concurrently via
                ``asyncio.gather``, and moving the read-modify-write off the loop
                would let two same-(key, name) children reuse one mock index. The
                actual output fetch and any override value function (both of which
                can block on HTTP) are deferred to :func:`_execute_mock_plan`, so
                only that part is safe to offload.

                Returns ``None`` when the span runs real code, otherwise an
                override-chain plan or a base-strategy plan.
                """
                replay_ctx = _replay_context.get()
                call_index, mock_entry = MATCHER.claim(
                    replay_ctx,
                    trace_function_key=trace_function_key,
                    span_name=span_name,
                    is_root_span=is_root_span,
                    variant_chain=variant_chain,
                )
                if call_index is None:
                    return None
                matched_chain = MATCHER.matched_variant_chain(replay_ctx, variant_chain)
                fetch_span_output = replay_ctx.get("fetch_span_output")  # type: ignore[union-attr]

                # Override chain: overrides win over the base strategy. The root
                # span is already excluded (call_index is None for it), so an
                # override that matches the root key never applies. The matcher
                # runs on structural metadata only (no output), so it stays here
                # in the non-blocking plan.
                overrides = replay_ctx.get("mock_overrides") or []  # type: ignore[union-attr]
                if overrides:
                    node = SpanNodeMeta(
                        trace_function_key=trace_function_key,
                        span_name=span_name,
                        type=span_type,
                        original_span_id=(
                            mock_entry.get("sourceSpanId") if mock_entry else None
                        ),
                        variant=variant,
                    )
                    matched = [o for o in overrides if o.match(node)]
                    if matched:
                        return (
                            "overrides",
                            matched,
                            node,
                            call_index,
                            mock_entry,
                            fetch_span_output,
                            replay_ctx.get("mock_strategy"),  # type: ignore[union-attr]
                            mock_on_replay,
                            matched_chain,
                        )

                # Base strategy fallthrough.
                strategy = replay_ctx.get("mock_strategy")  # type: ignore[union-attr]
                if strategy == "marked":
                    if not mock_on_replay:
                        return None
                elif strategy != "all":
                    return None
                if not mock_entry:
                    raise _missing_recording_error(
                        trace_function_key, span_name, call_index, matched_chain
                    )
                return ("base", mock_entry, fetch_span_output)

            def _execute_mock_plan(
                plan: tuple[Any, ...],
                new_stack: list[SpanContext],
                base_params: dict[str, Any],
                args: tuple[Any, ...],
                kwargs: dict[str, Any],
            ) -> Any:
                """Run a plan from :func:`_plan_mock_replay` and return the injected
                output, recording a ``mocked=True`` span.

                This is the part that can block on HTTP (the lazy recorded-output
                fetch, or an override value function calling ``get_original_output``),
                so the async wrapper offloads it to a worker thread. The counter has
                already advanced in the plan step, so running here off the loop is
                race-free.
                """
                kind = plan[0]
                if kind == "overrides":
                    (
                        _,
                        matched_overrides,
                        node,
                        call_index,
                        mock_entry,
                        fetch_span_output,
                        strategy,
                        mock_on_replay,
                        matched_chain,
                    ) = plan

                    def get_original_output() -> Any:
                        if not mock_entry:
                            raise RuntimeError(
                                "mock_override.get_original_output() has no "
                                f"recorded output for span '{trace_function_key}'"
                                f":'{span_name}': the live span has no "
                                "counterpart in the replayed trace."
                            )
                        return _resolve_recorded_output(mock_entry, fetch_span_output)

                    ctx = MockOverrideCtx(
                        node=node,
                        inputs=list(args),
                        kwargs=dict(kwargs),
                        get_original_output=get_original_output,
                    )
                    kind = "override"
                    for matched in matched_overrides:
                        raw_value = matched.value
                        injected = raw_value(ctx) if callable(raw_value) else raw_value
                        if injected is not NO_MOCK_OVERRIDE:
                            break
                    else:
                        should_mock = strategy == "all" or (
                            strategy == "marked" and mock_on_replay
                        )
                        if not should_mock:
                            return NO_MOCK_OVERRIDE
                        if not mock_entry:
                            raise _missing_recording_error(
                                trace_function_key,
                                span_name,
                                call_index,
                                matched_chain,
                            )
                        injected = _resolve_recorded_output(
                            mock_entry, fetch_span_output
                        )
                        kind = "base"
                else:
                    _, mock_entry, fetch_span_output = plan
                    injected = _resolve_recorded_output(mock_entry, fetch_span_output)

                _safe_send_span(
                    new_stack[-1],
                    **base_params,
                    result=injected,
                    error=None,
                    ended_at=_get_ended_at(),
                    mocked=True,
                    # Both paths short-circuit the call, so the target is always
                    # the output; only where the value came from differs.
                    mock_target="output",
                    mock_source="override" if kind == "override" else "recorded",
                )
                return injected

            def _check_mock_replay(
                new_stack: list[SpanContext],
                base_params: dict[str, Any],
                is_root_span: bool,
                args: tuple[Any, ...],
                kwargs: dict[str, Any],
            ) -> tuple[bool, Any]:
                """Short-circuit a child span during replay (synchronous path).

                Plans and executes in one call. Returns ``(True, output)`` when
                this span is mocked, ``(False, None)`` otherwise. When mocked,
                records the span so the experiment reflects the mocked execution.
                """
                selective = (_replay_context.get() or {}).get("selective_replay")
                if selective is not None:
                    mocked, output = selective.enter(
                        trace_function_key=trace_function_key,
                        span_name=span_name,
                        span_id=base_params["span_id"],
                        parent_span_id=base_params["parent_span_id"],
                        inputs=list(base_params["raw_args"]),
                        kwargs=kwargs,
                        safety_mock=mock_on_replay,
                        can_reuse_output=finalize is None
                        and not is_async_gen
                        and not inspect.isgeneratorfunction(fn)
                        and base_params["variant"] is None,
                        reuse_allowed=replay_reusable is True,
                    )
                    if mocked:
                        _safe_send_span(
                            new_stack[-1],
                            **base_params,
                            result=output,
                            error=None,
                            ended_at=_get_ended_at(),
                            mocked=True,
                            mock_target="output",
                            mock_source="recorded",
                        )
                    return mocked, output
                plan = _plan_mock_replay(
                    is_root_span,
                    base_params["variant"],
                    new_stack[-1].get("variantChain", ()),
                )
                if plan is None:
                    return False, None
                output = _execute_mock_plan(plan, new_stack, base_params, args, kwargs)
                if output is NO_MOCK_OVERRIDE:
                    return False, None
                return True, output

            def _safe_build_span_context(
                args: tuple[Any, ...], kwargs: dict[str, Any]
            ) -> tuple[list[SpanContext], dict[str, Any], bool] | None:
                """Run ``_build_span_context`` fail-open.

                Tracing is a side-channel: if span setup fails for any reason,
                the user's function must still run. Returns the build result, or
                ``None`` when nested-only capture has no parent or setup failed,
                signaling the caller to run the wrapped function untraced.
                ``_build_span_context`` registers trace state only as its final
                mutating step, so an exception here happens before registration
                and leaves no orphaned state to clean up.
                """
                try:
                    return _build_span_context(args, kwargs)
                except MixedTracingError:
                    raise
                except Exception:
                    # During replay (a controlled eval) a setup failure must
                    # surface, not silently run untraced: swallowing it would
                    # execute the real function with real side effects and skew
                    # the experiment. The never-crash fallback is for production
                    # hosts only.
                    if _replay_context.get():
                        raise
                    warn_once(
                        f"span-setup:{trace_function_key}",
                        f"span setup failed for '{trace_function_key}'; this "
                        "call runs untraced. Your function still executes and "
                        "returns normally.",
                    )
                    return None

            def _safe_check_mock_replay(
                new_stack: list[SpanContext],
                base_params: dict[str, Any],
                is_root_span: bool,
                args: tuple[Any, ...],
                kwargs: dict[str, Any],
            ) -> tuple[bool, Any]:
                """Run ``_check_mock_replay`` fail-open in production.

                In production this never runs a mock (no replay context), so the
                guard only matters under replay. There a malformed mock tree must
                surface, not silently run the real function: swallowing it would
                produce real side effects and skew the mock call counter,
                defeating the replay. So we re-raise during replay and only
                degrade to "unmocked" if somehow reached outside it.
                """
                try:
                    return _check_mock_replay(
                        new_stack, base_params, is_root_span, args, kwargs
                    )
                except Exception:
                    if _replay_context.get():
                        self.http_client.trace_completion.abort(
                            base_params["trace_id"], base_params["span_id"]
                        )
                        raise
                    warn_once(
                        f"mock-replay:{trace_function_key}",
                        f"replay mock lookup failed for '{trace_function_key}'; "
                        "running the real function instead of a recorded output.",
                    )
                    return False, None

            if is_async_gen:
                # Async-generator functions (`async def fn(...): yield ...`) return
                # an async generator synchronously, so the sync_wrapper branch would
                # close the span before the body ever ran - every nested with_span
                # inside the body would then become its own root trace. Iterate the
                # generator inside the span context and send the span once after
                # iteration completes (or errors).
                @functools.wraps(fn)
                async def async_gen_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                    # Decided per call, never at decoration: the key can load
                    # after this wrapper is built, and a replay item records
                    # with capture off.
                    if not self._should_record():
                        async for value in fn(*args, **kwargs):
                            yield value
                        return
                    if (
                        capture_when != "nested"
                        and self._awaits_first_simulation_plan_read()
                    ):
                        with contextlib.suppress(RuntimeError):
                            await asyncio.to_thread(
                                self._simulation_plan.wait_for_first_read
                            )
                    setup = _safe_build_span_context(args, kwargs)
                    if setup is None:
                        # Span setup failed: stream the user's generator
                        # directly, untraced, so the call still works.
                        async for value in fn(*args, **kwargs):
                            yield value
                        return
                    new_stack, base_params, is_root_span = setup
                    span_ctx = new_stack[-1]

                    # Async generators cannot be replaced by one recorded
                    # return value. The counter still advances so later sibling
                    # spans stay aligned, but a strategy or override that
                    # selects this span must fail closed before iteration.
                    call_index: int | None = None
                    replay_ctx = _replay_context.get()
                    if (replay_ctx or {}).get("selective_replay") is not None:
                        _safe_check_mock_replay(
                            new_stack, base_params, is_root_span, args, kwargs
                        )
                    variant_chain = span_ctx.get("variantChain", ())
                    call_index, _ = MATCHER.claim(
                        replay_ctx,
                        trace_function_key=trace_function_key,
                        span_name=span_name,
                        is_root_span=is_root_span,
                        variant_chain=variant_chain,
                    )
                    strategy = (replay_ctx or {}).get("mock_strategy")
                    base_selected = strategy == "all" or (
                        strategy == "marked" and mock_on_replay
                    )

                    overrides = (replay_ctx or {}).get("mock_overrides") or []
                    override_selected = False
                    if overrides and call_index is not None:
                        matched_key = MATCHER.key_for(
                            replay_ctx,
                            trace_function_key=trace_function_key,
                            span_name=span_name,
                            variant_chain=variant_chain,
                        )
                        mock_entry = (replay_ctx.get("mock_tree") or {}).get(
                            f"{matched_key}:{call_index}"
                        )
                        node = SpanNodeMeta(
                            trace_function_key=trace_function_key,
                            span_name=span_name,
                            type=span_type,
                            original_span_id=(
                                mock_entry.get("sourceSpanId") if mock_entry else None
                            ),
                            variant=base_params["variant"],
                        )

                        def get_original_output() -> Any:
                            if not mock_entry:
                                raise RuntimeError(
                                    "mock_override.get_original_output() has no "
                                    f"recorded output for span '{trace_function_key}'"
                                    f":'{span_name}': the live span has no "
                                    "counterpart in the replayed trace."
                                )
                            return _resolve_recorded_output(
                                mock_entry, replay_ctx.get("fetch_span_output")
                            )

                        override_ctx = MockOverrideCtx(
                            node=node,
                            inputs=list(args),
                            kwargs=dict(kwargs),
                            get_original_output=get_original_output,
                        )
                        for override in overrides:
                            if not override.match(node):
                                continue
                            raw_value = override.value
                            injected = (
                                raw_value(override_ctx)
                                if callable(raw_value)
                                else raw_value
                            )
                            if injected is not NO_MOCK_OVERRIDE:
                                override_selected = True
                                break

                    if base_selected or override_selected:
                        self.http_client.trace_completion.abort(
                            span_ctx["traceId"], span_ctx["spanId"]
                        )
                        raise RuntimeError(
                            "Replay selected async-generator span "
                            f"'{trace_function_key}:{span_name}' for mocking, but "
                            "async-generator spans cannot be mocked. The real span "
                            "was not executed; move unsafe work to a mockable sync "
                            "or coroutine descendant."
                        )

                    yielded: list[Any] = []
                    return_value: Any = None
                    error_msg: str | None = None
                    sent = False
                    iterator = fn(*args, **kwargs)

                    try:
                        while True:
                            token = _span_stack.set(new_stack)
                            try:
                                with subtree.borrowed_span(
                                    monitored_code,
                                    span_ctx["traceId"],
                                    span_ctx["spanId"],
                                ):
                                    try:
                                        value = await iterator.__anext__()
                                    except StopAsyncIteration:
                                        return
                            finally:
                                _span_stack.reset(token)
                            yielded.append(value)
                            yield value
                    except asyncio.CancelledError as e:
                        error_msg = str(e) or e.__class__.__name__
                        raise
                    except Exception as e:
                        error_msg = str(e)
                        raise
                    finally:
                        token = _span_stack.set(new_stack)
                        try:
                            try:
                                with subtree.borrowed_span(
                                    monitored_code,
                                    span_ctx["traceId"],
                                    span_ctx["spanId"],
                                ):
                                    await iterator.aclose()
                            except asyncio.CancelledError as e:
                                error_msg = str(e) or e.__class__.__name__
                                raise
                            except Exception as e:
                                error_msg = str(e)
                                raise
                            finally:
                                if not sent:
                                    sent = True
                                    try:
                                        # finalize (when set and the generator didn't
                                        # error) turns the collected chunks into a
                                        # serializable summary; otherwise record the
                                        # raw collected output.
                                        if finalize is not None and error_msg is None:
                                            (
                                                output,
                                                finalize_error,
                                            ) = await _run_finalize_async(
                                                finalize, yielded
                                            )
                                            send_error = finalize_error
                                        else:
                                            output = {
                                                "yielded": yielded,
                                                "return": return_value,
                                            }
                                            send_error = error_msg
                                    except asyncio.CancelledError as e:
                                        _safe_send_span(
                                            span_ctx,
                                            **base_params,
                                            result=None,
                                            error=str(e) or e.__class__.__name__,
                                            ended_at=_get_ended_at(),
                                        )
                                        raise
                                    else:
                                        _safe_send_span(
                                            span_ctx,
                                            **base_params,
                                            result=output,
                                            error=send_error,
                                            ended_at=_get_ended_at(),
                                        )
                        finally:
                            with contextlib.suppress(ValueError):
                                _span_stack.reset(token)

                async_gen_wrapper._bitfab_wrapped = True  # type: ignore[attr-defined]
                async_gen_wrapper._bitfab_options = options  # type: ignore[attr-defined]
                async_gen_wrapper._bitfab_trace_function_key = trace_function_key  # type: ignore[attr-defined]
                return async_gen_wrapper  # type: ignore[return-value]
            elif is_async:

                @functools.wraps(fn)
                async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                    # Decided per call, never at decoration: the key can load
                    # after this wrapper is built, and a replay item records
                    # with capture off.
                    if not self._should_record():
                        return await fn(*args, **kwargs)
                    if (
                        capture_when != "nested"
                        and self._awaits_first_simulation_plan_read()
                    ):
                        with contextlib.suppress(RuntimeError):
                            await asyncio.to_thread(
                                self._simulation_plan.wait_for_first_read
                            )
                    setup = _safe_build_span_context(args, kwargs)
                    if setup is None:
                        # Span setup failed: run untraced so the call still works.
                        return await fn(*args, **kwargs)
                    new_stack, base_params, is_root_span = setup
                    span_ctx = new_stack[-1]

                    # Executing a mock plan can block on HTTP (the lazy
                    # recorded-output fetch for a non-"all" replay tree, or an
                    # async override value function). An async root is awaited directly
                    # on the event loop and replay runs items concurrently via
                    # asyncio.gather, so that blocking work would stall every other
                    # in-flight item. When the lazy fetcher is active, PLAN
                    # synchronously on the loop (this advances the per-(key, name)
                    # counter, which must not race across gather'd sibling spans),
                    # then offload only the blocking EXECUTE to a worker thread
                    # (asyncio.to_thread propagates the replay contextvar). The
                    # counter has already advanced before the await, so the
                    # offload is race-free. Otherwise no path blocks, so run the
                    # combined check inline and skip the thread hop.
                    replay_ctx = _replay_context.get()
                    if replay_ctx is not None and (
                        replay_ctx.get("fetch_span_output") is not None
                    ):
                        # In replay a plan/execute failure must surface (it skews
                        # the experiment), so no fail-open guard here: this branch
                        # only runs under an active replay context.
                        try:
                            plan = _plan_mock_replay(
                                is_root_span,
                                base_params["variant"],
                                span_ctx.get("variantChain", ()),
                            )
                            if plan is not None:
                                mocked_output = await asyncio.to_thread(
                                    _execute_mock_plan,
                                    plan,
                                    new_stack,
                                    base_params,
                                    args,
                                    kwargs,
                                )
                                if mocked_output is not NO_MOCK_OVERRIDE:
                                    return mocked_output  # type: ignore[no-any-return]
                        except Exception:
                            self.http_client.trace_completion.abort(
                                span_ctx["traceId"], span_ctx["spanId"]
                            )
                            raise
                    else:
                        mocked, mocked_output = _safe_check_mock_replay(
                            new_stack, base_params, is_root_span, args, kwargs
                        )
                        if mocked:
                            return mocked_output  # type: ignore[no-any-return]

                    token = _span_stack.set(new_stack)
                    try:
                        with subtree.borrowed_span(
                            monitored_code,
                            span_ctx["traceId"],
                            span_ctx["spanId"],
                            name=span_name if mirror_in_enclosing_traces else None,
                            span_type=span_type,
                            args=base_params["raw_args"],
                            kwargs=kwargs,
                            experiment_id=base_params["experiment_id"],
                            variant=base_params["variant"],
                        ) as borrowed:
                            result = await fn(*args, **kwargs)
                        try:
                            if finalize is not None:
                                output, finalize_error = await _run_finalize_async(
                                    finalize, result
                                )
                            else:
                                output, finalize_error = result, None
                        except BaseException as e:
                            borrowed.emit(None, str(e) or e.__class__.__name__)
                            raise
                        borrowed.emit(output, finalize_error)
                        _safe_send_span(
                            span_ctx,
                            **base_params,
                            result=output,
                            error=finalize_error,
                            ended_at=_get_ended_at(),
                        )
                        return result
                    except asyncio.CancelledError as e:
                        _safe_send_span(
                            span_ctx,
                            **base_params,
                            result=None,
                            error=str(e) or e.__class__.__name__,
                            ended_at=_get_ended_at(),
                        )
                        raise
                    except Exception as e:
                        _safe_send_span(
                            span_ctx,
                            **base_params,
                            result=None,
                            error=str(e),
                            ended_at=_get_ended_at(),
                        )
                        raise
                    finally:
                        _span_stack.reset(token)

                async_wrapper._bitfab_wrapped = True  # type: ignore[attr-defined]
                async_wrapper._bitfab_options = options  # type: ignore[attr-defined]
                async_wrapper._bitfab_trace_function_key = trace_function_key  # type: ignore[attr-defined]
                return async_wrapper  # type: ignore[return-value]
            else:

                @functools.wraps(fn)
                def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                    # Decided per call, never at decoration: the key can load
                    # after this wrapper is built, and a replay item records
                    # with capture off.
                    if not self._should_record():
                        return fn(*args, **kwargs)
                    if (
                        capture_when != "nested"
                        and not _on_event_loop_thread()
                        and self._awaits_first_simulation_plan_read()
                    ):
                        self._simulation_plan.wait_for_first_read()
                    setup = _safe_build_span_context(args, kwargs)
                    if setup is None:
                        # Span setup failed: run untraced so the call still works.
                        return fn(*args, **kwargs)
                    new_stack, base_params, is_root_span = setup
                    span_ctx = new_stack[-1]

                    mocked, mocked_output = _safe_check_mock_replay(
                        new_stack, base_params, is_root_span, args, kwargs
                    )
                    if mocked:
                        return mocked_output  # type: ignore[no-any-return]

                    def execute() -> T:
                        with subtree.borrowed_span(
                            monitored_code,
                            span_ctx["traceId"],
                            span_ctx["spanId"],
                            name=span_name if mirror_in_enclosing_traces else None,
                            span_type=span_type,
                            args=base_params["raw_args"],
                            kwargs=kwargs,
                            experiment_id=base_params["experiment_id"],
                            variant=base_params["variant"],
                        ) as borrowed:
                            result = fn(*args, **kwargs)
                        try:
                            if finalize is not None:
                                output, finalize_error = _run_finalize(finalize, result)
                            else:
                                output, finalize_error = result, None
                        except BaseException as e:
                            borrowed.emit(None, str(e) or e.__class__.__name__)
                            raise
                        borrowed.emit(output, finalize_error)
                        _safe_send_span(
                            span_ctx,
                            **base_params,
                            result=output,
                            error=finalize_error,
                            ended_at=_get_ended_at(),
                        )
                        return result

                    try:
                        return _run_with_span_stack(new_stack, execute)
                    except Exception as e:
                        _safe_send_span(
                            span_ctx,
                            **base_params,
                            result=None,
                            error=str(e),
                            ended_at=_get_ended_at(),
                        )
                        raise

                sync_wrapper._bitfab_wrapped = True  # type: ignore[attr-defined]
                sync_wrapper._bitfab_options = options  # type: ignore[attr-defined]
                sync_wrapper._bitfab_trace_function_key = trace_function_key  # type: ignore[attr-defined]
                return sync_wrapper  # type: ignore[return-value]

        return decorator

    def node(
        self,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        capture: bool = True,
        test_run_id: str | None = None,
        mock_on_replay: bool | None = None,
        replay_reusable: bool = False,
        finalize: Callable[[Any], Any] | None = None,
        variant: str | Callable[..., str | None] | None = None,
        experiment_id: str | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Configure a function discovered beneath :meth:`trace`.

        ``node`` mirrors the applicable :meth:`span` options, but never creates
        a span or trace on its own. Outside an active ``trace`` call the
        decorated function runs exactly as written. Inside one, the enclosing
        trace owns capture, parenting, and replay behavior for the node.
        ``node`` belongs to the opt-out surface with ``trace``; entering it
        beneath an active ``span`` raises :class:`MixedTracingError`.

        Args:
            name: Captured node name. Defaults to the function name.
            type: Captured node type. Defaults to ``"custom"``.
            capture: Whether the enclosing trace captures this node. When
                False, the function is omitted and captured descendants attach
                to its nearest captured parent.
            test_run_id: Deprecated alias for ``experiment_id``.
            mock_on_replay: ``True`` marks the node for recorded-output
                mocking, ``False`` keeps it live, and ``None`` inherits the
                enclosing trace's ``mock_on_replay_default`` policy.
            replay_reusable: Experimental output-only subtree reuse; same
                lossless JSON and no-hidden-effects contract as :meth:`span`.
            finalize: Optional callable that records a serializable view of the
                result while returning the original result to the caller.
            variant: Tells apart calls sharing this node's name, such as one
                function running several times at once on a thread pool. A
                non-empty string, or a function that receives the call's
                arguments and returns one (or ``None`` for no variant). It is
                computed before the call runs, only inside an active trace.
                Replay matches recordings by name and variant before call
                order, and calls beneath the node only match recordings beneath
                the same name and variant.
            experiment_id: Optional experiment ID included on the captured node.

        Returns:
            A decorator that leaves the function untraced unless it runs under
            an active ``trace`` call.

        Raises:
            ValueError: If recorded-output mocking is requested for an
                uncaptured node, ``variant`` is not a non-empty string, a
                callable, or ``None``, or ``experiment_id`` and ``test_run_id``
                are both passed with different values.
            MixedTracingError: If the node runs beneath an active ``span``
                with no enclosing ``trace``.
        """
        experiment_id = resolve_experiment_id(
            experiment_id, test_run_id, where="Bitfab.node"
        )
        if not capture and (mock_on_replay is True or replay_reusable):
            raise ValueError(
                "client.node(capture=False) cannot use mock_on_replay=True or replay_reusable=True "
                "because an uncaptured node has no recorded output."
            )
        if (
            variant is not None
            and not callable(variant)
            and (not isinstance(variant, str) or not variant)
        ):
            raise ValueError(
                "client.node(variant=...) must be a non-empty string or a "
                "function of the call's arguments."
            )

        span_type = type
        options = {
            "name": name,
            "type": span_type,
            "capture": capture,
            "experiment_id": experiment_id,
            "mock_on_replay": mock_on_replay,
            "replay_reusable": replay_reusable,
            "variant": variant if isinstance(variant, str) else None,
        }

        def decorator(fn: Callable[P, T]) -> Callable[P, T]:
            configured = self._subtree_node_wrapper(
                fn,
                name=name,
                span_type=span_type,
                capture=capture,
                experiment_id=experiment_id,
                mock_on_replay=mock_on_replay,
                finalize=finalize,
                without_session=fn,
                guard_without_session=True,
                replay_reusable=replay_reusable,
                variant=variant,
            )
            configured._bitfab_node = True  # type: ignore[attr-defined]
            configured._bitfab_node_options = options  # type: ignore[attr-defined]
            return configured

        return decorator

    def _current_variant_chain(self) -> VariantChain:
        stack = _span_stack.get()
        return stack[-1].get("variantChain", ()) if stack else ()

    def _integration_span(
        self,
        trace_function_key: str,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        capture_when: CaptureWhen = "always",
        mock_on_replay: bool | None = None,
        finalize: Callable[[Any], Any] | None = None,
        instrumentation: SpanInstrumentation | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        span_type = type

        def decorator(fn: Callable[P, T]) -> Callable[P, T]:
            spanned = self._span_impl(
                trace_function_key,
                name=name,
                type=span_type,
                capture_when=capture_when,
                mock_on_replay=bool(mock_on_replay),
                finalize=finalize,
                surface="opt-in",
                instrumentation=instrumentation,
            )(fn)
            configured = self._subtree_node_wrapper(
                fn,
                name=name,
                span_type=span_type,
                capture=True,
                experiment_id=None,
                mock_on_replay=mock_on_replay,
                finalize=finalize,
                without_session=spanned,
                guard_without_session=False,
                instrumentation=instrumentation,
            )
            configured._bitfab_wrapped = True  # type: ignore[attr-defined]
            configured._bitfab_options = spanned._bitfab_options  # type: ignore[attr-defined]
            configured._bitfab_trace_function_key = trace_function_key  # type: ignore[attr-defined]
            return configured

        return decorator

    def _subtree_node_wrapper(
        self,
        fn: Callable[P, T],
        *,
        name: str | None,
        span_type: SpanType,
        capture: bool,
        experiment_id: str | None,
        mock_on_replay: bool | None,
        finalize: Callable[[Any], Any] | None,
        without_session: Callable[..., Any],
        guard_without_session: bool,
        replay_reusable: bool = False,
        instrumentation: SpanInstrumentation | None = None,
        variant: str | Callable[..., str | None] | None = None,
    ) -> Callable[P, T]:
        code = getattr(fn, "__code__", None)
        node_span_name = name or _function_span_name(fn)
        is_async = inspect.iscoroutinefunction(fn)
        is_async_gen = inspect.isasyncgenfunction(fn)
        traced_by_policy: dict[tuple[str, bool], Callable[..., Any]] = {}
        traced_by_policy_lock = threading.Lock()

        def captures_node(session: subtree.Session) -> bool:
            return capture and (code is None or code.co_name not in session.exclude)

        def align_span_parent(session: subtree.Session) -> Any:
            parent_span_id = subtree.current_parent_span_id(session)
            stack = _get_span_stack()
            if parent_span_id is None or (
                stack and stack[-1]["spanId"] == parent_span_id
            ):
                return None
            executing_thread = threading.current_thread()
            parent_context: SpanContext = {
                "traceId": session.trace_id,
                "spanId": parent_span_id,
                "threadId": executing_thread.ident or 0,
                "surface": "opt-out",
            }
            variant_chain = stack[-1].get("variantChain") if stack else None
            if variant_chain:
                parent_context["variantChain"] = variant_chain
            return _span_stack.set([*stack, parent_context])

        def resolve_variant(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
            if not callable(variant):
                return _node_variant.set((fn, variant))
            try:
                with subtree.uncaptured():
                    resolved = variant(*args, **kwargs)
            except Exception as error:
                warn_once(
                    f"node-variant-raised:{node_span_name}",
                    f"the variant function for node '{node_span_name}' raised "
                    f"({_safe_type_name(error)}: {error}); those calls record no "
                    "variant. Your function still runs normally.",
                )
                return _node_variant.set(None)
            if resolved is not None and not (isinstance(resolved, str) and resolved):
                warn_once(
                    f"node-variant-invalid:{node_span_name}",
                    f"the variant function for node '{node_span_name}' returned "
                    f"{_safe_type_name(resolved)} {resolved!r}; a variant must be a "
                    "non-empty string or None, so those calls record no variant.",
                )
                return _node_variant.set(None)
            return _node_variant.set((fn, resolved))

        def guard_outside_trace() -> None:
            if guard_without_session and _enclosing_surface() == "opt-in":
                raise _mixed_tracing_error("node", "span")

        def reset_span_parent(token: Any) -> None:
            if token is not None:
                _span_stack.reset(token)

        def build_traced(session: subtree.Session) -> Callable[..., Any]:
            resolved_mock_on_replay = (
                mock_on_replay
                if mock_on_replay is not None
                else session.mock_on_replay_default
            )
            policy_key = (session.label, resolved_mock_on_replay)
            existing = traced_by_policy.get(policy_key)
            if existing is not None:
                return existing
            with traced_by_policy_lock:
                existing = traced_by_policy.get(policy_key)
                if existing is not None:
                    return existing

                traced = self._span_impl(
                    session.label,
                    name=name,
                    type=span_type,
                    capture_when="nested",
                    experiment_id=experiment_id,
                    mock_on_replay=resolved_mock_on_replay,
                    replay_reusable=replay_reusable,
                    finalize=finalize,
                    surface="opt-out",
                    mirror_in_enclosing_traces=True,
                    instrumentation=instrumentation,
                )(fn)
                traced_by_policy[policy_key] = traced
                return traced

        if is_async_gen:

            @functools.wraps(fn)
            async def async_gen_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                session = subtree.current_session()
                if session is None:
                    guard_outside_trace()
                    async for value in without_session(*args, **kwargs):
                        yield value
                    return
                if not captures_node(session):
                    with subtree.suppressed_node(code, session, all_sessions=True):
                        async for value in fn(*args, **kwargs):
                            yield value
                    return
                token = align_span_parent(session)
                variant_token = resolve_variant(args, kwargs)
                try:
                    async for value in build_traced(session)(*args, **kwargs):
                        yield value
                finally:
                    with contextlib.suppress(ValueError):
                        _node_variant.reset(variant_token)
                    reset_span_parent(token)

            return async_gen_wrapper  # type: ignore[return-value]
        if is_async:

            @functools.wraps(fn)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                session = subtree.current_session()
                if session is None:
                    guard_outside_trace()
                    return await without_session(*args, **kwargs)
                if not captures_node(session):
                    with subtree.suppressed_node(code, session, all_sessions=True):
                        return await fn(*args, **kwargs)
                token = align_span_parent(session)
                variant_token = resolve_variant(args, kwargs)
                try:
                    return await build_traced(session)(*args, **kwargs)
                finally:
                    _node_variant.reset(variant_token)
                    reset_span_parent(token)

            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(fn)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            session = subtree.current_session()
            if session is None:
                guard_outside_trace()
                return without_session(*args, **kwargs)
            if not captures_node(session):
                with subtree.suppressed_node(code, session, all_sessions=True):
                    return fn(*args, **kwargs)
            token = align_span_parent(session)
            variant_token = resolve_variant(args, kwargs)
            try:
                return build_traced(session)(*args, **kwargs)
            finally:
                _node_variant.reset(variant_token)
                reset_span_parent(token)

        return sync_wrapper

    def _emit_subtree_span(
        self,
        trace_function_key: str,
        trace_id: str,
        *,
        span_id: str,
        parent_span_id: str,
        span_name: str,
        inputs: dict[str, Any],
        result: Any,
        error: str | None,
        started_at: str,
        ended_at: str,
        function_id: str | None = None,
        function_file: str | None = None,
        function_line: int | None = None,
        nested_trace: TraceLink | None = None,
        span_type: SpanType = "function",
        experiment_id: str | None = None,
        variant: str | None = None,
        declared_node: bool = False,
    ) -> None:
        try:
            self._send_span(
                trace_function_key=trace_function_key,
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                raw_args=(),
                raw_kwargs=inputs,
                result=result,
                error=error,
                started_at=started_at,
                ended_at=ended_at,
                function_name=span_name,
                span_name=span_name,
                span_type=span_type,
                function_id=function_id,
                function_file=function_file,
                function_line=function_line,
                nested_trace=nested_trace,
                experiment_id=experiment_id,
                instrumentation="trace",
                variant=variant,
                declared_node=declared_node,
            )
        except Exception as error:
            warn_once(
                f"span-send-failed:{span_name}",
                f"span '{span_name}' was not sent ({_safe_type_name(error)}: {error}); its child spans will appear without a parent",
            )

    def trace(
        self,
        trace_function_key: str,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        mock_on_replay_default: bool = False,
        max_depth: int | None = subtree.DEFAULT_MAX_DEPTH,
        max_captured_subtree_spans: int | None = None,
        exclude: Collection[str] = (),
        include_wrappers: bool = False,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """EXPERIMENTAL. Records a root span AND a span for every first-party
        function called beneath it, at any depth, without wrapping them.

        This API is new and may change in a future release; ``span`` is the
        stable decorator.

        Example usage:
            ```python
            @client.trace("order-processing")
            def process_order(order_id: str) -> dict:
                items = load_items(order_id)  # span, not wrapped
                return summarize(items)  # span, not wrapped
            ```

        First-party means the package directory containing the decorated
        function. Standard library, site-packages, and Bitfab's own code never
        record spans. Outside a traced call nothing is captured, so untraced
        code paths are unaffected.

        ``trace`` and :meth:`node` are the opt-out tracing surface: everything
        beneath the root is recorded unless excluded. :meth:`span` is the
        opt-in surface. The two are never mixed in one call stack: a ``trace``
        root entered beneath an active ``span`` raises
        :class:`MixedTracingError`, and so does a ``span`` entered beneath a
        ``trace``. A nested ``trace`` root starts an independent trace while
        its full subtree is also recorded in each outer trace, with separate
        span IDs. Each outer trace's span for the nested root carries
        ``nested_trace_id``, ``nested_trace_function_key``, and
        ``nested_root_span_id``, and the nested root span carries
        ``enclosing_trace_id``, ``enclosing_trace_function_key``, and
        ``enclosing_span_id``, so the two traces point at each other. Inside a
        replay item or ``seed_trace`` a nested root starts no trace of its
        own: the item's trace records it as an ordinary descendant.
        Async-generator capture is released between yielded items.

        Only functions the author wrote are recorded. Lambdas and generator
        expressions are skipped (a lambda in ``map`` runs once per element, so
        recording it would turn one call into thousands of spans), as are
        decorator wrappers, which otherwise add a span per decorator between a
        caller and the function it meant to call.

        Use :meth:`node` on a discovered function that needs a custom name,
        type, finalizer, capture decision, or replay-mocking policy. The node
        configuration is consumed only by this enclosing trace and never
        creates a span by itself.

        Requires Python 3.12+ (``sys.monitoring``). On older versions the root
        span is still recorded, exactly as ``span`` would, and a one-time
        warning explains that descendants were skipped.

        Args:
            trace_function_key: Identifier grouping spans, as in ``span``.
            name: Root span name. Defaults to the function name.
            type: Root span type. Descendant spans are typed ``"function"``.
            mock_on_replay_default: Replay-mocking default for configured
                descendants. When True, configured nodes are mocked by the
                default ``mock="marked"`` strategy unless they explicitly set
                ``mock_on_replay=False``. Automatically discovered unconfigured
                descendants are not replay boundaries.
            max_depth: Stop discovering below this call depth. Unbounded by
                default. Never applies to a ``node`` or a nested ``trace``.
            max_captured_subtree_spans: Cap on discovered calls sent with
                their inputs and outputs (default 500), so a hot loop cannot
                produce an unbounded trace. It does not count declared nodes,
                nested trace roots, framework integration spans, or spans the
                loaded sim plan turned capture off for, so those keep recording
                past it. Spans sent without inputs and outputs only because the
                sim plan could not be read still count toward it. Past it,
                further discovered calls with capture on record nothing.
                Resolved from this argument, then
                ``Bitfab(max_captured_subtree_spans=...)``, then
                ``BITFAB_MAX_CAPTURED_SUBTREE_SPANS``, then 500.
            exclude: Function names never recorded as descendant spans.
            include_wrappers: Record decorator wrappers too. Off by default; a
                wrapper is identified by taking only ``*args, **kwargs``.

        Returns:
            A decorator wrapping a function to trace it and its call subtree.

        Raises:
            MixedTracingError: If the root runs beneath an active ``span``.
        """
        span_type = type
        excluded = frozenset(exclude)
        self._simulation_plan.refresh()

        def decorator(fn: Callable[P, T]) -> Callable[P, T]:
            roots = subtree.roots_for(fn)
            code = getattr(fn, "__code__", None)

            if not subtree.SUPPORTED:
                warn_once(
                    "subtree-requires-3-12",
                    "client.trace() records the call subtree only on Python 3.12+ "
                    f"(running {sys.version_info.major}.{sys.version_info.minor}); "
                    "the decorated function still records its own span.",
                )

            def build() -> subtree.Session | None:
                current = get_current_span()
                trace_id = getattr(current, "trace_id", None)
                span_id = getattr(current, "id", None)
                if not trace_id or not span_id:
                    return None

                def emit(**kwargs: Any) -> None:
                    self._emit_subtree_span(trace_function_key, trace_id, **kwargs)

                return subtree.Session(
                    trace_id=trace_id,
                    root_span_id=span_id,
                    label=trace_function_key,
                    emit=emit,
                    now=now_iso_timestamp,
                    roots=roots,
                    max_depth=max_depth,
                    max_captured_subtree_spans=self._resolve_max_captured_subtree_spans(
                        max_captured_subtree_spans
                    ),
                    content_off=functools.partial(
                        self._simulation_plan.skips_content, trace_function_key
                    ),
                    exclude=excluded,
                    include_wrappers=include_wrappers,
                    mock_on_replay_default=mock_on_replay_default,
                    root_code=code,
                    root_span_context=getattr(current, "_context", None),
                    link_pending=True,
                )

            if inspect.isasyncgenfunction(fn):

                @functools.wraps(fn)
                async def inner(*args: P.args, **kwargs: P.kwargs) -> Any:
                    session = build()
                    iterator = fn(*args, **kwargs)
                    try:
                        while True:
                            with subtree.begin(session, code, finish_on_exit=False):
                                try:
                                    item = await iterator.__anext__()
                                except StopAsyncIteration:
                                    return
                            yield item
                    finally:
                        try:
                            with subtree.begin(session, code, finish_on_exit=False):
                                await iterator.aclose()
                        finally:
                            subtree.finish(session)

            elif inspect.iscoroutinefunction(fn):

                @functools.wraps(fn)
                async def inner(*args: P.args, **kwargs: P.kwargs) -> Any:  # type: ignore[misc]
                    with subtree.begin(build(), code):
                        return await fn(*args, **kwargs)

            else:

                @functools.wraps(fn)
                def inner(*args: P.args, **kwargs: P.kwargs) -> Any:  # type: ignore[misc]
                    with subtree.begin(build(), code):
                        return fn(*args, **kwargs)

            spanned = self._span_impl(
                trace_function_key,
                name=name or _function_span_name(fn),
                type=span_type,
                surface="opt-out",
            )(inner)

            def root_span_stack() -> list[SpanContext] | None:
                stack = _get_span_stack()
                enclosing = stack[-1].get("surface") if stack else None
                if enclosing == "opt-in":
                    raise _mixed_tracing_error("trace", "span")
                if enclosing != "opt-out":
                    return stack
                if _in_replay_item() or _in_seed_scope():
                    return None
                return []

            if inspect.isasyncgenfunction(fn):

                @functools.wraps(spanned)
                async def detached(*args: P.args, **kwargs: P.kwargs) -> Any:
                    root_stack = root_span_stack()
                    if root_stack is None:
                        absorbed = fn(*args, **kwargs)
                        try:
                            async for item in absorbed:
                                yield item
                        finally:
                            await absorbed.aclose()
                        return
                    iterator = spanned(*args, **kwargs)
                    try:
                        while True:
                            token = _span_stack.set(root_stack)
                            try:
                                try:
                                    item = await iterator.__anext__()
                                except StopAsyncIteration:
                                    return
                            finally:
                                _span_stack.reset(token)
                            yield item
                    finally:
                        token = _span_stack.set(root_stack)
                        try:
                            await iterator.aclose()
                        finally:
                            _span_stack.reset(token)

            elif inspect.iscoroutinefunction(fn):

                @functools.wraps(spanned)
                async def detached(*args: P.args, **kwargs: P.kwargs) -> Any:  # type: ignore[misc]
                    root_stack = root_span_stack()
                    if root_stack is None:
                        return await fn(*args, **kwargs)
                    token = _span_stack.set(root_stack)
                    try:
                        return await spanned(*args, **kwargs)
                    finally:
                        _span_stack.reset(token)

            else:

                @functools.wraps(spanned)
                def detached(*args: P.args, **kwargs: P.kwargs) -> Any:  # type: ignore[misc]
                    root_stack = root_span_stack()
                    if root_stack is None:
                        return fn(*args, **kwargs)
                    return _run_with_span_stack(
                        root_stack, lambda: spanned(*args, **kwargs)
                    )

            return detached  # type: ignore[return-value]

        return decorator

    def wrap_baml(
        self,
        method_or_client: Any,
        method: Callable[..., Any] | None = None,
        *,
        on_collector: Callable[[Any], None] | None = None,
    ) -> Callable[..., Any]:
        """Wrap a BAML client method to auto-extract prompt and LLM metadata.

        Creates a BAML Collector, calls the method through a tracked client,
        and automatically calls ``set_prompt()`` and ``add_context()`` on the
        current span with the rendered prompt and LLM metadata.

        Must be used inside a ``@span`` context so that ``get_current_span()``
        returns a real span handle.

        Pass ``on_collector`` to receive the BAML ``Collector`` after each
        invocation (for custom metadata extraction); the returned wrapper also
        exposes the most recent call's collector as a ``.collector`` attribute.
        If ``@boundaryml`` / ``baml-py`` is not installed, ``.collector`` is
        ``None`` and ``on_collector`` is not called.

        The BAML client can be provided in the constructor or passed explicitly::

            # Option 1: baml_client in constructor
            client = Bitfab(api_key="...", baml_client=b)


            @client.span("classify", type="llm")
            async def classify(text: str):
                return await client.wrap_baml(b.ClassifyText)(text=text)


            # Option 2: pass baml_client at call site
            client = Bitfab(api_key="...")


            @client.span("classify", type="llm")
            async def classify(text: str):
                return await client.wrap_baml(b, b.ClassifyText)(text=text)

        Args:
            method_or_client: Either a BAML method (uses constructor baml_client) or the BAML client instance
            method: The BAML method when the first argument is a client

        Returns:
            An async wrapper with the same signature that auto-instruments the call

        Raises:
            ValueError: If ``baml_client`` is not available (neither in constructor nor passed)
            ValueError: If the method has no ``__name__``
        """
        if method is not None:
            baml_client = method_or_client
            actual_method = method
        else:
            baml_client = self.baml_client
            actual_method = method_or_client
            if baml_client is None:
                raise ValueError(
                    "baml_client is required for wrap_baml. "
                    "Pass it in the Bitfab constructor or as the first argument."
                )

        method_name = getattr(actual_method, "__name__", None)
        if not method_name:
            raise ValueError(
                "wrap_baml requires a named function (e.g., b.ClassifyText)."
            )

        _load_baml_collector_class()  # warm cache

        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            collector_cls = _load_baml_collector_class()
            if collector_cls is None:
                # baml-py not available: call directly, no instrumentation.
                wrapper.collector = None
                return await getattr(baml_client, method_name)(*args, **kwargs)

            collector = collector_cls("bitfab-baml-tracing")
            tracked_client = baml_client.with_options(collector=collector)
            tracked_method = getattr(tracked_client, method_name)
            result = await tracked_method(*args, **kwargs)

            wrapper.collector = collector

            try:
                prompt = _extract_prompt_from_collector(collector)
                if prompt:
                    get_current_span().set_prompt(prompt)
                metadata = _extract_context_from_collector(collector)
                if metadata:
                    get_current_span().add_context(metadata)
            except Exception:
                pass

            if on_collector is not None:
                with contextlib.suppress(Exception):
                    on_collector(collector)

            return result

        functools.update_wrapper(wrapper, actual_method)
        wrapper.collector = None
        return wrapper

    def get_trace(self, trace_id: str) -> DetachedTrace:
        """Get a detached handle to a previously-created trace.

        Returns a handle that can be used to add context, merge metadata, or
        update the sessionId on a trace from a different process or thread
        than the one that created it. The handle is not tied to async
        context propagation.

        Raises ValueError if ``trace_id`` is not a valid Bitfab trace ID. The server returns
        404 if no trace exists with that id in the org; the failure is
        logged but not raised (fire-and-forget).

        Example::

            trace = client.get_trace(trace_id)
            trace.add_context({"refund_status": "approved"})
            trace.set_metadata({"region": "us-west"})

        Args:
            trace_id: The canonical Bitfab trace ID

        Returns:
            A DetachedTrace handle
        """
        _validate_trace_id(trace_id)
        return DetachedTrace(self, trace_id)

    def get_trace_span(
        self,
        trace_id: str,
        *,
        id: str | None = None,
        name: str | None = None,
        occurrence: SpanOccurrence = "last",
    ) -> CapturedSpan | None:
        """Fetch one persisted span without loading the full trace.

        Exactly one of ``id`` or ``name`` is required. Name lookups return
        the last matching span by default; use ``"first"`` or a zero-based
        integer occurrence to select another match.
        """
        _validate_trace_id(trace_id)
        if (id is None) == (name is None):
            raise ValueError("Provide exactly one of id or name")
        if id is not None:
            _validate_span_id(id)
        if name is not None and (not isinstance(name, str) or not name):
            raise ValueError("name must be a non-empty string")
        if not (
            occurrence in ("first", "last")
            or (
                isinstance(occurrence, int)
                and not isinstance(occurrence, bool)
                and occurrence >= 0
            )
        ):
            raise ValueError(
                'occurrence must be "first", "last", or a non-negative integer'
            )

        result = self.http_client.get_trace_span(
            trace_id,
            id=id,
            name=name,
            occurrence=occurrence,
        )
        return cast(CapturedSpan | None, result)

    def get_span(self, span_id: str) -> CapturedSpan | None:
        if not isinstance(span_id, str) or not span_id.strip():
            raise ValueError("span_id must be a non-empty string")

        result = self.http_client.get_span(span_id)
        return cast(CapturedSpan | None, result)

    def get_function(self, trace_function_key: str) -> BitfabFunction:
        """Get a function wrapper for a specific trace function key.

        This provides a fluent API alternative to calling span directly,
        allowing you to bind the trace_function_key once and wrap multiple functions.

        Example usage:
            ```python
            client = Bitfab(api_key="your-api-key")

            order_func = client.get_function("order-processing")


            @order_func.span()
            def process_order(order_id: str):
                pass


            @order_func.span()
            def validate_order(order_id: str):
                pass
            ```

        Args:
            trace_function_key: A string identifier for grouping spans

        Returns:
            A BitfabFunction instance for wrapping functions
        """
        self._simulation_plan.refresh()
        return BitfabFunction(self, trace_function_key)

    def _serialize_inputs(
        self, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> list[Any]:
        """Serialize function inputs for span data."""
        serialized_args = [self._serialize_value(arg) for arg in args]
        if kwargs:
            serialized_args.append(
                {k: self._serialize_value(v) for k, v in kwargs.items()}
            )
        return serialized_args

    def _serialize_value(self, value: Any) -> Any:
        """Serialize a value for JSON storage (human-readable span input).

        Delegates to the shared ``to_json_safe`` so the recurse-the-dump logic
        lives in exactly one place (see bitfab/serialize.py)."""
        return to_json_safe(value)

    @staticmethod
    def _is_jsonpickle_safe(value: Any) -> bool:
        """Check if a value can be safely handled by jsonpickle without producing massive output."""
        import datetime as dt
        from decimal import Decimal
        from uuid import UUID

        return isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
                type(None),
                dt.datetime,
                dt.date,
                dt.time,
                UUID,
                Decimal,
                bytes,
                bytearray,
                set,
                frozenset,
            ),
        )

    def _prepare_for_serialization(self, value: Any, _depth: int = 0) -> Any:
        """Pre-process a value for jsonpickle serialization.

        Converts complex non-serializable objects (e.g. framework classes with
        network connections, runtime state) to their human-readable form so
        jsonpickle doesn't attempt to serialize massive object graphs.
        Preserves types that jsonpickle handles well (datetime, UUID, etc.).

        Depth-bounded to avoid infinite recursion on cyclic graphs (e.g. a
        dict that contains itself). Without the bound, a circular dict input
        hangs the background span thread and produces a lost-0-span trace.
        """
        if _depth > 16:
            return f"<{type(value).__qualname__}: max_depth>"
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, enum.Enum):
            return self._prepare_for_serialization(value.value, _depth + 1)
        if isinstance(value, dict):
            return {
                k: self._prepare_for_serialization(v, _depth + 1)
                for k, v in value.items()
            }
        if isinstance(value, (list, tuple)):
            items = [
                self._prepare_for_serialization(item, _depth + 1) for item in value
            ]
            return _rebuild_sequence(value, items)
        if self._is_jsonpickle_safe(value):
            return value
        if hasattr(value, "model_dump") or (
            hasattr(value, "dict") and callable(value.dict)
        ):
            return value
        # Complex objects: convert to human-readable form
        return self._serialize_value(value)

    def _send_trace_completion(
        self,
        trace_function_key: str,
        trace_id: str,
        started_at: str,
        ended_at: str,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        contexts: list[ContextEntry] | None = None,
        experiment_id: str | None = None,
        input_source_trace_id: str | None = None,
        db_snapshot_ref: DbSnapshotRef | None = None,
        db_snapshot_usage: dict[str, Any] | None = None,
        commit_ref: CommitRef | None = None,
        dropped: bool | None = None,
        ingestion_type: str | None = None,
        name: str | None = None,
        replay_attempt: int | None = None,
    ) -> None:
        """Send trace completion when a root span ends.

        Args:
            trace_function_key: The trace function key
            trace_id: The trace ID
            started_at: When the trace started
            ended_at: When the trace ended
            session_id: Optional session ID (stored in DB column)
            metadata: Optional metadata (stored in raw trace data)
            contexts: Optional context entries (stored in raw trace data)
            experiment_id: Optional experiment ID, set during replay so the server
                can backfill the trace's experimentId if the trace row was first
                created by this completion request rather than by an earlier span.
            db_snapshot_usage: How the DB branch lease was used during this
                replay item (neon_branch_id, optional snapshot_timestamp and
                original_trace_id with its deprecated source_trace_id alias,
                and the accessed flag). Only sent when a DB branch lease was
                attached; None omits the object entirely so the server can
                distinguish "no branch" from "branch ignored".
            replay_attempt: 0-based attempt index of this replay trace within its experiment, or None outside replay.
        """
        raw_trace: dict[str, Any] = {
            "id": trace_id,
            "started_at": started_at,
            "ended_at": ended_at,
        }

        if name:
            raw_trace["name"] = name
        if metadata:
            raw_trace["metadata"] = metadata
        if contexts:
            raw_trace["contexts"] = contexts
        if input_source_trace_id is not None:
            raw_trace["input_source_trace_id"] = input_source_trace_id
        if replay_attempt is not None:
            raw_trace["replay_attempt"] = replay_attempt
        if db_snapshot_ref is not None:
            raw_trace["db_snapshot_ref"] = db_snapshot_ref
        if db_snapshot_usage is not None:
            raw_trace["db_snapshot_usage"] = db_snapshot_usage
        if commit_ref is not None:
            raw_trace["commit_ref"] = commit_ref
        if ingestion_type is not None:
            raw_trace["ingestion_type"] = ingestion_type

        payload: dict[str, Any] = {
            "id": trace_id,
            "type": "sdk-function",
            "source": "python-sdk-function",
            "traceFunctionKey": trace_function_key,
            "externalTrace": raw_trace,
            "completed": True,
        }

        if session_id:
            payload["sessionId"] = session_id
        if experiment_id is not None:
            payload["experimentId"] = experiment_id
            payload["testRunId"] = experiment_id
        if dropped:
            payload["dropped"] = True

        self.http_client.send_external_trace(payload)

    def _sends_span_on_completion(self, context: SpanContext) -> bool:
        if (
            context.get("isRoot", False)
            or context.get("declaredNode", False)
            or context.get("instrumentation") in FRAMEWORK_INSTRUMENTATIONS
        ):
            return True
        return not self._simulation_plan.skips_content(
            context.get("rootTraceFunctionKey"), context.get("spanName", "")
        )

    def _nearest_captured_ancestor_span_id(
        self, stack: list[SpanContext]
    ) -> str | None:
        for context in reversed(stack):
            if self._sends_span_on_completion(context):
                return context["spanId"]
        return None

    def _span_content(
        self, raw_args: tuple[Any, ...], raw_kwargs: dict[str, Any], result: Any
    ) -> dict[str, Any]:
        content: dict[str, Any] = {
            "input": _cap_payload_size(self._serialize_inputs(raw_args, raw_kwargs)),
            "output": _cap_payload_size(self._serialize_value(result)),
        }
        prepared_args = [self._prepare_for_serialization(arg) for arg in raw_args]
        prepared_kwargs = {
            k: self._prepare_for_serialization(v) for k, v in raw_kwargs.items()
        }
        inputs_struct: dict[str, Any] = {"args": prepared_args}
        if prepared_kwargs:
            inputs_struct["kwargs"] = prepared_kwargs
        serialized_inputs = serialize_value(inputs_struct)
        serialized_output = serialize_value(self._prepare_for_serialization(result))
        if "meta" in serialized_inputs or prepared_kwargs:
            content["input_serialized"] = serialized_inputs
        if "meta" in serialized_output:
            content["output_serialized"] = serialized_output
        return content

    def _send_span(
        self,
        trace_function_key: str,
        trace_id: str,
        span_id: str,
        parent_span_id: str | None,
        raw_args: tuple[Any, ...],
        raw_kwargs: dict[str, Any],
        result: Any,
        error: str | None,
        started_at: str,
        ended_at: str,
        root_trace_function_key: str | None = None,
        function_name: str | None = None,
        span_name: str | None = None,
        span_type: SpanType = "custom",
        contexts: list[ContextEntry] | None = None,
        prompt: str | None = None,
        experiment_id: str | None = None,
        input_source_span_id: str | None = None,
        is_root_span: bool = False,
        mocked: bool = False,
        mock_target: MockTarget | None = None,
        mock_source: MockSource | None = None,
        runtime: dict[str, Any] | None = None,
        function_id: str | None = None,
        function_file: str | None = None,
        function_line: int | None = None,
        nested_trace: TraceLink | None = None,
        enclosing_trace: TraceLink | None = None,
        instrumentation: SpanInstrumentation = "span",
        variant: str | None = None,
        declared_node: bool = False,
        nearest_captured_ancestor_span_id: str | None = None,
        replay_reusable: bool = False,
        replay_json_safe: bool = False,
    ) -> None:
        """Send span data to the server.

        Args:
            experiment_id: Optional experiment ID to include in the payload.
            is_root_span: Whether this is a root span (no parent).
            mocked: True when this span was served from the original trace's
                recorded output during a replay instead of re-executing, so the
                trace view can mark it.
            mock_target: What the mock replaced ("output" for every mock today,
                since both paths short-circuit the call).
            mock_source: Where the substituted value came from: "recorded" for
                the original trace's own, "override" for a caller-supplied one.
            runtime: Where the span executed: thread_id and thread_name always,
                parent_thread_id when the parent span's thread is known, and
                submit_thread_id/submit_thread_name when the
                trace_across_threads wrapper dispatched this execution.
        """
        resolved_span_name = span_name or trace_function_key
        span_data: dict[str, Any] = {
            "name": resolved_span_name,
            "type": span_type,
        }
        if replay_reusable or replay_json_safe:
            span_data["replay_reusable"] = replay_reusable
            span_data["replay_json_safe"] = (
                replay_json_safe
                and error is None
                and json_fingerprint([list(raw_args), raw_kwargs, result]) is not None
            )
        if (
            instrumentation not in FRAMEWORK_INSTRUMENTATIONS
            and not declared_node
            and (
                self._simulation_plan.skips_content(
                    _resolve_root_trace_function_key(
                        root_trace_function_key, trace_id, trace_function_key
                    ),
                    resolved_span_name,
                )
                or (parent_span_id is not None and self._simulation_plan.unreadable())
            )
        ):
            span_data[CONTENT_OFF_KEY] = True
            prompt = None
        else:
            span_data.update(self._span_content(raw_args, raw_kwargs, result))

        if function_name is not None:
            span_data["function_name"] = function_name

        if function_id is not None:
            span_data["function_id"] = function_id
        if function_file is not None:
            span_data["function_file"] = function_file
        if function_line is not None:
            span_data["function_line"] = function_line

        if nested_trace is not None:
            span_data["nested_trace_id"] = nested_trace["trace_id"]
            span_data["nested_trace_function_key"] = nested_trace["trace_function_key"]
            if "span_id" in nested_trace:
                span_data["nested_root_span_id"] = nested_trace["span_id"]
        if enclosing_trace is not None:
            span_data["enclosing_trace_id"] = enclosing_trace["trace_id"]
            span_data["enclosing_trace_function_key"] = enclosing_trace[
                "trace_function_key"
            ]
            if "span_id" in enclosing_trace:
                span_data["enclosing_span_id"] = enclosing_trace["span_id"]

        if error is not None:
            span_data["error"] = error
            span_data["error_source"] = "code"

        if contexts is not None:
            span_data["contexts"] = contexts

        if prompt is not None:
            span_data["prompt"] = prompt

        if runtime is not None:
            span_data["runtime"] = runtime

        if variant is not None:
            span_data["variant"] = variant

        external_span: dict[str, Any] = {
            "id": span_id,
            "trace_id": trace_id,
            "started_at": started_at,
            "ended_at": ended_at,
            "span_data": span_data,
            "span_origin": make_span_origin(instrumentation),
        }
        if parent_span_id is not None:
            external_span["parent_id"] = parent_span_id
        if (
            nearest_captured_ancestor_span_id is not None
            and nearest_captured_ancestor_span_id != parent_span_id
        ):
            external_span["nearest_captured_ancestor_id"] = (
                nearest_captured_ancestor_span_id
            )
        if input_source_span_id is not None:
            external_span["input_source_span_id"] = input_source_span_id

        payload: dict[str, Any] = {
            "id": span_id,
            "traceId": trace_id,
            "type": "sdk-function",
            "source": "python-sdk-function",
            "sourceTraceId": trace_id,
            "traceFunctionKey": trace_function_key,
            "rawSpan": external_span,
        }

        if root_trace_function_key is not None:
            payload[ROOT_TRACE_FUNCTION_KEY_FIELD] = root_trace_function_key

        if declared_node:
            payload[DECLARED_IN_CODE_FIELD] = True

        if experiment_id is not None:
            payload["experimentId"] = experiment_id
            payload["testRunId"] = experiment_id

        if mocked:
            payload["mocked"] = True

        if mock_target is not None:
            payload["mockTarget"] = mock_target

        if mock_source is not None:
            payload["mockSource"] = mock_source

        # If drop() was called on this trace, suppress the span PAYLOAD upload
        # for every span that completes after the flag was set. The trace
        # completion below still rides out with dropped: true, so the server
        # scrubs any sibling spans that already raced out before the flag was
        # set. Skipping the upload here avoids shipping payloads the server
        # will only discard.
        drop_state = _active_trace_states.get(trace_id)
        trace_dropped = bool(drop_state and drop_state.get("dropped"))

        if not trace_dropped:
            self.http_client.send_external_span(payload)

        if is_root_span:
            replay_ctx = _replay_context.get()
            trace_state = _active_trace_states.get(trace_id)
            # Built AFTER the wrapped fn finished (the root span ends once the
            # fn returns), so `accessed` reflects whether customer code
            # obtained the branch URL during this item. None (omitted) when no
            # lease was attached, so the server can distinguish "no branch"
            # from "branch ignored".
            db_snapshot_usage: dict[str, Any] | None = None
            if replay_ctx is not None:
                lease = replay_ctx.get("db_branch_lease")
                if lease:
                    db_snapshot_usage = {
                        "neon_branch_id": lease.get("neonBranchId"),
                    }
                    snapshot_timestamp = lease.get("snapshotTimestamp")
                    if snapshot_timestamp:
                        db_snapshot_usage["snapshot_timestamp"] = snapshot_timestamp
                    region = lease.get("region")
                    if region:
                        db_snapshot_usage["region"] = region
                    original_trace_id = replay_ctx.get("source_bitfab_trace_id")
                    if original_trace_id:
                        db_snapshot_usage["original_trace_id"] = original_trace_id
                        # Deprecated wire alias, kept so this SDK still reports
                        # usage against servers that predate the rename.
                        db_snapshot_usage["source_trace_id"] = original_trace_id
                    db_snapshot_usage["accessed"] = (
                        replay_ctx.get("db_snapshot_accessed") is True
                    )
                    timings = replay_ctx.get("db_branch_timings")
                    if timings:
                        db_snapshot_usage["timings"] = timings
            self._send_trace_completion(
                trace_function_key=trace_function_key,
                trace_id=trace_id,
                started_at=trace_state.get("startedAt", started_at)
                if trace_state
                else started_at,
                ended_at=ended_at,
                session_id=trace_state.get("sessionId") if trace_state else None,
                name=trace_state.get("name") if trace_state else None,
                metadata=caller_trace_metadata(trace_id),
                contexts=trace_state.get("contexts") if trace_state else None,
                experiment_id=trace_state.get("experimentId") if trace_state else None,
                input_source_trace_id=trace_state.get("inputSourceTraceId")
                if trace_state
                else None,
                db_snapshot_ref=trace_state.get("dbSnapshotRef")
                if trace_state
                else None,
                db_snapshot_usage=db_snapshot_usage,
                commit_ref=current_commit_ref(),
                dropped=trace_state.get("dropped") if trace_state else None,
                ingestion_type=trace_state.get("ingestionType")
                if trace_state
                else None,
                replay_attempt=trace_state.get("replayAttempt")
                if trace_state
                else None,
            )
            _active_trace_states.pop(trace_id, None)
            retire_trace_metadata(trace_id)


class BitfabFunction:
    """Represents a Bitfab function that can wrap user functions for tracing.

    This provides a fluent API for binding a trace_function_key once and
    then wrapping multiple functions with that key.

    Example usage:
        ```python
        client = Bitfab(api_key="your-api-key")

        order_func = client.get_function("order-processing")


        @order_func.span()
        def process_order(order_id: str):
            pass


        @order_func.span()
        def validate_order(order_id: str):
            pass
        ```
    """

    def __init__(self, client: Bitfab, trace_function_key: str):
        """Initialize a BitfabFunction.

        Args:
            client: The Bitfab client instance
            trace_function_key: The trace function key for grouping spans
        """
        self._client = client
        self._trace_function_key = trace_function_key

    def span(
        self,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        capture_when: CaptureWhen = "always",
        test_run_id: str | None = None,
        mock_on_replay: bool = False,
        replay_reusable: bool = False,
        finalize: Callable[[Any], Any] | None = None,
        experiment_id: str | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Decorator to wrap a function and automatically create a span.

        Example usage:
            ```python
            order_func = client.get_function("order-processing")


            @order_func.span()
            def process_order(order_id: str):
                # ... process order
                pass


            # With explicit span name and type
            @order_func.span(name="SafetyValidator", type="guardrail")
            def check_safety(content: str):
                pass
            ```

        Args:
            name: The name of the span. Defaults to the function name if available, otherwise the trace_function_key.
            type: The type of span. Defaults to "custom". Options: llm, agent, function, guardrail, handoff, custom
            capture_when: Controls whether the span may start a new trace. See
                ``Bitfab.span`` for details.
            test_run_id: Deprecated alias for ``experiment_id``.
            mock_on_replay: When True, replay reuses this span's recorded output under the
                default ``mock="marked"`` strategy. See ``Bitfab.span`` for details.
            replay_reusable: Experimental output-only subtree reuse. See
                ``Bitfab.span`` for the lossless JSON and no-hidden-effects contract.
            finalize: Optional callable to record a serializable view of a streaming
                result as the span output. See ``Bitfab.span`` for details.
            experiment_id: Attributes the span to an experiment. See ``Bitfab.span``
                for details.

        Returns:
            A decorator that wraps functions to create spans
        """
        return self._client.span(
            self._trace_function_key,
            name=name,
            type=type,
            capture_when=capture_when,
            mock_on_replay=mock_on_replay,
            replay_reusable=replay_reusable,
            finalize=finalize,
            experiment_id=resolve_experiment_id(
                experiment_id, test_run_id, where="BitfabFunction.span"
            ),
        )

    def trace(
        self,
        *,
        name: str | None = None,
        type: SpanType = "custom",
        mock_on_replay_default: bool = False,
        max_depth: int | None = subtree.DEFAULT_MAX_DEPTH,
        max_captured_subtree_spans: int | None = None,
        exclude: Collection[str] = (),
        include_wrappers: bool = False,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Create a trace decorator bound to this function's key.

        This is equivalent to ``client.trace(key, ...)`` and supports the same
        subtree capture, node configuration, and replay behavior.

        Args:
            name: Root span name. Defaults to the decorated function name.
            type: Root span type. Descendants are typed ``"function"``.
            mock_on_replay_default: Replay-mocking default for configured nodes.
            max_depth: Maximum number of recorded descendant levels.
            max_captured_subtree_spans: Cap on discovered calls sent with
                their inputs and outputs (default 500), so a hot loop cannot
                produce an unbounded trace. It does not count declared nodes,
                nested trace roots, framework integration spans, or spans the
                loaded sim plan turned capture off for, so those keep recording
                past it. Spans sent without inputs and outputs only because the
                sim plan could not be read still count toward it. Past it,
                further discovered calls with capture on record nothing.
                Resolved from this argument, then
                ``Bitfab(max_captured_subtree_spans=...)``, then
                ``BITFAB_MAX_CAPTURED_SUBTREE_SPANS``, then 500.
            exclude: Function names never recorded as descendants.
            include_wrappers: Record decorator wrappers when True.

        Returns:
            A decorator wrapping a function as an automatically expanded trace
            root under this handle's trace function key.
        """
        return self._client.trace(
            self._trace_function_key,
            name=name,
            type=type,
            mock_on_replay_default=mock_on_replay_default,
            max_depth=max_depth,
            max_captured_subtree_spans=max_captured_subtree_spans,
            exclude=exclude,
            include_wrappers=include_wrappers,
        )

    def get_claude_agent_handler(self):
        """Get a Claude Agent SDK handler bound to this function's key.

        Equivalent to ``Bitfab.get_claude_agent_handler(key)`` but reuses the
        key bound on this handle, so an outer ``span`` root and the handler
        share one key without repeating the string. With a matching key, the
        outer span is the replayable root and every handler span nests beneath
        it.

        Use the handler inside this handle's ``span`` body so its spans capture
        the enclosing root; framework calls made with no active span record
        their own root instead.

        Example::

            pipeline = client.get_function("my-agent")


            @pipeline.span(type="agent")
            async def run_agent(prompt: str):
                handler = pipeline.get_claude_agent_handler()
                options = handler.instrument_options(ClaudeAgentOptions(...))
                ...

        Returns:
            A BitfabClaudeAgentHandler configured for this client and key
        """
        return self._client.get_claude_agent_handler(self._trace_function_key)

    def get_langgraph_callback_handler(self):
        """Get a LangGraph/LangChain callback handler bound to this key.

        Equivalent to ``Bitfab.get_langgraph_callback_handler(key)`` but reuses
        the key bound on this handle, so an outer ``span`` root and the handler
        share one key without repeating the string. With a matching key, the
        outer span is the replayable root and the LangGraph spans nest beneath
        it.

        Use the handler inside this handle's ``span`` body so its spans capture
        the enclosing root; framework calls made with no active span record
        their own root instead.

        Example::

            pipeline = client.get_function("my-pipeline")


            @pipeline.span(type="agent")
            def run_agent(query: str):
                handler = pipeline.get_langgraph_callback_handler()
                return agent.invoke(
                    {"messages": [...]}, config={"callbacks": [handler]}
                )

        Returns:
            A BitfabLangGraphCallbackHandler configured for this client and key
        """
        return self._client.get_langgraph_callback_handler(self._trace_function_key)

    def get_langchain_callback_handler(self):
        """Get a LangChain callback handler bound to this key.

        Alias of :meth:`get_langgraph_callback_handler`. LangChain chains and
        LangGraph graphs share the same callback system, so one bound handler
        serves both.

        Returns:
            A BitfabLangGraphCallbackHandler configured for this client and key
        """
        return self._client.get_langchain_callback_handler(self._trace_function_key)

    def get_langgraph_integration(
        self,
        *,
        mock_tools_on_replay: bool | list[str] | tuple[str, ...] = True,
    ) -> BitfabLangGraphIntegration:
        """Get the experimental LangGraph integration bound to this key.

        This API may change before it is stable.
        """
        return self._client.get_langgraph_integration(
            self._trace_function_key,
            mock_tools_on_replay=mock_tools_on_replay,
        )

    def wrap_baml(
        self,
        method_or_client: Any,
        method: Callable[..., Any] | None = None,
    ) -> Callable[..., Any]:
        """Wrap a BAML client method to auto-extract prompt and LLM metadata.

        Delegates to ``Bitfab.wrap_baml``. See that method for details.

        Unlike the other methods on this handle, ``wrap_baml`` does NOT use the
        bound key: it opens no span of its own. It enriches the *current* span
        (via ``get_current_span().set_prompt()`` / ``add_context()``), so call
        it inside a function wrapped by this handle's ``span`` decorator -- the
        bound key keys that wrapper, and the BAML prompt/metadata attach to it.

        Args:
            method_or_client: Either a BAML method (uses constructor baml_client) or the BAML client instance
            method: The BAML method when the first argument is a client

        Returns:
            An async wrapper with the same signature that auto-instruments the call
        """
        return self._client.wrap_baml(method_or_client, method)
