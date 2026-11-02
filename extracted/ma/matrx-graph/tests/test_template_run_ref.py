"""``{"$run": name}`` inside a TEMPLATE — a produced element can say which run made it.

The step-input ``$run`` pass (``types/variables.py``) never reaches a template held in a
step's SETTINGS (``data.map_template``'s ``template``): before this, the ref passed through
as the literal dict ``{"$run": "id"}`` and the saved record carried no provenance.
"""

from __future__ import annotations

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import TemplatePathMissing, substitute_template

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def test_map_template_stamps_the_run_on_every_element() -> None:
    definition = {
        "version": "1",
        "nodes": [
            {
                "id": "shape_rows",
                "type": "data.map_template",
                "position": {"x": 0, "y": 0},
                "data": {
                    "spec_type": "data.map_template",
                    "input": {"items": [{"id": "a"}, {"id": "b"}]},
                    "config": {
                        "template": {
                            "id": "$item.id",
                            "metadata": {
                                "run_id": {"$run": "id"},
                                "workflow_id": {"$run": "workflow_id"},
                                "step_id": {"$run": "step_id"},
                            },
                            "idempotency_key": {"$uuid5": ["brand.choice", {"$run": "id"}, "$item.id"]},
                            "href": {"$format": "/workflows/{run.workflow_id}/runs/{run.id}"},
                        }
                    },
                },
            }
        ],
        "edges": [],
    }
    reg = _registry()
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=reg, definition_id="wf-1")
    result = await scheduler.run(run_id="run-42")
    values = result.last_outputs["shape_rows"]["values"]
    assert [v["metadata"] for v in values] == [
        {"run_id": "run-42", "workflow_id": "wf-1", "step_id": "shape_rows"}
    ] * 2
    assert values[0]["href"] == "/workflows/wf-1/runs/run-42"
    # one id per (run, element): stable on replay of the same run, distinct per element and per run
    assert values[0]["idempotency_key"] != values[1]["idempotency_key"]
    assert values[0]["idempotency_key"] == substitute_template(
        {"$uuid5": ["brand.choice", "run-42", "a"]}, None
    )


async def test_a_step_input_reads_its_own_step_id() -> None:
    definition = {
        "version": "1",
        "nodes": [
            {
                "id": "stamp",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {
                    "spec_type": "data.transform",
                    "input": {"meta": {"step": {"$run": "step_id"}}},
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
    assert result.last_outputs["stamp"]["meta"] == {"step": "stamp"}


def test_an_unknown_run_name_is_refused_and_optional_does_not_hide_it() -> None:
    run = {"id": "run-42", "workflow_id": "wf-1", "step_id": "s"}
    with pytest.raises(ExecutionError, match="user"):
        substitute_template({"who": {"$run": "user"}}, {}, run=run)
    with pytest.raises(ExecutionError) as caught:
        substitute_template({"$optional": {"$run": "user"}, "default": None}, {}, run=run)
    assert not isinstance(caught.value, TemplatePathMissing)


def test_no_run_context_is_refused_with_a_sentence() -> None:
    with pytest.raises(ExecutionError, match="no run"):
        substitute_template({"run_id": {"$run": "id"}}, {"id": "a"}, index=0)
    with pytest.raises(ExecutionError, match="no value in this run"):
        substitute_template({"run_id": {"$run": "workflow_id"}}, {}, run={"id": "r", "workflow_id": None})


def test_a_template_reads_the_runs_organization_and_user() -> None:
    # 2026-10-27: the same RUN_REF_FIELDS reach templates — organization_id and user_id come
    # from the run's carried context; a run without one is refused, never defaulted.
    run = {"id": "r1", "organization_id": "org-9", "user_id": "user-7"}
    out = substitute_template(
        {"org": {"$run": "organization_id"}, "who": {"$run": "user_id"},
         "path": {"$format": "/orgs/{run.organization_id}/runs/{run.id}"}},
        {"x": 1},
        run=run,
    )
    assert out == {"org": "org-9", "who": "user-7", "path": "/orgs/org-9/runs/r1"}
    with pytest.raises(ExecutionError, match="organization_id"):
        substitute_template({"$run": "organization_id"}, {"x": 1}, run={"id": "r1", "organization_id": None})
