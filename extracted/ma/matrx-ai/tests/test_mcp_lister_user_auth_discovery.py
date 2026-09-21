"""An MCP-managed bundle lister must discover with the CALLING USER's
connection and resolve the server's live members — or say plainly it has none.

Live break (2026-09-13, GitHub MCP): ``sync_server`` discovered with
server-level auth only (``None`` for every OAuth server), GitHub answered 401
to the anonymous ``tools/list``, ``last_synced_at`` stayed NULL and the
catalog stayed empty — while the same ``tools/list`` with the user's bearer
returned 47 tools. On top of that the lister resolved members through a
``platform.associations`` edge the catalog sync never writes, so EVERY MCP
bundle listed 0 members even when its server had synced.

Forcing functions:
  1. ``sync_server(..., discovery_auth=X)`` hands X to ``discover_tools``;
     without it the server-level auth (None here) is used.
  2. the lister, for a bundle with ``metadata.server_slug``, passes the
     host's ``mcp_auth_resolver`` result into the sync and loads the server's
     ``managed_by_server_id`` definitions as members.
  3. a server that produced zero members returns ``success=False`` with the
     sync error in the message — never a successful empty listing.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.tools import mcp_sync
from matrx_ai.tools.implementations import bundle_lister
from matrx_ai.tools.mcp_sync import SyncResult
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry

SERVER_ID = "c72aec9e-7468-4cf5-83be-32ccd5703faa"
USER_ID = "00000000-0000-4000-8000-0000000fffe1"
GITHUB_TOOLS = ("mcp.github.create_branch", "mcp.github.get_file_contents")


def _server_row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": SERVER_ID,
        "slug": "github",
        "transport": "http",
        "endpoint_url": "https://api.githubcopilot.com/mcp/",
        "auth_strategy": "oauth_discovery",
        "last_synced_at": None,
        "discovery_ttl_seconds": 18000,
    }
    row.update(overrides)
    return row


# ---------------------------------------------------------------------------
# 1. sync_server carries the caller's discovery auth to tools/list
# ---------------------------------------------------------------------------


async def test_sync_server_discovers_with_caller_auth(monkeypatch):
    seen_auth: list[Any] = []

    async def fake_fetch(slug: str):
        return _server_row(slug=slug)

    async def fake_discover(self, url, auth=None, **kwargs):
        seen_auth.append(auth)
        return []

    async def fake_register(server_id, specs):
        return {"inserted": [], "updated": [], "deactivated": []}

    async def fake_stamp(slug: str):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_register_mcp_discovered", fake_register)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    await mcp_sync.sync_server("github", force=True, discovery_auth={"bearer": "u-token"})
    await mcp_sync.sync_server("github", force=True)

    assert seen_auth == [{"bearer": "u-token"}, None]


# ---------------------------------------------------------------------------
# 2 + 3. the lister: user auth in, live members out, honest when empty
# ---------------------------------------------------------------------------


class _Row:
    def __init__(self, **fields: Any) -> None:
        self.__dict__.update(fields)


class _ServerManager:
    async def filter_items(self, **kwargs: Any):
        return [_Row(id=SERVER_ID, slug="github")] if kwargs.get("slug") == "github" else []


class _DefinitionQuery:
    def __init__(self, names: tuple[str, ...]) -> None:
        self._names = names

    async def all(self):
        return [_Row(name=n) for n in self._names]


class _DefinitionModel:
    def __init__(self, names: tuple[str, ...]) -> None:
        self.names = names
        self.filters: list[dict[str, Any]] = []

    def filter(self, **kwargs: Any):
        self.filters.append(kwargs)
        return _DefinitionQuery(self.names if kwargs.get("managed_by_server_id") == SERVER_ID else ())


@pytest.fixture
def github_members_in_registry():
    registry = ToolRegistry.get_instance()
    saved = {name: registry._tools.get(name) for name in GITHUB_TOOLS}
    for index, name in enumerate(GITHUB_TOOLS):
        registry._tools[name] = ToolDefinition(
            name=name,
            description=name,
            parameters={},
            tool_type=ToolType.EXTERNAL_MCP,
            tool_id=f"00000000-0000-4000-8000-0000000000a{index}",
        )
    try:
        yield
    finally:
        for name, tool in saved.items():
            if tool is None:
                registry._tools.pop(name, None)
            else:
                registry._tools[name] = tool


@pytest.fixture
def lister_host(monkeypatch):
    """Host seams the lister reaches: bundle row, server manager, definition
    model, the auth resolver ext, and an app context carrying the user."""
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    definition_model = _DefinitionModel(GITHUB_TOOLS)

    async def fake_bundle(name: str):
        return {"id": "b-1", "name": name, "metadata": {"server_slug": "github", "auto_managed": True}}

    def fake_get_instance(key: str):
        if key == "tool_mcp_server_manager_instance":
            return _ServerManager()
        raise KeyError(key)

    def fake_get_model(key: str):
        if key == "ToolDefinition":
            return definition_model
        raise KeyError(key)

    resolver_calls: list[tuple[str, str]] = []

    async def fake_resolver(slug: str, user_id: str):
        resolver_calls.append((slug, user_id))
        return {"bearer": "u-token"}

    monkeypatch.setattr(bundle_lister, "_fetch_bundle_by_name", fake_bundle)
    import matrx_ai.db._registry as db_registry

    monkeypatch.setattr(db_registry, "get_instance", fake_get_instance)
    monkeypatch.setattr(db_registry, "get_model", fake_get_model)
    saved_ext = dict(_ext._registry)
    _ext._registry["mcp_auth_resolver"] = fake_resolver

    class _NullEmitter:
        async def send_chunk(self, *_a, **_kw): ...
        async def send_reasoning_chunk(self, *_a, **_kw): ...
        async def send_data(self, *_a, **_kw): ...
        async def send_phase(self, *_a, **_kw): ...
        async def send_warning(self, *_a, **_kw): ...
        async def send_error(self, *_a, **_kw): ...
        async def send_tool_event(self, *_a, **_kw): ...
        async def fatal_error(self, *_a, **_kw): ...
        async def send_end(self, *_a, **_kw): ...

    ctx = AppContext(emitter=_NullEmitter(), is_authenticated=True, user_id=USER_ID, metadata={})
    token = set_app_context(ctx)
    try:
        yield {"resolver_calls": resolver_calls, "definition_model": definition_model}
    finally:
        clear_app_context(token)
        _ext._registry.clear()
        _ext._registry.update(saved_ext)


async def test_lister_discovers_as_the_user_and_loads_live_members(
    monkeypatch, lister_host, github_members_in_registry
):
    sync_calls: list[dict[str, Any]] = []

    async def fake_sync(slug: str, *, force: bool = False, discovery_auth=None):
        sync_calls.append({"slug": slug, "force": force, "discovery_auth": discovery_auth})
        return SyncResult(slug=slug, inserted=list(GITHUB_TOOLS))

    monkeypatch.setattr(mcp_sync, "sync_server", fake_sync)

    ctx = ToolContext(call_id="c-1", tool_name="bundle:list_github")
    result = await bundle_lister.list_bundle_tools({}, ctx)

    assert lister_host["resolver_calls"] == [("github", USER_ID)]
    assert sync_calls == [{"slug": "github", "force": False, "discovery_auth": {"bearer": "u-token"}}]
    assert result.success is True, result.error
    assert result.output["tools_loaded"] == sorted(GITHUB_TOOLS)
    assert result.output["count"] == len(GITHUB_TOOLS)
    # Members came from the server's managed definitions, not an edge walk.
    assert lister_host["definition_model"].filters == [
        {"managed_by_server_id": SERVER_ID, "is_active": True}
    ]


async def test_lister_with_no_members_fails_loudly_with_the_sync_reason(monkeypatch, lister_host):
    lister_host["definition_model"].names = ()

    async def fake_sync(slug: str, *, force: bool = False, discovery_auth=None):
        return SyncResult(
            slug=slug,
            error="discover_tools failed: HTTPStatusError(\"Client error '401 Unauthorized'\")",
            upstream_status=401,
        )

    monkeypatch.setattr(mcp_sync, "sync_server", fake_sync)

    ctx = ToolContext(call_id="c-2", tool_name="bundle:list_github")
    result = await bundle_lister.list_bundle_tools({}, ctx)

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "mcp_no_tools"
    assert "401 Unauthorized" in result.error.message
    assert "produced no tools" in result.error.message
