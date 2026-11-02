"""Tests for get_agent_retry_marker_aliases."""

from agentic_devtools.cli.ci.guards import get_agent_retry_marker_aliases
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_reads_aliases_only_from_trusted_retry_comments() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
        ),
        IssueCommentInfo(
            2,
            "workflow-bot",
            "<!-- agdt:agent-retry-alias:43 -->",
        ),
        IssueCommentInfo(
            3,
            "human",
            "<!-- agdt:agent-retry:task-2:1 -->\n<!-- agdt:agent-retry-alias:44 -->",
        ),
        IssueCommentInfo(4, "workflow-bot", "<!-- agdt:agent-retry:task-3:1 -->"),
    ]

    assert get_agent_retry_marker_aliases(comments, "workflow-bot") == {"42"}


def test_empty_dispatch_identity_trusts_no_aliases() -> None:
    comments = [
        IssueCommentInfo(
            1,
            "workflow-bot",
            "<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-alias:42 -->",
        )
    ]

    assert get_agent_retry_marker_aliases(comments, "") == set()
