"""A ``data.rules`` table may come from a run input — checked at run time like an authored one.

Smart Add rules-check finding (CONVERSION-PLAYBOOK, 2026-10-28): Plan the searches kept its query
patterns as a fixed rules table because "setting 'rules' cannot come from a run input". A table the
step marks editable (``x-run-input``) may now; every other list/object setting is still refused.
"""

from __future__ import annotations

import pytest

from matrx_graph import CompilationError, Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.validation import validate_definition

from tests._fixtures import make_app_context

DEFAULT_TABLE = [{"when": "inputs['n'] > 5", "then": {"label": "big"}}]


def _unit(default_table: object = DEFAULT_TABLE) -> Definition:
    variables = [{"name": "patterns", "default": default_table}] if default_table is not None else [
        {"name": "patterns"}
    ]
    return Definition.model_validate(
        {
            "variables": variables,
            "nodes": [
                {
                    "id": "decide",
                    "type": "data.rules",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"rules": {"$input": "patterns"}, "default": {"label": "other"}},
                             "inputs": {"n": 7}},
                }
            ],
            "edges": [],
        }
    )


async def _label(graph, registry, table: object | None):
    surface = {"patterns": table} if table is not None else {}
    return await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs=surface
    ).run(run_id="t-rules-from-input")


async def test_the_default_table_and_a_callers_table_each_decide() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_unit(), registry=registry)
    first = await _label(graph, registry, None)
    assert first.status is RunStatus.COMPLETED, first.error
    assert first.last_outputs["decide"]["label"] == "big"
    second = await _label(graph, registry, [{"when": "inputs['n'] == 7", "then": {"label": "seven"}}])
    assert second.status is RunStatus.COMPLETED, second.error
    assert second.last_outputs["decide"]["label"] == "seven"


async def test_a_callers_table_with_a_bad_predicate_fails_the_step_naming_the_row() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(_unit(), registry=registry)
    bad = await _label(graph, registry, [{"when": "__import__('os')", "then": {"label": "x"}}])
    assert bad.status is not RunStatus.COMPLETED
    assert "rule 0" in str(bad.error)


def test_the_table_is_accepted_at_save_and_other_list_settings_are_still_refused() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    ok = validate_definition(_unit().model_dump(mode="json"), registry=registry)
    assert not [i for i in ok.issues if "cannot come from a run input" in i.message]
    defn = _unit().model_dump(mode="json")
    defn["nodes"][0]["data"]["config"]["left_out_labels"] = {"$input": "patterns"}
    refused = validate_definition(defn, registry=registry)
    assert any("'left_out_labels' cannot come from a run input" in i.message for i in refused.issues)
    with pytest.raises(CompilationError):
        compile_graph(Definition.model_validate(defn), registry=registry)
