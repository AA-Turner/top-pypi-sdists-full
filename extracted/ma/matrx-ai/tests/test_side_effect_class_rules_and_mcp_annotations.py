"""The destructive-operations register's two structural rules (2026-10-10).

1. Every ``bundle:list_*`` is ``read_only`` BY RULE in the one ranking module, so
   a new lister never needs a register row and never stops a candidate run.
2. MCP discovery keeps each server's tool ``annotations`` and derives the class
   the server DECLARES. Before this, ``ExternalMCPClient.discover_tools`` and the
   ``mcp_sync`` spec builder both dropped them, so every discovered tool (44
   Notion rows on 2026-10-04) landed unclassified.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools import mcp_sync
from matrx_ai.tools.external_mcp import ExternalMCPClient
from matrx_ai.tools.side_effect_class import (
    EXTERNAL_WRITE,
    READ_ONLY,
    UNCLASSIFIED_AS,
    effective_invocation_side_effect_class,
    effective_side_effect_class,
    side_effect_class_from_mcp_annotations,
)


def test_a_new_lister_is_read_only_by_rule_without_a_row():
    row = {"name": "bundle:list_brand_new_server", "side_effect_class": None}
    assert effective_side_effect_class(row) == READ_ONLY
    assert effective_invocation_side_effect_class(row, {}) == READ_ONLY
    assert (
        effective_side_effect_class(None, tool_name="bundle:list_brand_new_server")
        == READ_ONLY
    )


def test_the_rule_is_narrow_a_non_lister_null_stays_the_maximum():
    assert effective_side_effect_class({"name": "bundle:other", "side_effect_class": None}) == UNCLASSIFIED_AS
    assert effective_side_effect_class({"name": "list_bundle:x", "side_effect_class": None}) == UNCLASSIFIED_AS
    assert effective_side_effect_class("read_only") == READ_ONLY


@pytest.mark.parametrize(
    ("annotations", "expected"),
    [
        ({"readOnlyHint": True}, READ_ONLY),
        ([{"title": "Search", "readOnlyHint": True, "openWorldHint": True}], READ_ONLY),
        ([{"type": "readOnlyHint", "value": True}], READ_ONLY),
        ({"readOnlyHint": False, "destructiveHint": False}, EXTERNAL_WRITE),
        ({"destructiveHint": True}, EXTERNAL_WRITE),
        ({"readOnlyHint": True, "destructiveHint": True}, EXTERNAL_WRITE),
        ({"openWorldHint": True}, EXTERNAL_WRITE),
        ({"title": "only a title"}, None),
        ([], None),
        (None, None),
    ],
)
def test_class_derived_from_what_the_server_declares(annotations: Any, expected: str | None):
    assert side_effect_class_from_mcp_annotations(annotations) == expected


@pytest.mark.asyncio
async def test_http_discovery_keeps_annotations(monkeypatch):
    async def fake_send(self, url, payload, auth):
        return {
            "result": {
                "tools": [
                    {"name": "notion-search", "inputSchema": {}, "annotations": {"readOnlyHint": True}},
                    {"name": "notion-update-page", "inputSchema": {}, "annotations": {"readOnlyHint": False, "destructiveHint": True}},
                    {"name": "bare", "inputSchema": {}},
                ]
            }
        }

    monkeypatch.setattr(ExternalMCPClient, "_send", fake_send)
    tools = await ExternalMCPClient().discover_tools("https://mcp.example.com/mcp")
    by_name = {t.name: t.annotations for t in tools}
    assert by_name["notion-search"] == [{"readOnlyHint": True}]
    assert by_name["notion-update-page"] == [{"readOnlyHint": False, "destructiveHint": True}]
    assert by_name["bare"] == []


@pytest.mark.asyncio
async def test_sync_sends_annotations_and_derived_class_to_the_rpc(monkeypatch):
    from matrx_ai.tools.models import ToolDefinition

    async def fake_fetch(slug):
        return {
            "id": "6a1f0000-0000-0000-0000-000000000001",
            "slug": slug,
            "transport": "http",
            "endpoint_url": "https://mcp.example.com/mcp",
            "auth_strategy": "none",
            "last_synced_at": None,
            "discovery_ttl_seconds": 60,
        }

    async def fake_discover(self, *args, **kwargs):
        return [
            ToolDefinition(name="mcp.notion.read", description="r", annotations=[{"readOnlyHint": True}]),
            ToolDefinition(name="mcp.notion.write", description="w", annotations=[{"destructiveHint": True}]),
            ToolDefinition(name="mcp.notion.bare", description="b"),
        ]

    captured: list[dict[str, Any]] = []

    async def fake_register(server_id, specs):
        captured.extend(specs)
        return {"inserted": [], "updated": [], "deactivated": []}

    async def fake_stamp(slug):
        return None

    monkeypatch.setattr(mcp_sync, "_fetch_mcp_server", fake_fetch)
    monkeypatch.setattr(mcp_sync.ExternalMCPClient, "discover_tools", fake_discover)
    monkeypatch.setattr(mcp_sync, "_register_mcp_discovered", fake_register)
    monkeypatch.setattr(mcp_sync, "_stamp_synced", fake_stamp)

    result = await mcp_sync._sync_server("notion", force=True)
    assert result.error is None
    by_name = {s["name"]: s for s in captured}
    assert set(by_name) == {"read", "write", "bare"}
    assert by_name["read"]["annotations"] == [{"readOnlyHint": True}]
    assert by_name["read"]["side_effect_class"] == READ_ONLY
    assert by_name["write"]["side_effect_class"] == EXTERNAL_WRITE
    assert by_name["bare"]["annotations"] == []
    assert by_name["bare"]["side_effect_class"] is None


def test_spaces_reads_narrow_to_read_only_and_writes_keep_the_ceiling():
    row = {"name": "spaces", "side_effect_class": "db_write"}
    assert effective_invocation_side_effect_class(row, {"action": "read"}) == READ_ONLY
    assert effective_invocation_side_effect_class(row, {"action": "list"}) == READ_ONLY
    for action in ("create", "save", "archive", "bogus"):
        assert effective_invocation_side_effect_class(row, {"action": action}) == "db_write"
    assert effective_invocation_side_effect_class(row, {}) == "db_write"
