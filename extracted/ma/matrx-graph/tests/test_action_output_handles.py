"""@register_node(extra_output_handles=...) — declared emission handles.

A branching ACTION (ctx.emit on named handles) must be able to declare those
handles on its NodeSpec, or validate_definition rejects every authored edge
that uses them as sourceHandle.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph.actions import register_node
from matrx_graph.actions.registry import ActionRegistry
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.definition import Definition, EdgeDef, NodeDef, Position
from matrx_graph.types.handle import HandleDirection
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool = True


def _register(registry: NodeRegistry) -> None:
    @register_node(
        name="testing.branchy_action",
        description="test action with named emission handles",
        input_schema=_In,
        output_schema=_Out,
        extra_output_handles=("yes", "no"),
        node_registry=registry,
        action_registry=ActionRegistry(),
        overwrite=True,
    )
    async def branchy(ctx: NodeExecutionContext, inputs: _In) -> NodeResult[_Out]:
        ctx.emit("yes", {})
        return success(_Out())

    @register_node(
        name="testing.sink_action",
        description="test sink",
        input_schema=_In,
        output_schema=_Out,
        node_registry=registry,
        action_registry=ActionRegistry(),
        overwrite=True,
    )
    async def sink(ctx: NodeExecutionContext, inputs: _In) -> NodeResult[_Out]:
        return success(_Out())


def test_extra_output_handles_are_declared_on_the_spec() -> None:
    registry = NodeRegistry()
    _register(registry)
    spec = registry.get("testing.branchy_action").spec
    outs = {h.id for h in spec.handles if h.direction == HandleDirection.OUTPUT}
    assert outs == {"out", "yes", "no"}


def test_edges_may_reference_declared_emission_handles() -> None:
    registry = NodeRegistry()
    _register(registry)
    definition = Definition(
        nodes=[
            NodeDef(id="a", type="testing.branchy_action", position=Position(x=0, y=0)),
            NodeDef(id="b", type="testing.sink_action", position=Position(x=100, y=0)),
            NodeDef(id="c", type="testing.sink_action", position=Position(x=100, y=100)),
        ],
        edges=[
            EdgeDef(id="e1", source="a", target="b", sourceHandle="yes", data={"kind": "data"}),
            EdgeDef(id="e2", source="a", target="c", sourceHandle="no", data={"kind": "data"}),
        ],
        entry_nodes=["a"],
    )
    result = validate_definition(definition, registry)
    handle_errors = [issue for issue in result.issues if "sourceHandle" in (issue.path or "")]
    assert handle_errors == []


def test_undeclared_source_handle_still_fails() -> None:
    registry = NodeRegistry()
    _register(registry)
    definition = Definition(
        nodes=[
            NodeDef(id="a", type="testing.branchy_action", position=Position(x=0, y=0)),
            NodeDef(id="b", type="testing.sink_action", position=Position(x=100, y=0)),
        ],
        edges=[
            EdgeDef(id="e1", source="a", target="b", sourceHandle="maybe", data={"kind": "data"}),
        ],
        entry_nodes=["a"],
    )
    result = validate_definition(definition, registry)
    assert any("sourceHandle" in (issue.path or "") for issue in result.issues)
