"""Tests for _state_value."""

from unittest.mock import patch

from agentic_devtools.cli.pull_request_thread import _state_value


class TestStateValue:
    """Validate state snapshot and live-state lookup behavior."""

    def test_reads_values_from_nested_state_snapshot(self) -> None:
        """Nested aliases are resolved from the supplied immutable state mapping."""
        state = {"nested": {"value": "snapshot"}}

        assert _state_value("missing", "nested.value", state=state) == "snapshot"
        assert _state_value("missing", state=state) is None

    def test_reads_live_state_when_snapshot_is_not_supplied(self) -> None:
        """Live state is consulted only when no snapshot argument is supplied."""
        with patch("agentic_devtools.cli.pull_request_thread.get_value", return_value="live"):
            assert _state_value("live") == "live"
        with patch("agentic_devtools.cli.pull_request_thread.get_value", return_value=None):
            assert _state_value("missing") is None
