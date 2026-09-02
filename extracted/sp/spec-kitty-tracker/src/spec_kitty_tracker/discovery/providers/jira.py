"""Jira workspace and resource discovery via Nango proxy.

Workspaces are Jira Cloud sites (accessible-resources).
Resources are Jira projects within a site.

CRITICAL: stable_ref uses the numeric project ID (str(project["id"])),
NOT the mutable project key.  Atlassian allows key renames, so the key
is stored in connector_params/routing_metadata for operational use but
must never be the identity anchor.
"""

from __future__ import annotations

from urllib.parse import urlparse

import httpx

from spec_kitty_tracker.discovery.registry import (
    register_resource_discoverer,
    register_workspace_discoverer,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.nango import NangoConnectionContext, NangoProxyTransport

_MAX_PAGES = 20
_PAGE_SIZE = 50


class JiraWorkspaceDiscovery:
    """Discover Jira Cloud sites via Atlassian accessible-resources endpoint."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(self) -> DiscoveryResult[DiscoveredWorkspace]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            response = await client.get(
                "https://api.atlassian.com/oauth/token/accessible-resources",
            )
            response.raise_for_status()
            sites = response.json()

        workspaces = []
        for site in sites:
            site_url = site.get("url", "")
            try:
                parsed_host = urlparse(site_url).hostname or ""
                handle = parsed_host.split(".")[0] if parsed_host else None
                workspace_handle: str | None = handle if handle else None
            except Exception:
                workspace_handle = None
            workspaces.append(
                DiscoveredWorkspace(
                    id=site["id"],
                    name=site["name"],
                    display=site_url or site["name"],
                    kind="site",
                    provider="jira",
                    provider_context={
                        "cloud_id": site["id"],
                        "site_url": site_url,
                        "workspace_handle": workspace_handle,
                        "workspace_url": site_url or None,
                    },
                )
            )
        return DiscoveryResult(items=workspaces, truncated=False)


class JiraResourceDiscovery:
    """Discover Jira projects within a cloud site.

    Uses the numeric project ID as stable_ref (immutable), not the
    mutable project key.
    """

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(self, workspace: DiscoveredWorkspace) -> DiscoveryResult[DiscoveredResource]:
        cloud_id = workspace.provider_context["cloud_id"]  # type: ignore[index]
        base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"

        resources: list[DiscoveredResource] = []
        start_at = 0
        truncated = False

        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            for page in range(_MAX_PAGES):
                response = await client.get(
                    f"{base_url}/rest/api/3/project/search",
                    params={
                        "startAt": str(start_at),
                        "maxResults": str(_PAGE_SIZE),
                    },
                )
                response.raise_for_status()
                data = response.json()

                site_url = (workspace.provider_context or {}).get("site_url", "") or ""
                for project in data.get("values", []):
                    resources.append(
                        DiscoveredResource(
                            provider="jira",
                            parent_workspace_id=workspace.id,
                            resource_type="project",
                            stable_ref=str(project["id"]),
                            display_name=project["name"],
                            connector_params={
                                "project_key": project["key"],
                                "cloud_id": cloud_id,
                                "base_url": base_url,
                            },
                            routing_metadata={
                                "project_id": str(project["id"]),
                                "project_key": project["key"],
                                "project_name": project["name"],
                                "display_key": project["key"],
                                "resource_url": f"{site_url}/browse/{project['key']}"
                                if site_url
                                else None,
                            },
                        )
                    )

                if data.get("isLast", True):
                    break
                start_at += _PAGE_SIZE
            else:
                # Loop completed without break -- hit page limit
                truncated = True

        return DiscoveryResult(items=resources, truncated=truncated)


# ---------------------------------------------------------------------------
# Module-scope registration
# ---------------------------------------------------------------------------

register_workspace_discoverer("jira", JiraWorkspaceDiscovery)
register_resource_discoverer("jira", JiraResourceDiscovery)
