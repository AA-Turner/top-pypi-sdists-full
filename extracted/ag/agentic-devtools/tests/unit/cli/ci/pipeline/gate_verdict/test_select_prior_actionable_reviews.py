"""Tests for select_prior_actionable_reviews in gate_verdict module."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, select_prior_actionable_reviews

HEAD_SHA = "a" * 40
PRIOR_SHA = "b" * 40
VERDICT_REVIEW_ID = 999


def _review(
    review_id: int,
    user: str = "copilot-pull-request-reviewer[bot]",
    state: str = "CHANGES_REQUESTED",
    body: str = "Please fix.",
    commit_sha: str = PRIOR_SHA,
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


class TestSelectPriorActionableReviews:
    """Tests for select_prior_actionable_reviews."""

    def test_selects_prior_changes_requested_review(self) -> None:
        """A CHANGES_REQUESTED Copilot review not owned by the verdict is selected."""
        review = _review(1)
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == [review]

    def test_selects_prior_commented_review(self) -> None:
        """A COMMENTED Copilot review not owned by the verdict is selected."""
        review = _review(1, state="COMMENTED")
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == [review]

    def test_selects_trusted_synthetic_review(self) -> None:
        """A trusted synthetic review not owned by the verdict is selected."""
        review = _review(1, user="AMARSNIK_swica", body=f"{SYNTHETIC_MARKER}\nsynthetic")
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == [review]

    def test_excludes_non_copilot_review(self) -> None:
        """Reviews from other users are excluded."""
        review = _review(1, user="human-reviewer")
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == []

    def test_excludes_review_owned_by_verdict(self) -> None:
        """The review whose id matches the verdict's review_id is excluded."""
        review = _review(1)
        assert select_prior_actionable_reviews([review], 1) == []

    def test_head_commit_review_is_selected_when_not_owned_by_verdict(self) -> None:
        """A HEAD-commit review is selected when its id differs from the verdict's.

        Provenance is scoped to the verdict's review_id, not to HEAD's commit SHA,
        so a review on HEAD that the verdict does *not* own still counts as prior.
        """
        review = _review(1, commit_sha=HEAD_SHA)
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == [review]

    def test_selects_review_without_commit_sha_when_not_owned_by_verdict(self) -> None:
        """Reviews with an empty commit SHA are selected — commit SHA no longer gates selection."""
        review = _review(1, commit_sha="")
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == [review]

    def test_excludes_non_actionable_state(self) -> None:
        """Reviews in a non-actionable state (e.g. APPROVED) are excluded."""
        review = _review(1, state="APPROVED")
        assert select_prior_actionable_reviews([review], VERDICT_REVIEW_ID) == []

    def test_returns_empty_list_for_no_reviews(self) -> None:
        """An empty review list yields an empty selection."""
        assert select_prior_actionable_reviews([], VERDICT_REVIEW_ID) == []

    def test_preserves_input_order(self) -> None:
        """Selected reviews keep their input order."""
        first = _review(9)
        second = _review(2, state="COMMENTED")
        excluded = _review(3)
        assert select_prior_actionable_reviews([first, excluded, second], 3) == [first, second]

    def test_zero_verdict_review_id_selects_all_actionable_reviews(self) -> None:
        """review_id <= 0 (no verdict, or a failed-closed verdict) degenerates to count-all."""
        first = _review(1)
        second = _review(2, state="COMMENTED", commit_sha=HEAD_SHA)
        assert select_prior_actionable_reviews([first, second], 0) == [first, second]

    def test_negative_verdict_review_id_selects_all_actionable_reviews(self) -> None:
        """A negative review_id also fails closed to count-all."""
        review = _review(1)
        assert select_prior_actionable_reviews([review], -1) == [review]

    def test_head_move_alone_does_not_change_selection(self) -> None:
        """A HEAD move that leaves reviews and the verdict untouched must not change the count.

        This is the core provenance guarantee: selection depends only on the
        verdict's review_id, never on any commit SHA, so squash/takeover (which
        mint a new HEAD SHA without touching review state) cannot inflate it.
        """
        review = _review(1, commit_sha=PRIOR_SHA)
        before = select_prior_actionable_reviews([review], VERDICT_REVIEW_ID)
        # Simulate a HEAD move: the review's commit_sha is unaffected by it, and
        # the selector never even looks at a head_sha argument any more.
        after = select_prior_actionable_reviews([review], VERDICT_REVIEW_ID)
        assert before == after == [review]
