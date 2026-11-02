"""Tests for _clear_session_mutex_pid."""

from agentic_devtools.cli.copilot.session import _clear_session_mutex_pid

_COPILOT_NS = "copilot"


class TestClearSessionMutexPid:
    """Tests for _clear_session_mutex_pid helper function."""

    def test_missing_copilot_namespace_is_noop(self):
        """No copilot key in state → returns without modifying state."""
        state: dict = {}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert state == {}

    def test_malformed_copilot_state_not_dict(self):
        """copilot namespace is not a dict → returns without modifying state."""
        state: dict = {_COPILOT_NS: "not-a-dict"}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert state == {_COPILOT_NS: "not-a-dict"}

    def test_malformed_copilot_state_none(self):
        """copilot namespace is None → returns without modifying state."""
        state: dict = {_COPILOT_NS: None}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert state == {_COPILOT_NS: None}

    def test_unparseable_pid_value_is_noop(self):
        """Non-numeric pid value → returns without modifying the pid entry."""
        copilot_state = {"pid": "not-a-number"}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == "not-a-number"

    def test_pid_not_str_or_int_is_noop(self):
        """pid value that is neither int nor str → returns without modifying."""
        copilot_state = {"pid": [1234]}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == [1234]

    def test_ownership_match_clears_pid(self):
        """When current pid matches owner_pid, pid is set to empty string."""
        copilot_state = {"pid": 1234}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == ""

    def test_ownership_match_string_pid_clears_pid(self):
        """String pid matching owner_pid is also cleared."""
        copilot_state = {"pid": "1234"}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == ""

    def test_ownership_mismatch_leaves_pid_unchanged(self):
        """When current pid does not match owner_pid, pid is not modified."""
        copilot_state = {"pid": 9999}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == 9999

    def test_ownership_mismatch_string_pid_leaves_pid_unchanged(self):
        """String pid not matching owner_pid is left unchanged."""
        copilot_state = {"pid": "9999"}
        state: dict = {_COPILOT_NS: copilot_state}
        _clear_session_mutex_pid(state, owner_pid=1234)
        assert copilot_state["pid"] == "9999"
