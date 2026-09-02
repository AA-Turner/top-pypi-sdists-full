"""Tests for get_copilot_review_status in copilot_review_status module."""

from unittest.mock import patch

from agentic_devtools.cli.github.copilot_review_status import (
    get_copilot_review_status,
)

MODULE = "agentic_devtools.cli.github.copilot_review_status"


class TestGetCopilotReviewStatus:
    """Tests for get_copilot_review_status."""

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_clean_review_full_flow(self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set):
        """Clean review produces correct dict and state keys."""
        mock_select.return_value = {
            "id": 100,
            "node_id": "PRR_abc",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "clean"
        assert result["reviewId"] == 100
        assert result["reviewNodeId"] == "PRR_abc"
        assert result["inlineCommentCount"] == 0
        assert result["suppressedCommentCount"] == 0
        assert result["actionRequired"] == "none"
        assert "pullrequestreview-100" in result["reviewUrl"]

        # Verify state keys written
        calls = {c.args[0]: c.args[1] for c in mock_set.call_args_list}
        assert calls["github.copilot_review_status"] == "clean"
        assert calls["github.copilot_review_id"] == 100
        assert calls["github.copilot_review_node_id"] == "PRR_abc"
        assert "pullrequestreview-100" in calls["github.copilot_review_url"]

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._select_latest_copilot_review", return_value=None)
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_no_review_case(self, mock_fetch, mock_select, mock_set):
        """No Copilot review returns no-review status with null fields."""
        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "no-review"
        assert result["reviewId"] is None
        assert result["reviewNodeId"] is None
        assert result["reviewUrl"] is None
        assert result["actionRequired"] == "wait"
        assert result["prNumber"] == 42
        assert result["repo"] == "owner/repo"
        assert result["commitId"] == "sha123"

        calls = {c.args[0]: c.args[1] for c in mock_set.call_args_list}
        assert calls["github.copilot_review_status"] == "no-review"
        assert calls["github.copilot_review_id"] is None

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=3)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_has_feedback_case(self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set):
        """Review with inline comments returns has-feedback."""
        mock_select.return_value = {
            "id": 200,
            "node_id": "PRR_xyz",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T10:00:00Z",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "has-feedback"
        assert result["actionRequired"] == "address-copilot-review"
        assert result["inlineCommentCount"] == 3

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_review_without_node_id(self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set):
        """Review without node_id skips suppressed count."""
        mock_select.return_value = {
            "id": 300,
            "node_id": None,
            "state": "APPROVED",
            "submitted_at": "2026-04-07T09:00:00Z",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "clean"
        mock_suppressed.assert_not_called()

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_does_not_call_sys_exit(self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set):
        """get_copilot_review_status never calls sys.exit."""
        mock_select.return_value = None

        # Should return normally, never call sys.exit
        result = get_copilot_review_status(42, "owner/repo", "sha123")
        assert isinstance(result, dict)

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_new_format_not_approved_body_yields_has_feedback(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """A new-format 'Not ready to approve' body (0 inline, 0 minimized) is NOT clean.

        Regression guard: without body parsing this COMMENTED review would be
        classified 'clean' and poll-ready would merge prematurely.
        """
        mock_select.return_value = {
            "id": 200,
            "node_id": "PRR_new",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": (
                "### 🟡 Not ready to approve\n\nPlease address the findings below.\n\n- **Comments generated:** 0 new\n"
            ),
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "has-feedback"
        assert result["actionRequired"] == "address-copilot-review"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_new_format_body_suppressed_counts_toward_feedback(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """Recovered new-format body-only suppressed comments count.

        GraphQL returns 0 minimized comments, but the body reports suppressed
        comments — the recovered body entries must surface them.
        """
        mock_select.return_value = {
            "id": 201,
            "node_id": "PRR_supp",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": (
                "### ✅ Ready to approve\n\n"
                "<details>\n<summary>Review details</summary>\n\n"
                "### Comments suppressed due to low confidence (8)\n\n"
                "**a.py:1**\n* finding\n\n"
                "- **Files reviewed:** 2/2 changed files\n"
                "</details>"
            ),
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["suppressedCommentCount"] == 1
        assert result["status"] == "has-feedback"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=5)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_graphql_suppressed_preserved_when_higher_than_body(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """The merge keeps the larger of GraphQL-minimized vs body-reported counts."""
        mock_select.return_value = {
            "id": 202,
            "node_id": "PRR_legacy",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": "Copilot generated no comments.",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["suppressedCommentCount"] == 5
        assert result["status"] == "has-feedback"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_body_entries_without_numeric_count_still_surface_feedback(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """Recovered suppressed entries count as feedback even without ``(N)``."""
        mock_select.return_value = {
            "id": 203,
            "node_id": "PRR_entries",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": "<details>\n<summary>Suppressed comments</summary>\n\n**a.py**: A finding\n\n</details>",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["suppressedCommentCount"] == 1
        assert result["status"] == "has-feedback"
        assert result["actionRequired"] == "address-copilot-review"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_unparsed_suppression_signal_requires_investigation(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """Unparsed suppression signals must not be classified as clean."""
        mock_select.return_value = {
            "id": 204,
            "node_id": "PRR_unparsed",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": "Suppressed comments (2) in wrapper.\n\n**a.py:1**\n",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "unknown-state"
        assert result["actionRequired"] == "investigate"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_declared_suppressed_count_without_entries_is_investigate_not_feedback(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """A declared suppressed count without entries is treated as unrecovered."""
        mock_select.return_value = {
            "id": 205,
            "node_id": "PRR_declared_only",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": "<details>\n<summary>Suppressed comments (1)</summary>\n\n</details>",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["suppressedCommentCount"] == 0
        assert result["status"] == "unknown-state"
        assert result["actionRequired"] == "investigate"

    @patch(f"{MODULE}.set_value")
    @patch(f"{MODULE}._count_suppressed_comments", return_value=0)
    @patch(f"{MODULE}._count_inline_comments", return_value=0)
    @patch(f"{MODULE}._select_latest_copilot_review")
    @patch(f"{MODULE}._fetch_reviews_for_pr", return_value=[])
    def test_unparsed_suppression_overrides_not_approved_verdict_without_feedback(
        self, mock_fetch, mock_select, mock_inline, mock_suppressed, mock_set
    ):
        """Verdict-only feedback is secondary to unrecovered suppression signals."""
        mock_select.return_value = {
            "id": 206,
            "node_id": "PRR_not_ready_unparsed",
            "state": "COMMENTED",
            "submitted_at": "2026-04-07T09:00:00Z",
            "body": "### 🟡 Not ready to approve\n\nSuppressed comments (2) in wrapper.\n\n**a.py:1**\n",
        }

        result = get_copilot_review_status(42, "owner/repo", "sha123")

        assert result["status"] == "unknown-state"
        assert result["actionRequired"] == "investigate"
