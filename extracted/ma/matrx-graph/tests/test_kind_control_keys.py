"""Guard W2-G7, pure leg: the control keys are ONE definition with byte-identical twins.

``matrx_graph.kind_control_keys.with_control_keys`` (here) and ``withControlKeys`` in
``@ai-matrx/content-ir`` (``apps/shared/content-ir-core/convert/control-keys.ts``) must produce
the same JSON for the same input. This file owns the shared golden
(``fixtures/kind_control_keys_golden.json``): every input schema below, every mode and flag
combination, serialized canonically. The TS test reads the same file and asserts its own output
equals it, so a change to either twin without the other turns one of the two suites red.

Regenerate after a deliberate change: ``KIND_CONTROL_KEYS_GOLDEN=write uv run pytest <this file>``.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import jsonschema
import pytest

from matrx_graph.kind_control_keys import CONTROL_KEYS, with_control_keys

GOLDEN = Path(__file__).parent / "fixtures" / "kind_control_keys_golden.json"

# Realistic inputs, each a shape the registry or a table kind really carries.
INPUTS: dict[str, dict] = {
    # A closed registry record kind (wine_tasting's live shape).
    "closed_record": {
        "type": "object",
        "additionalProperties": False,
        "required": ["__kind", "wine_name", "vintage", "rating"],
        "properties": {
            "__kind": {"const": "wine_tasting"},
            "wine_name": {"type": "string"},
            "vintage": {"type": "integer"},
            "rating": {"type": "integer", "minimum": 1, "maximum": 100},
            "notes": {"type": "string"},
        },
    },
    # A kind with its OWN allOf (type-dependent required Fields, as a table kind has).
    "typed_record": {
        "type": "object",
        "additionalProperties": False,
        "required": ["__kind", "move_size", "crew_size"],
        "properties": {
            "__kind": {"const": "movers_rate"},
            "move_size": {"type": "string", "enum": ["studio", "two_bedroom", "long_distance"]},
            "crew_size": {"type": "integer"},
            "rate_kind": {"type": "string", "enum": ["hourly", "mileage"]},
            "mileage_rate": {"anyOf": [{"type": "number"}, {"type": "null"}]},
        },
        "allOf": [
            {
                "if": {"properties": {"rate_kind": {"const": "mileage"}}, "required": ["rate_kind"]},
                "then": {"required": ["mileage_rate"]},
            }
        ],
    },
    # Document keywords and $defs stay at the root when a batch moves the record into items.
    "defs_record": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Flashcard set",
        "description": "A deck of study cards.",
        "type": "object",
        "additionalProperties": False,
        "required": ["__kind", "title", "cards"],
        "properties": {
            "__kind": {"const": "flashcard_set"},
            "title": {"type": "string"},
            "cards": {"type": "array", "items": {"$ref": "#/$defs/card"}},
        },
        "$defs": {
            "card": {
                "type": "object",
                "additionalProperties": False,
                "required": ["front", "back"],
                "properties": {"front": {"type": "string"}, "back": {"type": "string"}},
            }
        },
    },
    # Nothing required but the marker — nothing to lift, no branch added.
    "only_marker_required": {
        "type": "object",
        "required": ["__kind"],
        "properties": {"__kind": {"const": "note_card"}, "body": {"type": "string"}},
    },
    # Not an object with properties: returned unchanged.
    "any_value": {},
    "root_form": {"type": "array", "items": {"type": "string"}},
}

COMBOS = (
    ("stored", False, False),
    ("authored", False, False),
    ("authored", False, True),
    ("authored", True, False),
    ("authored", True, True),
)


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _derive() -> dict:
    out: dict = {"inputs": INPUTS, "outputs": {}}
    for name, schema in INPUTS.items():
        for mode, many, allow_edit in COMBOS:
            key = f"{name}|{mode}|many={str(many).lower()}|allow_edit={str(allow_edit).lower()}"
            out["outputs"][key] = with_control_keys(
                schema, mode=mode, many=many, allow_edit=allow_edit
            )
    return out


def test_golden_is_what_python_derives() -> None:
    derived = _derive()
    if os.environ.get("KIND_CONTROL_KEYS_GOLDEN") == "write":
        GOLDEN.write_text(json.dumps(derived, indent=2, sort_keys=True) + "\n")
    golden = json.loads(GOLDEN.read_text())
    assert _canonical(golden["inputs"]) == _canonical(derived["inputs"])
    for key, value in derived["outputs"].items():
        assert _canonical(value) == _canonical(golden["outputs"][key]), (
            f"with_control_keys drifted from the shared golden at {key}; the TS twin "
            f"(withControlKeys) is checked against the same file"
        )


@pytest.mark.parametrize("name", [n for n, s in INPUTS.items() if s.get("properties")])
@pytest.mark.parametrize("combo", COMBOS)
def test_every_output_is_a_valid_schema(name: str, combo: tuple) -> None:
    mode, many, allow_edit = combo
    schema = with_control_keys(INPUTS[name], mode=mode, many=many, allow_edit=allow_edit)
    jsonschema.Draft202012Validator.check_schema(schema)


def test_the_input_is_never_mutated() -> None:
    before = _canonical(INPUTS)
    _derive()
    assert _canonical(INPUTS) == before


def test_shapes_that_are_not_records_are_returned_unchanged() -> None:
    for name in ("any_value", "root_form"):
        for mode, many, allow_edit in COMBOS:
            assert with_control_keys(
                INPUTS[name], mode=mode, many=many, allow_edit=allow_edit
            ) is INPUTS[name]


def test_stored_mode_declares_all_four_and_never_flags() -> None:
    a = with_control_keys(INPUTS["closed_record"], mode="stored")
    b = with_control_keys(INPUTS["closed_record"], mode="stored", many=True, allow_edit=True)
    assert _canonical(a) == _canonical(b)
    assert set(CONTROL_KEYS) <= set(a["properties"])
