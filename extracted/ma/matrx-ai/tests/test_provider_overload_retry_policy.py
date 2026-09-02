from __future__ import annotations

import anthropic
import httpx

from matrx_ai.providers.errors import classify_provider_error


class _StatusError(Exception):
    status_code = 529


def test_anthropic_529_gets_wait_then_suspend_schedule() -> None:
    info = classify_provider_error("anthropic", _StatusError("overloaded_error"))

    assert info.error_type == "provider_overloaded"
    assert info.status_code == 529
    assert info.is_retryable is True
    assert info.retry_schedule == (2.0, 5.0, 10.0, 30.0, 60.0)
    assert [info.get_backoff_delay(i) for i in range(5)] == [2.0, 5.0, 10.0, 30.0, 60.0]
    assert info.details["retry_strategy"] == "provider_overload_wait_then_suspend"


class _QuotaError(Exception):
    status_code = 429


def test_insufficient_balance_429_is_not_retried() -> None:
    info = classify_provider_error(
        "moonshot",
        _QuotaError("exceeded_current_quota_error: account is suspended due to insufficient balance"),
    )

    assert info.error_type == "billing_error"
    assert info.status_code == 429
    assert info.is_retryable is False


def test_anthropic_low_credit_400_is_billing_not_invalid_request() -> None:
    response = httpx.Response(
        400,
        request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
    )
    exception = anthropic.BadRequestError(
        "Your credit balance is too low to access the Anthropic API",
        response=response,
        body={
            "type": "error",
            "error": {
                "type": "invalid_request_error",
                "message": "Your credit balance is too low to access the Anthropic API",
            },
        },
    )
    info = classify_provider_error("anthropic", exception)

    assert info.error_type == "billing_error"
    assert info.status_code == 400
    assert info.is_retryable is False
