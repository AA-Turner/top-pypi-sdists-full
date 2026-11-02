"""Stable reason codes remain available to ValueError handlers."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import ReconciliationValidationError


def test_reason():
    error = ReconciliationValidationError("missing_field")
    assert isinstance(error, ValueError)
    assert error.reason == "missing_field"
    assert str(error) == "missing_field"
