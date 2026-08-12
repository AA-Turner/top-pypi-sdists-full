"""Live test of the Streamable HTTP MCP client against a real MCP server.

Unlike ``test_mcp_header_mapping.py`` (which mocks the client to assert the
credential/wire contract), this drives the SDK's ``collect_mcp_tools`` /
``execute_mcp_tool`` against a *real* MCP server: the ``hello_mcp`` fixture
(conftest) spawns a minimal FastMCP "hello world" server in pure Python (no npx)
on a localhost port. It proves the Streamable HTTP client can actually connect to
an MCP, list its tools, and call one, the path a workflow uses to talk to an
external MCP directly (without a connector).

Self-contained: no Docker, no network egress, no external services, everything is
localhost. Skips if the ``mcp`` server extra (FastMCP) is unavailable.
"""

import pytest

pytest.importorskip("mcp.server.fastmcp", reason="FastMCP (mcp server extra) not installed")

from conftest import HelloMcp  # noqa: E402

from mistralai.workflows.plugins.mistralai.mcp import (  # noqa: E402
    CollectMCPToolsParams,
    ExecuteMCPToolParams,
    MCPStreamableHTTPConfig,
    collect_mcp_tools,
    collect_tools_streamable_http,
    execute_mcp_tool,
)


@pytest.mark.asyncio
async def test_collect_and_execute_against_a_real_local_mcp(hello_mcp: HelloMcp) -> None:
    """The client connects to the real MCP, lists `hello`, and calls it."""
    config = MCPStreamableHTTPConfig(url=hello_mcp.url, name="hello")

    collected = await collect_mcp_tools(CollectMCPToolsParams(configs=[config]))
    names = [t["function"]["name"] for t in collected.tools]
    assert "hello_hello" in names  # prefixed with the config name
    assert collected.tool_to_config_map.get("hello_hello") == 0

    executed = await execute_mcp_tool(
        ExecuteMCPToolParams(
            configs=[config],
            tool_name="hello_hello",
            tool_arguments={},
            config_index=0,
        )
    )
    assert executed.result == hello_mcp.reply


@pytest.mark.asyncio
async def test_collect_tools_helper_against_a_real_local_mcp(hello_mcp: HelloMcp) -> None:
    """The per-call helper opens, lists, and closes the client cleanly (no pooling)."""
    config = MCPStreamableHTTPConfig(url=hello_mcp.url, name="hello")
    tools = await collect_tools_streamable_http(config)
    assert [t["function"]["name"] for t in tools] == ["hello"]
