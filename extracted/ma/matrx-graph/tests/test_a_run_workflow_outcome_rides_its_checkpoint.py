"""A Run Workflow step's outcome rides its checkpoint, after the child's held end lands (P8-RUNS levers 1 + 2).

Live 2026-11-15 (Smart Add person round, v64): after a called child's last step the caller paid, one after
another, the child's event flush, the child's terminal write, then its OWN outcome write — before its next
step could start. Two of those leave the path:

- Lever 1: a step whose re-run hands back what its first run made (a Run Workflow whose host reattaches a
  finished child by its deterministic id, ``rerun_returns_saved_result``) need not write its outcome before the
  next step: the outcome rides the step's checkpoint (written beside the next step), as a pure step's does. A
  crash before that checkpoint re-runs the step, which reattaches — never a rerun of the child, never a charge.
- Lever 2: the child's flush + terminal write are HELD (``ctx.hold_outcome_until``): the step answers at once,
  and the scheduler awaits the held write before it writes this run's next outcome or checkpoint and before the
  run ends — so the child's end is durable BEFORE the caller's record of it, as it was.

Red before: the reattaching step wrote its outcome on its own (``record_outcome``); a held write was never
awaited before the checkpoint carrying the outcome (or ``hold_outcome_until`` did not exist).
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, ClassVar

from matrx_graph import Definition, RunStatus
from matrx_graph.types import NodeExecutionContext, NodeSpec
from matrx_graph.types.primitives import ActionTier
from matrx_graph.types.result import NodeResult
from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import _CountingCheckpointer, _scheduler
from tests.test_scheduler_ready_nodes_do_not_wait import _Cfg, _edge, _In, _node, _Out, _Sleeper

WRITE = 0.1  # one round trip under load


class _Calls(_Sleeper):
    """A Run Workflow in miniature: NON_DETERMINISTIC, may spend, and (``reattaches``) a re-run answers saved."""

    spec: ClassVar[NodeSpec] = _Sleeper.spec.model_copy(
        update={"node_type": "test.calls", "determinism": ActionTier.NON_DETERMINISTIC}
    )

    def __init__(self, timeline: list[str], *, reattaches: bool = True, hold: bool = True) -> None:
        super().__init__()
        self.timeline = timeline
        self.reattaches = reattaches
        self.hold = hold

    def rerun_returns_saved_result(self) -> bool:
        return self.reattaches

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        answer = await super().execute(ctx, inputs, config)

        async def child_end() -> None:  # the child's event flush, then its terminal write
            await asyncio.sleep(WRITE)
            self.timeline.append("child_events_durable")
            await asyncio.sleep(WRITE)
            self.timeline.append(f"child_terminal:{ctx.node_id}")

        if self.hold and ctx.holds_outcome_writes:
            assert ctx.hold_outcome_until(asyncio.ensure_future(child_end()))
        else:
            await child_end()
        self.timeline.append(f"answered:{ctx.node_id}")
        return answer


class _Ordered(_CountingCheckpointer):
    """Logs which write carried which step's outcome."""

    def __init__(self, timeline: list[str]) -> None:
        super().__init__()
        self.timeline = timeline
        self.alone: list[str] = []

        self.carrying = False

    async def record_outcome(self, outcome):  # type: ignore[override]
        if not self.carrying:  # an outcome written on its own (not inside a checkpoint's transaction)
            self.timeline.append(f"outcome:{outcome.node_id}")
        await super().record_outcome(outcome)

    async def save_checkpoint_with_outcomes(self, checkpoint, outcomes):  # type: ignore[override]
        await asyncio.sleep(WRITE)
        self.timeline.append("checkpoint_with:" + ",".join(o.node_id for o in outcomes))
        self.carrying = True
        try:
            await super().save_checkpoint_with_outcomes(checkpoint, outcomes)
        finally:
            self.carrying = False


