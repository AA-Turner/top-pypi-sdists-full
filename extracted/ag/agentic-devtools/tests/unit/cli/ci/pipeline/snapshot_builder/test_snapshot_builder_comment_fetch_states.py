"""Tests for review-comment collection across review states."""

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _provider_for_review


def test_does_not_fetch_comments_for_non_actionable_review_state() -> None:
    provider = _provider_for_review(ReviewInfo(id=1, user="Copilot", state="DISMISSED", commit_sha="head-sha"))

    snapshot = build_pr_state_snapshot(provider, 1)

    assert snapshot.copilot_review_inline_count == 0


def test_comment_fetch_failure_for_non_commented_review_is_not_counted() -> None:
    provider = _provider_for_review(ReviewInfo(id=1, user="Copilot", state="CHANGES_REQUESTED", commit_sha="head-sha"))
    provider.list_review_comments.side_effect = RuntimeError("comments unavailable")

    snapshot = build_pr_state_snapshot(provider, 1)

    assert snapshot.copilot_review_inline_count == 0
    assert snapshot.effective_review_comment_count is None
