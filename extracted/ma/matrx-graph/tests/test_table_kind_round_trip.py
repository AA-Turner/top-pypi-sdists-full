"""Guard 3 (pure leg): a table is a kind — the derived schemas validate its records and refuse bad ones.

KINDS-GLUE wave 3 §7.1. The facts are ``custom.table_kind_facts`` (N1) verbatim, captured on
live (as admin@admin.com) by ``apps/shared/records/scripts/table-kind-golden.ts`` (slice 0): Halvorsen
Moving's "Movers' Rate Card" (a type field whose Long distance records carry a Mileage rate),
"Home Exercise Programs", and one Field per declaration combination measured on live
(52). Field kinds the captured tables do not hold yet (status, address, barcode, rich_text, count and the
system formulas), a retired choice and an "other values" list are added as SYNTHETIC facts,
named so below.

This file OWNS the shared output golden ``fixtures/table_kind_golden.json``: the facts and every
derived schema, serialized canonically. The TS twin
(``apps/shared/records/src/__tests__/table-kind-round-trip.test.ts``) derives from the same facts
and must equal it byte for byte — assertion (a).

Regenerate after a deliberate change: ``TABLE_KIND_GOLDEN=write uv run pytest <this file>``.
Assertions (b) lint and (c2) the production envelope live in matrx-ai
(``matrx_ai/processing/blocks/tests/test_table_kind_envelope.py``): this package never imports
matrx-ai.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from matrx_graph.executor.schema_validation import validate_instance
from matrx_graph.kind_control_keys import CONTROL_KEYS
from matrx_graph.table_kinds import (
    TableKindFacts,
    authored_schema,
    field_kind_of,
    is_table_kind,
    json_schema_for,
    render_schema,
    render_schema_for,
    stored_schema,
    table_kind_slug,
)

HERE = Path(__file__).parent
GOLDEN = HERE / "fixtures" / "table_kind_golden.json"
CAPTURED = (
    HERE.parent.parent.parent
    / "apps/shared/records/src/__tests__/fixtures/table-kind-facts.golden.json"
)

CEDAR_RIDGE = "23c2ac41-8044-49ed-9af9-35761370e5c0"


def _field(key: str, label: str, **doc: Any) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "multi": False,
        "rules": [],
        "config": {},
        "required": False,
        "applies_to_types": [],
        **doc,
    }


# Kinds the clone holds no Field of today, written the way custom._field_document_for writes them.
SYNTHETIC: dict[str, dict[str, Any]] = {
    "synthetic_crew_dispatch": {
        "organization_id": CEDAR_RIDGE,
        "table_id": "5e7a9c11-2b44-4d0a-9f3e-8c1d2a6b7e01",
        "name": "Crew Dispatch Board",
        "title_field": "job",
        "agent_writable": True,
        "purpose": None,
        "version": 1,
        "type_field": None,
        "stamp": "synthetic",
        "fields": [
            _field("job", "Job", type="text", required=True, rules=[{"kind": "length", "value": "80"}]),
            _field("status", "Status", type="list", format="status", config={"options_table_id": "5e7a9c11-2b44-4d0a-9f3e-8c1d2a6b7e02", "status_groups": {"todo": ["booked"], "in_progress": ["en_route"], "done": ["delivered"]}}),
            _field("pickup_address", "Pickup address", type="text", format="address"),
            _field("dock_barcode", "Dock barcode", type="text", format="barcode", config={"symbology": "code128"}),
            _field("crew_notes", "Crew notes", type="text", format="rich_text"),
            _field("crew_rating", "Crew rating", type="range", format="rating", rules=[{"kind": "max", "value": 10}]),
            _field("drive_time", "Drive time", type="range", format="duration", unit="seconds"),
            _field("stops", "Stops", type="formula", format="count", config={"agg": "count", "via": "stop_list"}),
            _field("dispatched_by", "Dispatched by", type="formula", config={"system": "created_by"}),
            _field("changed_by", "Changed by", type="formula", config={"system": "modified_by"}),
            _field("dispatched_at", "Dispatched at", type="formula", config={"system": "created_time"}),
            _field("changed_at", "Changed at", type="formula", config={"system": "modified_time"}),
            _field("truck", "Truck", type="list", config={"options_table_id": "5e7a9c11-2b44-4d0a-9f3e-8c1d2a6b7e03", "allow_other": True}),
            _field("crew_size", "Crew size", type="range", rules=[{"kind": "min", "value": "1"}, {"kind": "max", "value": 6.0}]),
        ],
        "choices": {
            "status": [
                {"key": "booked", "label": "Booked", "id": "9b1f0e2a-0c3d-4e5f-8a7b-1c2d3e4f5a01", "retired": False, "position": 1},
                {"key": "en_route", "label": "En route", "id": "9b1f0e2a-0c3d-4e5f-8a7b-1c2d3e4f5a02", "retired": False, "position": 2},
                {"key": "delivered", "label": "Delivered", "id": "9b1f0e2a-0c3d-4e5f-8a7b-1c2d3e4f5a03", "retired": False, "position": 3},
                {"key": "on_hold", "label": "On hold", "id": "9b1f0e2a-0c3d-4e5f-8a7b-1c2d3e4f5a04", "retired": True, "position": 4},
            ],
            "truck": [
                {"key": "16_ft", "label": "16 ft box truck", "id": "9b1f0e2a-0c3d-4e5f-8a7b-1c2d3e4f5b01", "retired": False, "position": 1},
            ],
        },
    }
}

# Cedar Ridge's "Checklist steps" — a free_form Table (`columns: "free_form"`) read through
# custom.table_kind_facts on the clone 2026-10-02, PLUS the three facts the door does not carry yet
# and the chair is asked for: `column_source` (custom.table_column_source), `platform_keys`
# (custom.record_platform_keys()) and a per-Field `field_kind` (custom.field_kind_of). SYNTHETIC
# in those three keys only; the facts without them take today's derivation (every other case).
SYNTHETIC["synthetic_checklist_steps_free_form"] = json.loads(
    r'''{"agent_writable": true, "choices": {"status": [{"id": "16285e38-70e7-4c45-97e7-b586b3816126", "key": "blocked", "label": "Blocked", "position": null, "retired": false}, {"id": "325a0422-d3a5-47fc-9b79-d11dcd31439d", "key": "cancelled", "label": "Cancelled", "position": null, "retired": false}, {"id": "3aba3d98-5b2f-4e39-bf84-5d45022080a4", "key": "done", "label": "Done", "position": null, "retired": false}, {"id": "580884ff-7aee-43b1-ba16-b6c0fc3c278d", "key": "in_progress", "label": "In progress", "position": null, "retired": false}, {"id": "3258aff4-45e7-4307-b637-72f823b79ca1", "key": "not_started", "label": "Not started", "position": null, "retired": false}]}, "column_source": "free_form", "fields": [{"applies_to_types": [], "config": {}, "context_policy": "include", "dated": false, "depends_on": [], "entity_definition_id": "2ac98263-a4ab-49f4-a118-56f4b2bc6050", "field_kind": "text", "id": "927c1b9d-5464-45b9-91c0-cb22aad1e463", "key": "title", "label": "Step", "multi": false, "promoted": false, "required": true, "rules": [], "sensitivity": "internal", "sort": 10, "source": "manual", "source_config": {}, "type": "text", "unique": false, "version": 1}, {"applies_to_types": [], "config": {}, "context_policy": "include", "dated": false, "depends_on": [], "entity_definition_id": "2ac98263-a4ab-49f4-a118-56f4b2bc6050", "field_kind": "member", "id": "e8c57630-f526-4a15-a449-67d63e5d86e8", "key": "assignee", "label": "Assignee", "multi": false, "on_target_delete": "set_null", "parity_type": "member", "promoted": true, "relation_max": 1, "relation_target": "11111111-0000-4000-8000-000000000005", "required": false, "rules": [], "sensitivity": "internal", "sort": 900, "source": "manual", "source_config": {}, "type": "relation", "unique": false, "version": 1}, {"applies_to_types": [], "config": {"kind": "date"}, "context_policy": "include", "dated": false, "depends_on": [], "entity_definition_id": "2ac98263-a4ab-49f4-a118-56f4b2bc6050", "field_kind": "datetime", "id": "647495be-3543-49c3-bfa5-12130ef21fea", "key": "due_date", "label": "Due date", "multi": false, "parity_type": "datetime", "promoted": true, "required": false, "rules": [], "sensitivity": "internal", "sort": 910, "source": "manual", "source_config": {}, "type": "range", "unique": false, "version": 1}, {"applies_to_types": [], "config": {"options_table_id": "44c53bc3-f37f-4229-81ab-73aa4e2e3fa4"}, "context_policy": "include", "dated": false, "depends_on": [], "entity_definition_id": "2ac98263-a4ab-49f4-a118-56f4b2bc6050", "field_kind": "select", "id": "35cd36e6-e197-4749-8d9b-7d48f0ef368a", "key": "status", "label": "Status", "multi": false, "parity_type": "select", "promoted": true, "required": false, "rules": [], "sensitivity": "internal", "sort": 920, "source": "manual", "source_config": {}, "type": "list", "unique": false, "version": 1}], "name": "Checklist steps", "organization_id": "23c2ac41-8044-49ed-9af9-35761370e5c0", "platform_keys": ["parent_id"], "purpose": null, "stamp": "synthetic", "table_id": "2ac98263-a4ab-49f4-a118-56f4b2bc6050", "title_field": "title", "type_field": null, "version": 2}'''
)

SYNTHETIC_KINDS = {
    "job": "text",
    "status": "status",
    "pickup_address": "address",
    "dock_barcode": "barcode",
    "crew_notes": "rich_text",
    "crew_rating": "rating",
    "drive_time": "duration",
    "stops": "count",
    "dispatched_by": "created_by",
    "changed_by": "modified_by",
    "dispatched_at": "created_time",
    "changed_at": "modified_time",
    "truck": "select",
    "crew_size": "number",
}


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _cases(captured: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    for name, facts in captured["tables"].items():
        cases[name] = facts
    for combo in captured["combinations"]:
        c = combo["combination"]
        name = "combo:{kind}|{type}|{format}|{multi}|{typed}".format(
            kind=c["kind"] or "-", type=c["type"], format=c["format"] or "-",
            multi=str(c["multi"]).lower(), typed=str(c["typed"]).lower(),
        )
        cases[name] = combo["facts"]
    cases.update(SYNTHETIC)
    return cases


def _derive(facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "stored_fields": json_schema_for(facts, "stored"),
        "authored_fields": json_schema_for(facts, "authored"),
        "render_fields": render_schema_for(facts),
        "stored": stored_schema(facts),
        "authored": authored_schema(facts),
        "authored_many_edit": authored_schema(facts, many=True, allow_edit=True),
        "render": render_schema(facts),
    }


def _golden() -> dict[str, Any]:
    if os.environ.get("TABLE_KIND_GOLDEN") == "write":
        captured = json.loads(CAPTURED.read_text())
        cases = _cases(captured)
        out = {
            "about": "Owned by packages/matrx-graph/tests/test_table_kind_round_trip.py; facts are custom.table_kind_facts verbatim (synthetic_* are named synthetic).",
            "captured": captured["captured"],
            "combination_kinds": {
                name: combo["combination"]["kind"]
                for name, combo in zip(
                    [n for n in cases if n.startswith("combo:")], captured["combinations"], strict=True
                )
            },
            "combination_field_ids": {
                name: combo["field_id"]
                for name, combo in zip(
                    [n for n in cases if n.startswith("combo:")], captured["combinations"], strict=True
                )
            },
            "cases": {name: {"facts": facts, **_derive(facts)} for name, facts in cases.items()},
        }
        GOLDEN.write_text(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    return json.loads(GOLDEN.read_text())


GOLDEN_DATA = _golden()
CASES = GOLDEN_DATA["cases"]


# --------------------------------------------------------------------------- (a) the golden


@pytest.mark.parametrize("name", sorted(CASES))
def test_python_derives_exactly_the_golden(name: str) -> None:
    case = CASES[name]
    derived = _derive(case["facts"])
    for output, value in derived.items():
        assert _canonical(value) == _canonical(case[output]), f"{name}: {output} drifted from the golden"


def test_the_golden_facts_are_the_captured_door_answers() -> None:
    if not CAPTURED.exists():
        pytest.skip("the records package is not beside this checkout — the TS leg checks the same file")
    captured = json.loads(CAPTURED.read_text())
    for name, facts in _cases(captured).items():
        assert _canonical(facts) == _canonical(CASES[name]["facts"]), f"{name}: facts drifted from N1's capture"


def test_coverage_every_measured_combination_and_every_field_kind() -> None:
    combos = [n for n in CASES if n.startswith("combo:")]
    assert len(combos) == 52
    mapping_kinds = set(json.loads((Path(__file__).parent.parent / "matrx_graph" / "table_kind_mapping.json").read_text())["kinds"])
    seen: set[str] = set()
    for case in CASES.values():
        for d in case["facts"]["fields"]:
            kind = field_kind_of(d)
            if kind:
                seen.add(kind)
    assert mapping_kinds <= seen, f"field kinds with no golden case: {sorted(mapping_kinds - seen)}"


@pytest.mark.parametrize("name", sorted(GOLDEN_DATA["combination_kinds"]))
def test_field_kind_of_agrees_with_the_store(name: str) -> None:
    """The store measured each combination's kind with custom.field_kind_of; the twin agrees."""
    facts = CASES[name]["facts"]
    field_id = GOLDEN_DATA["combination_field_ids"][name]
    field = next(d for d in facts["fields"] if d["id"] == field_id)
    assert field_kind_of(field) == GOLDEN_DATA["combination_kinds"][name]


