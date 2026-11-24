"""Every matrx-graph reader of a raw Definition ignores information nodes and relation edges.

Rule (one-graph CONTRACTS 2.4): steps are `executes` nodes; counts, hashes, terminals and folds
ignore notes, frames and relations, and a fold keeps them. Each reader is run on the same workflow
with and without information and must answer the same.
"""

from __future__ import annotations

import copy
from typing import Any

from matrx_graph import Definition, NodeRegistry, compile_graph, register_builtin_nodes
from matrx_graph.composition import required_entry_fields
from matrx_graph.content_ir.authoring_gate import authored_kind_bindings
from matrx_graph.fan_out_payload import whole_list_payload_findings
from matrx_graph.fold import fold_reshape_steps
from matrx_graph.information import executable_of
from matrx_graph.overview import collapse_definition, definition_structure_hash
from matrx_graph.types.deliverables import compute_deliverables
from matrx_graph.visible_io import visible_io_findings


def _step(nid: str, spec: str = "data.transform", **cfg: Any) -> dict[str, Any]:
    return {"id": nid, "type": "data", "position": {"x": 0, "y": 0},
            "data": {"spec_type": spec, "label": nid, "config": cfg or {"expression": "{'ok': True}"}}}


def _plain() -> dict[str, Any]:
    return {
        "nodes": [_step("a"), _step("b", expression="{'got': inputs['x']}"), _step("c", expression="{'got': inputs['y']}")],
        "edges": [
            {"id": "ab", "source": "a", "target": "b", "data": {"kind": "data", "mappings": {"x": "ok"}}},
            {"id": "bc", "source": "b", "target": "c", "data": {"kind": "data", "mappings": {"y": "got"}}},
        ],
    }


def _with_info() -> dict[str, Any]:
    d = _plain()
    d["nodes"] += [
        {"id": "n1", "type": "info", "position": {"x": 0, "y": -90}, "data": {"spec_type": "info.note", "text": "hi", "color": "yellow"}},
        {"id": "f1", "type": "info", "position": {"x": 0, "y": 0}, "data": {"spec_type": "info.frame", "title": "F", "color": "gray"}},
    ]
    d["edges"] += [
        {"id": "r1", "source": "n1", "target": "c", "data": {"kind": "relation", "relation": "relates"}},
        {"id": "r2", "source": "f1", "target": "a", "data": {"kind": "relation", "relation": "contains"}},
    ]
    return d


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def test_the_overview_structure_hash_ignores_information() -> None:
    assert definition_structure_hash(Definition.model_validate(_with_info())) == definition_structure_hash(Definition.model_validate(_plain()))


def test_the_overview_has_no_step_for_a_note() -> None:
    with_info = collapse_definition(Definition.model_validate(_with_info()))
    without = collapse_definition(Definition.model_validate(_plain()))
    assert with_info == without


def test_deliverables_and_terminals_ignore_information() -> None:
    registry = _registry()
    def run(raw: dict[str, Any]) -> list[str]:
        d = Definition.model_validate(raw)
        return [x.node_id for x in compute_deliverables(compile_graph(d, registry=registry), d)]
    assert run(_with_info()) == run(_plain())


def test_visible_io_findings_ignore_relations_as_inbound_connections() -> None:
    registry = _registry()
    def findings(raw: dict[str, Any]) -> list[tuple[str, str]]:
        return sorted((f.node_id or "", f.code if hasattr(f, "code") else str(f)) for f in visible_io_findings(Definition.model_validate(raw), registry))
    assert findings(_with_info()) == findings(_plain())


def test_required_entry_fields_and_authored_kinds_ignore_information() -> None:
    assert required_entry_fields(Definition.model_validate(_with_info())) == required_entry_fields(Definition.model_validate(_plain()))
    assert authored_kind_bindings(Definition.model_validate(_with_info())) == authored_kind_bindings(Definition.model_validate(_plain()))


def test_whole_list_payload_findings_ignore_information() -> None:
    assert whole_list_payload_findings(Definition.model_validate(_with_info())) == whole_list_payload_findings(Definition.model_validate(_plain()))


def test_folding_never_counts_a_relation_as_a_consumer_and_keeps_the_notes() -> None:
    plain = _plain()
    folded_plain, folds_plain, _ = fold_reshape_steps(copy.deepcopy(plain))
    folded, folds, _ = fold_reshape_steps(_with_info())
    assert [f.step_id for f in folds] == [f.step_id for f in folds_plain], "a relation edge changed what folds"
    ids = {n["id"] for n in folded["nodes"]}
    assert {"n1", "f1"} <= ids, "a fold dropped the notes"
    assert all(e["id"] in {x["id"] for x in folded["edges"]} for e in _with_info()["edges"] if e["id"] == "r2")


def test_executable_of_accepts_a_stored_document_and_leaves_a_clean_one_alone() -> None:
    plain = _plain()
    assert executable_of(plain) is plain
    stripped = executable_of(_with_info())
    assert [n["id"] for n in stripped["nodes"]] == ["a", "b", "c"]
    assert [e["id"] for e in stripped["edges"]] == ["ab", "bc"]


def test_a_graph_object_passes_through() -> None:
    sentinel = object()
    assert executable_of(sentinel) is sentinel
