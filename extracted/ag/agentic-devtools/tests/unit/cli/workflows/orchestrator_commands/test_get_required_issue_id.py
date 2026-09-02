"""Tests for _get_required_issue_id."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import _get_required_issue_id


@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_issue_key_candidate")
def test_get_required_issue_id_returns_none_when_issue_key_missing(mock_get_issue_key_candidate, capsys) -> None:
    mock_get_issue_key_candidate.return_value = ""

    assert _get_required_issue_id("finalizing") is None
    assert "must be set and valid before finalizing" in capsys.readouterr().out


@patch("agentic_devtools.cli.workflows.orchestrator_commands._get_issue_key_candidate")
def test_get_required_issue_id_normalizes_valid_issue_key(mock_get_issue_key_candidate) -> None:
    mock_get_issue_key_candidate.return_value = "#42"

    assert _get_required_issue_id("initializing") == "42"
