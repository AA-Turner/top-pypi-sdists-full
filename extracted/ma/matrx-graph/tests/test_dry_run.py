"""ENGINE_SPEC §8 — dry-run: a formally distinct, synchronous, ZERO-side-effect mode.

``matrx_graph.dry_run(...)`` resolves the compiled graph topologically and
computes every node's would-be state (Ready | Blocked + missing-binding list
| unknowable), validates static inputs + edge mappings against schemas AND
the caller-supplied per-node samples (the host passes §7 slot data), and
returns a fully typed ``DryRunReport``:

  * a dot-path that misses the SAMPLE is a warning;
  * one that misses the (closed) SCHEMA is an error;
  * NO checkpointer, NO executor call, NO Send dispatch — pure computation.
"""

from __future__ import annotations

import inspect
from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    DryRunSample,
    NodeRegistry,
    compile_graph,
    dry_run,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult
from pydantic import BaseModel, ConfigDict, Field


class _ClosedInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _ClosedOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: Any = Field(default=None)
    count: int = 0


class _ClosedConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _ExplodingExecutor:
    """execute() must NEVER be reached by a dry run (§8 zero side effects)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.closed_output",
        category=NodeCategory.DATA,
        display_name="Closed-output node",
        description="Output schema is closed (extra=forbid).",
        input_schema=_ClosedInput,
        output_schema=_ClosedOutput,
        config_schema=_ClosedConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.executions = 0

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _ClosedInput, _config: _ClosedConfig
    ) -> NodeResult[_ClosedOutput]:
        self.executions += 1
        raise AssertionError("dry_run must NEVER invoke an executor (§8)")


def _registry() -> tuple[NodeRegistry, _ExplodingExecutor]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    spy = _ExplodingExecutor()
    reg.register(spy)
    return reg, spy


def _chain(mappings: dict[str, str] | None = None) -> dict[str, Any]:
    """a (closed-output source) → b (transform)."""
    edge: dict[str, Any] = {"id": "e1", "source": "a", "target": "b"}
    if mappings is not None:
        edge["data"] = {"mappings": mappings}
    return {
        "nodes": [
            {
                "id": "a",
                "type": "test.closed_output",
                "position": {"x": 0, "y": 0},
                "data": {},
            },
            {
                "id": "b",
                "type": "data.transform",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"expression": "inputs['value']"}},
            },
        ],
        "edges": [edge],
    }


def test_dry_run_no_samples_reports_blocked_with_missing_bindings() -> None:
    registry, spy = _registry()
    graph = compile_graph(Definition.model_validate(_chain({"value": "result"})), registry=registry)
    report = dry_run(graph, registry=registry)

    assert report.nodes["a"].state == "ready"  # entry node
    assert report.nodes["b"].state == "blocked"
    assert [m.edge_id for m in report.nodes["b"].missing_required] == ["e1"]
    assert report.nodes["b"].missing_required[0].reason == "no_source_data"
    assert report.edges["e1"].state == "unsatisfied"
    assert report.ok is True  # blocked-awaiting-data is informational, not an error
    assert spy.executions == 0


def test_dry_run_with_sample_computes_ready_and_preview() -> None:
    registry, spy = _registry()
    graph = compile_graph(Definition.model_validate(_chain({"value": "result"})), registry=registry)
    report = dry_run(
        graph,
        samples={"a": DryRunSample(value={"result": 7, "count": 1}, slot="declared_sample")},
        registry=registry,
    )

    assert report.nodes["b"].state == "ready"
    assert report.nodes["b"].missing_required == []
    assert report.nodes["b"].would_receive == {"value": 7}
    assert report.edges["e1"].state == "satisfied"
    assert report.edges["e1"].slot_used == "declared_sample"
    assert report.ok is True
    assert spy.executions == 0


def test_dry_run_mapping_missing_from_closed_schema_is_error() -> None:
    """A source key absent from the upstream's CLOSED declared schema (and
    from the sample) can never resolve — error, ok=False.

    Such a definition no longer COMPILES (validate_definition rejects the
    source path outright — see ``test_unknown_source_path_on_closed_schema_is_rejected``),
    so the graph here is built valid and its edge mapping swapped afterwards:
    definitions saved before that gate existed still reach dry_run.
    """
    registry, _spy = _registry()
    graph = compile_graph(
        Definition.model_validate(_chain({"value": "result"})), registry=registry
    )
    edge = graph.edges["e1"]
    graph = graph.model_copy(
        update={"edges": {"e1": edge.model_copy(update={"mappings": {"value": "nonexistent"}})}}
    )
    report = dry_run(
        graph,
        samples={"a": DryRunSample(value={"result": 7}, slot="last_test_output")},
        registry=registry,
    )

    issues = report.nodes["b"].mapping_issues
    assert any(i.severity == "error" and i.source_key == "nonexistent" for i in issues)
    assert report.ok is False
    assert report.errors
    assert any(m.reason == "mapping_unresolvable" for m in report.nodes["b"].missing_required)


def test_dry_run_mapping_missing_from_sample_only_is_warning() -> None:
    """The first path segment IS in the declared schema but the sample can't
    resolve the full dot-path — warning, still ok (spec §8)."""
    registry, _spy = _registry()
    graph = compile_graph(
        Definition.model_validate(_chain({"value": "result.deep"})), registry=registry
    )
    report = dry_run(
        graph,
        samples={"a": DryRunSample(value={"result": 7}, slot="last_live_output")},
        registry=registry,
    )

    issues = report.nodes["b"].mapping_issues
    assert any(i.severity == "warning" and i.source_key == "result.deep" for i in issues)
    assert report.ok is True
    assert report.warnings


def test_dry_run_var_missing_blocks_entry_node() -> None:
    registry, _spy = _registry()
    data = {
        "variables": [{"name": "topic"}],  # declared, NO default
        "nodes": [
            {
                "id": "a",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"expression": "inputs['topic']"},
                    "input": {"topic": {"$var": "topic"}},
                },
            }
        ],
        "edges": [],
    }
    graph = compile_graph(Definition.model_validate(data), registry=registry)

    report = dry_run(graph, registry=registry)
    assert report.nodes["a"].state == "blocked"
    assert any(m.reason == "var_missing" for m in report.nodes["a"].missing_required)

    supplied = dry_run(graph, variables={"topic": "cats"}, registry=registry)
    assert supplied.nodes["a"].state == "ready"
    assert supplied.nodes["a"].would_receive == {"topic": "cats"}


def test_dry_run_send_target_is_unknowable() -> None:
    """A node with no inbound edges that is NOT a declared entry can only be
    reached dynamically (Send) — its readiness is statically unknowable."""
    registry, _spy = _registry()
    data = {
        "entry_nodes": ["m"],
        "nodes": [
            {
                "id": "m",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"target_node_id": "w"}},
            },
            {
                "id": "w",
                "type": "data.transform",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"expression": "inputs['value']"}},
            },
        ],
        "edges": [],
    }
    graph = compile_graph(Definition.model_validate(data), registry=registry)
    report = dry_run(graph, registry=registry)
    assert report.nodes["m"].state == "ready"
    assert report.nodes["w"].state == "unknowable"


def test_dry_run_validates_routed_inputs_against_input_schema() -> None:
    """§8: static+routed inputs are validated against the target's input
    schema — a sample-derived preview that violates it is surfaced."""
    registry, _spy = _registry()
    data = {
        "nodes": [
            {
                "id": "a",
                "type": "test.closed_output",
                "position": {"x": 0, "y": 0},
                "data": {},
            },
            {
                "id": "m",
                "type": "control.map",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"target_node_id": "a"}},
            },
        ],
        "edges": [
            # map.items must be a LIST; the sample delivers an int.
            {
                "id": "e1",
                "source": "a",
                "target": "m",
                "data": {"mappings": {"items": "result"}},
            }
        ],
    }
    graph = compile_graph(Definition.model_validate(data), registry=registry)
    report = dry_run(
        graph,
        samples={"a": DryRunSample(value={"result": 7}, slot="declared_sample")},
        registry=registry,
    )
    assert report.nodes["m"].state == "ready"
    assert report.nodes["m"].diagnostics  # items=7 violates list[Any]
    assert any("items" in d for d in report.nodes["m"].diagnostics)


def test_dry_run_is_structurally_pure() -> None:
    """§8 zero side effects, enforced at the SIGNATURE level: the engine
    function cannot even receive a checkpointer/emitter/store — and the spy
    executor proves no execute() call happened across every test above."""
    params = set(inspect.signature(dry_run).parameters)
    assert "checkpointer" not in params
    assert "emitter" not in params
    assert params <= {"graph", "inputs", "node_inputs", "variables", "samples", "registry"}
