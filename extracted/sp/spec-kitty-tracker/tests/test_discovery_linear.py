"""Tests for Linear workspace and resource discovery."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any
from unittest.mock import patch

import httpx
import pytest

from spec_kitty_tracker.discovery.providers.linear import (
    LinearResourceDiscovery,
    LinearWorkspaceDiscovery,
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


def _make_context() -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id="conn-1",
        provider_config_key="linear-test",
        nango_secret_key="sk-test",
    )


# Canned API responses

ORGANIZATION_RESPONSE: dict[str, Any] = {
    "data": {
        "organization": {
            "id": "org-uuid-1",
            "name": "Acme Engineering",
            "urlKey": "acme-eng",
        }
    }
}

TEAMS_RESPONSE: dict[str, Any] = {
    "data": {
        "teams": {
            "nodes": [
                {"id": "team-uuid-1", "key": "ENG", "name": "Engineering"},
                {"id": "team-uuid-2", "key": "DES", "name": "Design"},
                {"id": "team-uuid-3", "key": "OPS", "name": "Operations"},
            ]
        }
    }
}


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    """Snapshot, clear, and restore the global registries around each test."""
    saved_workspace = dict(_workspace_discoverers)
    saved_resource = dict(_resource_discoverers)
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    yield
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    _workspace_discoverers.update(saved_workspace)
    _resource_discoverers.update(saved_resource)


def _make_workspace() -> DiscoveredWorkspace:
    """Build a sample workspace matching the ORGANIZATION_RESPONSE fixture."""
    return DiscoveredWorkspace(
        id="org-uuid-1",
        name="acme-eng",
        display="Acme Engineering",
        kind="workspace",
        provider="linear",
        provider_context={"org_id": "org-uuid-1", "url_key": "acme-eng"},
    )


# ---------------------------------------------------------------------------
# Workspace discovery tests
# ---------------------------------------------------------------------------


class TestLinearWorkspaceDiscovery:
    async def test_discover_returns_single_workspace(self) -> None:
        mock = RoutingMockTransport({"/graphql": (200, ORGANIZATION_RESPONSE)})
        discoverer = LinearWorkspaceDiscovery(_make_context())

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover()

        assert len(result.items) == 1
        assert result.truncated is False

        ws = result.items[0]
        assert ws.id == "org-uuid-1"
        assert ws.name == "acme-eng"
        assert ws.display == "Acme Engineering"
        assert ws.kind == "workspace"
        assert ws.provider == "linear"

    async def test_workspace_provider_context_matches_data_model(self) -> None:
        """T013: provider_context shape matches data-model.md."""
        mock = RoutingMockTransport({"/graphql": (200, ORGANIZATION_RESPONSE)})
        discoverer = LinearWorkspaceDiscovery(_make_context())

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover()

        ws = result.items[0]
        assert ws.provider_context == {
            "org_id": "org-uuid-1",
            "url_key": "acme-eng",
            "workspace_handle": "acme-eng",
            "workspace_url": "https://linear.app/acme-eng",
        }

    async def test_workspace_provider_context_json_serializable(self) -> None:
        """T013: provider_context must round-trip through JSON."""
        mock = RoutingMockTransport({"/graphql": (200, ORGANIZATION_RESPONSE)})
        discoverer = LinearWorkspaceDiscovery(_make_context())

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover()

        ws = result.items[0]
        serialized = json.dumps(ws.provider_context)
        assert json.loads(serialized) == ws.provider_context

    async def test_workspace_is_not_truncated(self) -> None:
        """Linear returns a single org — truncated must be False."""
        mock = RoutingMockTransport({"/graphql": (200, ORGANIZATION_RESPONSE)})
        discoverer = LinearWorkspaceDiscovery(_make_context())

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover()

        assert result.truncated is False


# ---------------------------------------------------------------------------
# Resource discovery tests
# ---------------------------------------------------------------------------


class TestLinearResourceDiscovery:
    async def test_discover_returns_all_teams(self) -> None:
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        assert len(result.items) == 3
        assert result.truncated is False

    async def test_team_stable_ref_is_team_id(self) -> None:
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        eng = result.items[0]
        assert eng.stable_ref == "team-uuid-1"
        assert eng.display_name == "Engineering"

    async def test_resource_fields(self) -> None:
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        for res in result.items:
            assert res.provider == "linear"
            assert res.parent_workspace_id == "org-uuid-1"
            assert res.resource_type == "team"

    async def test_connector_params_shape(self) -> None:
        """T013: connector_params matches data-model.md contract."""
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        for res in result.items:
            assert res.connector_params == {"team_id": res.stable_ref}

    async def test_routing_metadata_keys(self) -> None:
        """T013: routing_metadata keys match data-model.md contract."""
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        for res in result.items:
            assert set(res.routing_metadata.keys()) == {
                "team_key",
                "team_name",
                "url_key",
                "display_key",
                "resource_url",
            }

    async def test_routing_metadata_values(self) -> None:
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        eng = result.items[0]
        assert eng.routing_metadata == {
            "team_key": "ENG",
            "team_name": "Engineering",
            "url_key": "acme-eng",
            "display_key": "ENG",
            "resource_url": "https://linear.app/acme-eng/team/ENG",
        }

        des = result.items[1]
        assert des.routing_metadata == {
            "team_key": "DES",
            "team_name": "Design",
            "url_key": "acme-eng",
            "display_key": "DES",
            "resource_url": "https://linear.app/acme-eng/team/DES",
        }

    async def test_all_dict_fields_json_serializable(self) -> None:
        """T013: All dict fields must be JSON-serializable."""
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        for res in result.items:
            cp = json.dumps(res.connector_params)
            assert json.loads(cp) == res.connector_params
            rm = json.dumps(res.routing_metadata)
            assert json.loads(rm) == res.routing_metadata

    async def test_resources_not_truncated(self) -> None:
        """Linear returns all teams in single query — truncated must be False."""
        mock = RoutingMockTransport({"/graphql": (200, TEAMS_RESPONSE)})
        discoverer = LinearResourceDiscovery(_make_context())
        workspace = _make_workspace()

        with patch(
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport",
            return_value=mock,
        ):
            result = await discoverer.discover(workspace)

        assert result.truncated is False


# ---------------------------------------------------------------------------
# Registration tests
# ---------------------------------------------------------------------------


class TestLinearRegistration:
    def test_workspace_discoverer_registered(self) -> None:
        from spec_kitty_tracker.discovery.registry import register_workspace_discoverer

        register_workspace_discoverer("linear", LinearWorkspaceDiscovery)
        factory = get_workspace_discoverer("linear")
        assert factory is LinearWorkspaceDiscovery

    def test_resource_discoverer_registered(self) -> None:
        from spec_kitty_tracker.discovery.registry import register_resource_discoverer

        register_resource_discoverer("linear", LinearResourceDiscovery)
        factory = get_resource_discoverer("linear")
        assert factory is LinearResourceDiscovery

    def test_factory_creates_discoverer_with_context(self) -> None:
        from spec_kitty_tracker.discovery.registry import register_workspace_discoverer

        register_workspace_discoverer("linear", LinearWorkspaceDiscovery)
        factory = get_workspace_discoverer("linear")
        ctx = _make_context()
        discoverer = factory(ctx)
        assert isinstance(discoverer, LinearWorkspaceDiscovery)
