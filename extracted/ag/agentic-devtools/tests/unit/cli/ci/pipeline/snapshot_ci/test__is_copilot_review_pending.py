"""Tests for pending Copilot reviewer detection."""

from agentic_devtools.cli.ci.pipeline.snapshot_ci import _is_copilot_review_pending


def test_returns_false_when_no_copilot_reviewer_is_pending() -> None:
    assert _is_copilot_review_pending([]) is False
    assert _is_copilot_review_pending(["octocat"]) is False


def test_returns_true_when_copilot_reviewer_is_pending() -> None:
    assert _is_copilot_review_pending(["octocat", "Copilot"]) is True
