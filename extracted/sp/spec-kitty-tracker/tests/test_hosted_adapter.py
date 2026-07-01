"""Tests for discovery.hosted_adapter — connector_params → typed *HostedParams."""

from __future__ import annotations

import pytest

from spec_kitty_tracker.discovery.hosted_adapter import connector_params_to_hosted_params
from spec_kitty_tracker.discovery.types import DiscoveredResource
from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.hosted import (
    GitHubHostedParams,
    GitLabHostedParams,
    JiraHostedParams,
    LinearHostedParams,
)

# ---------------------------------------------------------------------------
# T042: Success cases for all 4 providers
# ---------------------------------------------------------------------------


class TestLinearSuccess:
    def test_minimal(self) -> None:
        result = connector_params_to_hosted_params("linear", {"team_id": "t1"})
        assert result == LinearHostedParams(team_id="t1")

    def test_extra_keys_tolerated(self) -> None:
        result = connector_params_to_hosted_params(
            "linear", {"team_id": "t1", "extra_future_field": 42}
        )
        assert isinstance(result, LinearHostedParams)
        assert result.team_id == "t1"


class TestJiraSuccess:
    def test_minimal(self) -> None:
        result = connector_params_to_hosted_params(
            "jira",
            {
                "project_key": "PROJ",
                "cloud_id": "abc",
                "base_url": "https://mysite.atlassian.net",
            },
        )
        assert result == JiraHostedParams(
            base_url="https://mysite.atlassian.net",
            project_key="PROJ",
        )

    def test_cloud_id_ignored(self) -> None:
        """cloud_id is routing metadata, not a JiraHostedParams field."""
        result = connector_params_to_hosted_params(
            "jira",
            {
                "project_key": "X",
                "cloud_id": "should-be-ignored",
                "base_url": "https://x.atlassian.net",
            },
        )
        assert isinstance(result, JiraHostedParams)
        assert not hasattr(result, "cloud_id")


class TestGitHubSuccess:
    def test_minimal(self) -> None:
        result = connector_params_to_hosted_params(
            "github", {"owner": "org", "repo": "repo"}
        )
        assert result == GitHubHostedParams(owner="org", repo="repo")

    def test_extra_keys_tolerated(self) -> None:
        result = connector_params_to_hosted_params(
            "github", {"owner": "o", "repo": "r", "v2_flag": True}
        )
        assert isinstance(result, GitHubHostedParams)
        assert result.owner == "o"
        assert result.repo == "r"


class TestGitLabSuccess:
    def test_with_base_url(self) -> None:
        result = connector_params_to_hosted_params(
            "gitlab",
            {"project_id": "123", "base_url": "https://gitlab.example.com/api/v4"},
        )
        assert result == GitLabHostedParams(
            project_id="123",
            base_url="https://gitlab.example.com/api/v4",
        )

    def test_default_base_url(self) -> None:
        result = connector_params_to_hosted_params(
            "gitlab", {"project_id": "456"}
        )
        assert result == GitLabHostedParams(
            project_id="456",
            base_url="https://gitlab.com/api/v4",
        )

    def test_extra_keys_tolerated(self) -> None:
        result = connector_params_to_hosted_params(
            "gitlab", {"project_id": "1", "namespace": "ns"}
        )
        assert isinstance(result, GitLabHostedParams)


# ---------------------------------------------------------------------------
# T042: Missing key cases → ConnectorConfigError
# ---------------------------------------------------------------------------


