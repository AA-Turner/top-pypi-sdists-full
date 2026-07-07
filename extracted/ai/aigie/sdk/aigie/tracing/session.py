"""Group several sequential top-level agent calls into ONE trace.

Without a session, each top-level call (e.g. ``agent()`` then
``agent.structured_output()``) opens and finalizes its own trace, so one logical
run surfaces as several disconnected traces. ``trace_session`` opens one trace +
one :class:`WorkflowRoot`; framework handlers reach the root via
``current_workflow_root()`` to nest their spans under it and feed it input/output.
Framework-neutral: any integration passes its ``SpanEventHandler``.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager, suppress
from contextvars import ContextVar
from typing import TYPE_CHECKING

from aigie.tracing.trace_state import (
    close_ambient,
    current_trace_id,
    is_inside_traced_run,
    open_ambient,
)
from aigie.tracing.workflow_root import WorkflowRoot

if TYPE_CHECKING:
    from aigie.tracing.span_event_handler import SpanEventHandler

_workflow_root: ContextVar[WorkflowRoot | None] = ContextVar("_aigie_workflow_root", default=None)


def current_workflow_root() -> WorkflowRoot | None:
    """The session's root span, or None when not inside a ``trace_session``."""
    return _workflow_root.get()


@contextmanager
def trace_session(
    spans: SpanEventHandler | None, *, name: str, framework: str
) -> Iterator[str | None]:
    # Nested / already tracing → reuse the active trace; open nothing.
    if spans is None or _workflow_root.get() is not None or is_inside_traced_run():
        yield current_trace_id()
        return
    # In-function import breaks the tracing → auto_instrument → client cycle.
    from aigie.auto_instrument.trace import get_or_create_trace_sync

    trace = get_or_create_trace_sync(
        name=name, metadata={"framework": framework, "type": framework}
    )
    if trace is None:  # not initialized / zero-retention
        yield None
        return

    trace_id = str(trace.id)
    token = open_ambient(trace_id=trace_id)
    root = WorkflowRoot(spans, name, trace_id=trace_id, framework=framework)
    root_token = _workflow_root.set(root)
    try:
        yield trace_id
    finally:
        root.close()
        _workflow_root.reset(root_token)
        with suppress(ValueError, LookupError):
            close_ambient(token)
