"""Tests for ExternalMCPClient namespace handling.

The namespace separator in canonical tool names was migrated from single-`_`
to `:` in Step 4 of the redesign. The remote MCP server is invoked with
the local segment only (after the prefix), since our namespace is our
identifier — not the server's.
"""

from __future__ import annotations

from types import SimpleNamespace

import httpx
import pytest

from matrx_ai import _ext
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.external_mcp import ExternalMCPClient
from matrx_ai.tools.models import ToolDefinition, ToolType


class TestStripNamespace:
    def test_database_discovered_mcp_name(self) -> None:
        assert (
            ExternalMCPClient._strip_namespace("mcp.docker-hub.getRepositoryTag")
            == "getRepositoryTag"
        )

    def test_canonical_colon_separator(self) -> None:
        """Post-redesign canonical: `<slug>:<local>` → strip to local."""
        assert ExternalMCPClient._strip_namespace("supabase:list_projects") == "list_projects"
        assert (
            ExternalMCPClient._strip_namespace("matrx-extend:take_screenshot") == "take_screenshot"
        )

    def test_local_name_with_underscores_preserved(self) -> None:
        """Local segment may contain underscores (commonly does); split
        on FIRST colon to preserve them."""
        assert (
            ExternalMCPClient._strip_namespace("linear:create_issue_with_attachment")
            == "create_issue_with_attachment"
        )

    def test_underscored_bare_names_are_never_stripped(self) -> None:
        """A name with no colon carries no namespace and must round-trip
        EXACTLY. The removed "legacy" underscore fallback corrupted every
        real remote tool name — these are DeepWiki's actual names (D128)."""
        assert ExternalMCPClient._strip_namespace("ask_question") == "ask_question"
        assert ExternalMCPClient._strip_namespace("read_wiki_contents") == "read_wiki_contents"
        assert ExternalMCPClient._strip_namespace("legacy_tool_name") == "legacy_tool_name"

    def test_no_separator_returns_input(self) -> None:
        """Bare names (no namespace) round-trip unchanged."""
        assert ExternalMCPClient._strip_namespace("simple_name") == "simple_name"
        assert ExternalMCPClient._strip_namespace("simplename") == "simplename"


@pytest.mark.asyncio
async def test_shopify_ucp_discovery_skips_initialize_and_supplies_agent_profile(
    monkeypatch,
) -> None:
    requests = []

    async def _post(self, url, *, json, headers):
        requests.append({"payload": json, "headers": headers})
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={"jsonrpc": "2.0", "id": json["id"], "result": {"tools": []}},
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", _post)

    tools = await ExternalMCPClient().discover_tools(
        "https://catalog.shopify.com/api/ucp/mcp"
    )

    assert tools == []
    assert [request["payload"]["method"] for request in requests] == ["tools/list"]
    profile = requests[0]["payload"]["params"]["arguments"]["meta"]["ucp-agent"][
        "profile"
    ]
    assert profile.startswith("https://shopify.dev/ucp/agent-profiles/")
    assert requests[0]["headers"]["User-Agent"] == (
        "AI-Matrx-MCP/1.0 (+https://www.aimatrx.com)"
    )


@pytest.mark.asyncio
async def test_ucp_user_agent_does_not_change_ordinary_mcp_headers(monkeypatch) -> None:
    client = ExternalMCPClient()
    captured_headers = []

    async def _handshake(http, url, headers):
        return None, "2025-06-18"

    async def _post(self, url, *, json, headers):
        captured_headers.append(headers)
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={"jsonrpc": "2.0", "id": json["id"], "result": {"tools": []}},
        )

    monkeypatch.setattr(client, "_handshake", _handshake)
    monkeypatch.setattr(httpx.AsyncClient, "post", _post)

    await client.discover_tools("https://ordinary.example/mcp")

    assert len(captured_headers) == 1
    assert "User-Agent" not in captured_headers[0]


def test_ucp_call_preserves_caller_meta_and_adds_profile() -> None:
    arguments = {
        "meta": {"request-id": "request-1"},
        "catalog": {"query": "headphones"},
    }

    enriched = ExternalMCPClient._request_arguments(
        "https://catalog.shopify.com/api/ucp/mcp", arguments
    )

    assert enriched["meta"]["request-id"] == "request-1"
    assert "ucp-agent" in enriched["meta"]
    assert arguments == {
        "meta": {"request-id": "request-1"},
        "catalog": {"query": "headphones"},
    }

    def test_double_colon_in_local_split_on_first(self) -> None:
        """If a local name contains `:` (rare but allowed), only the
        first colon is the namespace separator."""
        assert ExternalMCPClient._strip_namespace("ns:weird:tool") == "weird:tool"