class TestMissingKeys:
    def test_linear_missing_team_id(self) -> None:
        with pytest.raises(ConnectorConfigError, match="team_id"):
            connector_params_to_hosted_params("linear", {})

    def test_jira_missing_project_key(self) -> None:
        with pytest.raises(ConnectorConfigError, match="project_key"):
            connector_params_to_hosted_params(
                "jira", {"base_url": "https://x.atlassian.net"}
            )

    def test_jira_missing_base_url(self) -> None:
        with pytest.raises(ConnectorConfigError, match="base_url"):
            connector_params_to_hosted_params("jira", {"project_key": "P"})

    def test_jira_missing_both(self) -> None:
        with pytest.raises(ConnectorConfigError, match="Missing required"):
            connector_params_to_hosted_params("jira", {"cloud_id": "abc"})

    def test_github_missing_owner(self) -> None:
        with pytest.raises(ConnectorConfigError, match="owner"):
            connector_params_to_hosted_params("github", {"repo": "r"})

    def test_github_missing_repo(self) -> None:
        with pytest.raises(ConnectorConfigError, match="repo"):
            connector_params_to_hosted_params("github", {"owner": "o"})

    def test_gitlab_missing_project_id(self) -> None:
        with pytest.raises(ConnectorConfigError, match="project_id"):
            connector_params_to_hosted_params("gitlab", {})


# ---------------------------------------------------------------------------
# T042: Unknown provider → ConnectorConfigError
# ---------------------------------------------------------------------------


class TestUnknownProvider:
    def test_unknown_raises(self) -> None:
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            connector_params_to_hosted_params("notion", {"key": "val"})

    def test_empty_provider_raises(self) -> None:
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            connector_params_to_hosted_params("", {})


# ---------------------------------------------------------------------------
# T043: Round-trip from DiscoveredResource through adapter
# ---------------------------------------------------------------------------


class TestRoundTrip:
    def test_linear_round_trip(self) -> None:
        resource = DiscoveredResource(
            provider="linear",
            parent_workspace_id="ws-1",
            resource_type="team",
            stable_ref="linear://team/t-abc",
            display_name="Engineering",
            connector_params={"team_id": "t-abc"},
            routing_metadata={},
        )
        params = connector_params_to_hosted_params(
            resource.provider, resource.connector_params
        )
        assert isinstance(params, LinearHostedParams)
        assert params.team_id == "t-abc"

    def test_jira_round_trip(self) -> None:
        resource = DiscoveredResource(
            provider="jira",
            parent_workspace_id="cloud-xyz",
            resource_type="project",
            stable_ref="jira://cloud-xyz/PROJ",
            display_name="My Project",
            connector_params={
                "project_key": "PROJ",
                "cloud_id": "cloud-xyz",
                "base_url": "https://mysite.atlassian.net",
            },
            routing_metadata={"cloud_id": "cloud-xyz"},
        )
        params = connector_params_to_hosted_params(
            resource.provider, resource.connector_params
        )
        assert isinstance(params, JiraHostedParams)
        assert params.base_url == "https://mysite.atlassian.net"
        assert params.project_key == "PROJ"

    def test_github_round_trip(self) -> None:
        resource = DiscoveredResource(
            provider="github",
            parent_workspace_id="org-acme",
            resource_type="repository",
            stable_ref="github://acme/tracker",
            display_name="acme/tracker",
            connector_params={"owner": "acme", "repo": "tracker"},
            routing_metadata={},
        )
        params = connector_params_to_hosted_params(
            resource.provider, resource.connector_params
        )
        assert isinstance(params, GitHubHostedParams)
        assert params.owner == "acme"
        assert params.repo == "tracker"

    def test_gitlab_round_trip(self) -> None:
        resource = DiscoveredResource(
            provider="gitlab",
            parent_workspace_id="group-99",
            resource_type="project",
            stable_ref="gitlab://99",
            display_name="My GitLab Project",
            connector_params={
                "project_id": "99",
                "base_url": "https://gitlab.example.com/api/v4",
            },
            routing_metadata={},
        )
        params = connector_params_to_hosted_params(
            resource.provider, resource.connector_params
        )
        assert isinstance(params, GitLabHostedParams)
        assert params.project_id == "99"
        assert params.base_url == "https://gitlab.example.com/api/v4"
