"""Tests for retry_with_backoff utility."""

import math
from typing import Any, cast
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.retry import (
    DEFAULT_INITIAL_DELAY,
    DEFAULT_MAX_DELAY,
    DEFAULT_MAX_RETRIES,
    RetryableError,
    retry_with_backoff,
)


class TestRetryWithBackoff:
    """Tests for the retry_with_backoff decorator."""

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_no_retry_on_success(self, mock_sleep) -> None:
        call_count = 0

        @retry_with_backoff()
        def succeeds():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = succeeds()
        assert result == "ok"
        assert call_count == 1
        mock_sleep.assert_not_called()

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_retries_on_retryable_error(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=3)
        def fails_twice():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise RetryableError("transient failure")
            return "recovered"

        result = fails_twice()
        assert result == "recovered"
        assert attempts == 3
        assert mock_sleep.call_count == 2

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_raises_rate_limit_after_max_retries(self, mock_sleep) -> None:
        @retry_with_backoff(max_retries=5)
        def always_fails():
            raise RetryableError("always fails", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            always_fails()

        # Should have slept 5 times (once per retry)
        assert mock_sleep.call_count == 5

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_honors_retry_after(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=2)
        def fails_with_retry_after():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError("rate limited", retry_after=10.0)
            return "ok"

        result = fails_with_retry_after()
        assert result == "ok"
        mock_sleep.assert_called_once_with(10.0)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_long_retry_after_raises_immediately_without_sleeping(self, mock_sleep) -> None:
        @retry_with_backoff(max_delay=60.0, max_retries=2)
        def rate_limited():
            raise RetryableError("rate limited", retry_after=3600.0, provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            rate_limited()

        assert exc_info.value.retry_after_seconds == 3600.0
        mock_sleep.assert_not_called()

    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_long_reset_timestamp_raises_immediately_without_sleeping(self, mock_sleep, _mock_time) -> None:
        @retry_with_backoff(max_delay=60.0, max_retries=2)
        def rate_limited():
            raise RetryableError(
                "rate limited",
                reset_timestamp=1000.0,
                provider="github",
                is_rate_limit=True,
            )

        with pytest.raises(ProviderRateLimitError) as exc_info:
            rate_limited()

        assert exc_info.value.reset_timestamp == 1000.0
        mock_sleep.assert_not_called()

    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_reset_timestamp_exceeding_budget_with_safety_margin_raises(self, mock_sleep, _mock_time) -> None:
        @retry_with_backoff(max_delay=60.0, max_retries=2)
        def rate_limited():
            raise RetryableError("rate limited", reset_timestamp=155.0, provider="github", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            rate_limited()

        assert exc_info.value.reset_timestamp == 155.0
        mock_sleep.assert_not_called()

    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_reset_timestamp_budget_boundary_retries(self, mock_sleep, _mock_time) -> None:
        attempts = 0

        @retry_with_backoff(max_delay=60.0, max_retries=1)
        def rate_limited_once():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError("rate limited", reset_timestamp=150.0, provider="github", is_rate_limit=True)
            return "ok"

        assert rate_limited_once() == "ok"
        assert attempts == 2
        mock_sleep.assert_called_once_with(60.0)

    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_short_retry_after_with_long_reset_timestamp_keeps_retrying(self, mock_sleep, _mock_time) -> None:
        """retry_after takes precedence: a short Retry-After with a distant reset timestamp retries."""
        attempts = 0

        @retry_with_backoff(max_delay=60.0, max_retries=1)
        def rate_limited_once():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError(
                    "rate limited",
                    retry_after=10.0,
                    reset_timestamp=4000.0,
                    provider="github",
                    is_rate_limit=True,
                )
            return "ok"

        assert rate_limited_once() == "ok"
        assert attempts == 2
        mock_sleep.assert_called_once_with(10.0)

    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_rate_limit_reset_timestamp_within_budget_waits_until_reset(self, mock_sleep, _mock_time) -> None:
        attempts = 0

        @retry_with_backoff(max_delay=60.0, max_retries=1)
        def rate_limited_once():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError("rate limited", reset_timestamp=120.0, provider="github", is_rate_limit=True)
            return "ok"

        assert rate_limited_once() == "ok"
        assert attempts == 2
        mock_sleep.assert_called_once_with(30.0)

    @pytest.mark.parametrize("reset_timestamp", ["invalid", math.nan])
    @patch("agentic_devtools.cli.ci.retry.time.time", return_value=100.0)
    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_invalid_reset_timestamp_falls_back_to_retry(self, mock_sleep, _mock_time, reset_timestamp) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=1)
        def rate_limited_once():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError(
                    "rate limited",
                    reset_timestamp=reset_timestamp,
                    provider="github",
                    is_rate_limit=True,
                )
            return "ok"

        assert rate_limited_once() == "ok"
        assert attempts == 2
        mock_sleep.assert_called_once()

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_long_retry_after_non_rate_limit_keeps_retrying(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_delay=60.0, max_retries=1)
        def transient_server_error():
            nonlocal attempts
            attempts += 1
            raise RetryableError("server error", retry_after=3600.0, provider="github", is_rate_limit=False)

        with pytest.raises(RetryableError):
            transient_server_error()

        assert attempts == 2
        assert mock_sleep.call_count == 1

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_exponential_backoff(self, mock_sleep) -> None:
        """Verify delay increases exponentially."""
        attempts = 0

        @retry_with_backoff(initial_delay=1.0, max_delay=60.0, max_retries=3, jitter_factor=0.0)
        def fails_thrice():
            nonlocal attempts
            attempts += 1
            if attempts <= 3:
                raise RetryableError("fail")
            return "ok"

        result = fails_thrice()
        assert result == "ok"
        # With jitter_factor=0.0: delays are 1.0, 2.0, 4.0
        assert mock_sleep.call_count == 3
        delays = [call.args[0] for call in mock_sleep.call_args_list]
        assert delays == [1.0, 2.0, 4.0]

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_max_delay_cap(self, mock_sleep) -> None:
        """Verify delay never exceeds max_delay."""
        attempts = 0

        @retry_with_backoff(initial_delay=32.0, max_delay=60.0, max_retries=3, jitter_factor=0.0)
        def always_fails():
            nonlocal attempts
            attempts += 1
            raise RetryableError("fail", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            always_fails()

        delays = [call.args[0] for call in mock_sleep.call_args_list]
        for d in delays:
            assert d <= 60.0

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_rate_limit_error_preserves_retry_after(self, mock_sleep) -> None:
        @retry_with_backoff(max_retries=0)
        def fails_immediately():
            raise RetryableError("limited", retry_after=45.0, is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            fails_immediately()

        assert exc_info.value.retry_after_seconds == 45.0

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_rate_limit_error_preserves_earlier_metadata_when_last_attempt_omits_it(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=1)
        def fails_twice():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError(
                    "limited",
                    retry_after=45.0,
                    reset_timestamp=500.0,
                    remaining=0,
                    provider="github",
                    credential_identity="SPECKIT_PR_TOKEN",
                    source="retry-after",
                    is_rate_limit=True,
                )
            raise RetryableError("limited", is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            fails_twice()

        assert exc_info.value.retry_after_seconds == 45.0
        assert exc_info.value.reset_timestamp == 500.0
        assert exc_info.value.remaining == 0
        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "SPECKIT_PR_TOKEN"
        assert exc_info.value.source == "retry-after"
        mock_sleep.assert_called_once_with(45.0)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_rate_limit_merge_ignores_type_invalid_metadata(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=1)
        def fails_twice():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError(
                    "limited",
                    reset_timestamp=[],
                    remaining=[],
                    is_rate_limit=True,
                )
            raise RetryableError("limited", retry_after=1.0, remaining=0, is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            fails_twice()

        assert exc_info.value.retry_after_seconds == 1.0
        assert exc_info.value.remaining == 0
        mock_sleep.assert_called_once()

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_rate_limit_merge_ignores_negative_metadata(self, mock_sleep) -> None:
        attempts = 0

        @retry_with_backoff(max_retries=1)
        def fails_twice():
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RetryableError(
                    "limited",
                    retry_after=-1.0,
                    reset_timestamp=-10.0,
                    remaining=-1,
                    is_rate_limit=True,
                )
            raise RetryableError("limited", retry_after=1.0, remaining=0, is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError) as exc_info:
            fails_twice()

        assert exc_info.value.retry_after_seconds == 1.0
        assert exc_info.value.remaining == 0
        mock_sleep.assert_called_once()

    def test_default_constants(self) -> None:
        assert DEFAULT_INITIAL_DELAY == 1.0
        assert DEFAULT_MAX_DELAY == 60.0
        assert DEFAULT_MAX_RETRIES == 5

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    def test_non_retryable_errors_propagate(self, mock_sleep) -> None:
        @retry_with_backoff(max_retries=3)
        def raises_runtime():
            raise RuntimeError("not retryable")

        with pytest.raises(RuntimeError, match="not retryable"):
            raises_runtime()

        mock_sleep.assert_not_called()

    def test_negative_max_retries_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="max_retries must be >= 0"):
            retry_with_backoff(max_retries=-1)

    def test_invalid_jitter_factor_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="jitter_factor must be between 0 and 1"):
            retry_with_backoff(jitter_factor=1.5)

    def test_negative_initial_delay_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="initial_delay must be >= 0"):
            retry_with_backoff(initial_delay=-1.0)

    def test_negative_max_delay_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="max_delay must be >= 0"):
            retry_with_backoff(max_delay=-1.0)

    @pytest.mark.parametrize(
        ("kwargs", "field_name"),
        [
            ({"initial_delay": math.nan}, "initial_delay"),
            ({"initial_delay": math.inf}, "initial_delay"),
            ({"max_delay": math.nan}, "max_delay"),
            ({"max_delay": math.inf}, "max_delay"),
            ({"jitter_factor": math.nan}, "jitter_factor"),
            ({"jitter_factor": math.inf}, "jitter_factor"),
        ],
    )
    def test_non_finite_timing_values_raise_value_error(self, kwargs: dict[str, float], field_name: str) -> None:
        with pytest.raises(ValueError, match=field_name):
            retry_with_backoff(**cast(dict[str, Any], kwargs))
