"""Tests for _check_session_mutex."""

from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.copilot import session as session_module
from agentic_devtools.cli.copilot.session import _check_session_mutex


@pytest.fixture
def temp_state(tmp_path):
    """Redirect state storage to a temp directory."""
    with patch.object(state, "get_state_dir", return_value=tmp_path):
        with patch.object(session_module, "get_state_dir", return_value=tmp_path):
            state.clear_state()
            yield tmp_path


class TestCheckSessionMutex:
    """Tests for _check_session_mutex guard function."""

    def test_no_pid_in_state_allows(self, temp_state):
        """No copilot.pid in state → returns None (allow)."""
        result = _check_session_mutex()
        assert result is None

    def test_empty_pid_allows(self, temp_state):
        """Empty string copilot.pid → returns None (allow)."""
        state.set_value("copilot.pid", "")
        result = _check_session_mutex()
        assert result is None

    @patch.object(session_module.os, "getpid", return_value=7777)
    def test_claims_pid_when_empty(self, _mock_getpid, temp_state):
        """claim=True sets copilot.pid atomically when no active session exists."""
        result = _check_session_mutex(claim=True)
        assert result is None
        assert state.get_value("copilot.pid") == 7777

    def test_unparseable_pid_clears_and_allows(self, temp_state):
        """Non-numeric copilot.pid → clears value and returns None."""
        state.set_value("copilot.pid", "not-a-number")
        result = _check_session_mutex()
        assert result is None
        # Verify the stale value was cleared
        assert state.get_value("copilot.pid") == ""

    def test_zero_pid_clears_and_allows(self, temp_state):
        """PID 0 → clears value and returns None."""
        state.set_value("copilot.pid", "0")
        result = _check_session_mutex()
        assert result is None
        assert state.get_value("copilot.pid") == ""

    def test_numeric_zero_pid_clears_and_allows(self, temp_state):
        """Numeric PID 0 → clears value and returns None."""
        state.set_value("copilot.pid", 0)
        result = _check_session_mutex()
        assert result is None
        assert state.get_value("copilot.pid") == ""

    def test_negative_pid_clears_and_allows(self, temp_state):
        """Negative PID → clears value and returns None."""
        state.set_value("copilot.pid", "-1")
        result = _check_session_mutex()
        assert result is None
        assert state.get_value("copilot.pid") == ""

    @patch.object(session_module, "_is_process_alive", return_value=True)
    def test_live_pid_blocks(self, mock_alive, temp_state, capsys):
        """Live PID → returns snapshot dict and prints warning."""
        state.set_value("copilot.pid", "12345")
        state.set_value("copilot.session_id", "abc123")
        state.set_value("copilot.mode", "non-interactive")
        state.set_value("copilot.start_time", "2026-06-04T13:45:00Z")
        state.set_value("copilot.prompt_file", "/tmp/prompt.md")

        result = _check_session_mutex()

        assert result is not None
        assert result["pid"] == 12345
        assert result["session_id"] == "abc123"
        assert result["mode"] == "non-interactive"
        assert result["start_time"] == "2026-06-04T13:45:00Z"
        assert result["prompt_file"] == "/tmp/prompt.md"

        captured = capsys.readouterr()
        assert "already running" in captured.err
        assert "pid=12345" in captured.err

    @patch.object(session_module, "_is_process_alive", return_value=False)
    def test_stale_pid_clears_and_allows(self, mock_alive, temp_state):
        """Dead PID → clears stale value and returns None."""
        state.set_value("copilot.pid", "99999")
        result = _check_session_mutex()
        assert result is None
        assert state.get_value("copilot.pid") == ""

    @patch.object(session_module.os, "getpid", return_value=7777)
    @patch.object(session_module, "_is_process_alive", return_value=False)
    def test_claim_replaces_stale_pid(self, _mock_alive, _mock_getpid, temp_state):
        """claim=True replaces stale PID with current process PID."""
        state.set_value("copilot.pid", "99999")
        result = _check_session_mutex(claim=True)
        assert result is None
        assert state.get_value("copilot.pid") == 7777
