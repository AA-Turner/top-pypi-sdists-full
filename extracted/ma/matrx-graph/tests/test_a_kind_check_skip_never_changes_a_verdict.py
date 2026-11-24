"""The kind check's copy skip never changes a verdict — or a single error — against the full reduction.

L-SPEED 6e kept a subtree "whose schema accepts anything" as given in the validation copy, and validated against a
schema with its accept-anything positions dropped, claiming "the same verdict by construction". The independent
review (6h, I2) crafted 7 schemas and 6 gave a DIFFERENT verdict: a sibling ``allOf`` branch constraining the same
property or items, ``contains``, ``const`` on the same property, ``uniqueItems`` (markers make equal rows
distinct), and ``unevaluatedProperties: false`` beside the dropped free ``additionalProperties``. A subtree is now
kept only when the accept-anything schema is the ONLY one that reaches it (every container above it plain), and
``additionalProperties``/``items`` stay written whenever an ``unevaluated*`` keyword exists.

This file is the differential guard: the old path (``normalize_nonidentity_markers`` + ``strip_kind_markers`` +
the stored schema) and the live path (``_validate_reduced_copy``) must return the SAME ``(errors, checked)`` on the
reviewer's crafted schemas and on a seeded generated set that mixes every applicator with free positions.
Red before: 6 crafted cases and many generated ones differ.
"""

from __future__ import annotations

import random
from typing import Any

import pytest

from matrx_graph.content_ir.markers import normalize_nonidentity_markers, reduce_for_validation, strip_kind_markers
from matrx_graph.executor.schema_validation import validate_instance_checked
from matrx_graph.kinds import _validate_reduced_copy

J: dict[str, Any] = {"$defs": {"JsonValue": {}}}
FREE: dict[str, Any] = {"$ref": "#/$defs/JsonValue"}


def _full(schema: dict[str, Any], value: Any) -> tuple[list[str], bool]:
    return validate_instance_checked(schema, strip_kind_markers(normalize_nonidentity_markers(value, schema), schema))


CRAFTED: dict[str, tuple[dict[str, Any], Any]] = {
    "allOf sibling closes the same property": (
        {**J, "type": "object", "allOf": [
            {"properties": {"x": FREE}},
            {"properties": {"x": {"type": "object", "properties": {"a": {"type": "integer"}}, "additionalProperties": False}}},
        ]},
        {"x": {"__kind": "row", "a": 1}},
    ),
    "uniqueItems over free items": (
        {**J, "type": "object", "properties": {"items": {"type": "array", "uniqueItems": True, "items": FREE}}},
        {"items": [{"__kind": "a", "v": 1}, {"__kind": "b", "v": 1}]},
    ),
    "unevaluatedProperties beside free additionalProperties": (
        {**J, "type": "object", "properties": {"a": {"type": "integer"}}, "additionalProperties": FREE,
         "unevaluatedProperties": False},
        {"a": 1, "extra": {"z": 1}},
    ),
    "contains over free items": (
        {**J, "type": "object", "properties": {"items": {"type": "array", "items": FREE, "contains": {
            "type": "object", "properties": {"v": {"const": 1}}, "required": ["v"], "additionalProperties": False}}}},
        {"items": [{"__kind": "a", "v": 1}]},
    ),
    "const on the same property in an allOf branch": (
        {**J, "type": "object", "properties": {"cfg": FREE}, "allOf": [{"properties": {"cfg": {"const": {"m": 1}}}}]},
        {"cfg": {"__kind": "k", "m": 1}},
    ),
    "blank marker under a free position, parent closed": (
        {**J, "type": "object", "properties": {"items": {"type": "array", "items": FREE}}, "additionalProperties": False},
        {"items": [{"__kind": "", "v": 1}], "__kind": "list"},
    ),
    "free items typed by an allOf sibling": (
        {**J, "type": "object", "properties": {"items": {"type": "array", "allOf": [
            {"items": FREE}, {"items": {"type": "object", "additionalProperties": {"type": "integer"}}}]}}},
        {"items": [{"__kind": "row", "v": 1}]},
    ),
}


@pytest.mark.parametrize("name", list(CRAFTED))
def test_a_crafted_schema_keeps_its_verdict(name: str) -> None:
    schema, value = CRAFTED[name]
    assert _validate_reduced_copy(schema, value) == _full(schema, value), name