def _flow() -> Definition:
    call = _node("call", 0.0)
    call["type"] = "test.calls"
    return Definition.model_validate(
        {"nodes": [_node("a"), call, _node("next")], "edges": [_edge("a", "call"), _edge("call", "next")],
         "entry_nodes": ["a"]}
    )


def _run(timeline: list[str], **kw: Any):
    calls = _Calls(timeline, **kw)
    calls.runs, calls.started, calls.finished = {}, {}, {}
    sleeper = _Sleeper()
    sleeper.started = calls.started
    cp = _Ordered(timeline)
    sched, _ = _scheduler(_flow(), sleeper, checkpointer=cp, side=calls, fresh_history=True)
    return sched, cp, calls


async def test_a_reattaching_calls_outcome_rides_its_checkpoint_after_the_childs_end() -> None:
    timeline: list[str] = []
    sched, cp, calls = _run(timeline)
    began = time.monotonic()
    result = await sched.run(run_id="call-rides")
    assert result.status is RunStatus.COMPLETED, result
    # Lever 1: the call's outcome was never written on its own — it rode a checkpoint.
    assert "outcome:call" not in timeline, timeline
    carried = [e for e in timeline if e.startswith("checkpoint_with:") and "call" in e.split(":", 1)[1].split(",")]
    assert carried, timeline
    # Lever 2 keeps the order: the child's events, then its end, then the caller's record of it.
    assert timeline.index("child_events_durable") < timeline.index("child_terminal:call") < timeline.index(carried[0])
    # The step answered before the child's end landed (the held write left the step's path) …
    assert timeline.index("answered:call") < timeline.index("child_terminal:call"), timeline
    # … and the run never ended before it did.
    assert time.monotonic() - began >= 2 * WRITE


async def test_a_call_whose_rerun_would_run_again_still_writes_its_outcome_at_once() -> None:
    timeline: list[str] = []
    sched, _cp, _calls = _run(timeline, reattaches=False)
    assert (await sched.run(run_id="call-alone")).status is RunStatus.COMPLETED
    assert "outcome:call" in timeline, timeline
    # Its held child end still lands before its own outcome does.
    assert timeline.index("child_terminal:call") < timeline.index("outcome:call"), timeline


async def test_a_held_write_that_fails_is_never_dropped() -> None:
    class _Fails(_Calls):
        async def execute(self, ctx, inputs, config):  # type: ignore[override]
            answer = await _Sleeper.execute(self, ctx, inputs, config)

            async def broken() -> None:
                await asyncio.sleep(0.01)
                raise RuntimeError("the child's terminal write failed")

            ctx.hold_outcome_until(asyncio.ensure_future(broken()))
            return answer

    timeline: list[str] = []
    calls = _Fails(timeline)
    calls.runs, calls.started, calls.finished = {}, {}, {}
    sched, _ = _scheduler(_flow(), _Sleeper(), checkpointer=_Ordered(timeline), side=calls, fresh_history=True)
    try:
        result = await sched.run(run_id="call-held-fails")
    except RuntimeError as exc:
        assert "terminal write failed" in str(exc)
    else:
        assert result.status is not RunStatus.COMPLETED, result  # loud: the run does not finish as if it landed
    # The call's outcome never landed ahead of a write it was owed.
    assert not any(e.startswith("checkpoint_with:") and "call" in e for e in timeline), timeline


async def test_a_context_no_scheduler_awaits_refuses_to_hold() -> None:
    from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import FakeEmitter, make_app_context

    from matrx_graph.types.context import ChannelView

    ctx = NodeExecutionContext(app=make_app_context(FakeEmitter()), run_id="r", thread_id="r", node_id="n", step=0,
                               attempt=1, channels=ChannelView(_values={}, _pending_writes=[]), checkpointer=None)
    fut = asyncio.get_running_loop().create_future()
    assert ctx.holds_outcome_writes is False and ctx.hold_outcome_until(fut) is False
    fut.cancel()
