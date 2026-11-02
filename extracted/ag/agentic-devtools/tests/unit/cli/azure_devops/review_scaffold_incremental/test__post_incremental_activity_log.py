"""Tests for _post_incremental_activity_log."""

from datetime import UTC, datetime
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _post_incremental_activity_log
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewSession, ReviewState


def test_posts_activity_reply_and_saves_comment_id():
    session = ReviewSession(sessionId="session", modelId="model", startedUtc="2026-10-20T00:00:00+00:00")
    state = ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        activityLogThreadId=5,
        sessions=[session],
    )

    with (
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental._post_activity_log_entry", return_value=8),
        patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state") as save,
    ):
        _post_incremental_activity_log(
            state,
            None,
            {},
            "https://api/threads",
            "model",
            "new",
            datetime(2026, 10, 20, tzinfo=UTC),
            0,
            0,
            0,
            0,
        )

    assert session.activityLogCommentId == 8
    save.assert_called_once_with(state)
