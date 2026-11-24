"""The next step never waits for the previous boundary's checkpoint write (PF-WF E8, 2026-11-14).

Live (Smart Add person round, run a829e99f, v58): inside "Find a person's accounts" every step that is not
a pure chain member (a Run Workflow call, a links describe, a domain category, a For each) paid TWO
checkpoint round trips on the critical path — the pure chain before it was written before it could start
(~0.1 s), and its own boundary was written before the next step could start (~0.1 s). Fourteen such
boundaries in one unit ~1.5 s, the parent's tail another ~0.8 s.

A non-pure step's outcome is durable the moment it finishes (``record_outcome``); a pure step reruns safely.
So the checkpoint, a pointer over outcomes that are already safe, is written BESIDE the next step: the write
starts, the next step starts, and the following save (or the run's stop) waits for the write first. Rows stay
one per step, in order; ``checkpoint_saved`` still follows its write; the run's terminal event follows every
write. Step mode keeps the plain barrier.
"""

from __future__ import annotations

import asyncio
import time

from matrx_graph import Definition, RunStatus
from tests.test_a_boundaries_run_writes_one_checkpoint_per_chain import (
    _CountingCheckpointer,
    _scheduler,
    _SideEffect,
)
from tests.test_scheduler_ready_nodes_do_not_wait import _edge, _node, _Sleeper

WRITE_SECONDS = 0.1  # one checkpoint transaction under a busy pool (~8 round trips live)
# The unit's shape: pure transforms between steps that are not pure (Run Workflow, links describe, …).
# A non-pure step takes longer than one write (a Run Workflow call, a lookup): with one write in flight at a time
# (review 2026-11-14) the write beside it is fully hidden; instant steps would wait for the write before.
STEP_SECONDS = 0.12
SHAPE = ("p0", "x1", "p2", "x3", "p4", "x5", "p6", "x7", "p8")


class _SlowWrites(_CountingCheckpointer):
    """Every checkpoint transaction takes ``WRITE_SECONDS`` and is logged with its finish time."""

    def __init__(self) -> None:
        super().__init__()
        self.written: list[tuple[int, float]] = []

    async def save_checkpoint(self, checkpoint):  # type: ignore[override]
        await asyncio.sleep(WRITE_SECONDS)
        await super().save_checkpoint(checkpoint)
        self.written.append((checkpoint.step, time.monotonic()))

    async def save_checkpoint_with_outcomes(self, checkpoint, outcomes):  # type: ignore[override]
        await asyncio.sleep(WRITE_SECONDS)
        await super().save_checkpoint_with_outcomes(checkpoint, outcomes)
        self.written.append((checkpoint.step, time.monotonic()))

    async def save_checkpoint_chain(self, items):  # type: ignore[override]
        await asyncio.sleep(WRITE_SECONDS)
        await super().save_checkpoint_chain(items)
        for checkpoint, _ in items:
            self.written.append((checkpoint.step, time.monotonic()))


def _pair() -> tuple[_Sleeper, _SideEffect]:
    """A pure sleeper and a side-effect step writing ONE shared timeline."""
    sleeper, side = _Sleeper(), _SideEffect()
    side.runs, side.started, side.finished = sleeper.runs, sleeper.started, sleeper.finished
    return sleeper, side


def _mixed() -> Definition:
    nodes = []
    for node_id in SHAPE:
        node = _node(node_id, STEP_SECONDS if node_id.startswith("x") else 0.0)
        if node_id.startswith("x"):
            node["type"] = "test.side_effect"
        nodes.append(node)
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": [_edge(a, b) for a, b in zip(SHAPE, SHAPE[1:])],
            "entry_nodes": [SHAPE[0]],
        }
    )


async def test_a_mixed_chain_pays_no_checkpoint_write_between_its_steps() -> None:
    cp = _SlowWrites()
    sleeper, side = _pair()
    sched, _ = _scheduler(_mixed(), sleeper, checkpointer=cp, side=side, fresh_history=True)
    started = time.monotonic()
    result = await sched.run(run_id="mixed-chain")
    elapsed = time.monotonic() - started
    assert result.status is RunStatus.COMPLETED
    # Every step ran once, in order.
    assert [n for n, _ in sorted(sleeper.started.items(), key=lambda kv: kv[1])] == list(SHAPE)
    # THE GUARD: from the first step's start to the last step's start, no step waited for a write.
    # Before: each of the 8 hops waited for one (≥ 0.4 s at WRITE_SECONDS=0.1, the four non-pure
    # boundaries plus the four flushes of the pure step before them). Now: milliseconds.
    span = sleeper.started[SHAPE[-1]] - sleeper.started[SHAPE[0]]
    work = 4 * STEP_SECONDS  # the four non-pure steps' own time
    # One write in flight: a boundary right behind another (a pure step between two non-pure ones) awaits that write —
    # about one write per non-pure step (4 here), where it was two per step (8) before E8.
    assert span < work + 5 * WRITE_SECONDS, (
        f"the steps waited for checkpoint writes: {span:.2f}s across {len(SHAPE)} steps ({work:.2f}s of work)"
    )
    # Durability is intact at the end: one row per boundary, written in step order, all before the run returned.
    steps = [s for s, _ in cp.written]
    assert steps == sorted(steps), steps
    assert len(await cp.list_checkpoints("mixed-chain")) >= len(SHAPE) - 1
    assert elapsed >= WRITE_SECONDS  # the run's own last write was awaited


async def test_the_terminal_event_follows_every_checkpoint_write() -> None:
    cp = _SlowWrites()
    sched, _ = _scheduler(_mixed(), *_pair()[:1], checkpointer=cp, side=_pair()[1], fresh_history=True)
    assert (await sched.run(run_id="mixed-terminal")).status is RunStatus.COMPLETED
    events = [p.get("event") if isinstance(p, dict) else None for _m, p in sched.app.emitter.events]  # type: ignore[attr-defined]
    saved = [i for i, e in enumerate(events) if e == "checkpoint_saved"]
    done = [i for i, e in enumerate(events) if e == "run_completed"]
    assert saved and done, events
    assert max(saved) < done[0], "run_completed was announced before a checkpoint write landed"
