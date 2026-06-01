"""Unified trace state: ambient (per-call) + registry (cross-call).

ONE module exposing two API surfaces because they answer the same question
("what trace am I in?") at different timescales:

- Surface A (Ambient): within a single run. Per-asyncio-task ContextVar.
  Replaces the old SpanContext concept and absorbs the role of the previous
  ``_callback_context`` thread-local guard via ``is_inside_traced_run()``.

- Surface B (Registry): across runs. Module-level dict + lock. Maps a
  framework's resume_key (e.g. LangGraph thread_id) to the trace object so
  call N+1 can reuse the trace opened in call N (interrupt/resume).

Cross-task isolation comes free from ContextVar semantics: asyncio.gather
fans out via ``copy_context()`` so each task gets its own span_stack copy.
"""

from __future__ import annotations

import threading
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import Any

# ─── Surface A: Ambient state (per-call, per-task) ──────────────────────


@dataclass
class _AmbientState:
    trace_id: str
    span_stack: list[str] = field(default_factory=list)


_ambient: ContextVar[_AmbientState | None] = ContextVar(
    "_aigie_trace_state_ambient", default=None
)


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
        raise RuntimeError(
            "No active ambient trace_state; call open_ambient(trace_id=...) first"
        )
    _ambient.set(
        _AmbientState(trace_id=state.trace_id, span_stack=state.span_stack + [span_id])
    )


def pop_span() -> str | None:
    """Pop the deepest span. Safe no-op if no ambient state or empty stack."""
    state = _ambient.get()
    if state is None or not state.span_stack:
        return None
    popped = state.span_stack[-1]
    _ambient.set(
        _AmbientState(trace_id=state.trace_id, span_stack=state.span_stack[:-1])
    )
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


def _inc_thread_counter() -> None:
    tid = threading.get_ident()
    with _thread_counter_lock:
        _thread_counter[tid] = _thread_counter.get(tid, 0) + 1


def _dec_thread_counter() -> None:
    tid = threading.get_ident()
    with _thread_counter_lock:
        cur = _thread_counter.get(tid, 0)
        new = max(0, cur - 1)
        if new == 0:
            _thread_counter.pop(tid, None)
        else:
            _thread_counter[tid] = new


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
