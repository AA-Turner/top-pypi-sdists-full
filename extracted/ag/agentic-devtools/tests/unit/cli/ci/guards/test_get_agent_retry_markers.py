"""Tests for get_agent_retry_markers."""

from agentic_devtools.cli.ci.guards import get_agent_retry_markers
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_counts_distinct_markers_only_from_dispatch_identity() -> None:
    comments = [
        IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->"),
        IssueCommentInfo(2, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->"),
        IssueCommentInfo(3, "workflow-bot", "<!-- agdt:agent-retry:task-1:2 -->"),
        IssueCommentInfo(4, "human", "<!-- agdt:agent-retry:task-1:3 -->"),
        IssueCommentInfo(5, "workflow-bot", "<!-- agdt:agent-retry:malformed:x -->"),
    ]
    assert get_agent_retry_markers(comments, "workflow-bot") == {"task-1": 2}


def test_empty_dispatch_identity_trusts_no_markers() -> None:
    comments = [IssueCommentInfo(1, "workflow-bot", "<!-- agdt:agent-retry:task-1:1 -->")]
    assert get_agent_retry_markers(comments, "") == {}


def test_ignores_retry_markers_quoted_in_repair_findings() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "@copilot Please repair this finding.\n\n"
            "## Finding\n\n```text\n<!-- agdt:agent-retry:task-quoted:1 -->\n```",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "@copilot\n\n<!-- agdt:agent-retry:task-header:1 -->\nPlease resume.",
        ),
    ]

    assert get_agent_retry_markers(comments, "workflow-bot") == {"task-header": 1}
