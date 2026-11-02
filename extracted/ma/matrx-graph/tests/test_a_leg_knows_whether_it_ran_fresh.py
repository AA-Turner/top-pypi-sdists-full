"""A leg knows, in memory, whether it ran fresh — and which steps it only replayed (lane 11 round 5).

THE USE CASE: a physio clinic's "When a Patient is Booked, create a Visit" workflow writes as
its owner only inside the first leg its verified trigger started. Every recovery door —
resume, resume-paused, retry with inputs, manual-result, a recovery sweep, a timer wake —
continues a run through ``Scheduler.resume`` from a checkpoint; and a step whose outcome is
already stored (rows the owner can write) is REPLAYED, not executed. The write's decision
reads this module's in-memory record, never the database.

THE BREAKS:
* ``Scheduler.run`` stops marking its leg fresh, or stops naming the graph it drives;
* ``Scheduler.resume`` marks a checkpoint-loaded leg fresh;
* a replayed step is not remembered (a stored outcome would count as executed here).

All real engine: registry, compiler, scheduler, ``control.human_input``, MemoryCheckpointer.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.executor.execution import current_execution
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

SEEN: list[dict[str, Any]] = []


class _Free(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Probe:
    """The write step's seat: what does THIS leg look like from inside a node?"""

    spec = NodeSpec(
        type="test.leg_probe", category=NodeCategory.DATA, display_name="Leg Probe",
        input_schema=_Free, output_schema=_Free, determinism=ActionTier.SIDE_EFFECT,
        re_execute_on_resume=True,
    )

    async def execute(self, ctx, inputs, config=None):  # noqa: ANN001
        from matrx_orm.core.session_context import current_workflow_chain

        execution = current_execution()
        chain = current_workflow_chain()
        SEEN.append(
            {"run_id": execution.run_id, "fresh": execution.fresh,
             "hash": execution.definition_hash, "replayed": sorted(execution.replayed),
             "chain": (chain.root_run, chain.depth) if chain else None}
            if execution else {}
        )
        return success(_Free())


def _graph(with_pause: bool) -> tuple[Scheduler, MemoryCheckpointer, Any]:
    nodes = [{"id": "intake", "type": "data.transform", "position": {"x": 0, "y": 0},
              "data": {"config": {"expression": "'booked'"}}},
             {"id": "make_visit", "type": "test.leg_probe", "position": {"x": 400, "y": 0},
              "data": {}}]
    edges = [{"id": "e1", "source": "intake", "target": "make_visit", "data": {}}]
    if with_pause:
        nodes.append({"id": "front_desk_confirms", "type": "control.human_input",
                      "position": {"x": 200, "y": 0},
                      "data": {"config": {"title": "Confirm", "preset": "free_text",
                                          "prompt": "Book it?"}}})
        edges = [{"id": "e1", "source": "intake", "target": "front_desk_confirms", "data": {}},
                 {"id": "e2", "source": "front_desk_confirms", "target": "make_visit",
                  "data": {}}]
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Probe())
    graph = compile_graph(Definition.model_validate({"nodes": nodes, "edges": edges}),
                          registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    return scheduler, checkpointer, graph


async def test_a_started_leg_is_fresh_on_the_graph_it_drives() -> None:
    SEEN.clear()
    scheduler, _, graph = _graph(with_pause=False)
    result = await scheduler.run(run_id="visit-run-1")
    assert result.status is RunStatus.COMPLETED, result.error
    assert SEEN == [{"run_id": "visit-run-1", "fresh": True,
                     "hash": str(graph.definition_hash), "replayed": [],
                     "chain": ("visit-run-1", 1)}]
    assert current_execution() is None  # never leaks past the leg


async def test_a_resumed_leg_is_never_fresh() -> None:
    SEEN.clear()
    scheduler, checkpointer, _ = _graph(with_pause=True)
    parked = await scheduler.run(run_id="visit-run-2")
    assert parked.status is RunStatus.INTERRUPTED
    checkpoint = await checkpointer.latest_checkpoint("visit-run-2")
    resumed = await scheduler.resume(run_id="visit-run-2", checkpoint_id=checkpoint.checkpoint_id,
                                     resume_value={"answer": "yes"})
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert [s["fresh"] for s in SEEN] == [False], SEEN


async def test_a_stored_outcome_is_remembered_as_replayed() -> None:
    """A second start of the same run id (a forged start job) finds intake's outcome stored
    and replays it — the leg says so."""
    SEEN.clear()
    scheduler, _, _ = _graph(with_pause=False)
    await scheduler.run(run_id="visit-run-3")
    await scheduler.run(run_id="visit-run-3")
    assert [s["replayed"] for s in SEEN] == [[], ["intake"]], SEEN


async def test_a_resumed_leg_keeps_the_depth_of_the_change_that_started_it() -> None:
    """Round 5: a resumed leg declared a FRESH root (depth 1) — a loop could restart its count
    by pausing. Now the host's resolver names the starting change's chain (from the outbox)."""
    from matrx_graph.executor.resume_chain import configure_resume_chain_resolver

    async def from_outbox(run_id: str):
        return {"root_run": "the-first-run", "depth": 2}

    SEEN.clear()
    configure_resume_chain_resolver(from_outbox)
    try:
        scheduler, checkpointer, _ = _graph(with_pause=True)
        await scheduler.run(run_id="visit-run-4")
        checkpoint = await checkpointer.latest_checkpoint("visit-run-4")
        await scheduler.resume(run_id="visit-run-4", checkpoint_id=checkpoint.checkpoint_id,
                               resume_value={"answer": "yes"})
    finally:
        configure_resume_chain_resolver(None)
    assert [s["chain"] for s in SEEN] == [("the-first-run", 3)], SEEN


async def test_a_stored_failure_routed_to_the_write_is_remembered_too() -> None:
    """Round 7 (major): node_outcome is owner-insertable. A FAILED outcome stored for a step is
    walked forward / routed down its ERROR edge without the step running — it steers the leg
    exactly like a replayed success, so it is remembered as replayed too."""
    from matrx_graph.checkpoint.protocol import NodeOutcome

    SEEN.clear()
    nodes = [{"id": "intake", "type": "data.transform", "position": {"x": 0, "y": 0},
              "data": {"config": {"expression": "'booked'"}}},
             {"id": "make_visit", "type": "test.leg_probe", "position": {"x": 400, "y": 0},
              "data": {}}]
    edges = [{"id": "on_failure", "source": "intake", "target": "make_visit",
              "data": {"kind": "error", "mappings": {"why": "message"}}}]
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Probe())
    graph = compile_graph(Definition.model_validate({"nodes": nodes, "edges": edges}),
                          registry=registry)
    checkpointer = MemoryCheckpointer()
    for attempt in range(1, 11):  # every attempt the retry policy could walk through
        await checkpointer.record_outcome(NodeOutcome(
            run_id="visit-run-5", step=0, node_id="intake", attempt=attempt, output={},
            error={"type": "ValueError", "message": "forged by the run's owner"}))
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    await scheduler.run(run_id="visit-run-5")
    assert [s["replayed"] for s in SEEN] == [["intake"]], SEEN

