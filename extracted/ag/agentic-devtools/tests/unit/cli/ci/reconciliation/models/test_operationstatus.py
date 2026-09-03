"""Tests for OperationStatus."""

from agentic_devtools.cli.ci.reconciliation.models import OperationStatus


def test_contains_expected_values() -> None:
    assert OperationStatus.ACTIVE.value == "active"
    assert OperationStatus.COMPLETED.value == "completed"
    assert OperationStatus.EXPIRED.value == "expired"
