"""ENGINE_SPEC §4.4 — two independent dispatches delivering into ONE fan-in.

Regression pack for the per-item accumulator-key COLLISION: when two distinct
dispatch groups (two sibling ``control.map`` nodes, or nested maps) deliver to
one gather over the SAME edge in the same super-step routing pass, their equal
``item_index`` values used to collide on the ``"<edge_id>@@<item_index>"`` key
— one dispatch's items silently overwrote the other's and the run completed
with partial gather output. The fix keys per-item storage AND fan-in group
membership by ``(edge_id, dispatch_id)`` so the dispatches resolve as SEPARATE
logical arrivals that aggregate into one gather firing (one dispatch = one
logical upstream, §4.4).
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import kinds as kinds_mod
from matrx_graph.kinds import KindEntry
from matrx_graph.nodes.control.gather import GatherOutput
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _WorkerInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""


class _WorkerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: str = ""


class _WorkerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _UpperWorker:
    """Uppercases each fanned item — the spy that proves every item ran."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.upper_worker",
        category=NodeCategory.DATA,
        display_name="Upper worker",
        description="Uppercases one fanned item.",
        input_schema=_WorkerInput,
        output_schema=_WorkerOutput,
        config_schema=_WorkerConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.processed: list[str] = []

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _WorkerInput,
        _config: _WorkerConfig,
    ) -> NodeResult[_WorkerOutput]:
        self.processed.append(inputs.value)
        return success(_WorkerOutput(result=inputs.value.upper()))


def _registry() -> tuple[NodeRegistry, _UpperWorker]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    worker = _UpperWorker()
    reg.register(worker, overwrite=True)
    return reg, worker


def _map_node(node_id: str, items: list[Any], target: str, payload_key: str = "value") -> dict:
    data: dict[str, Any] = {"config": {"target_node_id": target, "payload_key": payload_key}}
    # Only seed a static items list for a driver map. A map invoked via Send
    # (a nested inner map) receives its items in the Send payload — a static
    # [] here would shadow that payload and dispatch nothing.
    if items:
        data["input"] = {"items": items}
    return {
        "id": node_id,
        "type": "control.map",
        "position": {"x": 0, "y": 0},
        "data": data,
    }


def _run(definition: Definition, registry: NodeRegistry, run_id: str):
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return scheduler.run(run_id=run_id)


def _contiguous(values: list[Any], first: Any, second: Any) -> bool:
    """The two values are present and adjacent, `first` immediately before
    `second` — proves per-group ordering survived aggregation (never
    interleaved by a naive item_index sort)."""
    return first in values and second in values and values.index(first) + 1 == values.index(second)


# ---------------------------------------------------------------------------
# 1. Two sibling maps → one worker → one gather (the headline collision)
# ---------------------------------------------------------------------------


async def test_two_sibling_maps_into_one_gather_keeps_all_items():
    registry, worker = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _map_node("map1", ["a", "b"], "worker"),
                _map_node("map2", ["c", "d"], "worker"),
                {
                    "id": "worker",
                    "type": "test.upper_worker",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "gather",
                    "type": "control.gather",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_wg",
                    "source": "worker",
                    "target": "gather",
                    "data": {"mappings": {"value": "result"}},
                }
            ],
            "entry_nodes": ["map1", "map2"],
        }
    )

    result = await _run(definition, registry, "sibling-maps")

    assert result.status is RunStatus.COMPLETED
    assert sorted(worker.processed) == ["a", "b", "c", "d"]
    gather = result.last_outputs["gather"]
    values = gather["values"]
    # All four land — none silently overwritten (the bug ended ['C','D']).
    assert sorted(values) == ["A", "B", "C", "D"]
    assert gather["count"] == 4
    assert gather["expected"] == 4
    assert gather["skipped_indexes"] == []
    assert gather["holes"] == []
    # Each dispatch group stays contiguous and in-order (never index-collision
    # interleaved): A before B, C before D.
    assert _contiguous(values, "A", "B")
    assert _contiguous(values, "C", "D")


