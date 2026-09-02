"""Tests for _map_retry_exhausted_error."""

from agentic_devtools.orchestration.llm.errors import (
    AuthenticationError,
    ModelNotAvailableError,
    RateLimitExhaustedError,
    RetryExhaustedError,
)
from agentic_devtools.orchestration.llm.providers.copilot import _map_retry_exhausted_error, _StatusError


def test_maps_auth_status_to_authentication_error() -> None:
    error = RetryExhaustedError("exhausted", last_status_code=401)

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert isinstance(mapped, AuthenticationError)


def test_maps_model_not_found_status_to_model_not_available() -> None:
    error = RetryExhaustedError("exhausted", last_status_code=404)

    mapped = _map_retry_exhausted_error(error, model="missing-model", operation="complete")

    assert isinstance(mapped, ModelNotAvailableError)
    assert mapped.model == "missing-model"


def test_maps_preflight_inventory_failures_to_actionable_status() -> None:
    error = RetryExhaustedError("exhausted", last_status_code=503)

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert isinstance(mapped, _StatusError)
    assert mapped.status_code == 503
    assert str(mapped) == "Copilot model inventory is unavailable"


def test_maps_non_inventory_preflight_retry_exhaustion_to_status_error() -> None:
    error = RetryExhaustedError("exhausted", last_status_code=502)

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert isinstance(mapped, _StatusError)
    assert mapped.status_code == 502
    assert str(mapped) == "Copilot request failed"


def test_maps_preflight_timeout_status_to_timeout_error() -> None:
    error = RetryExhaustedError("exhausted", last_status_code=504)

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert isinstance(mapped, _StatusError)
    assert mapped.status_code == 504
    assert str(mapped) == "Copilot request timed out"


def test_preserves_rate_limit_exhaustion_for_preflight_operation() -> None:
    error = RateLimitExhaustedError("rate limited", last_status_code=429)

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert mapped is error


def test_maps_unknown_preflight_retry_exhaustion_to_inventory_status() -> None:
    error = RetryExhaustedError("exhausted")

    mapped = _map_retry_exhausted_error(error, operation="preflight")

    assert isinstance(mapped, _StatusError)
    assert mapped.status_code == 503
    assert str(mapped) == "Copilot model inventory is unavailable"


def test_preserves_unknown_non_preflight_retry_exhaustion() -> None:
    error = RetryExhaustedError("exhausted")

    mapped = _map_retry_exhausted_error(error, operation="stream")

    assert mapped is error


def test_preserves_rate_limit_exhaustion_for_non_preflight_operations() -> None:
    error = RateLimitExhaustedError("rate limited", last_status_code=429)

    mapped = _map_retry_exhausted_error(error, operation="complete")

    assert mapped is error
