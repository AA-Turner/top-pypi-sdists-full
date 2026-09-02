"""Tests for ReasoningTimeoutError exception."""

from agentic_devtools.orchestration.execution.exceptions import ReasoningTimeoutError


class TestReasoningTimeoutError:
    def test_default_message(self) -> None:
        err = ReasoningTimeoutError()
        assert "timed out" in str(err)

    def test_custom_message(self) -> None:
        err = ReasoningTimeoutError("custom timeout")
        assert str(err) == "custom timeout"

    def test_timeout_seconds_attribute(self) -> None:
        err = ReasoningTimeoutError(timeout_seconds=30.0)
        assert err.timeout_seconds == 30.0

    def test_timeout_seconds_defaults_none(self) -> None:
        err = ReasoningTimeoutError()
        assert err.timeout_seconds is None

    def test_is_timeout_error(self) -> None:
        err = ReasoningTimeoutError()
        assert isinstance(err, TimeoutError)
