"""Guard (2026-09-11, expert-book challenge W28): a node fed a value its
input schema refuses is a FAILURE OF THAT NODE, and an ERROR edge catches it
like any other. Before this guard the input parse ran outside the routable
path, so a desk with a catch route wired for "no calendar date" still parked
the whole run on the weather step (runs 7 and 8 of the Verification Desk).
"""

from __future__ import annotations

import datetime as dt
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


class _DateIn(BaseModel):
    model_config = ConfigDict(extra="allow")

    date: dt.date


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"


def _spec(node_type: str, input_schema: type[BaseModel]) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="input-gate routability test node",
        input_schema=input_schema,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )


class _EmptyDateProducer:
    """Stands in for a post reader that honestly found no calendar date."""

    spec: ClassVar[NodeSpec] = _spec("test.w28_producer", _Open)

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg
    ) -> NodeResult[_Out]:
        return success(_Out(text=""))


class _StrictDateNode:
    """Stands in for the weather archive: a real date or nothing."""

    spec: ClassVar[NodeSpec] = _spec("test.w28_strict", _DateIn)
    calls: int = 0

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _DateIn, config: _Cfg
    ) -> NodeResult[_Out]:
        self.calls += 1
        return success(_Out(text=inputs.date.isoformat()))


class _Handler:
    spec: ClassVar[NodeSpec] = _spec("test.w28_handler", _Open)

    def __init__(self) -> None:
        self.seen: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg
    ) -> NodeResult[_Out]:
        self.seen.append(inputs.model_dump())
        return success(_Out(text="unchecked"))


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str) -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}}}


def _definition(*, with_error_edge: bool) -> dict:
    edges = [
        {
            "id": "e1",
            "source": "p",
            "target": "s",
            "data": {"kind": "data", "mappings": {"date": "text"}},
        },
    ]
    if with_error_edge:
        edges.append({"id": "e-err", "source": "s", "target": "h", "data": {"kind": "error"}})
    nodes = [_node("p", "test.w28_producer"), _node("s", "test.w28_strict")]
    if with_error_edge:
        nodes.append(_node("h", "test.w28_handler"))
    return {"nodes": nodes, "edges": edges}


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id), emitter


async def test_input_shape_refusal_routes_along_the_error_edge():
    strict = _StrictDateNode()
    handler = _Handler()
    result, _ = await _run(
        _definition(with_error_edge=True),
        _registry(_EmptyDateProducer(), strict, handler),
        "w28-caught",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert strict.calls == 0, "the executor never ran — the refusal happened at the door"
    assert len(handler.seen) == 1
    delivered = handler.seen[0]
    assert delivered.get("code") == "ValidationError"
    assert "date" in str(delivered.get("message", ""))


async def test_input_shape_refusal_still_parks_without_a_catch():
    strict = _StrictDateNode()
    result, _ = await _run(
        _definition(with_error_edge=False), _registry(_EmptyDateProducer(), strict), "w28-parked"
    )
    assert result.status is RunStatus.ERRORED
    assert strict.calls == 0
