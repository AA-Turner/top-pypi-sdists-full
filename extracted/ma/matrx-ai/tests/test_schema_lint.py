"""Provider-aware output-schema lint — platform tests.

Every assertion locks a rule the Agent Service schema gate (and the
agent_factory build path) relies on to reject a schema BEFORE a provider 400s on
it at runtime. The lint must run standalone — no host DB config, no provider SDK
— so these tests import only ``matrx_ai.schema``.
"""

from __future__ import annotations

from matrx_ai.schema import (
    check_sample_against_schema,
    lint_output_schema,
)
from matrx_ai.schema.rules import enforce_additional_properties_false


def test_non_dict_schema_is_structural_error() -> None:
    r = lint_output_schema("not a schema")
    assert r.ok is False
    assert any(f.provider == "structural" for f in r.errors)
    assert r.portable_schema is None


def test_non_object_root_rejected_for_all_providers() -> None:
    r = lint_output_schema({"type": "array", "items": {"type": "string"}})
    assert r.ok is False
    assert any(f.provider == "structural" and "object root" in f.message for f in r.errors)
    # Not derivable into a portable schema when the root isn't an object.
    assert r.portable_schema is None


def test_loose_object_is_the_authors_schema_and_is_not_refused() -> None:
    """An open object with an optional field is an AUTHORED schema, not an error:
    every translator's first step (``make_portable``) closes it and widens the
    optional field on the wire, and the answer is pruned back to it. Refusing it
    forced authors to store the portable copy (SCHEMA-TRANSLATION.md §13). The
    findings still say what the strict providers will receive."""
    schema = {"type": "object", "properties": {"a": {"type": "string"}, "b": {"type": "integer"}}}
    r = lint_output_schema(schema)
    assert r.ok is True
    assert not r.errors
    assert any("additionalProperties" in f.message for f in r.findings)
    assert any("Optional fields" in f.message for f in r.findings)
    assert r.portable_schema is not None


def test_portable_schema_is_clean_and_round_trips() -> None:
    schema = {"type": "object", "properties": {"a": {"type": "string"}, "b": {"type": "integer"}}}
    r = lint_output_schema(schema)
    portable = r.portable_schema
    assert portable is not None
    assert portable["additionalProperties"] is False
    assert sorted(portable["required"]) == ["a", "b"]
    # The portable output must itself pass the lint with zero errors.
    assert lint_output_schema(portable).ok is True


def test_portable_enforces_nested_objects() -> None:
    schema = {
        "type": "object",
        "properties": {
            "inner": {"type": "object", "properties": {"z": {"type": "string"}}},
            "list": {"type": "array", "items": {"type": "object", "properties": {"q": {"type": "integer"}}}},
        },
    }
    portable = lint_output_schema(schema).portable_schema

    def shape_of(node: dict) -> dict:
        """The real shape inside the nullable wrapper an OPTIONAL property carries.

        The portable contract lists every property in `required` (every provider
        demands that) and expresses the ones the author left optional as
        `anyOf: [X, {"type": "null"}]`, so `null` can carry "absent" instead of the
        model having to invent a value. The `anyOf` spelling rather than
        `{"type": ["X","null"]}` is measured, not stylistic — every provider
        refuses the type-array form in some combination (see
        `rules.widen_to_nullable`). What this check is about is the nested
        enforcement reaching inside, which it must.
        """
        branches = node.get("anyOf")
        if isinstance(branches, list):
            return next(b for b in branches if b.get("type") != "null")
        return node

    inner = shape_of(portable["properties"]["inner"])
    assert inner["additionalProperties"] is False
    assert inner["required"] == ["z"]
    items = shape_of(portable["properties"]["list"])["items"]
    assert items["additionalProperties"] is False
    assert items["required"] == ["q"]


def test_clean_schema_passes() -> None:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "age"],
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    }
    assert lint_output_schema(schema).ok is True


def test_provider_subset_only_flags_requested() -> None:
    schema = {"type": "object", "properties": {"a": {"type": "string"}}}
    # Google has no additionalProperties/required hard rule — google-only lint
    # of an object-root schema has no errors.
    r = lint_output_schema(schema, providers=("google",))
    assert r.ok is True


def test_google_ref_warning_does_not_flip_ok() -> None:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["x"],
        "properties": {"x": {"$ref": "#/$defs/y"}},
        "$defs": {"y": {"type": "string"}},
    }
    r = lint_output_schema(schema, providers=("google",))
    assert r.ok is True  # warning, not error
    assert any(f.provider == "google" and f.severity == "warning" for f in r.warnings)


def test_sample_consistent_with_schema() -> None:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["n"],
        "properties": {"n": {"type": "integer"}},
    }
    assert check_sample_against_schema({"n": 5}, schema) == []


def test_sample_inconsistent_with_schema_reports() -> None:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["n"],
        "properties": {"n": {"type": "integer"}},
    }
    findings = check_sample_against_schema({"n": "not-an-int"}, schema)
    assert findings
    assert findings[0].severity == "error"
    assert "schema" in findings[0].message.lower()


def test_enforcement_does_not_mutate_input() -> None:
    schema = {"type": "object", "properties": {"a": {"type": "string"}}}
    enforce_additional_properties_false(schema)
    assert "additionalProperties" not in schema  # original untouched
