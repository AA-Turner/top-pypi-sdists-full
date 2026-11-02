"""Tests for GitHubActionsProvider.list_open_copilot_pr_briefs()."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError


class TestListOpenCopilotPrBriefs:
    """Tests for the copilot-head open-PR enumerator used by the takeover."""

    def test_uses_pooled_rest_api_pages(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {
                    "number": 1,
                    "head": {"ref": "copilot/fix"},
                    "created_at": "2026-01-01",
                }
            ]
        )
        with (
            patch("agentic_devtools.cli.ci.github_provider.run_safe") as run_safe,
            patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload) as gh_api,
        ):
            assert provider.list_open_copilot_pr_briefs() == [
                {"number": 1, "head_branch": "copilot/fix", "created_at": "2026-01-01"}
            ]

        gh_api.assert_called_once_with("/repos/o/r/pulls?state=open&per_page=100&page=1")
        run_safe.assert_not_called()

    def test_reads_no_more_than_two_full_pages(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        first_page = [
            {"number": number, "head": {"ref": f"copilot/{number}"}, "created_at": "2026-01-01"}
            for number in range(1, 101)
        ]
        second_page = [{"number": 101, "head": {"ref": "copilot/101"}, "created_at": "2026-01-02"}]

        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=[json.dumps(first_page), json.dumps(second_page)],
        ) as gh_api:
            briefs = provider.list_open_copilot_pr_briefs()

        assert len(briefs) == 101
        assert [call.args[0] for call in gh_api.call_args_list] == [
            "/repos/o/r/pulls?state=open&per_page=100&page=1",
            "/repos/o/r/pulls?state=open&per_page=100&page=2",
        ]

    def test_stops_after_two_full_pages(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        full_page = [{"number": number, "head": {"ref": f"copilot/{number}"}} for number in range(1, 101)]
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            side_effect=[json.dumps(full_page), json.dumps(full_page)],
        ) as gh_api:
            briefs = provider.list_open_copilot_pr_briefs()

        assert len(briefs) == 200
        assert gh_api.call_count == 2

    def test_filters_non_copilot_and_sorts_oldest_first(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 2, "head": {"ref": "copilot/b"}, "created_at": "2026-01-02"},
                {"number": 1, "head": {"ref": "copilot/a"}, "created_at": "2026-01-01"},
                {"number": 3, "head": {"ref": "feature/x"}, "created_at": "2026-01-03"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload):
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
                {"number": True, "head": {"ref": "copilot/boolean"}, "created_at": "x"},
                {"number": 0, "head": {"ref": "copilot/zero"}, "created_at": "x"},
                {"number": -1, "head": {"ref": "copilot/neg"}, "created_at": "x"},
                {"number": 5, "head": {"ref": "copilot/ok"}, "created_at": "2026-01-05"},
                {"number": 6, "head": {"ref": "copilot/no-ts"}, "created_at": 123},
                {"number": 7, "head": {"ref": 123}, "created_at": "x"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload):
            briefs = provider.list_open_copilot_pr_briefs()
        assert briefs == [
            {"number": 5, "head_branch": "copilot/ok", "created_at": "2026-01-05"},
            {"number": 6, "head_branch": "copilot/no-ts", "created_at": ""},
        ]

    def test_handles_missing_optional_fields(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 9},  # missing head.ref → "" → not copilot → skipped
                {"number": 7, "head": {"ref": "copilot/c"}},  # missing created_at → ""
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload):
            briefs = provider.list_open_copilot_pr_briefs()
        assert briefs == [{"number": 7, "head_branch": "copilot/c", "created_at": ""}]

    def test_missing_timestamp_sorted_last(self) -> None:
        """Empty created_at should sort after valid ISO timestamps (treated as newest)."""
        provider = GitHubActionsProvider(repo="o/r")
        payload = json.dumps(
            [
                {"number": 10, "head": {"ref": "copilot/no-ts"}},  # missing → ""
                {"number": 1, "head": {"ref": "copilot/old"}, "created_at": "2026-01-01"},
                {"number": 5, "head": {"ref": "copilot/mid"}, "created_at": "2026-06-01"},
            ]
        )
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=payload):
            briefs = provider.list_open_copilot_pr_briefs()
        assert [b["number"] for b in briefs] == [1, 5, 10]

    def test_empty_stdout_returns_empty(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=""):
            assert provider.list_open_copilot_pr_briefs() == []

    def test_raises_on_invalid_json_output(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="not-json"):
            with pytest.raises(RuntimeError, match="gh pr list returned invalid JSON output"):
                provider.list_open_copilot_pr_briefs()

    def test_raises_with_stderr_on_nonzero_exit(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=RuntimeError("boom")):
            with pytest.raises(RuntimeError, match="gh pr list failed: boom"):
                provider.list_open_copilot_pr_briefs()

    def test_propagates_retryable_provider_error(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        expected = RetryableError("rate limited")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=expected):
            with pytest.raises(RetryableError) as raised:
                provider.list_open_copilot_pr_briefs()

        assert raised.value is expected

    def test_raises_when_response_is_not_a_list(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            return_value="{}",
        ):
            with pytest.raises(RuntimeError, match="gh pr list returned invalid JSON output"):
                provider.list_open_copilot_pr_briefs()
