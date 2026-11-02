"""Run variables — {'$var': name} substitution into node inputs.

The generic engine pass that delivers run-time ``initial_variables`` into ANY
node's inputs on ANY workflow:

    1. A run-time variable value lands in a node's inputs through a
       {'$var': name} reference in its authored static inputs.
    2. Precedence: run value → per-reference default → declared default.
    3. A reference with no value and no default parks the run ERRORED on
       that node (UnresolvedVariableError) — never a silent empty string.
    4. A reference to an UNDECLARED variable fails compile/validate loudly.
    5. An edge-routed value for the same key still wins over the resolved
       static value (last-writer-wins merge), and edge payloads are never
       scanned for refs.
    6. Nested refs (inside dicts/lists) resolve too.

Pattern mirrors test_scheduler_mock_response.py.
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
from matrx_graph import (
    CompilationError,
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    validate_definition,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field

from tests._fixtures import FakeEmitter, make_app_context


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")
    topic: str = Field(default="<unset>")
    extras: dict[str, Any] = Field(default_factory=dict)


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic: str = ""
    extras: dict[str, Any] = Field(default_factory=dict)


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


_received: list[dict[str, Any]] = []


class _EchoExecutor:
    """Records the exact inputs the scheduler delivered."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.var_echo",
        category=NodeCategory.DATA,
        display_name="Var echo",
        description="Echoes its inputs so tests can assert what arrived.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        _received.append(inputs.model_dump())
        return success(_Output(topic=inputs.topic, extras=inputs.extras))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_EchoExecutor(), overwrite=True)
    return reg


def _definition(
    static_input: dict[str, Any],
    variables: list[dict[str, Any]] | None = None,
    second_node: bool = False,
) -> Definition:
    nodes: list[dict[str, Any]] = [
        {
            "id": "echo",
            "type": "test.var_echo",
            "position": {"x": 0, "y": 0},
            "data": {"config": {}, "input": static_input},
        }
    ]
    edges: list[dict[str, Any]] = []
    if second_node:
        nodes.append(
            {
                "id": "echo2",
                "type": "test.var_echo",
                "position": {"x": 200, "y": 0},
                "data": {"config": {}, "input": static_input},
            }
        )
        edges.append(
            {
                "id": "e1",
                "source": "echo",
                "target": "echo2",
                "data": {"kind": "data", "mappings": {"topic": "topic"}},
            }
        )
    return Definition.model_validate(
        {
            "nodes": nodes,
            "edges": edges,
            "variables": variables or [],
        }
    )


async def test_run_variable_lands_in_node_inputs():
    """The core promise: a run-time initial_variables value reaches the node."""
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition({"topic": {"$var": "topic"}}, variables=[{"name": "topic"}]),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter(), initial_variables={"topic": "Photosynthesis"}),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-basic")
    assert result.status is RunStatus.COMPLETED
    assert _received[0]["topic"] == "Photosynthesis"
    assert result.last_outputs["echo"]["topic"] == "Photosynthesis"


async def test_nested_ref_resolves():
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(
            {"extras": {"meta": [{"$var": "topic"}], "plain": 1}},
            variables=[{"name": "topic"}],
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter(), initial_variables={"topic": "Mitosis"}),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-nested")
    assert result.status is RunStatus.COMPLETED
    assert _received[0]["extras"] == {"meta": ["Mitosis"], "plain": 1}


async def test_declared_default_applies_when_run_value_absent():
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(
            {"topic": {"$var": "topic"}},
            variables=[{"name": "topic", "default": "General Science"}],
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-default")
    assert result.status is RunStatus.COMPLETED
    assert _received[0]["topic"] == "General Science"


async def test_per_reference_default_beats_declared_default():
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(
            {"topic": {"$var": "topic", "default": "Ref Default"}},
            variables=[{"name": "topic", "default": "Declared Default"}],
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-ref-default")
    assert result.status is RunStatus.COMPLETED
    assert _received[0]["topic"] == "Ref Default"


async def test_missing_variable_with_no_default_parks_awaiting_input():
    """No value, no default → the run parks AWAITING_INPUT at the start gate
    (INPUT-SURFACE.md park-not-die: declared variables fold into the input
    surface; a referenced one with no default is a require input). Never a
    silent empty string, never a crash — supply the value and resume."""
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition({"topic": {"$var": "topic"}}, variables=[{"name": "topic"}]),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-missing")
    assert result.status is RunStatus.AWAITING_INPUT
    assert result.interrupt is not None
    assert [m["name"] for m in result.interrupt["missing"]] == ["topic"]
    assert _received == []  # executor never ran


async def test_undeclared_reference_fails_validation_and_compile():
    definition = _definition({"topic": {"$var": "topci"}}, variables=[{"name": "topic"}])
    result = validate_definition(definition, registry=_registry())
    assert not result.valid
    assert any("topci" in issue.message for issue in result.issues)
    # Did-you-mean points at the declared variable.
    assert any("topic" in issue.message for issue in result.issues)
    with pytest.raises(CompilationError):
        compile_graph(definition, registry=_registry())


async def test_edge_value_still_wins_over_resolved_static():
    """Edge-routed payloads overlay resolved static inputs (last-writer-wins),
    and edge payloads themselves are never scanned for refs."""
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(
            {"topic": {"$var": "topic"}},
            variables=[{"name": "topic"}],
            second_node=True,
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter(), initial_variables={"topic": "Static Wins?"}),
        registry=registry,
    )
    result = await scheduler.run(
        run_id="vars-edge",
        node_inputs={"echo": {"topic": "Seeded"}},
    )
    assert result.status is RunStatus.COMPLETED
    # Entry node: seeded value overlays the resolved static ref.
    assert _received[0]["topic"] == "Seeded"
    # Downstream node: edge-routed output overlays its own static ref.
    assert _received[1]["topic"] == "Seeded"


async def test_literal_dict_without_var_key_untouched():
    """Only {'$var': ...}-shaped dicts are references; other dicts pass through."""
    _received.clear()
    registry = _registry()
    graph = compile_graph(
        _definition(
            {"extras": {"$vars": "not-a-ref", "keep": True}},
            variables=[],
        ),
        registry=registry,
    )
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="vars-literal")
    assert result.status is RunStatus.COMPLETED
    assert _received[0]["extras"] == {"$vars": "not-a-ref", "keep": True}
