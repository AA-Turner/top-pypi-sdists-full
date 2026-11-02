"""Tests for error_handler_node function."""

from agentic_devtools.models.git_results import BlockedState, CommitResult, SetupResult
from agentic_devtools.orchestration.pilot_workflow import error_handler_node


class TestErrorHandlerNode:
    def test_sets_status_to_failed(self):
        result = error_handler_node({"step": "commit", "error": "something broke"})
        assert result["status"] == "failed"

    def test_sets_step_to_error_handler(self):
        result = error_handler_node({"step": "planning", "error": "boom"})
        assert result["step"] == "error_handler"

    def test_emits_error_handler_invoked_event(self):
        result = error_handler_node({"step": "verification", "error": "test failed"})
        assert len(result["events"]) == 1
        assert result["events"][0]["event"] == "error_handler_invoked"

    def test_event_signals_contain_error_context(self):
        result = error_handler_node({"step": "commit", "error": "git push failed"})
        signals = result["events"][0]["signals"]
        assert signals["error"] == "git push failed"
        assert signals["failed_step"] == "commit"

    def test_handles_missing_error_gracefully(self):
        result = error_handler_node({})
        assert result["status"] == "failed"
        signals = result["events"][0]["signals"]
        assert signals["error"] is None
        assert signals["failed_step"] is None

    def test_sets_error_field_on_failed_state(self):
        result = error_handler_node({"error": "git push failed"})
        assert result["error"] == "git push failed"

    def test_preserves_blocked_status_from_planning(self):
        """Incoming status='blocked' must survive the error_handler node unchanged."""
        result = error_handler_node({"step": "planning", "status": "blocked", "error": "Issue too vague"})
        assert result["status"] == "blocked"

    def test_overrides_other_statuses_to_failed(self):
        """Non-blocked incoming status (e.g. 'active') is replaced with 'failed'."""
        result = error_handler_node({"step": "commit", "status": "active", "error": "git push failed"})
        assert result["status"] == "failed"

    def test_derives_blocked_from_setup_result_error(self):
        """status='blocked' is derived from a setup_result with a non-None error."""
        blocked = BlockedState(category="transient", message="fetch failed")
        setup_result = SetupResult(error=blocked)
        result = error_handler_node({"step": "setup", "setup_result": setup_result, "error": "fetch failed"})
        assert result["status"] == "blocked"

    def test_derives_blocked_from_commit_result_error(self):
        """status='blocked' is derived from a commit_result with a non-None error."""
        blocked = BlockedState(category="conflict", message="push rejected")
        commit_result = CommitResult(error=blocked)
        result = error_handler_node({"step": "commit", "commit_result": commit_result, "error": "push rejected"})
        assert result["status"] == "blocked"
