"""Integration coverage for promotion when an unchanged literal source path exists."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo


def test_promotion_discloses_fallback_and_asks_for_a_related_anchor() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    review = ReviewInfo(
        id=55,
        user="Copilot",
        state="COMMENTED",
        body=(
            "<details><summary>Previously missed (1)</summary>\n"
            "### Finding\n**File:** `src/\u200ba.py`\n**Line:** 3\nDetails\n</details>"
        ),
    )
    diff = "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -2,0 +3,1 @@\n+clean file change\n"
    with (
        patch.object(provider, "get_commit_range_diff", return_value=diff),
        patch.object(provider, "list_all_review_comments", return_value=[]),
        patch.object(
            provider, "create_review_thread", return_value=ReviewCommentInfo(111, "src/a.py", "body", "url")
        ) as create,
        patch.object(provider, "_run_git", side_effect=["", "src/\u200ba.py\0", "", "src/\u200ba.py\0"]) as run_git,
        patch.object(provider, "_select_related_review_anchor_via_sdk", return_value=("src/a.py", 3)) as sdk_select,
    ):
        provider.promote_ccr_findings(
            pr_number=4,
            commit_sha="head-sha",
            base_sha="base-sha",
            reviews=[review],
        )

    assert run_git.call_count == 4
    sdk_select.assert_called_once()
    assert create.call_args.kwargs["path"] == "src/a.py"
    assert create.call_args.kwargs["line"] == 3
    assert "Fallback anchor disclosure:" in create.call_args.kwargs["body"]
