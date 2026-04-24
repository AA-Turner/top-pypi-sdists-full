"""
Extended tests for OpenSearch retry logic — covers branches missed by test_retry.py.
"""

import sys
import time
import types
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


def _make_fake_opensearchpy():
    """Build a fake opensearchpy module with the exception hierarchy for retry tests."""
    mod = types.ModuleType("opensearchpy")

    class TransportError(Exception):
        def __init__(self, status_code, message, info=None):
            super().__init__(message)
            self.status_code = status_code

    class ConnectionError(TransportError):
        def __init__(self, message, error=None, exception=None):
            super().__init__("N/A", message)

    mod.TransportError = TransportError
    mod.ConnectionError = ConnectionError
    return mod


@pytest.fixture
def fake_opensearchpy():
    """Fixture that injects a fake opensearchpy module into sys.modules."""
    mod = _make_fake_opensearchpy()
    to_remove = [k for k in sys.modules if k == "opensearchpy" or k.startswith("opensearchpy.")]
    saved = {k: sys.modules.pop(k) for k in to_remove if k in sys.modules}
    sys.modules["opensearchpy"] = mod
    yield mod
    del sys.modules["opensearchpy"]
    sys.modules.update(saved)


class TestRetryConfigExtended:
    """Extended RetryConfig tests."""

    def test_should_retry_opensearch_connection_error(self, fake_opensearchpy):
        """Test that OpenSearch ConnectionError without retryable status is not retried."""
        config = RetryConfig(max_attempts=3)
        err = fake_opensearchpy.ConnectionError("connect failed")
        # ConnectionError has status_code='N/A' which is not in [429, 502, 503, 504]
        assert config.should_retry(err, 0) is False

    def test_should_retry_opensearch_transport_error_non_retryable_status(self, fake_opensearchpy):
        """Non-retryable status codes should not be retried."""
        config = RetryConfig(max_attempts=3)
        err = fake_opensearchpy.TransportError(404, "not found")
        assert config.should_retry(err, 0) is False

    def test_should_retry_opensearch_transport_error_502(self, fake_opensearchpy):
        config = RetryConfig(max_attempts=3)
        err = fake_opensearchpy.TransportError(502, "bad gateway")
        assert config.should_retry(err, 0) is True

    def test_should_retry_opensearch_transport_error_504(self, fake_opensearchpy):
        config = RetryConfig(max_attempts=3)
        err = fake_opensearchpy.TransportError(504, "gateway timeout")
        assert config.should_retry(err, 0) is True

    def test_should_retry_no_opensearchpy(self):
        """When opensearch-py is not importable, non-retryable exceptions return False."""
        config = RetryConfig(max_attempts=3)

        modules_to_block = {
            k: None
            for k in list(sys.modules.keys())
            if k == "opensearchpy" or k.startswith("opensearchpy.")
        }
        modules_to_block["opensearchpy"] = None

        with patch.dict(sys.modules, modules_to_block):
            # A generic exception that's not TransientError should return False
            assert config.should_retry(RuntimeError("something"), 0) is False


