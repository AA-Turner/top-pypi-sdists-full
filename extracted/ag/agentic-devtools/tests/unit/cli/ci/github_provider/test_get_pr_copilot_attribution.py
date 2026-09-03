"""Tests for Copilot activity attribution."""

from __future__ import annotations

from unittest.mock import ANY, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import IssueCommentInfo, PRMetadata, ReviewInfo
from agentic_devtools.cli.ci.reconciliation import config


def test_get_pr_copilot_attribution_identifies_reviews_and_pushes() -> None:
    """Reports Copilot-authored reviews and commits independently."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(
            provider,
            "list_reviews",
            return_value=[
                ReviewInfo(
                    id=1,
                    user="copilot-swe-agent[bot]",
                    state="COMMENTED",
                    body="",
                    commit_sha="sha",
                    submitted_at="",
                )
            ],
        ),
        patch.object(
            provider,
            "list_issue_comments",
            return_value=[IssueCommentInfo(id=2, author="github-actions", body="", created_at="")],
        ),
        patch.object(
            provider,
            "get_pr_metadata",
            return_value=PRMetadata(
                number=42,
                title="",
                head_branch="feature",
                head_sha="head-sha",
                base_branch="main",
            ),
        ),
        patch.object(provider, "get_commit_author_login", return_value="copilot-swe-agent[bot]") as get_author,
    ):
        attribution = provider.get_pr_copilot_attribution(42)

    assert attribution["review"] is True
    assert attribution["push"] is True
    get_author.assert_called_once_with("head-sha")


def test_get_pr_copilot_attribution_returns_false_when_no_copilot_activity() -> None:
    """Returns false attribution when review, comment, and commit actors are ordinary users."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "list_reviews", return_value=[]),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(
            provider,
            "get_pr_metadata",
            return_value=PRMetadata(
                number=42,
                title="",
                head_branch="feature",
                head_sha="",
                base_branch="main",
            ),
        ),
        patch.object(provider, "get_commit_author_login") as get_author,
    ):
        attribution = provider.get_pr_copilot_attribution(42)

    assert attribution["review"] is False
    assert attribution["push"] is False
    get_author.assert_not_called()


def test_get_pr_copilot_attribution_scans_commits_since_watermark() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")

    def _list_commits_with_watermark_found(*_args, **kwargs):
        scan_state = kwargs.get("scan_state")
        if isinstance(scan_state, dict):
            scan_state["watermark_found"] = True
            scan_state["scan_complete"] = True
        return [
            {"sha": "copilot-sha", "author": {"login": "copilot-swe-agent[bot]"}},
        ]

    with (
        patch.object(provider, "list_reviews", return_value=[]),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(
            provider,
            "get_pr_metadata",
            return_value=PRMetadata(
                number=42,
                title="",
                head_branch="feature",
                head_sha="head-sha",
                base_branch="main",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.push_attribution.list_commits_since_watermark",
            side_effect=_list_commits_with_watermark_found,
        ) as list_commits,
    ):
        attribution = provider.get_pr_copilot_attribution(42, observation_watermark="watermark")

    assert attribution["review"] is False
    assert attribution["push"] is True
    list_commits.assert_called_once_with(
        "owner/repo",
        "watermark",
        pr_number=42,
        per_page=100,
        max_pages=config.MAX_PAGINATION_PAGES_PER_RUN,
        scan_state=ANY,
    )


def test_get_pr_copilot_attribution_treats_missing_watermark_as_push() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "list_reviews", return_value=[]),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(
            provider,
            "get_pr_metadata",
            return_value=PRMetadata(
                number=42,
                title="",
                head_branch="feature",
                head_sha="head-sha",
                base_branch="main",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.push_attribution.list_commits_since_watermark",
            return_value=[{"sha": f"sha-{index}", "author": {"login": "ordinary-user"}} for index in range(100)],
        ),
        patch("agentic_devtools.cli.ci.reconciliation.config.MAX_PAGINATION_PAGES_PER_RUN", 1),
    ):
        attribution = provider.get_pr_copilot_attribution(42, observation_watermark="missing")

    assert attribution["push"] is True


def test_get_pr_copilot_attribution_rejects_malformed_commit_history() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch.object(provider, "list_reviews", return_value=[]),
        patch.object(provider, "list_issue_comments", return_value=[]),
        patch.object(
            provider,
            "get_pr_metadata",
            return_value=PRMetadata(
                number=42,
                title="",
                head_branch="feature",
                head_sha="head-sha",
                base_branch="main",
            ),
        ),
        patch(
            "agentic_devtools.cli.ci.push_attribution.list_commits_since_watermark",
            side_effect=ValueError("GitHub commits response must be a list"),
        ),
    ):
        with pytest.raises(ValueError, match="GitHub commits response"):
            provider.get_pr_copilot_attribution(42, observation_watermark="watermark")


def test_get_pr_copilot_attribution_rejects_invalid_pr_number() -> None:
    """Rejects non-positive pull-request numbers before making API calls."""
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(ValueError, match="pr_number"):
        provider.get_pr_copilot_attribution(0)

    with pytest.raises(ValueError, match="pr_number"):
        provider.get_pr_copilot_attribution(True)  # type: ignore[arg-type]
