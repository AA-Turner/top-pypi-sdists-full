"""Tests for GitHubActionsProvider.list_closing_issues."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ClosingIssue


def test_reads_all_pages_and_normalizes_issue_body() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider,
        "graphql",
        side_effect=[
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "closingIssuesReferences": {
                                "nodes": [{"number": 1, "title": "Issue one", "body": "Spec"}],
                                "pageInfo": {"hasNextPage": True, "endCursor": "next"},
                            }
                        }
                    }
                }
            },
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "closingIssuesReferences": {
                                "nodes": [{"number": 2, "title": "Issue two", "body": None}],
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                            }
                        }
                    }
                }
            },
        ],
    ) as mock_graphql:
        assert provider.list_closing_issues(7) == [
            ClosingIssue(1, "Issue one", "Spec"),
            ClosingIssue(2, "Issue two", ""),
        ]
    assert mock_graphql.call_count == 2


def test_unavailable_closing_reference_shape_returns_empty() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(provider, "graphql", return_value={"data": {"repository": {"pullRequest": None}}}):
        assert provider.list_closing_issues(7) == []


def test_malformed_reference_shape_returns_existing_issues() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider,
        "graphql",
        side_effect=[
            {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "closingIssuesReferences": {
                                "nodes": [{"number": 1, "title": "Issue one"}],
                                "pageInfo": {"hasNextPage": True, "endCursor": "next"},
                            }
                        }
                    }
                }
            },
            {"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": None}}}}},
        ],
    ) as mock_graphql:
        assert provider.list_closing_issues(7) == [ClosingIssue(1, "Issue one", "")]
        assert mock_graphql.call_count == 2


def test_ignores_non_dict_closing_issue_nodes() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider,
        "graphql",
        return_value={
            "data": {
                "repository": {
                    "pullRequest": {
                        "closingIssuesReferences": {
                            "nodes": [
                                None,
                                {"number": True, "title": "Invalid issue"},
                                {"number": 2, "title": "Issue two"},
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            }
        },
    ):
        assert provider.list_closing_issues(7) == [ClosingIssue(2, "Issue two", "")]


def test_pagination_without_cursor_fails_closed() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with patch.object(
        provider,
        "graphql",
        return_value={
            "data": {
                "repository": {
                    "pullRequest": {
                        "closingIssuesReferences": {
                            "nodes": [],
                            "pageInfo": {"hasNextPage": True, "endCursor": None},
                        }
                    }
                }
            }
        },
    ):
        with pytest.raises(RuntimeError, match="no end cursor"):
            provider.list_closing_issues(7)
