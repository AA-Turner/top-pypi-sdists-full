"""Tests for fetch_github_issue_data."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.nodes._issue_retrieval import fetch_github_issue_data


class TestFetchGithubIssueData:
    """Tests for GitHub issue retrieval with comment truncation."""

    def _make_issue_detail(
        self,
        *,
        title: str = "Issue title",
        description: str = "Issue body",
        status: str = "open",
        labels: list[str] | None = None,
        comments: list | None = None,
    ) -> dict:
        return {
            "title": title,
            "description": description,
            "status": status,
            "labels": labels or [],
            "comments": comments or [],
        }

    def test_basic_issue_returns_normalized_dict(self) -> None:
        issue = self._make_issue_detail(labels=["bug", "high-priority"])
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter", return_value=adapter),
        ):
            result = fetch_github_issue_data("42", repo="owner/repo")

        assert result["key"] == "42"
        assert result["provider"] == "github"
        assert result["summary"] == "Issue title"
        assert result["description"] == "Issue body"
        assert result["labels"] == ["bug", "high-priority"]
        assert result["parent_key"] is None
        assert result["parent_summary"] is None
        assert result["epic_key"] is None
        assert result["epic_summary"] is None
        assert result["issue_type"] is None

    def test_issue_without_body(self) -> None:
        issue = self._make_issue_detail(description="")
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter", return_value=adapter),
        ):
            result = fetch_github_issue_data("#42", repo="owner/repo")

        assert result["description"] == ""
        assert result["acceptance_criteria"] is None

    def test_comments_truncated_to_30(self) -> None:
        # Create 35 comments
        comments = [
            {"comment_id": str(i), "body": f"Comment {i}", "created_at": f"2024-01-{i:02d}"} for i in range(1, 36)
        ]
        issue = self._make_issue_detail(comments=comments)
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter", return_value=adapter),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_github_comments",
                return_value=None,
            ),
        ):
            result = fetch_github_issue_data("99", repo="owner/repo")

        assert len(result["comments"]) == 30
        # Should keep the 30 newest (6-35) in chronological order
        assert result["comments"][0]["comment_id"] == "6"
        assert result["comments"][-1]["comment_id"] == "35"

    def test_empty_issue_key_raises(self) -> None:
        with pytest.raises(RuntimeError, match="must be a positive integer"):
            fetch_github_issue_data("", repo="owner/repo")

    def test_non_numeric_issue_key_raises(self) -> None:
        with pytest.raises(RuntimeError, match="must be a positive integer"):
            fetch_github_issue_data("abc", repo="owner/repo")

    def test_option_like_issue_key_raises(self) -> None:
        with pytest.raises(RuntimeError, match="must be a positive integer"):
            fetch_github_issue_data("--help", repo="owner/repo")

    def test_no_repo_resolved_raises(self) -> None:
        with patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value=None):
            with pytest.raises(RuntimeError, match="Cannot resolve GitHub repository"):
                fetch_github_issue_data("42")

    def test_gh_cli_error_raises(self) -> None:
        adapter = MagicMock()
        adapter.get_issue.side_effect = RuntimeError("gh command failed: not authenticated (auth)")

        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter", return_value=adapter),
        ):
            with pytest.raises(RuntimeError, match="authentication failed"):
                fetch_github_issue_data("42", repo="owner/repo")

    def test_acceptance_criteria_extracted_from_body(self) -> None:
        desc = "## Overview\nSome text\n## Acceptance Criteria\n- Must do X\n- Must do Y"
        issue = self._make_issue_detail(description=desc)
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo"),
            patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter", return_value=adapter),
        ):
            result = fetch_github_issue_data("42", repo="owner/repo")

        assert result["acceptance_criteria"] is not None
        assert "Must do X" in result["acceptance_criteria"]


class TestFetchGitHubIssueDataBranches:
    """Cover remaining GitHub branch conditions."""

    def test_generic_runtime_error_raised(self) -> None:
        """RuntimeError without 'not found' or 'auth' re-raises as generic error."""
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter.get_issue",
                side_effect=RuntimeError("server error 500"),
            ),
        ):
            with pytest.raises(RuntimeError, match="GitHub API error"):
                fetch_github_issue_data("42")

    def test_missing_gh_cli_is_reported_clearly(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter.get_issue",
                side_effect=FileNotFoundError("gh"),
            ),
        ):
            with pytest.raises(RuntimeError, match="GitHub CLI is not installed or not on PATH"):
                fetch_github_issue_data("42")


class TestFetchGitHubNotFound:
    """Cover not-found and auth error branches."""

    def test_not_found_error(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter.get_issue",
                side_effect=RuntimeError("not found 404"),
            ),
        ):
            with pytest.raises(RuntimeError, match="GitHub issue not found"):
                fetch_github_issue_data("42")

    def test_auth_error(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter.get_issue",
                side_effect=RuntimeError("401 Unauthorized auth failed"),
            ),
        ):
            with pytest.raises(RuntimeError, match="GitHub authentication failed"):
                fetch_github_issue_data("42")

    def test_non_auth_word_containing_auth_substring_is_not_misclassified(self) -> None:
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter.get_issue",
                side_effect=RuntimeError("author metadata unavailable"),
            ),
        ):
            with pytest.raises(RuntimeError, match="GitHub API error"):
                fetch_github_issue_data("42")


class TestFetchGitHubFewComments:
    """Cover the branch where comments count is under the max limit."""

    def test_fewer_than_max_comments_kept(self) -> None:
        """When there are fewer than 30 comments, all are kept."""
        mock_comments = []
        for i in range(3):
            c = {"comment_id": str(i), "body": f"Comment {i}", "created_at": f"2024-01-0{i + 1}T00:00:00Z"}
            mock_comments.append(c)
        mock_issue = {
            "title": "Test",
            "description": "Desc",
            "status": "open",
            "labels": [],
            "comments": mock_comments,
        }

        adapter = MagicMock()
        adapter.get_issue.return_value = mock_issue

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            result = fetch_github_issue_data("42")
        assert len(result["comments"]) == 3


class TestFetchGitHubNonDictComment:
    """Non-dict items in GitHub comments are skipped."""

    def test_non_dict_comment_skipped(self) -> None:
        mock_issue = {
            "title": "Test",
            "description": "Desc",
            "status": "open",
            "labels": [],
            "comments": [
                "not-a-dict",
                {"comment_id": "1", "body": "real", "created_at": "2024-01-01"},
            ],
        }
        adapter = MagicMock()
        adapter.get_issue.return_value = mock_issue

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            result = fetch_github_issue_data("42")
        assert len(result["comments"]) == 1
        assert result["comments"][0]["body"] == "real"


class TestFetchGithubIssueDataNonDictReturn:
    """adapter.get_issue() returns a non-dict → RuntimeError raised."""

    def test_none_return_raises_runtime_error(self) -> None:
        adapter = MagicMock()
        adapter.get_issue.return_value = None

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            with pytest.raises(RuntimeError, match="unexpected type"):
                fetch_github_issue_data("42")

    def test_list_return_raises_runtime_error(self) -> None:
        adapter = MagicMock()
        adapter.get_issue.return_value = [{"title": "x"}]

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            with pytest.raises(RuntimeError, match="unexpected type"):
                fetch_github_issue_data("42")


class TestFetchGithubIssueDataNonStringDescription:
    """Non-string description is coerced to empty string."""

    def test_dict_description_coerced_to_empty(self) -> None:
        adapter = MagicMock()
        adapter.get_issue.return_value = {
            "title": "My issue",
            "description": {"version": 1, "type": "doc"},
            "status": "open",
            "labels": [],
            "comments": [],
        }

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            result = fetch_github_issue_data("42")

        assert result["description"] == ""
        assert result["acceptance_criteria"] is None


class TestFetchGithubIssueDataFieldTypeCoercion:
    """summary/status/labels are coerced to expected types."""

    def _patch_adapter(self, issue_detail: dict) -> tuple:
        adapter = MagicMock()
        adapter.get_issue.return_value = issue_detail
        return (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        )

    def test_non_string_title_coerced_to_empty(self) -> None:
        p1, p2 = self._patch_adapter({"title": 123, "description": "", "status": "open", "labels": [], "comments": []})
        with p1, p2:
            result = fetch_github_issue_data("42")
        assert result["summary"] == ""

    def test_none_title_coerced_to_empty(self) -> None:
        p1, p2 = self._patch_adapter({"title": None, "description": "", "status": "open", "labels": [], "comments": []})
        with p1, p2:
            result = fetch_github_issue_data("42")
        assert result["summary"] == ""

    def test_non_string_status_coerced_to_empty(self) -> None:
        p1, p2 = self._patch_adapter(
            {"title": "T", "description": "", "status": {"state": "open"}, "labels": [], "comments": []}
        )
        with p1, p2:
            result = fetch_github_issue_data("42")
        assert result["status"] == ""

    def test_non_list_labels_coerced_to_empty_list(self) -> None:
        p1, p2 = self._patch_adapter(
            {"title": "T", "description": "", "status": "open", "labels": "bug", "comments": []}
        )
        with p1, p2:
            result = fetch_github_issue_data("42")
        assert result["labels"] == []

    def test_none_labels_coerced_to_empty_list(self) -> None:
        p1, p2 = self._patch_adapter(
            {"title": "T", "description": "", "status": "open", "labels": None, "comments": []}
        )
        with p1, p2:
            result = fetch_github_issue_data("42")
        assert result["labels"] == []


class TestFetchGithubIssueDataCommentsNotList:
    """Non-list comments field yields an empty comment list."""

    def test_comments_not_list_returns_empty(self) -> None:
        adapter = MagicMock()
        adapter.get_issue.return_value = {
            "title": "T",
            "description": "",
            "status": "open",
            "labels": [],
            "comments": "not-a-list",
        }
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            result = fetch_github_issue_data("42")
        assert result["comments"] == []


class TestFetchGithubIssueDataPersistence:
    """state_dir persists the raw GitHub response."""

    def test_persists_response_when_state_dir_given(self, tmp_path) -> None:
        adapter = MagicMock()
        adapter.get_issue.return_value = {
            "title": "T",
            "description": "D",
            "status": "open",
            "labels": [],
            "comments": [],
        }
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
        ):
            fetch_github_issue_data("42", state_dir=tmp_path)
        persisted = tmp_path / "temp-get-issue-details-response.json"
        assert persisted.exists()
        assert '"title": "T"' in persisted.read_text(encoding="utf-8")


class TestFetchGithubIssueDataFilterFirstTruncation:
    """Non-dict entries are filtered before truncation so 30 valid comments are kept."""

    def test_non_dict_entries_do_not_reduce_kept_count(self) -> None:
        # 31 valid dict comments plus interspersed non-dict entries.
        comments: list = []
        for i in range(1, 32):
            comments.append({"comment_id": str(i), "body": f"c{i}", "created_at": f"2024-01-{i:02d}"})
        comments.insert(0, "not-a-dict")
        comments.insert(5, 12345)
        issue = {"title": "T", "description": "", "status": "open", "labels": [], "comments": comments}
        adapter = MagicMock()
        adapter.get_issue.return_value = issue
        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_github_comments",
                return_value=None,
            ),
        ):
            result = fetch_github_issue_data("42")
        # 31 valid dicts → 30 newest kept (days 02-31), non-dicts never consume slots.
        assert len(result["comments"]) == 30
        assert result["comments"][0]["comment_id"] == "2"
        assert result["comments"][-1]["comment_id"] == "31"


class TestFetchGithubIssueDataNewestComments:
    """When the embedded payload is at the cap, newest comments are fetched via REST."""

    def _make_issue(self, n: int) -> dict:
        comments = [{"comment_id": str(i), "body": f"c{i}", "created_at": f"2024-01-{i:02d}"} for i in range(1, n + 1)]
        return {"title": "T", "description": "", "status": "open", "labels": [], "comments": comments}

    def test_at_cap_calls_fetch_newest(self) -> None:
        """When embedded count == _MAX_COMMENTS, REST fetch is called."""
        from agentic_devtools.orchestration.nodes._issue_retrieval import _MAX_COMMENTS

        issue = self._make_issue(_MAX_COMMENTS)
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        newest = [
            {"comment_id": f"new_{i}", "body": "new", "created_at": f"2024-02-{i:02d}"}
            for i in range(1, _MAX_COMMENTS + 1)
        ]

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_github_comments",
                return_value=newest,
            ) as mock_fetch,
        ):
            result = fetch_github_issue_data("42", repo="owner/repo")

        mock_fetch.assert_called_once_with("owner/repo", "42", _MAX_COMMENTS)
        assert result["comments"][0]["comment_id"] == "new_1"

    def test_fetch_newest_failure_falls_back_to_embedded(self) -> None:
        """When REST fetch returns None, the embedded list is used."""
        from agentic_devtools.orchestration.nodes._issue_retrieval import _MAX_COMMENTS

        issue = self._make_issue(_MAX_COMMENTS)
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_github_comments",
                return_value=None,
            ),
        ):
            result = fetch_github_issue_data("42", repo="owner/repo")

        # Falls back to embedded comments (all 30, chronological)
        assert len(result["comments"]) == _MAX_COMMENTS
        assert result["comments"][0]["comment_id"] == "1"

    def test_below_cap_does_not_call_fetch_newest(self) -> None:
        """When embedded count < _MAX_COMMENTS, REST fetch is NOT called."""
        from agentic_devtools.orchestration.nodes._issue_retrieval import _MAX_COMMENTS

        issue = self._make_issue(_MAX_COMMENTS - 1)
        adapter = MagicMock()
        adapter.get_issue.return_value = issue

        with (
            patch(
                "agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe",
                return_value="owner/repo",
            ),
            patch(
                "agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter",
                return_value=adapter,
            ),
            patch(
                "agentic_devtools.orchestration.nodes._issue_retrieval._fetch_newest_github_comments",
            ) as mock_fetch,
        ):
            result = fetch_github_issue_data("42", repo="owner/repo")

        mock_fetch.assert_not_called()
        assert len(result["comments"]) == _MAX_COMMENTS - 1
