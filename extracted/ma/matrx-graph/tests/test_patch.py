"""DefinitionPatch — the typed workflow-edit primitive (matrx_graph.patch).

Forcing-function posture: every test builds a real Definition, applies a
real patch through the public API, and asserts on the RESULTING definition
(round-tripped through Pydantic), never on internals.
"""

from __future__ import annotations

import pytest

from matrx_graph import (
    Definition,
    DefinitionPatch,
    DefinitionPatchError,
    apply_patch,
)


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "version": "1",
            "nodes": [
                {
                    "id": "a",
                    "type": "llm",
                    "position": {"x": 0, "y": 0},
                    "data": {"label": "A", "config": {"model": "m1", "timeout_s": 30}},
                },
                {
                    "id": "b",
                    "type": "llm",
                    "position": {"x": 100, "y": 0},
                    "data": {"label": "B", "config": {}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "a", "target": "b"},
            ],
            "variables": [{"name": "topic", "description": "d", "default": "x"}],
            "entry_nodes": ["a"],
        }
    )


def test_update_node_data_deep_merges_and_deletes() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "update_node_data",
                    "node_id": "a",
                    "data": {"config": {"timeout_s": 60, "model": None}},
                }
            ]
        }
    )
    result = apply_patch(_definition(), patch)
    node_a = next(n for n in result.nodes if n.id == "a")
    assert node_a.config == {"timeout_s": 60}
    assert node_a.label == "A"  # untouched siblings survive


def test_update_node_type_and_data_round_trip_as_one_consistent_patch() -> None:
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "plan-a",
                    "type": "plan",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "label": "Research the market",
                        "spec_type": "plan.step",
                        "category": "plan",
                        "config": {"plan_id": "plan-row-1", "stand_in_output": {}},
                    },
                }
            ]
        }
    )
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "update_node_type",
                    "node_id": "plan-a",
                    "type": "tool",
                },
                {
                    "op": "update_node_data",
                    "node_id": "plan-a",
                    "data": {
                        "spec_type": "http.get",
                        "category": "tool",
                        "config": {"plan_id": None, "stand_in_output": None, "timeout": 30},
                        "plan_id": "plan-row-1",
                    },
                },
            ]
        }
    )

    persisted = apply_patch(definition, patch)
    reloaded = Definition.model_validate(persisted.model_dump(mode="json"))
    node = reloaded.nodes[0]

    assert node.type == "tool"
    assert node.spec_type == "http.get"
    assert node.data["category"] == "tool"
    assert node.config == {"timeout": 30}
    assert node.data["plan_id"] == "plan-row-1"


def test_apply_patch_is_pure() -> None:
    definition = _definition()
    patch = DefinitionPatch.model_validate({"ops": [{"op": "remove_edge", "edge_id": "e1"}]})
    result = apply_patch(definition, patch)
    assert len(result.edges) == 0
    assert len(definition.edges) == 1  # input untouched


def test_remove_node_drops_its_edges_and_entry_ref() -> None:
    patch = DefinitionPatch.model_validate({"ops": [{"op": "remove_node", "node_id": "a"}]})
    result = apply_patch(_definition(), patch)
    assert [n.id for n in result.nodes] == ["b"]
    assert result.edges == []
    assert result.entry_nodes == []


def test_add_node_and_edge() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "add_node",
                    "node": {
                        "id": "c",
                        "type": "llm",
                        "position": {"x": 200, "y": 0},
                        "data": {},
                    },
                },
                {"op": "add_edge", "edge": {"id": "e2", "source": "b", "target": "c"}},
            ]
        }
    )
    result = apply_patch(_definition(), patch)
    assert {n.id for n in result.nodes} == {"a", "b", "c"}
    assert {e.id for e in result.edges} == {"e1", "e2"}


def test_set_and_remove_variable() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "set_variable",
                    "variable": {"name": "topic", "description": "new", "default": "y"},
                },
                {
                    "op": "set_variable",
                    "variable": {"name": "extra", "description": "", "default": None},
                },
                {"op": "remove_variable", "name": "topic"},
            ]
        }
    )
    result = apply_patch(_definition(), patch)
    assert [v.name for v in result.variables] == ["extra"]


def test_all_issues_collected_in_one_error() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {"op": "update_node_data", "node_id": "missing", "data": {}},
                {"op": "remove_edge", "edge_id": "nope"},
            ]
        }
    )
    with pytest.raises(DefinitionPatchError) as exc:
        apply_patch(_definition(), patch)
    assert len(exc.value.issues) == 2
    assert "missing" in exc.value.issues[0]
    assert "nope" in exc.value.issues[1]


