"""Tests for cancelling a verified Actions workflow run."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_posts_to_the_supported_run_cancel_endpoint() -> None:
    """Requests cancellation through the GitHub Actions REST endpoint."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}") as api:
        provider.cancel_workflow_run(700)

    api.assert_called_once_with("/repos/owner/repo/actions/runs/700/cancel", method="POST")


@pytest.mark.parametrize("run_id", [0, -1, True])
def test_rejects_invalid_run_ids(run_id: int) -> None:
    """Rejects non-positive and boolean run IDs before making a provider call."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api") as api,
        pytest.raises(ValueError, match="run_id must be a positive integer"),
    ):
        provider.cancel_workflow_run(run_id)
    api.assert_not_called()
