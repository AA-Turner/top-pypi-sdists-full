from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import (
    SessionOutcome,
    SessionState,
    _read_task_lifecycle_inventory,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_lookup_failure_retains_http_metadata() -> None:
    provider = MagicMock()
    error = RuntimeError("provider unavailable")
    error.__dict__["status_code"] = 403
    provider.list_pr_agent_task_lifecycles.side_effect = error
    result = _read_task_lifecycle_inventory(provider, 7, pr_id=None, head_branch="", head_sha="")
    assert isinstance(result, SessionState)
    assert result.outcome is SessionOutcome.UNKNOWN
    assert result.http_status == 403
    assert result.failure_category == "permission"


@pytest.mark.parametrize("value", [None, {}, [], "invalid"])
def test_malformed_typed_evidence_is_unavailable(value: object) -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.return_value = value
    result = _read_task_lifecycle_inventory(provider, 7, pr_id=None, head_branch="", head_sha="")
    assert isinstance(result, SessionState)
    assert result.outcome is SessionOutcome.UNKNOWN
    assert result.failure_category == "malformed_response"


def test_retryable_lifecycle_cooldown_preserves_metadata() -> None:
    provider = MagicMock()
    provider.list_pr_agent_task_lifecycles.side_effect = RetryableError(
        provider="github", credential_identity="reader", retry_after=12, is_rate_limit=True
    )
    with pytest.raises(ProviderRateLimitError) as caught:
        _read_task_lifecycle_inventory(provider, 7, pr_id=None, head_branch="", head_sha="")
    assert caught.value.credential_identity == "reader"
    assert caught.value.retry_after_seconds == 12