def test_duplicate_add_node_is_an_issue() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "add_node",
                    "node": {
                        "id": "a",
                        "type": "llm",
                        "position": {"x": 0, "y": 0},
                        "data": {},
                    },
                }
            ]
        }
    )
    with pytest.raises(DefinitionPatchError):
        apply_patch(_definition(), patch)


def test_empty_ops_rejected_by_schema() -> None:
    with pytest.raises(Exception):
        DefinitionPatch.model_validate({"ops": []})


def test_unknown_op_rejected() -> None:
    with pytest.raises(Exception):
        DefinitionPatch.model_validate({"ops": [{"op": "explode"}]})


# ---------------------------------------------------------------------------
# replace_node / replace_edge — whole-item restatement (2026-09-11)
#
# The partial-edit path an author reaches through aidream's `workflow_author
# action=patch`: "this node is now exactly this", without resending the other
# fifty. update_node_data MERGES and cannot drop a key the author omitted; a
# restatement has to be able to.
# ---------------------------------------------------------------------------


def test_replace_node_swaps_the_whole_node_in_place() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "replace_node",
                    "node": {
                        "id": "a",
                        "type": "text",
                        "position": {"x": 5, "y": 7},
                        "data": {"label": "A rewritten", "config": {}},
                    },
                }
            ]
        }
    )
    result = apply_patch(_definition(), patch)
    assert [n.id for n in result.nodes] == ["a", "b"], "order is the author's, not the patch's"
    node_a = next(n for n in result.nodes if n.id == "a")
    assert node_a.type == "text"
    assert node_a.position.x == 5
    assert node_a.data == {"label": "A rewritten", "config": {}}
    assert "timeout_s" not in node_a.config, "replace drops what the author omitted"
    assert [e.id for e in result.edges] == ["e1"], "replacing a node never re-wires it"


def test_replace_node_keeps_the_declared_result_when_the_step_keeps_its_id() -> None:
    """A workflow's declared result is a mark on its step (``set_result`` -> ``is_primary``
    + ``deliverable``). Restating that step whole used to drop the mark, so the next publish
    was refused for a workflow with no declared result (2026-10-27)."""
    declared = apply_patch(
        _definition(), DefinitionPatch.model_validate({"ops": [{"op": "set_result", "node_id": "b"}]})
    )
    restate = {"id": "b", "type": "text", "position": {"x": 1, "y": 1}, "data": {"label": "B2", "config": {}}}
    result = apply_patch(
        declared, DefinitionPatch.model_validate({"ops": [{"op": "replace_node", "node": restate}]})
    )
    node_b = next(n for n in result.nodes if n.id == "b")
    assert node_b.data.get("is_primary") is True, "the declared result was dropped"
    assert node_b.data.get("deliverable") is True
    assert node_b.data.get("label") == "B2"

    # An author who restates the step as NOT the result says so explicitly; that wins.
    unmark = {**restate, "data": {"label": "B3", "config": {}, "is_primary": False}}
    result = apply_patch(
        declared, DefinitionPatch.model_validate({"ops": [{"op": "replace_node", "node": unmark}]})
    )
    assert next(n for n in result.nodes if n.id == "b").data.get("is_primary") is False


def test_replace_node_refuses_an_id_that_is_not_there() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "replace_node",
                    "node": {"id": "nope", "type": "llm", "position": {"x": 0, "y": 0}, "data": {}},
                }
            ]
        }
    )
    with pytest.raises(DefinitionPatchError) as exc:
        apply_patch(_definition(), patch)
    assert "use add_node" in exc.value.issues[0]


def test_replace_edge_swaps_the_whole_edge_in_place() -> None:
    patch = DefinitionPatch.model_validate(
        {
            "ops": [
                {
                    "op": "replace_edge",
                    "edge": {"id": "e1", "source": "b", "target": "a", "data": {"kind": "control"}},
                }
            ]
        }
    )
    result = apply_patch(_definition(), patch)
    assert len(result.edges) == 1
    edge = result.edges[0]
    assert (edge.source, edge.target) == ("b", "a")
    assert edge.data == {"kind": "control"}


def test_replace_edge_refuses_an_id_that_is_not_there() -> None:
    patch = DefinitionPatch.model_validate(
        {"ops": [{"op": "replace_edge", "edge": {"id": "nope", "source": "a", "target": "b"}}]}
    )
    with pytest.raises(DefinitionPatchError) as exc:
        apply_patch(_definition(), patch)
    assert "use add_edge" in exc.value.issues[0]
