"""Tests for _read_assignment_postcondition()."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.agent_assignment import _read_assignment_postcondition


@patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call", return_value=json.dumps({}))
def test_handles_unexpected_shape(mock_gh_api: MagicMock) -> None:
    assert _read_assignment_postcondition(
        repo="owner/repo",
        issue_number=42,
        token="token",
        token_identity="SPECKIT_PR_TOKEN",
        max_reads=1,
    ) == (None, "unexpected_response_shape")
    mock_gh_api.assert_called_once()


@patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
@patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
def test_retries_after_negative_read(mock_gh_api: MagicMock, mock_sleep: MagicMock) -> None:
    mock_gh_api.side_effect = [
        json.dumps({"number": 42, "assignees": []}),
        json.dumps({"number": 42, "assignees": [{"login": "Copilot"}]}),
    ]

    assert _read_assignment_postcondition(
        repo="owner/repo",
        issue_number=42,
        token="token",
        token_identity="SPECKIT_PR_TOKEN",
        max_reads=2,
    ) == (True, "copilot_assigned")
    assert mock_gh_api.call_count == 2
    mock_sleep.assert_called_once_with(1)


@patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
@patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
def test_retries_after_unexpected_shape(mock_gh_api: MagicMock, mock_sleep: MagicMock) -> None:
    mock_gh_api.side_effect = [
        json.dumps({}),
        json.dumps({"number": 42, "assignees": [{"login": "Copilot"}]}),
    ]

    assert _read_assignment_postcondition(
        repo="owner/repo",
        issue_number=42,
        token="token",
        token_identity="SPECKIT_PR_TOKEN",
        max_reads=2,
    ) == (True, "copilot_assigned")
    assert mock_gh_api.call_count == 2
    mock_sleep.assert_called_once_with(1)


@patch("agentic_devtools.cli.ci.retry.time.sleep", return_value=None)
@patch("agentic_devtools.cli.ci.agent_assignment._gh_api_call")
def test_treats_malformed_assignee_entries_as_inconclusive(mock_gh_api: MagicMock, mock_sleep: MagicMock) -> None:
    mock_gh_api.side_effect = [
        json.dumps({"number": 42, "assignees": [None]}),
        json.dumps({"number": 42, "assignees": [{"login": "Copilot"}]}),
    ]

    assert _read_assignment_postcondition(
        repo="owner/repo",
        issue_number=42,
        token="token",
        token_identity="SPECKIT_PR_TOKEN",
        max_reads=2,
    ) == (True, "copilot_assigned")
    assert mock_gh_api.call_count == 2
    mock_sleep.assert_called_once_with(1)
