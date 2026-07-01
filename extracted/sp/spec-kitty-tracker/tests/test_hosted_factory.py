"""Tests for the hosted transport factory (WP01)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import get_args

import pytest

from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.hosted import (
    GitHubHostedParams,
    GitLabHostedParams,
    HostedConnectorRequest,
    HostedProviderSlug,
    JiraHostedParams,
    LinearHostedParams,
    create_hosted_connector,
)
from spec_kitty_tracker.nango import NANGO_MANAGED_TOKEN, NangoConnectionContext, NangoProxyAdapter
from spec_kitty_tracker.protocols import TaskTrackerConnector


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def nango_ctx() -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id="conn-123",
        provider_config_key="linear",
        nango_secret_key="secret-key",
    )


# ---------------------------------------------------------------------------
# T001: Params dataclass tests
# ---------------------------------------------------------------------------


class TestLinearHostedParams:
    def test_frozen(self) -> None:
        params = LinearHostedParams(team_id="team-1")
        with pytest.raises(FrozenInstanceError):
            params.team_id = "other"  # type: ignore[misc]

    def test_slots(self) -> None:
        assert hasattr(LinearHostedParams, "__slots__")

    def test_defaults(self) -> None:
        params = LinearHostedParams(team_id="team-1")
        assert params.workspace == "linear"
        assert params.graphql_url == "https://api.linear.app/graphql"
        assert params.status_to_state_id == {}


class TestJiraHostedParams:
    def test_frozen(self) -> None:
        params = JiraHostedParams(base_url="https://jira.example.com", project_key="PROJ")
        with pytest.raises(FrozenInstanceError):
            params.base_url = "other"  # type: ignore[misc]

    def test_slots(self) -> None:
        assert hasattr(JiraHostedParams, "__slots__")

    def test_defaults(self) -> None:
        params = JiraHostedParams(base_url="https://jira.example.com", project_key="PROJ")
        assert params.default_issue_type == "Task"
        assert params.status_name_map == {}


class TestGitHubHostedParams:
    def test_frozen(self) -> None:
        params = GitHubHostedParams(owner="octocat", repo="hello-world")
        with pytest.raises(FrozenInstanceError):
            params.owner = "other"  # type: ignore[misc]

    def test_slots(self) -> None:
        assert hasattr(GitHubHostedParams, "__slots__")

    def test_defaults(self) -> None:
        params = GitHubHostedParams(owner="octocat", repo="hello-world")
        assert params.base_url == "https://api.github.com"


class TestGitLabHostedParams:
    def test_frozen(self) -> None:
        params = GitLabHostedParams(project_id="12345")
        with pytest.raises(FrozenInstanceError):
            params.project_id = "other"  # type: ignore[misc]

    def test_slots(self) -> None:
        assert hasattr(GitLabHostedParams, "__slots__")

    def test_defaults(self) -> None:
        params = GitLabHostedParams(project_id="12345")
        assert params.base_url == "https://gitlab.com/api/v4"


# ---------------------------------------------------------------------------
# T002: HostedConnectorRequest tests
# ---------------------------------------------------------------------------


class TestHostedConnectorRequest:
    def test_frozen(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        with pytest.raises(FrozenInstanceError):
            req.provider = "jira"  # type: ignore[misc]

    def test_slots(self) -> None:
        assert hasattr(HostedConnectorRequest, "__slots__")

    def test_construction_all_providers(self, nango_ctx: NangoConnectionContext) -> None:
        """HostedConnectorRequest can be constructed with all 4 provider slugs."""
        HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        HostedConnectorRequest(
            provider="jira",
            nango_context=nango_ctx,
            params=JiraHostedParams(base_url="https://jira.example.com", project_key="PK"),
        )
        HostedConnectorRequest(
            provider="github",
            nango_context=nango_ctx,
            params=GitHubHostedParams(owner="o", repo="r"),
        )
        HostedConnectorRequest(
            provider="gitlab",
            nango_context=nango_ctx,
            params=GitLabHostedParams(project_id="123"),
        )


# ---------------------------------------------------------------------------
# Type alias test
# ---------------------------------------------------------------------------


class TestHostedProviderSlug:
    def test_literal_values(self) -> None:
        """HostedProviderSlug accepts exactly 'linear', 'jira', 'github', 'gitlab'."""
        args = set(get_args(HostedProviderSlug))
        assert args == {"linear", "jira", "github", "gitlab"}


# ---------------------------------------------------------------------------
# T003: Factory construction tests (one per provider)
# ---------------------------------------------------------------------------


class TestFactoryLinear:
    def test_returns_task_tracker_connector(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, TaskTrackerConnector)

    def test_sentinel_injection(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.api_key == NANGO_MANAGED_TOKEN


class TestFactoryJira:
    def test_returns_task_tracker_connector(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="jira",
            nango_context=nango_ctx,
            params=JiraHostedParams(base_url="https://jira.example.com", project_key="PROJ"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, TaskTrackerConnector)

    def test_sentinel_injection_both_credentials(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="jira",
            nango_context=nango_ctx,
            params=JiraHostedParams(base_url="https://jira.example.com", project_key="PROJ"),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.email == NANGO_MANAGED_TOKEN
        assert config.api_token == NANGO_MANAGED_TOKEN


class TestFactoryGitHub:
    def test_returns_task_tracker_connector(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="github",
            nango_context=nango_ctx,
            params=GitHubHostedParams(owner="octocat", repo="hello-world"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, TaskTrackerConnector)

    def test_sentinel_injection(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="github",
            nango_context=nango_ctx,
            params=GitHubHostedParams(owner="octocat", repo="hello-world"),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.token == NANGO_MANAGED_TOKEN


class TestFactoryGitLab:
    def test_returns_task_tracker_connector(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="gitlab",
            nango_context=nango_ctx,
            params=GitLabHostedParams(project_id="12345"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, TaskTrackerConnector)

    def test_sentinel_injection(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="gitlab",
            nango_context=nango_ctx,
            params=GitLabHostedParams(project_id="12345"),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.token == NANGO_MANAGED_TOKEN


# ---------------------------------------------------------------------------
# T004: Factory rejection tests
# ---------------------------------------------------------------------------


class TestFactoryRejection:
    def test_unknown_slug(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="unknown",  # type: ignore[arg-type]
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            create_hosted_connector(req)

    def test_beads_slug(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="beads",  # type: ignore[arg-type]
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            create_hosted_connector(req)

    def test_fp_slug(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="fp",  # type: ignore[arg-type]
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            create_hosted_connector(req)

    def test_azure_devops_slug(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="azure_devops",  # type: ignore[arg-type]
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        with pytest.raises(ConnectorConfigError, match="Unsupported hosted provider"):
            create_hosted_connector(req)

    def test_wrong_params_type_for_provider(self, nango_ctx: NangoConnectionContext) -> None:
        """Passing GitHubHostedParams with provider 'linear' raises ConnectorConfigError."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=GitHubHostedParams(owner="o", repo="r"),
        )
        with pytest.raises(ConnectorConfigError, match="Expected LinearHostedParams"):
            create_hosted_connector(req)

    def test_error_includes_slug_name(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="beads",  # type: ignore[arg-type]
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="t1"),
        )
        with pytest.raises(ConnectorConfigError, match="beads"):
            create_hosted_connector(req)


