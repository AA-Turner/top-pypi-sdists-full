"""Tests for Jira workspace and resource discovery providers."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx
import pytest

from spec_kitty_tracker.discovery.providers.jira import (
    JiraResourceDiscovery,
    JiraWorkspaceDiscovery,
)
from spec_kitty_tracker.discovery.registry import (
    _resource_discoverers,
    _workspace_discoverers,
    get_resource_discoverer,
    get_workspace_discoverer,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
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


class PaginatingMockTransport(httpx.AsyncBaseTransport):
    """Supports pagination by reading startAt query param."""

    def __init__(self, pages: list[dict[str, Any]]) -> None:
        self._pages = pages

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        start_at = int(request.url.params.get("startAt", "0"))
        max_results = int(request.url.params.get("maxResults", "50"))

        # Find the correct page based on startAt
        page_index = start_at // max_results
        if page_index < len(self._pages):
            body = self._pages[page_index]
        else:
            body = {"values": [], "isLast": True}

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
        provider_config_key="jira-test",
        nango_secret_key="sk-test",
    )


def _make_workspace(cloud_id: str = "cloud-abc") -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id=cloud_id,
        name="mysite",
        display="https://mysite.atlassian.net",
        kind="site",
        provider="jira",
        provider_context={"cloud_id": cloud_id},
    )


def _patch_transport(
    discoverer: JiraWorkspaceDiscovery | JiraResourceDiscovery,
    transport: httpx.AsyncBaseTransport,
) -> JiraWorkspaceDiscovery | JiraResourceDiscovery:
    """Replace the nango_ctx with one that will use the mock transport.

    Since the discoverer creates transport inside discover(), we
    monkey-patch the NangoProxyTransport constructor behaviour.
    """
    return discoverer


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------


class TestJiraRegistration:
    def test_workspace_discoverer_registered(self) -> None:
        assert get_workspace_discoverer("jira") is JiraWorkspaceDiscovery

    def test_resource_discoverer_registered(self) -> None:
        assert get_resource_discoverer("jira") is JiraResourceDiscovery


# ---------------------------------------------------------------------------
# Workspace discovery tests
# ---------------------------------------------------------------------------


class TestJiraWorkspaceDiscovery:
    @pytest.mark.anyio
    async def test_discover_single_site(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_sites = [
            {"id": "cloud-abc", "name": "My Site", "url": "https://mysite.atlassian.net"},
        ]
        mock_transport = RoutingMockTransport(
            {"/oauth/token/accessible-resources": (200, canned_sites)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraWorkspaceDiscovery(_make_context())
        result = await discoverer.discover()

        assert isinstance(result, DiscoveryResult)
        assert result.truncated is False
        assert len(result.items) == 1

        ws = result.items[0]
        assert ws.id == "cloud-abc"
        assert ws.name == "My Site"
        assert ws.display == "https://mysite.atlassian.net"
        assert ws.kind == "site"
        assert ws.provider == "jira"
        assert ws.provider_context == {
            "cloud_id": "cloud-abc",
            "site_url": "https://mysite.atlassian.net",
            "workspace_handle": "mysite",
            "workspace_url": "https://mysite.atlassian.net",
        }

    @pytest.mark.anyio
    async def test_discover_multiple_sites(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_sites = [
            {"id": "cloud-abc", "name": "Site A", "url": "https://a.atlassian.net"},
            {"id": "cloud-def", "name": "Site B", "url": "https://b.atlassian.net"},
            {"id": "cloud-ghi", "name": "Site C", "url": "https://c.atlassian.net"},
        ]
        mock_transport = RoutingMockTransport(
            {"/oauth/token/accessible-resources": (200, canned_sites)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraWorkspaceDiscovery(_make_context())
        result = await discoverer.discover()

        assert len(result.items) == 3
        assert result.items[0].id == "cloud-abc"
        assert result.items[1].id == "cloud-def"
        assert result.items[2].id == "cloud-ghi"

    @pytest.mark.anyio
    async def test_discover_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_transport = RoutingMockTransport(
            {"/oauth/token/accessible-resources": (200, [])}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraWorkspaceDiscovery(_make_context())
        result = await discoverer.discover()

        assert result.items == []
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_display_falls_back_to_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When site has no url field, display should fall back to name."""
        canned_sites = [
            {"id": "cloud-xyz", "name": "No URL Site"},
        ]
        mock_transport = RoutingMockTransport(
            {"/oauth/token/accessible-resources": (200, canned_sites)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraWorkspaceDiscovery(_make_context())
        result = await discoverer.discover()

        assert result.items[0].display == "No URL Site"


# ---------------------------------------------------------------------------
# Resource discovery tests
# ---------------------------------------------------------------------------


class TestJiraResourceDiscovery:
    @pytest.mark.anyio
    async def test_stable_ref_is_project_id_not_key(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """P1 CRITICAL: stable_ref MUST be str(project['id']), NOT project['key']."""
        canned_response = {
            "values": [
                {"id": "10001", "key": "PROJ", "name": "My Project"},
                {"id": "10002", "key": "ENG", "name": "Engineering"},
            ],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        assert len(result.items) == 2

        # CRITICAL: stable_ref is numeric ID, not key
        assert result.items[0].stable_ref == "10001"
        assert result.items[0].stable_ref != "PROJ"
        assert result.items[1].stable_ref == "10002"
        assert result.items[1].stable_ref != "ENG"

    @pytest.mark.anyio
    async def test_display_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_response = {
            "values": [
                {"id": "10001", "key": "PROJ", "name": "My Project"},
            ],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        assert result.items[0].display_name == "My Project"

    @pytest.mark.anyio
    async def test_connector_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_response = {
            "values": [
                {"id": "10001", "key": "PROJ", "name": "My Project"},
            ],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace("cloud-abc"))

        params = result.items[0].connector_params
        assert params["project_key"] == "PROJ"
        assert params["cloud_id"] == "cloud-abc"
        assert params["base_url"] == "https://api.atlassian.com/ex/jira/cloud-abc"

    @pytest.mark.anyio
    async def test_routing_metadata(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_response = {
            "values": [
                {"id": "10001", "key": "PROJ", "name": "My Project"},
            ],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        meta = result.items[0].routing_metadata
        assert meta["project_id"] == "10001"
        assert meta["project_key"] == "PROJ"
        assert meta["project_name"] == "My Project"

    @pytest.mark.anyio
    async def test_resource_fields(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_response = {
            "values": [
                {"id": "10001", "key": "PROJ", "name": "My Project"},
            ],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace("cloud-abc"))

        res = result.items[0]
        assert res.provider == "jira"
        assert res.parent_workspace_id == "cloud-abc"
        assert res.resource_type == "project"

    @pytest.mark.anyio
    async def test_empty_projects(self, monkeypatch: pytest.MonkeyPatch) -> None:
        canned_response = {"values": [], "isLast": True}
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        assert result.items == []
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_pagination_collects_all_pages(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Multi-page response should collect projects from all pages."""
        pages = [
            {
                "values": [{"id": "10001", "key": "P1", "name": "Project 1"}],
                "isLast": False,
            },
            {
                "values": [{"id": "10002", "key": "P2", "name": "Project 2"}],
                "isLast": False,
            },
            {
                "values": [{"id": "10003", "key": "P3", "name": "Project 3"}],
                "isLast": True,
            },
        ]
        mock_transport = PaginatingMockTransport(pages)
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        assert len(result.items) == 3
        assert result.items[0].stable_ref == "10001"
        assert result.items[1].stable_ref == "10002"
        assert result.items[2].stable_ref == "10003"
        assert result.truncated is False

    @pytest.mark.anyio
    async def test_pagination_truncation_at_max_pages(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When pagination hits the 20-page limit, truncated must be True."""
        # Build 20 pages, none of which say isLast=True
        pages = [
            {
                "values": [{"id": str(10000 + i), "key": f"P{i}", "name": f"Project {i}"}],
                "isLast": False,
            }
            for i in range(21)  # 21 pages available, but we cap at 20
        ]
        mock_transport = PaginatingMockTransport(pages)
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )
        # Also patch the max pages constant to confirm truncation
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira._MAX_PAGES", 20
        )

        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(_make_workspace())

        assert len(result.items) == 20
        assert result.truncated is True

    @pytest.mark.anyio
    async def test_cloud_id_from_workspace_context(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """cloud_id in connector_params comes from workspace.provider_context."""
        canned_response = {
            "values": [{"id": "10001", "key": "X", "name": "X Project"}],
            "isLast": True,
        }
        mock_transport = RoutingMockTransport(
            {"/rest/api/3/project/search": (200, canned_response)}
        )
        monkeypatch.setattr(
            "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
            lambda ctx: mock_transport,
        )

        workspace = _make_workspace("cloud-custom-id")
        discoverer = JiraResourceDiscovery(_make_context())
        result = await discoverer.discover(workspace)

        assert result.items[0].connector_params["cloud_id"] == "cloud-custom-id"
        assert "cloud-custom-id" in result.items[0].connector_params["base_url"]
