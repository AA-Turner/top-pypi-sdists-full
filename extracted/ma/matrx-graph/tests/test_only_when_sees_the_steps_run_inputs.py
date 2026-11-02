"""'Only when' sees the same run inputs the step does.

Live defect 2026-10-28 (Smart Add offerings units): a run input given directly to a step —
``{"$input": name}`` in its ``data.inputs`` / ``data.input``, or a declared run input reaching an
entry step — never reached the step's 'Only when' check. The check runs on a gate the step's
connections are re-pointed to; the step's own authored inputs stayed on the step, so the gate saw
``inputs['name']`` missing and the condition raised or said no for every run.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context


def _step(when: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {
        "label": "Greet",
        "when": when,
        "config": {"expression": "{'greeting': 'hi ' + str(inputs['who'])}"},
    }
    if inputs is not None:
        data["inputs"] = inputs
    return {"id": "greet", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": data}


async def _run(defn: dict[str, Any], inputs: dict[str, Any], run_id: str):
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs=inputs
    )
    return await scheduler.run(run_id=run_id, inputs=inputs)


def _with_input_ref(when: str) -> dict[str, Any]:
    return {
        "variables": [{"name": "who", "default": ""}, {"name": "enabled", "default": False}],
        "nodes": [
            {"id": "start", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'ok': True}"}}},
            _step(when, {"who": {"$input": "who"}, "enabled": {"$input": "enabled"}}),
            {"id": "end", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'got': get(inputs, 'greeting')}"}}},
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "greet", "data": {"kind": "data", "mappings": {"ok": "ok"}}},
            {"id": "e2", "source": "greet", "target": "end",
             "data": {"kind": "data", "mappings": {"greeting": "greeting"}}},
        ],
    }


async def test_a_step_input_given_by_name_reaches_only_when_and_it_says_yes() -> None:
    result = await _run(_with_input_ref("inputs['enabled']"), {"who": "Ann", "enabled": True}, "ow-ref-yes")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs.get("end") == {"got": "hi Ann"}, result.last_outputs


async def test_a_step_input_given_by_name_reaches_only_when_and_it_says_no() -> None:
    result = await _run(_with_input_ref("inputs['enabled']"), {"who": "Ann", "enabled": False}, "ow-ref-no")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "greet" not in result.last_outputs


async def test_a_declared_run_input_reaches_only_when_on_an_entry_step() -> None:
    defn = {
        "variables": [{"name": "who", "default": ""}, {"name": "enabled", "default": False}],
        "nodes": [_step("bool(inputs['enabled'])", {"who": {"$input": "who"}})],
        "edges": [],
    }
    result = await _run(defn, {"who": "Bo", "enabled": True}, "ow-entry-yes")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["greet"] == {"greeting": "hi Bo"}, result.last_outputs


async def test_only_when_on_a_strict_entry_step_reads_a_run_input_the_step_does_not_take() -> None:
    # data.batch is closed (extra="forbid"); the gate must not hand it the run inputs it read.
    defn = {
        "variables": [{"name": "page_list", "default": []}, {"name": "max_pages", "default": 0}],
        "nodes": [{
            "id": "split", "type": "data.batch", "position": {"x": 0, "y": 0},
            "data": {"when": "inputs['max_pages'] > 0", "config": {"size": 2},
                     "inputs": {"items": {"$input": "page_list"}}},
        }],
        "edges": [],
    }
    result = await _run(defn, {"page_list": [1, 2, 3], "max_pages": 4}, "ow-strict-entry")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "[1, 2]" in str(result.last_outputs.get("split")), result.last_outputs