def test_synthetic_kinds() -> None:
    facts = CASES["synthetic_crew_dispatch"]["facts"]
    for d in facts["fields"]:
        assert field_kind_of(d) == SYNTHETIC_KINDS[d["key"]], d["key"]


# --------------------------------------------------------------------------- (c1) validation

RATE_CARD = CASES["movers_rate_card"]["facts"]
SLUG = table_kind_slug(RATE_CARD["table_id"])
STORED = stored_schema(RATE_CARD)

GOOD = {
    "local_two_bedroom": {
        "__kind": SLUG, "rate_name": "Two bedroom local — 3 movers, 20 ft truck", "rate_kind": "local",
        "move_size": "two_bedroom", "crew_size": 3, "truck": "20_ft_box_truck", "hourly_rate": 189,
        "minimum_hours": 3, "fuel_surcharge": 6, "packing_included": False, "valid_from": "2026-10-01",
        "notes": "Weekday rate. Stairs over two flights add $40 per flight.",
        "quote_page": "https://halvorsenmoving.com/quote/two-bedroom-local",
    },
    "long_distance_with_mileage": {
        "__kind": SLUG, "rate_name": "Three bedroom long distance — 4 movers, 26 ft truck",
        "rate_kind": "long_distance", "move_size": "three_bedroom", "crew_size": 4,
        "truck": "26 ft box truck", "hourly_rate": 245, "mileage_rate": 1.85, "packing_included": True,
    },
    "labels_and_nulls": {
        "__kind": SLUG, "rate_name": "Studio local", "move_size": "Studio", "crew_size": 2,
        "hourly_rate": 139, "notes": None, "estimator": None, "booked_move": [],
    },
    "store_envelope_keys": {"__kind": SLUG, "rate_name": "Studio local", "move_size": "studio", "crew_size": 2, "hourly_rate": 139, "_values": {}},
    "reference": {"__kind": SLUG, "_record_id": "0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30"},
    # custom.record_platform_keys(): containment rides every record, a Field or not.
    "inside_a_container": {"__kind": SLUG, "rate_name": "Studio local", "move_size": "studio", "crew_size": 2, "hourly_rate": 139, "parent_id": "0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30"},
    "no_container": {"__kind": SLUG, "rate_name": "Studio local", "move_size": "studio", "crew_size": 2, "hourly_rate": 139, "parent_id": None},
    # The store's id regex is case-insensitive, and its date cast reads more than ISO.
    "ids_and_dates_the_store_reads": {"__kind": SLUG, "rate_name": "Studio local", "move_size": "studio", "crew_size": 2, "hourly_rate": 139, "booked_move": "0F6F2C9E-3D4B-4C1E-8A57-6B2D1E9F4C30", "valid_from": "Oct 1 2026"},
    "patch": {"__kind": SLUG, "_record_id": "0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30", "hourly_rate": 199},
    "batch": {
        "__kind": SLUG,
        "_records": [
            {"rate_name": "One bedroom local", "move_size": "one_bedroom", "crew_size": 2, "hourly_rate": 159},
            {"rate_name": "Four bedroom long distance", "rate_kind": "long_distance", "move_size": "four_bedroom", "crew_size": 5, "hourly_rate": 289, "mileage_rate": 2.1},
        ],
    },
}

