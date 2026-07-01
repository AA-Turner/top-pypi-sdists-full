"""Tests for GitHub discovery provider (workspaces + resources)."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any
from unittest.mock import patch

import httpx
import pytest

from spec_kitty_tracker.discovery.providers.github import (
    GitHubResourceDiscovery,
    GitHubWorkspaceDiscovery,
    _parse_next_url,
)
from spec_kitty_tracker.discovery.registry import (
    _resource_discoverers,
    _workspace_discoverers,
    registered_resource_providers,
    registered_workspace_providers,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredWorkspace,
)
from spec_kitty_tracker.nango import NangoConnectionContext


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class RoutingMockTransport(httpx.AsyncBaseTransport):
    """Returns canned responses based on URL matching, with Link header support."""

    def __init__(
        self,
        routes: dict[str, tuple[int, Any, dict[str, str] | None]],
    ) -> None:
        # routes: pattern -> (status, body, optional extra headers)
        self._routes = routes
        self.requests: list[httpx.Request] = []

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        url_str = str(request.url)
        path = request.url.raw_path.decode("ascii")

        for pattern, (status, body, extra_headers) in self._routes.items():
            if pattern in url_str or pattern in path:
                headers: dict[str, str] = {"content-type": "application/json"}
                if extra_headers:
                    headers.update(extra_headers)
                return httpx.Response(
                    status_code=status,
                    content=json.dumps(body).encode(),
                    headers=headers,
                )
        raise ValueError(f"No mock route for {url_str} (path={path})")

    async def aclose(self) -> None:
        pass


def _make_context() -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id="conn-gh",
        provider_config_key="github",
        nango_secret_key="sk-test-gh",
    )


def _patch_transport(mock_transport: RoutingMockTransport):
    """Patch NangoProxyTransport so discovery classes use our mock transport."""
    return patch(
        "spec_kitty_tracker.discovery.providers.github.NangoProxyTransport",
        return_value=mock_transport,
    )


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    """Snapshot, clear, and restore the global registries around each test."""
    saved_workspace = dict(_workspace_discoverers)
    saved_resource = dict(_resource_discoverers)
    yield
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    _workspace_discoverers.update(saved_workspace)
    _resource_discoverers.update(saved_resource)


def _sample_org(
    org_id: int = 100, login: str = "acme", description: str = "Acme Corp"
) -> dict[str, Any]:
    return {"id": org_id, "login": login, "description": description}


def _sample_user(
    user_id: int = 42, login: str = "octocat", name: str = "The Octocat"
) -> dict[str, Any]:
    return {"id": user_id, "login": login, "name": name}


def _sample_repo(
    repo_id: int = 1,
    name: str = "hello-world",
    full_name: str = "acme/hello-world",
    owner_login: str = "acme",
    default_branch: str = "main",
    html_url: str = "https://github.com/acme/hello-world",
    visibility: str = "public",
) -> dict[str, Any]:
    return {
        "id": repo_id,
        "name": name,
        "full_name": full_name,
        "owner": {"login": owner_login},
        "default_branch": default_branch,
        "html_url": html_url,
        "visibility": visibility,
    }


# ---------------------------------------------------------------------------
# _parse_next_url tests
# ---------------------------------------------------------------------------


class TestParseNextUrl:
    def test_parses_next_link(self) -> None:
        header = (
            '<https://api.github.com/user/repos?page=2>; rel="next", '
            '<https://api.github.com/user/repos?page=5>; rel="last"'
        )
        assert _parse_next_url(header) == "https://api.github.com/user/repos?page=2"

    def test_no_next_link(self) -> None:
        header = '<https://api.github.com/user/repos?page=5>; rel="last"'
        assert _parse_next_url(header) is None

    def test_empty_header(self) -> None:
        assert _parse_next_url("") is None

    def test_only_next(self) -> None:
        header = '<https://api.github.com/orgs/acme/repos?page=3>; rel="next"'
        assert _parse_next_url(header) == "https://api.github.com/orgs/acme/repos?page=3"


# ---------------------------------------------------------------------------
# Workspace discovery tests
# ---------------------------------------------------------------------------


class TestGitHubWorkspaceDiscovery:
    @pytest.mark.anyio
    async def test_org_and_personal_workspaces(self) -> None:
        """Discover 2 orgs + 1 personal workspace."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/orgs": (
                200,
                [
                    _sample_org(100, "acme", "Acme Corp"),
                    _sample_org(200, "widgets", "Widgets Inc"),
                ],
                None,
            ),
            "/user": (
                200,
                _sample_user(42, "octocat", "The Octocat"),
                None,
            ),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubWorkspaceDiscovery(_make_context())

        with _patch_transport(mock):
            result = await discoverer.discover()

        assert len(result.items) == 3
        assert result.truncated is False

        # Verify org workspaces
        orgs = [w for w in result.items if w.kind == "org"]
        assert len(orgs) == 2
        assert orgs[0].id == "100"
        assert orgs[0].name == "acme"
        assert orgs[0].display == "Acme Corp"
        assert orgs[0].provider == "github"
        assert orgs[0].provider_context == {
            "workspace_type": "org",
            "login": "acme",
            "account_id": "100",
            "workspace_handle": "acme",
            "workspace_url": "https://github.com/acme",
        }

        assert orgs[1].id == "200"
        assert orgs[1].name == "widgets"
        assert orgs[1].display == "Widgets Inc"
        assert orgs[1].provider_context == {
            "workspace_type": "org",
            "login": "widgets",
            "account_id": "200",
            "workspace_handle": "widgets",
            "workspace_url": "https://github.com/widgets",
        }

        # Verify personal workspace
        personal = [w for w in result.items if w.kind == "user"]
        assert len(personal) == 1
        assert personal[0].id == "42"
        assert personal[0].name == "octocat"
        assert personal[0].display == "The Octocat"
        assert personal[0].provider == "github"
        assert personal[0].provider_context == {
            "workspace_type": "user",
            "login": "octocat",
            "account_id": "42",
            "workspace_handle": "octocat",
            "workspace_url": "https://github.com/octocat",
        }

    @pytest.mark.anyio
    async def test_personal_workspace_uses_login_when_name_missing(self) -> None:
        """When user has no name, display falls back to login."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/orgs": (200, [], None),
            "/user": (200, {"id": 99, "login": "ghostuser", "name": None}, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubWorkspaceDiscovery(_make_context())

        with _patch_transport(mock):
            result = await discoverer.discover()

        assert len(result.items) == 1
        personal = result.items[0]
        assert personal.display == "ghostuser"
        assert personal.name == "ghostuser"

    @pytest.mark.anyio
    async def test_graceful_degradation_user_403(self) -> None:
        """When /user returns 403, only org workspaces are returned."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/orgs": (
                200,
                [_sample_org(100, "acme", "Acme Corp")],
                None,
            ),
            "/user": (403, {"message": "Forbidden"}, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubWorkspaceDiscovery(_make_context())

        with _patch_transport(mock):
            result = await discoverer.discover()

        assert len(result.items) == 1
        assert result.items[0].kind == "org"
        assert result.items[0].name == "acme"
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_no_orgs_only_personal(self) -> None:
        """User with no org memberships still gets personal workspace."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/orgs": (200, [], None),
            "/user": (200, _sample_user(42, "octocat", "The Octocat"), None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubWorkspaceDiscovery(_make_context())

        with _patch_transport(mock):
            result = await discoverer.discover()

        assert len(result.items) == 1
        assert result.items[0].kind == "user"
        assert result.items[0].id == "42"

    @pytest.mark.anyio
    async def test_org_without_description_uses_login(self) -> None:
        """Org with null description uses login as display."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/orgs": (
                200,
                [{"id": 100, "login": "acme", "description": None}],
                None,
            ),
            "/user": (200, _sample_user(), None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubWorkspaceDiscovery(_make_context())

        with _patch_transport(mock):
            result = await discoverer.discover()

        org = [w for w in result.items if w.kind == "org"][0]
        assert org.display == "acme"


# ---------------------------------------------------------------------------
# Resource discovery tests
# ---------------------------------------------------------------------------


class TestGitHubResourceDiscovery:
    @pytest.mark.anyio
    async def test_org_repo_discovery(self) -> None:
        """Discover repos for an org workspace."""
        repos = [
            _sample_repo(1, "alpha", "acme/alpha", "acme"),
            _sample_repo(2, "beta", "acme/beta", "acme", visibility="private"),
        ]
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/orgs/acme/repos": (200, repos, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100",
            name="acme",
            display="Acme Corp",
            kind="org",
            provider="github",
            provider_context={
                "workspace_type": "org",
                "login": "acme",
                "account_id": "100",
            },
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 2
        assert result.truncated is False

        r1 = result.items[0]
        assert r1.stable_ref == "1"
        assert r1.display_name == "acme/alpha"
        assert r1.resource_type == "repository"
        assert r1.provider == "github"
        assert r1.parent_workspace_id == "100"
        assert r1.connector_params == {"owner": "acme", "repo": "alpha"}
        assert r1.routing_metadata["repo_id"] == "1"
        assert r1.routing_metadata["full_name"] == "acme/alpha"
        assert r1.routing_metadata["default_branch"] == "main"
        assert r1.routing_metadata["html_url"] == "https://github.com/acme/hello-world"
        assert r1.routing_metadata["visibility"] == "public"

        r2 = result.items[1]
        assert r2.stable_ref == "2"
        assert r2.connector_params == {"owner": "acme", "repo": "beta"}
        assert r2.routing_metadata["visibility"] == "private"

    @pytest.mark.anyio
    async def test_personal_repo_discovery(self) -> None:
        """Discover repos for a personal workspace uses /user/repos?affiliation=owner."""
        repos = [
            _sample_repo(10, "my-project", "octocat/my-project", "octocat"),
        ]
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/user/repos": (200, repos, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="42",
            name="octocat",
            display="The Octocat",
            kind="user",
            provider="github",
            provider_context={
                "workspace_type": "user",
                "login": "octocat",
                "account_id": "42",
            },
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 1
        assert result.truncated is False

        r = result.items[0]
        assert r.stable_ref == "10"
        assert r.display_name == "octocat/my-project"
        assert r.parent_workspace_id == "42"
        assert r.connector_params == {"owner": "octocat", "repo": "my-project"}

        # Verify the request URL includes affiliation=owner
        assert len(mock.requests) == 1
        req_url = str(mock.requests[0].url)
        assert "affiliation=owner" in req_url

    @pytest.mark.anyio
    async def test_visibility_fallback_from_private_flag(self) -> None:
        """When visibility field is absent, derive from private boolean."""
        repo = _sample_repo(1, "secret", "acme/secret", "acme")
        del repo["visibility"]
        repo["private"] = True

        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/orgs/acme/repos": (200, [repo], None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert result.items[0].routing_metadata["visibility"] == "private"

    @pytest.mark.anyio
    async def test_visibility_fallback_public(self) -> None:
        """When visibility is absent and private is False, visibility is public."""
        repo = _sample_repo(1, "open", "acme/open", "acme")
        del repo["visibility"]
        repo["private"] = False

        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/orgs/acme/repos": (200, [repo], None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert result.items[0].routing_metadata["visibility"] == "public"


# ---------------------------------------------------------------------------
# Pagination tests
# ---------------------------------------------------------------------------


class TestGitHubPagination:
    @pytest.mark.anyio
    async def test_two_pages_collected(self) -> None:
        """Follow Link header for 2-page response."""
        page1_repos = [_sample_repo(1, "repo-1", "acme/repo-1", "acme")]
        page2_repos = [_sample_repo(2, "repo-2", "acme/repo-2", "acme")]

        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/orgs/acme/repos?sort=full_name&per_page=100": (
                200,
                page1_repos,
                {"link": '<https://api.github.com/orgs/acme/repos?page=2>; rel="next"'},
            ),
            "page=2": (200, page2_repos, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 2
        assert result.items[0].stable_ref == "1"
        assert result.items[1].stable_ref == "2"
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_truncation_at_max_pages(self) -> None:
        """Set truncated=True when page limit (10) is reached and more pages exist."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {}

        for page_num in range(1, 12):  # 11 pages total, but we stop at 10
            repos = [
                _sample_repo(page_num, f"repo-{page_num}", f"acme/repo-{page_num}", "acme")
            ]
            if page_num == 1:
                key = "/orgs/acme/repos?sort=full_name&per_page=100"
            else:
                key = f"page={page_num}"

            next_page = page_num + 1
            link_header = (
                f'<https://api.github.com/orgs/acme/repos?page={next_page}>; rel="next"'
            )
            routes[key] = (200, repos, {"link": link_header})

        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 10  # 10 pages, 1 repo each
        assert result.truncated is True

    @pytest.mark.anyio
    async def test_no_link_header_single_page(self) -> None:
        """Single page without Link header => no pagination, not truncated."""
        repos = [_sample_repo(1, "solo", "acme/solo", "acme")]
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {
            "/orgs/acme/repos": (200, repos, None),
        }
        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 1
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_exactly_max_pages_no_more(self) -> None:
        """When exactly 10 pages with no next link on last page, not truncated."""
        routes: dict[str, tuple[int, Any, dict[str, str] | None]] = {}

        for page_num in range(1, 11):  # 10 pages
            repos = [
                _sample_repo(page_num, f"repo-{page_num}", f"acme/repo-{page_num}", "acme")
            ]
            if page_num == 1:
                key = "/orgs/acme/repos?sort=full_name&per_page=100"
            else:
                key = f"page={page_num}"

            if page_num < 10:
                next_page = page_num + 1
                link_header: str | None = (
                    f'<https://api.github.com/orgs/acme/repos?page={next_page}>; rel="next"'
                )
            else:
                link_header = None  # Last page has no next

            extra = {"link": link_header} if link_header else None
            routes[key] = (200, repos, extra)

        mock = RoutingMockTransport(routes)
        discoverer = GitHubResourceDiscovery(_make_context())

        workspace = DiscoveredWorkspace(
            id="100", name="acme", display="Acme", kind="org", provider="github",
            provider_context={"workspace_type": "org", "login": "acme", "account_id": "100"},
        )

        with _patch_transport(mock):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 10
        assert result.truncated is False


# ---------------------------------------------------------------------------
# Registration tests
# ---------------------------------------------------------------------------


class TestGitHubRegistration:
    def test_github_workspace_discoverer_registered(self) -> None:
        assert "github" in registered_workspace_providers()

    def test_github_resource_discoverer_registered(self) -> None:
        assert "github" in registered_resource_providers()
