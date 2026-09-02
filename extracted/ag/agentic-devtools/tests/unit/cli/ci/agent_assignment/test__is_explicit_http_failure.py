"""Tests for _is_explicit_http_failure()."""

from agentic_devtools.cli.ci.agent_assignment import _is_explicit_http_failure
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_returns_true_for_definitive_runtime_error() -> None:
    assert _is_explicit_http_failure(RuntimeError("GitHub API error: gh: HTTP 404 Not Found")) is True


def test_returns_true_for_explicit_rate_limit_retryable_error() -> None:
    assert _is_explicit_http_failure(RetryableError("GitHub API rate limited: gh: API rate limit exceeded")) is True


def test_returns_true_for_explicit_server_error_retryable_error() -> None:
    assert _is_explicit_http_failure(RetryableError("GitHub API server error: gh: 503 Service Unavailable")) is True


def test_returns_true_for_structured_http_five_hundred_error() -> None:
    assert _is_explicit_http_failure(RetryableError("gh: HTTP 503 Service Unavailable")) is True


def test_returns_true_for_provider_rate_limit_wrapping_explicit_http_error() -> None:
    try:
        raise ProviderRateLimitError() from RetryableError("HTTP 429 rate limited")
    except ProviderRateLimitError as exc:
        assert _is_explicit_http_failure(exc) is True


def test_returns_true_for_explicit_cause_chain() -> None:
    try:
        try:
            raise RetryableError("HTTP 429 rate limited")
        except RetryableError as inner:
            raise RuntimeError("wrapper") from inner
    except RuntimeError as exc:
        assert _is_explicit_http_failure(exc) is True


def test_returns_true_for_implicit_exception_context() -> None:
    try:
        try:
            raise RetryableError("gh: HTTP 503 Service Unavailable")
        except RetryableError:
            raise RuntimeError("wrapper without explicit cause")
    except RuntimeError as exc:
        assert _is_explicit_http_failure(exc) is True


def test_returns_false_for_exception_cycle_without_http_error() -> None:
    first = RuntimeError("outer wrapper")
    second = RuntimeError("inner wrapper")
    first.__cause__ = second
    second.__context__ = first

    assert _is_explicit_http_failure(first) is False


def test_returns_false_for_transport_retryable_error() -> None:
    assert _is_explicit_http_failure(RetryableError("connection reset by peer")) is False


def test_returns_false_for_transport_runtime_error() -> None:
    assert _is_explicit_http_failure(RuntimeError("connection reset by peer")) is False
