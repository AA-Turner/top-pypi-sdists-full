"""Tests for the report-only supervisor PR inventory."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_list_supervisor_prs_skips_session_and_retry_enrichment() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    response = json.dumps(
        {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": [
                            {
                                "number": 12,
                                "labels": {"nodes": [{"name": "triage"}]},
                                "isCrossRepository": False,
                                "headRefName": "feature",
                                "title": "Example PR",
                                "isDraft": False,
                                "changedFiles": 1,
                            }
                        ],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            }
        }
    )

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=response),
        patch.object(provider, "_fetch_agent_tasks") as fetch_tasks,
        patch("agentic_devtools.cli.ci.pipeline.session_detector.get_latest_session_state") as session_state,
        patch.object(provider, "list_issue_comments") as issue_comments,
        patch.object(provider, "list_pr_files") as pr_files,
    ):
        result = provider.list_supervisor_prs()

    assert [pr.number for pr in result] == [12]
    fetch_tasks.assert_not_called()
    session_state.assert_not_called()
    issue_comments.assert_not_called()
    pr_files.assert_not_called()
