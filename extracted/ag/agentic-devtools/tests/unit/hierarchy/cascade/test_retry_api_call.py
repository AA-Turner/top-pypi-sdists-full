"""Tests for _retry_api_call with exponential backoff (NFR-005)."""

from unittest.mock import patch

import pytest

from agentic_devtools.hierarchy.cascade import _retry_api_call, _RetryAfterError


class TestRetryApiCall:
    """Tests for the retry wrapper function."""

    def test_success_on_first_attempt(self) -> None:
        """Returns value immediately on success."""
        result = _retry_api_call(lambda: "ok")
        assert result == "ok"

    def test_retries_on_runtime_error(self) -> None:
        """Retries up to max_attempts on RuntimeError."""
        call_count = 0

        def flaky() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("transient")
            return "recovered"

        with patch("agentic_devtools.hierarchy.cascade.time.sleep"):
            result = _retry_api_call(flaky, max_attempts=3)
        assert result == "recovered"
        assert call_count == 3

    def test_raises_after_exhaustion(self) -> None:
        """Raises the last RuntimeError after all retries exhausted."""

        def always_fail() -> str:
            raise RuntimeError("permanent failure")

        with (
            patch("agentic_devtools.hierarchy.cascade.time.sleep"),
            pytest.raises(RuntimeError, match="permanent failure"),
        ):
            _retry_api_call(always_fail, max_attempts=3)

    def test_exponential_backoff_delays(self) -> None:
        """Verifies sleep is called with exponential delays: 1, 2, 4 (NFR-005)."""
        call_count = 0

        def fail_three_times() -> str:
            nonlocal call_count
            call_count += 1
            if call_count <= 3:
                raise RuntimeError("fail")
            return "ok"

        with patch("agentic_devtools.hierarchy.cascade.time.sleep") as mock_sleep:
            _retry_api_call(fail_three_times, max_attempts=4)

        assert mock_sleep.call_count == 3
        mock_sleep.assert_any_call(1.0)
        mock_sleep.assert_any_call(2.0)
        mock_sleep.assert_any_call(4.0)

    def test_does_not_retry_non_runtime_errors(self) -> None:
        """Non-RuntimeError exceptions are not retried."""

        def raises_value_error() -> str:
            raise ValueError("not retryable")

        with pytest.raises(ValueError, match="not retryable"):
            _retry_api_call(raises_value_error, max_attempts=3)

    def test_validates_max_attempts_positive(self) -> None:
        """Raises ValueError when max_attempts is not positive."""
        with pytest.raises(ValueError, match="max_attempts must be positive"):
            _retry_api_call(lambda: "ok", max_attempts=0)

        with pytest.raises(ValueError, match="max_attempts must be positive"):
            _retry_api_call(lambda: "ok", max_attempts=-1)

    def test_retry_after_error_uses_provided_delay(self) -> None:
        """_RetryAfterError.retry_after overrides exponential backoff (NFR-005)."""
        call_count = 0

        def fail_once() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _RetryAfterError("HTTP 429", retry_after=30.0)
            return "ok"

        with patch("agentic_devtools.hierarchy.cascade.time.sleep") as mock_sleep:
            result = _retry_api_call(fail_once, max_attempts=3)

        assert result == "ok"
        # Should sleep for the Retry-After value (30s), not exponential backoff (1s)
        mock_sleep.assert_called_once_with(30.0)

    def test_retry_after_error_without_retry_after_uses_backoff(self) -> None:
        """_RetryAfterError with retry_after=None falls back to exponential backoff."""
        call_count = 0

        def fail_once() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise _RetryAfterError("HTTP 429", retry_after=None)
            return "ok"

        with patch("agentic_devtools.hierarchy.cascade.time.sleep") as mock_sleep:
            result = _retry_api_call(fail_once, max_attempts=3)

        assert result == "ok"
        # Falls back to exponential backoff: 1s for first retry
        mock_sleep.assert_called_once_with(1.0)
