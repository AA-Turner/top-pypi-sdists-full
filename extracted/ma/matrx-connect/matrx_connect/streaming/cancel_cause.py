"""Why a stream's work ended in ``asyncio.CancelledError`` — the ONE classifier.

A cancelled stream used to be filed as ``stream_cancelled`` with the text "client disconnect or
shutdown" whatever happened (live 2026-11-16: every research row read "client disconnect" while the
traceback showed the person's Stop, or a child workflow run that ended cancelled because of that Stop).
Every streaming cancel handler asks this module instead, so the recorded reason is the true one and a
by-design end (an honored Stop, a client leaving a route that declared its work disposable) is never an
open error, while a cancel that cut work off with nothing to restart it still files one.

The causes, in the order they are decided:

* ``stopped`` / ``child_run_stopped`` — nobody cancelled this task: the work read a Stop (a person's Stop,
  ``POST /cancel``) and unwound by raising ``CancelledError`` itself; ``child_run_stopped`` when it raised
  it FROM a child run's cancelled end (``raise CancelledError(...) from MandateStopped``). By design.
* ``server_shutdown`` — the host reports it is draining (a deploy). Work was cut off: an error, UNLESS
  something resumes it. Only the host's run reaper knows that (it skips a run whose resumer carries it on
  and alarms ``runtime_execution_abandoned`` otherwise), so a stream with a durable run leaves the alarm
  to the reaper; one with no run files here.
* ``client_disconnect`` — the route opted out of detaching and its client left, so the work was stopped
  on purpose. By design.
* ``external_cancel`` — someone called ``task.cancel()`` and it was none of the above (or a shutdown the
  host did not report). Work was cut off: an error.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal

from matrx_connect.streaming.run_tracking import host_is_shutting_down

StreamCancelCause = Literal[
    "stopped", "child_run_stopped", "server_shutdown", "client_disconnect", "external_cancel"
]

_BY_DESIGN: frozenset[str] = frozenset({"stopped", "child_run_stopped", "client_disconnect"})


@dataclass(frozen=True)
class StreamCancel:
    """One classified cancel: its cause, the true sentence to record, and whether it is an error."""

    cause: StreamCancelCause
    reason: str

    @property
    def by_design(self) -> bool:
        """True when nothing was lost that should have been kept: never an open error row."""
        return self.cause in _BY_DESIGN

    def text(self, label: str) -> str:
        return f"{label} {self.reason}"


def work_stopped_itself() -> bool:
    """True when the CancelledError being handled was RAISED BY THE WORK, not delivered to this task.

    A task someone cancelled (shutdown, a disconnect, ``task.cancel()``) has ``cancelling() > 0``; work that
    read a Stop and unwound by raising ``CancelledError`` itself leaves it at 0. A host shutting down is never
    a Stop: its runs are abandoned so the reaper and the restart hook pick them up."""
    task = asyncio.current_task()
    if task is None or task.cancelling() > 0:
        return False
    return not host_is_shutting_down()


def _said(exc: BaseException) -> str:
    text = str(exc).strip()
    return f": {text}" if text else ""


def classify_stream_cancel(exc: BaseException, *, client_disconnected: bool = False) -> StreamCancel:
    """Classify the ``CancelledError`` being handled in the current task. Never raises."""
    if work_stopped_itself():
        cause = exc.__cause__
        if cause is not None and not isinstance(cause, asyncio.CancelledError):
            return StreamCancel(
                "child_run_stopped",
                f"stopped: a child run it waited on ended cancelled ({type(cause).__name__}{_said(cause)})",
            )
        return StreamCancel("stopped", f"stopped by a Stop the work obeyed{_said(exc)}")
    if host_is_shutting_down():
        return StreamCancel(
            "server_shutdown",
            "cut off by a server shutdown (deploy drain)",
        )
    if client_disconnected:
        return StreamCancel(
            "client_disconnect",
            "stopped because its client disconnected (the route does not detach its work)",
        )
    return StreamCancel(
        "external_cancel",
        "cut off by an outside task.cancel() that was not a Stop, a client disconnect or a reported "
        f"shutdown{_said(exc)}",
    )


__all__ = ["StreamCancel", "StreamCancelCause", "classify_stream_cancel", "work_stopped_itself"]
