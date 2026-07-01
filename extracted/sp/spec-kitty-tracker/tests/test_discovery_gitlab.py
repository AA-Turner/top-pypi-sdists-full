"""Tests for GitLab workspace and resource discovery provider."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from spec_kitty_tracker.discovery.providers.gitlab import (
    GitLabResourceDiscovery,
    GitLabWorkspaceDiscovery,
    _MAX_PAGES,
    _PER_PAGE,
)
from spec_kitty_tracker.discovery.registry import (
    _resource_discoverers,
    _workspace_discoverers,
    get_resource_discoverer,
    get_workspace_discoverer,
    register_resource_discoverer,
    register_workspace_discoverer,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredWorkspace,
)
from spec_kitty_tracker.nango import NangoConnectionContext


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class RoutingMockTransport(httpx.AsyncBaseTransport):
    """Returns canned responses based on URL path matching."""

    def __init__(self, routes: dict[str, tuple[int, Any]]) -> None:
        self._routes = routes

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode("ascii")
        for pattern, (status, body) in self._routes.items():
            if pattern in path:
                return httpx.Response(
                    status_code=status,
                    content=json.dumps(body).encode(),
                    headers={"content-type": "application/json"},
                )
        raise ValueError(f"No mock route for {path}")

    async def aclose(self) -> None:
        pass


class PageAwareMockTransport(httpx.AsyncBaseTransport):
    """Returns different responses per page number for pagination testing."""

    def __init__(
        self, path_prefix: str, pages: dict[int, list[dict[str, Any]]]
    ) -> None:
        self._path_prefix = path_prefix
        self._pages = pages

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode("ascii")
        if self._path_prefix not in path:
            raise ValueError(f"No mock route for {path}")

        page_param = request.url.params.get("page", "1")
        page_num = int(page_param)
        body = self._pages.get(page_num, [])

        return httpx.Response(
            status_code=200,
            content=json.dumps(body).encode(),
            headers={"content-type": "application/json"},
        )

    async def aclose(self) -> None:
        pass


def _make_context() -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id="conn-1",
        provider_config_key="gitlab-test",
        nango_secret_key="sk-test",
    )


def _make_workspace_discoverer(
    mock_transport: httpx.AsyncBaseTransport,
) -> GitLabWorkspaceDiscovery:
    """Create a GitLabWorkspaceDiscovery with a mock transport.

    We monkey-patch NangoProxyTransport to use our mock so that
    the `async with httpx.AsyncClient(transport=...)` inside discover()
    uses the canned responses.
    """
    discoverer = GitLabWorkspaceDiscovery(_make_context())
    discoverer._mock_transport = mock_transport  # type: ignore[attr-defined]
    return discoverer


def _make_resource_discoverer(
    mock_transport: httpx.AsyncBaseTransport,
) -> GitLabResourceDiscovery:
    discoverer = GitLabResourceDiscovery(_make_context())
    discoverer._mock_transport = mock_transport  # type: ignore[attr-defined]
    return discoverer


def _gitlab_workspace(
    group_id: str = "42",
    full_path: str = "acme/engineering",
    web_url: str = "https://gitlab.com/groups/acme/engineering",
) -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id=group_id,
        name=full_path,
        display="Acme / Engineering",
        kind="group",
        provider="gitlab",
        provider_context={
            "group_id": group_id,
            "full_path": full_path,
            "web_url": web_url,
        },
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    """Snapshot, clear, and restore the global registries around each test."""
    saved_workspace = dict(_workspace_discoverers)
    saved_resource = dict(_resource_discoverers)
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    # Re-register gitlab explicitly (module-level registration only fires once)
    register_workspace_discoverer("gitlab", GitLabWorkspaceDiscovery)
    register_resource_discoverer("gitlab", GitLabResourceDiscovery)
    yield
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    _workspace_discoverers.update(saved_workspace)
    _resource_discoverers.update(saved_resource)


# ---------------------------------------------------------------------------
# Mock patching — inject mock transport into discover() lifecycle
# ---------------------------------------------------------------------------

# We need to intercept `NangoProxyTransport` construction inside `discover()`
# so that the `httpx.AsyncClient(transport=...)` uses our mock.
# We do this via monkeypatch on the module-level NangoProxyTransport import.


@pytest.fixture()
def _patch_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch NangoProxyTransport in the gitlab module to return
    whatever mock transport is stored on the discoverer instance."""

    import spec_kitty_tracker.discovery.providers.gitlab as gitlab_mod

    _original_class = gitlab_mod.NangoProxyTransport

    class _PatchedTransport:
        """Intercepts construction to return the mock if available."""

        def __new__(cls, *args: Any, **kwargs: Any) -> Any:
            # Walk the call stack to find 'self' with _mock_transport
            import inspect

            frame = inspect.currentframe()
            caller_locals = frame.f_back.f_locals if frame and frame.f_back else {}
            self_ref = caller_locals.get("self")
            if self_ref and hasattr(self_ref, "_mock_transport"):
                return self_ref._mock_transport
            return _original_class(*args, **kwargs)

    monkeypatch.setattr(gitlab_mod, "NangoProxyTransport", _PatchedTransport)


