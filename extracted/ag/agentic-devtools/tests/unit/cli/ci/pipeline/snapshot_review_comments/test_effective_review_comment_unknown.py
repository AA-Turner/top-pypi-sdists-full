"""Tests for build_pr_state_snapshot."""

from typing import cast

from agentic_devtools.cli.ci.models import (
    ReviewCommentInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider


class TestBuildPrStateSnapshot:
    """Tests for count_effective_review_comments()."""

    def test_effective_review_comment_count_is_unknown_for_unmapped_comment(self) -> None:
        """A positive comment missing from thread state keeps dispatch fail-open."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False, (102,))},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_for_non_integer_comment_id(self) -> None:
        """Malformed comment identifiers keep the effective inventory unknown."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=cast(int, "bad"), path="a.py", body="fix", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_counts_synthetic_entries(self) -> None:
        """Recovered synthetic entries count as effective review work."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=-1, path="a.py", body="suppressed", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 1

    def test_effective_review_comment_count_is_unknown_for_zero_comment_id(self) -> None:
        """A zero comment identifier is malformed and cannot prove no work remains."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=0, path="a.py", body="fix", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None
