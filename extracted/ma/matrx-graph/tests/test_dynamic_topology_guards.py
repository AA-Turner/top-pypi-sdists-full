"""Dynamic-topology hardening guards.

Three sharp edges around dynamic fan-out, each formerly a silent or
crash-shaped failure:

1. ``validate_definition`` badges a dispatcher whose ``target_node_id`` names
   a node that is not on the canvas (formerly compiled clean, KeyError'd at
   runtime) — and a dispatcher that targets itself.
2. A runtime ``ctx.send`` to an unknown target is a framework
   ``ExecutionError`` → terminal FAILED with the dispatching node named
   (formerly a bare KeyError out of ``_route_outputs``).
3. ``max_total_invocations`` bounds run WIDTH — total invocations scheduled
   in one drive segment — where ``max_steps`` only bounds depth.
"""

from __future__ import annotations

from typing import Any, ClassVar
from uuid import uuid4

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
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _RogueSender:
    """Sends one payload to a target that is not on the graph."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.rogue_sender",
        category=NodeCategory.CONTROL,
        display_name="Rogue sender",
        description="ctx.send to a nonexistent node.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        dynamic_output=True,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _AnyIO, config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        ctx.send("no_such_node", {"value": 1})
        return success(_AnyIO())


class _Echo:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.echo_guard",
        category=NodeCategory.DATA,
        display_name="Echo",
        description="Echoes inputs.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _AnyIO, _config: _NoConfig
    ) -> NodeResult[_AnyIO]:
        return success(_AnyIO(**inputs.model_dump(mode="json")))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_RogueSender(), overwrite=True)
    reg.register(_Echo(), overwrite=True)
    return reg


def _scheduler(definition: Definition, registry: NodeRegistry) -> Scheduler:
    graph = compile_graph(definition, registry=registry)
    return Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )


# ---------------------------------------------------------------------------
# 1. validate_definition — dispatch-target checks
# ---------------------------------------------------------------------------


def _map_def(target: str) -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": "fanout",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": target},
                    "input": {"items": [1, 2]},
                },
            },
            {
                "id": "worker",
                "type": "test.echo_guard",
                "position": {"x": 200, "y": 0},
                "data": {"config": {}},
            },
        ],
        "edges": [],
        "entry_nodes": ["fanout"],
    }


def test_validate_flags_unknown_dispatch_target():
    result = validate_definition(_map_def("wroker"), registry=_registry())
    assert not result.valid
    hits = [i for i in result.issues if "target_node_id" in i.path]
    assert hits, result.issues
    assert hits[0].node_id == "fanout"
    assert "wroker" in hits[0].message
    # Closest-match hint names the real node.
    assert "worker" in hits[0].message


def test_validate_flags_self_target():
    result = validate_definition(_map_def("fanout"), registry=_registry())
    assert not result.valid
    hits = [i for i in result.issues if "targets itself" in i.message]
    assert hits and hits[0].node_id == "fanout"


def test_validate_accepts_valid_dispatch_target():
    result = validate_definition(_map_def("worker"), registry=_registry())
    target_issues = [i for i in result.issues if "target_node_id" in i.path]
    assert not target_issues, target_issues


# ---------------------------------------------------------------------------
# 2. Runtime Send to unknown target — typed failure, dispatcher named
# ---------------------------------------------------------------------------


async def test_runtime_send_to_unknown_target_fails_run_with_named_dispatcher():
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "rogue",
                    "type": "test.rogue_sender",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
            "entry_nodes": ["rogue"],
        }
    )
    scheduler = _scheduler(definition, _registry())
    result = await scheduler.run(run_id=str(uuid4()))
    assert result.status is RunStatus.FAILED
    assert result.error is not None
    assert "rogue" in result.error
    assert "no_such_node" in result.error
    assert "KeyError" not in result.error


# ---------------------------------------------------------------------------
# 3. max_total_invocations — width guard
# ---------------------------------------------------------------------------


async def test_width_cap_fails_oversized_fanout():
    definition = Definition.model_validate(_map_def("worker"))
    definition = definition.model_copy(
        update={
            "nodes": [
                n.model_copy(
                    update={
                        "data": {
                            **n.data,
                            "input": {"items": list(range(20))},
                        }
                    }
                )
                if n.id == "fanout"
                else n
                for n in definition.nodes
            ]
        }
    )
    scheduler = _scheduler(definition, _registry())
    result = await scheduler.run(run_id=str(uuid4()), max_total_invocations=5)
    assert result.status is RunStatus.FAILED
    assert result.error is not None
    assert "max_total_invocations" in result.error


async def test_width_cap_default_allows_normal_runs():
    definition = Definition.model_validate(_map_def("worker"))
    scheduler = _scheduler(definition, _registry())
    result = await scheduler.run(run_id=str(uuid4()))
    assert result.status is RunStatus.COMPLETED
