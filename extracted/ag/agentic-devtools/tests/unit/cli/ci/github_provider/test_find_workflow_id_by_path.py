"""Tests for resolving workflow IDs by repository path."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_resolves_exact_workflow_path_without_using_observed_id() -> None:
    """Finds a workflow by its path and returns its ID from the current repository."""
    provider = GitHubActionsProvider(repo="owner/repo")
    payload = {
        "workflows": [
            {"id": 77, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"},
            {"id": 88, "path": ".github/workflows/dynamic/agents/copilot-pull-request-reviewer.yml"},
        ]
    }
    with patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        return_value=json.dumps(payload),
    ) as api:
        workflow_id = provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot")

    assert workflow_id == "77"
    api.assert_called_once_with("/repos/owner/repo/actions/workflows?per_page=100&page=1")


def test_returns_none_when_only_the_reviewer_workflow_matches() -> None:
    """Never treats the CCR reviewer workflow as the cloud writer."""
    provider = GitHubActionsProvider(repo="owner/repo")
    payload = {"workflows": [{"id": 88, "path": ".github/workflows/dynamic/agents/copilot-pull-request-reviewer.yml"}]}
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps(payload)):
        assert provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot") is None


def test_rejects_empty_workflow_path_before_api_call() -> None:
    """An empty path is invalid and does not trigger a repository read."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api") as api,
        pytest.raises(ValueError, match="workflow_path must be a non-empty"),
    ):
        provider.find_workflow_id_by_path(".github/workflows/")
    api.assert_not_called()


def test_workflow_path_lookup_requires_workflows_list() -> None:
    """A malformed workflow inventory is surfaced as an explicit error."""
    provider = GitHubActionsProvider(repo="owner/repo")
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({"unexpected": []})),
        pytest.raises(RuntimeError, match="missing its workflows list"),
    ):
        provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot")


def test_workflow_path_lookup_paginates_and_caches_the_result() -> None:
    """A full page triggers one bounded follow-up and the result is cached."""
    provider = GitHubActionsProvider(repo="owner/repo")
    first_page = [{"id": index, "path": f".github/workflows/other-{index}.yml"} for index in range(100)]
    second_page = [
        {"id": 77, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"},
        None,
        {"id": True, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"},
    ]
    with patch(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        side_effect=[json.dumps({"workflows": first_page}), json.dumps({"workflows": second_page})],
    ) as api:
        resolved = provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot")
        cached = provider.find_workflow_id_by_path(".github/workflows/dynamic/copilot-swe-agent/copilot.yaml")

    assert resolved == "77"
    assert cached == resolved
    assert api.call_count == 2


def test_workflow_path_lookup_stops_at_ten_full_pages() -> None:
    """Workflow discovery remains bounded when every page is full."""
    provider = GitHubActionsProvider(repo="owner/repo")
    pages = []
    for page in range(10):
        workflows = [{"id": 77, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"}]
        workflows.extend(
            {"id": page * 100 + index, "path": f".github/workflows/other-{page}-{index}.yml"} for index in range(99)
        )
        pages.append(json.dumps({"workflows": workflows}))

    with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=pages) as api:
        workflow_id = provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot")

    assert workflow_id == "77"
    assert api.call_count == 10


def test_ambiguous_workflow_path_is_cached_as_unresolved() -> None:
    """Multiple distinct IDs for the exact path fail closed and avoid repeated reads."""
    provider = GitHubActionsProvider(repo="owner/repo")
    payload = {
        "workflows": [
            {"id": 77, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"},
            {"id": 78, "path": ".github/workflows/dynamic/copilot-swe-agent/copilot.yml"},
        ]
    }
    with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps(payload)) as api:
        assert provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot") is None
        assert provider.find_workflow_id_by_path("dynamic/copilot-swe-agent/copilot") is None

    api.assert_called_once()
