"""Cooperative drain support.

Draining asks a running graph to stop at the next superstep boundary, save its
checkpoint, and raise ``GraphDrained`` so the run can be re-queued and resumed
by another worker. The support (``RunControl`` / ``GraphDrained``) arrived in
langgraph 1.2; the server also supports older langgraph, so the imports are
guarded and the placeholders below never match or instantiate anything.
"""

from __future__ import annotations

import contextvars
import threading
from typing import Any

# The control of the run whose top-level graph this context is executing. The
# server sets it before streaming the graph; asyncio tasks and LangGraph's node
# executors copy it, while threads a node starts itself don't.
_TOP_LEVEL_CONTROL: contextvars.ContextVar[Any] = contextvars.ContextVar(
    "langgraph_api_top_level_run_control", default=None
)


def _in_graph_node() -> bool:
    """Whether the caller runs inside a graph node (and so in any subgraph loop).

    LangGraph runs node code under a runnable config context whose
    checkpoint_ns names the node; the run's top-level loop has no such context.
    """
    try:
        from langgraph.config import get_config  # noqa: PLC0415

        config = get_config()
    except RuntimeError:
        return False
    return bool((config.get("configurable") or {}).get("checkpoint_ns"))


try:
    from langgraph.errors import GraphDrained
    from langgraph.runtime import RunControl

    class ServerRunControl(RunControl):
        """A RunControl whose drain request only the run's top-level graph sees.

        LangGraph hands a run's control to its subgraphs. A drain inside a
        subgraph would, with durability="exit", lose the subgraph's progress.
        The request is visible only where this is provably the run's top-level
        loop: in a context the server marked for this control (see
        mark_top_level) and outside any graph node. So the run drains only at
        a top-level step boundary, after that step's subgraphs have finished,
        and never before its first step.
        Graph code inside a node, and threads a node starts, see no drain
        (drain_requested False, drain_reason None).
        """

        __slots__ = ("_first_check_done",)

        def __init__(self) -> None:
            super().__init__()
            self._first_check_done = False

        def _visible(self) -> bool:
            return _TOP_LEVEL_CONTROL.get() is self and not _in_graph_node()

        @property
        def drain_requested(self) -> bool:
            if not self._visible():
                return False
            # LangGraph checks once per top-level step boundary, before the
            # step. Only a server drain can be pending at the first check. A
            # run started with a Command has no checkpoint of its own until its
            # first step ends, so if it drained there, its next claim would
            # re-send the Command and LangGraph would apply it again. So a run
            # always completes a step before it drains.
            if not self._first_check_done:
                self._first_check_done = True
                return False
            return RunControl.drain_requested.fget(self)

        @property
        def drain_reason(self) -> str | None:
            return RunControl.drain_reason.fget(self) if self._visible() else None

    DRAIN_SUPPORT = True
except ImportError:

    class GraphDrained(Exception):
        """Placeholder that is never raised or matched on langgraph < 1.2."""

        reason: str | None = None

    class RunControl:
        """Placeholder; new_run_control() never creates one on langgraph < 1.2."""

    class ServerRunControl(RunControl):
        """Placeholder; new_run_control() never creates one on langgraph < 1.2."""

    DRAIN_SUPPORT = False

# Reason the server passes to request_drain() when its pod is shutting down.
# Graph code can pass any reason (request_drain() defaults to "shutdown"), so
# this distinct value is what tells server drains from graph drains in logs.
SERVER_SHUTDOWN_DRAIN_REASON = "server_shutdown"


def mark_top_level(control: ServerRunControl | None) -> None:
    """Mark the current context as running ``control``'s top-level graph."""
    _TOP_LEVEL_CONTROL.set(control)


def new_run_control() -> ServerRunControl | None:
    """Return a fresh control for a run, or None without drain support."""
    if DRAIN_SUPPORT:
        return ServerRunControl()
    return None


class RunControlRegistry:
    """Controls of the runs a queue drains at shutdown, keyed by run ID.

    Workers can finish on background threads (isolated loops), so every access
    takes a lock and ``drain_all`` works on a snapshot. Controls are registered
    before the run starts, and removed only by the claim that registered them,
    so a fast-finishing or superseded claim can't leave or remove the wrong
    entry.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._controls: dict[str, ServerRunControl] = {}

    def add(self, run_id: Any, control: ServerRunControl) -> None:
        """Register a run's control before the run starts."""
        with self._lock:
            self._controls[str(run_id)] = control

    def release(self, run_id: Any, control: ServerRunControl | None) -> None:
        """Remove a run's control if it is still the one this claim registered."""
        if control is None:
            return
        with self._lock:
            if self._controls.get(str(run_id)) is control:
                del self._controls[str(run_id)]

    def drain_all(self, reason: str) -> int:
        """Request a drain from every registered run; return how many."""
        with self._lock:
            controls = list(self._controls.values())
        for control in controls:
            control.request_drain(reason)
        return len(controls)


__all__ = [
    "DRAIN_SUPPORT",
    "SERVER_SHUTDOWN_DRAIN_REASON",
    "GraphDrained",
    "RunControl",
    "RunControlRegistry",
    "ServerRunControl",
    "mark_top_level",
    "new_run_control",
]
