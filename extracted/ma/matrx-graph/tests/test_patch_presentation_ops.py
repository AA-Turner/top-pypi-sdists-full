"""Every Studio canvas edit has a typed patch op (generic-only RULES.md Rule 11).

Group/ungroup, move, sticky notes and edge kind/note used to exist only as a
whole-draft save from the Studio; an agent had to post a whole definition to do
them. These ops write exactly the shapes the Studio stores
(metadata.annotations / metadata.groups, edge.data.kind / edge.data.note).
"""

from __future__ import annotations

import pytest

from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch
from matrx_graph.types.definition import Definition


def _definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "intake", "type": "control.passthrough", "position": {"x": 100, "y": 100}, "data": {}},
                {"id": "triage", "type": "control.passthrough", "position": {"x": 400, "y": 160}, "data": {}},
            ],
            "edges": [{"id": "e1", "source": "intake", "target": "triage"}],
            "entry_nodes": ["intake"],
        }
    )


def _apply(*ops: dict) -> Definition:
    return apply_patch(_definition(), DefinitionPatch.model_validate({"ops": list(ops)}))


def test_move_a_step() -> None:
    d = _apply({"op": "move_node", "node_id": "triage", "position": {"x": 640, "y": 200}})
    triage = next(n for n in d.nodes if n.id == "triage")
    assert (triage.position.x, triage.position.y) == (640, 200)


def test_edge_kind_and_note() -> None:
    d = _apply(
        {"op": "set_edge_kind", "edge_id": "e1", "kind": "control"},
        {"op": "set_edge_note", "edge_id": "e1", "note": "only urgent forms\nline 2\nline 3\nline 4"},
    )
    data = d.edges[0].data
    assert data["kind"] == "control"
    assert data["note"] == "only urgent forms\nline 2\nline 3", "notes keep at most three lines, like the Studio"
    cleared = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "set_edge_note", "edge_id": "e1", "note": "  "}]}))
    assert "note" not in cleared.edges[0].data
    with pytest.raises(Exception):
        DefinitionPatch.model_validate({"ops": [{"op": "set_edge_kind", "edge_id": "e1", "kind": "teleport"}]})


def test_sticky_notes_live_in_metadata_annotations() -> None:
    d = _apply(
        {"op": "add_annotation", "annotation_id": "n1", "position": {"x": 0, "y": 0}, "text": "Check fever first", "color": "amber"},
        {"op": "update_annotation", "annotation_id": "n1", "text": "Check fever over 102F first"},
        {"op": "move_node", "node_id": "n1", "position": {"x": 20, "y": 30}},
    )
    (note,) = d.metadata["annotations"]
    assert note["type"] == "annotation" and note["data"] == {"text": "Check fever over 102F first", "color": "amber"}
    assert note["position"] == {"x": 20, "y": 30}
    assert not any(n.id == "n1" for n in d.nodes), "a note is never an engine step"
    gone = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "remove_annotation", "annotation_id": "n1"}]}))
    assert gone.metadata["annotations"] == []


def test_a_note_is_sized_and_moved_without_a_whole_save() -> None:
    # 2026-10-30: a note with no size grew over a group's header and only a whole-draft save
    # could size it. Size rides add and update; update can move it in the same op.
    d = _apply(
        {"op": "add_annotation", "annotation_id": "n1", "position": {"x": 0, "y": -140}, "text": "How to tune", "width": 300},
        {"op": "update_annotation", "annotation_id": "n1", "width": 360, "height": 120, "position": {"x": 0, "y": -240}},
    )
    (note,) = d.metadata["annotations"]
    assert (note["width"], note["height"]) == (360, 120)
    assert note["style"] == {"width": 360, "height": 120}, "the canvas reads the size from style too"
    assert note["position"] == {"x": 0, "y": -240}
    assert note["data"] == {"text": "How to tune"}, "sizing leaves the text alone"


def test_a_note_is_never_smaller_than_the_canvas_draws() -> None:
    d = _apply({"op": "add_annotation", "annotation_id": "n1", "position": {"x": 0, "y": 0}, "text": "x", "width": 20, "height": 10})
    (note,) = d.metadata["annotations"]
    assert (note["width"], note["height"]) == (180, 100)


def test_group_and_ungroup() -> None:
    d = _apply({"op": "group_nodes", "group_id": "g1", "title": "Score the applicant", "node_ids": ["intake", "triage"], "color": "blue"})
    (group,) = d.metadata["groups"]
    assert group["type"] == "group"
    assert group["data"] == {"title": "Score the applicant", "color": "blue", "memberIds": ["intake", "triage"]}
    assert group["position"] == {"x": 100 - 28, "y": 100 - 28 - 36}
    with pytest.raises(DefinitionPatchError, match="already in another group"):
        apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "group_nodes", "group_id": "g2", "title": "x", "node_ids": ["triage"]}]}))
    flat = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "ungroup", "group_id": "g1"}]}))
    assert flat.metadata["groups"] == []
    assert [n.id for n in flat.nodes] == ["intake", "triage"]


def test_missing_targets_are_all_reported() -> None:
    with pytest.raises(DefinitionPatchError) as err:
        _apply(
            {"op": "move_node", "node_id": "nope", "position": {"x": 0, "y": 0}},
            {"op": "set_edge_note", "edge_id": "e9", "note": "x"},
            {"op": "group_nodes", "group_id": "g", "title": "t", "node_ids": ["ghost"]},
        )
    assert len(err.value.issues) == 3


def test_removing_a_step_drops_it_from_its_group() -> None:
    grouped = _apply({"op": "group_nodes", "group_id": "g1", "title": "Score", "node_ids": ["intake", "triage"]})
    after = apply_patch(grouped, DefinitionPatch.model_validate({"ops": [{"op": "remove_node", "node_id": "triage"}]}))
    assert after.metadata["groups"][0]["data"]["memberIds"] == ["intake"]
    assert [n.id for n in after.nodes] == ["intake"]
