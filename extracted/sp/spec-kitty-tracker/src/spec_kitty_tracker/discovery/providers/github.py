"""GitHub discovery provider: org + personal workspaces and repository resources."""

from __future__ import annotations

import logging
import re

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

logger = logging.getLogger(__name__)

_MAX_PAGES = 10


def _parse_next_url(link_header: str) -> str | None:
    """Extract the URL with rel="next" from a GitHub Link header."""
    for part in link_header.split(","):
        if 'rel="next"' in part:
            match = re.search(r"<([^>]+)>", part)
            if match:
                return match.group(1)
    return None


class GitHubWorkspaceDiscovery:
    """Discover GitHub workspaces: orgs (kind='org') + personal (kind='user')."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(self) -> DiscoveryResult[DiscoveredWorkspace]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            workspaces: list[DiscoveredWorkspace] = []

            # Fetch org workspaces
            response = await client.get("https://api.github.com/user/orgs")
            response.raise_for_status()
            for org in response.json():
                workspaces.append(
                    DiscoveredWorkspace(
                        id=str(org["id"]),
                        name=org["login"],
                        display=org.get("description") or org["login"],
                        kind="org",
                        provider="github",
                        provider_context={
                            "workspace_type": "org",
                            "login": org["login"],
                            "account_id": str(org["id"]),
                            "workspace_handle": org["login"],
                            "workspace_url": f"https://github.com/{org['login']}",
                        },
                    )
                )

            # Fetch personal workspace identity
            try:
                user_response = await client.get("https://api.github.com/user")
                user_response.raise_for_status()
                user = user_response.json()
                workspaces.append(
                    DiscoveredWorkspace(
                        id=str(user["id"]),
                        name=user["login"],
                        display=user.get("name") or user["login"],
                        kind="user",
                        provider="github",
                        provider_context={
                            "workspace_type": "user",
                            "login": user["login"],
                            "account_id": str(user["id"]),
                            "workspace_handle": user["login"],
                            "workspace_url": f"https://github.com/{user['login']}",
                        },
                    )
                )
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "Failed to fetch GitHub user identity (status %s), "
                    "omitting personal workspace",
                    exc.response.status_code,
                )

            return DiscoveryResult(items=workspaces, truncated=False)


class GitHubResourceDiscovery:
    """Discover GitHub repositories within an org or personal workspace."""

    def __init__(self, nango_ctx: NangoConnectionContext) -> None:
        self._nango_ctx = nango_ctx

    async def discover(
        self, workspace: DiscoveredWorkspace
    ) -> DiscoveryResult[DiscoveredResource]:
        transport = NangoProxyTransport(self._nango_ctx)
        async with httpx.AsyncClient(transport=transport) as client:
            workspace_type = (workspace.provider_context or {}).get(
                "workspace_type", "org"
            )
            if workspace_type == "user":
                url: str | None = (
                    "https://api.github.com/user/repos"
                    "?affiliation=owner&sort=full_name&per_page=100"
                )
            else:
                url = (
                    f"https://api.github.com/orgs/{workspace.name}/repos"
                    f"?sort=full_name&per_page=100"
                )

            all_repos: list[dict] = []  # type: ignore[type-arg]
            page_count = 0
            truncated = False

            while url and page_count < _MAX_PAGES:
                response = await client.get(url)
                response.raise_for_status()
                repos = response.json()
                all_repos.extend(repos)
                page_count += 1
                url = _parse_next_url(response.headers.get("link", ""))

            if url is not None:
                truncated = True

            resources: list[DiscoveredResource] = []
            for repo in all_repos:
                visibility = repo.get("visibility")
                if visibility is None:
                    visibility = "private" if repo.get("private", False) else "public"
                resources.append(
                    DiscoveredResource(
                        provider="github",
                        parent_workspace_id=workspace.id,
                        resource_type="repository",
                        stable_ref=str(repo["id"]),
                        display_name=repo["full_name"],
                        connector_params={
                            "owner": repo["owner"]["login"],
                            "repo": repo["name"],
                        },
                        routing_metadata={
                            "repo_id": str(repo["id"]),
                            "full_name": repo["full_name"],
                            "default_branch": repo.get("default_branch", "main"),
                            "html_url": repo.get("html_url", ""),
                            "visibility": visibility,
                            "display_key": repo["name"],
                            "resource_url": repo.get("html_url") or None,
                        },
                    )
                )

            return DiscoveryResult(items=resources, truncated=truncated)


# Self-register on import
register_workspace_discoverer("github", GitHubWorkspaceDiscovery)
register_resource_discoverer("github", GitHubResourceDiscovery)
