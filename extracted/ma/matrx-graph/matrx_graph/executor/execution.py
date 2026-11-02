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

from collections.abc import Iterator
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


_current: ContextVar[Execution | None] = ContextVar("matrx_graph_execution", default=None)


def current_execution() -> Execution | None:
    return _current.get()


@contextmanager
def executing(execution: Execution) -> Iterator[Execution]:
    token = _current.set(execution)
    try:
        yield execution
    finally:
        _current.reset(token)


def note_replayed(run_id: str, node_id: str) -> None:
    execution = _current.get()
    if execution is not None and execution.run_id == run_id:
        execution.replayed.add(node_id)


__all__ = ["Execution", "current_execution", "executing", "note_replayed"]
