"""The one-graph migration of notes and frames into information nodes (CONTRACTS §2.5).

Proof: the round trip is identity; a row with no notes or frames is returned as it came (so its hash cannot
move); a row that has them hashes the same after as before and compiles; a hash recorded before the move
still verifies through the recorded alias. Every check is a function the tests also run against a
deliberately broken transform and expect to fail (a check that cannot fail proves nothing).
"""

from __future__ import annotations

import copy
from typing import Any, Callable

import pytest

from matrx_graph import Definition, NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.information import (
    HASH_ALIASES_KEY,
    assert_graph_is_executable,
    definition_hash,
    information_problems,
    legacy_definition_hash,
    legacy_hashes,
)
from matrx_graph.information_migration import (
    MigrationRefused,
    census_of,
    has_legacy_content,
    migrate_document,
    normalized_legacy,
    restore_document,
)
from matrx_graph.validation import validate_definition


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _step(nid: str, x: float = 0, y: float = 0) -> dict[str, Any]:
    return {"id": nid, "type": "data", "position": {"x": x, "y": y},
            "data": {"spec_type": "data.transform", "config": {"expression": "{'ok': True}"}}}


def _note(nid: str, **extra: Any) -> dict[str, Any]:
    return {"id": nid, "type": "annotation", "position": {"x": 5, "y": 6}, "data": {"text": "mind the rate limit", "color": "yellow"}, **extra}


def _group(nid: str, members: list[str], **extra: Any) -> dict[str, Any]:
    return {"id": nid, "type": "group", "position": {"x": -30, "y": -60},
            "data": {"title": "Fetch", "color": "blue", "memberIds": members}, **extra}


def _legacy(*, annotations: list[Any] | None = None, groups: list[Any] | None = None) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    if annotations is not None:
        meta["annotations"] = annotations
    if groups is not None:
        meta["groups"] = groups
    return {
        "nodes": [_step("a", 0, 0), _step("b", 200, 0)],
        "edges": [{"id": "ab", "source": "a", "target": "b", "data": {"kind": "data", "mappings": {"x": "ok"}}}],
        "metadata": meta,
    }


def _noted() -> dict[str, Any]:
    return _legacy(annotations=[_note("n1"), _note("n2", width=200, style={"width": "200px"})],
                   groups=[_group("g1", ["a", "n1"], dragHandle=".h", measured={"width": 9, "height": 9}), _group("g2", ["b"], description="second")])


def _h(doc: dict[str, Any]) -> str:
    return definition_hash(Definition.model_validate(doc), _registry())


# ---- the checks (each run against a broken transform below to prove it can fail) -----------------------

Migrate = Callable[[dict[str, Any]], Any]


def check_round_trip(migrate: Migrate, doc: dict[str, Any]) -> None:
    moved = migrate(doc)
    assert restore_document(moved.document) == normalized_legacy(doc)


def check_hash_and_compile(migrate: Migrate, doc: dict[str, Any]) -> None:
    moved = migrate(doc).document
    assert _h(moved) == _h(doc), "the executable hash moved"
    assert census_of(moved) == (0, 0), "notes or frames are still in metadata"
    assert information_problems(Definition.model_validate(moved), _registry()) == []
    assert validate_definition(moved, registry=_registry()).valid
    graph = compile_graph(Definition.model_validate(moved), registry=_registry())
    assert set(graph.nodes) == {"a", "b"}
    assert_graph_is_executable(graph)


def check_members_follow_frames(migrate: Migrate, doc: dict[str, Any]) -> None:
    by_id = {n["id"]: n for n in migrate(doc).document["nodes"]}
    assert (by_id["a"].get("parentId"), by_id["n1"].get("parentId"), by_id["b"].get("parentId")) == ("g1", "g1", "g2")
    assert by_id["g1"]["data"]["spec_type"] == "info.frame" and "memberIds" not in by_id["g1"]["data"]
    assert by_id["n2"]["data"]["spec_type"] == "info.note" and "parentId" not in by_id["n2"]


def _no_reparent(doc: dict[str, Any]) -> Any:
    moved = migrate_document(doc)
    for n in moved.document["nodes"]:
        n.pop("parentId", None)
    return moved


def _leaves_metadata(doc: dict[str, Any]) -> Any:
    moved = migrate_document(doc)
    return moved._replace(document={**moved.document, "metadata": doc["metadata"]})


def _loses_a_note_color(doc: dict[str, Any]) -> Any:
    moved = migrate_document(doc)
    for n in moved.document["nodes"]:
        if n["id"] == "n1":
            n["data"].pop("color")
    return moved


def _moves_a_step(doc: dict[str, Any]) -> Any:
    moved = migrate_document(doc)
    for n in moved.document["nodes"]:
        if n["id"] == "a":
            n["data"]["config"] = {"expression": "{'ok': False}"}
    return moved


# ---- the migration ---------------------------------------------------------------------------------


def test_a_noted_row_round_trips_to_identity() -> None:
    check_round_trip(migrate_document, _noted())


def test_a_noted_row_hashes_the_same_and_compiles_after() -> None:
    check_hash_and_compile(migrate_document, _noted())


