from __future__ import annotations

import asyncio
import datetime as dt
import random as random_module
import uuid as uuid_module
from datetime import timedelta

import temporalio.activity
import temporalio.workflow

from .errors import SdkError

_ACTIVITY_SLEEP_SLICE_SECONDS = 5.0
_ACTIVITY_SLEEP_HEADROOM_SECONDS = 5.0


def now() -> dt.datetime:
    """The current time in UTC, as a timezone-aware datetime.

    Use it instead of ``datetime.now()``. In the agent loop of a deployed agent, such as in a custom
    sandbox's methods or a ``SandboxHook``, it gets the same time when the agent runs the loop again
    to resume a session, so a deadline holds. In a tool, a ``Hook`` or a local run, it is the clock's
    time: tools and ``Hook`` methods run as recorded steps, outside the part of the loop a deployed
    agent replays.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.now()

    return dt.datetime.now(dt.UTC)


def uuid4() -> uuid_module.UUID:
    """A random UUID that stays the same when a deployed agent runs the agent loop again.

    Use it instead of ``uuid.uuid4()``. In a tool, a ``Hook`` or a local run, it is ``uuid.uuid4()``.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.uuid4()

    return uuid_module.uuid4()


def random() -> random_module.Random:
    """A random number generator that gives the same numbers when a deployed agent runs the loop again.

    Use it instead of the ``random`` module. It has methods such as ``random``, ``uniform``,
    ``choice`` and ``shuffle``. In a tool, a ``Hook`` or a local run, it is a new
    ``random.Random``.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.random()

    return random_module.Random()  # noqa: S311 - public helper is not a cryptographic random source


async def sleep(duration: timedelta | float, *, summary: str | None = None) -> None:
    """Wait for ``duration``, in the agent loop, a tool, a ``Hook`` or a local run.

    Use it instead of ``asyncio.sleep()``. In the agent loop of a deployed agent, such as in a custom
    sandbox's methods or a ``SandboxHook``, the wait is a timer on the server: it survives a restart
    of the agent, and nothing of the agent runs while it waits. Tools and ``Hook`` methods run as
    recorded steps, outside the part of the loop a deployed agent replays: there the wait must end
    within the step's time limit. In a local run, it is ``asyncio.sleep()``.

    Args:
        duration: How long to wait, as a ``timedelta`` or in seconds.
        summary: A label for the wait in the agent loop of a deployed agent. Ignored elsewhere.

    Raises:
        SdkError: When the wait of a tool or a ``Hook`` would outlast the step's time limit.
    """
    if temporalio.workflow.in_workflow():
        await temporalio.workflow.sleep(duration, summary=summary)
        return

    seconds = duration.total_seconds() if isinstance(duration, timedelta) else float(duration)

    if seconds <= 0:
        return

    if not temporalio.activity.in_activity():
        await asyncio.sleep(seconds)
        return

    info = temporalio.activity.info()
    budget = info.start_to_close_timeout

    if budget is not None:
        elapsed = dt.datetime.now(dt.UTC) - info.started_time
        remaining_budget = budget.total_seconds() - elapsed.total_seconds() - _ACTIVITY_SLEEP_HEADROOM_SECONDS

        if seconds >= remaining_budget:
            raise SdkError(
                f"agents.sleep({seconds:g}s) does not fit in the time left for this call: "
                f"{max(remaining_budget, 0.0):g}s of its {budget.total_seconds():g}s time limit remain. "
                "The call would be stopped mid-sleep and run again from the start. Sleep for less."
            )

    slice_seconds = _ACTIVITY_SLEEP_SLICE_SECONDS

    if info.heartbeat_timeout is not None:
        slice_seconds = min(slice_seconds, info.heartbeat_timeout.total_seconds() / 3)

    remaining = seconds

    while remaining > 0:
        temporalio.activity.heartbeat()
        await asyncio.sleep(min(remaining, slice_seconds))
        remaining -= slice_seconds


__all__ = ["now", "random", "sleep", "uuid4"]
