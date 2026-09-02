"""mcp_sync contract tests — transport gate + catalog-drift reconciliation.

The external-MCP client speaks JSON-RPC over plain HTTP POST only, so a
``tool.mcp_server`` row declaring ``sse``/``stdio`` must be REJECTED loudly at
sync time (clear error naming the transport) instead of failing opaquely at
discovery time. And the sync report must carry the REAL per-tool delta —
derived by diffing the managed ``tool.definition`` rows around the RPC —
never the historical always-empty lists.
"""
from __future__ import annotations

from typing import Any

import httpx
import pytest

from matrx_ai.tools import mcp_sync
from matrx_ai.tools.models import ToolDefinition


def _server_row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": "6a1f0000-0000-0000-0000-000000000001",
        "slug": "asana",
        "transport": "http",
        "endpoint_url": "https://mcp.example.com/rpc",
        "auth_strategy": "none",
        "last_synced_at": None,
        "discovery_ttl_seconds": 60,
    }
    row.update(overrides)
    return row


@pytest.mark.parametrize("transport", ["sse"])
async def test_unsupported_transport_rejected_loudly(monkeypatch, transport):
    errors: list[tuple[str, str]] = []

    async def fake_fetch(slug: str):
        return _server_row(slug=slug, transport=transport)

    async def fake_record(slug: str, error: str):
        errors.append((slug, error))

    async def must_not_discover(self, *a, **k):  # pragma: no cover - guard
        raise AssertionError("discover_tools must not run for an unsupported transport")

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync, "_record_sync_error", fake_record)
    monkeypatch.setattr(
        mcp_sync.ExternalMCPClient, "discover_tools", must_not_discover
    )

    result = await mcp_sync.sync_server("asana", force=True)

    assert result.error is not None
    assert transport in result.error
    assert "transport" in result.error
    assert "ExternalMCPClient" in result.error
    # The rejection is persisted on the server row, not just returned.
    assert errors and errors[0][0] == "asana"
    assert transport in errors[0][1]


async def test_http_transport_passes_the_gate(monkeypatch):
    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        return []

    async def fake_register(server_id, specs):
        return {"inserted": [], "updated": [], "deactivated": []}

    async def fake_stamp(slug: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_register_mcp_discovered", fake_register)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    result = await mcp_sync.sync_server("asana", force=True)

    assert result.error is None


async def test_remote_auth_rejection_preserves_upstream_status(monkeypatch):
    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        request = httpx.Request("POST", url)
        response = httpx.Response(401, request=request)
        raise httpx.HTTPStatusError("unauthorized", request=request, response=response)

    async def fake_record(slug: str, error: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync, "_record_sync_error", fake_record)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)

    result = await mcp_sync.sync_server("courtlistener", force=True)

    assert result.error is not None
    assert result.upstream_status == 401


async def test_stdio_uses_launch_recipe_and_filters_catalog_allowlist(monkeypatch):
    server = _server_row(
        slug="docker-hub",
        transport="stdio",
        endpoint_url=None,
        metadata={"tool_allowlist": ["search", "getRepositoryTag"]},
    )

    async def fake_fetch(slug: str):
        return server

    async def fake_config(server_id: str):
        return {"command": "node", "args": ["/opt/hub/dist/index.js", "--transport=stdio"]}

    async def fake_discover(self, url, auth=None, **kwargs):
        assert url is None
        assert kwargs == {
            "transport": "stdio",
            "command": "node",
            "args": ["/opt/hub/dist/index.js", "--transport=stdio"],
        }
        return [
            ToolDefinition(name="search"),
            ToolDefinition(name="createRepository"),
            ToolDefinition(name="getRepositoryTag"),
        ]

    captured = {}

    async def fake_register(server_id, specs):
        captured["specs"] = specs
        return {"inserted": [], "updated": [], "deactivated": []}

    async def fake_stamp(slug: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync, "_fetch_default_mcp_config", fake_config)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_register_mcp_discovered", fake_register)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    result = await mcp_sync.sync_server("docker-hub", force=True)

    assert result.error is None
    assert [spec["name"] for spec in captured["specs"]] == [
        "search",
        "getRepositoryTag",
    ]


async def test_register_reports_real_delta_from_row_diff(monkeypatch):
    before = {
        "mcp.asana.old_tool": {
            "is_active": True,
            "description": "old",
            "parameters": {},
            "output_schema": None,
        },
        "mcp.asana.changed_tool": {
            "is_active": True,
            "description": "old description",
            "parameters": {},
            "output_schema": None,
        },
        "mcp.asana.stable_tool": {
            "is_active": True,
            "description": "same",
            "parameters": {},
            "output_schema": None,
        },
    }
    after = {
        "mcp.asana.changed_tool": {
            "is_active": True,
            "description": "NEW description",
            "parameters": {},
            "output_schema": None,
        },
        "mcp.asana.stable_tool": {
            "is_active": True,
            "description": "same",
            "parameters": {},
            "output_schema": None,
        },
        "mcp.asana.old_tool": {
            "is_active": False,
            "description": "old",
            "parameters": {},
            "output_schema": None,
        },
        "mcp.asana.new_tool": {
            "is_active": True,
            "description": "brand new",
            "parameters": {},
            "output_schema": None,
        },
    }
    snapshots = [before, after]

    async def fake_snapshot(server_id: str):
        return snapshots.pop(0)

    called: dict[str, Any] = {}

    async def fake_call_function(database, schema, name, *args, **kwargs):
        called["rpc"] = (schema, name)
        return len(args)

    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)
    monkeypatch.setattr(
        "matrx_orm.core.config.get_all_database_project_names", lambda: ["main"]
    )
    import matrx_orm

    monkeypatch.setattr(matrx_orm, "call_function", fake_call_function)

    delta = await mcp_sync._register_mcp_discovered("server-1", [])

    assert called["rpc"] == ("public", "tool_register_mcp_discovered")
    assert delta["inserted"] == ["mcp.asana.new_tool"]
    assert delta["updated"] == ["mcp.asana.changed_tool"]
    assert delta["deactivated"] == ["mcp.asana.old_tool"]


async def test_register_degrades_to_empty_delta_without_model(monkeypatch):
    async def fake_snapshot(server_id: str):
        return None

    async def fake_call_function(database, schema, name, *args, **kwargs):
        return 0

    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)
    monkeypatch.setattr(
        "matrx_orm.core.config.get_all_database_project_names", lambda: ["main"]
    )
    import matrx_orm

    monkeypatch.setattr(matrx_orm, "call_function", fake_call_function)

    delta = await mcp_sync._register_mcp_discovered("server-1", [])

    assert delta == {"inserted": [], "updated": [], "deactivated": []}
