"""Tests for RetryExhaustedError exception."""

from agentic_devtools.orchestration.execution.exceptions import RetryExhaustedError


class TestRetryExhaustedError:
    def test_default_message(self) -> None:
        err = RetryExhaustedError()
        assert "exhausted" in str(err)

    def test_custom_message(self) -> None:
        err = RetryExhaustedError("all done")
        assert str(err) == "all done"

    def test_attempts_attribute(self) -> None:
        err = RetryExhaustedError(attempts=5)
        assert err.attempts == 5

    def test_attempts_defaults_zero(self) -> None:
        err = RetryExhaustedError()
        assert err.attempts == 0

    def test_last_error_attribute(self) -> None:
        err = RetryExhaustedError(last_error="boom")
        assert err.last_error == "boom"

    def test_last_error_defaults_empty(self) -> None:
        err = RetryExhaustedError()
        assert err.last_error == ""

    def test_is_runtime_error(self) -> None:
        err = RetryExhaustedError()
        assert isinstance(err, RuntimeError)
