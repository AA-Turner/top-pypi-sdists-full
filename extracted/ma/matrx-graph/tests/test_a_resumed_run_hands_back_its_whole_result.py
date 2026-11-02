"""Guards (2026-10-28, child run 0c33f0f5 of "Assess one assurance lane", parent 520e47bc):
a called workflow ran every step, its server died before the run row said "completed", the
dead-server sweep parked it, and the parent's retry resumed it from its LAST checkpoint — an
empty frontier. The resumed leg ran nothing, so its ``last_outputs`` was ``{}``: the child read
"completed" with 0 steps and no result, and the parent failed ``child_result_missing``.

A resumed leg's result is the run's WHOLE result: what earlier legs settled rides beside what
this leg ran (this leg wins). A resumed leg that ran nothing and can read nothing of what ran
before ends FAILED saying so — never "completed" with nothing.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


class _Step:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.resumed_result_step",
        category=NodeCategory.DATA,
        display_name="step",
        description="resumed-result test node",
        input_schema=_Open,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )

    def __init__(self) -> None:
        self.calls: list[str] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg
    ) -> NodeResult[_Out]:
        self.calls.append(ctx.node_id)
        return success(_Out(text=f"{ctx.node_id} done"))


class _Quiet(_Step):
    """A side-effect step: its output never goes in the run row (``output_in_run_row=False``)."""

    spec: ClassVar[NodeSpec] = _Step.spec.model_copy(
        update={"node_type": "test.resumed_quiet_step", "output_in_run_row": False}
    )


class _HistoryLost(MemoryCheckpointer):
    """A store that cannot say what earlier legs settled (a read error)."""

    async def settled_outputs(
        self, run_id: str, node_ids: set[str], up_to_step: int | None = None
    ) -> dict[str, Any]:
        raise RuntimeError("node_outcome read timed out")


class _Spy(MemoryCheckpointer):
    """Records the step bound each ``settled_outputs`` read was scoped to."""

    def __init__(self) -> None:
        super().__init__()
        self.bounds: list[int | None] = []

    async def settled_outputs(
        self, run_id: str, node_ids: set[str], up_to_step: int | None = None
    ) -> dict[str, Any]:
        self.bounds.append(up_to_step)
        return await super().settled_outputs(run_id, node_ids, up_to_step)


def _chain(node_type: str = "test.resumed_result_step") -> dict:
    """start → result (the deliverable) → after (a closing step)."""

    def node(node_id: str, **data: Any) -> dict:
        return {
            "id": node_id,
            "type": node_type,
            "position": {"x": 0, "y": 0},
            "data": {"config": {}, **data},
        }

    def edge(eid: str, src: str, tgt: str) -> dict:
        return {
            "id": eid,
            "source": src,
            "target": tgt,
            "data": {"kind": "data", "mappings": {"a": "text"}},
        }

    return {
        "nodes": [node("start"), node("result", deliverable=True), node("after")],
        "edges": [edge("e1", "start", "result"), edge("e2", "result", "after")],
    }


def _scheduler(checkpointer: MemoryCheckpointer, quiet: bool = False) -> tuple[Scheduler, _Step]:
    step = _Quiet() if quiet else _Step()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    graph = compile_graph(Definition.model_validate(_chain(step.spec.node_type)), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry), step


async def _finished_run(checkpointer: MemoryCheckpointer, run_id: str) -> None:
    scheduler, _ = _scheduler(checkpointer)
    first = await scheduler.run(run_id=run_id)
    assert first.status is RunStatus.COMPLETED, first.error
    assert set(first.last_outputs) == {"start", "result", "after"}


async def test_a_run_resumed_after_every_step_had_run_hands_back_its_result():
    checkpointer = MemoryCheckpointer()
    await _finished_run(checkpointer, "resumed-finished")
    last = await checkpointer.latest_checkpoint("resumed-finished")
    assert last is not None and last.next_invocations == [], (
        "the last checkpoint has nothing left to run"
    )

    # The server died before the row said "completed"; the recovery resumes from the last checkpoint.
    scheduler, step = _scheduler(checkpointer)
    resumed = await scheduler.resume(run_id="resumed-finished", checkpoint_id=last.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.steps_executed == 0
    assert step.calls == [], "nothing re-runs"
    assert resumed.last_outputs.get("result") == {"text": "result done"}, resumed.last_outputs
    assert set(resumed.last_outputs) == {"start", "result", "after"}


async def test_a_resumed_leg_hands_back_what_earlier_legs_ran():
    checkpointer = MemoryCheckpointer()
    await _finished_run(checkpointer, "resumed-midway")
    # The checkpoint saved after `result` ran: only `after` is left (a drain cut the run there).
    midway = next(
        cp
        for cp in await checkpointer.list_checkpoints("resumed-midway")
        if [ni.node_id for ni in cp.next_invocations] == ["after"]
    )

    scheduler, _ = _scheduler(checkpointer)
    resumed = await scheduler.resume(run_id="resumed-midway", checkpoint_id=midway.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert resumed.last_outputs.get("result") == {"text": "result done"}, resumed.last_outputs
    assert resumed.last_outputs.get("start") == {"text": "start done"}, resumed.last_outputs
    assert "after" in resumed.last_outputs


async def test_a_resumed_run_with_nothing_left_and_no_readable_history_fails_loudly():
    checkpointer = _HistoryLost()
    await _finished_run(checkpointer, "resumed-blind")
    last = await checkpointer.latest_checkpoint("resumed-blind")
    assert last is not None

    scheduler, _ = _scheduler(checkpointer)
    resumed = await scheduler.resume(run_id="resumed-blind", checkpoint_id=last.checkpoint_id)

    assert resumed.status is RunStatus.FAILED, (resumed.status, resumed.last_outputs)
    assert resumed.failure is not None
    assert resumed.failure.error_type == "ResumedWithoutResult"
    assert "could not be read" in resumed.failure.message


async def test_a_resumed_run_whose_steps_legitimately_return_nothing_still_completes():
    """Side-effect steps keep their output out of the run row: a resume that ran 0 steps has
    nothing to hand back and that is an ordinary finish, never ResumedWithoutResult."""
    checkpointer = MemoryCheckpointer()
    scheduler, _ = _scheduler(checkpointer, quiet=True)
    first = await scheduler.run(run_id="resumed-quiet")
    assert first.status is RunStatus.COMPLETED, first.error
    last = await checkpointer.latest_checkpoint("resumed-quiet")
    assert last is not None and last.next_invocations == []

    scheduler, step = _scheduler(checkpointer, quiet=True)
    resumed = await scheduler.resume(run_id="resumed-quiet", checkpoint_id=last.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED, (resumed.status, resumed.error)
    assert resumed.steps_executed == 0
    assert step.calls == []


async def test_earlier_results_are_read_only_up_to_the_resumed_checkpoint():
    """A resume from an OLDER checkpoint of the run never takes a later leg's output as "earlier":
    the read is bounded by the resumed checkpoint's step, which travels as an argument of the leg
    (never Scheduler instance state)."""
    checkpointer = _Spy()
    await _finished_run(checkpointer, "resumed-bounded")
    midway = next(
        cp
        for cp in await checkpointer.list_checkpoints("resumed-bounded")
        if [ni.node_id for ni in cp.next_invocations] == ["after"]
    )
    scheduler, _ = _scheduler(checkpointer)
    resumed = await scheduler.resume(run_id="resumed-bounded", checkpoint_id=midway.checkpoint_id)
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert checkpointer.bounds == [midway.step]
    assert not hasattr(scheduler, "_resumed_leg")

    # The store itself never returns an outcome recorded after the bound.
    final = await checkpointer.latest_checkpoint("resumed-bounded")
    assert final is not None
    later = await checkpointer.settled_outputs("resumed-bounded", {"after"}, up_to_step=midway.step)
    assert later == {}, later
    assert await checkpointer.settled_outputs("resumed-bounded", {"after"}, up_to_step=final.step)
