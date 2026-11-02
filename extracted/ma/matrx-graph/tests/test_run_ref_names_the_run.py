"""``{"$run": "id"}`` — a step's authored input can name the run executing it.

A record a run writes often has to say which run wrote it (a study kit's outline rows carry
``metadata.built_by_run_id``; the page compares that run's inputs with the kit's Sources to
call the outline stale). Before this reference a workflow had no way to say it: no step
echoes the run id, and edges carry data only.
"""

from __future__ import annotations

import dataclasses

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.errors import UnresolvedInputError
from matrx_graph.types.variables import resolve_var_refs

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def test_a_step_reads_the_run_it_belongs_to() -> None:
    definition = {
        "version": "1",
        "nodes": [
            {
                "id": "stamp",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {
                    "spec_type": "data.transform",
                    "input": {"meta": {"built_by_run_id": {"$run": "id"}, "workflow": {"$run": "workflow_id"}}},
                    "config": {"expression": "{'meta': inputs['meta']}"},
                },
            }
        ],
        "edges": [],
    }
    reg = _registry()
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=reg, definition_id="wf-1")
    result = await scheduler.run(run_id="run-42")
    assert result.last_outputs["stamp"]["meta"] == {"built_by_run_id": "run-42", "workflow": "wf-1"}


def test_an_unknown_run_field_is_refused() -> None:
    with pytest.raises(UnresolvedInputError):
        resolve_var_refs({"x": {"$run": "user"}}, run_variables={}, declared={}, node_id="n", run_facts={"id": "r"})


def test_no_run_to_read_is_loud_when_strict_and_none_when_lenient() -> None:
    with pytest.raises(UnresolvedInputError):
        resolve_var_refs({"$run": "id"}, run_variables={}, declared={}, node_id="n")
    assert resolve_var_refs({"$run": "id"}, run_variables={}, declared={}, node_id="n", strict=False) is None


def _stamp_graph(fields: dict[str, str]):
    reg = _registry()
    definition = {
        "version": "1",
        "nodes": [
            {
                "id": "stamp",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {
                    "spec_type": "data.transform",
                    "input": {"meta": {k: {"$run": v} for k, v in fields.items()}},
                    "config": {"expression": "{'meta': inputs['meta']}"},
                },
            }
        ],
        "edges": [],
    }
    return compile_graph(Definition.model_validate(definition), registry=reg), reg


async def test_a_step_reads_the_runs_organization_and_user_from_its_carried_context() -> None:
    # 2026-10-27: $run offers organization_id and user_id — read from the run's own
    # AppContext (the carried request context), never resolved from a default.
    graph, reg = _stamp_graph(
        {"org": "organization_id", "who": "user_id", "step": "step_id", "run": "id"}
    )
    app = dataclasses.replace(make_app_context(user_id="user-7"), organization_id="org-9")
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=reg, definition_id="wf-1")
    result = await scheduler.run(run_id="run-42")
    assert result.last_outputs["stamp"]["meta"] == {
        "org": "org-9",
        "who": "user-7",
        "step": "stamp",
        "run": "run-42",
    }


async def test_a_run_without_an_organization_refuses_rather_than_inventing_one() -> None:
    graph, reg = _stamp_graph({"org": "organization_id"})
    app = dataclasses.replace(make_app_context(), organization_id=None)
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=reg, definition_id="wf-1")
    result = await scheduler.run(run_id="run-43")
    assert result.status.value != "completed"
    assert "organization_id" in (result.error or "")