BASE = GOOD["local_two_bedroom"]
BAD = {
    "a word in Hourly rate": ({**BASE, "hourly_rate": "one eighty-nine"}, "hourly_rate"),
    "an unknown choice": ({**BASE, "move_size": "mansion"}, "move_size"),
    "a list for one value": ({**BASE, "move_size": ["studio"]}, "move_size"),
    "a missing required Field": ({k: v for k, v in BASE.items() if k != "crew_size"}, "crew_size"),
    "a missing type-required Field": ({**BASE, "rate_kind": "long_distance"}, "mileage_rate"),
    "null in a required Field": ({**BASE, "hourly_rate": None}, "hourly_rate"),
    "an unknown key Discount": ({**BASE, "Discount": 0.1}, "Discount"),
    "two booked moves where one fits": ({**BASE, "booked_move": ["0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30", "5b0d7a52-8e36-4a43-9b1e-2f1c6d0e9a11"]}, "booked_move"),
    "not-a-uuid in Booked move": ({**BASE, "booked_move": "not-a-uuid"}, "booked_move"),
    "not-a-uuid in Estimator": ({**BASE, "estimator": ["not-a-uuid"]}, "estimator"),
    "not a date in Valid from": ({**BASE, "valid_from": "not a date"}, "valid_from"),
    "a parent that is not an id": ({**BASE, "parent_id": "not-a-uuid"}, "parent_id"),
    "a batch item with a word for crew": ({"__kind": SLUG, "_records": [{"rate_name": "x", "move_size": "studio", "crew_size": "two", "hourly_rate": 1}]}, "crew_size"),
}


