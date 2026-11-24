"""The matrx-scraper stdio MCP server answers ``tools/list`` and ``tools/call`` through the real mcp 2 SDK.

mcp 2 removed the low-level ``@server.list_tools()`` / ``@server.call_tool()`` decorators and stopped
auto-wrapping handler return values, so ``build_server`` registers ``on_list_tools`` / ``on_call_tool``
handlers that return typed results. Driven here through the SDK's in-memory ``Client`` — the same
dispatch a stdio client reaches — so a handler that returns the wrong shape goes red.
"""

from __future__ import annotations

import json

import pytest
from mcp import Client

from matrx_scraper.ai_tools import ToolSpec
from matrx_scraper.mcp.server import build_server


async def _echo(arguments: dict) -> dict:
    return {"success": True, "echo": arguments}


async def _crash(_arguments: dict) -> dict:
    raise ValueError("boom")


_SPECS = [
    ToolSpec(
        name="echo",
        description="Echo the arguments.",
        input_schema={"type": "object", "properties": {"x": {"type": "string"}}},
        handler=_echo,
        group="scrape",
    ),
    ToolSpec(
        name="crash",
        description="Always raises.",
        input_schema={"type": "object", "properties": {}},
        handler=_crash,
        group="scrape",
    ),
]


@pytest.mark.asyncio
async def test_list_and_call_round_trip_over_the_sdk() -> None:
    server = build_server(_SPECS)
    assert server is not None
    async with Client(server) as client:
        listed = await client.list_tools()
        assert [(t.name, t.input_schema) for t in listed.tools] == [
            (s.name, s.input_schema) for s in _SPECS
        ]

        ok = await client.call_tool("echo", {"x": "hi"})
        assert ok.is_error is False
        assert json.loads(ok.content[0].text) == {"success": True, "echo": {"x": "hi"}}

        crashed = await client.call_tool("crash", {})
        body = json.loads(crashed.content[0].text)
        assert body["error_type"] == "handler_crash" and "ValueError: boom" in body["error_message"]

        unknown = await client.call_tool("nope", {})
        assert unknown.is_error is True
        assert "unknown tool: nope" in unknown.content[0].text
