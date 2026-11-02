"""``set_entry_nodes`` — the edit that sets a workflow's starting steps (2026-10-26).

The break this catches: there is no op for ``entry_nodes``, so a builder has to
save a whole draft to change where a run starts; or the op writes ids that name
no step, which then fails compile far from the edit that caused it.
"""

from __future__ import annotations

import pytest

from matrx_graph import NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch
from matrx_graph.types.definition import Definition


def _news_digest() -> Definition:
    # Two independent sources feed one summary; today the run starts at both.
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "fetch_harbor_gazette", "type": "data.merge", "position": {"x": 0, "y": 0}, "data": {"inputs": {"base": {"source": "Harbor Gazette"}}}},
                {"id": "fetch_ferry_bulletin", "type": "data.merge", "position": {"x": 0, "y": 200}, "data": {"inputs": {"base": {"source": "Ferry Bulletin"}}}},
                {"id": "summarize", "type": "data.merge", "position": {"x": 300, "y": 100}, "data": {}},
            ],
            "edges": [
                {"id": "e1", "source": "fetch_harbor_gazette", "target": "summarize", "data": {"mappings": {"base": "result"}}},
                {"id": "e2", "source": "fetch_ferry_bulletin", "target": "summarize", "data": {"mappings": {"overlay": "result"}}},
            ],
        }
    )


def _apply(*ops: dict) -> Definition:
    return apply_patch(_news_digest(), DefinitionPatch.model_validate({"ops": list(ops)}))


def _compiled_entries(definition: Definition) -> list[str]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return sorted(compile_graph(definition, registry=registry).entry_node_ids)


@pytest.mark.parametrize(
    "starting_steps",
    [["fetch_harbor_gazette"], ["fetch_ferry_bulletin"]],
)
def test_set_entry_nodes_makes_the_run_start_at_exactly_those_steps(starting_steps):
    patched = _apply({"op": "set_entry_nodes", "node_ids": starting_steps})
    assert patched.entry_nodes == starting_steps
    assert _compiled_entries(patched) == starting_steps


def test_set_entry_nodes_refuses_ids_that_name_no_step():
    with pytest.raises(DefinitionPatchError, match=r"steps not found: \['fetch_tide_tables'\]"):
        _apply({"op": "set_entry_nodes", "node_ids": ["fetch_harbor_gazette", "fetch_tide_tables"]})


def test_set_entry_nodes_accepts_a_step_added_earlier_in_the_same_patch():
    patched = _apply(
        {
            "op": "add_node",
            "node": {"id": "fetch_tide_tables", "type": "data.merge", "position": {"x": 0, "y": 400}, "data": {}},
        },
        {"op": "set_entry_nodes", "node_ids": ["fetch_tide_tables"]},
    )
    assert patched.entry_nodes == ["fetch_tide_tables"]


def test_an_empty_list_clears_it_so_the_engine_derives_the_starting_steps():
    started_at_one = _apply({"op": "set_entry_nodes", "node_ids": ["fetch_ferry_bulletin"]})
    cleared = apply_patch(
        started_at_one, DefinitionPatch.model_validate({"ops": [{"op": "set_entry_nodes", "node_ids": []}]})
    )
    assert cleared.entry_nodes == []
    assert _compiled_entries(cleared) == ["fetch_ferry_bulletin", "fetch_harbor_gazette"]
