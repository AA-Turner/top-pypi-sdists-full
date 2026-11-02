"""Tests for receipt-preserving repair bookkeeping quota errors."""

from agentic_devtools.cli.ci.provider import RepairDispatchBookkeepingRateLimitError
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_preserves_confirmed_receipt_and_quota_metadata() -> None:
    rate_limit = ProviderRateLimitError(
        retry_after_seconds=30,
        reset_timestamp=1234,
        remaining=0,
        provider="github",
        credential_identity="AI_PR_LOOP_BOOKKEEPING_TOKEN",
        source="response-header",
    )

    error = RepairDispatchBookkeepingRateLimitError("task:owner/repo:9999", rate_limit)

    assert error.receipt == "task:owner/repo:9999"
    assert error.metadata == rate_limit.metadata
    assert error.is_rate_limit
