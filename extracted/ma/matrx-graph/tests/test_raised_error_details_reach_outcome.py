"""Structured context a host attaches to a raised exception lands on the failed outcome.

MKT-058 (2026-10-14): a step that raised after making provider calls stored ``output={}`` and an
error with no details, so its request ledger was gone. A host attaches ``node_error_details`` to the
exception on its way out; the engine folds it into ``node_outcome.error.details``.
"""

from __future__ import annotations

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
from matrx_graph.types.result import NodeResult
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _RaisingNode:
    spec = NodeSpec(
        type="test.raises_with_details",
        category=NodeCategory.DATA,
        display_name="Fetch",
        description="raises after recording calls",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.SIDE_EFFECT,
        retry=RetryPolicy(max_attempts=1),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        exc = RuntimeError("provider refused")
        exc.node_error_details = {"requests": [{"seq": 1, "status": 401}]}  # type: ignore[attr-defined]
        raise exc


async def test_raised_node_error_details_land_on_the_failed_outcome():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_RaisingNode(), overwrite=True)
    definition = {
        "nodes": [{"id": "fetch", "type": "test.raises_with_details", "position": {"x": 0, "y": 0},
                   "data": {"label": "Fetch", "config": {}}}],
        "edges": [],
    }
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="raised-details")
    assert result.status is RunStatus.ERRORED
    outcome = await scheduler.checkpointer.get_outcome(run_id="raised-details", step=0, node_id="fetch", attempt=1)
    assert outcome is not None and outcome.error is not None
    assert outcome.error["details"]["requests"] == [{"seq": 1, "status": 401}]
