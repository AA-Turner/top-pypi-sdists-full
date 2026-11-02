"""Focused tests for prior review-thread counting."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads


class TestCountUnresolvedPriorThreads:
    """Tests for count_unresolved_prior_threads()."""

    def test_unresolved_promoted_verdict_thread_is_blocking(self) -> None:
        """An unresolved promoted root from the verdict review remains blocking."""
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(
                id=101,
                path="a.py",
                body="Recovered CCR finding\n\n<!-- ccr-promoted:10:posted:1 -->",
                html_url="",
                source_review_id=10,
            ),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="head-sha")],
            verdict_review_id=10,
        )

        assert result == (1, 1, False, False)

    def test_unresolved_promoted_root_from_older_approved_review_is_blocking(self) -> None:
        """Promoted roots remain blocking after a later clean review becomes effective."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [
                ReviewCommentInfo(
                    id=101,
                    path="a.py",
                    body="Recovered CCR finding\n\n<!-- ccr-promoted:10:posted:1 -->",
                    html_url="",
                    source_review_id=10,
                )
            ],
            [],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha"),
                ReviewInfo(id=20, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
            ],
            verdict_review_id=20,
        )

        assert result == (1, 1, False, False)