@pytest.mark.parametrize("name", sorted(GOOD))
def test_every_good_record_validates(name: str) -> None:
    assert validate_instance(STORED, GOOD[name]) == [], name


@pytest.mark.parametrize("name", sorted(BAD))
def test_every_bad_record_is_refused_naming_its_field(name: str) -> None:
    value, field = BAD[name]
    errors = validate_instance(STORED, value)
    assert errors, f"{name} was accepted"
    assert any(field in str(e) for e in errors), f"{name}: no error names {field}: {errors}"


CHECKLIST = CASES["synthetic_checklist_steps_free_form"]["facts"]


def test_a_free_form_table_keeps_any_key_and_still_judges_its_fields() -> None:
    """custom._undeclared_key_guard passes every key on a free_form Table; validate_values still
    judges the Fields it declares. A record the store holds on the clone, verbatim."""
    schema = stored_schema(CHECKLIST)
    step = {
        "__kind": table_kind_slug(CHECKLIST["table_id"]), "ref": "step_1", "role": "front_desk",
        "title": "Verify insurance benefits", "run_id": "de0cda2f-f278-465b-b95d-bd897f295819",
        "status": "done", "assignee": "d64e3ce7-aa1d-4fba-aff5-bf306958d28f",
        "due_date": "2026-09-29T20:21:05.043Z", "evidence": {}, "position": 1,
        "requires": {"kind": "none"}, "template": "New patient intake", "depends_on": [],
        "parent_id": None,
    }
    assert validate_instance(schema, step) == []
    assert validate_instance(schema, {**step, "assignee": "not-a-uuid"})
    assert validate_instance(schema, {**step, "due_date": "not a date"})
    assert validate_instance(schema, {**step, "status": "someday"})


