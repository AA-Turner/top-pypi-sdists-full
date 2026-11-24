"""A step no connection reaches runs the same however its run is started (lane H10b, 2026-11-16).

Live defect: 'Research: search and save one keyword' v39 had a clock step (``datetime.now``) with no incoming
connection, so it was an entry step beside the run's input step. Started from the Studio form (values addressed to
the input step, ``node_inputs``) it ran. Called by another workflow (inline child, and any ``inputs=`` start: API,
MCP, a durable child), every io.user_input field value was BROADCAST to every entry step; the clock is closed
(``extra="forbid"``) and refused ``topic_id`` / ``round_at`` ..., so every step after it errored on all keywords.

The engine now treats an input step's field names like declared variables: they reach an entry step only when that
step takes the name, and stay readable as ``{"$input": name}``. A name the workflow does not declare is still
broadcast, so a strict step still refuses a typo.

Red: the old ``_entry_broadcast`` counted only ``origin == "variable"`` names as declared — the ``inputs=`` and
inline cases errored ``extra_forbidden`` on NowInput.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph.nodes.subgraph.inline import run_inline_child
from tests._fixtures import make_app_context

VALUES = {"topic_id": "t1", "round_at": ""}


def _definition() -> Definition:
    return Definition.model_validate({
        "nodes": [
            {"id": "inputs", "type": "io.user_input", "position": {"x": 0, "y": 0}, "data": {"config": {"fields": [
                {"name": "topic_id", "label": "Topic", "required": True},
                {"name": "round_at", "label": "Round", "required": False, "defaultValue": ""},
            ]}}},
            # No connection reaches the clock: it is an entry step beside the input step.
            {"id": "clock", "type": "datetime.now", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "round", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'at': inputs['given'] or inputs['now']}"}}},
        ],
        "edges": [
            {"id": "e1", "source": "inputs", "target": "round", "data": {"kind": "data", "mappings": {"given": "round_at"}}},
            {"id": "e2", "source": "clock", "target": "round", "data": {"kind": "data", "mappings": {"now": "iso"}}},
        ],
    })


def _graph():
    registry = register_builtin_nodes(NodeRegistry())
    return compile_graph(_definition(), registry=registry), registry


def _assert_whole_run(result) -> None:
    assert result.status is RunStatus.COMPLETED, result.error
    assert "clock" in result.last_outputs, "the step no connection reaches never ran"
    assert str(result.last_outputs["round"]["at"]) == str(result.last_outputs["clock"]["iso"])


def test_the_clock_is_an_entry_step() -> None:
    graph, _ = _graph()
    assert set(graph.entry_node_ids) == {"inputs", "clock"}


@pytest.mark.parametrize("start", ["node_inputs", "inputs"])
async def test_a_top_level_start_runs_the_unconnected_step(start: str) -> None:
    graph, registry = _graph()
    kwargs = {"node_inputs": {"inputs": dict(VALUES)}} if start == "node_inputs" else {"inputs": dict(VALUES)}
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id=f"t-root-{start}", **kwargs
    )
    _assert_whole_run(result)


async def test_an_inline_child_runs_the_unconnected_step() -> None:
    graph, registry = _graph()
    ctx = SimpleNamespace(
        run_id="t-root-parent", node_id="call", dispatch_id="", item_index=0, firing=0, thread_id=None,
        attempt=1, app=make_app_context(),
    )
    result = await run_inline_child(ctx, graph, checkpointer=MemoryCheckpointer(), registry=registry, inputs=dict(VALUES))
    _assert_whole_run(result)


async def test_an_input_field_still_reaches_steps_that_read_it_by_name() -> None:
    """The field values are not lost to the steps that did not take them: ``{"$input": name}`` still reads them."""
    definition = _definition().model_copy(deep=True)
    definition.nodes.append(Definition.model_validate({"nodes": [
        {"id": "echo", "type": "data.transform", "position": {"x": 0, "y": 0},
         "data": {"config": {"expression": "{'topic': inputs['topic']}"}, "inputs": {"topic": {"$input": "topic_id"}}}},
    ], "edges": []}).nodes[0])
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(definition, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id="t-root-echo", inputs=dict(VALUES)
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["echo"]["topic"] == "t1"


async def test_a_name_the_workflow_does_not_declare_is_still_refused_by_a_strict_step() -> None:
    graph, registry = _graph()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id="t-root-typo", inputs={**VALUES, "topik_id": "x"}
    )
    assert result.status is not RunStatus.COMPLETED
    assert "topik_id" in str(result.error)
