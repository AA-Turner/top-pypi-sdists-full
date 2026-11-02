import pytest

from agentic_devtools.cli.ci.pipeline.actions.critique_task_binding import confirmed_receipt_accounting_failure
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_confirmed_receipt_accounting_failure_includes_retryable_binding_context() -> None:
    binding_failure = ActionResult(
        name="dispatch_repair",
        decision=ActionDecision.FAILED,
        error="marker unavailable",
    )

    result = confirmed_receipt_accounting_failure(
        "dispatch_repair",
        "task:owner/repo:123",
        RuntimeError("receipt unavailable"),
        binding_failure,
    )

    assert result.decision is ActionDecision.EXECUTE
    assert "receipt unavailable" in (result.error or "")
    assert "marker unavailable" in result.details


def test_confirmed_receipt_accounting_failure_without_binding_issue() -> None:
    result = confirmed_receipt_accounting_failure(
        "dispatch_repair",
        "task:owner/repo:123",
        RuntimeError("receipt unavailable"),
        None,
    )

    assert result.details == (
        "Repair dispatched (receipt=task:owner/repo:123); accounting unresolved: receipt unavailable. "
        "Reconcile authentic task/trigger evidence before any replacement."
    )


def test_confirmed_receipt_accounting_failure_propagates_rate_limit() -> None:
    error = ProviderRateLimitError(provider="github", is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError) as exc_info:
        confirmed_receipt_accounting_failure("dispatch_repair", "task:123", error, None)

    assert exc_info.value is error
