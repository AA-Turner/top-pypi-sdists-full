"""Tests for the retry confirmation window."""

from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.guards import is_agent_retry_confirmation_expired
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_expires_when_latest_trusted_retry_marker_reaches_confirmation_window() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->",
            created_at="2026-01-01T00:00:00Z",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-2:2 -->",
            created_at="2026-01-01T00:30:00Z",
        ),
    ]
    now = datetime(2026, 1, 1, 1, 30, tzinfo=UTC)

    assert is_agent_retry_confirmation_expired(comments, "workflow-bot", now=now) is True


def test_does_not_expire_before_confirmation_window_or_for_untrusted_markers() -> None:
    comments = [
        IssueCommentInfo(0, "workflow-bot", "An unrelated comment."),
        IssueCommentInfo(
            1,
            "other-user",
            "<!-- agdt:agent-retry:task-old:1 -->",
            created_at="2026-01-01T00:00:00Z",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-new:1 -->",
            created_at="2026-01-01T00:30:01Z",
        ),
    ]
    now = datetime(2026, 1, 1, 1, 30, tzinfo=UTC)

    assert is_agent_retry_confirmation_expired(comments, "workflow-bot", now=now) is False


def test_does_not_expire_without_a_trusted_timestamp_or_dispatch_identity() -> None:
    comments = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->"),
    ]
    now = datetime.now(UTC) + timedelta(days=2)

    assert is_agent_retry_confirmation_expired(comments, "workflow-bot", now=now) is False
    assert is_agent_retry_confirmation_expired(comments, "", now=now) is False
    assert is_agent_retry_confirmation_expired([], "workflow-bot", now=now) is False
