"""Hosted transport factory for SaaS-hosted connector construction via Nango proxy."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal

from spec_kitty_tracker.connectors.github import GitHubConnector, GitHubConnectorConfig
from spec_kitty_tracker.connectors.gitlab import GitLabConnector, GitLabConnectorConfig
from spec_kitty_tracker.connectors.jira import JiraConnector, JiraConnectorConfig
from spec_kitty_tracker.connectors.linear import LinearConnector, LinearConnectorConfig
from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.models import CanonicalStatus
from spec_kitty_tracker.nango import (
    NANGO_MANAGED_TOKEN,
    NangoConnectionContext,
    NangoProxyAdapter,
)

# ---------------------------------------------------------------------------
# T001: Per-provider hosted params dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LinearHostedParams:
    """Non-credential parameters for constructing a hosted Linear connector."""

    team_id: str
    workspace: str = "linear"
    graphql_url: str = "https://api.linear.app/graphql"
    status_to_state_id: Mapping[CanonicalStatus, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class JiraHostedParams:
    """Non-credential parameters for constructing a hosted Jira connector."""

    base_url: str
    project_key: str
    default_issue_type: str = "Task"
    status_name_map: Mapping[CanonicalStatus, str] = field(default_factory=dict)
    spec_kitty_mission_field_id: str | None = None


@dataclass(frozen=True, slots=True)
class GitHubHostedParams:
    """Non-credential parameters for constructing a hosted GitHub connector."""

    owner: str
    repo: str
    base_url: str = "https://api.github.com"


@dataclass(frozen=True, slots=True)
class GitLabHostedParams:
    """Non-credential parameters for constructing a hosted GitLab connector."""

    project_id: str
    base_url: str = "https://gitlab.com/api/v4"


# ---------------------------------------------------------------------------
# T002: HostedProviderSlug type alias and HostedConnectorRequest
# ---------------------------------------------------------------------------

HostedProviderSlug = Literal["linear", "jira", "github", "gitlab"]


@dataclass(frozen=True, slots=True)
class HostedConnectorRequest:
    """Bundles provider slug, Nango context, and provider-specific params for factory dispatch."""

    provider: HostedProviderSlug
    nango_context: NangoConnectionContext
    params: LinearHostedParams | JiraHostedParams | GitHubHostedParams | GitLabHostedParams


# ---------------------------------------------------------------------------
# T003 / T004: create_hosted_connector factory
# ---------------------------------------------------------------------------


def create_hosted_connector(request: HostedConnectorRequest) -> NangoProxyAdapter:
    """Construct a NangoProxyAdapter for SaaS-hosted transport.

    The factory maps provider-specific params to the existing connector config,
    injecting NANGO_MANAGED_TOKEN for all credential fields, then wraps the
    connector in a NangoProxyAdapter using the provided NangoConnectionContext.

    The returned adapter satisfies the TaskTrackerConnector protocol and also
    supports async context manager usage (``async with``) for resource cleanup.

    Args:
        request: HostedConnectorRequest with provider slug, params, and Nango context.

    Returns:
        A NangoProxyAdapter routed through Nango proxy transport.

    Raises:
        ConnectorConfigError: If the provider slug is unsupported or params are invalid.
    """
    provider = request.provider
    params = request.params
    ctx = request.nango_context

    if provider == "linear":
        if not isinstance(params, LinearHostedParams):
            raise ConnectorConfigError(
                f"Expected LinearHostedParams for provider 'linear', got {type(params).__name__}"
            )
        linear_config = LinearConnectorConfig(
            api_key=NANGO_MANAGED_TOKEN,
            team_id=params.team_id,
            workspace=params.workspace,
            graphql_url=params.graphql_url,
            status_to_state_id=params.status_to_state_id,
        )
        return NangoProxyAdapter(LinearConnector, linear_config, ctx)

    if provider == "jira":
        if not isinstance(params, JiraHostedParams):
            raise ConnectorConfigError(
                f"Expected JiraHostedParams for provider 'jira', got {type(params).__name__}"
            )
        jira_config = JiraConnectorConfig(
            base_url=params.base_url,
            email=NANGO_MANAGED_TOKEN,
            api_token=NANGO_MANAGED_TOKEN,
            project_key=params.project_key,
            default_issue_type=params.default_issue_type,
            status_name_map=params.status_name_map,
            spec_kitty_mission_field_id=params.spec_kitty_mission_field_id,
        )
        return NangoProxyAdapter(JiraConnector, jira_config, ctx)

    if provider == "github":
        if not isinstance(params, GitHubHostedParams):
            raise ConnectorConfigError(
                f"Expected GitHubHostedParams for provider 'github', got {type(params).__name__}"
            )
        github_config = GitHubConnectorConfig(
            owner=params.owner,
            repo=params.repo,
            token=NANGO_MANAGED_TOKEN,
            base_url=params.base_url,
        )
        return NangoProxyAdapter(GitHubConnector, github_config, ctx)

    if provider == "gitlab":
        if not isinstance(params, GitLabHostedParams):
            raise ConnectorConfigError(
                f"Expected GitLabHostedParams for provider 'gitlab', got {type(params).__name__}"
            )
        gitlab_config = GitLabConnectorConfig(
            project_id=params.project_id,
            token=NANGO_MANAGED_TOKEN,
            base_url=params.base_url,
        )
        return NangoProxyAdapter(GitLabConnector, gitlab_config, ctx)

    raise ConnectorConfigError(f"Unsupported hosted provider: {provider!r}")
