"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider


class TestBuildPrStateSnapshot:
    """Tests for count_effective_review_comments()."""

    def test_effective_review_comment_count_is_unknown_for_unrecovered_suppressed_comments(self) -> None:
        """A declared suppressed count without recovered entries is incomplete."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False, (101,))},
            body="### Comments suppressed due to low confidence (1)",
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_accepts_promoted_suppressed_coverage(self) -> None:
        """Authenticated native occurrences prove a suppressed review is complete."""
        provider = _current_review_provider(
            [
                ReviewCommentInfo(
                    id=101,
                    path="a.py",
                    body="first\n\n<!-- ccr-promoted:12:suppressed:1 -->\n\n🤖 AI PR Loop ·",
                    html_url="",
                    source_review_id=12,
                    author_login="workflow[bot]",
                ),
                ReviewCommentInfo(
                    id=102,
                    path="a.py",
                    body="second\n\n<!-- ccr-promoted:12:suppressed:2 -->\n\n🤖 AI PR Loop ·",
                    html_url="",
                    source_review_id=12,
                    author_login="workflow[bot]",
                ),
            ],
            {"thread-1": (True, (101,)), "thread-2": (True, (102,))},
            body="### Comments suppressed due to low confidence (2)",
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 0

    def test_effective_review_comment_count_accepts_explicitly_resolved_suppressed_entries(self) -> None:
        """Explicitly resolved suppressed entries need no promoted native thread."""
        provider = _current_review_provider(
            [],
            {},
            body=(
                "<details><summary>Comments suppressed due to low confidence (1)</summary>\n"
                "**a.py**: Resolved since the previous review.\n"
                "</details>"
            ),
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 0

    def test_effective_review_comment_count_skips_non_actionable_review_states(self) -> None:
        """Reviews outside repair-triggering states do not require comment retrieval."""
        provider = _current_review_provider([], {})
        provider.list_reviews.return_value[0] = ReviewInfo(
            id=12,
            user="Copilot",
            state="DISMISSED",
            commit_sha="head-sha",
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_handles_non_commented_fetch_failure(self) -> None:
        """A failed fetch for an approved review remains fail-open."""
        provider = _current_review_provider([], {})
        provider.list_reviews.return_value[0] = ReviewInfo(
            id=12,
            user="Copilot",
            state="APPROVED",
            commit_sha="head-sha",
        )
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None
