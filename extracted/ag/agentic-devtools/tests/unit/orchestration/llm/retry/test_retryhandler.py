"""Tests for RetryHandler and execute_with_retry."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.orchestration.llm.errors import RateLimitExhaustedError, RetryExhaustedError
from agentic_devtools.orchestration.llm.retry import (
    RetryConfig,
    RetryHandler,
    _compute_delay,
    execute_with_retry,
)


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_defaults(self):
        config = RetryConfig()
        assert config.max_attempts == 5
        assert config.base_delay_seconds == 1.0
        assert config.max_delay_seconds == 60.0
        assert config.jitter_factor == 0.5
        assert config.total_timeout_seconds == 120.0

    def test_custom_values(self):
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.5, total_timeout_seconds=30.0)
        assert config.max_attempts == 3
        assert config.total_timeout_seconds == 30.0

    def test_negative_max_attempts_raises(self):
        """Negative max_attempts must raise ValueError at construction time."""
        with pytest.raises(ValueError, match="max_attempts"):
            RetryConfig(max_attempts=-1)

    def test_negative_base_delay_raises(self):
        """Negative base_delay_seconds must raise ValueError at construction time."""
        with pytest.raises(ValueError, match="base_delay_seconds"):
            RetryConfig(base_delay_seconds=-0.5)

    def test_negative_max_delay_raises(self):
        """Negative max_delay_seconds must raise ValueError at construction time."""
        with pytest.raises(ValueError, match="max_delay_seconds"):
            RetryConfig(max_delay_seconds=-1.0)

    def test_negative_jitter_factor_raises(self):
        """Negative jitter_factor must raise ValueError at construction time."""
        with pytest.raises(ValueError, match="jitter_factor"):
            RetryConfig(jitter_factor=-0.1)

    def test_negative_total_timeout_raises(self):
        """Negative total_timeout_seconds must raise ValueError at construction time."""
        with pytest.raises(ValueError, match="total_timeout_seconds"):
            RetryConfig(total_timeout_seconds=-10.0)

    def test_zero_max_attempts_allowed(self):
        """Zero max_attempts is valid (loop never runs); must not raise."""
        config = RetryConfig(max_attempts=0)
        assert config.max_attempts == 0

    def test_zero_total_timeout_allowed(self):
        """Zero total_timeout_seconds is valid (immediate timeout); must not raise."""
        config = RetryConfig(total_timeout_seconds=0.0)
        assert config.total_timeout_seconds == 0.0

    def test_compute_delay_scales_jitter_with_exponential_backoff(self):
        config = RetryConfig(base_delay_seconds=1.0, max_delay_seconds=60.0, jitter_factor=0.5)
        with patch("agentic_devtools.orchestration.llm.retry._SYSTEM_RANDOM.uniform", return_value=0.0) as mock_uniform:
            delay = _compute_delay(config, attempt=3)
        mock_uniform.assert_called_once_with(0, 4.0)
        assert delay == 8.0

    def test_compute_delay_is_clamped_to_max_delay(self):
        config = RetryConfig(base_delay_seconds=1.0, max_delay_seconds=5.0, jitter_factor=0.5)
        with patch("agentic_devtools.orchestration.llm.retry._SYSTEM_RANDOM.uniform", return_value=2.5):
            delay = _compute_delay(config, attempt=3)
        assert delay == 5.0


class TestRetryHandler:
    """Tests for RetryHandler."""

    def test_config_property(self):
        config = RetryConfig(max_attempts=7)
        handler = RetryHandler(config)
        assert handler.config is config
        assert handler.config.max_attempts == 7

    @pytest.mark.asyncio
    async def test_success_on_first_try(self):
        handler = RetryHandler()
        func = AsyncMock(return_value="success")
        result = await handler.execute(func)
        assert result == "success"
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_429(self):
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01, total_timeout_seconds=5.0)
        handler = RetryHandler(config)

        error_429 = MagicMock()
        error_429.status_code = 429
        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=[exc, exc, "success"])
        result = await handler.execute(func)
        assert result == "success"
        assert func.call_count == 3

    @pytest.mark.asyncio
    async def test_exhausts_retries_raises(self):
        config = RetryConfig(max_attempts=2, base_delay_seconds=0.01, total_timeout_seconds=5.0)
        handler = RetryHandler(config)

        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=exc)
        with pytest.raises(RateLimitExhaustedError) as exc_info:
            await handler.execute(func)
        assert exc_info.value.attempts == 2

    @pytest.mark.asyncio
    async def test_exhausted_error_preserves_underlying_cause(self):
        config = RetryConfig(max_attempts=1, base_delay_seconds=0.01, total_timeout_seconds=5.0)
        handler = RetryHandler(config)

        exc = Exception("Service unavailable")
        exc.status_code = 503  # type: ignore[attr-defined]
        func = AsyncMock(side_effect=exc)

        with pytest.raises(RetryExhaustedError) as exc_info:
            await handler.execute(func)
        assert exc_info.value.attempts == 1
        assert exc_info.value.__cause__ is exc

    @pytest.mark.asyncio
    async def test_non_retryable_error_raises_immediately(self):
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01)
        handler = RetryHandler(config)

        exc = Exception("Auth error")
        exc.status_code = 401  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=exc)
        with pytest.raises(Exception, match="Auth error"):
            await handler.execute(func)
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_no_sleep_after_last_attempt(self):
        """asyncio.sleep must not be called after the final failing attempt."""
        config = RetryConfig(max_attempts=2, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=exc)
        with patch("agentic_devtools.orchestration.llm.retry.asyncio.sleep") as mock_sleep:
            with pytest.raises(RateLimitExhaustedError):
                await execute_with_retry(func, retry_config=config)
        # max_attempts=2: sleep once (between attempt 0 and 1), never after attempt 1
        assert mock_sleep.call_count == 1

    @pytest.mark.asyncio
    async def test_execute_rejects_retry_config_kwarg(self):
        """RetryHandler.execute should fail clearly on reserved retry_config kwarg."""
        handler = RetryHandler()
        func = AsyncMock(return_value="success")

        with pytest.raises(TypeError, match="does not accept 'retry_config'"):
            await handler.execute(func, retry_config=RetryConfig())


class TestExecuteWithRetry:
    """Tests for execute_with_retry."""

    @pytest.mark.asyncio
    async def test_success(self):
        func = AsyncMock(return_value=42)
        result = await execute_with_retry(func)
        assert result == 42

    @pytest.mark.asyncio
    async def test_timeout_exceeded(self):
        config = RetryConfig(max_attempts=100, base_delay_seconds=0.01, total_timeout_seconds=0.0)

        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]
        func = AsyncMock(side_effect=exc)

        with pytest.raises(RetryExhaustedError, match="timeout"):
            await execute_with_retry(func, retry_config=config)

    @pytest.mark.asyncio
    async def test_respects_retry_after_header(self):
        """Retry-After header should influence the delay."""
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01, total_timeout_seconds=10.0)

        response_mock = MagicMock()
        response_mock.status_code = 429
        response_mock.headers = {"Retry-After": "0.01"}

        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]
        exc.response = response_mock  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=[exc, "success"])
        result = await execute_with_retry(func, retry_config=config)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_delay_exceeds_remaining_timeout_raises(self):
        """When next delay would exceed timeout, raise immediately."""
        config = RetryConfig(max_attempts=5, base_delay_seconds=100.0, total_timeout_seconds=1.0)

        exc = Exception("Server error")
        exc.status_code = 500  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=exc)
        with pytest.raises(RetryExhaustedError, match="would exceed timeout"):
            await execute_with_retry(func, retry_config=config)

    @pytest.mark.asyncio
    async def test_httpx_response_status_code(self):
        """Extract status code from response attribute (httpx style)."""
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        response_mock = MagicMock()
        response_mock.status_code = 503
        response_mock.headers = {}

        exc = Exception("Service unavailable")
        exc.response = response_mock  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=[exc, "recovered"])
        result = await execute_with_retry(func, retry_config=config)
        assert result == "recovered"

    @pytest.mark.asyncio
    async def test_httpx_response_status_code_used_when_status_code_is_none(self):
        """Fallback to response.status_code when top-level status_code is None."""
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        response_mock = MagicMock()
        response_mock.status_code = 503
        response_mock.headers = {}

        exc = Exception("Service unavailable")
        exc.status_code = None  # type: ignore[attr-defined]
        exc.response = response_mock  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=[exc, "recovered"])
        result = await execute_with_retry(func, retry_config=config)
        assert result == "recovered"

    @pytest.mark.asyncio
    async def test_retry_after_invalid_value_ignored(self):
        """Invalid Retry-After value should be ignored gracefully."""
        config = RetryConfig(max_attempts=3, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        response_mock = MagicMock()
        response_mock.status_code = 429
        response_mock.headers = {"Retry-After": "not-a-number"}

        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]
        exc.response = response_mock  # type: ignore[attr-defined]

        func = AsyncMock(side_effect=[exc, "success"])
        result = await execute_with_retry(func, retry_config=config)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_no_status_code_raises_immediately(self):
        """Errors without status_code are not retried."""
        config = RetryConfig(max_attempts=5, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        exc = ValueError("Some internal error")
        func = AsyncMock(side_effect=exc)

        with pytest.raises(ValueError, match="Some internal error"):
            await execute_with_retry(func, retry_config=config)
        assert func.call_count == 1

    @pytest.mark.asyncio
    async def test_zero_max_attempts_raises_immediately(self):
        """When max_attempts=0 the loop body never runs and exhausted error is raised."""
        config = RetryConfig(max_attempts=0, base_delay_seconds=0.01, total_timeout_seconds=5.0)

        func = AsyncMock(return_value="should not be called")
        with pytest.raises(RetryExhaustedError, match="0 retry attempts exhausted"):
            await execute_with_retry(func, retry_config=config)
        assert func.call_count == 0

    @pytest.mark.asyncio
    async def test_429_exhaustion_still_raises_rate_limit_error(self):
        config = RetryConfig(max_attempts=1, base_delay_seconds=0.01, total_timeout_seconds=5.0)
        exc = Exception("Rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]
        func = AsyncMock(side_effect=exc)
        with pytest.raises(RateLimitExhaustedError):
            await execute_with_retry(func, retry_config=config)

    @pytest.mark.asyncio
    async def test_wrapped_func_with_config_kwarg_passes_through(self):
        """A function that uses 'config' as its own kwarg must receive it correctly.

        This guards against the old parameter name ('config') shadowing the
        wrapped function's own 'config' argument.
        """
        received: dict = {}

        async def func_with_config_kwarg(config: str) -> str:
            received["config"] = config
            return "ok"

        result = await execute_with_retry(func_with_config_kwarg, config="my-config")
        assert result == "ok"
        assert received["config"] == "my-config"