# ── the generated set ─────────────────────────────────────────────────────────────────────────────────────

_KEYS = ("a", "b", "c")


def _free(rng: random.Random) -> Any:
    return rng.choice([{}, dict(FREE), {"title": "t"}, {"$ref": "#/$defs/Alias"}])


def _value(rng: random.Random, depth: int) -> Any:
    roll = rng.random()
    if depth > 3 or roll < 0.25:
        return rng.choice([1, 2, "s", None, True, 1.5])
    if roll < 0.65:
        out: dict[str, Any] = {k: _value(rng, depth + 1) for k in _KEYS if rng.random() < 0.6}
        marker = rng.random()
        if marker < 0.4:
            out["__kind"] = rng.choice(["row", "item", "a"])
        elif marker < 0.55:
            out["__kind"] = ""
        return out
    return [_value(rng, depth + 1) for _ in range(rng.randint(0, 3))]


def _schema(rng: random.Random, depth: int, refs: bool = True) -> Any:
    roll = rng.random()
    if depth > 3 or roll < 0.3:
        return _free(rng) if rng.random() < 0.6 else rng.choice([{"type": "integer"}, {"type": "string"}, {"type": "object"}])
    if roll < 0.65:
        node: dict[str, Any] = {"type": "object", "properties": {k: _schema(rng, depth + 1, refs) for k in _KEYS if rng.random() < 0.7}}
        if rng.random() < 0.2:
            node["properties"]["__kind"] = {"type": "string"}
        if rng.random() < 0.3:
            node["required"] = [rng.choice(_KEYS)]
        if rng.random() < 0.4:
            node["additionalProperties"] = rng.choice([False, _free(rng), {"type": "integer"}])
    else:
        node = {"type": "array", "items": _schema(rng, depth + 1, refs)}
    extras = [
        lambda: {"allOf": [_schema(rng, depth + 1, refs)]},
        lambda: {"anyOf": [_schema(rng, depth + 1, refs), _schema(rng, depth + 1, refs)]},
        lambda: {"oneOf": [_schema(rng, depth + 1, refs), _free(rng)]},
        lambda: {"not": {"type": "integer"}},
        lambda: {"uniqueItems": True},
        lambda: {"contains": _schema(rng, depth + 1, refs)},
        lambda: {"const": _value(rng, 2)},
        lambda: {"enum": [_value(rng, 2), _value(rng, 2)]},
        lambda: {"unevaluatedProperties": False},
        lambda: {"unevaluatedItems": False},
        lambda: {"prefixItems": [_schema(rng, depth + 1, refs)]},
        lambda: {"patternProperties": {"^[ab]$": _schema(rng, depth + 1, refs)}},
        lambda: {"minItems": 2, "maxProperties": 1},
        lambda: {"if": {"required": ["a"]}, "then": _schema(rng, depth + 1, refs)},
        lambda: {"propertyNames": {"maxLength": 1}},
        lambda: {"title": "annotated", "description": "d"},
    ]
    for _ in range(rng.choice([0, 0, 1, 2])):
        node.update(rng.choice(extras)())
    if refs and depth and rng.random() < 0.1:
        node = {"$ref": "#/$defs/Wrapped", "title": "via ref"}
    return node


def _generated(seed: int) -> tuple[dict[str, Any], Any]:
    rng = random.Random(seed)
    body = _schema(rng, 0)
    root = {"$defs": {"JsonValue": {}, "Alias": dict(FREE), "Wrapped": _schema(rng, 2, refs=False)}}
    root.update(body if isinstance(body, dict) else {})
    return root, _value(rng, 0)


GENERATED = 3000


def test_a_generated_schema_set_keeps_every_verdict() -> None:
    skipped = 0
    for seed in range(GENERATED):
        schema, value = _generated(seed)
        full = _full(schema, value)
        live = _validate_reduced_copy(schema, value)
        assert live == full, f"seed {seed}: schema={schema!r} value={value!r}\n  full={full}\n  live={live}"
        if reduce_for_validation(value, schema) != strip_kind_markers(normalize_nonidentity_markers(value, schema), schema):
            skipped += 1
    # The set must actually exercise the skip, or the equality above proves nothing about it.
    assert skipped >= 25, f"only {skipped} of {GENERATED} generated cases kept a subtree as given"
