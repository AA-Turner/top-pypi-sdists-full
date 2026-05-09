"""Comprehensive tests for sage/providers/retry.py - 100% coverage target."""

import time
from unittest.mock import MagicMock, patch

import httpx
import pytest

from sage.providers.retry import (
    AGGRESSIVE_RETRY_CONFIG,
    DEFAULT_RETRY_CONFIG,
    FAST_FAIL_CONFIG,
    PERMANENT_STATUS_CODES,
    TRANSIENT_STATUS_CODES,
    CircuitBreaker,
    RateLimiter,
    RetryConfig,
    get_rate_limiter,
    get_retry_after,
    is_rate_limited,
    is_transient_error,
    retry_generator,
    with_retry,
)

# =============================================================================
# is_transient_error Tests
# =============================================================================


class TestIsTransientError:
    """Tests for is_transient_error function."""

    def test_transient_http_status_codes(self):
        """Test that transient HTTP status codes return True."""
        for status_code in TRANSIENT_STATUS_CODES:
            response = MagicMock()
            response.status_code = status_code
            exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
            assert is_transient_error(exc) is True

    def test_permanent_http_status_codes(self):
        """Test that permanent HTTP status codes return False."""
        for status_code in PERMANENT_STATUS_CODES:
            response = MagicMock()
            response.status_code = status_code
            exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
            assert is_transient_error(exc) is False

    def test_read_timeout(self):
        """Test that ReadTimeout is transient."""
        exc = httpx.ReadTimeout("Timeout")
        assert is_transient_error(exc) is True

    def test_connect_timeout(self):
        """Test that ConnectTimeout is transient."""
        exc = httpx.ConnectTimeout("Timeout")
        assert is_transient_error(exc) is True

    def test_connect_error(self):
        """Test that ConnectError is transient."""
        exc = httpx.ConnectError("Connection failed")
        assert is_transient_error(exc) is True

    def test_remote_protocol_error(self):
        """Test that RemoteProtocolError is transient."""
        exc = httpx.RemoteProtocolError("Protocol error")
        assert is_transient_error(exc) is True

    def test_connection_error(self):
        """Test that ConnectionError is transient."""
        exc = ConnectionError("Connection failed")
        assert is_transient_error(exc) is True

    def test_other_exception_not_transient(self):
        """Test that unknown exceptions are not transient."""
        exc = ValueError("Some error")
        assert is_transient_error(exc) is False


# =============================================================================
# is_rate_limited Tests
# =============================================================================


class TestIsRateLimited:
    """Tests for is_rate_limited function."""

    def test_429_is_rate_limited(self):
        """Test that 429 status code is rate limited."""
        response = MagicMock()
        response.status_code = 429
        exc = httpx.HTTPStatusError("Too Many Requests", request=MagicMock(), response=response)
        assert is_rate_limited(exc) is True

    def test_other_status_not_rate_limited(self):
        """Test that other status codes are not rate limited."""
        response = MagicMock()
        response.status_code = 500
        exc = httpx.HTTPStatusError("Server Error", request=MagicMock(), response=response)
        assert is_rate_limited(exc) is False

    def test_non_http_error_not_rate_limited(self):
        """Test that non-HTTP errors are not rate limited."""
        exc = ValueError("Some error")
        assert is_rate_limited(exc) is False


# =============================================================================
# get_retry_after Tests
# =============================================================================


class TestGetRetryAfter:
    """Tests for get_retry_after function."""

    def test_retry_after_header_numeric(self):
        """Test extracting numeric Retry-After header."""
        response = MagicMock()
        response.headers = {"Retry-After": "30"}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) == 30.0

    def test_retry_after_header_float(self):
        """Test extracting float Retry-After header."""
        response = MagicMock()
        response.headers = {"Retry-After": "15.5"}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) == 15.5

    def test_retry_after_header_invalid(self):
        """Test invalid Retry-After header returns None."""
        response = MagicMock()
        response.headers = {"Retry-After": "invalid"}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) is None

    def test_no_retry_after_header(self):
        """Test missing Retry-After header returns None."""
        response = MagicMock()
        response.headers = {}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) is None

    def test_non_http_error_returns_none(self):
        """Test non-HTTP error returns None."""
        exc = ValueError("Some error")
        assert get_retry_after(exc) is None


# =============================================================================
# RetryConfig Tests
# =============================================================================


