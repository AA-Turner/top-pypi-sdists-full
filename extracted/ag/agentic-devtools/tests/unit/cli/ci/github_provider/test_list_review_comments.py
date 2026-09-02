"""Tests for GitHubActionsProvider.list_review_comments() method."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


class TestListReviewComments:
    """Tests for GitHubActionsProvider.list_review_comments()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_preserves_reply_author_and_parent_metadata(self, mock_run_safe) -> None:
        """Root and Cloud Coding Agent reply metadata are mapped from REST payloads."""
        mock_run_safe.side_effect = [
            _mock_run_safe_response(
                [
                    {
                        "id": 101,
                        "path": "src/foo.py",
                        "body": "Fix this",
                        "html_url": "https://example.test/root",
                        "user": {"login": "copilot-pull-request-reviewer[bot]"},
                    },
                    {
                        "id": 202,
                        "path": "src/foo.py",
                        "body": "Implemented.",
                        "html_url": "https://example.test/reply",
                        "user": {"login": "copilot-swe-agent[bot]"},
                        "in_reply_to_id": 101,
                    },
                    {
                        "id": 303,
                        "path": "src/foo.py",
                        "body": "Malformed parent",
                        "html_url": "https://example.test/malformed",
                        "user": {"login": "copilot-swe-agent[bot]"},
                        "in_reply_to_id": "not-an-id",
                    },
                ]
            ),
            _mock_run_safe_response({"body": ""}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_comments(42, 7)

        assert result[0].author_login == "copilot-pull-request-reviewer[bot]"
        assert result[0].in_reply_to_id is None
        assert result[1].author_login == "copilot-swe-agent[bot]"
        assert result[1].in_reply_to_id == 101
        assert result[2].author_login == "copilot-swe-agent[bot]"
        assert result[2].in_reply_to_id is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_review_comment_info_objects(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 101,
                    "path": "src/foo.py",
                    "body": "Fix the null check",
                    "html_url": "https://github.com/owner/repo/pull/42#pullreviewcomment-101",
                    "line": 15,
                    "start_line": 14,
                },
                {
                    "id": 202,
                    "path": "src/bar.py",
                    "body": "Add error handling",
                    "html_url": "https://github.com/owner/repo/pull/42#pullreviewcomment-202",
                },
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 7)

        assert len(result) == 2
        assert isinstance(result[0], ReviewCommentInfo)
        assert result[0].id == 101
        assert result[0].path == "src/foo.py"
        assert result[0].body == "Fix the null check"
        assert result[0].html_url == "https://github.com/owner/repo/pull/42#pullreviewcomment-101"
        assert result[0].is_suppressed is False
        assert result[0].start_line == 14
        assert result[0].end_line == 15
        assert result[0].source_review_id == 7
        assert result[1].source_review_id == 7

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_is_suppressed_defaults_to_false(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [{"id": 1, "path": "f.py", "body": "x", "html_url": "http://x"}]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(1, 1)
        assert result[0].is_suppressed is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_is_suppressed_maps_from_minimized_flag(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [{"id": 2, "path": "f.py", "body": "x", "html_url": "http://x", "is_minimized": True}]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(1, 1)
        assert result[0].is_suppressed is True

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_handles_missing_optional_fields(self, mock_run_safe) -> None:
        """Missing body or html_url fall back to empty string."""
        mock_run_safe.return_value = _mock_run_safe_response([{"id": 5, "path": "foo.py"}])
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert len(result) == 1
        assert result[0].body == ""
        assert result[0].html_url == ""
        assert result[0].start_line is None
        assert result[0].end_line is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_uses_line_as_start_line_when_start_line_missing(self, mock_run_safe) -> None:
        """Single-line comments should map start_line from line."""
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 6,
                    "path": "foo.py",
                    "body": "single line",
                    "html_url": "https://example.test",
                    "line": 21,
                },
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert len(result) == 1
        assert result[0].start_line == 21
        assert result[0].end_line == 21

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_empty_list_when_no_comments(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([])
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 7)
        assert result == []

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_commit_id_is_populated_from_api_response(self, mock_run_safe) -> None:
        """commit_id from the API response is carried into ReviewCommentInfo."""
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 7,
                    "path": "src/foo.py",
                    "body": "fix this",
                    "html_url": "https://example.test",
                    "commit_id": "abc123def456",
                },
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert len(result) == 1
        assert result[0].commit_id == "abc123def456"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_commit_id_defaults_to_empty_string_when_absent(self, mock_run_safe) -> None:
        """commit_id falls back to empty string when not present in the API response."""
        mock_run_safe.return_value = _mock_run_safe_response(
            [{"id": 8, "path": "src/foo.py", "body": "fix", "html_url": "https://example.test"}]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert result[0].commit_id == ""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_original_commit_id_is_populated_from_api_response(self, mock_run_safe) -> None:
        """original_commit_id from the API response is carried into ReviewCommentInfo."""
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 9,
                    "path": "src/foo.py",
                    "body": "fix this",
                    "html_url": "https://example.test",
                    "commit_id": "5008f6e",
                    "original_commit_id": "83bf0725",
                },
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert len(result) == 1
        assert result[0].commit_id == "5008f6e"
        assert result[0].original_commit_id == "83bf0725"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_original_commit_id_defaults_to_empty_string_when_absent(self, mock_run_safe) -> None:
        """original_commit_id falls back to empty string when not present in the API response."""
        mock_run_safe.return_value = _mock_run_safe_response(
            [{"id": 10, "path": "src/foo.py", "body": "fix", "html_url": "https://example.test"}]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert result[0].original_commit_id == ""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_merges_suppressed_comments_from_review_body(self, mock_run_safe) -> None:
        """Suppressed comments from review body are merged into the result."""
        rest_response = [{"id": 1, "path": "a.py", "body": "Fix A", "html_url": "http://x"}]
        review_body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**b.py**: Fix B\n"
            "\n"
            "</details>"
        )
        review_response = {"body": review_body}
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response(review_response),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)
        assert len(result) == 2
        assert result[0].path == "a.py"
        assert result[0].is_suppressed is False
        assert result[1].path == "b.py"
        assert result[1].is_suppressed is True

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_review_body_fetch_failure_returns_rest_only(self, mock_run_safe) -> None:
        """When review body fetch fails, only REST comments are returned."""

        class _FailResult:
            returncode = 1
            stdout = ""
            stderr = "Not Found"

        rest_response = [{"id": 1, "path": "a.py", "body": "Fix A", "html_url": "http://x"}]
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _FailResult(),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)
        assert len(result) == 1
        assert result[0].path == "a.py"
        assert result[0].is_suppressed is False

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_review_body_rate_limit_is_propagated(self, mock_run_safe, _mock_sleep) -> None:
        mock_run_safe.side_effect = [
            _mock_run_safe_response([{"id": 1, "path": "a.py", "body": "Fix", "html_url": "http://x"}]),
            ProviderRateLimitError(provider="github", is_rate_limit=True),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ProviderRateLimitError):
            provider.list_review_comments(42, 100)

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_non_rate_limit_review_body_error_returns_rest_comments(self, mock_run_safe, _mock_sleep) -> None:
        mock_run_safe.side_effect = [
            _mock_run_safe_response([{"id": 1, "path": "a.py", "body": "Fix", "html_url": "http://x"}]),
            ProviderRateLimitError(provider="github", is_rate_limit=False),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.list_review_comments(42, 100)

        assert [comment.id for comment in result] == [1]

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_no_details_block_returns_rest_only(self, mock_run_safe) -> None:
        """When review body has no <details> block, only REST comments returned."""
        rest_response = [{"id": 1, "path": "a.py", "body": "Fix", "html_url": "http://x"}]
        review_response = {"body": "Normal review without suppressed comments."}
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response(review_response),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)
        assert len(result) == 1
        assert result[0].is_suppressed is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_suppressed_only_review_returns_suppressed_entries(self, mock_run_safe) -> None:
        """When REST comments are empty but review body has suppressed, return those."""
        review_body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**src/foo.py**: Some feedback\n"
            "\n"
            "</details>"
        )
        mock_run_safe.side_effect = [
            _mock_run_safe_response([]),
            _mock_run_safe_response({"body": review_body}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)
        assert len(result) == 1
        assert result[0].path == "src/foo.py"
        assert result[0].is_suppressed is True
        assert result[0].source_review_id == 100

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_prefers_api_review_id_when_present(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 11,
                    "path": "src/foo.py",
                    "body": "fix",
                    "html_url": "https://example.test",
                    "pull_request_review_id": 999,
                }
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(10, 20)
        assert result[0].source_review_id == 999

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_deduplication_removes_suppressed_duplicate(self, mock_run_safe) -> None:
        """When the same comment exists in both REST and suppressed, suppressed is dropped."""
        rest_response = [{"id": 1, "path": "f.py", "body": "same comment", "html_url": "http://x"}]
        review_body = (
            "<details>\n"
            "<summary>Comments suppressed due to low confidence (1)</summary>\n"
            "\n"
            "**f.py**: same comment\n"
            "\n"
            "</details>"
        )
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response({"body": review_body}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)
        assert len(result) == 1
        assert result[0].is_suppressed is False

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_review_id_zero_skips_review_body_fetch(self, mock_run_safe) -> None:
        rest_response = [{"id": 1, "path": "a.py", "body": "Fix A", "html_url": "http://x"}]
        mock_run_safe.return_value = _mock_run_safe_response(rest_response)

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 0)

        assert len(result) == 1
        assert result[0].path == "a.py"
        assert result[0].is_suppressed is False
        assert mock_run_safe.call_count == 1

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_merges_new_format_suppressed_comments_from_review_body(self, mock_run_safe) -> None:
        """FR-005: the ``Suppressed comments (N)`` body reaches the merged comment list.

        Regression for swai-factory/agentic-devtools#3585 (PR #3548 review
        4840056140): the gate counted two suppressed comments while the dispatch
        comment carried none, because the block was never located.
        """
        rest_response = [{"id": 1, "path": "a.py", "body": "Fix A", "html_url": "http://x"}]
        review_body = (
            "<details>\n"
            "<summary>Suppressed comments (2)</summary>\n"
            "\n"
            "**specs/1793-subtask-property-section-mapping/spec.md:59**\n"
            "* The configuration example maps `labels` to `body:Metadata`, but the schema disallows it.\n"
            "**specs/1793-subtask-property-section-mapping/spec.md:50**\n"
            "* The spec references `project.json` but should reference the config file.\n"
            "</details>"
        )
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response({"body": review_body}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(3548, 4840056140)

        assert len(result) == 3
        assert result[0].path == "a.py"
        assert result[0].is_suppressed is False
        suppressed = [c for c in result if c.is_suppressed]
        assert [c.path for c in suppressed] == [
            "specs/1793-subtask-property-section-mapping/spec.md:59",
            "specs/1793-subtask-property-section-mapping/spec.md:50",
        ]
        assert suppressed[0].body.startswith("The configuration example maps")

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_new_format_suppressed_entry_colocated_with_distinct_body_is_kept(self, mock_run_safe) -> None:
        """A suppressed entry sharing a path with a REST comment survives dedup.

        Only an exact path-and-body duplicate is dropped, so distinct feedback on
        the same file is never silently lost.
        """
        rest_response = [{"id": 1, "path": "src/app.py", "body": "Fix the REST finding", "html_url": "http://x"}]
        review_body = (
            "<details>\n<summary>Suppressed comment (1)</summary>\n\n"
            "**`src/app.py`**: A different, suppressed finding\n\n</details>"
        )
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response({"body": review_body}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)

        assert len(result) == 2
        assert result[1].path == "src/app.py"
        assert result[1].body == "A different, suppressed finding"
        assert result[1].is_suppressed is True

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_new_format_exact_duplicate_suppressed_entry_is_dropped(self, mock_run_safe) -> None:
        """An exact path-and-body duplicate of a REST comment is deduplicated away."""
        rest_response = [{"id": 1, "path": "src/app.py", "body": "Guard against None here.", "html_url": "http://x"}]
        review_body = (
            "<details>\n<summary>Suppressed comment (1)</summary>\n\n"
            "**`src/app.py`**: Guard against None here.\n\n</details>"
        )
        mock_run_safe.side_effect = [
            _mock_run_safe_response(rest_response),
            _mock_run_safe_response({"body": review_body}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.list_review_comments(42, 100)

        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].is_suppressed is False
