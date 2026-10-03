"""Guard W2-G7 (pure legs): the control keys reach the store, and the flags shape what a model sees.

KINDS-GLUE wave 2 §1.4. Before this, the envelope's ``_partition`` moved every key a closed
schema does not declare into residue, so ``_replaces`` vanished from the value, a ``_record_id``
patch failed the kind's required Fields and was never stamped, and a batch could not exist.

STAMP LEG — drives the PRODUCTION ``StreamBlockProcessor`` (detector → partition → validation →
``__ir`` envelope) over a kind-catalog snapshot that knows each kind's disposition, exactly as
``prime_registered_kinds`` fills it. Only the snapshot is injected: it is the seam under test.

SHAPE LEG — ``response_format_for_kind(..., control_keys=True)`` over a resolved registry entry
(the default binds as registered): ``_record_id`` only with
``allow_edit``, the batch root only with ``many``, and the provider lint passes every combination.

Plants that must turn this red (``plant.py``, this file as CMD): replace the kind's ``allOf``
instead of appending → the type-required Field is no longer required; lift only on
``_record_id`` → the batch does not stamp.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks import kind_catalog
from matrx_ai.processing.blocks.block_detector import KIND_BLOCK_TYPE
from matrx_ai.processing.blocks.envelope import IR_ENVELOPE_KEY
from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor

RATE = "movers_rate_card_row"
DECK = "patient_exercise_flashcards"

# A record kind with its OWN allOf: a long-distance rate must name its mileage rate.
RATE_SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "move_size", "crew_size", "hourly_rate"],
    "properties": {
        "__kind": {"const": RATE},
        "move_size": {"type": "string", "enum": ["studio", "two_bedroom", "long_distance"]},
        "crew_size": {"type": "integer", "minimum": 1},
        "hourly_rate": {"type": "number"},
        "rate_kind": {"type": "string", "enum": ["hourly", "mileage"]},
        "mileage_rate": {"type": "number"},
    },
    "allOf": [
        {
            "if": {"properties": {"rate_kind": {"const": "mileage"}}, "required": ["rate_kind"]},
            "then": {"required": ["mileage_rate"]},
        }
    ],
}

# The same shape registered as an ENVELOPE kind: it must not gain the keys.
DECK_SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "title"],
    "properties": {"__kind": {"const": DECK}, "title": {"type": "string"}},
}

ROW = {
    "__kind": RATE,
    "move_size": "two_bedroom",
    "crew_size": 3,
    "hourly_rate": 189.0,
    "rate_kind": "hourly",
}
OUTPUT_ID = "5b0d7a52-8e36-4a43-9b1e-2f1c6d0e9a11"
RECORD_ID = "0f6f2c9e-3d4b-4c1e-8a57-6b2d1e9f4c30"


def _fence(payload: dict) -> str:
    return "Here are Halvorsen's rates.\n\n```json\n" + json.dumps(payload, indent=2) + "\n```\n"


def _run(payload: dict) -> list:
    processor = StreamBlockProcessor()
    text = _fence(payload)
    for i in range(0, len(text), 11):
        processor.process_token(text[i : i + 11])
    processor.finalize()
    return processor.get_blocks()


def _stamped(payload: dict) -> dict | None:
    kinds = [b for b in _run(payload) if b.type == KIND_BLOCK_TYPE]
    if not kinds:
        return None
    envelope = (kinds[0].metadata or {}).get(IR_ENVELOPE_KEY)
    return envelope["root"] if envelope else None


@pytest.fixture
def snapshot():
    kind_catalog.invalidate()
    for slug, schema, disposition in ((RATE, RATE_SCHEMA, "record"), (DECK, DECK_SCHEMA, "envelope")):
        kind_catalog._snapshot[slug] = (schema, 4)
        kind_catalog._known_versions[slug] = 4
        kind_catalog._dispositions[slug] = disposition
    kind_catalog._listing_seen = True
    yield
    kind_catalog.invalidate()


# --------------------------------------------------------------------------- stamp leg


def test_a_plain_row_still_stamps_unchanged(snapshot):
    root = _stamped(ROW)
    assert root is not None and root["kindState"] == "resolved"
    assert root["value"] == ROW


@pytest.mark.parametrize(
    ("label", "payload", "key"),
    [
        ("replaces", {**ROW, "_replaces": OUTPUT_ID}, "_replaces"),
        ("new", {**ROW, "_new": True}, "_new"),
        ("patch", {"__kind": RATE, "_record_id": RECORD_ID, "hourly_rate": 199.0}, "_record_id"),
        (
            "batch",
            {
                "__kind": RATE,
                "_records": [
                    {"move_size": "studio", "crew_size": 2, "hourly_rate": 139.0},
                    {
                        "move_size": "long_distance",
                        "crew_size": 4,
                        "hourly_rate": 245.0,
                        "rate_kind": "mileage",
                        "mileage_rate": 1.85,
                    },
                ],
            },
            "_records",
        ),
        ("reference", {"__kind": RATE, "_record_id": RECORD_ID}, "_record_id"),
    ],
)
def test_every_control_key_stamps_and_stays_in_the_value(snapshot, label, payload, key):
    root = _stamped(payload)
    assert root is not None, f"{label}: a record kind's {key} value got NO envelope"
    assert root["kindState"] == "resolved"
    assert key in root["value"], f"{label}: {key} was partitioned out of root.value"
    assert root["value"][key] == payload[key]
    extra = ((root.get("residue") or {}).get("extra")) or {}
    assert key not in extra, f"{label}: {key} landed in residue"


def test_the_kinds_own_allof_still_holds(snapshot):
    """A long-distance mileage row without its mileage rate is refused (the kind's own branch)."""
    bad = {**ROW, "move_size": "long_distance", "rate_kind": "mileage"}
    assert _stamped(bad) is None, "the kind's own allOf if/then was lost in the wrap"
    good = {**bad, "mileage_rate": 1.85}
    assert _stamped(good) is not None


def test_a_batch_item_is_still_checked_against_the_record(snapshot):
    bad = {"__kind": RATE, "_records": [{"move_size": "studio", "crew_size": "two", "hourly_rate": 139.0}]}
    assert _stamped(bad) is None, "a batch item with a word for crew_size stamped"


def test_a_full_row_missing_a_required_field_is_still_refused(snapshot):
    """The lift is for patches and batches only — a new row still needs its required Fields."""
    bad = {k: v for k, v in ROW.items() if k != "hourly_rate"}
    assert _stamped(bad) is None
    assert _stamped({**bad, "_record_id": None}) is None, "a null _record_id lifted the required Fields"


def test_a_non_record_kind_does_not_gain_the_keys(snapshot):
    assert "_replaces" not in (kind_catalog.registered_kind_schema(DECK) or {}).get("properties", {})
    assert kind_catalog.registered_kind_schema(DECK) is DECK_SCHEMA
    root = _stamped({"__kind": DECK, "title": "Knee rehab", "_replaces": OUTPUT_ID})
    if root is not None:
        assert "_replaces" not in root["value"]


def test_the_registry_row_is_never_edited(snapshot):
    before = json.dumps(RATE_SCHEMA, sort_keys=True)
    kind_catalog.registered_kind_schema(RATE)
    _stamped({**ROW, "_replaces": OUTPUT_ID})
    assert json.dumps(RATE_SCHEMA, sort_keys=True) == before
    assert kind_catalog._snapshot[RATE][0] is RATE_SCHEMA


# --------------------------------------------------------------------------- shape leg


@pytest.fixture
def resolved(monkeypatch):
    from matrx_graph.kinds import KindEntry

    import matrx_ai.kinds as kinds_mod

    entries = {
        RATE: KindEntry(slug=RATE, version=4, json_schema=RATE_SCHEMA, disposition="record"),
        DECK: KindEntry(slug=DECK, version=4, json_schema=DECK_SCHEMA, disposition="envelope"),
    }

    async def fake_get_kind(slug: str):
        return entries.get(slug)

    monkeypatch.setattr(kinds_mod, "get_kind", fake_get_kind)
    return kinds_mod


def _bound_schema(fmt) -> dict:
    return fmt.model_dump(mode="json", by_alias=True, exclude_none=True)["json_schema"]["schema"]


@pytest.mark.parametrize("many", [False, True])
@pytest.mark.parametrize("allow_edit", [False, True])
async def test_the_flags_shape_what_the_model_sees(resolved, many, allow_edit):
    from matrx_ai.schema.lint import lint_output_schema

    fmt = await resolved.response_format_for_kind(
        RATE, control_keys=True, many=many, allow_edit=allow_edit
    )
    assert fmt is not None, "a record kind with control keys could not be bound"
    schema = _bound_schema(fmt)
    props = schema["properties"]
    assert list(props)[0] == "__kind"
    assert "_replaces" in props and "_new" in props
    assert ("_record_id" in props) is allow_edit
    assert ("_records" in props) is many
    if many:
        # The batch root: the Fields moved into the items, none left beside them.
        assert set(props) <= {"__kind", "_records", "_replaces", "_new", "_record_id"}
        assert set(schema["required"]) == {"__kind", "_records"}
        item = props["_records"]["items"]
        assert {"move_size", "crew_size", "hourly_rate"} <= set(item["properties"])
        assert "__kind" not in item["properties"]
    else:
        assert {"move_size", "crew_size", "hourly_rate"} <= set(schema["required"])
        assert not {"_replaces", "_new", "_record_id"} & set(schema["required"])
    report = lint_output_schema(schema)
    assert not report.errors, [f.message for f in report.errors]
    assert report.portable_schema is not None


async def test_a_non_record_kind_is_bound_as_registered(resolved):
    fmt = await resolved.response_format_for_kind(
        DECK, control_keys=True, many=True, allow_edit=True
    )
    assert fmt is not None
    props = _bound_schema(fmt)["properties"]
    assert not set(props) & {"_replaces", "_new", "_record_id", "_records"}


async def test_a_record_kind_is_bound_as_registered_unless_the_run_is_chain_aware(resolved):
    """The default binding carries no control key: only wave 2's router opts in."""
    fmt = await resolved.response_format_for_kind(RATE)
    assert fmt is not None
    props = _bound_schema(fmt)["properties"]
    assert not set(props) & {"_replaces", "_new", "_record_id", "_records"}


async def test_a_flag_without_control_keys_is_refused_loudly(resolved):
    with pytest.raises(ValueError, match="control_keys=True"):
        await resolved.response_format_for_kind(RATE, many=True)
