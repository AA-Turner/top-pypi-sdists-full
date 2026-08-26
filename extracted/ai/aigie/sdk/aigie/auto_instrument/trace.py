"""
Automatic trace creation for workflows.

Provides utilities to automatically create traces when workflows start,
without requiring manual trace creation.
"""

import asyncio
import contextlib
import logging
import threading
from contextvars import ContextVar
from typing import Any

# Re-export shims preserving legacy import paths used by sdk/aigie/callback.py
# and tests. Canonical implementations live in sdk/aigie/tracing/trace_state.py.
from aigie.tracing.retention import is_retention_suppressed
from aigie.tracing.trace_state import (
    _dec_thread_counter,
    _inc_thread_counter,
    is_inside_traced_run,
    provider_spans_claimed,
)
from aigie.tracing.trace_state import (
    _thread_counter as _callback_counts,  # noqa: F401
)
from aigie.tracing.trace_state import (
    _thread_counter_lock as _callback_lock,  # noqa: F401
)
from aigie.tracing.trace_state import (
    get_resumed_trace as get_thread_trace,  # noqa: F401
)
from aigie.tracing.trace_state import (
    pop_resumable_trace as pop_thread_trace,  # noqa: F401
)
from aigie.tracing.trace_state import (
    register_resumable_trace as register_thread_trace,  # noqa: F401
)

logger = logging.getLogger(__name__)


def is_in_callback_context() -> bool:
    """The bare LLM-provider patch's suppression predicate: is this call already
    being traced by an integration that emits its own ``llm`` span?

    Consumed only by the provider patches in ``auto_instrument.llm`` — every
    other caller asks ``is_inside_traced_run()`` directly. Kept under the legacy
    name because that is where the question is asked from.

    ``is_inside_traced_run`` answers it for integrations whose run state reaches
    the provider call (a ContextVar, or the thread counter when a callback fires
    from a raw thread). ``provider_spans_claimed`` covers the ones where it
    cannot: Pipecat hands each observer its own asyncio task, so the ambient
    trace opened there is invisible in the task its LLM service runs in, and the
    patch would otherwise open a second trace for a call already priced from
    Pipecat's own usage metrics.
    """
    return is_inside_traced_run() or provider_spans_claimed()


# Context variable to track current trace
_current_trace: ContextVar[Any | None] = ContextVar("_current_trace", default=None)

# Thread-safe counter for callback context.
# Uses a threading lock + counter instead of ContextVar because LangGraph
# dispatches node functions to thread pool workers, and ContextVar does NOT
# Thread-keyed callback context counter. Keyed by thread ID so concurrent
# agents in different threads don't see each other's callback state.
# Uses a counter (not boolean) to handle nested callbacks within one thread.
# Callback-context state moved to sdk/aigie/integrations/langgraph/_callback_context.py.
# Re-exported here (including the private state dict + lock) for backwards
# compatibility with tests that touched the internals.

# Context variable to prevent re-entry across LLM instrumentation layers
_in_llm_instrumentation: ContextVar[bool] = ContextVar("_in_llm_instrumentation", default=False)

# Ambient parent span id. Propagates via copy_context() into worker threads
# (e.g. Strands' agents-as-tools pattern, which runs the inner Agent in a
# ThreadPoolExecutor). Thread-local is kept below as a same-thread fallback.
_current_parent_span_id_var: ContextVar[str | None] = ContextVar(
    "_current_parent_span_id", default=None
)

# Thread-local trace_id for propagation into tool-spawned agents running in the same OS thread
# (e.g. strands_tools.think creates Agents internally without invocation_state or ContextVar)
_trace_thread_local = threading.local()

# Legacy symbols retained for tests that reach into the old internal state.
# Nothing writes to these now — Surface B holds the canonical state — but
# they exist as empty containers so imports don't break.
_thread_traces: dict[str, Any] = {}
_thread_traces_lock = threading.Lock()


# LangGraph thread_id -> AigieCallbackHandler. Enables resume after interrupt
# to reuse the first stream's handler rather than creating a fresh one.
# LangGraph's Pregel stores the first-stream config internally and dispatches
# node-level callbacks via it; a second handler added only to the new config
# never receives node-level on_chain_start events. The fix: reuse the handler
# that is already registered in the Pregel's stored config.
_thread_handlers: dict[str, Any] = {}
_thread_handlers_lock = threading.Lock()


