"""``{"$uuid5": [values...], "join"?: "json" | "colon", "namespace"?: "<uuid>"}`` — a stable id from values.

Two runs filing the same thing must name ONE record, so the id comes from the values (upsert on
it) rather than from a find-then-add that two concurrent runs both lose. ``json`` (default) is
collision-free; ``colon`` reproduces ids older code wrote as ``uuid5(NAMESPACE_URL, f"{a}:{b}")``.
"""

from __future__ import annotations

import json
from uuid import NAMESPACE_DNS, NAMESPACE_URL, UUID, uuid5

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._template import TemplatePathMissing, substitute_template

ROW = {"sku": "A-1", "size": "m"}
IN = {"shop_id": "s-1"}
TEMPLATE = {"$uuid5": ["order", "$in.shop_id", "$item.sku"]}


def _sub(template, item=None, extra=None):
    return substitute_template(template, {} if item is None else item, index=0, extra=extra or {})


def test_json_is_the_default_the_parts_as_one_compact_json_list() -> None:
    assert _sub(TEMPLATE, ROW, IN) == str(uuid5(NAMESPACE_URL, '["order","s-1","A-1"]'))
    assert _sub({**TEMPLATE, "join": "json"}, ROW, IN) == _sub(TEMPLATE, ROW, IN)


def test_json_never_collides_on_a_separator() -> None:
    assert _sub({"$uuid5": ["a:b", "c"]}) != _sub({"$uuid5": ["a", "b:c"]})
    assert _sub({"$uuid5": ['a","b']}) != _sub({"$uuid5": ["a", "b"]})


def test_json_keeps_types_apart() -> None:
    assert _sub({"$uuid5": [True]}) == str(uuid5(NAMESPACE_URL, "[true]"))
    assert _sub({"$uuid5": [True]}) != _sub({"$uuid5": ["True"]})
    assert _sub({"$uuid5": [5]}) != _sub({"$uuid5": ["5"]})


def test_json_writes_a_uuid_value_as_its_text() -> None:
    u = UUID("0d5c2f6e-1111-4a3b-9c1d-2e3f4a5b6c7d")
    assert _sub({"$uuid5": ["$item"]}, u) == str(uuid5(NAMESPACE_URL, json.dumps([str(u)])))


def test_colon_is_str_of_each_value_joined_like_an_f_string() -> None:
    u = UUID("0d5c2f6e-1111-4a3b-9c1d-2e3f4a5b6c7d")
    got = _sub({"$uuid5": [5, True, "$item"], "join": "colon"}, u)
    assert got == str(uuid5(NAMESPACE_URL, f"5:True:{u}"))


def test_colon_keeps_the_legacy_separator_collision() -> None:
    assert _sub({"$uuid5": ["a:b", "c"], "join": "colon"}) == _sub({"$uuid5": ["a", "b:c"], "join": "colon"})


def test_the_same_values_give_the_same_id_and_different_values_a_different_one() -> None:
    a = _sub(TEMPLATE, ROW, IN)
    assert a == substitute_template(TEMPLATE, dict(ROW), index=7, extra=dict(IN))
    assert a != _sub(TEMPLATE, {**ROW, "sku": "A-2"}, IN)


def test_inside_a_row_template_it_fills_one_column() -> None:
    row = _sub({"id": TEMPLATE, "sku": "$item.sku"}, ROW, IN)
    assert row["sku"] == "A-1" and len(row["id"]) == 36


def test_a_named_namespace_is_used() -> None:
    got = _sub({"$uuid5": ["x"], "namespace": str(NAMESPACE_DNS), "join": "colon"})
    assert got == str(uuid5(NAMESPACE_DNS, "x"))


@pytest.mark.parametrize("item", [{"size": "m"}, {"sku": None}, {"sku": ""}, {"sku": "  "}])
@pytest.mark.parametrize("join", ["json", "colon"])
def test_a_missing_or_blank_value_fails_instead_of_colliding(item, join) -> None:
    with pytest.raises(TemplatePathMissing):
        _sub({**TEMPLATE, "join": join}, item, IN)


def test_optional_around_it_supplies_a_default_when_a_value_is_missing() -> None:
    assert _sub({"$optional": TEMPLATE, "default": None}, {"size": "m"}, IN) is None


@pytest.mark.parametrize("nested", [{"b": 1}, [1, 2]])
def test_a_list_or_record_value_is_refused(nested) -> None:
    with pytest.raises(ExecutionError, match="list or record"):
        _sub({"$uuid5": ["x", "$item"]}, nested)


@pytest.mark.parametrize(
    "bad",
    [
        {"$uuid5": []},
        {"$uuid5": "x"},
        {"$uuid5": ["x"], "namespace": "not-a-uuid"},
        {"$uuid5": ["x"], "join": "pipe"},
        {"$uuid5": ["x"], "other": 1},
    ],
)
def test_a_malformed_ref_fails(bad) -> None:
    with pytest.raises(ExecutionError):
        _sub(bad)


def test_the_namespace_is_a_literal_never_a_ref() -> None:
    with pytest.raises(ExecutionError, match="namespace must be a UUID"):
        _sub({"$uuid5": ["x"], "namespace": "$in.ns"}, extra={"ns": str(NAMESPACE_DNS)})
