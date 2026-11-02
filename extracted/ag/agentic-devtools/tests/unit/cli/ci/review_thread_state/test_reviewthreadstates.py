"""Tests for the ReviewThreadStates result dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.review_thread_state import ReviewThreadStates


class TestReviewThreadStates:
    """Tests for the ReviewThreadStates dataclass."""

    def test_defaults_to_empty_non_degraded_result(self) -> None:
        """A default result reports an empty mapping that is not degraded."""
        result = ReviewThreadStates()

        assert result.states == {}
        assert result.degraded is False
        assert result.reason == ""

    def test_stores_states_and_degraded_reason(self) -> None:
        """Explicit fields are preserved verbatim."""
        result = ReviewThreadStates(states={7: (True, False)}, degraded=True, reason="boom")

        assert result.states == {7: (True, False)}
        assert result.degraded is True
        assert result.reason == "boom"

    def test_is_frozen(self) -> None:
        """The result is immutable so callers cannot mask a degraded lookup."""
        result = ReviewThreadStates(degraded=True, reason="boom")

        with pytest.raises(dataclasses.FrozenInstanceError):
            result.degraded = False  # type: ignore[misc]
