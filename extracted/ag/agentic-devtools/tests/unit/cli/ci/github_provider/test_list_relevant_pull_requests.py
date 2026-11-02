"""Tests for complete relevant pull-request inventory pagination."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _response(nodes: list[dict], *, has_next: bool = False, cursor: str | None = None) -> str:
    return json.dumps(
        {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": nodes,
                        "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                    }
                }
            }
        }
    )


def _node(number: int) -> dict:
    return {
        "number": number,
        "title": f"PR {number}",
        "headRefName": f"feature/{number}",
        "headRefOid": f"sha-{number}",
        "baseRefName": "main",
        "headRepository": {"nameWithOwner": "owner/repo"},
        "repository": {"nameWithOwner": "owner/repo"},
        "labels": {"nodes": [{"name": "automation"}]},
        "isDraft": False,
    }


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_returns_page_and_cursor(mock_api) -> None:
    """Returns normalized metadata and the provider's next cursor."""
    mock_api.return_value = _response([_node(1), _node(2)], has_next=True, cursor="cursor-1")
    provider = GitHubActionsProvider(repo="owner/repo")

    pull_requests, next_cursor = provider.list_relevant_pull_requests(limit=2)

    assert [pull_request.number for pull_request in pull_requests] == [1, 2]
    assert pull_requests[0].base_branch == "main"
    assert next_cursor == "cursor-1"
    assert mock_api.call_args.kwargs["body"]["variables"]["after"] is None


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_uses_cursor(mock_api) -> None:
    """Passes a supplied cursor to the next inventory page."""
    mock_api.return_value = _response([_node(3)])
    provider = GitHubActionsProvider(repo="owner/repo")

    provider.list_relevant_pull_requests(cursor="cursor-1", limit=25)

    assert mock_api.call_args.kwargs["body"]["variables"]["after"] == "cursor-1"


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_tolerates_missing_optional_fields(mock_api) -> None:
    """Uses safe defaults when optional labels, repositories, and draft fields are absent."""
    node = _node(4)
    node["labels"] = None
    node["headRepository"] = None
    node["repository"] = None
    node["isDraft"] = "unknown"
    mock_api.return_value = _response([node])
    provider = GitHubActionsProvider(repo="owner/repo")

    pull_requests, next_cursor = provider.list_relevant_pull_requests()

    assert pull_requests[0].labels == []
    assert pull_requests[0].head_repo_full_name == ""
    assert pull_requests[0].base_repo_full_name == ""
    assert pull_requests[0].is_draft is False
    assert next_cursor is None


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_excludes_forks_and_skip_label(mock_api) -> None:
    """Excludes pull requests that the scheduler never considers relevant."""
    fork = _node(5)
    fork["isCrossRepository"] = True
    ignored = _node(6)
    ignored["labels"] = {"nodes": [{"name": "ai-pr-loop-ignore"}]}
    mock_api.return_value = _response([fork, ignored, _node(7)])
    provider = GitHubActionsProvider(repo="owner/repo")

    pull_requests, _ = provider.list_relevant_pull_requests()

    assert [pull_request.number for pull_request in pull_requests] == [7]


def test_list_relevant_pull_requests_rejects_invalid_limit() -> None:
    """Rejects page sizes outside the GitHub GraphQL range."""
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(ValueError, match="limit"):
        provider.list_relevant_pull_requests(limit=0)


def test_list_relevant_pull_requests_rejects_invalid_cursor() -> None:
    """Rejects cursor values that cannot be sent to GraphQL."""
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(ValueError, match="cursor"):
        provider.list_relevant_pull_requests(cursor=42)  # type: ignore[arg-type]


@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_rejects_malformed_response(mock_api) -> None:
    """Raises a controlled error when the inventory payload is malformed."""
    mock_api.return_value = json.dumps({"data": {"repository": {}}})
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(RuntimeError, match="inventory"):
        provider.list_relevant_pull_requests()


@pytest.mark.parametrize(
    "payload",
    [
        [],
        None,
        1,
        {"errors": [{"message": "provider unavailable"}]},
        {"errors": [None]},
        {},
        {"data": {"repository": None}},
        {"data": {"repository": {"pullRequests": {"nodes": {}, "pageInfo": {}}}}},
        {"data": {"repository": {"pullRequests": {"nodes": [[]], "pageInfo": {}}}}},
        {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": [{"number": 0}],
                        "pageInfo": {},
                    }
                }
            }
        },
        {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": [],
                        "pageInfo": {"hasNextPage": "yes", "endCursor": None},
                    }
                }
            }
        },
        {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": [],
                        "pageInfo": {"hasNextPage": True, "endCursor": None},
                    }
                }
            }
        },
    ],
)
@patch("agentic_devtools.cli.ci.github_provider._gh_api")
def test_list_relevant_pull_requests_rejects_malformed_pages(mock_api, payload) -> None:
    """Rejects provider errors and malformed page, node, and cursor data."""
    mock_api.return_value = json.dumps(payload)
    provider = GitHubActionsProvider(repo="owner/repo")

    with pytest.raises(RuntimeError, match="inventory"):
        provider.list_relevant_pull_requests()
