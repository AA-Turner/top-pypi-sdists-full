"""Tests for _get_approval_state."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_approval_state


def test_matches_human_approver_to_effective_head_review() -> None:
    """Only a human approval on the current HEAD is attributed to the approver."""
    provider = MagicMock()
    provider.get_approver_login.return_value = "review-bot"
    reviews = [
        ReviewInfo(id=1, user="review-bot", state="APPROVED", commit_sha="head"),
        ReviewInfo(id=2, user="review-bot", state="CHANGES_REQUESTED", commit_sha="old"),
    ]

    result = _get_approval_state(provider, 7, reviews, "head")

    assert result == (True, "review-bot", True)


def test_unavailable_approver_login_does_not_claim_approver_approval() -> None:
    """A failed best-effort login lookup leaves the approver-specific flag false."""
    provider = MagicMock()
    provider.get_approver_login.side_effect = RuntimeError("lookup failed")
    reviews = [ReviewInfo(id=1, user="review-bot", state="APPROVED", commit_sha="head")]

    assert _get_approval_state(provider, 7, reviews, "head") == (True, "", False)
