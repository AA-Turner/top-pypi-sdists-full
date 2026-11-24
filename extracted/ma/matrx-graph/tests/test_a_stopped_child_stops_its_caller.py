"""Guard (H12b, 2026-11-16): a run a step waits on that a Stop ended CANCELLED stops the caller — never errors it.

Live (research Stop pairs): a workflow step calling a workflow-held mandate whose run a Stop ended ``cancelled``
parked its caller ``errored`` ("child run ended cancelled"). The stopped twin of ``ChildRunPaused``: a step whose
child was stopped raises ``ChildRunStopped``; the calling run ends CANCELLED at that step, no step after it starts,
a sibling already working finishes, and nothing is recorded as a failure.

Real ``Scheduler`` + ``MemoryCheckpointer``; the only double is the calling step (the host's ``subgraph.call`` /
mandate-step resolver).
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
from matrx_graph.errors import ChildRunStopped
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
    """Waits on a child run that a Stop ended cancelled."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.call_child",
        category=NodeCategory.SUBGRAPH,
        display_name="Run a workflow",
        description="stopped-child test step",
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
        raise ChildRunStopped("child-run-1")


class _Sibling:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.sibling",
        category=NodeCategory.DATA,
        display_name="Sibling",
        description="stopped-child test sibling",
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
    async def check(self) -> str | None:
        return "running"


async def test_a_stopped_child_ends_its_caller_cancelled_and_nothing_new_starts() -> None:
    call, sibling, checkpointer = _CallChild(), _Sibling(), MemoryCheckpointer()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(call, overwrite=True)
    registry.register(sibling, overwrite=True)
    graph = compile_graph(Definition.model_validate(_definition()), registry=registry)
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry,
                          control_check=_Control().check)

    stopped = await scheduler.run(run_id="stopped-child")

    assert stopped.status is RunStatus.CANCELLED, (stopped.status, stopped.error)
    assert stopped.error is None, "a Stop is never recorded as a failure"
    assert "after" not in stopped.last_outputs, "no step after the stopped child starts"
    assert call.calls == 1, "a stopped child is never retried"
    # A sibling already working finishes; one not yet started never starts (it waits in the saved frontier).
    assert sibling.calls <= 1
    assert await checkpointer.latest_checkpoint("stopped-child") is not None, "the frontier is saved"
