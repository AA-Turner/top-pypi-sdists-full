"""Ceiling interaction — max_total_invocations vs control.map's max_dispatches.

scheduler.py documents the relationship: the run-wide invocation budget
(DEFAULT_MAX_TOTAL_INVOCATIONS = 25_000) must sit comfortably ABOVE the
largest single legal dispatch (control.map's le=10_000 ceiling) plus its
surrounding graph, or a previously-legal max-size map regresses to FAILED.
That relationship was documented but never proven. These tests run it for
real: a genuine 10_000-item map inside the default budget COMPLETES with
all 10_000 child executions accounted for; an over-budget run terminates
with the NAMED ExecutionError (never a hang, never a silent truncation).
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
from matrx_graph.executor.scheduler import DEFAULT_MAX_TOTAL_INVOCATIONS

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _ItemWorker:
    """Trivial per-item worker: records each received item value."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.item_worker",
        category=NodeCategory.DATA,
        display_name="Item worker",
        description="Echoes one mapped item.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.seen: list[int] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _AnyIO, _config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        value = int(inputs.model_dump(mode="json")["value"])
        self.seen.append(value)
        return success(_AnyIO(value=value))


def _map_definition(n_items: int, *, max_dispatches: int) -> Definition:
    return Definition.model_validate(
        {
            "entry_nodes": ["fan"],
            "nodes": [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "target_node_id": "worker",
                            "max_dispatches": max_dispatches,
                        },
                        "input": {"items": list(range(n_items))},
                    },
                },
                {
                    "id": "worker",
                    "type": "test.item_worker",
                    "position": {"x": 200, "y": 0},
                    "data": {},
                },
            ],
            "edges": [],
        }
    )


def _make_scheduler(definition: Definition) -> tuple[Scheduler, _ItemWorker]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = _ItemWorker()
    reg.register(worker, overwrite=True)
    graph = compile_graph(definition, registry=reg)
    return (
        Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg),
        worker,
    )


def test_documented_headroom_relationship_holds() -> None:
    """The invariant the docstring at scheduler.py promises: the run-wide
    default budget clears the largest legal single map dispatch with room
    for the surrounding graph. If someone lowers the default below 10k,
    this fails BEFORE a production max-size map regresses to FAILED."""
    assert DEFAULT_MAX_TOTAL_INVOCATIONS > 10_000
    assert DEFAULT_MAX_TOTAL_INVOCATIONS == 25_000


async def test_max_size_map_completes_inside_default_budget() -> None:
    """A REAL 10_000-item map (the node's own le=10_000 ceiling) under the
    default 25k run budget: every one of the 10_000 children must actually
    execute — the recorded item multiset is exactly 0..9999 — and the run
    COMPLETES. Only genuine dispatch + execution of all ten thousand
    invocations can produce that multiset."""
    scheduler, worker = _make_scheduler(_map_definition(10_000, max_dispatches=10_000))

    result = await scheduler.run(run_id="run-map-10k", max_steps=50)

    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["fan"]["dispatched"] == 10_000
    assert len(worker.seen) == 10_000
    assert sorted(worker.seen) == list(range(10_000))


async def test_over_budget_run_fails_with_named_error_not_a_hang() -> None:
    """400 dispatches against an explicit max_total_invocations=100: the
    run must terminate in the NAMED budget error — naming the cap and the
    remediation — with status FAILED, never a hang and never a silent
    partial completion presented as success."""
    scheduler, worker = _make_scheduler(_map_definition(400, max_dispatches=1000))

    result = await scheduler.run(
        run_id="run-map-overbudget", max_steps=50, max_total_invocations=100
    )

    assert result.status is RunStatus.FAILED
    assert result.error is not None
    assert "max_total_invocations=100" in result.error
    assert "raise the cap deliberately" in result.error.lower()
    # Terminal, not partial-success: far fewer than 400 children ran, and
    # the run said FAILED — nothing pretended the fan-out finished.
    assert len(worker.seen) < 400


async def test_map_over_its_own_dispatch_cap_fails_the_node_loudly() -> None:
    """The OTHER ceiling: a list larger than max_dispatches fails the map
    node itself with its named error before any child dispatches."""
    scheduler, worker = _make_scheduler(_map_definition(51, max_dispatches=50))

    result = await scheduler.run(run_id="run-map-overcap", max_steps=50)

    assert result.status is not RunStatus.COMPLETED
    assert result.error is not None
    assert "max_dispatches=50" in result.error
    assert worker.seen == []  # nothing dispatched — the cap fired first
