"""compile_plan synthesis rules — goldens that pin the compiler's output.

The layer-padding math is the correctness-critical piece: Pregel fires a
node when ANY incoming edge fires, so an unequal-depth join without pads
would fire early with a partial payload. These tests pin the synthesized
nodes/edges/channels for each plan construct so a regression is a loud
diff, not a runtime park.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_ai.plans import AgentPlan, AgentPlanValidationError, compile_plan

_A1 = "1fd0cb1f-5b95-49f0-a7f8-79308dc50f58"
_A2 = "9f8eab67-96e4-4a08-9563-7a982f920527"

AGENT_TYPE = "ai.agent.start"


def _plan(steps: list[dict], inputs: dict | None = None) -> AgentPlan:
    return AgentPlan.model_validate(
        {"name": "t", "reasoning": "r", "inputs": inputs or {}, "steps": steps}
    )


def _nodes(definition: Any) -> dict[str, Any]:
    return {n.id: n for n in definition.nodes}


def _edges(definition: Any) -> dict[tuple[str, str], Any]:
    return {(e.source, e.target): e for e in definition.edges}


def test_linear_two_step_plan():
    definition = compile_plan(
        _plan(
            [
                {
                    "step": 1,
                    "agent_id": _A1,
                    "purpose": "generate cards",
                    "inputs": {"user_input": "make 25 cards", "topic": "Chemistry"},
                },
                {
                    "step": 2,
                    "agent_id": _A2,
                    "purpose": "summarize",
                    "inputs": {"front": "$steps.1.output.structured_output.cards.0.question"},
                },
            ]
        )
    )
    nodes = _nodes(definition)
    assert set(nodes) == {"step_1_args", "step_1", "step_2_args", "step_2"}
    assert nodes["step_1"].type == AGENT_TYPE
    assert nodes["step_1"].data["input"] == {"agent_id": _A1}
    assert nodes["step_1"].data["label"] == "generate cards"
    assert (
        nodes["step_1_args"].data["config"]["expression"]
        == "{'user_input': 'make 25 cards', 'variables': {'topic': 'Chemistry'}}"
    )
    assert nodes["step_2_args"].data["config"]["expression"] == (
        "{'variables': {'front': "
        "inputs['src_step_1']['structured_output']['cards'][0]['question']}}"
    )

    edges = _edges(definition)
    assert set(edges) == {
        ("step_1_args", "step_1"),
        ("step_1", "step_2_args"),
        ("step_2_args", "step_2"),
    }
    dep_edge = edges[("step_1", "step_2_args")]
    assert dep_edge.mappings == {"src_step_1": "$FULL_PAYLOAD"}

    assert definition.entry_nodes == ["step_1_args"]
    assert definition.channels == []
    meta = definition.metadata["agent_plan"]
    assert meta["result_map"] == {
        "1": {"node_id": "step_1", "kind": "single"},
        "2": {"node_id": "step_2", "kind": "single"},
    }
    assert meta["layers"] == 4  # args1=0, s1=1, args2=2, s2=3
    assert definition.metadata["source"] == "agent_plan"
    assert meta["plan"]["name"] == "t"


def test_diamond_with_unequal_depths_gets_padded():
    """1 → 2 (plain) and 1 → 3 (for_each); 4 joins 2+3 — the 2-branch is
    2 layers shorter and must be padded so both arrive in the same wave."""
    definition = compile_plan(
        _plan(
            [
                {"step": 1, "agent_id": _A1, "purpose": "seed", "inputs": {}},
                {
                    "step": 2,
                    "agent_id": _A1,
                    "purpose": "left",
                    "inputs": {"x": "$steps.1.output.final_text"},
                },
                {
                    "step": 3,
                    "agent_id": _A2,
                    "purpose": "right fan-out",
                    "for_each": "$steps.1.output.structured_output.cards",
                    "inputs": {"q": "$item.question"},
                },
                {
                    "step": 4,
                    "agent_id": _A1,
                    "purpose": "join",
                    "inputs": {
                        "left": "$steps.2.output.final_text",
                        "right": "$steps.3.output.count",
                    },
                },
            ]
        )
    )
    nodes = _nodes(definition)
    edges = _edges(definition)

    # fire: args1=0 s1=1 | args2=2 s2=3 | args3=2 map=3 worker=4 gather=5
    # args4 = 1+max(3,5) = 6 → the step_2 branch (out at 3) needs 2 pads.
    assert "pad_2_to_4_1" in nodes and "pad_2_to_4_2" in nodes
    assert nodes["pad_2_to_4_1"].data["config"]["expression"] == "inputs"
    assert edges[("step_2", "pad_2_to_4_1")].mappings == {"src_step_2": "$FULL_PAYLOAD"}
    assert edges[("pad_2_to_4_1", "pad_2_to_4_2")].mappings is None
    assert edges[("pad_2_to_4_2", "step_4_args")].mappings is None
    # The gather branch arrives directly (gap 0), payload namespaced.
    assert edges[("step_3_gather", "step_4_args")].mappings == {
        "src_step_3": "$FULL_PAYLOAD"
    }
    assert nodes["step_4_args"].data["config"]["expression"] == (
        "{'variables': {'left': inputs['src_step_2']['final_text'], "
        "'right': inputs['src_step_3']['count']}}"
    )


def test_for_each_synthesis():
    definition = compile_plan(
        _plan(
            [
                {"step": 1, "agent_id": _A1, "purpose": "seed", "inputs": {}},
                {
                    "step": 2,
                    "agent_id": _A2,
                    "purpose": "enrich each card",
                    "for_each": "$steps.1.output.structured_output.cards",
                    "inputs": {
                        "front": "$item.question",
                        "back": "$item.answer",
                        "topic": "$inputs.topic",
                        "difficulty": "Medium",
                        "user_input": "$item.question",
                    },
                },
            ],
            inputs={"topic": "General Chemistry"},
        )
    )
    nodes = _nodes(definition)
    edges = _edges(definition)

    assert set(nodes) == {
        "step_1_args",
        "step_1",
        "step_2_args",
        "step_2_map",
        "step_2",
        "step_2_empty",
        "step_2_gather",
    }
    assert (
        nodes["step_2_args"].data["config"]["expression"]
        == "{'items': inputs['src_step_1']['structured_output']['cards']}"
    )
    map_config = nodes["step_2_map"].data["config"]
    assert map_config["target_node_id"] == "step_2"
    assert map_config["max_dispatches"] == 200
    assert map_config["payload_template"] == {
        "user_input": "$item.question",
        "variables": {
            "back": "$item.answer",
            "difficulty": "Medium",
            "front": "$item.question",
            "topic": "General Chemistry",  # $inputs inlined at compile time
        },
    }
    worker = nodes["step_2"]
    assert worker.type == AGENT_TYPE
    assert worker.data["output_channel"] == "step_2_results"
    assert [c.name for c in definition.channels] == ["step_2_results"]
    assert definition.channels[0].reducer == "append"

    # Worker triggers gather; the empty-pad conditional keeps gather firing
    # (same super-step) when the map dispatches zero items.
    assert ("step_2", "step_2_gather") in edges
    empty_edge = edges[("step_2_map", "step_2_empty")]
    assert empty_edge.kind.value == "conditional"
    assert empty_edge.condition == "inputs['dispatched'] == 0"
    assert ("step_2_empty", "step_2_gather") in edges

    meta = definition.metadata["agent_plan"]
    assert meta["result_map"]["2"] == {"node_id": "step_2_gather", "kind": "list"}


def test_when_condition_rides_the_first_dependency_edge():
    definition = compile_plan(
        _plan(
            [
                {"step": 1, "agent_id": _A1, "purpose": "seed", "inputs": {}},
                {
                    "step": 2,
                    "agent_id": _A2,
                    "purpose": "maybe",
                    "depends_on": [1],
                    "when": "$steps.1.output.iterations < 5",
                },
            ]
        )
    )
    edge = _edges(definition)[("step_1", "step_2_args")]
    assert edge.kind.value == "conditional"
    assert edge.condition == "inputs['iterations'] < 5"
    assert edge.mappings == {"src_step_1": "$FULL_PAYLOAD"}


def test_inputs_inlining_in_plain_steps():
    definition = compile_plan(
        _plan(
            [
                {
                    "step": 1,
                    "agent_id": _A1,
                    "purpose": "seed",
                    "inputs": {"topic": "$inputs.topic", "count": 25, "deep": "$inputs.nested.0"},
                }
            ],
            inputs={"topic": "Chemistry", "nested": ["first"]},
        )
    )
    expression = _nodes(definition)["step_1_args"].data["config"]["expression"]
    assert expression == (
        "{'variables': {'count': 25, 'deep': 'first', 'topic': 'Chemistry'}}"
    )


def test_compile_runs_the_gate_first():
    with pytest.raises(AgentPlanValidationError):
        compile_plan(
            _plan([{"step": 1, "agent_id": _A1, "purpose": "bad", "inputs": {"x": "$steps.9.output"}}])
        )


def test_compiled_definition_passes_engine_compilation():
    """The end-to-end proof that synthesized output is a valid workflow."""
    from matrx_ai.graph_nodes import register_with_graph
    from matrx_graph import compile_graph, register_builtin_nodes
    from matrx_graph.executor.registry import default_registry

    register_builtin_nodes(default_registry(), overwrite=True)
    register_with_graph()

    definition = compile_plan(
        _plan(
            [
                {"step": 1, "agent_id": _A1, "purpose": "seed", "inputs": {"user_input": "go"}},
                {
                    "step": 2,
                    "agent_id": _A2,
                    "purpose": "fan out",
                    "for_each": "$steps.1.output.structured_output.cards",
                    "inputs": {"front": "$item.question"},
                },
                {
                    "step": 3,
                    "agent_id": _A1,
                    "purpose": "join",
                    "inputs": {"n": "$steps.2.output.count", "seed": "$steps.1.output.final_text"},
                },
            ]
        )
    )
    graph = compile_graph(definition)
    assert graph.nodes["step_2"].output_channel == "step_2_results"
    assert graph.channels["step_2_results"].reducer == "append"
