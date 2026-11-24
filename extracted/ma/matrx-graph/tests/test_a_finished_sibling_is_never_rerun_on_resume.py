"""A sibling that finished is never run again when its run resumes (P8-RUNS Gap 1, 2026-11-15).

Live (Smart Add Brand — Identify, workflow.run 7f560f36): a For-each-shaped step fanned four agent steps.
Two agent calls finished and were paid (runtime.global_execution completed at 01:56:25 and 01:56:29), but only
ONE outcome row landed (entity_kind, 01:56:26). The database stalled, the run died, and the resume ran three of
the four again: the second finished call was paid twice.

Cause: a step's outcome row is written at the END of its body — after its paid call returned, its live wire was
settled (up to 20 s), and its output kind was checked. When the run stops (lost lease, worker stop, a raising
boundary) ``_run_step`` canceled EVERY member, so a member whose paid call had already returned, but whose
outcome write was still in flight, was cut off and its result dropped.

The guard: n=4 non-pure siblings, k=2 finish (one with a slow outcome write, the stalled database), the run is
killed, resume runs exactly n-k.
"""

from __future__ import annotations

import asyncio

from matrx_graph import Definition, RunStatus
from matrx_graph.checkpoint.memory import MemoryCheckpointer
from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import _scheduler, _SideEffect
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper

SIBLINGS = ("a", "b", "c", "d")
FINISHED = ("a", "b")
WRITE_STALL_S = 0.3  # the outcome write of ``b`` sits in a slow database


class _StallingWrites(MemoryCheckpointer):
    def __init__(self) -> None:
        super().__init__()
        self.stall: set[str] = set()

    async def record_outcome(self, outcome):  # type: ignore[override]
        if outcome.node_id in self.stall and outcome.error is None:
            await asyncio.sleep(WRITE_STALL_S)
        await super().record_outcome(outcome)


def _fan_out(slow_s: float = 30.0) -> Definition:
    nodes = [_node("start")]
    for node_id in SIBLINGS:
        node = _node(node_id, 0.0 if node_id in FINISHED else slow_s)
        node["type"] = "test.side_effect"  # an agent step: never pure, never deferred
        nodes.append(node)
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": [_edge("start", s) for s in SIBLINGS],
            "entry_nodes": ["start"],
        }
    )


def _pair() -> tuple[_Sleeper, _SideEffect]:
    sleeper, side = _Sleeper(), _SideEffect()
    side.runs, side.started, side.finished = sleeper.runs, sleeper.started, sleeper.finished
    return sleeper, side


async def test_a_run_killed_mid_fan_out_reruns_only_the_siblings_that_never_finished() -> None:
    cp = _StallingWrites()
    cp.stall = {"b"}
    sleeper, side = _pair()
    sched, _ = _scheduler(_fan_out(), sleeper, checkpointer=cp, side=side)
    run = asyncio.create_task(sched.run(run_id="killed-mid-fan-out"))

    # Wait until both finishers returned from their paid call; ``b``'s outcome write is still in flight.
    for _ in range(400):
        if all(n in sleeper.finished for n in FINISHED):
            break
        await asyncio.sleep(0.005)
    assert all(n in sleeper.finished for n in FINISHED), sleeper.finished
    await asyncio.sleep(WRITE_STALL_S / 3)
    # The run dies (lease lost / worker stop): the drive task is canceled.
    run.cancel()
    try:
        await run
    except asyncio.CancelledError:
        pass

    checkpoint = await cp.latest_checkpoint("killed-mid-fan-out")
    assert checkpoint is not None
    sleeper2, side2 = _pair()
    sched2, _ = _scheduler(_fan_out(slow_s=0.0), sleeper2, checkpointer=cp, side=side2)
    result = await sched2.resume(run_id="killed-mid-fan-out", checkpoint_id=checkpoint.checkpoint_id)
    assert result.status is RunStatus.COMPLETED, result

    rerun = sorted(n for n in SIBLINGS if sleeper2.runs.get(n))
    unfinished = sorted(set(SIBLINGS) - set(FINISHED))
    assert rerun == unfinished, (
        f"resume ran {rerun} (n-k = {len(unfinished)} expected: {unfinished}) — a finished, paid sibling "
        "was run (and paid for) a second time"
    )
