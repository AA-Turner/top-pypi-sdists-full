"""Unit tests for Phase 5b — triggers and observability.

DB integration is covered by the gated Postgres tests. Here we exercise:

- TriggerRow shape + round-trip
- Observability spans are no-ops when OTel isn't configured (never raise)
- cron expression parsing works on realistic schedules
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from matrx_graph.db.trigger_store import TriggerRow, _compute_next_run
from matrx_graph.observability import is_enabled, record_exception, set_attributes, span
from pydantic import ValidationError

# ---------------------------------------------------------------------------
# TriggerRow
# ---------------------------------------------------------------------------


def test_trigger_row_defaults():
    row = TriggerRow(
        id="t1",
        definition_id="d1",
        name="nightly",
        kind="cron",
    )
    assert row.timezone == "UTC"
    assert row.max_steps == 1000
    assert row.is_active is True
    assert row.fire_count == 0
    assert row.default_inputs == {}


def test_trigger_row_requires_name_and_definition():
    with pytest.raises(ValidationError):
        TriggerRow.model_validate({"id": "t1", "kind": "cron", "name": "x"})
    with pytest.raises(ValidationError):
        TriggerRow.model_validate({"id": "t1", "definition_id": "d1", "kind": "cron"})


def test_trigger_row_rejects_unknown_kind():
    with pytest.raises(ValidationError):
        TriggerRow(
            id="t1",
            definition_id="d1",
            name="bogus",
            kind="banana",  # type: ignore[arg-type]
        )


def test_trigger_row_json_roundtrip():
    row = TriggerRow(
        id="t1",
        definition_id="d1",
        name="hourly",
        kind="cron",
        cron_expression="0 * * * *",
        default_inputs={"x": 1, "y": [2, 3]},
        fire_count=4,
    )
    dumped = row.model_dump(mode="json")
    re_parsed = TriggerRow.model_validate(dumped)
    assert re_parsed.name == "hourly"
    assert re_parsed.default_inputs == {"x": 1, "y": [2, 3]}


# ---------------------------------------------------------------------------
# Cron expression evaluation
# ---------------------------------------------------------------------------


def test_compute_next_run_hourly():
    # Minute-aligned, UTC
    base = datetime(2026, 4, 22, 14, 30, 0, tzinfo=UTC)
    next_run = _compute_next_run("0 * * * *", "UTC", base=base)
    assert next_run.tzinfo is not None
    # Next hourly fire after 14:30 is 15:00 UTC
    assert next_run.hour == 15
    assert next_run.minute == 0


def test_compute_next_run_respects_timezone():
    # Midnight in America/New_York is 04:00 or 05:00 UTC depending on DST.
    base = datetime(2026, 6, 15, 10, 0, 0, tzinfo=UTC)  # summer → EDT (UTC-4)
    next_run = _compute_next_run("0 0 * * *", "America/New_York", base=base)
    # Next midnight NY after 10:00 UTC Jun 15 is 04:00 UTC Jun 16 (EDT midnight).
    assert next_run.hour == 4
    assert next_run.day == 16


def test_compute_next_run_rejects_invalid_timezone():
    with pytest.raises(ValueError):
        _compute_next_run("0 * * * *", "Mars/Olympus", base=None)


# ---------------------------------------------------------------------------
# Observability — no-op path
# ---------------------------------------------------------------------------


def test_span_context_manager_yields_without_otel_raising():
    # Regardless of whether OTel is installed, this must not raise.
    with span("workflow.test", run_id="r1", step=0) as sp:
        set_attributes(sp, foo="bar", count=7, nested=[1, 2, 3])
        record_exception(sp, ValueError("decorative"))
    # Never raises


def test_is_enabled_returns_bool():
    assert isinstance(is_enabled(), bool)


def test_set_attributes_coerces_non_primitives():
    # Smoke test the private coercer via set_attributes on an OTel-enabled
    # span is hard to test without the SDK. We just verify the no-op path
    # handles complex values without raising.
    set_attributes(None, obj=object(), dt=datetime.now(UTC), lst=[1, "two"])