async def test_gather_engine_mode_output_validates_against_its_own_model_schema():
    """The engine's REAL emitted gather payload validates against GatherOutput.

    🚨 THIS TEST CANNOT SEE A STALE REGISTRY ROW, AND ITS OLD NAME CLAIMED IT
    COULD ("...matches_registered_gather_result_schema"). It seeds the kind
    cache from ``GatherOutput.model_json_schema()`` — the model — so it compares
    the model against the model and is green by construction no matter what
    ``content_ir.kind_definition`` actually holds. It was green through BOTH
    stale-row incidents: the 2026-08-26 enforcement pre-flight, and 2026-09-12,
    when the live row sat at v6/2026-08-23 without the three AI-projection
    fields and the Newsroom Desk run died at ``n_gather``.

    What it DOES prove, and why it stays: the engine really does fan out, really
    does reassemble, and the payload it really emits satisfies the model's own
    contract end to end (`output_kind_ok`, no `output_kind_errors`) — a genuine
    leg, just not the registry leg.

    THE REGISTRY-VS-MODEL WITNESS IS ``scripts/check_kind_registry_drift.py``
    (`--self-test` proves it can fail). Nothing in this file can replace it: a
    pytest run has no database.
    """
    kinds_mod._cache["gather_result"] = (
        time.monotonic(),
        KindEntry(
            slug="gather_result",
            version=1,
            label="gather_result",
            json_schema=GatherOutput.model_json_schema(),
        ),
    )
    try:
        registry, worker = _registry()
        definition = Definition.model_validate(
            {
                "nodes": [
                    _map_node("map1", ["a", "b"], "worker"),
                    {
                        "id": "worker",
                        "type": "test.upper_worker",
                        "position": {"x": 200, "y": 0},
                        "data": {"config": {}},
                    },
                    {
                        "id": "gather",
                        "type": "control.gather",
                        "position": {"x": 400, "y": 0},
                        "data": {"config": {}},
                    },
                ],
                "edges": [
                    {
                        "id": "e_wg",
                        "source": "worker",
                        "target": "gather",
                        "data": {"mappings": {"value": "result"}},
                    }
                ],
                "entry_nodes": ["map1"],
            }
        )
        graph = compile_graph(definition, registry=registry)
        emitter = FakeEmitter()
        scheduler = Scheduler(
            graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry
        )
        result = await scheduler.run(run_id="gather-kind-check")

        assert result.status is RunStatus.COMPLETED
        completed = [
            p
            for (m, p) in emitter.events
            if m == "data"
            and isinstance(p, dict)
            and p.get("event") == "node_completed"
            and p.get("node_id") == "gather"
        ]
        assert len(completed) == 1
        assert completed[0]["output_kind"] == "gather_result"
        assert completed[0]["output_kind_errors"] is None, completed[0]["output_kind_errors"]
        assert completed[0]["output_kind_ok"] is True
    finally:
        kinds_mod._cache.pop("gather_result", None)


# ---------------------------------------------------------------------------
# 2. Nested map [[a,b],[c]] → leaf → gather — item A must not vanish
# ---------------------------------------------------------------------------


async def test_nested_maps_into_one_gather_no_item_vanishes():
    registry, worker = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                # outer fans each SUBLIST to an inner map (payload_key='items').
                _map_node("outer", [["a", "b"], ["c"]], "inner", payload_key="items"),
                _map_node("inner", [], "leaf"),  # items arrive per-dispatch
                {
                    "id": "leaf",
                    "type": "test.upper_worker",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "gather",
                    "type": "control.gather",
                    "position": {"x": 600, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_lg",
                    "source": "leaf",
                    "target": "gather",
                    "data": {"mappings": {"value": "result"}},
                }
            ],
            "entry_nodes": ["outer"],
        }
    )

    result = await _run(definition, registry, "nested-maps")

    assert result.status is RunStatus.COMPLETED
    assert sorted(worker.processed) == ["a", "b", "c"]
    gather = result.last_outputs["gather"]
    values = gather["values"]
    # 'A' (inner-dispatch-1 index 0) used to be overwritten by 'C'
    # (inner-dispatch-2 index 0) — the collision. It must survive.
    assert "A" in values
    assert sorted(values) == ["A", "B", "C"]
    assert gather["count"] == 3
    assert gather["expected"] == 3
    assert _contiguous(values, "A", "B")


# ---------------------------------------------------------------------------
# 3. Asymmetric item counts — the per-dispatch expected count is not
#    cross-contaminated (2 items + 1 item, both resolve independently)
# ---------------------------------------------------------------------------


async def test_two_dispatches_with_different_counts_resolve_independently():
    registry, worker = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                _map_node("map1", ["a", "b"], "worker"),  # 2 items
                _map_node("map2", ["c"], "worker"),  # 1 item
                {
                    "id": "worker",
                    "type": "test.upper_worker",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "gather",
                    "type": "control.gather",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "e_wg",
                    "source": "worker",
                    "target": "gather",
                    "data": {"mappings": {"value": "result"}},
                }
            ],
            "entry_nodes": ["map1", "map2"],
        }
    )

    result = await _run(definition, registry, "asymmetric-maps")

    assert result.status is RunStatus.COMPLETED
    assert sorted(worker.processed) == ["a", "b", "c"]
    gather = result.last_outputs["gather"]
    values = gather["values"]
    # If the single-int expected count were cross-contaminated, one group
    # would never complete (deadlock/ERRORED) or drop an item. All three land.
    assert sorted(values) == ["A", "B", "C"]
    assert gather["count"] == 3
    assert gather["expected"] == 3
    assert _contiguous(values, "A", "B")
