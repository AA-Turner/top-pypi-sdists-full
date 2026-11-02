"""Tests for human change-requested review detection."""

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_reviews import has_non_copilot_changes_requested_on_head


def test_returns_false_without_a_human_change_request() -> None:
    assert has_non_copilot_changes_requested_on_head([], "head") is False
    assert (
        has_non_copilot_changes_requested_on_head(
            [ReviewInfo(id=1, user="Copilot", state="CHANGES_REQUESTED", commit_sha="head")],
            "head",
        )
        is False
    )


def test_returns_true_for_a_human_change_request_on_head() -> None:
    review = ReviewInfo(id=1, user="octocat", state="CHANGES_REQUESTED", commit_sha="head")

    assert has_non_copilot_changes_requested_on_head([review], "head") is True
