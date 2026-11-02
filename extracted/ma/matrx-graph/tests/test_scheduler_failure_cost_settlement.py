"""Cost settlement on a failed node carrying billed usage.

The scheduler settles a paid call's usage on the SUCCESS path only for
AGENT/LLM category nodes (avoids double-counting a pass-through node that
forwards an upstream payload's usage block verbatim). The FAILURE path has
no such forwarding risk — ``NodeError.details`` is always the failing
node's own error — so cost settlement on failure must fire whenever
``error.details.usage`` is present, REGARDLESS of node category. This
covers IO-category paid actions (e.g. ``aidream/graph_actions/page_extraction``)
that spend money via a provider call before failing.
"""

from __future__ import annotations

from typing import ClassVar

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
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


_USAGE = {
    "input_tokens": 1200,
    "output_tokens": 0,
    "total_tokens": 1200,
    "cost_usd": 0.045,
}


class _PaidIoFailExecutor:
    """A NodeCategory.IO node (like page_extraction.run) that spends money
    via a paid call and then fails — usage travels under
    ``error.details.usage`` per the documented convention."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.paid_io_fail",
        category=NodeCategory.IO,
        display_name="Paid IO node that fails after spending",
        description="Simulates a paid-but-failed extraction run.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _Input,
        config: _Config,
    ) -> NodeResult[_Output]:
        return failure(
            "extraction_failed",
            "provider call succeeded but extraction failed",
            details={"usage": _USAGE},
        )


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_PaidIoFailExecutor(), overwrite=True)
    return reg


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "test.paid_io_fail",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
        }
    )


def _events_of_kind(emitter: FakeEmitter, event: str) -> list[dict]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == event
    ]


async def test_io_category_failure_with_usage_settles_cost():
    """An IO-category node's Failure carrying details.usage MUST emit a
    node_cost event — the presence of usage is the signal money was spent,
    independent of category (2026-07-09 fix; category gate is a
    success-path-only anti-double-count guard)."""
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="io-fail-cost")

    assert result.status is RunStatus.ERRORED

    failed = _events_of_kind(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["error"]["code"] == "extraction_failed"

    cost_events = _events_of_kind(emitter, "node_cost")
    assert len(cost_events) == 1
    assert cost_events[0]["node_id"] == "n"
    assert cost_events[0]["cost_usd"] == _USAGE["cost_usd"]
    assert cost_events[0]["input_tokens"] == _USAGE["input_tokens"]
