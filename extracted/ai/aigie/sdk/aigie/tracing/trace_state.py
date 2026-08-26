"""Unified trace state: ambient (per-call) + registry (cross-call).

ONE module exposing several API surfaces because they answer the same question
("what trace am I in?") at different timescales and for different consumers:

- Surface A (Ambient): within a single run. Per-asyncio-task ContextVar.
  Replaces the old SpanContext concept and absorbs the role of the previous
  ``_callback_context`` thread-local guard via ``is_inside_traced_run()``.

- Surface B (Registry): across runs. Module-level dict + lock. Maps a
  framework's resume_key (e.g. LangGraph thread_id) to the trace object so
  call N+1 can reuse the trace opened in call N (interrupt/resume).

- Surface B2 / C (Registries): traces whose root has already closed, and
  in-flight spans registered with a finalize callable so an unclean shutdown
  still ships them as interrupted.

- Surface D (Provider-span claim): which threads have an integration that
  already emits the ``llm`` span for any provider call made there. Thread-keyed
  because the frameworks that need it (Pipecat) run on tasks Surface A cannot
  reach. Read only by the bare provider patch's suppression predicate.

Cross-task isolation comes free from ContextVar semantics: asyncio.gather
fans out via ``copy_context()`` so each task gets its own span_stack copy.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Callable
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import Any

from aigie.tracing.types import SpanStatus

# ─── Surface A: Ambient state (per-call, per-task) ──────────────────────


@dataclass
class _AmbientState:
    trace_id: str
    span_stack: list[str] = field(default_factory=list)


_ambient: ContextVar[_AmbientState | None] = ContextVar("_aigie_trace_state_ambient", default=None)


def open_ambient(*, trace_id: str) -> Token:
    """Begin a traced run. Returns a token to pass to ``close_ambient()``."""
    return _ambient.set(_AmbientState(trace_id=trace_id))


def close_ambient(token: Token) -> None:
    """End a traced run; restore the previous (possibly None) ambient state."""
    _ambient.reset(token)


def push_span(span_id: str) -> None:
    """Mark ``span_id`` as the current parent for nested span creation.

    Creates a fresh state object and installs it via ``_ambient.set(...)`` so
    parallel tasks (asyncio.gather, threadpool with copy_context) each get
    their own copy. Mutating the existing state in place would alias across
    tasks — the dataclass and its list are shared by reference until ``set``.
    """
    state = _ambient.get()
    if state is None:
        raise RuntimeError("No active ambient trace_state; call open_ambient(trace_id=...) first")
    _ambient.set(_AmbientState(trace_id=state.trace_id, span_stack=state.span_stack + [span_id]))


def pop_span() -> str | None:
    """Pop the deepest span. Safe no-op if no ambient state or empty stack."""
    state = _ambient.get()
    if state is None or not state.span_stack:
        return None
    popped = state.span_stack[-1]
    _ambient.set(_AmbientState(trace_id=state.trace_id, span_stack=state.span_stack[:-1]))
    return popped


def current_trace_id() -> str | None:
    state = _ambient.get()
    return state.trace_id if state else None


def current_parent_span_id() -> str | None:
    state = _ambient.get()
    if state is None or not state.span_stack:
        return None
    return state.span_stack[-1]


def is_inside_traced_run() -> bool:
    """True when this thread/task is inside a traced run.

    Checks the ambient ContextVar first (per-task isolation via copy_context).
    Falls back to the thread-keyed counter — populated by
    ``_inc_thread_counter`` / ``_dec_thread_counter`` — for code paths where
    ContextVar didn't propagate (e.g. legacy LangChain dispatching callbacks
    from raw threads spawned without copy_context)."""
    if _ambient.get() is not None:
        return True
    return _thread_counter.get(threading.get_ident(), 0) > 0


# Thread-keyed fallback for "am I tracing?" when ContextVar doesn't propagate.
# Populated via the _inc/_dec helpers below; consulted by is_inside_traced_run.
_thread_counter: dict[int, int] = {}
_thread_counter_lock = threading.Lock()


def _counter_inc(counter: dict[int, int], lock: threading.Lock) -> None:
    """Add one to this thread's entry in a thread-keyed reentrancy counter."""
    tid = threading.get_ident()
    with lock:
        counter[tid] = counter.get(tid, 0) + 1


def _counter_dec(counter: dict[int, int], lock: threading.Lock) -> None:
    """Remove one, flooring at zero and dropping the key so the dict stays bounded."""
    tid = threading.get_ident()
    with lock:
        remaining = max(0, counter.get(tid, 0) - 1)
        if remaining:
            counter[tid] = remaining
        else:
            counter.pop(tid, None)


def _counter_active(counter: dict[int, int], lock: threading.Lock) -> bool:
    """True when this thread holds at least one entry."""
    with lock:
        return counter.get(threading.get_ident(), 0) > 0


def _inc_thread_counter() -> None:
    _counter_inc(_thread_counter, _thread_counter_lock)


def _dec_thread_counter() -> None:
    _counter_dec(_thread_counter, _thread_counter_lock)


# ─── Surface B: Cross-call registry ─────────────────────────────────────


_resume_registry: dict[str, Any] = {}
_resume_registry_lock = threading.Lock()