class TestRetryConfig:
    """Tests for RetryConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.base_delay == 0.5
        assert config.max_delay == 30.0
        assert config.exponential_base == 2.0
        assert config.jitter == 0.1

    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=1.0,
            max_delay=60.0,
            exponential_base=3.0,
            jitter=0.2,
        )
        assert config.max_attempts == 5
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 3.0
        assert config.jitter == 0.2

    def test_calculate_delay_with_retry_after(self):
        """Test calculate_delay respects Retry-After header."""
        config = RetryConfig(max_delay=10.0)
        delay = config.calculate_delay(0, retry_after=5.0)
        assert delay == 5.0

    def test_calculate_delay_retry_after_capped(self):
        """Test calculate_delay caps Retry-After to max_delay."""
        config = RetryConfig(max_delay=10.0)
        delay = config.calculate_delay(0, retry_after=20.0)
        assert delay == 10.0

    def test_calculate_delay_exponential_backoff(self):
        """Test calculate_delay uses exponential backoff."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=0.0)
        # attempt 0: 1 * 2^0 = 1
        # attempt 1: 1 * 2^1 = 2
        # attempt 2: 1 * 2^2 = 4
        with patch("sage.providers.retry.random.uniform", return_value=0):
            assert config.calculate_delay(0) == 1.0
            assert config.calculate_delay(1) == 2.0
            assert config.calculate_delay(2) == 4.0

    def test_calculate_delay_capped_at_max(self):
        """Test calculate_delay is capped at max_delay."""
        config = RetryConfig(base_delay=1.0, max_delay=3.0, jitter=0.0)
        with patch("sage.providers.retry.random.uniform", return_value=0):
            assert config.calculate_delay(5) == 3.0

    def test_calculate_delay_with_jitter(self):
        """Test calculate_delay adds jitter."""
        config = RetryConfig(base_delay=1.0, jitter=0.1)
        delays = [config.calculate_delay(0) for _ in range(10)]
        # Delays should vary due to jitter
        assert len(set(delays)) > 1

    def test_calculate_delay_minimum_zero(self):
        """Test calculate_delay returns at least 0."""
        config = RetryConfig(base_delay=0.1, jitter=1.0)
        # Even with large negative jitter, result should be >= 0
        for _ in range(100):
            assert config.calculate_delay(0) >= 0


# =============================================================================
# CircuitBreaker Tests
# =============================================================================


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_initial_state_closed(self):
        """Test that circuit starts closed."""
        cb = CircuitBreaker()
        assert cb._state == "closed"
        assert cb.can_proceed() is True

    def test_record_success_resets_failures(self):
        """Test that success resets failure count."""
        cb = CircuitBreaker()
        cb._failures = 3
        cb.record_success()
        assert cb._failures == 0
        assert cb._state == "closed"

    def test_record_failure_increments(self):
        """Test that failure increments counter."""
        cb = CircuitBreaker()
        cb.record_failure()
        assert cb._failures == 1
        cb.record_failure()
        assert cb._failures == 2

    def test_circuit_opens_after_threshold(self):
        """Test that circuit opens after failure threshold."""
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb._state == "closed"
        cb.record_failure()
        assert cb._state == "open"

    def test_open_circuit_blocks_calls(self):
        """Test that open circuit blocks calls."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert cb._state == "open"
        assert cb.can_proceed() is False

    def test_circuit_half_open_after_timeout(self):
        """Test that circuit goes half-open after timeout."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        assert cb._state == "open"

        time.sleep(0.15)
        assert cb.can_proceed() is True
        assert cb._state == "half-open"

    def test_half_open_allows_one_attempt(self):
        """Test that half-open allows one attempt."""
        cb = CircuitBreaker()
        cb._state = "half-open"
        assert cb.can_proceed() is True

    def test_is_open_returns_correct_value(self):
        """Test is_open method."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
        assert cb.is_open() is False

        cb.record_failure()
        cb.record_failure()
        assert cb.is_open() is True

    def test_is_open_false_after_timeout(self):
        """Test is_open returns False after recovery timeout."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        assert cb.is_open() is True

        time.sleep(0.15)
        assert cb.is_open() is False


# =============================================================================
# with_retry Decorator Tests
# =============================================================================


