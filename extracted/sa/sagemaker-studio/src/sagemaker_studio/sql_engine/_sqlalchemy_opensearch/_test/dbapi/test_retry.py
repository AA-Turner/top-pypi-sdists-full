"""
Unit tests for OpenSearch retry logic and circuit breaker.
"""

from unittest.mock import patch

import pytest

from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.exceptions import (
    OperationalError,
    TransientError,
)
from sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry import (
    CircuitBreaker,
    RetryConfig,
    RetryContext,
    retry_on_transient_error,
    with_retry,
)


class TestRetryConfig:
    """Test RetryConfig initialization and methods."""

    def test_defaults(self):
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.backoff_multiplier == 2.0
        assert config.jitter is True
        assert TransientError in config.retryable_exceptions

    def test_custom_values(self):
        config = RetryConfig(
            max_attempts=5,
            base_delay=0.5,
            max_delay=30.0,
            backoff_multiplier=3.0,
            jitter=False,
            retryable_exceptions=(ValueError,),
        )
        assert config.max_attempts == 5
        assert config.base_delay == 0.5
        assert config.max_delay == 30.0
        assert config.backoff_multiplier == 3.0
        assert config.jitter is False
        assert config.retryable_exceptions == (ValueError,)

    def test_calculate_delay_exponential_backoff(self):
        config = RetryConfig(base_delay=1.0, backoff_multiplier=2.0, jitter=False, max_delay=60.0)
        assert config.calculate_delay(0) == 1.0
        assert config.calculate_delay(1) == 2.0
        assert config.calculate_delay(2) == 4.0
        assert config.calculate_delay(3) == 8.0

    def test_calculate_delay_capped_at_max(self):
        config = RetryConfig(base_delay=1.0, backoff_multiplier=2.0, jitter=False, max_delay=5.0)
        assert config.calculate_delay(10) == 5.0

    def test_calculate_delay_with_retry_after(self):
        config = RetryConfig(jitter=False)
        assert config.calculate_delay(0, retry_after=10.0) == 10.0

    def test_calculate_delay_retry_after_capped(self):
        config = RetryConfig(jitter=False, max_delay=5.0)
        assert config.calculate_delay(0, retry_after=10.0) == 5.0

    def test_calculate_delay_with_jitter(self):
        config = RetryConfig(base_delay=10.0, jitter=True)
        delay = config.calculate_delay(0)
        # With 10% jitter on base_delay=10, delay should be in [9.0, 11.0]
        assert 9.0 <= delay <= 11.0

    def test_calculate_delay_never_negative(self):
        config = RetryConfig(base_delay=0.01, jitter=True)
        for attempt in range(10):
            assert config.calculate_delay(attempt) >= 0

    def test_should_retry_transient_error(self):
        config = RetryConfig(max_attempts=3)
        assert config.should_retry(TransientError("temp"), 0) is True
        assert config.should_retry(TransientError("temp"), 1) is True

    def test_should_retry_max_attempts_exceeded(self):
        config = RetryConfig(max_attempts=3)
        assert config.should_retry(TransientError("temp"), 2) is False

    def test_should_retry_non_retryable_exception(self):
        config = RetryConfig(max_attempts=3)
        assert config.should_retry(ValueError("bad"), 0) is False

    def test_should_retry_opensearch_transport_error(self):
        """Test retry for OpenSearch transport errors with retryable status codes."""
        config = RetryConfig(max_attempts=3)
        try:
            from opensearchpy import TransportError

            err_429 = TransportError(429, "too many requests", {})
            assert config.should_retry(err_429, 0) is True

            err_503 = TransportError(503, "service unavailable", {})
            assert config.should_retry(err_503, 0) is True

            err_400 = TransportError(400, "bad request", {})
            assert config.should_retry(err_400, 0) is False
        except ImportError:
            pytest.skip("opensearch-py not installed")


class TestRetryContext:
    """Test RetryContext tracking."""

    def test_initialization(self):
        ctx = RetryContext("test_op")
        assert ctx.operation_name == "test_op"
        assert ctx.attempt_count == 0
        assert ctx.last_exception is None
        assert ctx.total_delay == 0.0
        assert ctx.execution_context == {}

    def test_initialization_with_context(self):
        ctx = RetryContext("op", {"key": "val"})
        assert ctx.execution_context == {"key": "val"}

    def test_log_attempt(self):
        ctx = RetryContext("op")
        err = TransientError("temp")
        ctx.log_attempt(err, 1.5)
        assert ctx.attempt_count == 1
        assert ctx.last_exception is err
        assert ctx.total_delay == 1.5

    def test_log_multiple_attempts(self):
        ctx = RetryContext("op")
        ctx.log_attempt(TransientError("a"), 1.0)
        ctx.log_attempt(TransientError("b"), 2.0)
        assert ctx.attempt_count == 2
        assert ctx.total_delay == 3.0

    def test_log_success(self):
        ctx = RetryContext("op")
        ctx.log_success()  # Should not raise

    def test_log_failure(self):
        ctx = RetryContext("op")
        ctx.log_failure()  # Should not raise


