"""GitLab workspace and resource discovery provider."""

from __future__ import annotations

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
_PER_PAGE = 100


class GitLabWorkspaceDiscovery:
    """Discover GitLab groups the authenticated user can access."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(self) -> DiscoveryResult[DiscoveredWorkspace]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            workspaces: list[DiscoveredWorkspace] = []
            truncated = False
            page = 1

            for _ in range(_MAX_PAGES):
                response = await client.get(
                    "https://gitlab.com/api/v4/groups",
                    params={
                        "min_access_level": "10",
                        "per_page": str(_PER_PAGE),
                        "page": str(page),
                    },
                )
                response.raise_for_status()
                groups = response.json()

                if not groups:
                    break

                for group in groups:
                    workspaces.append(
                        DiscoveredWorkspace(
                            id=str(group["id"]),
                            name=group["full_path"],
                            display=group.get("full_name", group["full_path"]),
                            kind="group",
                            provider="gitlab",
                            provider_context={
                                "group_id": str(group["id"]),
                                "full_path": group["full_path"],
                                "web_url": group.get("web_url", ""),
                                "workspace_handle": group["full_path"],
                                "workspace_url": group.get("web_url") or None,
                            },
                        )
                    )

                if len(groups) < _PER_PAGE:
                    break
                page += 1
            else:
                # Exited the for-loop without breaking -> hit the page limit
                truncated = True

        return DiscoveryResult(items=workspaces, truncated=truncated)


class GitLabResourceDiscovery:
    """Discover GitLab projects within a group workspace."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(
        self, workspace: DiscoveredWorkspace
    ) -> DiscoveryResult[DiscoveredResource]:
        group_id = workspace.provider_context["group_id"]  # type: ignore[index]
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            resources: list[DiscoveredResource] = []
            truncated = False
            page = 1

            for _ in range(_MAX_PAGES):
                response = await client.get(
                    f"https://gitlab.com/api/v4/groups/{group_id}/projects",
                    params={
                        "include_subgroups": "true",
                        "per_page": str(_PER_PAGE),
                        "page": str(page),
                    },
                )
                response.raise_for_status()
                projects = response.json()

                if not projects:
                    break

                for project in projects:
                    project_id = str(project["id"])
                    display_name = project.get(
                        "name_with_namespace"
                    ) or project.get("path_with_namespace", "")

                    connector_params = {
                        "project_id": project_id,
                        "base_url": "https://gitlab.com/api/v4",
                    }

                    namespace = project.get("namespace", {}) or {}
                    routing_metadata = {
                        "project_id": project_id,
                        "path_with_namespace": project.get(
                            "path_with_namespace", ""
                        ),
                        "web_url": project.get("web_url", ""),
                        "namespace_id": str(namespace.get("id", "")),
                        "namespace_path": namespace.get("full_path", ""),
                        "display_key": project.get("path_with_namespace") or None,
                        "resource_url": project.get("web_url") or None,
                    }

                    resources.append(
                        DiscoveredResource(
                            provider="gitlab",
                            parent_workspace_id=workspace.id,
                            resource_type="project",
                            stable_ref=project_id,
                            display_name=display_name,
                            connector_params=connector_params,
                            routing_metadata=routing_metadata,
                        )
                    )

                if len(projects) < _PER_PAGE:
                    break
                page += 1
            else:
                truncated = True

        return DiscoveryResult(items=resources, truncated=truncated)


# --- Module-scope registration ---
register_workspace_discoverer("gitlab", GitLabWorkspaceDiscovery)
register_resource_discoverer("gitlab", GitLabResourceDiscovery)