def test_the_doors_field_kind_wins_over_the_derivation() -> None:
    facts = json.loads(json.dumps(CHECKLIST))
    title = next(d for d in facts["fields"] if d["key"] == "title")
    title["field_kind"] = "number"  # the store's word, even where this twin would say text
    assert json_schema_for(facts, "stored")["properties"]["title"] == {"type": "number"}
    del title["field_kind"]
    assert json_schema_for(facts, "stored")["properties"]["title"] == {"type": "string"}


def test_without_the_door_facts_a_table_is_closed_and_parent_id_is_allowed() -> None:
    """Silence means the doctrine: no `column_source` -> `fields`; no `platform_keys` -> the mapping's."""
    facts = {k: v for k, v in CHECKLIST.items() if k not in ("column_source", "platform_keys")}
    schema = json_schema_for(facts, "stored")
    assert schema["additionalProperties"] is False
    assert "parent_id" in schema["properties"]
    assert "additionalProperties" not in json_schema_for(CHECKLIST, "stored")


def test_the_three_fixture_records_written_on_the_clone_validate() -> None:
    """The records the store accepted on the clone (slice 0) are accepted here too."""
    for value in (GOOD["local_two_bedroom"], GOOD["long_distance_with_mileage"]):
        assert validate_instance(STORED, value) == []


