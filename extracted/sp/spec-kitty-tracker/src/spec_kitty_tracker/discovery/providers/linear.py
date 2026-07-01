"""Linear workspace and resource discovery via GraphQL."""

from __future__ import annotations

import httpx

from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.nango import NangoConnectionContext, NangoProxyTransport

LINEAR_GRAPHQL_URL = "https://api.linear.app/graphql"


class LinearWorkspaceDiscovery:
    """Discover the Linear organization as a workspace."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(self) -> DiscoveryResult[DiscoveredWorkspace]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            query = "{ organization { id name urlKey } }"
            response = await client.post(
                LINEAR_GRAPHQL_URL,
                json={"query": query},
            )
            response.raise_for_status()
            data = response.json()
            org = data["data"]["organization"]

            workspace = DiscoveredWorkspace(
                id=org["id"],
                name=org["urlKey"],
                display=org["name"],
                kind="workspace",
                provider="linear",
                provider_context={
                    "org_id": org["id"],
                    "url_key": org["urlKey"],
                    "workspace_handle": org["urlKey"],
                    "workspace_url": f"https://linear.app/{org['urlKey']}",
                },
            )
            return DiscoveryResult(items=[workspace], truncated=False)


class LinearResourceDiscovery:
    """Discover Linear teams as resources within a workspace."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(
        self, workspace: DiscoveredWorkspace
    ) -> DiscoveryResult[DiscoveredResource]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            query = "{ teams { nodes { id key name } } }"
            response = await client.post(
                LINEAR_GRAPHQL_URL,
                json={"query": query},
            )
            response.raise_for_status()
            data = response.json()
            teams = data["data"]["teams"]["nodes"]

            resources = [
                DiscoveredResource(
                    provider="linear",
                    parent_workspace_id=workspace.id,
                    resource_type="team",
                    stable_ref=team["id"],
                    display_name=team["name"],
                    connector_params={"team_id": team["id"]},
                    routing_metadata={
                        "team_key": team["key"],
                        "team_name": team["name"],
                        "url_key": workspace.name,
                        "display_key": team["key"],
                        "resource_url": f"https://linear.app/{workspace.name}/team/{team['key']}",
                    },
                )
                for team in teams
            ]
            return DiscoveryResult(items=resources, truncated=False)


# ---------------------------------------------------------------------------
# Self-registration
# ---------------------------------------------------------------------------

from spec_kitty_tracker.discovery.registry import (  # noqa: E402
    register_resource_discoverer,
    register_workspace_discoverer,
)

register_workspace_discoverer("linear", LinearWorkspaceDiscovery)
register_resource_discoverer("linear", LinearResourceDiscovery)
