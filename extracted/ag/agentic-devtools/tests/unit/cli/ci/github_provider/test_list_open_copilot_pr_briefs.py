"""Tests for GitHubActionsProvider.list_open_copilot_pr_briefs()."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _result(returncode: int = 0, stdout: str = "[]", stderr: str = "") -> MagicMock:
    result = MagicMock()
    result.returncode = returncode
    result.stdout = stdout
    result.stderr = stderr
    return result


class TestListOpenCopilotPrBriefs:
    """Tests for the copilot-head open-PR enumerator used by the takeover."""

    def test_filters_non_copilot_and_sorts_oldest_first(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 2, "headRefName": "copilot/b", "createdAt": "2026-01-02"},
                {"number": 1, "headRefName": "copilot/a", "createdAt": "2026-01-01"},
                {"number": 3, "headRefName": "feature/x", "createdAt": "2026-01-03"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout=payload)):
            briefs = provider.list_open_copilot_pr_briefs()
        assert briefs == [
            {"number": 1, "head_branch": "copilot/a", "created_at": "2026-01-01"},
            {"number": 2, "head_branch": "copilot/b", "created_at": "2026-01-02"},
        ]

    def test_skips_non_dict_and_invalid_numbers(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                "not-a-dict",
                {"number": 0, "headRefName": "copilot/zero", "createdAt": "x"},
                {"number": -1, "headRefName": "copilot/neg", "createdAt": "x"},
                {"number": 5, "headRefName": "copilot/ok", "createdAt": "2026-01-05"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout=payload)):
            briefs = provider.list_open_copilot_pr_briefs()
        assert briefs == [{"number": 5, "head_branch": "copilot/ok", "created_at": "2026-01-05"}]

    def test_handles_missing_optional_fields(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 9},  # missing headRefName → "" → not copilot → skipped
                {"number": 7, "headRefName": "copilot/c"},  # missing createdAt → ""
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout=payload)):
            briefs = provider.list_open_copilot_pr_briefs()
        assert briefs == [{"number": 7, "head_branch": "copilot/c", "created_at": ""}]

    def test_missing_timestamp_sorted_last(self) -> None:
        """Empty created_at should sort after valid ISO timestamps (treated as newest)."""
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 10, "headRefName": "copilot/no-ts"},  # missing → ""
                {"number": 1, "headRefName": "copilot/old", "createdAt": "2026-01-01"},
                {"number": 5, "headRefName": "copilot/mid", "createdAt": "2026-06-01"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout=payload)):
            briefs = provider.list_open_copilot_pr_briefs()
        assert [b["number"] for b in briefs] == [1, 5, 10]

    def test_empty_stdout_returns_empty(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout="")):
            assert provider.list_open_copilot_pr_briefs() == []

    def test_raises_on_invalid_json_output(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_result(stdout="not-json")):
            with pytest.raises(RuntimeError, match="gh pr list returned invalid JSON output"):
                provider.list_open_copilot_pr_briefs()

    def test_raises_with_stderr_on_nonzero_exit(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider.run_safe",
            return_value=_result(returncode=1, stderr="boom"),
        ):
            with pytest.raises(RuntimeError, match="gh pr list failed: boom"):
                provider.list_open_copilot_pr_briefs()

    def test_raises_with_exit_code_when_no_stderr(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider.run_safe",
            return_value=_result(returncode=2, stderr=""),
        ):
            with pytest.raises(RuntimeError, match="gh pr list failed: exit code 2"):
                provider.list_open_copilot_pr_briefs()
