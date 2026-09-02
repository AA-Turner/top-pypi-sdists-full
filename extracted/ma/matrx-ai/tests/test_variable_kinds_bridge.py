"""The agent-input bridge — the laws it must obey (§10d-C).

Companion to the cross-language gate (`tests/parity/test_variable_kind_fixture.py`,
which proves the TS twin agrees). This file proves the laws themselves:

1. THE ROUND-TRIP LAW — for the clean subset, fields → variables → fields is
   the identity with zero losses.
2. THE OUT-OF-BAND LAW — a picklist or scope binding NEVER enters the emitted
   schema. Flattening one in would let a caller forge which LIST a value comes
   from; the server resolves that from the agent row alone.
3. NOTHING THROWS — an unknown component type is a recorded loss, because a
   bridge that raises on one odd live row takes a whole campaign down.
4. THE SCHEMA IS REAL — a bare, validating JSON Schema, never the
   `{name, schema, strict}` response-format wrapper (which validates nothing).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.agents.variable_kinds import (
    agent_input_json_schema,
    kind_fields_signature,
    kind_fields_to_variable_definitions,
    variable_definitions_to_kind,
    variable_definitions_to_kind_fields,
)

FIXTURE = (
    Path(__file__).resolve().parent
    / "parity"
    / "fixtures"
    / "variable-kind-bridge.generated.json"
)


def _cases() -> list[dict]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]


# --- 1. the round-trip law -------------------------------------------------

CLEAN_SUBSET = {
    "bare_variable",
    "help_and_default",
    "closed_enum",
    "open_enum",
    "items_enum_checkbox",
    "numeric_bounds",
    "toggles",
    "picklist_static_single",
}


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_fields_survive_a_full_round_trip(case: dict) -> None:
    """fields → variables → fields is the identity for the clean subset."""
    if case["name"] not in CLEAN_SUBSET:
        pytest.skip("documented flattening — covered by the loss assertions instead")
    variables = kind_fields_to_variable_definitions(
        case["fields"], sidecar=case["sidecar"]
    )
    again = variable_definitions_to_kind_fields(variables)
    assert again.fields == case["fields"]
    assert again.sidecar == case["sidecar"]
    assert again.losses == []


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_every_narrowing_is_recorded(case: dict) -> None:
    """A field that lost information says so — silence is the banned outcome."""
    conversion = variable_definitions_to_kind_fields(case["variables"])
    assert [loss.model_dump() for loss in conversion.losses] == case["losses"]


# --- 2. the out-of-band law ------------------------------------------------


def test_a_picklist_binding_never_enters_the_schema() -> None:
    conversion, schema = variable_definitions_to_kind(
        [
            {
                "name": "product",
                "customComponent": {
                    "type": "select",
                    "structured_list": {"listId": "list-xyz", "multiple": True},
                },
            }
        ]
    )
    assert conversion.sidecar["product"]["structuredList"]["listId"] == "list-xyz"
    assert "list-xyz" not in json.dumps(schema)
    assert "structured_list" not in json.dumps(schema)


def test_a_scope_binding_never_enters_the_schema() -> None:
    conversion, schema = variable_definitions_to_kind(
        [
            {
                "name": "company_name",
                "binding": {"itemKey": "company_name", "scopeTypeId": "brand"},
            }
        ]
    )
    assert conversion.sidecar["company_name"]["scopeBinding"]["itemKey"] == "company_name"
    assert "scopeTypeId" not in json.dumps(schema)
    assert schema["properties"]["company_name"] == {"type": "string"}


# --- 3. nothing throws -----------------------------------------------------


def test_an_unknown_component_type_is_a_loss_not_an_exception() -> None:
    conversion = variable_definitions_to_kind_fields(
        [{"name": "legacy", "customComponent": {"type": "text"}}]
    )
    assert conversion.fields["legacy"] == {"type": "string"}
    assert "unknown component type" in conversion.losses[0].reason


def test_junk_entries_are_skipped_not_fatal() -> None:
    conversion = variable_definitions_to_kind_fields(
        [None, "nonsense", {}, {"name": ""}, {"name": "real"}]
    )
    assert list(conversion.fields) == ["real"]


# --- 4. the schema is a real one ------------------------------------------


def test_the_schema_is_bare_and_validating() -> None:
    _, schema = variable_definitions_to_kind(
        [
            {"name": "topic", "required": True},
            {
                "name": "tone",
                "customComponent": {"type": "select", "options": ["warm", "dry"]},
            },
        ]
    )
    # NOT the `{name, schema, strict}` response-format wrapper: that shape is
    # not a validating schema, so every value would pass.
    assert "schema" not in schema
    assert schema["type"] == "object"
    assert schema["required"] == ["topic"]
    assert schema["properties"]["tone"] == {"type": "string", "enum": ["warm", "dry"]}
    assert schema["additionalProperties"] is False


def test_open_enums_keep_their_option_set() -> None:
    """The historical information loss this bridge exists to end."""
    _, schema = variable_definitions_to_kind(
        [
            {
                "name": "format",
                "customComponent": {
                    "type": "radio",
                    "options": ["blog", "email"],
                    "allowOther": True,
                },
            }
        ]
    )
    assert schema["properties"]["format"] == {
        "anyOf": [
            {"type": "string", "enum": ["blog", "email"]},
            {"type": "string"},
        ]
    }


def test_numeric_bounds_reach_the_schema() -> None:
    _, schema = variable_definitions_to_kind(
        [
            {
                "name": "words",
                "customComponent": {"type": "number", "min": 100, "max": 900, "step": 50},
            }
        ]
    )
    assert schema["properties"]["words"] == {
        "type": "number",
        "minimum": 100,
        "maximum": 900,
        "multipleOf": 50,
    }


def test_the_schema_is_draft_valid_for_every_fixture_case() -> None:
    from matrx_graph.executor.schema_validation import schema_validity_errors

    for case in _cases():
        errors = schema_validity_errors(agent_input_json_schema(case["fields"]))
        assert errors == [], f"{case['name']}: {errors}"


# --- the signature the promote-on-reuse rule counts ------------------------


def test_the_signature_ignores_declaration_order_only() -> None:
    a = variable_definitions_to_kind_fields(
        [{"name": "topic"}, {"name": "tone", "required": True}]
    )
    b = variable_definitions_to_kind_fields(
        [{"name": "tone", "required": True}, {"name": "topic"}]
    )
    c = variable_definitions_to_kind_fields([{"name": "topic"}, {"name": "tone"}])
    assert kind_fields_signature(a.fields) == kind_fields_signature(b.fields)
    assert kind_fields_signature(a.fields) != kind_fields_signature(c.fields)
