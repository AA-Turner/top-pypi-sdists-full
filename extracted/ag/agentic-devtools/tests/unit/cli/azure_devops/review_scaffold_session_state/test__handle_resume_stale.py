"""Tests for _handle_resume_stale."""

from datetime import UTC, datetime
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_scaffold_session_state import _handle_resume_stale
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewSession, ReviewState


def _state():
    session = ReviewSession(
        sessionId="old",
        modelId="model",
        startedUtc="2020-01-01T00:00:00+00:00",
        status="in_progress",
        commitHash="commit",
    )
    return ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        sessions=[session],
        commitHash="commit",
    )


def test_dry_run_leaves_stale_session_unchanged():
    state = _state()

    result = _handle_resume_stale(
        state,
        "model",
        "commit",
        1,
        True,
        None,
        {},
        "https://api/threads",
        datetime(2026, 10, 20, tzinfo=UTC),
    )

    assert result is state
    assert state.sessions[0].status == "in_progress"


def test_marks_session_failed_and_starts_resume():
    state = _state()
    with patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"):
        result = _handle_resume_stale(
            state,
            "model",
            "commit",
            1,
            False,
            None,
            {},
            "https://api/threads",
            datetime(2026, 10, 20, tzinfo=UTC),
        )

    assert result is state
    assert state.sessions[0].status == "failed"
    assert len(state.sessions) == 2


def test_posts_resume_activity_log_when_thread_exists():
    state = _state()
    state.activityLogThreadId = 5
    state.sessions[0].activityLogCommentId = 8
    with (
        patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"),
        patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_session_state._update_activity_log_comment_status",
            return_value=None,
        ),
        patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_session_state._post_activity_log_entry",
            return_value=9,
        ) as post,
    ):
        result = _handle_resume_stale(
            state,
            "model",
            "commit",
            1,
            False,
            None,
            {},
            "https://api/threads",
            datetime(2026, 10, 20, tzinfo=UTC),
        )

    assert result is state
    assert state.sessions[-1].activityLogCommentId == 9
    post.assert_called_once()


def test_reports_failed_resume_activity_log_post(capsys):
    state = _state()
    state.activityLogThreadId = 5
    with (
        patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"),
        patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_session_state._post_activity_log_entry",
            side_effect=OSError("offline"),
        ),
    ):
        _handle_resume_stale(
            state,
            "model",
            "commit",
            1,
            False,
            None,
            {},
            "https://api/threads",
            datetime(2026, 10, 20, tzinfo=UTC),
        )

    assert "offline" in capsys.readouterr().err
