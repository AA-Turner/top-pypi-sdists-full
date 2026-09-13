"""mcp_sync contract tests — transport gate + catalog-drift reconciliation.

The external-MCP client speaks JSON-RPC over plain HTTP POST only, so a
``tool.mcp_server`` row declaring ``sse``/``stdio`` must be REJECTED loudly at
sync time (clear error naming the transport) instead of failing opaquely at
discovery time. And the sync report must carry the REAL per-tool delta —
derived by diffing the managed ``tool.definition`` rows around the RPC —
never the historical always-empty lists.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest
from matrx_orm import (
    configure_session_context,
    current_actor,
    declared_actor,
    declared_actor_gucs,
)

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


class _RecordingConnection:
    """Minimal driver boundary: transaction + session GUCs + RPC are observable."""

    def __init__(self, *, fetchval_error: Exception | None = None) -> None:
        self.calls: list[tuple[str, str, tuple[Any, ...]]] = []
        self.fetchval_error = fetchval_error

    async def execute(self, sql: str, *args: Any, **_kwargs: Any) -> None:
        self.calls.append(("execute", sql, args))

    async def fetchval(self, sql: str, *args: Any, **_kwargs: Any) -> int:
        self.calls.append(("fetchval", sql, args))
        if self.fetchval_error is not None:
            raise self.fetchval_error
        return 1


class _RecordingAdapter:
    def __init__(self, connection: _RecordingConnection) -> None:
        self.connection = connection

    @asynccontextmanager
    async def get_connection(self, timeout: float = 10.0):
        yield self.connection


@pytest.fixture
def recording_connection(monkeypatch):
    """Record both real transaction and bare call_function connection leases."""
    from matrx_orm.adapters import AdapterRegistry
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager
    from matrx_orm.core import session_context

    connection = _RecordingConnection()
    adapter = _RecordingAdapter(connection)
    old_provider = session_context._provider
    configure_session_context(declared_actor_gucs)
    monkeypatch.setattr(AdapterRegistry, "get", lambda _database: adapter)
    monkeypatch.setattr(
        AsyncDatabaseManager,
        "get_connection",
        classmethod(lambda _cls, _database, timeout=10.0: adapter.get_connection(timeout)),
    )
    monkeypatch.setattr(
        "matrx_orm.core.config.get_all_database_project_names", lambda: ["test"]
    )
    try:
        yield connection
    finally:
        configure_session_context(old_provider)


def _rpc_call_index(connection: _RecordingConnection) -> int:
    rpc_index = next(
        (
            index
            for index, (method, sql, _args) in enumerate(connection.calls)
            if method == "fetchval" and '"tool_register_mcp_discovered"' in sql
        ),
        None,
    )
    assert rpc_index is not None, "catalog reconciliation must call its registration RPC"
    return rpc_index


def _assert_rpc_has_named_actor_gucs(connection: _RecordingConnection) -> int:
    rpc_index = _rpc_call_index(connection)
    assert connection.calls[rpc_index - 2 : rpc_index] == [
        ("execute", "SELECT set_config($1, $2, true)", ("app.actor_tier", "code")),
        ("execute", "SELECT set_config($1, $2, true)", ("app.actor_system", "mcp_sync")),
    ], (
        "catalog reconciliation RPC must be preceded by named actor GUCs on the "
        "same connection"
    )
    return rpc_index


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


async def test_catalog_reconciliation_sets_named_actor_gucs_on_its_rpc_connection(
    monkeypatch, recording_connection
):
    """Discovery is outside the transaction; reconciliation is not."""
    discovery_observed_calls: list[tuple[str, str, tuple[Any, ...]]] = []

    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        discovery_observed_calls.extend(recording_connection.calls)
        return []

    async def fake_snapshot(server_id: str):
        return None

    async def fake_stamp(slug: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    result = await mcp_sync.sync_server("public-docs", force=True)

    assert result.error is None
    assert discovery_observed_calls == []
    rpc_index = _assert_rpc_has_named_actor_gucs(recording_connection)
    assert recording_connection.calls == [
        ("execute", "BEGIN", ()),
        ("execute", "SELECT set_config($1, $2, true)", ("app.actor_tier", "code")),
        ("execute", "SELECT set_config($1, $2, true)", ("app.actor_system", "mcp_sync")),
        recording_connection.calls[rpc_index],
        ("execute", "COMMIT", ()),
    ]
    method, sql, args = recording_connection.calls[rpc_index]
    assert method == "fetchval"
    assert sql == 'SELECT "public"."tool_register_mcp_discovered"($1, $2::jsonb)'
    assert args == ("6a1f0000-0000-0000-0000-000000000001", "[]")


async def test_catalog_reconciliation_rolls_back_when_rpc_fails(
    monkeypatch, recording_connection
):
    recording_connection.fetchval_error = RuntimeError("catalog RPC refused")

    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        return []

    async def fake_snapshot(server_id: str):
        return None

    async def fake_record(slug: str, error: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)
    monkeypatch.setattr(mcp_sync, "_record_sync_error", fake_record)

    result = await mcp_sync.sync_server("public-docs", force=True)

    assert "catalog RPC refused" in (result.error or "")
    assert _assert_rpc_has_named_actor_gucs(recording_connection) == 3
    assert recording_connection.calls[-1] == ("execute", "ROLLBACK", ())
    assert ("execute", "COMMIT", ()) not in recording_connection.calls


async def test_catalog_reconciliation_restores_outer_actor_declaration(
    monkeypatch, recording_connection
):
    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        return []

    async def fake_snapshot(server_id: str):
        return None

    async def fake_stamp(slug: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    async with declared_actor("human", "outer"):
        result = await mcp_sync.sync_server("public-docs", force=True)
        assert result.error is None
        assert current_actor() is not None
        assert current_actor().tier == "human"
        assert current_actor().system == "outer"
        assert declared_actor_gucs() == {
            "app.actor_tier": "human",
            "app.actor_system": "outer",
        }

    assert current_actor() is None
    assert recording_connection.calls[2] == (
        "execute",
        "SELECT set_config($1, $2, true)",
        ("app.actor_system", "mcp_sync"),
    )


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


async def test_register_reports_real_delta_from_row_diff(monkeypatch, recording_connection):
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

    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)

    delta = await mcp_sync._register_mcp_discovered("server-1", [])

    assert _rpc_call_index(recording_connection) == 1
    assert delta["inserted"] == ["mcp.asana.new_tool"]
    assert delta["updated"] == ["mcp.asana.changed_tool"]
    assert delta["deactivated"] == ["mcp.asana.old_tool"]


async def test_register_degrades_to_empty_delta_without_model(monkeypatch, recording_connection):
    async def fake_snapshot(server_id: str):
        return None

    monkeypatch.setattr(mcp_sync, "_snapshot_managed_tools", fake_snapshot)

    delta = await mcp_sync._register_mcp_discovered("server-1", [])

    assert _rpc_call_index(recording_connection) == 1
    assert delta == {"inserted": [], "updated": [], "deactivated": []}
