"""Tests for structured operator observability reporting."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.observability import ObservationSlaBreach, create_operator_report


def test_create_operator_report_defaults_to_empty_tuples() -> None:
    report = create_operator_report()
    assert report.failures == ()
    assert report.sla_breaches == ()


def test_create_operator_report_preserves_records() -> None:
    report = create_operator_report(
        failures=[{"record_id": "r1", "status": "failure"}],
        stale_records=[{"record_id": "r2", "status": "stale"}],
        invalidations=[{"record_id": "r3", "status": "invalidated"}],
        lease_conflicts=[{"record_id": "r4", "status": "conflict"}],
        retry_exhaustions=[{"record_id": "r5", "status": "exhausted"}],
        sla_breaches=[
            ObservationSlaBreach(
                record_id="r6", breached_interval_seconds=120, observed_at_utc_z="2026-09-15T12:00:00Z"
            )
        ],
    )
    assert report.failures[0]["record_id"] == "r1"
    assert report.sla_breaches[0].record_id == "r6"
