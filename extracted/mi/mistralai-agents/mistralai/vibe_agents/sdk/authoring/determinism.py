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
    """Return the current time as a timezone-aware UTC datetime.

    In a workflow, this returns Temporal's replay-stable workflow time. In an activity or a local run,
    it returns the host clock. An activity result is recorded in workflow history, so its observed time
    remains stable on replay.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.now()

    return dt.datetime.now(dt.UTC)


def uuid4() -> uuid_module.UUID:
    """Return a UUID4 that is stable across replay of one workflow run.

    In a workflow, this uses Temporal's seeded generator. Outside a workflow, it uses `uuid.uuid4()`. A
    continue-as-new starts a new run with a new seed. Carry identifiers in continuation state when they
    must survive that boundary.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.uuid4()

    return uuid_module.uuid4()


def random() -> random_module.Random:
    """Return a random source that is stable across replay of one workflow run.

    In a workflow, this returns Temporal's seeded generator. Outside a workflow, it returns a new
    `random.Random`. A continue-as-new starts a new random sequence. The returned generator supports
    methods such as `random`, `uniform`, `choice`, and `shuffle`.
    """
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.random()

    return random_module.Random()  # noqa: S311 - public helper is not a cryptographic random source


async def sleep(duration: timedelta | float, *, summary: str | None = None) -> None:
    """Wait from a workflow, an activity, or a local run.

    In a workflow, this uses a durable Temporal timer. The timer survives worker restarts, holds no
    worker slot, and uses `summary` as its Temporal UI label. In an activity, this uses a heartbeating
    local sleep bounded by the activity's `start_to_close_timeout`. In a local run, this uses
    `asyncio.sleep`. The `summary` argument is ignored outside a workflow.

    Raises:
        SdkError: When an activity sleep would exceed its remaining `start_to_close_timeout`.
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
                f"agents.sleep({seconds:g}s) does not fit in what is left of activity "
                f"{info.activity_type!r}: {max(remaining_budget, 0.0):g}s of its "
                f"{budget.total_seconds():g}s start_to_close_timeout remain. The activity would be "
                "killed mid-sleep and its whole body retried. Sleep for less, or move the wait to "
                "the workflow side where it becomes a durable timer."
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
