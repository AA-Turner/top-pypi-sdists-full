"""Only the dispatch credential can supply authentic accounting evidence."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.repair_accounting import authentic_repair_comments


def test_authentic_repair_comments_filters_quotes_and_spoofs() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "Dispatch-Bot"
    genuine = IssueCommentInfo(1, "dispatch-bot", "marker")
    provider.list_issue_comments.return_value = [genuine, IssueCommentInfo(2, "stranger", "marker")]
    assert authentic_repair_comments(provider, 42) == [genuine]


def test_workflow_identity_can_only_supply_summaries_not_success_receipts() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "dispatch-bot"
    summary = IssueCommentInfo(1, "github-actions[bot]", "<!-- agdt:ai-pr-loop-summary -->")
    provider.list_issue_comments.return_value = [
        summary,
        IssueCommentInfo(2, "github-actions[bot]", "<!-- repair-dispatch:v2:spoof -->"),
    ]
    assert authentic_repair_comments(provider, 42, include_workflow_summaries=True) == [summary]
    assert authentic_repair_comments(provider, 42) == []


@pytest.mark.parametrize("login", ["", None, 3])
def test_authentic_repair_comments_requires_resolved_identity(login: object) -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = login
    with pytest.raises(RuntimeError, match="identity"):
        authentic_repair_comments(provider, 42)