def test_members_are_re_parented_and_notes_and_frames_become_info_nodes() -> None:
    check_members_follow_frames(migrate_document, _noted())
    moved = migrate_document(_noted())
    assert (moved.notes, moved.frames, moved.empty_frames_dropped, moved.claims_ignored) == (2, 2, 0, 0)


def test_what_the_canvas_ignores_on_load_is_ignored_and_counted() -> None:
    doc = _legacy(annotations=[_note("n1")],
                  groups=[_group("g1", ["a", "ghost"]), _group("g2", ["a", "b"]), _group("g3", ["ghost"])])
    moved = migrate_document(doc)
    by_id = {n["id"]: n for n in moved.document["nodes"]}
    assert by_id["a"]["parentId"] == "g1", "first frame wins"
    assert by_id["b"]["parentId"] == "g2"
    assert "g3" not in by_id, "a frame with no live member is not carried"
    assert (moved.frames, moved.empty_frames_dropped, moved.claims_ignored) == (2, 1, 1)
    check_round_trip(migrate_document, doc)
    check_hash_and_compile(migrate_document, doc)


def test_the_order_a_frame_lists_its_members_in_does_not_matter() -> None:
    doc = _legacy(groups=[_group("g1", ["b", "a"])])
    check_round_trip(migrate_document, doc)
    assert restore_document(migrate_document(doc).document)["metadata"]["groups"][0]["data"]["memberIds"] == ["a", "b"]


def test_a_row_with_nothing_to_move_comes_back_untouched() -> None:
    for meta in ({}, {"annotations": [], "groups": []}, {"annotations": [], "other": 1}):
        doc = {**_legacy(), "metadata": meta}
        moved = migrate_document(doc)
        assert moved.document is doc and not moved.changed
        assert not has_legacy_content(doc)
        assert _h(moved.document) == _h(doc)
        assert restore_document(moved.document) is moved.document


def test_only_the_key_that_carried_content_is_removed_so_an_empty_key_keeps_its_hash() -> None:
    doc = _legacy(annotations=[_note("n1")], groups=[])
    moved = migrate_document(doc).document
    assert moved["metadata"] == {"groups": []}
    assert _h(moved) == _h(doc)
    assert restore_document(moved)["metadata"]["annotations"][0]["id"] == "n1"


def test_the_migration_never_edits_its_input() -> None:
    doc = _noted()
    before = copy.deepcopy(doc)
    migrate_document(doc)
    assert doc == before


def test_migrating_twice_changes_nothing_more() -> None:
    once = migrate_document(_noted()).document
    again = migrate_document(once)
    assert again.document is once and not again.changed


@pytest.mark.parametrize("doc", [
    _legacy(annotations=[_note("a")]),                       # a note with a step's id
    _legacy(annotations=[{**_note("n1"), "type": "sticky"}]),  # not the old note shape
    _legacy(groups=[{**_group("g1", ["a"]), "type": "box"}]),  # not the old frame shape
    _legacy(annotations=[_note("n1"), _note("n1")]),         # an id twice
])
def test_a_row_the_migration_cannot_carry_faithfully_is_refused(doc: dict[str, Any]) -> None:
    with pytest.raises(MigrationRefused):
        migrate_document(doc)


def test_a_frame_inside_a_frame_cannot_go_back_to_the_old_shape() -> None:
    moved = migrate_document(_noted()).document
    for n in moved["nodes"]:
        if n["id"] == "g2":
            n["parentId"] = "g1"
    with pytest.raises(MigrationRefused):
        restore_document(moved)


# ---- the recorded hash pair ------------------------------------------------------------------------


def test_an_old_recorded_hash_verifies_through_the_alias_and_no_hash_moves() -> None:
    doc = _noted()
    old = legacy_definition_hash(Definition.model_validate(doc))
    moved = migrate_document(doc).document
    plain = Definition.model_validate(moved)
    assert old not in legacy_hashes(plain), "without the alias the old recorded hash is lost"
    moved["metadata"][HASH_ALIASES_KEY] = [{"old": old, "new": definition_hash(plain, _registry())}]
    stamped = Definition.model_validate(moved)
    assert old in legacy_hashes(stamped)
    assert definition_hash(stamped, _registry()) == definition_hash(plain, _registry()), "the alias entered the hash"
    assert legacy_definition_hash(stamped) == legacy_definition_hash(plain)
    assert compile_graph(stamped, registry=_registry()).definition_hash == definition_hash(plain, _registry())


# ---- every check can fail --------------------------------------------------------------------------


def test_the_round_trip_check_can_fail() -> None:
    with pytest.raises(AssertionError):
        check_round_trip(_loses_a_note_color, _noted())
    with pytest.raises(AssertionError):
        check_round_trip(_no_reparent, _noted())


def test_the_hash_and_compile_check_can_fail() -> None:
    with pytest.raises(AssertionError):
        check_hash_and_compile(_leaves_metadata, _noted())
    with pytest.raises(AssertionError):
        check_hash_and_compile(_moves_a_step, _noted())


def test_the_membership_check_can_fail() -> None:
    with pytest.raises(AssertionError):
        check_members_follow_frames(_no_reparent, _noted())
