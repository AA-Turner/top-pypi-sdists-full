"""Tests for ProbeStatus."""

from agentic_devtools.cli.ci.reconciliation.models import ProbeStatus


def test_contains_expected_values() -> None:
    assert ProbeStatus.PENDING.value == "pending"
    assert ProbeStatus.IN_PROGRESS.value == "in_progress"
    assert ProbeStatus.SUCCEEDED.value == "succeeded"
    assert ProbeStatus.FAILED.value == "failed"
    assert ProbeStatus.ALERTABLE.value == "alertable"
