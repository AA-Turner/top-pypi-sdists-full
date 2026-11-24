"""Information nodes (notes, frames, media, kinds, records, reference cards) never run, never
change the hash of a workflow that has none, and are ignored by the engine readers.

One-graph CONTRACTS section 2.3. Real registry, real compiler, real scheduler; the hash
equality over every live row is proved by the read-only script named in the lane report.

THE BREAKS: a lone note that becomes an entry node and runs; a note edit that moves the
definition hash; a relation edge read as a data edge; a note that makes a job unclaimable by a
worker that predates it.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

import pytest

from matrx_graph import Definition, NodeRegistry, RunStatus, Scheduler, MemoryCheckpointer, compile_graph, register_builtin_nodes
from matrx_graph.information import (
    InformationReachedTheGraph,
    assert_graph_is_executable,
    information_problems,
    split_information,
)
from matrx_graph.patch import DefinitionPatch, apply_patch
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.validation import validate_definition
from matrx_graph.workers.capability import required_node_types

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def _step(nid: str, expression: str = "{'ok': True}") -> dict[str, Any]:
    return {"id": nid, "type": "data", "position": {"x": 0, "y": 0},
            "data": {"spec_type": "data.transform", "config": {"expression": expression}}}


def _note(nid: str = "note1", **extra: Any) -> dict[str, Any]:
    return {"id": nid, "type": "info", "position": {"x": 40, "y": -80},
            "data": {"spec_type": "info.note", "text": "remember the rate limit", "color": "yellow"}, **extra}


def _frame(nid: str = "frame1") -> dict[str, Any]:
    return {"id": nid, "type": "info", "position": {"x": -20, "y": -20}, "width": 400, "height": 200,
            "data": {"spec_type": "info.frame", "title": "Fetch", "color": "blue"}}


def _relation(eid: str, source: str, target: str, relation: str = "relates") -> dict[str, Any]:
    return {"id": eid, "source": source, "target": target, "data": {"kind": "relation", "relation": relation}}


def _plain() -> dict[str, Any]:
    return {
        "nodes": [_step("a"), _step("b", "{'got': inputs['x']}")],
        "edges": [{"id": "ab", "source": "a", "target": "b", "data": {"kind": "data", "mappings": {"x": "ok"}}}],
    }


def _with_info() -> dict[str, Any]:
    d = _plain()
    d["nodes"] += [_note(), _frame()]
    d["nodes"][0]["parentId"] = "frame1"
    d["edges"] += [_relation("r1", "note1", "a"), _relation("r2", "frame1", "b", "contains")]
    return d


def _hash(raw: dict[str, Any]) -> str:
    return compile_graph(Definition.model_validate(raw), registry=_registry()).definition_hash


def _old_hash(raw: dict[str, Any]) -> str:
    """What ``_hash_definition`` produced before information nodes existed, spelled out."""
    payload = Definition.model_validate(raw).model_dump(mode="json")
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:32]


# ---------------------------------------------------------------- the engine seam


async def test_a_lone_note_never_runs() -> None:
    registry = _registry()
    raw = {"nodes": [_step("a"), _note("lonely")], "edges": []}
    graph = compile_graph(Definition.model_validate(raw), registry=registry)
    assert set(graph.nodes) == {"a"}, "the note reached the compiled graph"
    assert list(graph.entry_node_ids) == ["a"], "the lone note became an entry node"
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry).run(run_id="lone-note")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "lonely" not in result.last_outputs


def test_a_workflow_of_only_notes_has_nothing_to_run_and_never_runs_a_note() -> None:
    raw = {"nodes": [_note("n1"), _note("n2")], "edges": []}
    registry = _registry()
    try:
        graph = compile_graph(Definition.model_validate(raw), registry=registry)
    except Exception:  # an empty workflow may be refused; either way no note is a step
        return
    assert not graph.nodes


def test_information_never_reaches_the_compiled_graph() -> None:
    graph = compile_graph(Definition.model_validate(_with_info()), registry=_registry())
    assert set(graph.nodes) == {"a", "b"}
    assert set(graph.edges) == {"ab"}
    assert_graph_is_executable(graph)


def test_the_scheduler_refuses_a_graph_holding_information() -> None:
    graph = compile_graph(Definition.model_validate(_plain()), registry=_registry())
    forged_edge = graph.edges["ab"].model_copy(update={"kind": EdgeKind.RELATION})
    forged = graph.model_copy(update={"edges": {**graph.edges, "ab": forged_edge}})
    with pytest.raises(InformationReachedTheGraph):
        Scheduler(forged, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=_registry())


def test_split_information_separates_nodes_and_relations() -> None:
    d = Definition.model_validate(_with_info())
    executable, info_nodes, relations = split_information(d, _registry())
    assert [n.id for n in executable.nodes] == ["a", "b"]
    assert [n.id for n in info_nodes] == ["note1", "frame1"]
    assert [e.id for e in relations] == ["r1", "r2"]
    assert [e.id for e in executable.edges] == ["ab"]


def test_a_definition_with_no_information_is_returned_as_it_is() -> None:
    d = Definition.model_validate(_plain())
    executable, info_nodes, relations = split_information(d, _registry())
    assert executable is d and info_nodes == [] and relations == []


# ---------------------------------------------------------------- the hash


def test_a_definition_without_information_hashes_exactly_as_it_always_did() -> None:
    assert _hash(_plain()) == _old_hash(_plain())


def test_a_note_free_definition_with_empty_legacy_keys_keeps_its_hash() -> None:
    raw = {**_plain(), "metadata": {"annotations": [], "groups": [], "start_when_ready": True}}
    assert _hash(raw) == _old_hash(raw)


def test_adding_editing_and_moving_information_never_moves_the_hash() -> None:
    base = _hash(_plain())
    assert _hash(_with_info()) == base
    edited = _with_info()
    edited["nodes"][2]["data"]["text"] = "completely different"
    edited["nodes"][2]["position"] = {"x": 900, "y": 900}
    edited["nodes"][3]["width"] = 999
    assert _hash(edited) == base


def test_a_real_step_edit_still_moves_the_hash() -> None:
    changed = _with_info()
    changed["nodes"][1]["data"]["config"]["expression"] = "{'got': 2}"
    assert _hash(changed) != _hash(_with_info())


def test_legacy_notes_in_metadata_do_not_move_the_hash_either() -> None:
    raw = {**_plain(), "metadata": {"annotations": [{"id": "x", "type": "annotation", "position": {"x": 0, "y": 0}, "data": {"text": "hi"}}]}}
    assert _hash(raw) == _hash(_plain())


def test_parent_id_is_only_written_when_it_is_set() -> None:
    plain = Definition.model_validate(_plain()).model_dump(mode="json")
    assert all("parentId" not in n for n in plain["nodes"])
    inside = Definition.model_validate(_with_info()).model_dump(mode="json")
    assert inside["nodes"][0]["parentId"] == "frame1"


# ---------------------------------------------------------------- validation


def test_a_workflow_with_notes_frames_and_relations_validates() -> None:
    result = validate_definition(_with_info(), registry=_registry())
    assert result.valid, [i.message for i in result.issues]


def test_a_note_is_not_judged_as_a_half_wired_step() -> None:
    raw = _with_info()
    messages = [i.message for i in validate_definition(raw, registry=_registry()).issues if i.node_id in {"note1", "frame1"}]
    assert messages == []


def test_a_plain_data_connection_onto_a_note_is_refused() -> None:
    raw = _plain()
    raw["nodes"].append(_note())
    raw["edges"].append({"id": "bad", "source": "a", "target": "note1", "data": {"kind": "data"}})
    result = validate_definition(raw, registry=_registry())
    assert not result.valid
    assert any(i.edge_id == "bad" for i in result.issues)


def test_an_entry_node_that_is_a_note_is_refused() -> None:
    raw = {**_with_info(), "entry_nodes": ["note1"]}
    result = validate_definition(raw, registry=_registry())
    assert not result.valid and any("note1" in i.message and "entry" in i.message for i in result.issues)


def test_a_note_cannot_be_the_result() -> None:
    raw = _with_info()
    raw["nodes"][2]["data"]["is_primary"] = True
    assert not validate_definition(raw, registry=_registry()).valid


def test_an_unknown_info_type_is_refused_by_name() -> None:
    raw = _plain()
    raw["nodes"].append({"id": "weird", "type": "info", "position": {"x": 0, "y": 0}, "data": {"spec_type": "info.hologram"}})
    problems = information_problems(Definition.model_validate(raw), _registry())
    assert [p.node_id for p in problems] == ["weird"]


def test_a_parent_must_be_a_frame() -> None:
    raw = _plain()
    raw["nodes"][1]["parentId"] = "a"
    result = validate_definition(raw, registry=_registry())
    assert not result.valid and any("parentId" in i.path for i in result.issues)


def test_an_unknown_edge_kind_is_still_refused() -> None:
    raw = _plain()
    raw["edges"][0]["data"]["kind"] = "teleport"
    with pytest.raises(Exception, match="unknown edge kind"):
        Definition.model_validate(raw)


def test_relation_is_a_known_edge_kind() -> None:
    assert Definition.model_validate(_with_info()).edges[1].kind is EdgeKind.RELATION


# ---------------------------------------------------------------- workers


def test_a_note_never_makes_a_job_need_a_capability() -> None:
    d = Definition.model_validate(_with_info())
    assert required_node_types(d) == ["data.transform"]


# ---------------------------------------------------------------- patch


def test_removing_a_node_prunes_its_relations_and_frees_its_children() -> None:
    d = Definition.model_validate(_with_info())
    patched = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "remove_node", "node_id": "frame1"}]}))
    assert {e.id for e in patched.edges} == {"ab", "r1"}
    assert all(n.parentId is None for n in patched.nodes)
    patched = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "remove_node", "node_id": "note1"}]}))
    assert {e.id for e in patched.edges} == {"ab", "r2"}


def test_set_parent_round_trips_through_the_declared_field() -> None:
    d = Definition.model_validate(_with_info())
    moved = apply_patch(d, DefinitionPatch.model_validate({"ops": [{"op": "set_parent", "node_id": "b", "parent_id": "frame1"}]}))
    assert next(n for n in moved.nodes if n.id == "b").parentId == "frame1"


# ---------------------------------------------------------------- the registry


def test_every_information_spec_declares_it_never_executes_and_sits_on_its_shelf() -> None:
    registry = _registry()
    info = [s for s in registry.all_specs() if s.node_type.startswith("info.")]
    assert {s.node_type for s in info} >= {"info.note", "info.frame", "info.media", "info.kind", "info.record",
                                           "info.agent", "info.workflow", "info.position", "info.topic"}
    for spec in info:
        descriptor = spec.to_palette_descriptor()
        assert descriptor["executes"] is False and descriptor["category"] == "info" and descriptor["group"] == "notes"
        assert descriptor["allowed_graphs"], spec.node_type
    for spec in registry.all_specs():
        if not spec.node_type.startswith("info."):
            assert spec.executes, f"{spec.node_type} stopped executing"


def test_references_are_placeable_beyond_their_home_graph() -> None:
    registry = _registry()
    assert "orchestra" in registry.get("info.agent").spec.allowed_graphs
    assert registry.get("info.note").spec.allowed_graphs == ("*",)


def test_copies_keep_information_verbatim() -> None:
    raw = _with_info()
    assert Definition.model_validate(copy.deepcopy(raw)).model_dump(mode="json") == Definition.model_validate(raw).model_dump(mode="json")


# ---------------------------------------------------------------- the hash projection itself


def _projection(raw: dict[str, Any]) -> dict[str, Any]:
    from matrx_graph.information import hash_projection

    return hash_projection(Definition.model_validate(raw), _registry())


def test_the_projection_of_a_note_free_definition_is_the_old_dump_exactly() -> None:
    raw = _plain()
    assert _projection(raw) == Definition.model_validate(raw).model_dump(mode="json")


def test_adding_a_note_a_relation_or_an_annotation_leaves_the_projection_unchanged() -> None:
    base = _projection(_plain())
    assert _projection(_with_info()) == base
    legacy = {**_plain(), "metadata": {"annotations": [{"id": "x", "type": "annotation", "position": {"x": 0, "y": 0}, "data": {"text": "hi"}}]}}
    assert _projection(legacy) == {**base, "metadata": {}}


def test_one_rule_says_what_is_information_for_a_definition_and_a_stored_document() -> None:
    from matrx_graph.information import executable_of, is_information_raw

    assert is_information_raw("info", None) and is_information_raw("data", "info.note")
    assert not is_information_raw("data", "data.transform")
    doc = {"nodes": [{"id": "z", "type": "info", "data": {}}, {"id": "a", "type": "data", "data": {"spec_type": "data.transform"}}], "edges": []}
    assert [n["id"] for n in executable_of(doc)["nodes"]] == ["a"]


def test_every_type_that_never_executes_is_in_the_info_family() -> None:
    """The SQL (`workflow.is_step`) and TS (`isInformationNode`) rules are the `info.` prefix; this
    keeps them exact: a non-executing type outside the family would be a step there."""
    outside = [s.node_type for s in _registry().all_specs() if not s.executes and not s.node_type.startswith("info.")]
    assert outside == []
