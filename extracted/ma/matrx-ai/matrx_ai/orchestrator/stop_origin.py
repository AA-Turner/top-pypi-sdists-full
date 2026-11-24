"""Who asked a run to stop, readable from inside the cancelled run.

A background helper stopped with ``task_stop`` is cancelled with ``task.cancel()``; the run keeps what it streamed
and saves it as a stopped partial. The saved row and its closing sentence must say WHO stopped it (the person, or
the agent that started the helper), and the cancel carries no reason. The code that starts the work opens a box
before creating the task (the task copies the context, so the box is shared); whoever stops it writes ``by`` into
the box; the executor's cancel handler reads it. ``None`` = nobody said (a disconnect, a deploy): the saved text
then claims no stopper.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Literal

StoppedBy = Literal["person", "agent"]

_BOX: ContextVar[dict[str, str] | None] = ContextVar("matrx_ai_stop_origin", default=None)


@contextmanager
def open_stop_box() -> Iterator[dict[str, str]]:
    """Open the box for work about to be started as a task (create the task inside the ``with``)."""
    box: dict[str, str] = {}
    token = _BOX.set(box)
    try:
        yield box
    finally:
        _BOX.reset(token)


def mark_stopped_by(box: dict[str, str] | None, by: str | None) -> None:
    if box is not None and by in ("person", "agent"):
        box["by"] = by


def stopped_by() -> StoppedBy | None:
    """Who stopped the run this code is inside, or None."""
    box = _BOX.get()
    by = box.get("by") if box else None
    return by if by in ("person", "agent") else None  # type: ignore[return-value]
