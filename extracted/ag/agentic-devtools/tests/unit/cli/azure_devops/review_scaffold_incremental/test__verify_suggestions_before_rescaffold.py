"""Tests for _verify_suggestions_before_rescaffold."""

from types import SimpleNamespace

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _verify_suggestions_before_rescaffold
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewState


def test_returns_false_when_state_has_no_prior_suggestions():
    state = ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
    )

    blocked = _verify_suggestions_before_rescaffold(
        state,
        SimpleNamespace(new_files=[], modified_files=[], deleted_files=[]),
        False,
        "commit",
        "model",
        None,
        "commit",
        "https://api/threads",
        AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="project",
            repository="repo",
        ),
        "repo",
        None,
        {},
    )

    assert blocked is False
