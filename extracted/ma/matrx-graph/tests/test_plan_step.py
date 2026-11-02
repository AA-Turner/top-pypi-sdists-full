"""plan.step — the Plan Node primitive's engine behavior.

Proves the three standalone/resolver modes from docs/workflow/PLAN_NODE_DESIGN.md:
junction pass-through (sketch plan), stand-in substitution (pinned sample),
resolver delegation incl. the production refusal posture. Real scheduler runs,
in-memory checkpointer — no mocks of the system under test.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph import MemoryCheckpointer, compile_graph
from matrx_graph.contracts import ConformanceState, audit_registry
from matrx_graph.executor.scheduler import Scheduler
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.nodes.plan.step import set_plan_resolver
from matrx_graph.types.definition import Definition

from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture()
def registry() -> NodeRegistry:
    return register_builtin_nodes(NodeRegistry())


def _definition(plan_data: dict[str, Any]) -> Definition:
    return Definition.model_validate(
        {
            "id": "wf-plan-test",
            "name": "plan test",
            "nodes": [
                {
                    "id": "seed",
                    "type": "data",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "spec_type": "data.transform",
                        "config": {"expression": "{'topic': 'espresso'}"},
                    },
                },
                {
                    "id": "the_plan",
                    "type": "plan",
                    "position": {"x": 200, "y": 0},
                    "data": plan_data,
                },
            ],
            "edges": [
                {"id": "e1", "source": "seed", "target": "the_plan"},
            ],
            "entry_nodes": ["seed"],
        }
    )


def test_plan_step_contract_is_fully_typed(registry: NodeRegistry) -> None:
    """Dynamic plan I/O is still bounded to JSON — never untyped Any."""
    report = audit_registry(registry)
    plan = next(node for node in report.nodes if node.node_type == "plan.step")
    assert plan.state is ConformanceState.FULL


async def _run(definition: Definition, registry: NodeRegistry) -> dict[str, Any]:
    compiled = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        compiled, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="plan-test")
    assert result.status.value == "completed", f"run did not complete: {result.status}"
    return result.last_outputs["the_plan"]


@pytest.mark.asyncio
async def test_sketch_plan_is_a_junction(registry: NodeRegistry) -> None:
    """A sketch-phase plan (no sample, no resolver) passes input through —
    the graph never refuses to run because a thought is immature."""
    out = await _run(_definition({"spec_type": "plan.step", "config": {}}), registry)
    assert out == {"topic": "espresso"}


@pytest.mark.asyncio
async def test_stand_in_sample_substitutes(registry: NodeRegistry) -> None:
    """A pinned sample output is served verbatim (n8n pin-data semantics)."""
    sample = {"websites": ["a.com", "b.com"], "count": 2}
    out = await _run(
        _definition(
            {
                "spec_type": "plan.step",
                "config": {"stand_in_output": sample},
            }
        ),
        registry,
    )
    assert out == sample


@pytest.mark.asyncio
async def test_dynamic_output_schema_comes_from_contract(registry: NodeRegistry) -> None:
    """The plan's candidate output contract IS the compiled output schema."""
    schema = {
        "type": "object",
        "properties": {"websites": {"type": "array", "items": {"type": "string"}}},
        "required": ["websites"],
    }
    definition = _definition(
        {
            "spec_type": "plan.step",
            "config": {"output_schema_json": schema},
        }
    )
    compiled = compile_graph(definition, registry=registry)
    assert compiled.nodes["the_plan"].effective_output_schema == schema


@pytest.mark.asyncio
async def test_resolver_delegation_and_refusal(registry: NodeRegistry) -> None:
    """With a resolver installed and a plan_id set, execution delegates; a
    'refused' result parks the run as a named failure on the plan node."""
    calls: list[str] = []

    async def resolver(ctx: Any, config: Any, inputs: Any) -> dict[str, Any]:
        calls.append(config.plan_id)
        return {"mode": "stand_in", "output": {"served": True}}

    set_plan_resolver(resolver)
    try:
        out = await _run(
            _definition(
                {
                    "spec_type": "plan.step",
                    "config": {"plan_id": "11111111-1111-1111-1111-111111111111"},
                }
            ),
            registry,
        )
        assert out == {"served": True}
        assert calls == ["11111111-1111-1111-1111-111111111111"]

        async def not_built_resolver(ctx: Any, config: Any, inputs: Any) -> dict[str, Any]:
            return {"mode": "not_built", "plan_name": "Agent research"}

        set_plan_resolver(not_built_resolver)
        definition = _definition(
            {
                "spec_type": "plan.step",
                "config": {"plan_id": "11111111-1111-1111-1111-111111111111"},
            }
        )
        compiled = compile_graph(definition, registry=registry)
        scheduler = Scheduler(
            compiled,
            MemoryCheckpointer(),
            make_app_context(FakeEmitter()),
            registry=registry,
        )
        result = await scheduler.run(run_id="plan-test-not-built")
        # The honest stop: a typed failure naming the plan, never a pass-through.
        assert result.status.value == "errored"
        assert "This step is planned but not built yet: Agent research" in str(result.failure or result.error)
    finally:
        set_plan_resolver(None)
