"""An 'Only when' gate hands its step only the names the step takes — at any position in the run.

2026-11-09 (L7e, search workflow 79c58b1f): the gate (``<step>~when``) forwards everything its condition
reads; a closed step (``extra="forbid"``) in the MIDDLE of the run refused the names only the condition read
(the reserve step got ``on``, the YouTube calls ``granted`` / ``ids`` → extra_forbidden). The engine trimmed
this only for a gate at the start of the run. And validation said nothing about a whole-output connection
handing a closed step fields it does not declare.

Red before: the run below failed on ``on``; the validation warning did not exist.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    ActionRegistry,
    ActionTier,
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_node,
)
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from tests._fixtures import make_app_context


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Found(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[str] = []
    on: bool = False


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[str] = []


class _Count(BaseModel):
    model_config = ConfigDict(extra="forbid")
    count: int = 0


def _registry() -> NodeRegistry:
    from matrx_graph.nodes import register_builtin_nodes

    nreg, areg = register_builtin_nodes(NodeRegistry()), ActionRegistry()

    @register_node(name="test.finds", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_Open, output_schema=_Found, node_registry=nreg, action_registry=areg)
    async def _finds(_ctx, inputs: _Open) -> NodeResult[_Found]:
        return success(_Found(items=["a", "b"], on=True))

    @register_node(name="test.strict_count", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_Strict, output_schema=_Count, node_registry=nreg, action_registry=areg)
    async def _count(_ctx, inputs: _Strict) -> NodeResult[_Count]:
        return success(_Count(count=len(inputs.items)))

    return nreg


def _definition(*, when: bool = True, mappings: dict | None = None) -> Definition:
    edge: dict = {"id": "e", "source": "find", "target": "count", "data": {"kind": "data"}}
    if mappings is not None:
        edge["data"]["mappings"] = mappings
    return Definition.model_validate({
        "nodes": [
            {"id": "find", "type": "test.finds", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "count", "type": "test.strict_count", "position": {"x": 100, "y": 0},
             "data": {"when": "inputs['on']"} if when else {}},
        ],
        "edges": [edge],
    })


async def test_a_gate_in_the_middle_hands_its_closed_step_only_what_it_takes() -> None:
    nreg = _registry()
    result = await Scheduler(
        compile_graph(_definition(mappings={"items": "items", "on": "on"}), registry=nreg),
        MemoryCheckpointer(), make_app_context(), registry=nreg,
    ).run(run_id="gate-mid", inputs={})
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["count"]["count"] == 2


def test_a_whole_output_connection_into_a_closed_step_warns_about_fields_it_does_not_take() -> None:
    nreg = _registry()
    issues = validate_definition(_definition(when=False), registry=nreg).issues
    warned = [i for i in issues if i.edge_id == "e" and "does not take" in i.message]
    assert warned and "on" in warned[0].message, [i.message for i in issues]
    # Field links that map only what the step takes: no such warning.
    issues = validate_definition(_definition(when=False, mappings={"items": "items"}), registry=nreg).issues
    assert not [i for i in issues if "does not take" in i.message]
