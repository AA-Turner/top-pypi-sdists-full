"""Tests for _update_incremental_metadata."""

from datetime import UTC, datetime
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _update_incremental_metadata
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewState


def test_updates_commit_metadata_and_renders_comment():
    state = ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        commitHash="old",
    )
    config = AzureDevOpsConfig(organization="https://dev.azure.com/org", project="project", repository="repo")

    with (
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental._archive_commit_thread") as archive,
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.upsert_consolidated_comment") as upsert,
    ):
        _update_incremental_metadata(
            state,
            "old",
            "new",
            "model",
            2,
            True,
            datetime(2026, 10, 20, tzinfo=UTC),
            config,
            "repo",
            None,
            {},
        )

    archive.assert_called_once()
    upsert.assert_called_once()
    assert (state.commitHash, state.latestIterationId, state.rebaseConflicts) == ("new", 2, True)
