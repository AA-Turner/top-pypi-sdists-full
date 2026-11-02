"""A mandate-candidate workflow run executes PURE and agent nodes only.

PLAN.md (common-docs/systems/intelligence/mandates/projects/mandate-candidates) item C1: under the
``mandate_candidate`` marker the scheduler runs PURE nodes and agent/LLM nodes
(their tool calls are contained by matrx-ai one by one); any other node ends
the run TERMINALLY before it executes, recorded the same way a stopped tool
call is (the shared ledger's ``stopped_at`` + a ``stopped`` disposition).
Real Scheduler, in-memory checkpointer, a counting side-effect node.
"""

from __future__ import annotations

import dataclasses
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
from matrx_graph.types import HandleDirection, HandleSpec, NodeCategory, NodeSpec
from matrx_graph.types.primitives import ActionTier
from matrx_graph.types.result import success
from tests._fixtures import FakeEmitter, make_app_context

MARKER = {
    "candidate_id": "11111111-1111-1111-1111-111111111111",
    "candidate_run_id": "22222222-2222-2222-2222-222222222222",
    "live_request_id": "33333333-3333-3333-3333-333333333333",
}

WRITES: list[Any] = []


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    wrote: bool = True


class _SideEffectExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.writes_something",
        category=NodeCategory.DATA,
        display_name="Writes something",
        input_schema=_In,
        output_schema=_Out,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.SIDE_EFFECT,
    )

    async def execute(self, ctx: Any, inputs: Any, config: Any) -> Any:
        WRITES.append(inputs)
        return success(_Out())


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_SideEffectExecutor())
    return reg


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "'ALPHA'"}},
                },
                {"id": "b", "type": "test.writes_something", "position": {"x": 200, "y": 0}},
            ],
            "edges": [{"id": "e1", "source": "a", "target": "b"}],
        }
    )


def _candidate_app(emitter: FakeEmitter) -> Any:
    try:
        from matrx_graph.candidate import candidate_context_metadata

        metadata = candidate_context_metadata(MARKER)
    except ImportError:
        metadata = {"mandate_candidate": dict(MARKER)}
    return dataclasses.replace(make_app_context(emitter), metadata=metadata)


async def test_candidate_run_stops_before_a_side_effect_node() -> None:
    WRITES.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    emitter = FakeEmitter()
    app = _candidate_app(emitter)

    result = await Scheduler(graph, MemoryCheckpointer(), app, registry=registry).run(
        run_id="candidate-gate-1"
    )

    assert WRITES == [], "a side-effect node executed inside a candidate run"
    assert result.status is RunStatus.CANCELLED
    stop = getattr(result, "candidate_stopped", None)
    assert stop is not None and stop["tool"] == "test.writes_something"
    assert stop["class"] == "workflow_node:side_effect"
    assert stop["args"]["node_id"] == "b"
    ledger = app.metadata["mandate_candidate_containment"]
    assert ledger["stopped_at"] == stop
    assert ledger["tool_dispositions"][-1]["disposition"] == "stopped"
    # The PURE node before it ran.
    assert "a" in result.last_outputs
    cancelled = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_cancelled"
    ]
    assert cancelled and cancelled[-1]["reason"] == "candidate_stopped"


async def test_without_the_marker_the_same_graph_runs_to_completion() -> None:
    WRITES.clear()
    registry = _registry()
    graph = compile_graph(_definition(), registry=registry)
    result = await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    ).run(run_id="candidate-gate-2")
    assert result.status is RunStatus.COMPLETED
    assert len(WRITES) == 1
    assert getattr(result, "candidate_stopped", None) is None


# ── The named allow-list (chair ruling 2026-09-30) ───────────────────────────


class _FakeRecordGateway:
    """Read-only by protocol: the four read methods and nothing else."""

    async def describe_entity(self, entity_type: str) -> Any:
        from matrx_graph.records import RecordEntity

        return RecordEntity(entity_type=entity_type, schema_name="demo", table_name="thing")

    async def known_entity_types(self) -> list[str]:
        return ["demo_thing"]

    async def may_read(self, *, actor_id: str, entity_type: str, record_id: str) -> bool:
        return True

    async def read_row(self, *, entity: Any, record_id: str) -> dict[str, Any]:
        return {"id": record_id, "name": "Thing"}


def _allow_listed_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "fan",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["a", "b"]},
                    },
                },
                {
                    "id": "route",
                    "type": "control.send",
                    "position": {"x": 0, "y": 100},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["c"]},
                    },
                },
                {
                    "id": "worker",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "'W'"}},
                },
                {
                    "id": "read",
                    "type": "data.read_record",
                    "position": {"x": 0, "y": 200},
                    "data": {"input": {"entity_type": "demo_thing", "record_id": "r-1"}},
                },
                {
                    "id": "show",
                    "type": "output.to_frontend",
                    "position": {"x": 200, "y": 200},
                    "data": {"config": {"mode": "full"}},
                },
            ],
            "edges": [{"id": "e1", "source": "read", "target": "show"}],
        }
    )


async def test_allow_listed_nodes_run_to_completion_under_the_marker() -> None:
    from matrx_graph.records import configure_record_gateway

    registry = _registry()
    graph = compile_graph(_allow_listed_definition(), registry=registry)
    app = _candidate_app(FakeEmitter())
    configure_record_gateway(_FakeRecordGateway())
    try:
        result = await Scheduler(graph, MemoryCheckpointer(), app, registry=registry).run(
            run_id="candidate-gate-allow"
        )
    finally:
        configure_record_gateway(None)
    assert getattr(result, "candidate_stopped", None) is None, result.candidate_stopped
    assert result.status is RunStatus.COMPLETED, (result.status, result.error)
    assert app.metadata["mandate_candidate_containment"]["stopped_at"] is None
    assert {"fan", "route", "worker", "read", "show"} <= set(result.last_outputs)


def test_every_allow_listed_node_is_named_with_a_reason() -> None:
    from matrx_graph.candidate import CANDIDATE_ALLOWED_NODE_TYPES

    assert set(CANDIDATE_ALLOWED_NODE_TYPES) == {
        "control.send",
        "control.map",
        "output.to_frontend",
        "data.read_record",
        "http.get",
    }
    assert all(len(reason) > 20 for reason in CANDIDATE_ALLOWED_NODE_TYPES.values())


async def test_a_data_write_node_still_stops() -> None:
    """log.record writes a row — not on the allow-list, so it stops the run."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "note",
                    "type": "log.record",
                    "position": {"x": 0, "y": 0},
                    "data": {"input": {"label": "x", "message": "y"}},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    app = _candidate_app(FakeEmitter())
    result = await Scheduler(graph, MemoryCheckpointer(), app, registry=registry).run(
        run_id="candidate-gate-write"
    )
    assert result.status is RunStatus.CANCELLED
    assert result.candidate_stopped["tool"] == "log.record"
    assert "allow-list" in result.candidate_stopped["reason"]
