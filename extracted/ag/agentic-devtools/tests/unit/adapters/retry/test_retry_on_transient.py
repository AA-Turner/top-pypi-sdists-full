"""Tests for retry utility."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.retry import (
    TransientError,
    is_transient_error,
    retry_on_transient,
)


class TestRetryOnTransient:
    """Verify retry behavior with exponential backoff."""

    def test_no_retry_on_success(self):
        call_count = {"n": 0}

        @retry_on_transient
        def succeed():
            call_count["n"] += 1
            return "ok"

        assert succeed() == "ok"
        assert call_count["n"] == 1

    def test_retries_on_transient_error(self):
        call_count = {"n": 0}

        @retry_on_transient(max_retries=3, initial_delay=0.01, max_total_wait=1.0)
        def fail_then_succeed():
            call_count["n"] += 1
            if call_count["n"] < 3:
                raise TransientError("rate limited", status_code=429)
            return "ok"

        assert fail_then_succeed() == "ok"
        assert call_count["n"] == 3

    def test_raises_after_max_retries(self):
        @retry_on_transient(max_retries=2, initial_delay=0.01, max_total_wait=1.0)
        def always_fail():
            raise TransientError("503 Service Unavailable", status_code=503)

        with pytest.raises(TransientError):
            always_fail()

    def test_original_traceback_preserved_after_retries_exhausted(self):
        """After retries are exhausted the original traceback location is preserved."""

        def _inner():
            raise TransientError("exhausted", status_code=503)

        @retry_on_transient(max_retries=1, initial_delay=0.01, max_total_wait=1.0)
        def always_fail():
            _inner()

        with pytest.raises(TransientError) as exc_info:
            always_fail()

        # The traceback must include _inner — the original raise site
        tb_frames = [f.name for f in exc_info.traceback]
        assert "_inner" in tb_frames, "Original raise site (_inner) missing from traceback"

    def test_original_traceback_preserved_when_max_total_wait_exceeded(self):
        """When max_total_wait stops retries the original traceback is preserved."""

        def _inner():
            raise TransientError("overloaded", status_code=429)

        @retry_on_transient(max_retries=10, initial_delay=1.0, max_total_wait=0.0)
        def fail_immediately():
            _inner()

        with pytest.raises(TransientError) as exc_info:
            fail_immediately()

        tb_frames = [f.name for f in exc_info.traceback]
        assert "_inner" in tb_frames, "Original raise site (_inner) missing from traceback"

    def test_does_not_retry_non_transient_error(self):
        call_count = {"n": 0}

        @retry_on_transient(max_retries=3, initial_delay=0.01, max_total_wait=1.0)
        def permanent_error():
            call_count["n"] += 1
            raise ValueError("permanent")

        with pytest.raises(ValueError, match="permanent"):
            permanent_error()
        assert call_count["n"] == 1

    def test_stops_when_max_total_wait_exceeded(self):
        """Retry stops when next delay would exceed max_total_wait."""
        call_count = {"n": 0}

        # max_retries=10 but max_total_wait=0 means first retry check will break
        @retry_on_transient(max_retries=10, initial_delay=1.0, max_total_wait=0.0)
        def always_transient():
            call_count["n"] += 1
            raise TransientError("overloaded", status_code=503)

        with pytest.raises(TransientError):
            always_transient()
        # Only 1 call: attempt 0 fails, then delay(1.0) > max_total_wait(0.0) → break
        assert call_count["n"] == 1

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"max_retries": -1}, "max_retries"),
            ({"initial_delay": -0.01}, "initial_delay"),
            ({"max_total_wait": -1.0}, "max_total_wait"),
        ],
    )
    def test_invalid_retry_configuration_raises_value_error(self, kwargs, message):
        with pytest.raises(ValueError, match=message):

            @retry_on_transient(**kwargs)
            def _noop():
                return "ok"


class TestIsTransientError:
    """Verify transient error detection."""

    def test_transient_error_instance(self):
        assert is_transient_error(TransientError("test", 429)) is True

    def test_runtime_error_with_status_code(self):
        assert is_transient_error(RuntimeError("HTTP 429 too many requests")) is True
        assert is_transient_error(RuntimeError("HTTP 502 bad gateway")) is True
        assert is_transient_error(RuntimeError("HTTP 503 service unavailable")) is True
        assert is_transient_error(RuntimeError("503 service unavailable")) is True

    def test_non_transient_error(self):
        assert is_transient_error(ValueError("permanent")) is False
        assert is_transient_error(RuntimeError("HTTP 404 not found")) is False

    def test_non_runtime_error_with_status_code_not_transient(self):
        # Status-code substring heuristic must NOT fire for non-RuntimeError types
        assert is_transient_error(ValueError("503")) is False
        assert is_transient_error(ValueError("429 too many requests")) is False
        assert is_transient_error(OSError("502 bad gateway")) is False

    def test_runtime_error_with_embedded_code_not_transient(self):
        # "1429", "5029" contain transient codes as substrings but must not trigger retry
        assert is_transient_error(RuntimeError("error code 1429")) is False
        assert is_transient_error(RuntimeError("port 5029 unreachable")) is False
        assert is_transient_error(RuntimeError("timeout after 5030ms")) is False

    def test_runtime_error_with_http_50200_not_transient(self):
        # "HTTP 50200" embeds "502" but the trailing digits must NOT trigger retry (T025)
        assert is_transient_error(RuntimeError("HTTP 50200 weird status")) is False