class TestWithRetryDecorator:
    """Test the with_retry decorator."""

    def test_success_on_first_attempt(self):
        @with_retry(RetryConfig(max_attempts=3))
        def succeed():
            return "ok"

        assert succeed() == "ok"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_retries_on_transient_error(self, mock_sleep):
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3, base_delay=0.01, jitter=False))
        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise TransientError("temp")
            return "ok"

        assert fail_then_succeed() == "ok"
        assert call_count == 3

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_raises_after_max_attempts(self, mock_sleep):
        @with_retry(RetryConfig(max_attempts=2, base_delay=0.01, jitter=False))
        def always_fail():
            raise TransientError("always fails")

        with pytest.raises(TransientError, match="always fails"):
            always_fail()

    def test_non_retryable_exception_not_retried(self):
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3))
        def raise_value_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("not retryable")

        with pytest.raises(ValueError, match="not retryable"):
            raise_value_error()
        assert call_count == 1

    def test_custom_operation_name(self):
        @with_retry(RetryConfig(max_attempts=1), operation_name="my_op")
        def succeed():
            return "ok"

        assert succeed() == "ok"


class TestRetryOnTransientError:
    """Test the retry_on_transient_error function."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_success_on_first_call(self, mock_sleep):
        result = retry_on_transient_error(lambda: "ok")
        assert result == "ok"
        mock_sleep.assert_not_called()

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_retries_transient_error(self, mock_sleep):
        call_count = 0

        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TransientError("temp")
            return "done"

        result = retry_on_transient_error(
            fail_then_succeed,
            config=RetryConfig(max_attempts=3, base_delay=0.01, jitter=False),
        )
        assert result == "done"
        assert call_count == 2

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_exhausts_retries(self, mock_sleep):
        def always_fail():
            raise TransientError("always")

        with pytest.raises(TransientError, match="always"):
            retry_on_transient_error(
                always_fail,
                config=RetryConfig(max_attempts=2, base_delay=0.01, jitter=False),
            )

    def test_non_retryable_raises_immediately(self):
        call_count = 0

        def raise_value():
            nonlocal call_count
            call_count += 1
            raise ValueError("bad")

        with pytest.raises(OperationalError):
            retry_on_transient_error(raise_value, config=RetryConfig(max_attempts=3))
        assert call_count == 1

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_passes_args_and_kwargs(self, mock_sleep):
        def add(a, b, extra=0):
            return a + b + extra

        result = retry_on_transient_error(add, args=(1, 2), kwargs={"extra": 10})
        assert result == 13


class TestCircuitBreaker:
    """Test the CircuitBreaker pattern."""

    def test_initial_state_closed(self):
        cb = CircuitBreaker()
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_success_keeps_closed(self):
        cb = CircuitBreaker()
        result = cb.call(lambda: "ok")
        assert result == "ok"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_failure_increments_count(self):
        cb = CircuitBreaker(failure_threshold=5)
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.failure_count == 1
        assert cb.state == "CLOSED"

    def test_opens_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            with pytest.raises(ValueError):
                cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

    def test_open_circuit_raises_operational_error(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

        with pytest.raises(OperationalError, match="Circuit breaker is OPEN"):
            cb.call(lambda: "should not run")

    def test_half_open_after_recovery_timeout(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.0)
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

        # With recovery_timeout=0, should immediately transition to HALF_OPEN
        result = cb.call(lambda: "recovered")
        assert result == "recovered"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_half_open_failure_reopens(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.0)
        # Trip the breaker
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

        # Attempt recovery but fail again
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

    def test_success_resets_failure_count(self):
        cb = CircuitBreaker(failure_threshold=3)
        # Two failures
        for _ in range(2):
            with pytest.raises(ValueError):
                cb.call(self._raise_value_error)
        assert cb.failure_count == 2

        # One success resets
        cb.call(lambda: "ok")
        assert cb.failure_count == 0
        assert cb.state == "CLOSED"

    def test_custom_expected_exception(self):
        cb = CircuitBreaker(failure_threshold=2, expected_exception=TypeError)

        # ValueError should not be caught by circuit breaker logic
        # but it still propagates
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        # failure_count stays 0 because ValueError != TypeError
        assert cb.failure_count == 0

    @staticmethod
    def _raise_value_error():
        raise ValueError("test error")
