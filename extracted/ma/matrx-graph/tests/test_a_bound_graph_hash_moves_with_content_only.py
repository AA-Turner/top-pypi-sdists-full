"""The bound graph hash moves with the workflow's CONTENT, and only with it (lane 11 round 7).

A record trigger binds the compiled-graph hash of the published version it was turned on with;
the fire refuses when the version it loads compiles to a different hash. That is only a guard
if the REAL hash (``compile_graph(...).definition_hash``) changes for every real edit and stays
put for a no-op re-serialisation. Real compiler, real registry, a real-shaped definition:
"When a Patient is Booked, note the visit and tell the front desk".

THE BREAKS: a hash that ignores node config, nodes or edges (an in-place edit slips through);
a hash that depends on key order or JSON whitespace (every re-save looks like an edit).
"""

from __future__ import annotations

import copy
import json
from typing import Any

import pytest
from matrx_graph import Definition, NodeRegistry, compile_graph, register_builtin_nodes

BOOKED: dict[str, Any] = {
    "nodes": [
        {"id": "visit_note", "type": "data.transform", "position": {"x": 0, "y": 0},
         "data": {"label": "Write the visit note",
                  "config": {"expression": "'Visit booked for ' + str(inputs)"}}},
        {"id": "front_desk", "type": "data.transform", "position": {"x": 320, "y": 0},
         "data": {"label": "Tell the front desk",
                  "config": {"expression": "'New booking: ' + str(inputs)"}}},
    ],
    "edges": [{"id": "note_to_desk", "source": "visit_note", "target": "front_desk",
               "data": {"kind": "data", "mappings": {"result": "result"}}}],
}


def _hash(definition: dict[str, Any]) -> str:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return compile_graph(Definition.model_validate(definition), registry=registry).definition_hash


def _reversed_keys(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _reversed_keys(value[k]) for k in reversed(list(value))}
    if isinstance(value, list):
        return [_reversed_keys(v) for v in value]
    return value


def _edit_config(d):
    d["nodes"][1]["data"]["config"]["expression"] = "'New booking, call the patient: ' + str(inputs)"


def _add_node(d):
    d["nodes"].append({"id": "archive_copy", "type": "data.transform",
                       "position": {"x": 640, "y": 0}, "data": {"config": {"expression": "inputs"}}})


def _change_edge(d):
    d["edges"][0]["data"]["mappings"] = {"note": "result"}


@pytest.mark.parametrize(("label", "edit"), [
    ("a node's config edited", _edit_config),
    ("a node added", _add_node),
    ("an edge changed", _change_edge),
])
def test_a_real_edit_changes_the_hash(label, edit) -> None:
    edited = copy.deepcopy(BOOKED)
    edit(edited)
    assert _hash(edited) != _hash(BOOKED), label


@pytest.mark.parametrize(("label", "same"), [
    ("every key reordered", lambda d: _reversed_keys(d)),
    ("re-serialised with other whitespace", lambda d: json.loads(json.dumps(d, indent=7))),
])
def test_a_no_op_reserialisation_keeps_the_hash(label, same) -> None:
    assert _hash(same(copy.deepcopy(BOOKED))) == _hash(BOOKED), label
