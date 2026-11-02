"""Tests for _update_stale_activity_log_comments."""

from unittest.mock import Mock

from agentic_devtools.cli.azure_devops.review_scaffold_session_state import _update_stale_activity_log_comments
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewSession, ReviewState


def test_updates_fallback_comment_id(monkeypatch):
    session = ReviewSession(
        "session",
        "model",
        "2020-01-01T00:00:00+00:00",
        activityLogCommentId=8,
    )
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
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.review_scaffold_session_state._update_activity_log_comment_status",
        lambda *args: 9,
    )

    _update_stale_activity_log_comments(state, [session], None, {}, "https://api/threads", "commit")

    assert session.activityLogCommentId == 9


def test_skips_missing_comment_and_reports_update_errors(monkeypatch, capsys):
    missing_comment = ReviewSession("missing", "model", "2020-01-01T00:00:00+00:00")
    failed_update = ReviewSession(
        "failed",
        "model",
        "2020-01-01T00:00:00+00:00",
        activityLogCommentId=10,
    )
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
        sessions=[missing_comment, failed_update],
    )
    updater = Mock(side_effect=OSError("offline"))
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.review_scaffold_session_state._update_activity_log_comment_status",
        updater,
    )

    _update_stale_activity_log_comments(state, state.sessions, None, {}, "https://api/threads", "commit")

    updater.assert_called_once()
    assert "offline" in capsys.readouterr().err
