"""Tests for with_retry composable retry mechanism."""

import pytest

from agentic_devtools.orchestration.execution.exceptions import RetryExhaustedError
from agentic_devtools.orchestration.execution.retry import RetryContext, with_retry


class TestWithRetry:
    def test_successful_first_attempt(self) -> None:
        def fn(ctx: RetryContext) -> str:
            return "success"

        result = with_retry(fn, max_retries=2)
        assert result == "success"

    def test_retry_on_failure_then_success(self) -> None:
        call_count = 0

        def fn(ctx: RetryContext) -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("first attempt fails")
            return "second attempt"

        result = with_retry(fn, max_retries=2)
        assert result == "second attempt"
        assert call_count == 2

    def test_max_retries_exhausted(self) -> None:
        def fn(ctx: RetryContext) -> str:
            raise ValueError("always fails")

        with pytest.raises(RetryExhaustedError) as exc_info:
            with_retry(fn, max_retries=2)
        assert exc_info.value.attempts == 3  # initial + 2 retries
        assert "always fails" in exc_info.value.last_error

    def test_configurable_max_retries(self) -> None:
        call_count = 0

        def fn(ctx: RetryContext) -> str:
            nonlocal call_count
            call_count += 1
            raise ValueError("fail")

        with pytest.raises(RetryExhaustedError):
            with_retry(fn, max_retries=4)
        assert call_count == 5  # initial + 4 retries

    def test_context_accumulates_failure_reasons(self) -> None:
        contexts: list[RetryContext] = []

        def fn(ctx: RetryContext) -> str:
            contexts.append(
                RetryContext(
                    attempt=ctx.attempt,
                    max_retries=ctx.max_retries,
                    failure_reasons=list(ctx.failure_reasons),
                )
            )
            if ctx.attempt < 2:
                raise ValueError(f"fail_{ctx.attempt}")
            return "ok"

        with_retry(fn, max_retries=2)

        assert len(contexts) == 3
        # First attempt: no prior failures
        assert contexts[0].failure_reasons == []
        # Second attempt: one prior failure
        assert contexts[1].failure_reasons == ["fail_0"]
        # Third attempt: two prior failures
        assert contexts[2].failure_reasons == ["fail_0", "fail_1"]

    def test_zero_retries(self) -> None:
        def fn(ctx: RetryContext) -> str:
            raise ValueError("single attempt")

        with pytest.raises(RetryExhaustedError) as exc_info:
            with_retry(fn, max_retries=0)
        assert exc_info.value.attempts == 1

    def test_retry_context_is_first_attempt(self) -> None:
        ctx = RetryContext(attempt=0, max_retries=2)
        assert ctx.is_first_attempt is True
        ctx.attempt = 1
        assert ctx.is_first_attempt is False

    def test_retry_context_has_retries_remaining(self) -> None:
        ctx = RetryContext(attempt=0, max_retries=2)
        assert ctx.has_retries_remaining is True
        ctx.attempt = 2
        assert ctx.has_retries_remaining is False

    def test_negative_max_retries_raises(self) -> None:
        """with_retry must reject negative max_retries up front."""

        def fn(ctx: RetryContext) -> str:
            return "ok"

        with pytest.raises(ValueError, match="max_retries must be >= 0"):
            with_retry(fn, max_retries=-1)
