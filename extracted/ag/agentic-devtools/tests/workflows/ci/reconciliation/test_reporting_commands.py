"""Workflow tests for structured reconciliation reporting."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.observability import ObservationSlaBreach, create_operator_report


def test_reporting_contains_failure_and_breach_metadata() -> None:
    report = create_operator_report(
        failures=[{"record_id": "owner/repo#5", "status": "failure"}],
        sla_breaches=[
            ObservationSlaBreach(
                record_id="owner/repo#5", breached_interval_seconds=1800, observed_at_utc_z="2026-09-15T12:00:00Z"
            )
        ],
    )
    assert report.failures[0]["record_id"] == "owner/repo#5"
    assert report.sla_breaches[0].breached_interval_seconds == 1800