@pytest.mark.asyncio
async def test_http_tool_call_preserves_structured_content_without_content_blocks(
    monkeypatch,
) -> None:
    client = ExternalMCPClient()

    async def _send(server_url, payload, auth):
        assert server_url == "https://catalog.example/mcp"
        assert payload["params"]["name"] == "search_catalog"
        assert auth is None
        return {
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": {
                "structuredContent": {
                    "products": [{"id": "product-1", "title": "Headphones"}],
                    "pagination": {"cursor": None},
                }
            },
        }

    monkeypatch.setattr(client, "_send", _send)
    tool_def = ToolDefinition(
        name="search_catalog",
        tool_type=ToolType.EXTERNAL_MCP,
        mcp_transport="http",
        mcp_server_url="https://catalog.example/mcp",
    )

    result = await client.call_tool(
        tool_def,
        {"catalog": {"query": "headphones"}},
        SimpleNamespace(call_id="structured-content-test"),
    )

    assert result.success is True
    assert result.error is None
    assert result.output is not None
    assert '"title": "Headphones"' in result.output
    assert result.output != "[]"


@pytest.mark.asyncio
async def test_executor_uses_resolved_scoped_endpoint_without_leaking_metadata(
    monkeypatch,
) -> None:
    endpoint = "https://mcp.supabase.com/mcp?project_ref=dev&read_only=true"

    async def _resolver(server_slug: str, user_id: str):
        assert server_slug == "supabase"
        assert user_id == "user-1"
        return {
            "bearer": "AT-live",
            "__matrx_mcp_endpoint_url": endpoint,
        }

    captured = {}

    async def _call_tool(self, tool_def, args, ctx):
        captured["url"] = tool_def.mcp_server_url
        captured["auth"] = tool_def.mcp_server_auth
        return "ok"

    monkeypatch.setitem(_ext._registry, "mcp_auth_resolver", _resolver)
    monkeypatch.setattr(ExternalMCPClient, "call_tool", _call_tool)

    executor = object.__new__(ToolExecutor)
    tool_def = ToolDefinition(
        name="mcp.supabase.list_tables",
        tool_type=ToolType.EXTERNAL_MCP,
        mcp_server_url="https://mcp.supabase.com/mcp",
    )
    ctx = SimpleNamespace(user_id="user-1")
    result = await executor._execute_external_mcp(tool_def, {}, ctx)

    assert result == "ok"
    assert captured == {"url": endpoint, "auth": {"bearer": "AT-live"}}


@pytest.mark.asyncio
async def test_catalog_allowlist_refuses_unregistered_remote_tool() -> None:
    client = ExternalMCPClient()
    tool_def = ToolDefinition(
        name="mcp.docker-hub.createRepository",
        tool_type=ToolType.EXTERNAL_MCP,
        mcp_transport="stdio",
        mcp_command="must-not-run",
        mcp_tool_allowlist=["search", "getRepositoryTag"],
    )
    ctx = SimpleNamespace(call_id="allowlist-test")

    result = await client.call_tool(tool_def, {}, ctx)

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "not_allowed"
    assert "createRepository" in result.error.message


@pytest.mark.asyncio
async def test_stdio_runtime_merges_vault_resolved_environment() -> None:
    client = ExternalMCPClient()
    tool_def = ToolDefinition(
        name="mcp.woocommerce.mcp-adapter-discover-abilities",
        tool_type=ToolType.EXTERNAL_MCP,
        mcp_transport="stdio",
        mcp_command="npx",
        mcp_args=["-y", "@automattic/mcp-wordpress-remote@0.4.0"],
        mcp_env={"OAUTH_ENABLED": "false"},
        mcp_server_auth={
            "env": {
                "WP_API_URL": "https://store.test/wp-json/mcp/mcp-adapter-default-server",
                "WP_API_USERNAME": "aimatrx_integration",
                "WP_API_PASSWORD": "sealed",
            }
        },
    )

    runtime = await client._resolve_runtime(tool_def)

    assert runtime.transport == "stdio"
    assert runtime.command == "npx"
    assert runtime.env == {
        "OAUTH_ENABLED": "false",
        "WP_API_URL": "https://store.test/wp-json/mcp/mcp-adapter-default-server",
        "WP_API_USERNAME": "aimatrx_integration",
        "WP_API_PASSWORD": "sealed",
    }
