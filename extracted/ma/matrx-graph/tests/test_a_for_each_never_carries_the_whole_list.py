"""Guard (FX8 class fix, 2026-11-02): no per-item template copies a per-item list whole into each item.

Run 424e086e (Brand foundation) died four times on ``check~each``: the shared unit "Ask a mandate per
batch and check each answer" (b6ca80bb, published v21) fanned 30 checks out with ``src: "$in.batches"``
— every item carried all 30 batches (~9 MB each, ~280 MB for the step). The instance was fixed in the
unit's draft; this pins the CLASS at the one validator every save / publish / apply-patch door runs:

* the 424e086e shape (a bare ``$in.batches`` beside ``$in.batches.[batch_id={$item…}]``) is an ERROR
  whose message hands over the selector that fixes it, and the fixed shape is clean;
* a For each that copies the very list it iterates into each item is an ERROR, on ``data.for_each``
  (default payload too) and on a hand-built ``control.map`` / ``data.map_template``;
* a list another For each iterates, broadcast whole, is a WARNING (offered, never blocked);
* shared values that are not per item (an agent key, a brand state) stay silent.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.fan_out_payload import whole_list_payload_findings
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.types.definition import Definition
from matrx_graph.validation import validate_definition

OWN_BATCH = "$in.batches.[batch_id={$item.values.0.batch_id}]"


def _node(nid: str, spec: str, *, config: dict[str, Any] | None = None, **data: Any) -> dict[str, Any]:
    return {"id": nid, "type": spec, "position": {"x": 0, "y": 0},
            "data": {"spec_type": spec, "label": nid, "config": config or {}, **data}}


def _edge(eid: str, source: str, target: str, mappings: dict[str, str]) -> dict[str, Any]:
    return {"id": eid, "source": source, "target": target, "data": {"kind": "data", "mappings": mappings}}


def _ask_and_check(src: Any) -> dict[str, Any]:
    """The b6ca80bb wiring, on builtin steps: ``take`` holds the batches, ``tag`` has one answer list
    per batch, ``check`` runs once per batch and reads the batches to check each quote."""
    check_payload = {
        "src": src,
        "sent": {"default": [], "$optional": f"{OWN_BATCH}.sent_ids"},
        "extra": "$in.extra",
        "items": "$item.values",
    }
    return {
        "nodes": [
            _node("take", "data.transform", config={"expression": "inputs"}),
            _node("tag", "data.transform", config={"expression": "inputs"}),
            _node("check", "data.check_items", config={"checks": [], "checks_from": "extra"},
                  for_each={"payload_template": check_payload}),
        ],
        "edges": [
            _edge("e_take_tag", "take", "tag", {"batches": "batches"}),
            _edge("e_take_check", "take", "check", {"extra": "extra", "batches": "batches"}),
            _edge("e_tag_check", "tag", "check", {"items": "values"}),
        ],
    }


def _issues(raw: dict[str, Any]) -> list[Any]:
    register_builtin_nodes(overwrite=True)
    return [i for i in validate_definition(raw).issues if "WHOLE" in i.message]


def test_the_424e086e_shape_is_refused_and_names_the_fix() -> None:
    issues = _issues(_ask_and_check("$in.batches"))
    assert len(issues) == 1, issues
    (issue,) = issues
    assert issue.severity == "error"
    assert issue.node_id == "check", "the badge belongs on the step the author wrote"
    assert issue.path == "nodes[check].data.for_each.payload_template.src"
    assert OWN_BATCH in issue.message, "the message must hand over the selector that fixes it"
    assert validate_definition(_ask_and_check("$in.batches")).valid is False


def test_the_fixed_shape_is_clean() -> None:
    assert _issues(_ask_and_check([OWN_BATCH])) == []


def test_the_list_being_iterated_copied_into_each_item_is_refused() -> None:
    # data.for_each with NO payload_template: the default payload hands every shared input on whole.
    raw = {
        "nodes": [_node("take", "data.transform", config={"expression": "inputs"}),
                  _node("each", "data.transform", config={"expression": "inputs"}, for_each={})],
        "edges": [_edge("e", "take", "each", {"items": "pages", "pages": "pages"})],
    }
    (issue,) = _issues(raw)
    assert issue.severity == "error" and issue.node_id == "each"
    assert "$in.pages.{$index}" in issue.message

    # The same on a hand-built For each and on a list reshape.
    raw = {
        "nodes": [_node("take", "data.transform", config={"expression": "inputs"}),
                  _node("fan", "control.map", config={"target_node_id": "work", "payload_template": {
                      "page": "$item", "all": "$in.everything"}}),
                  _node("work", "data.transform", config={"expression": "inputs"}),
                  _node("shape", "data.map_template", config={"template": {"p": "$item", "all": "$in.pages"}})],
        "edges": [_edge("e1", "take", "fan", {"items": "pages", "everything": "pages"}),
                  _edge("e2", "take", "shape", {"items": "pages", "pages": "pages"})],
    }
    found = {(i.node_id, i.severity) for i in _issues(raw)}
    assert found == {("fan", "error"), ("shape", "error")}, found


def test_a_list_another_for_each_iterates_is_a_warning() -> None:
    raw = {
        "nodes": [_node("take", "data.transform", config={"expression": "inputs"}),
                  _node("ask", "data.transform", config={"expression": "inputs"}, for_each={}),
                  _node("check", "data.transform", config={"expression": "inputs"},
                        for_each={"payload_template": {"answer": "$item", "batches": "$in.batches"}})],
        "edges": [_edge("e1", "take", "ask", {"items": "batches"}),
                  _edge("e2", "ask", "check", {"items": "values"}),
                  _edge("e3", "take", "check", {"batches": "batches"})],
    }
    (issue,) = _issues(raw)
    assert issue.severity == "warning" and issue.node_id == "check"
    assert validate_definition(raw).valid is True


def test_shared_values_that_are_not_per_item_stay_silent() -> None:
    raw = {
        "nodes": [_node("take", "data.transform", config={"expression": "inputs"}),
                  _node("draft", "data.transform", config={"expression": "inputs"},
                        for_each={"payload_template": {"job": "$item", "mk": "$in.mk", "state": "$in.state",
                                                       "page": "$in.pages.{$index}"}})],
        "edges": [_edge("e", "take", "draft", {"items": "jobs", "mk": "mk", "state": "state", "pages": "pages"})],
    }
    assert _issues(raw) == []
    assert whole_list_payload_findings(Definition.model_validate(raw)) == []


def test_a_count_or_a_lookup_by_key_is_not_a_copy_of_the_list() -> None:
    """Review of the guard, 2026-11-02: ``{in.batches:count}`` writes a number, and ``.{$item.id}``
    may key into a lookup table that is legitimately passed whole — neither proves N x N."""

    def step(template: dict[str, Any]) -> dict[str, Any]:
        return {
            "nodes": [_node("take", "data.transform", config={"expression": "inputs"}),
                      _node("each", "data.transform", config={"expression": "inputs"},
                            for_each={"payload_template": template})],
            "edges": [_edge("e", "take", "each", {"items": "jobs", "batches": "batches", "table": "table"})],
        }

    assert _issues(step({"n": {"$format": "{in.batches:count} batches"}, "own": [OWN_BATCH], "j": "$item"})) == []
    assert _issues(step({"table": "$in.table", "row": "$in.table.{$item.id}", "j": "$item"})) == []
    # The whole list written into text IS a copy.
    (issue,) = _issues(step({"all": {"$format": "{in.batches:join}"}, "own": [OWN_BATCH], "j": "$item"}))
    assert issue.severity == "error"
