"""Guard (H3, 2026-11-16): a run a step waits on that a person PAUSED pauses the caller — never fails it.

Live (research parity row 657db1ce): Pause on a run-everything run ended its caller "failed: child run ended
paused". The rule for every workflow: a step whose child is paused raises ``ChildRunPaused``; the calling run
parks PAUSED at that step (a sibling already finished keeps its result), and Resume runs the step again, which
continues the child — the run then completes.

Real ``Scheduler`` + ``MemoryCheckpointer``; the only double is the calling step (it stands for the host's
``subgraph.call`` / mandate-step resolver: paused child on the first leg, continued child on the resume).
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
from matrx_graph.errors import ChildRunPaused
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: str


class _CallChild:
    """Waits on a child run: the child is paused on the first call, continued (and answers) on the next."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.call_child",
        category=NodeCategory.SUBGRAPH,
        display_name="Run a workflow",
        description="paused-child test step",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    def __init__(self) -> None:
        self.calls = 0
        self.child_paused = True

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        if self.child_paused:
            raise ChildRunPaused("child-run-1")
        return success(_Out(answer="child finished"))


class _Sibling:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.sibling",
        category=NodeCategory.DATA,
        display_name="Sibling",
        description="paused-child test sibling",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        return success(_Out(answer="sibling"))


def _definition() -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "start", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'go': 1}"}}},
            {"id": "call", "type": "test.call_child", "position": {"x": 300, "y": 0}, "data": {"config": {}}},
            {"id": "sibling", "type": "test.sibling", "position": {"x": 300, "y": 200}, "data": {"config": {}}},
            {"id": "after", "type": "data.transform", "position": {"x": 600, "y": 0},
             "data": {"config": {"expression": "{'got': inputs['answer']}"}}},
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "call", "data": {"kind": "data", "mappings": {"go": "go"}}},
            {"id": "e2", "source": "start", "target": "sibling", "data": {"kind": "data", "mappings": {"go": "go"}}},
            {"id": "e3", "source": "call", "target": "after",
             "data": {"kind": "data", "mappings": {"answer": "answer"}}},
        ],
        "entry_nodes": ["start"],
    }


class _Control:
    def __init__(self) -> None:
        self.status: str | None = "running"

    async def check(self) -> str | None:
        return self.status


def _scheduler(call: _CallChild, sibling: _Sibling, checkpointer: MemoryCheckpointer, control: _Control) -> Scheduler:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(call, overwrite=True)
    registry.register(sibling, overwrite=True)
    graph = compile_graph(Definition.model_validate(_definition()), registry=registry)
    return Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry,
                     control_check=control.check)


async def test_a_paused_child_parks_its_caller_paused_and_resume_continues_it() -> None:
    call, sibling, checkpointer, control = _CallChild(), _Sibling(), MemoryCheckpointer(), _Control()

    paused = await _scheduler(call, sibling, checkpointer, control).run(run_id="paused-child")

    assert paused.status is RunStatus.PAUSED, (paused.status, paused.error)
    assert paused.error is None
    assert "after" not in paused.last_outputs

    call.child_paused = False  # the person presses Resume: the host continues the paused child
    checkpoint = await checkpointer.latest_checkpoint("paused-child")
    assert checkpoint is not None
    resumed = await _scheduler(call, sibling, checkpointer, control).resume(
        run_id="paused-child", checkpoint_id=checkpoint.checkpoint_id
    )

    assert resumed.status is RunStatus.COMPLETED, (resumed.status, resumed.error)
    assert resumed.last_outputs["after"] == {"got": "child finished"}
    assert call.calls == 2  # the step ran again on Resume, and was never retried as a failure
    assert sibling.calls == 1  # a sibling that finished before the pause is never run twice
