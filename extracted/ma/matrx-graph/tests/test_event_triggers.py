"""Unit tests for event triggers — EventSourceSpec, the event-input
assembly, and the EventWatcher loop.

DB integration (the capture function, SKIP LOCKED claims, coalescing) is
covered by the live migration; here we exercise the pure pieces against
fake stores, mirroring test_triggers_and_observability.py.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.db.trigger_event_store import TriggerEventRow, build_event_inputs
from matrx_graph.db.trigger_store import (
    TableEventSource,
    TriggerRow,
    event_run_organization_id,
    event_source_json,
)
from matrx_graph.workers.event_watcher import EventWatcher
from pydantic import ValidationError

# ---------------------------------------------------------------------------
# EventSourceSpec
# ---------------------------------------------------------------------------


def test_event_source_defaults():
    spec = TableEventSource(table="workbench.product_capture_item")
    assert spec.operation == "insert"
    assert spec.entity_key_column == "id"
    assert spec.debounce_seconds == 0
    assert spec.input_map == {}


def test_event_source_requires_schema_qualified_table():
    with pytest.raises(ValidationError):
        TableEventSource(table="product_capture_item")
    with pytest.raises(ValidationError):
        TableEventSource(table="workbench.product_capture_item; DROP TABLE x")


def test_event_source_when_pair_enforced():
    with pytest.raises(ValidationError):
        TableEventSource(table="a.b", when_column="status")
    with pytest.raises(ValidationError):
        TableEventSource(table="a.b", when_value="captured")
    spec = TableEventSource(table="a.b", when_column="status", when_value="captured")
    assert spec.when_column == "status"


def test_event_source_rejects_unknown_operation():
    with pytest.raises(ValidationError):
        TableEventSource(table="a.b", operation="delete")  # type: ignore[arg-type]


def test_event_source_new_keys_default_off():
    spec = TableEventSource(table="a.b")
    assert spec.when_from_value is None
    assert spec.organization_scope == "own"


def test_event_source_json_is_unchanged_when_new_keys_are_absent():
    """A spec that does not use the hop or the scope stores the exact pre-0118 JSON."""
    stored = event_source_json(
        {"table": "a.b", "operation": "update", "when_column": "stage", "when_value": "research"}
    )
    assert stored == {
        "source": "table",
        "table": "a.b",
        "operation": "update",
        "when_column": "stage",
        "when_value": "research",
        "entity_key_column": "id",
        "debounce_seconds": 0,
        "input_map": {},
        "include_event": False,
    }
    # A stored row that spelled the defaults out round-trips to the same shape.
    assert event_source_json({**stored, "when_from_value": None, "organization_scope": "own"}) == stored


def test_event_source_hop_is_stored_and_validated():
    stored = event_source_json(
        {
            "table": "workbench.product_capture_item",
            "operation": "update",
            "when_column": "stage",
            "when_value": "research",
            "when_from_value": "analysis",
        }
    )
    assert stored["when_from_value"] == "analysis"
    assert "organization_scope" not in stored
    # The hop needs the to-pair, UPDATE, and a real change.
    with pytest.raises(ValidationError):
        TableEventSource(table="a.b", operation="update", when_from_value="analysis")
    with pytest.raises(ValidationError):
        TableEventSource(
            table="a.b", when_column="stage", when_value="research", when_from_value="analysis"
        )  # operation defaults to insert
    with pytest.raises(ValidationError):
        TableEventSource(
            table="a.b",
            operation="update",
            when_column="stage",
            when_value="research",
            when_from_value="research",
        )


def test_event_source_organization_scope():
    stored = event_source_json({"table": "a.b", "organization_scope": "any"})
    assert stored["organization_scope"] == "any"
    with pytest.raises(ValidationError):
        TableEventSource(table="a.b", organization_scope="everyone")  # type: ignore[arg-type]


def test_event_run_organization_id_follows_the_scope():
    own = {"table": "a.b"}
    anyorg = {"table": "a.b", "organization_scope": "any"}
    store = {"source": "store", "organization_scope": "any"}
    kw = {"event_organization_id": "row-org", "trigger_organization_id": "trigger-org"}
    assert event_run_organization_id(event_source=own, **kw) == "trigger-org"
    assert event_run_organization_id(event_source=None, **kw) == "trigger-org"
    assert event_run_organization_id(event_source=store, **kw) == "trigger-org"
    assert event_run_organization_id(event_source=anyorg, **kw) == "row-org"
    with pytest.raises(ValueError):
        event_run_organization_id(
            event_source=anyorg, event_organization_id=None, trigger_organization_id="trigger-org"
        )


def test_trigger_row_accepts_event_kind():
    row = TriggerRow(
        id="t1",
        definition_id="d1",
        name="on-capture",
        kind="event",
        event_source={"table": "workbench.product_capture_item", "operation": "update"},
    )
    assert row.kind == "event"
    assert row.event_source is not None and row.event_source["operation"] == "update"


# ---------------------------------------------------------------------------
# build_event_inputs
# ---------------------------------------------------------------------------


def _event(payload: dict[str, Any] | None = None, **overrides: Any) -> TriggerEventRow:
    if payload is None:
        payload = {
            "table": "workbench.product_capture_item",
            "operation": "update",
            "entity_key": "item-1",
            "row": {"id": "item-1", "organization_id": "org-1", "status": "captured"},
        }
    base: dict[str, Any] = {
        "id": "e1",
        "trigger_id": "t1",
        "entity_key": "item-1",
        "payload": payload,
    }
    base.update(overrides)
    return TriggerEventRow.model_validate(base)


def test_build_event_inputs_layers_defaults_map_and_opt_in_envelope():
    inputs = build_event_inputs(
        default_inputs={"pipeline": "photos", "item_id": "will-be-overridden"},
        event_source={
            "input_map": {"item_id": "id", "org": "organization_id"},
            "include_event": True,
        },
        event=_event(),
    )
    assert inputs["pipeline"] == "photos"
    assert inputs["item_id"] == "item-1"  # input_map wins over default_inputs
    assert inputs["org"] == "org-1"
    assert inputs["event"]["table"] == "workbench.product_capture_item"
    assert inputs["event"]["row"]["status"] == "captured"
    assert inputs["event"]["entity_key"] == "item-1"


def test_build_event_inputs_envelope_carries_the_raw_key_under_any_scope():
    # organization_scope 'any' queues the row as '<org>:<key>' (a dedupe handle);
    # the envelope still says the row's key, exactly as a hand fire would.
    inputs = build_event_inputs(
        default_inputs=None,
        event_source={"include_event": True, "organization_scope": "any"},
        event=_event(entity_key="org-1:item-1"),
    )
    assert inputs["event"]["entity_key"] == "item-1"


def test_build_event_inputs_envelope_is_opt_in():
    # Default: NO event key — trigger inputs broadcast to entry nodes
    # unfiltered, and an uninvited extra key breaks strict entry schemas.
    inputs = build_event_inputs(
        default_inputs=None,
        event_source={"input_map": {"item_id": "id"}},
        event=_event(),
    )
    assert inputs == {"item_id": "item-1"}


def test_build_event_inputs_skips_missing_columns_and_handles_empty():
    inputs = build_event_inputs(
        default_inputs=None,
        event_source={"input_map": {"nope": "missing_column"}},
        event=_event(),
    )
    assert "nope" not in inputs

    bare = build_event_inputs(
        default_inputs=None,
        event_source={"include_event": True},
        event=_event({}),
    )
    assert bare["event"]["row"] == {}


# ---------------------------------------------------------------------------
# EventWatcher
# ---------------------------------------------------------------------------


class _FakeEventStore:
    def __init__(self, batches: list[list[TriggerEventRow]]) -> None:
        self._batches = batches
        self.fired: list[tuple[str, str]] = []
        self.failed: list[tuple[str, str]] = []
        self.dead: list[tuple[str, str]] = []

    async def claim_due(self, **_kw: Any) -> list[TriggerEventRow]:
        if not self._batches:
            return []
        return self._batches.pop(0)

    async def mark_fired(self, event_id: str, run_id: str) -> None:
        self.fired.append((event_id, run_id))

    async def mark_failed(self, event_id: str, *, error: str, **_kw: Any) -> None:
        self.failed.append((event_id, error))

    async def mark_dead(self, event_id: str, *, error: str) -> None:
        self.dead.append((event_id, error))


class _FakeTriggerStore:
    def __init__(self, triggers: dict[str, TriggerRow | None]) -> None:
        self._triggers = triggers
        self.fires: list[tuple[str, str]] = []
        self.loads: list[str] = []

    async def load(self, trigger_id: str) -> TriggerRow | None:
        self.loads.append(trigger_id)
        return self._triggers.get(trigger_id)

    async def record_fire(self, trigger_id: str, run_id: str) -> None:
        self.fires.append((trigger_id, run_id))


def _trigger(trigger_id: str = "t1", **overrides: Any) -> TriggerRow:
    base: dict[str, Any] = {
        "id": trigger_id,
        "definition_id": "d1",
        "name": f"trig-{trigger_id}",
        "kind": "event",
        "event_source": {"table": "a.b", "operation": "insert"},
    }
    base.update(overrides)
    return TriggerRow.model_validate(base)


async def test_event_watcher_fires_claimed_events_and_records():
    events = [
        _event(id="e1", trigger_id="t1"),
        _event(id="e2", trigger_id="t1", entity_key="item-2"),
    ]
    store = _FakeEventStore([events])
    trig_store = _FakeTriggerStore({"t1": _trigger("t1")})

    fired: list[tuple[str, str]] = []

    async def _fire(trig: TriggerRow, ev: TriggerEventRow) -> str:
        fired.append((trig.id, ev.id))
        return f"run-{ev.id}"

    watcher = EventWatcher(fire_event=_fire, store=store, trigger_store=trig_store)  # type: ignore[arg-type]
    count = await watcher.tick_once()

    assert count == 2
    assert fired == [("t1", "e1"), ("t1", "e2")]
    assert store.fired == [("e1", "run-e1"), ("e2", "run-e2")]
    assert trig_store.fires == [("t1", "run-e1"), ("t1", "run-e2")]
    # Parent trigger loaded once per unique trigger, not per event.
    assert trig_store.loads == ["t1"]


async def test_event_watcher_failure_marks_failed_and_continues():
    events = [
        _event(id="e1", trigger_id="t1"),
        _event(id="e2", trigger_id="t1", entity_key="item-2"),
    ]
    store = _FakeEventStore([events])
    trig_store = _FakeTriggerStore({"t1": _trigger("t1")})

    async def _fire(trig: TriggerRow, ev: TriggerEventRow) -> str:
        if ev.id == "e1":
            raise RuntimeError("simulated fire failure")
        return f"run-{ev.id}"

    watcher = EventWatcher(fire_event=_fire, store=store, trigger_store=trig_store)  # type: ignore[arg-type]
    count = await watcher.tick_once()

    assert count == 2
    assert store.failed and store.failed[0][0] == "e1"
    assert "simulated fire failure" in store.failed[0][1]
    assert store.fired == [("e2", "run-e2")]
    assert trig_store.fires == [("t1", "run-e2")]


async def test_event_watcher_dead_letters_orphaned_and_inactive():
    events = [
        _event(id="e1", trigger_id="missing"),
        _event(id="e2", trigger_id="inactive"),
        _event(id="e3", trigger_id="wrong-kind"),
    ]
    store = _FakeEventStore([events])
    trig_store = _FakeTriggerStore(
        {
            "missing": None,
            "inactive": _trigger("inactive", is_active=False),
            "wrong-kind": _trigger(
                "wrong-kind", kind="manual", event_source=None
            ),
        }
    )

    async def _fire(trig: TriggerRow, ev: TriggerEventRow) -> str:
        raise AssertionError("fire must not be called for orphaned events")

    watcher = EventWatcher(fire_event=_fire, store=store, trigger_store=trig_store)  # type: ignore[arg-type]
    count = await watcher.tick_once()

    assert count == 3
    assert [event_id for event_id, _ in store.dead] == ["e1", "e2", "e3"]
    assert store.fired == [] and store.failed == []


async def test_event_watcher_tick_returns_zero_on_empty():
    store = _FakeEventStore([])
    trig_store = _FakeTriggerStore({})

    async def _fire(trig: TriggerRow, ev: TriggerEventRow) -> str:
        raise AssertionError("fire should not be called when no due events")

    watcher = EventWatcher(fire_event=_fire, store=store, trigger_store=trig_store)  # type: ignore[arg-type]
    assert await watcher.tick_once() == 0


# ---------------------------------------------------------------------------
# event_row_actor — the party a table event serves
# ---------------------------------------------------------------------------


def test_event_row_actor_prefers_updated_by_then_created_by():
    from matrx_graph.db import event_row_actor

    source = {"table": "workbench.product_capture_item", "operation": "update"}
    both = _event(
        {"row": {"id": "i1", "updated_by": "user-b", "created_by": "user-a"}}
    )
    assert event_row_actor(event_source=source, event=both) == "user-b"
    created_only = _event({"row": {"id": "i1", "updated_by": None, "created_by": "user-a"}})
    assert event_row_actor(event_source=source, event=created_only) == "user-a"


def test_event_row_actor_is_none_for_service_rows_and_store_sources():
    from matrx_graph.db import event_row_actor

    source = {"table": "a.b", "operation": "insert"}
    assert event_row_actor(event_source=source, event=_event({"row": {"id": "i1"}})) is None
    # The stringified absences the capture function can leave behind are absences.
    assert (
        event_row_actor(
            event_source=source,
            event=_event({"row": {"id": "i1", "updated_by": "None", "created_by": "null"}}),
        )
        is None
    )
    # A store change carries its own verified actor — never read from the payload.
    store = {"source": "store", "event": "record.updated", "table_id": "t", "operations": ["updated"]}
    assert (
        event_row_actor(event_source=store, event=_event({"row": {"updated_by": "user-x"}}))
        is None
    )
