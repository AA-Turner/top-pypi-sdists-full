"""Backwards-compat shim. Canonical implementation now lives in
``sdk/aigie/tracing/trace_state.py`` (Surface A: ``is_inside_traced_run``).

The old ``set_callback_context(True/False)`` API was a thread-keyed counter
used to detect "am I inside a traced run?" — that question is now answered
by the ambient ContextVar state in ``trace_state``. The set_/is_in_ pair is
kept as no-ops + ambient delegation for external callers on the old import
path.
"""

from __future__ import annotations

from aigie.tracing.trace_state import (
    _dec_thread_counter,
    _inc_thread_counter,
    is_inside_traced_run,
)


def set_callback_context(active: bool) -> None:
    """Maintains the legacy thread-keyed counter. ``is_inside_traced_run`` in
    ``trace_state`` is the canonical "am I tracing?" check — it consults the
    ambient ContextVar first and falls back to this counter."""
    if active:
        _inc_thread_counter()
    else:
        _dec_thread_counter()


def is_in_callback_context() -> bool:
    return is_inside_traced_run()