class TestWithRetry:
    """Tests for with_retry decorator."""

    def test_successful_call(self):
        """Test successful call returns result."""

        @with_retry()
        def success_func():
            return "success"

        assert success_func() == "success"

    def test_retry_on_transient_error(self):
        """Test retry on transient error."""
        call_count = [0]

        @with_retry(config=RetryConfig(max_attempts=3, base_delay=0.01))
        def transient_func():
            call_count[0] += 1
            if call_count[0] < 3:
                response = MagicMock()
                response.status_code = 500
                raise httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
            return "success"

        result = transient_func()
        assert result == "success"
        assert call_count[0] == 3

    def test_no_retry_on_permanent_error(self):
        """Test no retry on permanent error."""
        call_count = [0]

        @with_retry(config=RetryConfig(max_attempts=3))
        def permanent_func():
            call_count[0] += 1
            response = MagicMock()
            response.status_code = 401
            raise httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response)

        with pytest.raises(httpx.HTTPStatusError):
            permanent_func()
        assert call_count[0] == 1

    def test_keyboard_interrupt_not_caught(self):
        """Test KeyboardInterrupt is not caught."""

        @with_retry()
        def interrupt_func():
            raise KeyboardInterrupt()

        with pytest.raises(KeyboardInterrupt):
            interrupt_func()

    def test_circuit_breaker_integration(self):
        """Test with_retry with circuit breaker."""
        cb = CircuitBreaker(failure_threshold=2)

        @with_retry(circuit_breaker=cb)
        def cb_func():
            return "success"

        result = cb_func()
        assert result == "success"
        assert cb._failures == 0

    def test_circuit_breaker_blocks_when_open(self):
        """Test that open circuit breaker blocks calls."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60)
        cb.record_failure()  # Open the circuit

        @with_retry(circuit_breaker=cb)
        def blocked_func():
            return "success"

        with pytest.raises(RuntimeError) as exc_info:
            blocked_func()
        assert "Circuit breaker open" in str(exc_info.value)

    def test_circuit_breaker_records_failures(self):
        """Test that circuit breaker records failures."""
        cb = CircuitBreaker(failure_threshold=10)

        @with_retry(config=RetryConfig(max_attempts=2, base_delay=0.01), circuit_breaker=cb)
        def failing_func():
            response = MagicMock()
            response.status_code = 500
            raise httpx.HTTPStatusError("Error", request=MagicMock(), response=response)

        with pytest.raises(httpx.HTTPStatusError):
            failing_func()
        assert cb._failures >= 1

    def test_all_retries_exhausted(self):
        """Test exception raised when all retries exhausted."""

        @with_retry(config=RetryConfig(max_attempts=2, base_delay=0.01))
        def always_fails():
            response = MagicMock()
            response.status_code = 500
            raise httpx.HTTPStatusError("Error", request=MagicMock(), response=response)

        with pytest.raises(httpx.HTTPStatusError):
            always_fails()


# =============================================================================
# retry_generator Tests
# =============================================================================


class TestRetryGenerator:
    """Tests for retry_generator function."""

    def test_successful_generator(self):
        """Test successful generator yields all values."""

        @retry_generator
        def success_gen():
            yield 1
            yield 2
            yield 3

        result = list(success_gen())
        assert result == [1, 2, 3]

    def test_retry_on_transient_error(self):
        """Test generator retries on transient error."""
        call_count = [0]

        @retry_generator
        def transient_gen():
            call_count[0] += 1
            if call_count[0] < 2:
                yield 1
                response = MagicMock()
                response.status_code = 500
                raise httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
            yield 1
            yield 2

        # Note: Generator restarts from beginning on retry
        result = list(transient_gen())
        assert result == [1, 1, 2]

    def test_no_retry_on_permanent_error(self):
        """Test no retry on permanent error."""

        @retry_generator
        def permanent_gen():
            yield 1
            response = MagicMock()
            response.status_code = 401
            raise httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response)

        with pytest.raises(httpx.HTTPStatusError):
            list(permanent_gen())

    def test_keyboard_interrupt_not_caught(self):
        """Test KeyboardInterrupt is not caught."""

        @retry_generator
        def interrupt_gen():
            yield 1
            raise KeyboardInterrupt()

        gen = interrupt_gen()
        assert next(gen) == 1
        with pytest.raises(KeyboardInterrupt):
            next(gen)

    def test_all_retries_exhausted(self):
        """Test exception raised when all retries exhausted."""
        config = RetryConfig(max_attempts=2, base_delay=0.01)

        @retry_generator
        def always_fails():
            response = MagicMock()
            response.status_code = 500
            raise httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
            yield  # Never reached

        # Need to call the decorator with config
        wrapped = retry_generator(always_fails, config=config)
        with pytest.raises(httpx.HTTPStatusError):
            list(wrapped())


# =============================================================================
# RateLimiter Tests
# =============================================================================


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_initial_tokens(self):
        """Test initial token count equals burst size."""
        rl = RateLimiter(requests_per_minute=60, burst_size=10)
        assert rl._tokens == 10.0

    def test_default_burst_size(self):
        """Test default burst size equals requests_per_minute."""
        rl = RateLimiter(requests_per_minute=120)
        assert rl.burst_size == 120

    def test_try_acquire_success(self):
        """Test try_acquire succeeds when tokens available."""
        rl = RateLimiter(requests_per_minute=60, burst_size=5)
        assert rl.try_acquire() is True
        assert rl._tokens == 4.0

    def test_try_acquire_no_tokens(self):
        """Test try_acquire fails when no tokens."""
        rl = RateLimiter(requests_per_minute=60, burst_size=1)
        rl._tokens = 0
        assert rl.try_acquire() is False

    def test_acquire_success(self):
        """Test acquire succeeds when tokens available."""
        rl = RateLimiter(requests_per_minute=60, burst_size=5)
        assert rl.acquire(timeout=0.1) is True
        assert rl._tokens == 4.0

    def test_acquire_waits_for_token(self):
        """Test acquire waits for token refill."""
        rl = RateLimiter(requests_per_minute=6000, burst_size=1)  # 100/sec = fast refill
        rl._tokens = 0

        start = time.monotonic()
        result = rl.acquire(timeout=1.0)
        elapsed = time.monotonic() - start

        assert result is True
        assert elapsed < 0.5  # Should refill quickly

    def test_acquire_timeout(self):
        """Test acquire returns False on timeout."""
        rl = RateLimiter(requests_per_minute=6, burst_size=1)  # 0.1/sec = slow refill
        rl._tokens = 0

        result = rl.acquire(timeout=0.01)
        assert result is False

    def test_refill_over_time(self):
        """Test tokens refill over time."""
        rl = RateLimiter(requests_per_minute=600, burst_size=10)  # 10/sec
        rl._tokens = 0

        time.sleep(0.1)  # Should add ~1 token
        rl._refill()

        assert rl._tokens > 0.5
        assert rl._tokens < 2.0

    def test_refill_capped_at_burst_size(self):
        """Test refill doesn't exceed burst size."""
        rl = RateLimiter(requests_per_minute=60, burst_size=5)
        rl._tokens = 5.0

        time.sleep(0.1)
        rl._refill()

        assert rl._tokens == 5.0


