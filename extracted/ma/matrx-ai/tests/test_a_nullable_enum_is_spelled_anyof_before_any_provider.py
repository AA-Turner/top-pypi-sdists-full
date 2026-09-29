"""A nullable enum reaches every provider as ``anyOf`` branches, and the lint names it.

Anthropic refused this exact live contract at run time (2026-09-28):

    output_config.format.schema: Invalid schema: Enum value 'victim' does not
    match declared type '['string', 'null']'

It is the shape every Pydantic ``Optional[SomeEnum]`` emits. ``make_portable`` —
the shared first step of every provider translator — must rewrite it to the one
spelling all three providers accept, keeping the description, and
``lint_output_schema`` must say so instead of returning an empty report.

Siblings of the class, each covered below: the type array with no null in the
enum, a ``const`` beside a type array (``const`` becomes ``enum: [X]`` first), a
null enum member beside a SCALAR type, and the same shapes nested in ``items`` /
``$defs`` / a non-object root.
"""

from __future__ import annotations

from matrx_ai.schema.lint import lint_output_schema, make_portable
from matrx_ai.schema.rules import (
    express_nullable_as_anyof,
    split_enum_from_type_union,
    structured_output_schema_violations,
)

REFUSED = {
    "type": ["string", "null"],
    "enum": ["victim", "accidental", "preventable", "open", None],
    "description": "Who the crisis happened to.",
}
ACCEPTED = {
    "description": "Who the crisis happened to.",
    "anyOf": [
        {"type": "string", "enum": ["victim", "accidental", "preventable", "open"]},
        {"type": "null"},
    ],
}


def _root(prop: dict) -> dict:
    return {
        "type": "object",
        "properties": {"crisis_type": prop},
        "required": ["crisis_type"],
        "additionalProperties": False,
    }


def test_the_refused_live_schema_becomes_the_accepted_form() -> None:
    out = make_portable(_root(REFUSED))
    assert out["properties"]["crisis_type"] == ACCEPTED
    assert structured_output_schema_violations(out) == []


def test_the_lint_names_the_refused_shape_for_anthropic() -> None:
    report = lint_output_schema(_root(REFUSED))
    hits = [f for f in report.findings if f.path == "#/properties/crisis_type"]
    assert hits, report.findings
    assert hits[0].provider == "anthropic"
    assert "anyOf" in hits[0].message
    # The lint's own portable copy is repaired too.
    assert report.portable_schema["properties"]["crisis_type"] == ACCEPTED


def test_the_accepted_form_is_clean_and_untouched() -> None:
    assert make_portable(_root(ACCEPTED))["properties"]["crisis_type"] == ACCEPTED
    report = lint_output_schema(_root(ACCEPTED))
    assert not [f for f in report.findings if f.path == "#/properties/crisis_type"]


def test_no_null_in_the_enum_is_still_the_type_array_refusal() -> None:
    prop = {"type": ["string", "null"], "enum": ["a", "b"]}
    out = make_portable(_root(prop))["properties"]["crisis_type"]
    assert out == {"anyOf": [{"type": "string", "enum": ["a", "b"]}, {"type": "null"}]}


def test_const_beside_a_type_array() -> None:
    prop = {"type": ["string", "null"], "const": "only"}
    out = make_portable(_root(prop))["properties"]["crisis_type"]
    assert out == {"anyOf": [{"type": "string", "enum": ["only"]}, {"type": "null"}]}
    assert lint_output_schema(_root(prop)).findings


def test_null_member_beside_a_scalar_type() -> None:
    prop = {"type": "string", "enum": ["a", None], "title": "T"}
    out = make_portable(_root(prop))["properties"]["crisis_type"]
    # `type: "string"` already refuses null, so the null member admits nothing:
    # dropping it is the identical constraint (widening to null would let the
    # model answer a value the author's own schema then refuses).
    assert out == {"type": "string", "enum": ["a"], "title": "T"}
    assert lint_output_schema(_root(prop)).findings


def test_other_constraints_stay_on_the_branch() -> None:
    prop = {"type": ["string", "null"], "enum": ["a", None], "minLength": 1, "default": None}
    assert split_enum_from_type_union(prop) == {
        "default": None,
        "anyOf": [{"type": "string", "enum": ["a"], "minLength": 1}, {"type": "null"}],
    }


def test_nested_in_items_defs_and_a_non_object_root() -> None:
    schema = {
        "type": "object",
        "properties": {"rows": {"type": "array", "items": {"$ref": "#/$defs/Row"}}},
        "required": ["rows"],
        "additionalProperties": False,
        "$defs": {
            "Row": {
                "type": "object",
                "properties": {"k": {"type": ["integer", "null"], "enum": [1, 2, None]}},
                "required": ["k"],
                "additionalProperties": False,
            }
        },
    }
    out = make_portable(schema)
    assert out["$defs"]["Row"]["properties"]["k"] == {
        "anyOf": [{"type": "integer", "enum": [1, 2]}, {"type": "null"}]
    }
    assert any(f.path == "#/$defs/Row/properties/k" for f in lint_output_schema(schema).findings)
    assert make_portable({"type": "array", "items": dict(REFUSED)})["items"] == ACCEPTED


def test_express_nullable_as_anyof_does_not_duplicate_the_enum() -> None:
    out = express_nullable_as_anyof({"type": ["string", "null"], "enum": ["a"], "description": "d"})
    assert out == {"description": "d", "anyOf": [{"type": "string", "enum": ["a"]}, {"type": "null"}]}


def test_idempotent() -> None:
    once = make_portable(_root(REFUSED))
    assert make_portable(once) == once
