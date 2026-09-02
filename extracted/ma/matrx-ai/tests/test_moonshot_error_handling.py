from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.providers.errors import classify_provider_error


class _MoonshotError(Exception):
    def __init__(
        self,
        status_code: int,
        error_type: str,
        message: str,
        *,
        retry_after: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = {"error": {"type": error_type, "message": message}}
        self.response = (
            SimpleNamespace(headers={"retry-after": retry_after})
            if retry_after is not None
            else None
        )


def test_moonshot_quota_is_a_non_retryable_billing_error() -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(429, "exceeded_current_quota_error", "account balance is insufficient"),
    )

    assert result.error_type == "billing_error"
    assert result.is_retryable is False
    assert result.details["provider_error_type"] == "exceeded_current_quota_error"


def test_moonshot_rate_limit_without_wait_hint_does_not_burn_retries() -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(429, "rate_limit_reached_error", "RPM limit reached"),
    )

    assert result.error_type == "rate_limit"
    assert result.is_retryable is False


def test_moonshot_rate_limit_retries_when_the_provider_supplies_a_wait() -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(
            429,
            "rate_limit_reached_error",
            "RPM limit reached",
            retry_after="2",
        ),
    )

    assert result.error_type == "rate_limit"
    assert result.is_retryable is True
    assert result.retry_after == 2


def test_moonshot_overload_retries() -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(429, "engine_overloaded_error", "engine is overloaded"),
    )

    assert result.error_type == "provider_overloaded"
    assert result.is_retryable is True


def test_moonshot_unknown_response_is_stable_and_safe() -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(418, "future_provider_type", "opaque provider detail"),
    )

    assert result.error_type == "provider_error"
    assert result.is_retryable is False
    assert result.user_message == "Moonshot could not complete this request. Please try again."


@pytest.mark.parametrize(
    ("status_code", "provider_type", "expected_type", "retryable"),
    [
        (400, "content_filter", "content_filtered", False),
        (400, "invalid_request_error", "invalid_request", False),
        (401, "incorrect_api_key_error", "auth_error", False),
        (403, "permission_denied_error", "permission_error", False),
        (404, "resource_not_found_error", "not_found", False),
        (499, "client_closed_request", "provider_request_cancelled", False),
        (500, "server_error", "server_error", True),
        (503, "service_unavailable", "server_error", True),
        (504, "timeout", "provider_timeout", True),
    ],
)
def test_moonshot_documented_errors_have_stable_classifications(
    status_code: int,
    provider_type: str,
    expected_type: str,
    retryable: bool,
) -> None:
    result = classify_provider_error(
        "moonshot",
        _MoonshotError(status_code, provider_type, "provider diagnostic"),
    )

    assert result.error_type == expected_type
    assert result.is_retryable is retryable
