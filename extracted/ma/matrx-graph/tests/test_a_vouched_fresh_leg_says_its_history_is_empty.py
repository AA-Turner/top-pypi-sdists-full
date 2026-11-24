"""A leg the host vouched for (``fresh_history=True``) says, in memory, that its run has no history.

THE USE CASE: a records.write step looks for its own earlier held change before writing
(``matrx_records.held.prior_hold`` — a checkpoint read before EVERY write, ~1 round trip). On the
first and only leg of a run this process just created, no step can have paused yet, so the step may
skip that read; it learns so from ``Execution.history_known_empty`` (workflow lane B2, 2026-11-13).

THE BREAKS: a vouched fresh leg stops saying so (the read comes back); an unvouched fresh leg, or a
resumed one, says so (a retried step would file its held change a second time).
"""

from __future__ import annotations

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph.executor.execution import current_execution
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

SEEN: list[bool] = []


class _Free(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Probe:
    spec = NodeSpec(
        type="test.history_probe", category=NodeCategory.DATA, display_name="History Probe",
        input_schema=_Free, output_schema=_Free, determinism=ActionTier.SIDE_EFFECT,
        re_execute_on_resume=True,
    )

    async def execute(self, ctx, inputs, config=None):  # noqa: ANN001
        execution = current_execution()
        SEEN.append(bool(execution and execution.history_known_empty))
        return success(_Free())


def _scheduler(*, fresh_history: bool, with_pause: bool = False) -> tuple[Scheduler, MemoryCheckpointer]:
    nodes = [{"id": "save_visit", "type": "test.history_probe", "position": {"x": 400, "y": 0}, "data": {}}]
    edges = []
    if with_pause:
        nodes.append({"id": "front_desk_confirms", "type": "control.human_input", "position": {"x": 0, "y": 0},
                      "data": {"config": {"title": "Confirm", "preset": "free_text", "prompt": "Book it?"}}})
        edges = [{"id": "e1", "source": "front_desk_confirms", "target": "save_visit", "data": {}}]
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Probe())
    graph = compile_graph(Definition.model_validate({"nodes": nodes, "edges": edges}), registry=registry)
    checkpointer = MemoryCheckpointer()
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry,
                     fresh_history=fresh_history), checkpointer


async def test_a_vouched_first_leg_says_its_history_is_empty() -> None:
    SEEN.clear()
    scheduler, _ = _scheduler(fresh_history=True)
    result = await scheduler.run(run_id="booking-run-1")
    assert result.status is RunStatus.COMPLETED, result.error
    assert SEEN == [True]


async def test_an_unvouched_first_leg_never_says_so() -> None:
    SEEN.clear()
    scheduler, _ = _scheduler(fresh_history=False)
    await scheduler.run(run_id="booking-run-2")
    assert SEEN == [False]


async def test_a_resumed_leg_never_says_so_even_when_its_start_was_vouched() -> None:
    SEEN.clear()
    scheduler, checkpointer = _scheduler(fresh_history=True, with_pause=True)
    parked = await scheduler.run(run_id="booking-run-3")
    assert parked.status is RunStatus.INTERRUPTED
    checkpoint = await checkpointer.latest_checkpoint("booking-run-3")
    resumed = await scheduler.resume(run_id="booking-run-3", checkpoint_id=checkpoint.checkpoint_id,
                                     resume_value={"answer": "yes"})
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert SEEN == [False]
