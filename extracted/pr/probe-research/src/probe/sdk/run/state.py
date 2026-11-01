"""RunState: a run's close, OPEN -> FINISHING -> CLOSING -> CLOSED, read (never set) from the three
fields a close already keeps (`_finish_result`, `_terminal_in_flight`, `_closed_status`)."""

from __future__ import annotations

from typing import Any

from ...foundation.compat.compat import StrEnum


class RunState(StrEnum):
    #: Nothing has started closing it (a DisabledRun is always here: it records nothing).
    OPEN = "open"
    #: `finish()` is running: delivering the run's queued writes before its terminal status.
    FINISHING = "finishing"
    #: The terminal status write is on its way (an interrupt now re-queues that same status).
    CLOSING = "closing"
    #: The terminal status is recorded, or `finish()` returned with nothing left queued.
    CLOSED = "closed"


#: Every move a run can make. A bare `set_status` (a terminal status without `finish()`, as
#: `run.execute()` writes) skips FINISHING; a close that fails goes back to OPEN (finish() may
#: retry); nothing ever leaves CLOSED.
TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.OPEN: frozenset({RunState.FINISHING, RunState.CLOSING, RunState.CLOSED}),
    RunState.FINISHING: frozenset({RunState.OPEN, RunState.CLOSING, RunState.CLOSED}),
    RunState.CLOSING: frozenset({RunState.OPEN, RunState.CLOSED}),
    RunState.CLOSED: frozenset(),
}


def get_run_state(run: Any) -> RunState:
    """Where `run` is in its close, from the fields its close sets; no side effects."""
    from .closing.closing import _FINISHING
    from .handle import _UNSET

    fields = vars(run)
    finish_result = fields.get("_finish_result", _UNSET)
    in_flight = fields.get("_terminal_in_flight") is not None  # only ever set inside finish()
    if fields.get("_closed_status") is not None:
        return RunState.CLOSED
    if finish_result is _FINISHING:
        return RunState.CLOSING if in_flight else RunState.FINISHING
    if finish_result is not _UNSET:  # finish() returned; its status may still be queued
        return RunState.CLOSING if in_flight else RunState.CLOSED
    return RunState.OPEN  # never finished, or a close that failed: finish() may try again
