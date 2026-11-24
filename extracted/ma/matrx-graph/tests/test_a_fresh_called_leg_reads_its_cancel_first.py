"""A fresh leg whose row another run can stop before it starts reads its status first.

A called workflow is created by its caller and run at once (``fresh_history``: no outcome lookups,
no first status read). Its caller's Cancel cascades onto its row (``RunStore.mark_cancelling``), and
can land between the row's creation and the first step. ``poll_first_boundary`` (set by the
resolver) makes that first boundary read the row, so the child never runs a paid first step after
its caller was cancelled (review of 118310e66, PF-WF 2026-11-02).
"""

from __future__ import annotations

import pytest

from matrx_graph import RunStatus
from tests.test_scheduler_ready_nodes_do_not_wait import _podcast_shape, _scheduler, _Sleeper


async def _cancelled_before_start() -> str:
    return "cancelling"


@pytest.mark.parametrize("polls", [True, False])
async def test_a_fresh_leg_cancelled_before_its_first_step_runs_nothing(polls: bool) -> None:
    sleeper = _Sleeper()
    scheduler, _cp, _em = _scheduler(
        _podcast_shape(),
        sleeper,
        control_check=_cancelled_before_start,
        control_check_reads_own_row=True,
        fresh_history=True,
        poll_first_boundary=polls,
    )
    result = await scheduler.run(run_id=f"fresh-called-{polls}")
    assert result.status is RunStatus.CANCELLED
    if polls:
        assert sleeper.runs == {}, f"a cancelled child ran {sleeper.runs}"
    else:
        # The gap the setting closes: without the first read the first step runs.
        assert "start" in sleeper.runs
