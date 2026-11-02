"""Tests for is_copilot_or_synthetic_review in gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, is_copilot_or_synthetic_review

HEAD_SHA = "a" * 40


def _review(
    review_id: int,
    user: str = "copilot-pull-request-reviewer[bot]",
    state: str = "COMMENTED",
    body: str = "Copilot generated no comments.",
    commit_sha: str = HEAD_SHA,
    submitted_at: str = "2024-01-01T10:00:00Z",
) -> ReviewInfo:
    return ReviewInfo(
        id=review_id,
        user=user,
        state=state,
        body=body,
        commit_sha=commit_sha,
        submitted_at=submitted_at,
    )


class TestIsCopilotOrSyntheticReview:
    """Tests for is_copilot_or_synthetic_review."""

    def test_accepts_trusted_synthetic(self) -> None:
        """Trusted synthetic reviews are accepted."""
        review = _review(1, user="AMARSNIK_swica", body=f"{SYNTHETIC_MARKER}\nsynthetic")
        assert is_copilot_or_synthetic_review(review) is True

    def test_accepts_casefolded_synthetic_user(self) -> None:
        """Trusted synthetic users are matched case-insensitively."""
        review = _review(1, user="amarsnik_swica", body=f"{SYNTHETIC_MARKER}\nsynthetic")
        assert is_copilot_or_synthetic_review(review) is True

    def test_non_string_user_returns_false(self) -> None:
        """Non-string review users are not treated as synthetic."""
        review = _review(1)
        review = ReviewInfo(
            id=review.id,
            user=None,  # type: ignore[arg-type]
            state=review.state,
            body=review.body,
            commit_sha=review.commit_sha,
            submitted_at=review.submitted_at,
        )
        assert is_copilot_or_synthetic_review(review) is False