# --------------------------------------------------------------------------- (d) authored mode


@pytest.mark.parametrize("name", sorted(CASES))
def test_authored_mode_is_a_plain_object_and_omits_what_no_model_writes(name: str) -> None:
    facts = CASES[name]["facts"]
    authored = json_schema_for(facts, "authored")
    text = json.dumps(authored)
    for word in ('"allOf"', '"if"', '"patternProperties"', '"readOnly"', '"x-matrx-unit"'):
        assert word not in text, f"{name}: authored mode carries {word}"
    for d in facts["fields"]:
        kind = field_kind_of(d)
        omitted = kind in (
            "signature", "attachment", "formula", "lookup", "rollup", "count",
            "created_by", "modified_by", "autonumber", "created_time", "modified_time",
        ) or (kind is None and d.get("type") == "formula")
        assert (d["key"] in authored["properties"]) is not omitted, f"{name}: {d['key']} ({kind})"


@pytest.mark.parametrize("name", sorted(CASES))
def test_every_schema_is_valid_json_schema(name: str) -> None:
    facts = CASES[name]["facts"]
    for schema in (
        stored_schema(facts),
        authored_schema(facts),
        authored_schema(facts, many=True, allow_edit=True),
    ):
        jsonschema.Draft202012Validator.check_schema(schema)


def test_control_keys_shape_authored_mode_and_the_type_branches_survive() -> None:
    plain = authored_schema(RATE_CARD)
    assert "_records" not in plain["properties"] and "_record_id" not in plain["properties"]
    batch = authored_schema(RATE_CARD, many=True, allow_edit=True)
    assert set(batch["properties"]) == {"__kind", "_records", "_replaces", "_new", "_record_id"}
    assert "hourly_rate" in batch["properties"]["_records"]["items"]["properties"]
    stored_branches = [b for b in STORED.get("allOf", []) if "then" in b]
    assert stored_branches and "mileage_rate" in stored_branches[0]["then"]["required"]
    assert set(CONTROL_KEYS) <= set(STORED["properties"])


def test_the_slug() -> None:
    assert is_table_kind(SLUG)
    assert not is_table_kind(SLUG.upper())
    assert not is_table_kind("table_" + RATE_CARD["table_id"].replace("-", "_"))
    assert TableKindFacts.model_validate(RATE_CARD).type_field == "rate_kind"
