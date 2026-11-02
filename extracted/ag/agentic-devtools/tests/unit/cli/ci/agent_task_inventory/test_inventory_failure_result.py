"""Tests for shared inventory exception classification."""

import subprocess
from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import inventory_failure_result
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


@pytest.mark.parametrize(
    ("exception", "category"),
    [
        (RuntimeError("HTTP 404 but not structured"), "provider_unavailable"),
        (OSError("missing executable"), "provider_unavailable"),
        (subprocess.TimeoutExpired("gh", 10), "retrieval_exhausted"),
        (ValueError("bad JSON"), "malformed_response"),
        (TypeError("bad shape"), "malformed_response"),
        (ProviderRateLimitError(is_rate_limit=False), "provider_unavailable"),
    ],
)
def test_classifies_exception_type_without_text_guessing(exception, category) -> None:
    result = inventory_failure_result(exception)
    assert result.failure_category == category
    assert result.http_status is None
    assert result.availability == "unavailable"
    assert result.incomplete_reasons


@pytest.mark.parametrize(
    ("status", "category"),
    [
        (401, "authentication"),
        (403, "permission"),
        (404, "http_not_found"),
        (500, "provider_unavailable"),
    ],
)
def test_structured_http_status_precedes_exception_type(status, category) -> None:
    exception = ValueError("not used for classification")
    setattr(exception, "status_code", status)
    result = inventory_failure_result(exception)
    assert result.failure_category == category
    assert result.http_status == status


def test_real_rate_limits_propagate_unchanged() -> None:
    exception = ProviderRateLimitError(is_rate_limit=True)
    with pytest.raises(ProviderRateLimitError) as caught:
        inventory_failure_result(exception)
    assert caught.value is exception


def test_preserves_explicit_status_from_nested_exception_response() -> None:
    exception = RuntimeError("HTTP request failed")
    setattr(exception, "response", SimpleNamespace(status_code=404))
    result = inventory_failure_result(exception)
    assert result.http_status == 404
    assert result.failure_category == "http_not_found"


def test_retryable_rate_limit_preserves_all_metadata() -> None:
    exception = RetryableError(
        "rate limited",
        retry_after=12.5,
        reset_timestamp=1792632200.0,
        remaining=0,
        provider="github",
        credential_identity="pool-identity",
        source="retry-after-header",
        is_rate_limit=True,
    )
    with pytest.raises(ProviderRateLimitError) as caught:
        inventory_failure_result(exception)
    assert caught.value.retry_after_seconds == 12.5
    assert caught.value.reset_timestamp == 1792632200.0
    assert caught.value.remaining == 0
    assert caught.value.provider == "github"
    assert caught.value.credential_identity == "pool-identity"
    assert caught.value.source == "retry-after-header"
    assert caught.value.is_rate_limit is True
    assert caught.value.__cause__ is exception