def get_thread_handler(thread_id: str | None) -> Any | None:
    """Return the handler associated with a LangGraph thread_id, if any."""
    if not thread_id:
        return None
    with _thread_handlers_lock:
        return _thread_handlers.get(thread_id)


def register_thread_handler(thread_id: str | None, handler: Any) -> None:
    """Associate a handler with a LangGraph thread_id."""
    if not thread_id or handler is None:
        return
    with _thread_handlers_lock:
        _thread_handlers[thread_id] = handler


def pop_thread_handler(thread_id: str | None) -> Any | None:
    """Remove and return the handler for thread_id (call on graph completion)."""
    if not thread_id:
        return None
    with _thread_handlers_lock:
        return _thread_handlers.pop(thread_id, None)


async def get_or_create_trace(
    name: str, metadata: dict[str, Any] | None = None, tags: list | None = None
) -> Any:
    """
    Get current trace or create a new one if none exists.

    This is used by auto-instrumentation to ensure traces exist
    without requiring manual creation.

    Args:
        name: Trace name
        metadata: Optional metadata
        tags: Optional tags

    Returns:
        TraceContext instance
    """
    from aigie.client import get_aigie

    if is_retention_suppressed():
        return None

    current = _current_trace.get()
    if current:
        return current

    # Get global aigie instance
    aigie = get_aigie()
    if not aigie or not aigie._initialized:
        # No aigie instance, return None (instrumentation will skip)
        return None

    # Create new trace
    try:
        trace = aigie.trace(name=name, metadata=metadata or {}, tags=tags or [])

        # Enter the trace context (it's an async context manager)
        trace_context = await trace.__aenter__()

        # Store in context variable
        _current_trace.set(trace_context)

        return trace_context
    except Exception as e:
        logger.warning(f"Failed to create auto-trace: {e}")
        return None


def get_current_trace() -> Any | None:
    """Get the current trace from context."""
    return _current_trace.get()


def set_current_trace(trace: Any | None) -> None:
    """Set the current trace in context."""
    _current_trace.set(trace)

    # Also set process-level trace ID for OTel bridge (thread pool workers
    # where ContextVars don't propagate, e.g., LangGraph nodes)
    # OTel bridge is optional — best-effort propagation.
    with contextlib.suppress(Exception):
        import importlib

        bridge = importlib.import_module("aigie.auto_instrument.span_enricher")
        bridge.set_active_trace_id(getattr(trace, "id", None) if trace else None)


def clear_current_trace() -> None:
    """Clear the current trace from context (ContextVar + thread-local)."""
    _current_trace.set(None)
    _trace_thread_local.trace_id = None
    _trace_thread_local.parent_span_id = None
    _current_parent_span_id_var.set(None)


def get_thread_local_trace_id() -> str | None:
    """Get the trace_id stored in thread-local (for tool-spawned agents)."""
    return getattr(_trace_thread_local, "trace_id", None)


def set_thread_local_trace_id(trace_id: str | None) -> None:
    """Set the trace_id in thread-local storage."""
    _trace_thread_local.trace_id = trace_id


def get_thread_local_parent_span_id() -> str | None:
    """Get the ambient parent span_id.

    Reads the ContextVar first (propagates across ``contextvars.copy_context()``
    into worker threads — Strands runs Agent.__call__ in a ThreadPoolExecutor)
    and falls back to thread-local for same-thread scenarios.

    Used so that an Agent invoked synchronously inside a tool body (the
    "agents-as-tools" pattern) can attach its agent span to the enclosing
    tool span across handler instances.
    """
    val = _current_parent_span_id_var.get()
    if val:
        return val
    return getattr(_trace_thread_local, "parent_span_id", None)


def set_thread_local_parent_span_id(span_id: str | None) -> None:
    """Set the ambient parent span_id in both ContextVar and thread-local."""
    _current_parent_span_id_var.set(span_id)
    _trace_thread_local.parent_span_id = span_id