# ---------------------------------------------------------------------------
# Config propagation test
# ---------------------------------------------------------------------------


class TestConfigPropagation:
    def test_empty_team_id_raises(self, nango_ctx: NangoConnectionContext) -> None:
        """Empty team_id propagates ConnectorConfigError from LinearConnector validation."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id=""),
        )
        with pytest.raises(ConnectorConfigError):
            create_hosted_connector(req)

    def test_params_fields_propagate_to_config(self, nango_ctx: NangoConnectionContext) -> None:
        """Non-credential fields from params appear in the underlying connector config."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(
                team_id="team-42",
                workspace="my-workspace",
                graphql_url="https://custom.linear.app/graphql",
            ),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.team_id == "team-42"
        assert config.workspace == "my-workspace"
        assert config.graphql_url == "https://custom.linear.app/graphql"

    def test_jira_params_propagate(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="jira",
            nango_context=nango_ctx,
            params=JiraHostedParams(
                base_url="https://my-jira.atlassian.net",
                project_key="SKT",
                default_issue_type="Bug",
            ),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.base_url == "https://my-jira.atlassian.net"
        assert config.project_key == "SKT"
        assert config.default_issue_type == "Bug"

    def test_github_params_propagate(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="github",
            nango_context=nango_ctx,
            params=GitHubHostedParams(
                owner="acme",
                repo="widgets",
                base_url="https://github.example.com/api/v3",
            ),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.owner == "acme"
        assert config.repo == "widgets"
        assert config.base_url == "https://github.example.com/api/v3"

    def test_gitlab_params_propagate(self, nango_ctx: NangoConnectionContext) -> None:
        req = HostedConnectorRequest(
            provider="gitlab",
            nango_context=nango_ctx,
            params=GitLabHostedParams(
                project_id="99",
                base_url="https://gitlab.example.com/api/v4",
            ),
        )
        adapter = create_hosted_connector(req)
        config = adapter._connector.config  # type: ignore[attr-defined]
        assert config.project_id == "99"
        assert config.base_url == "https://gitlab.example.com/api/v4"


# ---------------------------------------------------------------------------
# Return type tests
# ---------------------------------------------------------------------------


class TestFactoryReturnType:
    def test_returns_nango_proxy_adapter(self, nango_ctx: NangoConnectionContext) -> None:
        """Factory returns NangoProxyAdapter (supports async context manager)."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, NangoProxyAdapter)

    def test_return_satisfies_protocol(self, nango_ctx: NangoConnectionContext) -> None:
        """Factory result also satisfies TaskTrackerConnector protocol."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        result = create_hosted_connector(req)
        assert isinstance(result, TaskTrackerConnector)

    def test_return_has_context_manager(self, nango_ctx: NangoConnectionContext) -> None:
        """Factory result supports async context manager (async with)."""
        req = HostedConnectorRequest(
            provider="linear",
            nango_context=nango_ctx,
            params=LinearHostedParams(team_id="team-1"),
        )
        result = create_hosted_connector(req)
        assert hasattr(result, "__aenter__")
        assert hasattr(result, "__aexit__")