def register_resumable_trace(resume_key: str | None, trace: Any) -> None:
    """Persist a trace under ``resume_key`` so a future call can resume it."""
    if not resume_key or trace is None:
        return
    with _resume_registry_lock:
        _resume_registry[resume_key] = trace


def get_resumed_trace(resume_key: str | None) -> Any | None:
    """Return a previously-registered trace, or None."""
    if not resume_key:
        return None
    with _resume_registry_lock:
        return _resume_registry.get(resume_key)


def pop_resumable_trace(resume_key: str | None) -> Any | None:
    """Remove and return the trace for ``resume_key`` (call on graph done)."""
    if not resume_key:
        return None
    with _resume_registry_lock:
        return _resume_registry.pop(resume_key, None)


# ─── Surface B2: Traces whose root has closed ────────────────────────────
#
# The root span is stamped ``span_id == trace_id``, so a later call that
# adopts a finished trace and opens its own workflow root writes over that
# same row — replacing the run's name and output with its own. Recording the
# close lets a boundary decline to open a second root for a trace that
# already had one. Bounded: a long-lived process would otherwise accumulate
# one entry per trace forever.

_ROOT_CLOSED_MAX = 4096
_root_closed: OrderedDict[str, None] = OrderedDict()
_root_closed_lock = threading.Lock()


def mark_root_closed(trace_id: str | None) -> None:
    """Record that ``trace_id``'s workflow root has been closed."""
    if not trace_id:
        return
    with _root_closed_lock:
        _root_closed[trace_id] = None
        _root_closed.move_to_end(trace_id)
        while len(_root_closed) > _ROOT_CLOSED_MAX:
            _root_closed.popitem(last=False)


def root_already_closed(trace_id: str | None) -> bool:
    """True when this trace already had its root closed."""
    if not trace_id:
        return False
    with _root_closed_lock:
        return trace_id in _root_closed


# ─── Surface C: Open-span registry (shutdown-only orphan finalizer) ──────
#
# A span that is built mutably in memory but not yet emitted registers a
# *finalize callable* here. On clean close the emitter deregisters it; on an
# unclean shutdown ``drain_open_spans_as_interrupted`` invokes the survivors
# so their roots still ship (status="interrupted"). Storing a callable rather
# than a payload keeps this registry emitter-agnostic — each emitter shapes
# its own finalized dict.

_OpenSpanFinalize = Callable[[], "dict[str, Any] | None"]
_open_spans: dict[str, _OpenSpanFinalize] = {}
_open_spans_lock = threading.Lock()


def register_open_span(span_id: str, finalize: _OpenSpanFinalize) -> None:
    """Register an in-flight span's finalize callable (idempotent per span_id)."""
    if not span_id or finalize is None:
        return
    with _open_spans_lock:
        _open_spans[span_id] = finalize


def deregister_open_span(span_id: str) -> None:
    """Drop a span once it has been emitted normally. Safe no-op if absent."""
    if not span_id:
        return
    with _open_spans_lock:
        _open_spans.pop(span_id, None)


def drain_open_spans_as_interrupted() -> list[dict[str, Any]]:
    """Pop every open span and finalize it as interrupted.

    Invokes each registered finalize callable and stamps
    ``status="interrupted"`` on the resulting payload. A second drain is a
    no-op (the registry is emptied atomically). Callables returning ``None``
    (already finalized concurrently) are skipped.
    """
    with _open_spans_lock:
        finalizers = list(_open_spans.values())
        _open_spans.clear()

    payloads: list[dict[str, Any]] = []
    for finalize in finalizers:
        payload = finalize()
        if payload is None:
            continue
        payload["status"] = SpanStatus.INTERRUPTED.value
        payloads.append(payload)
    return payloads


# ─── Surface D: Provider-span ownership (thread-keyed) ───────────────────
#
# An integration whose framework drives its pipeline from several
# independently-created asyncio tasks on one event loop (Pipecat) cannot rely
# on Surface A to suppress the bare LLM-provider patch: the ambient state is
# opened in the task that observed the conversation start, and every task
# asyncio creates gets its own ``copy_context()``, so the task the framework's
# LLM service runs in sees no ambient trace at all. The provider patch would
# then open a whole second trace for a call the integration is already
# emitting a priceable ``llm`` span for.
#
# Keyed by thread rather than process-global so the claim reaches the sibling
# tasks of one event loop (they share a thread) and nothing else: a provider
# call issued from another thread — another framework's run, or a worker pool —
# is left untouched. Deliberately consulted ONLY by the provider patch's
# suppression predicate; it must not gate whether a run opens its own root.

_provider_span_claims: dict[int, int] = {}
_provider_span_claims_lock = threading.Lock()


def claim_provider_spans() -> None:
    """Declare that this thread's integration owns ``llm`` spans for its runs."""
    _counter_inc(_provider_span_claims, _provider_span_claims_lock)


def release_provider_spans() -> None:
    """Drop one claim made by ``claim_provider_spans`` (idempotent at zero)."""
    _counter_dec(_provider_span_claims, _provider_span_claims_lock)


def provider_spans_claimed() -> bool:
    """True when an integration on this thread already emits the ``llm`` spans."""
    return _counter_active(_provider_span_claims, _provider_span_claims_lock)