class TestRetryOnTransientErrorExtended:
    """Extended tests for retry_on_transient_error."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_exact_call_count_on_exhaustion(self, mock_sleep):
        """Verify max_attempts means total number of calls."""
        call_count = 0

        def always_fail():
            nonlocal call_count
            call_count += 1
            raise TransientError("fail")

        with pytest.raises(TransientError):
            retry_on_transient_error(
                always_fail,
                config=RetryConfig(max_attempts=3, base_delay=0.01, jitter=False),
            )
        assert call_count == 3  # not 4

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_maps_non_dbapi_exception(self, mock_sleep):
        """Non-DB-API exceptions should be mapped before retry check."""
        call_count = 0

        def raise_runtime():
            nonlocal call_count
            call_count += 1
            raise RuntimeError("unmapped error")

        with pytest.raises(OperationalError):
            retry_on_transient_error(
                raise_runtime,
                config=RetryConfig(max_attempts=2, base_delay=0.01, jitter=False),
            )
        # Should only be called once since RuntimeError is not retryable
        assert call_count == 1

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_with_operation_name(self, mock_sleep):
        """Test that operation_name parameter is accepted."""
        result = retry_on_transient_error(
            lambda: "ok",
            operation_name="test_operation",
        )
        assert result == "ok"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_with_execution_context(self, mock_sleep):
        """Test that execution_context parameter is accepted."""
        result = retry_on_transient_error(
            lambda: "ok",
            execution_context={"host": "localhost"},
        )
        assert result == "ok"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_retry_with_retry_after_attribute(self, mock_sleep):
        """Test that retry_after attribute on exception is used."""
        call_count = 0

        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                err = TransientError("rate limited", retry_after=5.0)
                raise err
            return "ok"

        result = retry_on_transient_error(
            fail_then_succeed,
            config=RetryConfig(max_attempts=3, base_delay=0.01, jitter=False),
        )
        assert result == "ok"
        assert call_count == 2


class TestWithRetryDecoratorExtended:
    """Extended tests for with_retry decorator."""

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_exact_call_count_on_exhaustion(self, mock_sleep):
        """Verify max_attempts means total number of calls, not retries."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3, base_delay=0.01, jitter=False))
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise TransientError("fail")

        with pytest.raises(TransientError):
            always_fail()
        assert call_count == 3  # not 4

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_default_config(self, mock_sleep):
        """Test decorator with default config."""

        @with_retry()
        def succeed():
            return "ok"

        assert succeed() == "ok"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_with_execution_context(self, mock_sleep):
        """Test decorator with execution_context."""

        @with_retry(
            RetryConfig(max_attempts=1),
            operation_name="test",
            execution_context={"key": "val"},
        )
        def succeed():
            return "ok"

        assert succeed() == "ok"

    @patch("sagemaker_studio.sql_engine._sqlalchemy_opensearch.dbapi.retry.time.sleep")
    def test_retry_uses_retry_after(self, mock_sleep):
        """Test that retry_after from exception is used for delay."""
        call_count = 0

        @with_retry(RetryConfig(max_attempts=3, base_delay=0.01, jitter=False))
        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TransientError("wait", retry_after=2.0)
            return "ok"

        assert fail_then_succeed() == "ok"
        assert call_count == 2

    def test_preserves_function_metadata(self):
        """Verify functools.wraps preserves the decorated function's metadata."""

        @with_retry(RetryConfig(max_attempts=1))
        def my_retried_function():
            """Docstring for retried function."""
            return "ok"

        assert my_retried_function.__name__ == "my_retried_function"
        assert my_retried_function.__doc__ == "Docstring for retried function."


class TestCircuitBreakerExtended:
    """Extended CircuitBreaker tests."""

    def test_should_attempt_reset_no_failure_time(self):
        """When last_failure_time is None, should attempt reset."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)
        assert cb._should_attempt_reset() is True

    def test_should_attempt_reset_timeout_not_elapsed(self):
        """When timeout hasn't elapsed, should not attempt reset."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60.0)
        cb.last_failure_time = time.time()
        assert cb._should_attempt_reset() is False

    def test_should_attempt_reset_timeout_elapsed(self):
        """When timeout has elapsed, should attempt reset."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.0)
        cb.last_failure_time = time.time() - 1.0
        assert cb._should_attempt_reset() is True

    def test_on_success_resets_from_half_open(self):
        """Success in HALF_OPEN state should transition to CLOSED."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.0)
        cb.state = "HALF_OPEN"
        cb.failure_count = 1
        cb._on_success()
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_on_success_in_closed_state(self):
        """Success in CLOSED state should reset failure count."""
        cb = CircuitBreaker(failure_threshold=5)
        cb.failure_count = 3
        cb._on_success()
        assert cb.failure_count == 0
        assert cb.state == "CLOSED"

    def test_on_failure_records_time(self):
        """Failure should record the time."""
        cb = CircuitBreaker(failure_threshold=5)
        before = time.time()
        cb._on_failure()
        after = time.time()
        assert cb.failure_count == 1
        assert before <= cb.last_failure_time <= after

    def test_on_failure_opens_at_threshold(self):
        """Reaching threshold should open the circuit."""
        cb = CircuitBreaker(failure_threshold=2)
        cb._on_failure()
        assert cb.state == "CLOSED"
        cb._on_failure()
        assert cb.state == "OPEN"

    def test_open_circuit_with_recovery_timeout_not_elapsed(self):
        """OPEN circuit with timeout not elapsed should raise OperationalError."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=9999.0)
        with pytest.raises(ValueError):
            cb.call(self._raise_value_error)
        assert cb.state == "OPEN"

        with pytest.raises(OperationalError, match="Circuit breaker is OPEN"):
            cb.call(lambda: "should not run")

    @staticmethod
    def _raise_value_error():
        raise ValueError("test error")


class TestRetryContextExtended:
    """Extended RetryContext tests."""

    def test_start_time_is_set(self):
        before = time.time()
        ctx = RetryContext("op")
        after = time.time()
        assert before <= ctx.start_time <= after

    def test_log_attempt_updates_last_exception(self):
        ctx = RetryContext("op")
        err1 = TransientError("first")
        err2 = TransientError("second")
        ctx.log_attempt(err1, 1.0)
        assert ctx.last_exception is err1
        ctx.log_attempt(err2, 2.0)
        assert ctx.last_exception is err2
