"""What THIS process is executing right now — in memory, never read from the database.

LANE 11 ROUND 5 (2026-10-02). Engine state persisted in ``workflow.*`` (checkpoints, node
outcomes, run inputs, metadata) is writable by a run's owner through PostgREST (WF-028). So any
decision that must not be talked into — "is this write the owner's standing rule?" — reads
the run's execution from here: the compiled graph the scheduler is actually driving, whether
this leg started fresh (``Scheduler.run``) or was loaded from a checkpoint
(``Scheduler.resume``: resume, resume-paused, retry, manual-result, recovery, a timer wake),
and which steps of this leg REPLAYED a stored outcome instead of executing.

The scheduler sets it for the length of one ``run``/``resume`` call; node tasks inherit it
(ContextVar). It is never persisted.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Execution:
    run_id: str
    definition_hash: str
    graph: Any
    fresh: bool
    #: Steps of THIS leg whose output came from a stored outcome, not from executing.
    replayed: set[str] = field(default_factory=set)
    #: The execution this one runs INSIDE (a called workflow running inline in a step), set by ``executing``.
    parent: Execution | None = None
    #: True only on a FRESH leg whose host vouched the run has no recorded history (``Scheduler(fresh_history=True)``:
    #: it created the run row moments ago in this process and this is the run's first and only leg). Nothing earlier
    #: in such a run can be read back — no outcome, no checkpoint, no paused step — so a step may skip a read that
    #: looks for one (``matrx_records.held.prior_hold``). Every resumed or re-delivered leg leaves it False.
    history_known_empty: bool = False
    #: ``async () -> bool``: is this run being stopped (a person's Stop or Pause, a lost lease)? Set by the
    #: scheduler; a step about to start a side effect asks it first (``tool.call``).
    stopping: Callable[[], Awaitable[bool]] | None = None


_current: ContextVar[Execution | None] = ContextVar("matrx_graph_execution", default=None)


def current_execution() -> Execution | None:
    return _current.get()


#: Root run id -> how many CALLED (child) executions are inside the block right now. A root's own execution is not
#: counted: it is the one settling. Lets a host keep what a root owns while a child still holds it.
_live_children: dict[str, int] = {}
_last_child_exit: Callable[[str], None] | None = None


def configure_last_child_exit(hook: Callable[[str], None] | None) -> None:
    """Install ``hook(root_run_id)``, called when the last child execution under a root leaves ``executing``."""
    global _last_child_exit
    _last_child_exit = hook


def live_children(root_run: str) -> int:
    """How many called workflows under ``root_run`` are executing right now (in this process)."""
    return _live_children.get(str(root_run), 0)


def _root_of(execution: Execution) -> str:
    while execution.parent is not None:
        execution = execution.parent
    return str(execution.run_id)


@contextmanager
def executing(execution: Execution) -> Iterator[Execution]:
    outer = _current.get()
    if execution.parent is None and outer is not None and outer is not execution:
        execution.parent = outer
    token = _current.set(execution)
    root = _root_of(execution) if execution.parent is not None else None
    if root is not None:
        _live_children[root] = _live_children.get(root, 0) + 1
    try:
        yield execution
    finally:
        try:
            _current.reset(token)
        finally:  # the count and the host's last-child hook run even when the reset raises
            if root is not None:
                left = _live_children.get(root, 1) - 1
                if left > 0:
                    _live_children[root] = left
                else:
                    _live_children.pop(root, None)
                    if _last_child_exit is not None:
                        try:
                            _last_child_exit(root)
                        except Exception:  # noqa: BLE001 — a host reaction never breaks the run leaving its block
                            pass


def root_run_id() -> str | None:
    """The top-level run this step belongs to: the called workflow's outermost caller (itself when it has none).

    Things a child run produces for its caller (a downloaded file's path) live and die with this run, never the
    child's own."""
    execution = _current.get()
    while execution is not None and execution.parent is not None:
        execution = execution.parent
    return str(execution.run_id) if execution is not None else None


def note_replayed(run_id: str, node_id: str) -> None:
    execution = _current.get()
    if execution is not None and execution.run_id == run_id:
        execution.replayed.add(node_id)


__all__ = [
    "Execution",
    "configure_last_child_exit",
    "current_execution",
    "executing",
    "live_children",
    "note_replayed",
    "root_run_id",
]