# ---------------------------------------------------------------------------
# Workspace Discovery Tests
# ---------------------------------------------------------------------------


class TestGitLabWorkspaceDiscovery:
    @pytest.mark.anyio
    async def test_discover_groups(self, _patch_transport: None) -> None:
        routes = {
            "/api/v4/groups": (
                200,
                [
                    {
                        "id": 42,
                        "full_path": "acme/engineering",
                        "full_name": "Acme / Engineering",
                        "web_url": "https://gitlab.com/groups/acme/engineering",
                    },
                    {
                        "id": 99,
                        "full_path": "acme/design",
                        "full_name": "Acme / Design",
                        "web_url": "https://gitlab.com/groups/acme/design",
                    },
                ],
            ),
        }
        mock = RoutingMockTransport(routes)
        discoverer = _make_workspace_discoverer(mock)
        result = await discoverer.discover()

        assert len(result.items) == 2
        assert result.truncated is False

        ws0 = result.items[0]
        assert ws0.id == "42"
        assert ws0.name == "acme/engineering"
        assert ws0.display == "Acme / Engineering"
        assert ws0.kind == "group"
        assert ws0.provider == "gitlab"
        assert ws0.provider_context == {
            "group_id": "42",
            "full_path": "acme/engineering",
            "web_url": "https://gitlab.com/groups/acme/engineering",
            "workspace_handle": "acme/engineering",
            "workspace_url": "https://gitlab.com/groups/acme/engineering",
        }

        ws1 = result.items[1]
        assert ws1.id == "99"
        assert ws1.name == "acme/design"
        assert ws1.provider_context["group_id"] == "99"  # type: ignore[index]

    @pytest.mark.anyio
    async def test_discover_empty(self, _patch_transport: None) -> None:
        routes = {"/api/v4/groups": (200, [])}
        mock = RoutingMockTransport(routes)
        discoverer = _make_workspace_discoverer(mock)
        result = await discoverer.discover()

        assert result.items == []
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_missing_web_url_defaults_to_empty(
        self, _patch_transport: None
    ) -> None:
        routes = {
            "/api/v4/groups": (
                200,
                [
                    {
                        "id": 1,
                        "full_path": "solo/group",
                        "full_name": "Solo Group",
                        # no web_url
                    }
                ],
            ),
        }
        mock = RoutingMockTransport(routes)
        discoverer = _make_workspace_discoverer(mock)
        result = await discoverer.discover()

        assert len(result.items) == 1
        assert result.items[0].provider_context["web_url"] == ""  # type: ignore[index]

    @pytest.mark.anyio
    async def test_pagination_multiple_pages(
        self, _patch_transport: None
    ) -> None:
        # Page 1: full page of _PER_PAGE items, Page 2: partial page
        page1 = [
            {
                "id": i,
                "full_path": f"group-{i}",
                "full_name": f"Group {i}",
                "web_url": f"https://gitlab.com/groups/group-{i}",
            }
            for i in range(_PER_PAGE)
        ]
        page2 = [
            {
                "id": _PER_PAGE,
                "full_path": "last-group",
                "full_name": "Last Group",
                "web_url": "https://gitlab.com/groups/last-group",
            }
        ]
        mock = PageAwareMockTransport(
            "/api/v4/groups", {1: page1, 2: page2}
        )
        discoverer = _make_workspace_discoverer(mock)
        result = await discoverer.discover()

        assert len(result.items) == _PER_PAGE + 1
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_truncation_at_page_limit(
        self, _patch_transport: None
    ) -> None:
        # Every page returns exactly _PER_PAGE items, forcing all _MAX_PAGES to be fetched
        full_page = [
            {
                "id": i,
                "full_path": f"group-{i}",
                "full_name": f"Group {i}",
                "web_url": f"https://gitlab.com/groups/group-{i}",
            }
            for i in range(_PER_PAGE)
        ]
        pages = {p: full_page for p in range(1, _MAX_PAGES + 1)}
        mock = PageAwareMockTransport("/api/v4/groups", pages)
        discoverer = _make_workspace_discoverer(mock)
        result = await discoverer.discover()

        assert len(result.items) == _PER_PAGE * _MAX_PAGES
        assert result.truncated is True


