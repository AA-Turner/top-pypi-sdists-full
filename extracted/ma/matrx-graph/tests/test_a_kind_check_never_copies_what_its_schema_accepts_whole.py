"""A kind check never copies a subtree its schema accepts whole.

L-SPEED 6e (2026-11-10): the production Brand pick child spent ~0.9 s per run in ``_validate_reduced_copy`` — every
step's input and output kind check (``items``, ``join_request``, ``filter_result``…) rebuilt the 900 KB list of source
rows leaf by leaf to strip ``__kind`` markers, although each of those kinds types the list ``items: {$ref: JsonValue}``
and ``JsonValue`` is ``{}``: nothing under it can fail. The validation copy now keeps such a subtree as given. The
verdict is identical; a stored or returned value is still reduced by ``strip_kind_markers`` itself.

Red before: the rows came back as new objects (copied), and each nested marker was stripped from the copy.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.markers import reduce_for_validation, strip_kind_markers
from matrx_graph.kinds import _validate_reduced_copy

ITEMS_KIND: dict[str, Any] = {
    "type": "object",
    "$defs": {"JsonValue": {}, "Row": {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}},
    "required": ["items"],
    "properties": {
        "__kind": {"type": "string", "const": "items"},
        "items": {"type": "array", "items": {"$ref": "#/$defs/JsonValue"}, "title": "Items"},
        "rows": {"type": "array", "items": {"$ref": "#/$defs/Row"}},
        "loose": {"$ref": "#/$defs/Missing"},
    },
    "additionalProperties": False,
}


def _rows() -> list[dict[str, Any]]:
    return [{"__kind": "source_row", "id": i, "body": "x" * 50, "meta": {"__kind": "", "n": i}} for i in range(50)]


def test_a_subtree_under_json_value_is_validated_as_given() -> None:
    rows = _rows()
    value = {"__kind": "items", "items": rows}
    reduced = reduce_for_validation(value, ITEMS_KIND)
    assert all(a is b for a, b in zip(reduced["items"], rows, strict=True)), (
        "rows the schema accepts whole must not be copied for the check"
    )
    assert reduced["__kind"] == "items"  # the root marker the kind declares stays


def test_a_constrained_subtree_is_still_reduced() -> None:
    rows = _rows()
    reduced = reduce_for_validation({"rows": rows}, ITEMS_KIND)
    assert reduced["rows"] is not rows
    assert all("__kind" not in r and "__kind" not in r["meta"] for r in reduced["rows"])


def test_an_unresolvable_ref_is_not_treated_as_accepting() -> None:
    loose = {"__kind": "x", "a": 1}
    assert reduce_for_validation({"loose": loose}, ITEMS_KIND)["loose"] == {"a": 1}


def test_the_verdict_is_the_same_as_the_full_reduction() -> None:
    from matrx_graph.content_ir.markers import normalize_nonidentity_markers
    from matrx_graph.executor.schema_validation import validate_instance_checked

    cases = [
        {"__kind": "items", "items": _rows()},
        {"__kind": "items", "items": _rows(), "rows": [{"id": "nope"}]},
        {"__kind": "items", "items": "not a list"},
        {"__kind": "items", "items": _rows(), "extra": 1},
        {"rows": [{"__kind": "r", "id": 1}]},
    ]
    for case in cases:
        full = validate_instance_checked(
            ITEMS_KIND, strip_kind_markers(normalize_nonidentity_markers(case, ITEMS_KIND), ITEMS_KIND)
        )
        assert _validate_reduced_copy(ITEMS_KIND, case) == full, case


def test_the_validator_never_walks_a_list_its_schema_accepts_whole() -> None:
    """Part 2: the schema the validator applies leaves out ``items: {$ref: JsonValue}`` — jsonschema resolved that
    ``$ref`` once per element (most of a live kind check). Red before: the check applied the stored schema."""
    from matrx_graph.kinds import _checking_schema

    checking = _checking_schema(ITEMS_KIND)
    assert checking["properties"]["items"] == {"type": "array", "title": "Items"}
    assert checking["properties"]["rows"]["items"] == {"$ref": "#/$defs/Row"}  # a constrained element stays
    assert checking["properties"]["loose"] == {"$ref": "#/$defs/Missing"}  # an unresolvable ref stays (a skip)
    assert _checking_schema(ITEMS_KIND) is checking  # once per schema object


def test_the_checking_schema_gives_the_same_verdict_on_open_and_nested_schemas() -> None:
    from matrx_graph.executor.schema_validation import validate_instance_checked
    from matrx_graph.kinds import _checking_schema

    nested = {
        "type": "object",
        "$defs": {"JsonValue": {}, "Item": {"type": "object", "required": ["id"],
                                            "properties": {"id": {"type": "integer"}, "extra": {"$ref": "#/$defs/JsonValue"}},
                                            "additionalProperties": {"$ref": "#/$defs/JsonValue"}}},
        "properties": {
            "a": {"anyOf": [{"type": "array", "items": {"$ref": "#/$defs/Item"}}, {"type": "null"}]},
            "b": {"type": "object", "additionalProperties": {"$ref": "#/$defs/JsonValue"}},
            "c": {"not": {"$ref": "#/$defs/JsonValue"}},
        },
    }
    cases = [
        {"a": [{"id": 1, "extra": {"x": [1, 2]}, "z": 3}], "b": {"q": [1]}},
        {"a": [{"id": "no"}], "b": {"q": 1}},
        {"a": [{"extra": 1}]},
        {"a": None, "b": []},
        {"c": 1},
        {"a": "x"},
    ]
    for case in cases:
        assert validate_instance_checked(_checking_schema(nested), case) == validate_instance_checked(nested, case), case
