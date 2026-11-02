"""Tests for read_reconciliation_lifecycle_inventory."""

from functools import partial
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventoryAvailability, FailureCategory
from agentic_devtools.cli.ci.pipeline.lifecycle_reconciliation_support import read_reconciliation_lifecycle_inventory
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RateLimitMetadata, RetryableError

_EXPECTED_RATE_LIMIT = RateLimitMetadata(
    retry_after_seconds=30.0,
    reset_timestamp=1_800_000_000.0,
    remaining=0,
    provider="github",
    credential_identity="repo-token",
    source="api",
)


def test_read_reconciliation_lifecycle_inventory_forwards_exact_scope():
    provider = MagicMock()

    result = read_reconciliation_lifecycle_inventory(provider, 7, pr_id=None, head_branch="b", head_sha="s")
    provider.list_pr_agent_task_lifecycles.assert_called_once_with(7, head_branch="b", head_sha="s")
    assert result is provider.list_pr_agent_task_lifecycles.return_value

    provider.reset_mock()
    read_reconciliation_lifecycle_inventory(provider, 7, pr_id=99, head_branch="b", head_sha="s")
    provider.list_pr_agent_task_lifecycles.assert_called_once_with(7, pr_id=99, head_branch="b", head_sha="s")


def test_read_reconciliation_lifecycle_inventory_classifies_only_explicit_404():
    provider = MagicMock()
    error = RuntimeError("lifecycle endpoint unavailable")
    error.response = SimpleNamespace(status_code=404)
    provider.list_pr_agent_task_lifecycles.side_effect = error

    result = read_reconciliation_lifecycle_inventory(provider, 7, pr_id=None, head_branch="b", head_sha="s")

    assert result == SessionState(
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
        failure_category=FailureCategory.HTTP_NOT_FOUND,
        http_status=404,
        failure_source="agent-task-lifecycle",
    )
    provider.list_pr_agent_task_lifecycles.assert_called_once_with(7, head_branch="b", head_sha="s")


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (RuntimeError("HTTP 404"), None),
        (RuntimeError("permission denied"), 403),
        (RuntimeError("provider unavailable"), 500),
        (ValueError("invalid lifecycle response"), None),
    ],
)
def test_read_reconciliation_lifecycle_inventory_reraises_non_404_exception(error, status):
    provider = MagicMock()
    if status is not None:
        error.status_code = status
    provider.list_pr_agent_task_lifecycles.side_effect = error

    with pytest.raises(type(error)) as caught:
        read_reconciliation_lifecycle_inventory(provider, 7, pr_id=None, head_branch="b", head_sha="s")

    assert caught.value is error


@pytest.mark.parametrize("is_rate_limit", [True, False])
@pytest.mark.parametrize("error_type", [RetryableError, ProviderRateLimitError])
def test_read_reconciliation_lifecycle_inventory_preserves_rate_limit_exception(error_type, is_rate_limit):
    provider = MagicMock()
    error_factory = (
        partial(RetryableError, "rate limited" if is_rate_limit else "temporary failure")
        if error_type is RetryableError
        else ProviderRateLimitError
    )
    error = error_factory(
        _EXPECTED_RATE_LIMIT.retry_after_seconds,
        reset_timestamp=_EXPECTED_RATE_LIMIT.reset_timestamp,
        remaining=_EXPECTED_RATE_LIMIT.remaining,
        provider=_EXPECTED_RATE_LIMIT.provider,
        credential_identity=_EXPECTED_RATE_LIMIT.credential_identity,
        source=_EXPECTED_RATE_LIMIT.source,
        is_rate_limit=is_rate_limit,
    )
    provider.list_pr_agent_task_lifecycles.side_effect = error

    with pytest.raises(type(error)) as caught:
        read_reconciliation_lifecycle_inventory(provider, 7, pr_id=None, head_branch="b", head_sha="s")

    assert caught.value is error
    assert caught.value.is_rate_limit is is_rate_limit
    assert caught.value.metadata == _EXPECTED_RATE_LIMIT
