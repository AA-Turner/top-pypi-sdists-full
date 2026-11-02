"""Optional provider compatibility and cooldown normalization."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.approver_preflight import ApproverPreflightResult
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_approver_preflight
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_provider_without_optional_method_is_unsupported() -> None:
    assert _get_approver_preflight(Mock(spec=["get_approver_login"]), "o/r") is None


@pytest.mark.parametrize("result", [None, "", object(), ApproverPreflightResult()])
def test_supported_provider_cannot_return_unsupported_or_empty_evidence(result: object) -> None:
    provider = Mock()
    provider.get_approver_preflight = Mock(return_value=result)
    evidence = _get_approver_preflight(provider, "base/repo")
    assert isinstance(evidence, ApproverPreflightResult)
    provider.get_approver_preflight.assert_called_once_with("base/repo")


def test_lookup_error_is_unknown_not_empty_login() -> None:
    provider = Mock()
    provider.get_approver_preflight = Mock(side_effect=RuntimeError("private raw response"))
    evidence = _get_approver_preflight(provider, "base/repo")
    assert evidence is not None
    assert evidence.blocking_capability == "identity"
    assert "private" not in repr(evidence)


def test_real_retryable_rate_limit_normalizes_with_all_metadata() -> None:
    provider = Mock()
    provider.get_approver_preflight = Mock(
        side_effect=RetryableError(
            "limited",
            retry_after=42,
            reset_timestamp=123,
            remaining=0,
            provider="github",
            credential_identity="AGDT_PR_APPROVER_PAT",
            source="retry-after",
            is_rate_limit=True,
        )
    )
    with pytest.raises(ProviderRateLimitError) as caught:
        _get_approver_preflight(provider, "o/r")
    error = caught.value
    assert (error.retry_after_seconds, error.reset_timestamp, error.remaining) == (42, 123, 0)
    assert (error.provider, error.credential_identity, error.source) == (
        "github",
        "AGDT_PR_APPROVER_PAT",
        "retry-after",
    )
    assert provider.get_approver_preflight.call_count == 1


@pytest.mark.parametrize(
    "error",
    [
        RetryableError("transient", is_rate_limit=False),
        ProviderRateLimitError(),
    ],
)
def test_unrelated_transients_and_normalized_rate_limits_propagate(error: Exception) -> None:
    provider = Mock()
    provider.get_approver_preflight = Mock(side_effect=error)
    with pytest.raises(type(error)) as caught:
        _get_approver_preflight(provider, "o/r")
    assert caught.value is error
