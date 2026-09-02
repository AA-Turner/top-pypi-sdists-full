"""Tests for _get_issue_key_candidate."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import _get_issue_key_candidate


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
def test_get_issue_key_candidate_prefers_scoped_issue_key(mock_get_value, mock_get_bootstrap_state) -> None:
    mock_get_value.return_value = 42

    assert _get_issue_key_candidate() == "42"
    mock_get_bootstrap_state.assert_not_called()


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_value")
def test_get_issue_key_candidate_falls_back_to_bootstrap_worktree_key(mock_get_value, mock_get_bootstrap_state) -> None:
    mock_get_value.return_value = ""
    mock_get_bootstrap_state.return_value = {"worktree_key": "BOOT-7"}

    assert _get_issue_key_candidate() == "BOOT-7"
