"""WF-026 — a Workflow can start "When a record changes" (the ``source: 'store'`` arm).

THE USE CASE: a landscaping company texts the crew lead when a Job's Stage changes. The
trigger names the Jobs Table and the Stage field by id; the store's emitter puts one
``workflow.trigger_event`` per change on the engine's queue (``entity_key`` = the outbox
id), and the run receives that change — ids only — as its ``trigger`` input, with
``{record_id, change_id, chain}`` stamped on the run so "what ran on this record" is one
query.

THE BREAKS THESE CATCH:
* the discriminator stops defaulting to ``table`` → every existing event trigger row stops
  validating (``test_a_spec_from_before_the_store_arm_is_still_a_table_trigger``);
* the store arm grows or keeps a ``table`` key → it could match the raw-table emitter,
  which selects on ``event_source->>'table'`` (``test_a_store_trigger_carries_no_table``,
  and against the real function in ``tests/workflow/test_store_trigger_never_matches_the_table_emitter.py``);
* ``build_event_inputs`` / ``event_run_metadata`` build a store run from an event payload
  again (``test_a_store_payload_is_never_trusted``) — the run is built from the outbox row by
  the host's verified fire.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.db import (
    StoreEventSource,
    TableEventSource,
    build_event_inputs,
    event_run_metadata,
    event_source_json,
    validate_event_source,
)
from matrx_graph.db.trigger_event_store import TriggerEventRow
from pydantic import ValidationError

JOBS = "0c6e1f2a-8b3d-4e57-9a10-3f2b7c4d5e61"
STAGE = "ff0041b4-3a76-46b3-aa02-2b7294bd0a78"
JOB_1042 = "a3b4c5d6-e7f8-4a9b-8c0d-1e2f3a4b5c6d"
OUTBOX_ID = "11111111-2222-4333-8444-555555555553"

STAGE_CHANGED = {
    "source": "store",
    "event": "record.updated",
    "table_id": JOBS,
    "operations": ["updated"],
    "field_ids": [STAGE],
}


def test_a_spec_from_before_the_store_arm_is_still_a_table_trigger() -> None:
    legacy = {"table": "workbench.product_capture_item", "operation": "update"}
    spec = validate_event_source(legacy)
    assert isinstance(spec, TableEventSource)
    assert event_source_json(legacy) == {
        "source": "table",
        "table": "workbench.product_capture_item",
        "operation": "update",
        "when_column": None,
        "when_value": None,
        "entity_key_column": "id",
        "debounce_seconds": 0,
        "input_map": {},
        "include_event": False,
    }


def test_a_store_trigger_validates_as_the_store_arm() -> None:
    spec = validate_event_source(STAGE_CHANGED)
    assert isinstance(spec, StoreEventSource)
    assert event_source_json(STAGE_CHANGED) == {
        "source": "store",
        "event": "record.updated",
        "table_id": JOBS,
        "operations": ["updated"],
        "field_ids": [STAGE],
        "via": [],  # chairdoors4_b: empty = any door; form.answered / booking.made imply theirs
        "to": None,
        "debounce_per_record": False,
        "bound_graph_hash": None,  # set by the server when the trigger is turned on
    }


@pytest.mark.parametrize(
    ("label", "spec"),
    [
        ("no table id", {"source": "store", "event": "record.updated"}),
        ("table id not an id", {**STAGE_CHANGED, "table_id": "Jobs"}),
        ("unknown event", {**STAGE_CHANGED, "event": "record.renamed"}),
        ("unknown operation", {**STAGE_CHANGED, "operations": ["archived"]}),
        ("field by name", {**STAGE_CHANGED, "field_ids": ["stage"]}),
        ("a table key on the store arm", {**STAGE_CHANGED, "table": "custom.record"}),
        ("table arm without a table", {"source": "table", "operation": "insert"}),
    ],
)
def test_a_malformed_spec_is_refused(label: str, spec: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        validate_event_source(spec)


def test_a_store_trigger_carries_no_table() -> None:
    """workflow.emit_trigger_events selects ``event_source->>'table' = <watched table>``.
    The stored store arm has no ``table`` key, so that predicate is NULL for it — never true."""
    stored = event_source_json(STAGE_CHANGED)
    assert "table" not in stored
    assert stored["source"] == "store"


def _store_event(payload: dict[str, Any]) -> TriggerEventRow:
    return TriggerEventRow.model_validate(
        {"id": "e1", "trigger_id": "t1", "entity_key": OUTBOX_ID, "payload": payload}
    )


@pytest.mark.parametrize("helper", ["build_event_inputs", "event_run_metadata"])
def test_a_store_payload_is_never_trusted(helper) -> None:
    """Round 4: a trigger editor can INSERT workflow.trigger_event rows, payload included, so
    no helper may build a store run (or its record metadata) from that payload. The refusal
    names the verified fire to use instead."""
    from matrx_graph.db.store_change import StoreChangeRefused

    payload = {"change_id": OUTBOX_ID, "record_id": JOB_1042, "table_id": JOBS,
               "operation": "updated", "changed_field_ids": [STAGE]}
    with pytest.raises(StoreChangeRefused, match="fire_store_event"):
        if helper == "build_event_inputs":
            build_event_inputs(default_inputs=None, event_source=event_source_json(STAGE_CHANGED),
                               event=_store_event(payload))
        else:
            event_run_metadata(event_source=event_source_json(STAGE_CHANGED),
                               event=_store_event(payload))


def test_a_table_event_adds_no_record_metadata() -> None:
    meta = event_run_metadata(
        event_source={"table": "a.b"},
        event=_store_event({"row": {"id": "x"}}),
    )
    assert meta == {}


def test_a_number_that_survives_jsonb_hashes_the_same() -> None:
    """Round 5: -0.0 and 1e20 come back from JSONB as 0 and 10**20; a hash that saw the float
    and then the int caused false holds."""
    from matrx_graph.db.trigger_proof import input_hash

    assert input_hash({"fee": -0.0, "cap": 1e20}, {}) == input_hash({"fee": 0, "cap": 10**20}, {})
    assert input_hash({"fee": 12.5}, {}) != input_hash({"fee": 12}, {})
