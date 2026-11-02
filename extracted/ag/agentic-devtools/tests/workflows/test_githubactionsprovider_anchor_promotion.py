"""Integration tests for recovered CCR promotion anchor selection."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo


class TestGitHubActionsProviderAnchorPromotion:
    """Exercise provider promotion together with CCR recovery and diff anchors."""

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    def test_missing_anchor_leaves_occurrence_pending(self, mock_list_comments, mock_diff) -> None:
        mock_diff.return_value = ""
        mock_list_comments.return_value = []
        review = ReviewInfo(
            55,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n### Finding\n**File:** `src/a.py`\nBody\n</details>"
            ),
        )

        with pytest.raises(RuntimeError, match="no changed-line anchor"):
            GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_promotes_zero_width_source_path_on_exact_context_anchor(
        self, mock_create, mock_list_comments, mock_diff
    ) -> None:
        mock_diff.return_value = (
            "diff --git a/src/a.py b/src/a.py\n"
            "--- a/src/a.py\n"
            "+++ b/src/a.py\n"
            "@@ -2,2 +2,3 @@\n"
            " context\n"
            "+added\n"
            " source line\n"
        )
        mock_list_comments.return_value = []
        mock_create.return_value = ReviewCommentInfo(304, "src/a.py", "body", "url")
        review = ReviewInfo(
            80,
            "copilot-pull-request-reviewer[bot]",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/\u200ba.py`\n**Line:** 4\nDetails\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with (
            patch.object(provider, "_run_git", return_value=""),
            patch.object(provider, "_select_related_review_anchor_via_sdk") as sdk_selector,
        ):
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        created = mock_create.call_args.kwargs
        assert (created["path"], created["line"], created["side"]) == ("src/a.py", 4, "RIGHT")
        assert "Fallback anchor disclosure:" not in created["body"]
        assert "src/\u200ba.py" in created["body"]
        assert "https://github.com/owner/repo/pull/4#pullrequestreview-80" in created["body"]
        sdk_selector.assert_not_called()

    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_cross_file_fallback_consults_related_anchor_sdk(self, mock_create, mock_list_comments, mock_diff) -> None:
        mock_diff.return_value = (
            "diff --git a/src/\u200ba.py b/src/\u200ba.py\n"
            "old mode 100644\n"
            "new mode 100755\n"
            "diff --git a/src/a.py b/src/a.py\n"
            "--- a/src/a.py\n"
            "+++ b/src/a.py\n"
            "@@ -2,0 +3,1 @@\n"
            "+clean file change\n"
            "diff --git a/src/related.py b/src/related.py\n"
            "--- a/src/related.py\n"
            "+++ b/src/related.py\n"
            "@@ -4,0 +5,1 @@\n"
            "+related file change\n"
        )
        mock_list_comments.return_value = []
        mock_create.return_value = ReviewCommentInfo(305, "src/related.py", "body", "url")
        review = ReviewInfo(
            81,
            "copilot-pull-request-reviewer[bot]",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/\u200ba.py`\n**Line:** 3\nDetails\n</details>"
            ),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.object(
            provider,
            "_select_related_review_anchor_via_sdk",
            return_value=("src/related.py", 5),
        ) as sdk_selector:
            provider.promote_ccr_findings(
                pr_number=4,
                commit_sha="head",
                base_sha="base",
                reviews=[review],
            )

        sdk_selector.assert_called_once()
        assert (mock_create.call_args.kwargs["path"], mock_create.call_args.kwargs["line"]) == (
            "src/related.py",
            5,
        )
        assert "Fallback anchor disclosure:" in mock_create.call_args.kwargs["body"]

    @patch.object(
        GitHubActionsProvider,
        "_select_related_review_anchor_via_sdk",
        return_value=("src/changed.py", 1),
    )
    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_fallback_anchor_discloses_original_location_and_source_review(
        self, mock_create, mock_list_comments, mock_diff, mock_anchor_selector
    ) -> None:
        mock_diff.return_value = (
            "diff --git a/src/changed.py b/src/changed.py\n+++ b/src/changed.py\n@@ -1 +1,2 @@\n+new\n"
        )
        mock_list_comments.return_value = []
        mock_create.return_value = ReviewCommentInfo(301, "src/changed.py", "body", "url")
        review = ReviewInfo(
            id=77,
            user="Copilot",
            state="COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/original.py`\n**Line:** 12\nDetails\n</details>"
            ),
        )

        GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=[review],
        )

        posted_body = mock_create.call_args.kwargs["body"]
        assert "proper source line could not be determined for the current diff" in posted_body
        assert "`src/original.py:12`" in posted_body
        assert "https://github.com/owner/repo/pull/4#pullrequestreview-77" in posted_body
        mock_anchor_selector.assert_called_once()
        assert mock_create.call_args.kwargs["path"] == "src/changed.py"
        assert mock_create.call_args.kwargs["line"] == 1

    @patch.object(
        GitHubActionsProvider,
        "_select_related_review_anchor_via_sdk",
        return_value=("src/not-in-diff.py", 99),
    )
    @patch.object(GitHubActionsProvider, "get_commit_range_diff")
    @patch.object(GitHubActionsProvider, "list_all_review_comments")
    @patch.object(GitHubActionsProvider, "create_review_thread")
    def test_invalid_sdk_anchor_uses_first_changed_line(
        self, mock_create, mock_list_comments, mock_diff, mock_anchor_selector
    ) -> None:
        mock_diff.return_value = (
            "diff --git a/src/changed.py b/src/changed.py\n+++ b/src/changed.py\n@@ -1 +1,2 @@\n+new\n"
        )
        mock_list_comments.return_value = []
        mock_create.return_value = ReviewCommentInfo(303, "src/changed.py", "body", "url")
        review = ReviewInfo(
            79,
            "Copilot",
            "COMMENTED",
            body=(
                "<details><summary>Previously missed (1)</summary>\n"
                "### Finding\n**File:** `src/original.py`\n**Line:** 12\nDetails\n</details>"
            ),
        )

        GitHubActionsProvider(repo="owner/repo").promote_ccr_findings(
            pr_number=4,
            commit_sha="head",
            base_sha="base",
            reviews=[review],
        )

        assert mock_create.call_args.kwargs["path"] == "src/changed.py"
        assert mock_create.call_args.kwargs["line"] == 1
        assert "proper source line could not be determined for the current diff" in mock_create.call_args.kwargs["body"]
        mock_anchor_selector.assert_called_once()
