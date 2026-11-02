"""Tests for correlating session failures with trusted retry markers."""

from agentic_devtools.cli.ci.guards import classify_agent_retry_failure
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_classifies_matching_failure_identity_as_handled() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->")]

    assert classify_agent_retry_failure({"task-1"}, None, comments, "workflow-bot") == "handled"


def test_typed_task_identity_matches_its_marker() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->")]

    assert (
        classify_agent_retry_failure(
            {"task-1"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-1",
        )
        == "handled"
    )


def test_typed_timeline_identity_matches_its_explicit_alias() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-old:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "42"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-new",
            failure_event_id=42,
        )
        == "handled"
    )


def test_keeps_ambiguous_numeric_primary_identity_uncorrelated_without_timestamps() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:123:1 -->")]

    assert (
        classify_agent_retry_failure(
            {"123"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="123",
        )
        == "uncorrelated"
    )


def test_classifies_older_failure_from_a_different_source_as_handled() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"42"},
            "2026-01-01T00:01:00Z",
            comments,
            "workflow-bot",
        )
        == "handled"
    )


def test_classifies_verified_newer_failure_from_a_different_source_as_new() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"42"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
        )
        == "new"
    )


def test_keeps_unverifiable_source_switch_fail_closed() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->")]

    assert classify_agent_retry_failure({"42"}, None, comments, "workflow-bot") == "uncorrelated"


def test_ignores_retry_markers_from_an_untrusted_author() -> None:
    comments = [IssueCommentInfo(1, "other-user", "<!-- agdt:agent-retry:task-1:1 -->")]

    assert classify_agent_retry_failure({"42"}, None, comments, "workflow-bot") == "new"


def test_classifies_an_unmatched_task_failure_as_new() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-old:1 -->")]

    assert classify_agent_retry_failure({"task-new"}, None, comments, "workflow-bot") == "new"


def test_ignores_untrusted_comments_when_finding_latest_retry_timestamp() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->",
            created_at="2026-01-01T00:02:00Z",
        ),
        IssueCommentInfo(
            2,
            "other-user",
            "<!-- agdt:agent-retry:task-2:1 -->",
            created_at="2026-01-01T00:04:00Z",
        ),
    ]

    assert (
        classify_agent_retry_failure(
            {"42"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
        )
        == "new"
    )


def test_keeps_source_switch_unresolved_without_retry_timestamp() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->")]

    assert (
        classify_agent_retry_failure(
            {"42"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
        )
        == "uncorrelated"
    )


def test_classifies_newer_task_with_correlated_event_as_new_by_timestamp() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:42:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "43"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
        )
        == "new"
    )


def test_classifies_older_task_with_correlated_event_as_handled_by_timestamp() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:43:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-old", "42"},
            "2026-01-01T00:01:00Z",
            comments,
            "workflow-bot",
        )
        == "handled"
    )


def test_classifies_distinct_failure_against_task_marker_as_new() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-old:1 -->",
            created_at="2026-01-01T00:05:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "43"},
            "2026-01-01T00:04:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-new",
            failure_event_id=43,
        )
        == "new"
    )


def test_numeric_task_marker_does_not_match_a_later_correlated_event_id() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:123:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "123"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-new",
            failure_event_id=123,
        )
        == "new"
    )


def test_correlated_timeline_marker_deduplicates_same_task_failure() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:123:1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "123"},
            "2026-01-01T00:01:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-new",
            failure_event_id=123,
        )
        == "handled"
    )


def test_classifies_a_later_failure_in_the_same_task_as_new() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-1", "43"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-1",
            failure_event_id=43,
        )
        == "new"
    )


def test_keeps_same_task_failure_without_a_correlated_event_ambiguous() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-1", "43"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-1",
            failure_event_id=43,
        )
        == "uncorrelated"
    )


def test_distinct_timeline_failure_at_retry_timestamp_is_new() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-old:1 -->\n"
            "<!-- agdt:agent-retry-alias:42 -->\n"
            "<!-- agdt:agent-retry-identity:event:42 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-new", "43"},
            "2026-01-01T00:02:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-new",
            failure_event_id=43,
        )
        == "new"
    )


def test_classifies_matching_source_qualified_event_identity_as_handled() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-identity:event:42 -->",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-1", "42"},
            None,
            comments,
            "workflow-bot",
            failure_event_id=42,
        )
        == "handled"
    )


def test_ignores_non_numeric_source_qualified_event_identity() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-identity:event:unknown -->",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-2", "42"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-2",
            failure_event_id=42,
        )
        == "new"
    )


def test_classifies_source_qualified_task_identity() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-identity:task:task-1 -->",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-1"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-1",
        )
        == "handled"
    )
    assert (
        classify_agent_retry_failure(
            {"task-2"},
            None,
            comments,
            "workflow-bot",
            failure_task_id="task-2",
        )
        == "new"
    )


def test_correlates_later_event_after_matching_source_qualified_task_marker() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-identity:task:task-1 -->",
            created_at="2026-01-01T00:02:00Z",
        )
    ]

    assert (
        classify_agent_retry_failure(
            {"task-1", "43"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-1",
            failure_event_id=43,
        )
        == "new"
    )


def test_new_event_is_handled_when_a_later_cross_source_retry_marker_exists() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n"
            "<!-- agdt:agent-retry-identity:event:42 -->\n"
            "<!-- agdt:agent-retry-alias:42 -->",
            created_at="2026-01-01T00:02:00Z",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-2:2 -->\n<!-- agdt:agent-retry-identity:task:task-2 -->",
            created_at="2026-01-01T00:04:00Z",
        ),
        IssueCommentInfo(
            3,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-old:1 -->\n\nCopied retry context.",
            created_at="2026-01-01T00:01:00Z",
        ),
        IssueCommentInfo(4, "workflow-bot", "An unrelated comment."),
    ]

    assert (
        classify_agent_retry_failure(
            {"43"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
            failure_event_id=43,
        )
        == "handled"
    )


def test_new_event_is_handled_when_matching_task_retry_marker_is_later() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n"
            "<!-- agdt:agent-retry-identity:task:task-1 -->\n"
            "<!-- agdt:agent-retry-identity:event:42 -->",
            created_at="2026-01-01T00:02:00Z",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-2:2 -->\n<!-- agdt:agent-retry-identity:task:task-2 -->",
            created_at="2026-01-01T00:04:00Z",
        ),
    ]

    assert (
        classify_agent_retry_failure(
            {"task-2", "43"},
            "2026-01-01T00:03:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-2",
            failure_event_id=43,
        )
        == "handled"
    )


def test_later_failure_in_matching_task_remains_new() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n"
            "<!-- agdt:agent-retry-identity:task:task-1 -->\n"
            "<!-- agdt:agent-retry-identity:event:42 -->",
            created_at="2026-01-01T00:02:00Z",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-2:2 -->\n<!-- agdt:agent-retry-identity:task:task-2 -->",
            created_at="2026-01-01T00:04:00Z",
        ),
    ]

    assert (
        classify_agent_retry_failure(
            {"task-2", "43"},
            "2026-01-01T00:05:00Z",
            comments,
            "workflow-bot",
            failure_task_id="task-2",
            failure_event_id=43,
        )
        == "new"
    )
