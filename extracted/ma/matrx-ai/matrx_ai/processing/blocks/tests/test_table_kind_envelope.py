"""Guard 3 (pure leg), the two assertions that need matrx-ai: (b) the provider lint, (c2) the envelope.

KINDS-GLUE wave 3 §7.1. The facts and derived schemas are the golden
``packages/matrx-graph/tests/fixtures/table_kind_golden.json`` (owned by
``test_table_kind_round_trip.py``; facts = ``custom.table_kind_facts`` verbatim from the clone).

(b) every authored schema — plain, and the batch with edit rights — lints for OpenAI, Anthropic
and Google with no error and a portable form.

(c2) drives the PRODUCTION ``StreamBlockProcessor`` over a fenced ``table:<uuid>`` record of
Halvorsen Moving's "Movers' Rate Card", with the kind catalog holding the table's stored schema
(what wave 3's ``prime_table_kinds`` overlay will hold): a type-wrong record yields no envelope;
the unknown key ``Discount`` is partitioned to residue and named there; a batch keeps ``_records``
and a reference keeps ``_record_id`` in the value. Plant: build the stored schema without
``with_control_keys`` → the batch and the reference lose their keys → red.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_graph.table_kinds import authored_schema, stored_schema, table_kind_slug

from matrx_ai.processing.blocks import kind_catalog
from matrx_ai.processing.blocks.block_detector import KIND_BLOCK_TYPE
from matrx_ai.processing.blocks.envelope import IR_ENVELOPE_KEY
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor
from matrx_ai.schema.lint import lint_output_schema

GOLDEN = (
    Path(__file__).resolve().parents[5]
    / "matrx-graph/tests/fixtures/table_kind_golden.json"
)
CASES = json.loads(GOLDEN.read_text())["cases"]
RATE_CARD = CASES["movers_rate_card"]["facts"]
SLUG = table_kind_slug(RATE_CARD["table_id"])

BASE = {
    "__kind": SLUG,
    "rate_name": "Two bedroom local — 3 movers, 20 ft truck",
    "rate_kind": "local",
    "move_size": "two_bedroom",
    "crew_size": 3,
    "truck": "20_ft_box_truck",
    "hourly_rate": 189,
    "minimum_hours": 3,
    "fuel_surcharge": 6,
    "packing_included": False,
    "valid_from": "2026-10-01",
}


# --------------------------------------------------------------------------- (b) lint


@pytest.mark.parametrize("name", sorted(CASES))
@pytest.mark.parametrize("flags", [{}, {"many": True, "allow_edit": True}])
def test_every_authored_schema_binds_on_every_provider(name: str, flags: dict) -> None:
    schema = authored_schema(CASES[name]["facts"], **flags)
    report = lint_output_schema(schema)
    assert not report.errors, [f"{f.provider} {f.path}: {f.message}" for f in report.errors]
    assert report.portable_schema is not None


# --------------------------------------------------------------------------- (c2) envelope


@pytest.fixture
def table_in_catalog():
    kind_catalog.invalidate()
    kind_catalog._snapshot[SLUG] = (stored_schema(RATE_CARD), int(RATE_CARD["version"] or 1))
    kind_catalog._known_versions[SLUG] = int(RATE_CARD["version"] or 1)
    kind_catalog._listing_seen = True
    yield
    kind_catalog.invalidate()


def _root(payload: dict) -> dict | None:
    processor = StreamBlockProcessor()
    text = "Here is Halvorsen's rate.\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n"
    for i in range(0, len(text), 17):
        processor.process_token(text[i : i + 17])
    processor.finalize()
    kinds = [b for b in processor.get_blocks() if b.type == KIND_BLOCK_TYPE]
    if not kinds:
        return None
    envelope = (kinds[0].metadata or {}).get(IR_ENVELOPE_KEY)
    return envelope["root"] if envelope else None


def test_a_good_record_stamps(table_in_catalog):
    root = _root(BASE)
    assert root is not None and root["kind"] == SLUG and root["kindState"] == "resolved"


@pytest.mark.parametrize(
    "bad",
    [
        {**BASE, "hourly_rate": "one eighty-nine"},
        {**BASE, "move_size": "mansion"},
        {**BASE, "move_size": ["studio"]},
        {**BASE, "rate_kind": "long_distance"},
        {**BASE, "hourly_rate": None},
    ],
    ids=["word in hourly rate", "unknown choice", "list for one value", "missing mileage rate", "null required"],
)
def test_a_type_wrong_record_yields_no_envelope(table_in_catalog, bad):
    assert _root(bad) is None


def test_an_unknown_key_is_partitioned_to_residue_and_named(table_in_catalog):
    root = _root({**BASE, "Discount": 0.1})
    assert root is not None, "a record with one unknown key lost its whole envelope"
    assert "Discount" not in root["value"]
    assert "Discount" in ((root.get("residue") or {}).get("extra") or {})


def test_a_batch_keeps_its_records(table_in_catalog):
    batch = {
        "__kind": SLUG,
        "_records": [
            {"rate_name": "One bedroom local", "move_size": "one_bedroom", "crew_size": 2, "hourly_rate": 159},
            {"rate_name": "Four bedroom long distance", "rate_kind": "long_distance", "move_size": "four_bedroom", "crew_size": 5, "hourly_rate": 289, "mileage_rate": 2.1},
        ],
    }
    root = _root(batch)
    assert root is not None, "a batch of rate-card rows got no envelope"
    assert root["value"]["_records"] == batch["_records"]


def test_a_reference_keeps_its_record_id(table_in_catalog):
    ref = {"__kind": SLUG, "_record_id": "0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30"}
    root = _root(ref)
    assert root is not None, "a dropped record reference got no envelope"
    assert root["value"]["_record_id"] == ref["_record_id"]