# =============================================================================
# get_rate_limiter Tests
# =============================================================================


class TestGetRateLimiter:
    """Tests for get_rate_limiter function."""

    def test_creates_new_limiter(self):
        """Test creates new limiter for unknown provider."""
        # Use unique provider name to avoid interference
        limiter = get_rate_limiter("test_provider_unique", 120)
        assert limiter.requests_per_minute == 120

    def test_returns_existing_limiter(self):
        """Test returns same limiter for same provider."""
        limiter1 = get_rate_limiter("shared_provider")
        limiter2 = get_rate_limiter("shared_provider")
        assert limiter1 is limiter2


# =============================================================================
# Default Configs Tests
# =============================================================================


class TestDefaultConfigs:
    """Tests for pre-defined configurations."""

    def test_default_config(self):
        """Test DEFAULT_RETRY_CONFIG values."""
        assert DEFAULT_RETRY_CONFIG.max_attempts == 3
        assert DEFAULT_RETRY_CONFIG.base_delay == 0.5

    def test_aggressive_config(self):
        """Test AGGRESSIVE_RETRY_CONFIG values."""
        assert AGGRESSIVE_RETRY_CONFIG.max_attempts == 5
        assert AGGRESSIVE_RETRY_CONFIG.base_delay == 1.0

    def test_fast_fail_config(self):
        """Test FAST_FAIL_CONFIG values."""
        assert FAST_FAIL_CONFIG.max_attempts == 2
        assert FAST_FAIL_CONFIG.base_delay == 0.2
        assert FAST_FAIL_CONFIG.max_delay == 2.0
