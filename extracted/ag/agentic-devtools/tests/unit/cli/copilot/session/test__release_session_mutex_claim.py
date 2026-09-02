"""Tests for _release_session_mutex_claim."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.copilot import session as session_module
from agentic_devtools.cli.copilot.session import _release_session_mutex_claim


@pytest.fixture
def temp_state(tmp_path):
    """Redirect state storage to a temp directory."""
    with patch.object(state, "get_state_dir", return_value=tmp_path):
        with patch.object(session_module, "get_state_dir", return_value=tmp_path):
            state.clear_state()
            yield tmp_path


class TestReleaseSessionMutexClaim:
    """Tests for _release_session_mutex_claim helper."""

    def test_clears_pid_when_owned(self, temp_state):
        """_release_session_mutex_claim clears pid when owned by caller."""
        state.set_value("copilot.pid", "5555")
        _release_session_mutex_claim(5555)
        assert state.get_value("copilot.pid") == ""

    def test_ignores_non_owned_pid(self, temp_state):
        """_release_session_mutex_claim leaves pid when owned by another process."""
        state.set_value("copilot.pid", "5555")
        _release_session_mutex_claim(6666)
        assert state.get_value("copilot.pid") == "5555"

    def test_ignores_non_dict_copilot_state(self, temp_state):
        """_release_session_mutex_claim is a no-op when copilot state is malformed."""
        state.set_value("copilot", "bad-state")
        _release_session_mutex_claim(5555)
        assert state.get_value("copilot") == "bad-state"

    def test_ignores_non_scalar_pid(self, temp_state):
        """_release_session_mutex_claim is a no-op for non int/str pid values."""
        state.set_value("copilot.pid", ["bad"])
        _release_session_mutex_claim(5555)
        assert state.get_value("copilot.pid") == ["bad"]

    def test_ignores_unparseable_pid(self, temp_state):
        """_release_session_mutex_claim is a no-op for unparseable string pid values."""
        state.set_value("copilot.pid", "not-a-number")
        _release_session_mutex_claim(5555)
        assert state.get_value("copilot.pid") == "not-a-number"

    def test_uses_explicit_state_file(self, temp_state, tmp_path):
        """Explicit state-file cleanup clears a matching PID without relying on process CWD."""
        path = tmp_path / "explicit-state.json"
        path.write_text(json.dumps({"copilot": {"pid": "5555"}}), encoding="utf-8")

        _release_session_mutex_claim(5555, state_file_path=path)

        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["copilot"]["pid"] == ""

    def test_leaves_explicit_state_file_when_pid_not_owned(self, temp_state, tmp_path):
        """Explicit state-file cleanup does not clear a PID owned by another process."""
        path = tmp_path / "explicit-state.json"
        original = {"copilot": {"pid": "5555"}}
        path.write_text(json.dumps(original), encoding="utf-8")

        _release_session_mutex_claim(6666, state_file_path=path)

        assert json.loads(path.read_text(encoding="utf-8")) == original

    def test_ignores_corrupt_explicit_state_file(self, temp_state, tmp_path):
        """Explicit state-file cleanup ignores malformed JSON."""
        path = tmp_path / "explicit-state.json"
        path.write_text("{", encoding="utf-8")

        _release_session_mutex_claim(5555, state_file_path=path)

        assert path.read_text(encoding="utf-8") == "{"

    def test_ignores_non_dict_explicit_state_file(self, temp_state, tmp_path):
        """Explicit state-file cleanup ignores a non-object JSON document."""
        path = tmp_path / "explicit-state.json"
        path.write_text("[]", encoding="utf-8")

        _release_session_mutex_claim(5555, state_file_path=path)

        assert json.loads(path.read_text(encoding="utf-8")) == []
