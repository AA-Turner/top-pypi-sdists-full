"""Tests for _transfer_session_mutex_claim."""

from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.copilot import session as session_module
from agentic_devtools.cli.copilot.session import _transfer_session_mutex_claim


@pytest.fixture
def temp_state(tmp_path):
    """Redirect state storage to a temp directory."""
    with patch.object(state, "get_state_dir", return_value=tmp_path):
        with patch.object(session_module, "get_state_dir", return_value=tmp_path):
            state.clear_state()
            yield tmp_path


class TestTransferSessionMutexClaim:
    """Tests for _transfer_session_mutex_claim helper."""

    def test_transfers_pid_when_owned(self, temp_state):
        """_transfer_session_mutex_claim updates pid when owned by old_pid."""
        state.set_value("copilot.pid", 4242)
        assert _transfer_session_mutex_claim(4242, 8888) is True
        assert state.get_value("copilot.pid") == 8888

    def test_skips_transfer_when_pid_not_matching(self, temp_state):
        """_transfer_session_mutex_claim is a no-op when stored PID does not match old_pid."""
        state.set_value("copilot.pid", 9999)
        assert _transfer_session_mutex_claim(4242, 8888) is False
        assert state.get_value("copilot.pid") == 9999

    def test_skips_transfer_when_pid_not_parseable(self, temp_state):
        """_transfer_session_mutex_claim is a no-op when stored PID is not parseable."""
        state.set_value("copilot.pid", "not-a-pid")
        assert _transfer_session_mutex_claim(4242, 8888) is False
        assert state.get_value("copilot.pid") == "not-a-pid"

    def test_ignores_non_dict_copilot_state(self, temp_state):
        """_transfer_session_mutex_claim is a no-op when copilot state is malformed."""
        state.set_value("copilot", "bad-state")
        assert _transfer_session_mutex_claim(4242, 8888) is False
        assert state.get_value("copilot") == "bad-state"

    def test_suppresses_state_write_errors(self, temp_state):
        """_transfer_session_mutex_claim suppresses exceptions from state writes."""
        state.set_value("copilot.pid", 4242)
        with patch.object(session_module, "read_modify_write_state", side_effect=OSError("locked")):
            assert _transfer_session_mutex_claim(4242, 8888) is False
        assert state.get_value("copilot.pid") == 4242
