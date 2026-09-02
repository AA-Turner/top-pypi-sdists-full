"""Tests for GitHubActionsProvider.list_all_review_comments() method."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewCommentInfo


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


class TestListAllReviewComments:
    """Tests for GitHubActionsProvider.list_all_review_comments()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_review_comment_info_list(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 100,
                    "path": "src/main.py",
                    "body": "Consider refactoring",
                    "html_url": "https://github.com/owner/repo/pull/1#discussion_r100",
                    "start_line": 10,
                    "line": 15,
                    "position": 5,
                    "diff_hunk": "@@ -10,5 +10,5 @@",
                    "commit_id": "abc123",
                    "original_commit_id": "def456",
                    "pull_request_review_id": 321,
                    "user": {"login": "reviewer1"},
                    "in_reply_to_id": None,
                },
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=42)

        assert len(result) == 1
        assert isinstance(result[0], ReviewCommentInfo)
        assert result[0].id == 100
        assert result[0].path == "src/main.py"
        assert result[0].body == "Consider refactoring"
        assert result[0].author_login == "reviewer1"
        assert result[0].start_line == 10
        assert result[0].end_line == 15
        assert result[0].source_review_id == 321

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_empty_comments(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([])

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=1)

        assert result == []

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_handles_empty_string_response(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response("  ")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=1)

        assert result == []

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_suppressed_comment_detected(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 200,
                    "path": "file.py",
                    "body": "hidden",
                    "html_url": "",
                    "is_minimized": True,
                    "user": {"login": "bot"},
                },
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=1)

        assert len(result) == 1
        assert result[0].is_suppressed is True

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_source_review_id_defaults_to_zero_when_absent(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 201,
                    "path": "file.py",
                    "body": "feedback",
                    "html_url": "https://github.com/owner/repo/pull/1#discussion_r201",
                },
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=1)

        assert len(result) == 1
        assert result[0].source_review_id == 0

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_source_review_id_defaults_to_zero_when_none(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 202,
                    "path": "file.py",
                    "body": "feedback",
                    "html_url": "https://github.com/owner/repo/pull/1#discussion_r202",
                    "pull_request_review_id": None,
                },
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_all_review_comments(pr_number=1)

        assert len(result) == 1
        assert result[0].source_review_id == 0
