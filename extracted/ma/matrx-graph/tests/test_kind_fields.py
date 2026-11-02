"""fields_for_kind — a kind's output-table Fields (KINDS-GLUE wave 2 slice 1b, design §2.3).

The pure half; the store half (declared on the clone, read back through
``custom.table_kind_facts``) is aidream's ``test_kind_output_fields_live.py`` (W2-G4).
"""

from __future__ import annotations

import pytest

from matrx_graph.kind_fields import (
    PLATFORM_KEYS,
    SELF,
    KindEdgeSpec,
    KindFieldsRefused,
    declarations_for,
    fields_for_kind,
    record_values_for,
    title_field_for,
    value_from_record,
)

FLASHCARD_SET = {
    "type": "object",
    "$defs": {"card": {"type": "object", "properties": {"front": {"type": "string"}}}},
    "required": ["__kind", "title", "cards"],
    "properties": {
        "__kind": {"type": "string", "const": "flashcard_set"},
        "title": {"type": "string"},
        "cards": {"type": "array", "items": {"$ref": "#/$defs/card"}},
        "level": {"enum": ["intro", "advanced"], "type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "estimatedMinutes": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
        "price": {"type": "number", "x-matrx-unit": "USD"},
        "shared": {"type": "boolean"},
        "summary": {"type": "string", "maxLength": 4000},
        "due": {"type": ["string", "null"], "format": "date"},
        "_note": {"type": "string"},
    },
}
EDGES = [
    KindEdgeSpec("cards", "flashcard", 0),
    KindEdgeSpec("cards", "enhanced_flashcard", 1),
    {"field_name": "cards", "child_kind": "tiered_flashcard", "position": 2},
]


def _by_key(fields):
    return {f.key: f for f in fields}


def test_a_union_edge_gets_one_relation_field_per_child_kind() -> None:
    got = _by_key(fields_for_kind(FLASHCARD_SET, EDGES, kind="flashcard_set"))
    for child in ("flashcard", "enhanced_flashcard", "tiered_flashcard"):
        f = got[f"cards__{child}"]
        assert f.child_kind == child
        assert f.declaration["type"] == "relation" and f.declaration["multi"] is True
        assert f.declaration["config"] == {"kind_key": "cards", "child_kind": child, "kind_many": True}
        assert "flavor" not in f.declaration and "flavor" not in f.declaration["config"]
        # A many-relation's limit is the seeded records.children.fan_out_ceiling (500), never
        # the store's 25 default — and it follows the ceiling the lander passes in.
        assert f.declaration["relation_max"] == 500
    assert "cards" not in got
    narrowed = _by_key(fields_for_kind(FLASHCARD_SET, EDGES, kind="flashcard_set", children_ceiling=40))
    assert narrowed["cards__flashcard"].declaration["relation_max"] == 40


def test_each_property_maps_by_design_section_2_3() -> None:
    got = _by_key(fields_for_kind(FLASHCARD_SET, EDGES))
    assert got["title"].declaration["type"] == "text"
    assert (got["level"].declaration["type"], got["level"].declaration["options"]) == ("select", ["intro", "advanced"])
    assert got["tags"].declaration["type"] == "long_text" and got["tags"].declaration["config"]["holds_json"] is True
    assert got["estimated_minutes"].declaration["type"] == "number"
    assert got["estimated_minutes"].declaration["config"]["kind_key"] == "estimatedMinutes"
    assert (got["price"].declaration["type"], got["price"].declaration["unit"]) == ("currency", "USD")
    assert got["shared"].declaration["type"] == "checkbox"
    assert got["summary"].declaration["type"] == "long_text"
    assert (got["due"].declaration["type"], got["due"].declaration["kind"]) == ("datetime", "date")
    assert "__kind" not in got and "_note" not in got


def test_platform_fields_are_kept_by_agent_output_with_n_c1_values() -> None:
    fields = fields_for_kind(FLASHCARD_SET, EDGES)
    got = _by_key(fields)
    for key in PLATFORM_KEYS:
        assert got[key].declaration["config"] == {"kept_by": "agent_output"}
    assert got["output_state"].declaration["options"] == ["draft", "superseded"]
    assert got["output_replaced_by"].child_kind == SELF
    assert got["output_replaced_by"].declaration["relation_max"] == 1
    assert [f.key for f in fields][-len(PLATFORM_KEYS) :] == list(PLATFORM_KEYS)
    assert title_field_for(fields) == "title"


def test_a_self_edge_targets_this_table() -> None:
    schema = {"type": "object", "properties": {"yes": {"type": "object"}, "question": {"type": "string"}}}
    got = _by_key(fields_for_kind(schema, [KindEdgeSpec("yes", "decision_node")], kind="decision_node"))
    assert got["yes__decision_node"].child_kind == SELF
    assert got["yes__decision_node"].declaration["relation_max"] == 1


def test_declarations_resolve_targets_and_never_drop_a_child_silently() -> None:
    fields = fields_for_kind(FLASHCARD_SET, EDGES)
    targets = {"flashcard": "t1", "enhanced_flashcard": "t2", "tiered_flashcard": "t3"}
    before = {d["key"] for d in declarations_for(fields, targets)}
    assert "output_replaced_by" not in before  # SELF waits for the table's own id
    after = {d["key"]: d for d in declarations_for(fields, targets, self_table_id="me")}
    assert after["cards__enhanced_flashcard"]["relation_target"] == "t2"
    assert after["output_replaced_by"]["relation_target"] == "me"
    with pytest.raises(KeyError):
        declarations_for(fields, {"flashcard": "t1"})


def test_a_value_splits_into_its_record_and_contained_records_and_back() -> None:
    fields = [f.declaration for f in fields_for_kind(FLASHCARD_SET, EDGES)]
    value = {
        "__kind": "flashcard_set",
        "title": "Post-op knee",
        "tags": ["knee", "rehab"],
        "estimatedMinutes": 12,
        "cards": [
            {"__kind": "flashcard", "front": "Quad set hold?"},
            {"__kind": "enhanced_flashcard", "front": "Heel slide goal?"},
            {"__kind": "flashcard", "front": "Ankle pumps per hour?"},
        ],
    }
    values, children = record_values_for(value, fields)
    assert values == {"title": "Post-op knee", "tags": '["knee", "rehab"]', "estimated_minutes": 12}
    assert [(k, p) for k, p, _ in children] == [
        ("cards__flashcard", 0),
        ("cards__enhanced_flashcard", 1),
        ("cards__flashcard", 2),
    ]
    assert value_from_record(values, children, fields, kind="flashcard_set") == value


def test_a_member_the_table_has_no_field_for_is_refused_by_name() -> None:
    fields = [f.declaration for f in fields_for_kind(FLASHCARD_SET, EDGES[:1])]
    value = {"cards": [{"__kind": "enhanced_flashcard", "front": "Heel slide goal?"}]}
    with pytest.raises(KindFieldsRefused, match="enhanced_flashcard"):
        record_values_for(value, fields)
    with pytest.raises(KindFieldsRefused, match="'nope'"):
        record_values_for({"nope": 1}, fields)


def test_no_two_fields_share_a_label_mkt161() -> None:
    """A property titled ``reason`` (or ``state``, ``agent``…) must not share a label with a platform Field.

    The store refuses a second column with a label it already has, so the whole output was lost.
    """
    schema = {
        "type": "object",
        "properties": {
            "__kind": {"type": "string", "const": "x"},
            "reason": {"type": "string"},
            "State": {"type": "string"},
            "foo_bar": {"type": "string"},
            "fooBar": {"type": "string"},
        },
    }
    labels = [" ".join(str(f.declaration["label"]).split()).lower() for f in fields_for_kind(schema)]
    assert len(labels) == len(set(labels)), labels
    by_key = {f.declaration["key"]: f.declaration["label"] for f in fields_for_kind(schema)}
    assert by_key["output_reason"] == "Reason"
    assert by_key["reason"] == "Reason (2)"
