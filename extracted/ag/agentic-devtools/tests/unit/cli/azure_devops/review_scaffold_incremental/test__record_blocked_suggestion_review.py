"""Tests for _record_blocked_suggestion_review."""

from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _record_blocked_suggestion_review
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewState


def _state():
    return ReviewState(
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


def test_records_blocked_review_without_activity_thread():
    state = _state()
    result = SimpleNamespace(suggestion=SimpleNamespace(threadId=7))
    now = datetime(2026, 10, 20, tzinfo=UTC)

    with (
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental._post_reply"),
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.upsert_consolidated_comment"),
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state") as save,
    ):
        _record_blocked_suggestion_review(
            state,
            [result],
            AzureDevOpsConfig(
                organization="https://dev.azure.com/org",
                project="project",
                repository="repo",
            ),
            "repo",
            "model",
            "new",
            now,
            "new",
            "https://api/threads",
            None,
            {},
        )

    assert state.commitHash == "new"
    assert state.sessions[0].status == "failed"
    save.assert_called_once_with(state)