# ---------------------------------------------------------------------------
# Resource Discovery Tests
# ---------------------------------------------------------------------------


class TestGitLabResourceDiscovery:
    @pytest.mark.anyio
    async def test_discover_projects(self, _patch_transport: None) -> None:
        routes = {
            "/api/v4/groups/42/projects": (
                200,
                [
                    {
                        "id": 101,
                        "name_with_namespace": "Acme / Eng / Backend",
                        "path_with_namespace": "acme/eng/backend",
                        "web_url": "https://gitlab.com/acme/eng/backend",
                        "namespace": {
                            "id": 42,
                            "full_path": "acme/engineering",
                        },
                    },
                    {
                        "id": 102,
                        "name_with_namespace": "Acme / Eng / Frontend",
                        "path_with_namespace": "acme/eng/frontend",
                        "web_url": "https://gitlab.com/acme/eng/frontend",
                        "namespace": {
                            "id": 42,
                            "full_path": "acme/engineering",
                        },
                    },
                ],
            ),
        }
        workspace = _gitlab_workspace()
        mock = RoutingMockTransport(routes)
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert len(result.items) == 2
        assert result.truncated is False

        r0 = result.items[0]
        assert r0.provider == "gitlab"
        assert r0.parent_workspace_id == "42"
        assert r0.resource_type == "project"
        assert r0.stable_ref == "101"
        assert r0.display_name == "Acme / Eng / Backend"
        assert r0.connector_params == {
            "project_id": "101",
            "base_url": "https://gitlab.com/api/v4",
        }
        assert r0.routing_metadata == {
            "project_id": "101",
            "path_with_namespace": "acme/eng/backend",
            "web_url": "https://gitlab.com/acme/eng/backend",
            "namespace_id": "42",
            "namespace_path": "acme/engineering",
            "display_key": "acme/eng/backend",
            "resource_url": "https://gitlab.com/acme/eng/backend",
        }

        r1 = result.items[1]
        assert r1.stable_ref == "102"
        assert r1.display_name == "Acme / Eng / Frontend"

    @pytest.mark.anyio
    async def test_discover_empty_group(
        self, _patch_transport: None
    ) -> None:
        routes = {"/api/v4/groups/42/projects": (200, [])}
        workspace = _gitlab_workspace()
        mock = RoutingMockTransport(routes)
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert result.items == []
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_missing_namespace_fields(
        self, _patch_transport: None
    ) -> None:
        """Projects without namespace field should default gracefully."""
        routes = {
            "/api/v4/groups/42/projects": (
                200,
                [
                    {
                        "id": 200,
                        "path_with_namespace": "acme/legacy-app",
                        # no name_with_namespace, no web_url, no namespace
                    }
                ],
            ),
        }
        workspace = _gitlab_workspace()
        mock = RoutingMockTransport(routes)
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert len(result.items) == 1
        r = result.items[0]
        assert r.stable_ref == "200"
        assert r.display_name == "acme/legacy-app"
        assert r.connector_params["project_id"] == "200"
        assert r.connector_params["base_url"] == "https://gitlab.com/api/v4"
        assert r.routing_metadata["project_id"] == "200"
        assert r.routing_metadata["path_with_namespace"] == "acme/legacy-app"
        assert r.routing_metadata["web_url"] == ""
        assert r.routing_metadata["namespace_id"] == ""
        assert r.routing_metadata["namespace_path"] == ""

    @pytest.mark.anyio
    async def test_display_name_falls_back_to_path_with_namespace(
        self, _patch_transport: None
    ) -> None:
        """When name_with_namespace is absent, use path_with_namespace."""
        routes = {
            "/api/v4/groups/42/projects": (
                200,
                [
                    {
                        "id": 300,
                        "path_with_namespace": "acme/some-repo",
                        "web_url": "https://gitlab.com/acme/some-repo",
                    }
                ],
            ),
        }
        workspace = _gitlab_workspace()
        mock = RoutingMockTransport(routes)
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert result.items[0].display_name == "acme/some-repo"

    @pytest.mark.anyio
    async def test_pagination_multiple_pages(
        self, _patch_transport: None
    ) -> None:
        page1 = [
            {
                "id": i,
                "name_with_namespace": f"Project {i}",
                "path_with_namespace": f"acme/project-{i}",
                "web_url": f"https://gitlab.com/acme/project-{i}",
                "namespace": {"id": 42, "full_path": "acme"},
            }
            for i in range(_PER_PAGE)
        ]
        page2 = [
            {
                "id": _PER_PAGE,
                "name_with_namespace": "Last Project",
                "path_with_namespace": "acme/last-project",
                "web_url": "https://gitlab.com/acme/last-project",
                "namespace": {"id": 42, "full_path": "acme"},
            }
        ]
        mock = PageAwareMockTransport(
            "/api/v4/groups/42/projects", {1: page1, 2: page2}
        )
        workspace = _gitlab_workspace()
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert len(result.items) == _PER_PAGE + 1
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_truncation_at_page_limit(
        self, _patch_transport: None
    ) -> None:
        full_page = [
            {
                "id": i,
                "name_with_namespace": f"Project {i}",
                "path_with_namespace": f"acme/project-{i}",
                "web_url": f"https://gitlab.com/acme/project-{i}",
                "namespace": {"id": 42, "full_path": "acme"},
            }
            for i in range(_PER_PAGE)
        ]
        pages = {p: full_page for p in range(1, _MAX_PAGES + 1)}
        mock = PageAwareMockTransport(
            "/api/v4/groups/42/projects", pages
        )
        workspace = _gitlab_workspace()
        discoverer = _make_resource_discoverer(mock)
        result = await discoverer.discover(workspace)

        assert len(result.items) == _PER_PAGE * _MAX_PAGES
        assert result.truncated is True


# ---------------------------------------------------------------------------
# Registration Tests
# ---------------------------------------------------------------------------


class TestGitLabRegistration:
    def test_workspace_discoverer_registered(self) -> None:
        factory = get_workspace_discoverer("gitlab")
        assert factory is GitLabWorkspaceDiscovery

    def test_resource_discoverer_registered(self) -> None:
        factory = get_resource_discoverer("gitlab")
        assert factory is GitLabResourceDiscovery

    def test_factory_returns_discoverer(self) -> None:
        ctx = _make_context()
        workspace_disc = get_workspace_discoverer("gitlab")(ctx)
        assert isinstance(workspace_disc, GitLabWorkspaceDiscovery)

        resource_disc = get_resource_discoverer("gitlab")(ctx)
        assert isinstance(resource_disc, GitLabResourceDiscovery)
