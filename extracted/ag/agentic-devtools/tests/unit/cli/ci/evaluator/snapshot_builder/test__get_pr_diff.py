"""Tests for _get_pr_diff()."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.evaluator.snapshot_builder import _get_pr_diff


def test_prefers_range_diff_after_head_change() -> None:
    """Uses the review-to-current range diff when the head changed."""
    provider = MagicMock()
    provider.get_commit_range_diff.return_value = "range"

    assert _get_pr_diff(provider, 42, "review", "current", True) == "range"
    provider.get_commit_range_diff.assert_called_once_with("review", "current")
    provider.get_pr_diff.assert_not_called()


def test_uses_pr_diff_when_no_post_review_range_is_available() -> None:
    """Uses the full PR diff when there is no changed review range."""
    provider = MagicMock()
    provider.get_pr_diff.return_value = "full"

    assert _get_pr_diff(provider, 42, "", "current", False) == "full"
    provider.get_pr_diff.assert_called_once_with(42)


def test_returns_empty_diff_when_provider_does_not_support_diff() -> None:
    """Treats unsupported and failed diff fetches as unavailable."""
    provider = MagicMock()
    provider.get_pr_diff.side_effect = NotImplementedError("unsupported")

    assert _get_pr_diff(provider, 42, "", "current", False) == ""
