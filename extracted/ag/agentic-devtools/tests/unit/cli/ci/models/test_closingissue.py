"""Tests for ClosingIssue."""

from agentic_devtools.cli.ci.models import ClosingIssue


def test_closing_issue_preserves_task_context() -> None:
    issue = ClosingIssue(number=4257, title="Retry agent", body="Refined specification")
    assert (issue.number, issue.title, issue.body) == (4257, "Retry agent", "Refined specification")
