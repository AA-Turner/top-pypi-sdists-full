"""Adapter bridging connector_params dicts to typed *HostedParams dataclasses.

Translates ``DiscoveredResource.connector_params`` (``dict[str, JSONValue]``)
into the typed dataclasses that ``create_hosted_connector()`` expects, giving
hosts one blessed translation path without modifying ``hosted.py``.
"""

from __future__ import annotations

from spec_kitty_tracker.errors import ConnectorConfigError
from spec_kitty_tracker.hosted import (
    GitHubHostedParams,
    GitLabHostedParams,
    JiraHostedParams,
    LinearHostedParams,
)
from spec_kitty_tracker.types import JSONValue

HostedParams = LinearHostedParams | JiraHostedParams | GitHubHostedParams | GitLabHostedParams


def _require_keys(connector_params: dict[str, JSONValue], *keys: str) -> None:
    """Validate that all *keys* are present in *connector_params*.

    Raises:
        ConnectorConfigError: If any required key is missing.
    """
    missing = [k for k in keys if k not in connector_params]
    if missing:
        raise ConnectorConfigError(
            f"Missing required connector_params keys: {missing}"
        )


def connector_params_to_hosted_params(
    provider: str,
    connector_params: dict[str, JSONValue],
) -> HostedParams:
    """Convert a ``connector_params`` dict to the corresponding ``*HostedParams`` dataclass.

    Args:
        provider: Provider slug (``"linear"``, ``"jira"``, ``"github"``, ``"gitlab"``).
        connector_params: Flat key/value dict from ``DiscoveredResource.connector_params``.

    Returns:
        The typed ``*HostedParams`` instance for *provider*.

    Raises:
        ConnectorConfigError: If required keys are missing or *provider* is unknown.
    """
    if provider == "linear":
        _require_keys(connector_params, "team_id")
        return LinearHostedParams(team_id=str(connector_params["team_id"]))

    if provider == "jira":
        _require_keys(connector_params, "project_key", "base_url")
        return JiraHostedParams(
            base_url=str(connector_params["base_url"]),
            project_key=str(connector_params["project_key"]),
        )

    if provider == "github":
        _require_keys(connector_params, "owner", "repo")
        return GitHubHostedParams(
            owner=str(connector_params["owner"]),
            repo=str(connector_params["repo"]),
        )

    if provider == "gitlab":
        _require_keys(connector_params, "project_id")
        return GitLabHostedParams(
            project_id=str(connector_params["project_id"]),
            base_url=str(
                connector_params.get("base_url", "https://gitlab.com/api/v4")
            ),
        )

    raise ConnectorConfigError(f"Unsupported hosted provider: {provider!r}")
