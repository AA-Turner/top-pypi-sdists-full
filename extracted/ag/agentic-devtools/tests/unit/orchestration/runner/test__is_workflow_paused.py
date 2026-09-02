"""Tests for _is_workflow_paused helper."""

import pytest

from agentic_devtools.orchestration.runner import _is_workflow_paused


class TestIsWorkflowPaused:
    """Tests for the _is_workflow_paused helper function."""

    def test_returns_true_when_status_active(self):
        """A status of 'active' means the workflow is paused."""
        assert _is_workflow_paused({"step": "planning", "status": "active"}) is True

    def test_returns_true_when_status_empty(self):
        """An empty status string means the workflow is paused."""
        assert _is_workflow_paused({"step": "planning", "status": ""}) is True

    def test_returns_true_when_status_missing(self):
        """A missing status key means the workflow is paused."""
        assert _is_workflow_paused({"step": "planning"}) is True

    def test_returns_false_when_status_completed(self):
        """A status of 'completed' means the workflow is NOT paused."""
        assert _is_workflow_paused({"step": "completion", "status": "completed"}) is False

    @pytest.mark.parametrize("status", ["failed", "blocked"])
    def test_returns_false_for_terminal_non_completed_statuses(self, status):
        """Terminal failure/blocked statuses are NOT treated as paused."""
        assert _is_workflow_paused({"step": "error_handler", "status": status}) is False

    def test_raises_for_none_result(self):
        """None result raises RuntimeError — unexpected LangGraph return type."""
        with pytest.raises(RuntimeError, match="Unexpected LangGraph invoke\\(\\) return type"):
            _is_workflow_paused(None)

    def test_raises_for_non_dict_result(self):
        """Non-dict result raises RuntimeError — unexpected LangGraph return type."""
        with pytest.raises(RuntimeError, match="Unexpected LangGraph invoke\\(\\) return type"):
            _is_workflow_paused("unexpected")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "status",
        ["active", "paused", "running", "waiting", "error", ""],
    )
    def test_returns_true_for_various_non_completed_statuses(self, status):
        """Non-terminal statuses are treated as paused."""
        assert _is_workflow_paused({"step": "some_step", "status": status}) is True
