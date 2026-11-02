"""A declared variable passed as a run input never reaches a strict entry step that lacks it.

Live defect 2026-10-27: "Choose pages to read" started over MCP/API with
``inputs={"brand_id", "kinds_first", "max_pages"}`` died at its entry step
(``web.stored_pages.read``, ``extra="forbid"``) because every run input was copied into
every entry step, including ``kinds_first`` / ``max_pages`` that later steps read with
``{"$input": name}``. A declared variable now reaches a strict entry step only when the
step declares an input of that name, and stays readable as ``{"$input": name}``. A name
that is NOT a declared variable is still broadcast, so a strict step refuses a typo.
"""

from __future__ import annotations

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context


def _defn() -> Definition:
    return Definition.model_validate(
        {
            "variables": [
                {"name": "page_list", "default": []},
                {"name": "max_pages", "default": 20},
                {"name": "items", "default": []},
            ],
            "nodes": [
                {
                    # data.batch is closed (extra="forbid"): its only input is `items`.
                    "id": "split",
                    "type": "data.batch",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"size": 2}, "inputs": {"items": {"$input": "page_list"}}},
                }
            ],
            "edges": [],
        }
    )


async def _run(inputs: dict, run_id: str):
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_defn(), registry=registry)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id=run_id, inputs=inputs
    )


async def test_declared_variables_the_entry_step_lacks_are_not_sent_to_it() -> None:
    result = await _run({"page_list": [1, 2, 3], "max_pages": 4}, "t-strict-entry-vars")
    assert result.status is RunStatus.COMPLETED, result.error
    # page_list was not handed to the step, yet {"$input": "page_list"} still resolved.
    out = result.last_outputs["split"]
    assert "[1, 2]" in str(out) and "[3]" in str(out), out


async def test_an_undeclared_extra_still_reaches_a_strict_step_and_is_refused() -> None:
    result = await _run({"page_list": [1], "max_pagez": 4}, "t-strict-entry-typo")
    assert result.status is not RunStatus.COMPLETED
    assert "max_pagez" in str(result.error)
