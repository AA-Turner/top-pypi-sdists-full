"""A chain of instant (pure) steps lands its checkpoints in ONE save (PF-WF, 2026-11-02).

Live, after the event-loop fixes: an instant step still cost ~110 ms, 88 of them its own checkpoint
transaction (~8 round trips), so an 11-step sub-workflow of transforms took 1.2 s. Consecutive
pure super-steps now queue their checkpoints and write them in one transaction when the chain
ends — one row per step is kept (Re-run from, Fork from, the timeline and step mode need it), and
each step's completion event still precedes its ``checkpoint_saved``.

Red before: 12 transforms made 12 separate saves and no chain save.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph import register_builtin_nodes
from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome
from tests._fixtures import FakeEmitter, make_app_context

STEPS = 12


def _chain(n: int = STEPS) -> Definition:
    nodes = [
        {
            "id": f"t{i}",
            "type": "data.transform",
            "position": {"x": i * 200, "y": 0},
            "data": {"label": f"Step {i}", "config": {"expression": f"{{'n': {i}}}"}},
        }
        for i in range(n)
    ]
    edges = [
        {
            "id": f"e{i}",
            "source": f"t{i}",
            "target": f"t{i + 1}",
            "data": {"kind": "data", "mappings": {"n": "n"}},
        }
        for i in range(n - 1)
    ]
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["t0"]})


class _CountingCheckpointer(MemoryCheckpointer):
    """Counts each kind of save the scheduler makes (each is one transaction in Postgres)."""

    def __init__(self) -> None:
        super().__init__()
        self.single_saves = 0
        self.chain_saves: list[int] = []

    async def save_checkpoint_with_outcomes(self, checkpoint: Checkpoint, outcomes: list[NodeOutcome]) -> None:
        self.single_saves += 1
        await super().save_checkpoint_with_outcomes(checkpoint, outcomes)

    async def save_checkpoint_chain(self, items: list[tuple[Checkpoint, list[NodeOutcome]]]) -> None:
        self.chain_saves.append(len(items))
        for checkpoint, outcomes in items:
            await MemoryCheckpointer.save_checkpoint_with_outcomes(self, checkpoint, outcomes)


def _scheduler(checkpointer: MemoryCheckpointer, emitter: FakeEmitter, **kwargs: Any) -> Scheduler:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(_chain(), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry, **kwargs)


def _events(emitter: FakeEmitter) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    for kind, payload in emitter.events:
        if kind != "data" or not isinstance(payload, dict):
            continue
        name = payload.get("event")
        out.append((str(name), payload.get("step") if name == "checkpoint_saved" else payload.get("node_id")))
    return out


async def test_twelve_instant_steps_land_in_one_chain_save_with_every_checkpoint_kept() -> None:
    checkpointer = _CountingCheckpointer()
    emitter = FakeEmitter()
    result = await _scheduler(checkpointer, emitter).run(run_id="chain")

    assert result.status is RunStatus.COMPLETED, result.error
    saves = checkpointer.single_saves + len(checkpointer.chain_saves)
    assert saves <= 2, f"{saves} saves for {STEPS} instant steps (single {checkpointer.single_saves}, chains {checkpointer.chain_saves})"
    checkpoints = await checkpointer.list_checkpoints("chain")
    assert sorted(cp.step for cp in checkpoints) == list(range(STEPS)), "a step lost its checkpoint"
    by_id = {cp.checkpoint_id: cp for cp in checkpoints}
    for cp in checkpoints:
        if cp.step:
            assert by_id[cp.parent_checkpoint_id].step == cp.step - 1, "the checkpoint chain is broken"
    # Every step's outcome landed, and its completion is announced before its step's checkpoint.
    for i in range(STEPS):
        assert await checkpointer.get_outcome(run_id="chain", step=i, node_id=f"t{i}", attempt=1) is not None
    events = [e for e in _events(emitter) if e[0] in ("node_completed", "checkpoint_saved")]
    for i in range(STEPS):
        assert events.index(("node_completed", f"t{i}")) < events.index(("checkpoint_saved", i)), events


async def test_step_mode_keeps_one_save_per_step() -> None:
    """Step mode (Run N steps from here) parks on its own checkpoint: never part of a chain."""
    checkpointer = _CountingCheckpointer()
    assert (await _scheduler(checkpointer, FakeEmitter()).run(run_id="stepping")).status is RunStatus.COMPLETED
    first = min(await checkpointer.list_checkpoints("stepping"), key=lambda cp: cp.step)
    chains_before = list(checkpointer.chain_saves)
    stepped = await _scheduler(checkpointer, FakeEmitter()).resume(
        run_id="stepping", checkpoint_id=first.checkpoint_id, stop_after_steps=3
    )
    assert stepped.status is RunStatus.PAUSED, stepped.error
    assert checkpointer.chain_saves == chains_before, "step mode queued its checkpoints into a chain"


async def test_a_cancel_inside_a_chain_stops_the_run_and_lands_every_checkpoint_before_it() -> None:
    """A Cancel that arrives while a chain is queued stops the run at the next boundary, CANCELLED
    (never a run that ends 'completed' over a cancel), and every step before it keeps its
    checkpoint (review of the chain change, 2026-11-02: a latch-only boundary lost the cancel)."""
    checkpointer = _CountingCheckpointer()
    polls = {"n": 0}

    async def cancel_after_four_boundaries() -> bool:
        polls["n"] += 1
        return polls["n"] >= 4

    scheduler = _scheduler(checkpointer, FakeEmitter(), cancel_check=cancel_after_four_boundaries)
    result = await scheduler.run(run_id="cancel-chain")
    assert result.status is RunStatus.CANCELLED, result.status
    steps = sorted(cp.step for cp in await checkpointer.list_checkpoints("cancel-chain"))
    assert steps and steps == list(range(len(steps))), f"a checkpoint inside the chain was lost: {steps}"
    assert len(steps) < STEPS, "the run did not stop at the cancel"
    assert checkpointer.chain_saves, "the steps before the cancel were not a chain"


async def test_a_pause_inside_a_chain_parks_on_its_own_checkpoint() -> None:
    checkpointer = _CountingCheckpointer()
    polls = {"n": 0}

    async def pause_after_three_boundaries() -> bool:
        polls["n"] += 1
        return polls["n"] >= 3

    result = await _scheduler(checkpointer, FakeEmitter(), pause_check=pause_after_three_boundaries).run(run_id="pause-chain")
    assert result.status is RunStatus.PAUSED, result.status
    steps = sorted(cp.step for cp in await checkpointer.list_checkpoints("pause-chain"))
    assert steps == list(range(len(steps))), steps
