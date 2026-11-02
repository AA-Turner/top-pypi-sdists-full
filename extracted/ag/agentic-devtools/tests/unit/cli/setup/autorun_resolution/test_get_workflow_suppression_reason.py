"""Tests for get_workflow_suppression_reason."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.autorun_resolution import get_workflow_suppression_reason


def _patch_state(value: object):
    """Patch ``get_workflow_state`` to return *value*."""
    return patch("agentic_devtools.state.get_workflow_state", return_value=value)


class TestGetWorkflowSuppressionReasonSuppressing:
    """Workflow states that suppress auto-run (FR-006)."""

    def test_work_on_jira_issue_setup_step(self) -> None:
        """The work-on-jira-issue workflow at the setup step suppresses auto-run."""
        with _patch_state({"active": "work-on-jira-issue", "step": "setup"}):
            reason = get_workflow_suppression_reason()

        assert reason is not None
        assert "work-on-jira-issue" in reason
        assert "setup" in reason

    def test_pull_request_review_initiate_step(self) -> None:
        """The pull-request-review workflow at the initiate step suppresses auto-run."""
        with _patch_state({"active": "pull-request-review", "step": "initiate"}):
            reason = get_workflow_suppression_reason()

        assert reason is not None
        assert "pull-request-review" in reason
        assert "initiate" in reason


class TestGetWorkflowSuppressionReasonNotSuppressing:
    """Workflow states that leave auto-run untouched."""

    @pytest.mark.parametrize(
        "state",
        [
            None,
            {},
            {"status": "active"},
            {"active": "work-on-jira-issue"},
            {"active": "work-on-jira-issue", "step": None},
            {"active": "work-on-jira-issue", "step": ""},
            {"active": "work-on-jira-issue", "step": "implementation"},
            {"active": "pull-request-review", "step": "review-file"},
            {"active": "create-jira-issue", "step": "setup"},
            {"active": None, "step": "setup"},
            # Malformed truthy non-string payloads must degrade to no
            # suppression rather than raising ``TypeError: unhashable type``.
            {"active": ["work-on-jira-issue"], "step": "setup"},
            {"active": "work-on-jira-issue", "step": ["setup"]},
            {"active": {"x": 1}, "step": "setup"},
            {"active": 123, "step": "setup"},
        ],
    )
    def test_returns_none(self, state: object) -> None:
        """Non-suppressing workflow states resolve to no suppression."""
        with _patch_state(state):
            assert get_workflow_suppression_reason() is None

    def test_non_dict_workflow_state(self) -> None:
        """A malformed (non-dict) workflow state never suppresses auto-run."""
        with _patch_state("work-on-jira-issue"):
            assert get_workflow_suppression_reason() is None

    def test_unreadable_state_file(self) -> None:
        """An unreadable state file degrades to no suppression instead of failing setup."""
        with patch("agentic_devtools.state.get_workflow_state", side_effect=OSError("permission denied")):
            assert get_workflow_suppression_reason() is None
