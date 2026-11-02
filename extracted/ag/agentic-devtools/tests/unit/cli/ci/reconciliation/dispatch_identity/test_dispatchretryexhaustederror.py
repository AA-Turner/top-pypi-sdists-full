"""Tests for DispatchRetryExhaustedError."""

from agentic_devtools.cli.ci.reconciliation.dispatch_identity import DispatchRetryExhaustedError


def test_dispatch_retry_exhausted_error_is_a_runtime_error() -> None:
    error = DispatchRetryExhaustedError("retry budget exhausted")

    assert isinstance(error, RuntimeError)
    assert str(error) == "retry budget exhausted"
    assert error.pr_number is None
    assert error.change_id == ""
    assert error.operation_id == ""