def push_thread_local_parent_span_id(span_id: str | None) -> str | None:
    """Publish a new ambient parent span_id, returning the previous value.

    Callers are responsible for restoring the previous value (typically in
    _on_after_tool_call) by passing it back to ``set_thread_local_parent_span_id``.
    """
    prev = _current_parent_span_id_var.get() or getattr(_trace_thread_local, "parent_span_id", None)
    _current_parent_span_id_var.set(span_id)
    _trace_thread_local.parent_span_id = span_id
    return prev


def set_callback_context(active: bool) -> None:
    """Legacy thread-counter API. Delegates to trace_state."""
    if active:
        _inc_thread_counter()
    else:
        _dec_thread_counter()


def is_in_llm_instrumentation() -> bool:
    """Check if we're already inside an LLM instrumentation wrapper (prevents recursion across layers)."""
    return _in_llm_instrumentation.get()


def set_llm_instrumentation(active: bool) -> None:
    """Set whether we're inside an LLM instrumentation wrapper."""
    _in_llm_instrumentation.set(active)


def _build_trace_start_payload(trace: Any) -> dict[str, Any]:
    """Build the trace_create payload from a Trace object."""
    enriched_metadata = dict(trace.metadata)
    user_id = enriched_metadata.get("user_id") or enriched_metadata.get("userId")
    session_id = enriched_metadata.get("session_id") or enriched_metadata.get("sessionId")
    environment = enriched_metadata.get("environment") or enriched_metadata.get("env", "default")
    payload: dict[str, Any] = {
        "id": trace.id,
        "name": trace.name,
        "status": "running",
        "metadata": enriched_metadata,
        "tags": trace.tags,
        "spans": [],
    }
    start_time = getattr(trace, "start_time", None)
    if start_time is not None:
        payload["start_time"] = start_time.isoformat()
    if user_id:
        payload["user_id"] = user_id
    if session_id:
        payload["session_id"] = session_id
    if environment:
        payload["environment"] = environment
    return payload


async def _send_trace_start(trace: Any) -> None:
    """Register the trace as an open root span (record-only).

    Trace identity rides the root span (root.id == trace_id) emitted once at
    completion — no trace-create event. Registering the trace's finalize
    callable means an unclean shutdown still ships the root (interrupted).
    (The prior dispatch did a malformed ``buffer.add`` that always failed.)"""
    try:
        from aigie.tracing.trace_state import register_open_span

        finalize = getattr(trace, "_build_interrupted_root_payload", None)
        if finalize is not None and getattr(trace, "id", None):
            register_open_span(trace.id, finalize)
    except Exception as e:
        logger.debug(f"Error in _send_trace_start: {e}")


def _init_trace_in_running_loop(
    aigie: Any,
    loop: asyncio.AbstractEventLoop,
    name: str,
    metadata: dict[str, Any] | None,
    tags: list | None,
) -> Any:
    """Build a trace, set it as current, and fire-and-forget the create event."""
    from uuid import uuid4

    trace = aigie.trace(name=name, metadata=metadata or {}, tags=tags or [])
    if not trace.id:
        trace.id = str(uuid4())
    _current_trace.set(trace)
    loop.create_task(_send_trace_start(trace))
    return trace


def get_or_create_trace_sync(
    name: str, metadata: dict[str, Any] | None = None, tags: list | None = None
) -> Any:
    """Synchronous version of get_or_create_trace.

    Reuses the running event loop if one exists (fire-and-forget the trace
    start), otherwise schedules via the safe utility. Returns None if Aigie
    isn't initialized or zero-retention is active.
    """
    from aigie.client import get_aigie

    if is_retention_suppressed():
        return None

    current = _current_trace.get()
    if current:
        return current
    aigie = get_aigie()
    if not aigie or not aigie._initialized:
        return None

    try:
        loop: asyncio.AbstractEventLoop | None = None
        with contextlib.suppress(RuntimeError):
            loop = asyncio.get_running_loop()
        if loop:
            return _init_trace_in_running_loop(aigie, loop, name, metadata, tags)
        from aigie.utils.safe import schedule_async

        return schedule_async(get_or_create_trace(name, metadata, tags))
    except Exception as e:
        logger.warning(f"Failed to create sync trace: {e}")
        return None
