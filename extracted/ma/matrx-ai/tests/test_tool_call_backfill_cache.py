"""The EARLY-arrival fix for cx_tool_call.message_id.

When a tool's result message is persisted, ``backfill_message_id`` must link the
message to the tool-call row. The row's INSERT (from ``log_started``) may still
be DEFERRED on the coordinator Session — invisible to a DB read — so a read-to-
find-the-row races the commit and, when it loses, used to DROP the link silently
(leaving ``cx_tool_call.message_id = NULL`` → the rebuild duplicate-tool_result
400, conversation bcc588b6-…).

The fix is an in-process ``(conversation_id, call_id) -> row_id`` registry that
``log_started`` populates the instant the row is born, so the link resolves by pk
regardless of arrival order. These tests pin that behavior with no DB.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import matrx_ai.tools.logger as logger_mod
from matrx_ai.tools.logger import (
    _TOOL_CALL_ROW_BY_CALL_ID,
    ToolExecutionLogger,
    _call_row_key,
)


class _FakeCoord:
    def __init__(self) -> None:
        self.queued: list[tuple] = []

    def queue(self, table, payload, *, op_type, primary_key):
        self.queued.append((table, payload, op_type, primary_key))
        return "op-1"


class _FakeToolCallMgr:
    def __init__(self, rows=None) -> None:
        self.rows = rows or []
        self.filter_calls = 0
        self.updated: list[tuple] = []

    async def filter_items(self, **kw):
        self.filter_calls += 1
        return self.rows

    async def update_item_fields(self, row_id, **kw):
        self.updated.append((row_id, kw))
        return 1


class _FakeCxm:
    def __init__(self, rows=None) -> None:
        self.tool_call = _FakeToolCallMgr(rows)


@pytest.mark.asyncio
async def test_backfill_links_via_cache_when_insert_not_committed(monkeypatch):
    """The early race: the DB read would find nothing, but the cache knows the
    row id, so the link is queued by pk instead of dropped."""
    conv, call_id, row_id, msg_id = "conv-A", "toolu_A", "row-A", "msg-A"
    _TOOL_CALL_ROW_BY_CALL_ID.set(_call_row_key(conv, call_id), row_id)

    coord = _FakeCoord()
    fake_cxm = _FakeCxm(rows=[])  # DB read would find nothing (INSERT deferred)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_cxm", lambda: fake_cxm)

    await ToolExecutionLogger().backfill_message_id(call_id, conv, msg_id)

    assert coord.queued == [
        ("chat.tool_call", {"id": row_id, "message_id": msg_id}, "update", ("id", row_id))
    ], "message_id must be linked via the cache, not dropped"
    assert fake_cxm.tool_call.filter_calls == 0, "cache hit must not touch the DB"


@pytest.mark.asyncio
async def test_backfill_falls_back_to_db_on_cache_miss(monkeypatch):
    """A genuine cache miss (cross-process / expired after a long tool whose
    INSERT has since committed) falls back to the DB read and links the row."""
    conv, call_id, row_id, msg_id = "conv-B", "toolu_B", "row-B", "msg-B"
    _TOOL_CALL_ROW_BY_CALL_ID.remove(_call_row_key(conv, call_id) or "")

    coord = _FakeCoord()
    fake_cxm = _FakeCxm(rows=[SimpleNamespace(id=row_id)])
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_cxm", lambda: fake_cxm)

    await ToolExecutionLogger().backfill_message_id(call_id, conv, msg_id)

    assert fake_cxm.tool_call.filter_calls == 1
    assert coord.queued == [
        ("chat.tool_call", {"id": row_id, "message_id": msg_id}, "update", ("id", row_id))
    ]


@pytest.mark.asyncio
async def test_backfill_screams_when_neither_cache_nor_db_has_row(monkeypatch):
    """No cache entry AND no committed row — never silently drop; surface it."""
    conv, call_id, msg_id = "conv-C", "toolu_C", "msg-C"
    _TOOL_CALL_ROW_BY_CALL_ID.remove(_call_row_key(conv, call_id) or "")

    coord = _FakeCoord()
    fake_cxm = _FakeCxm(rows=[])
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: coord)
    monkeypatch.setattr(logger_mod, "_cxm", lambda: fake_cxm)

    # Must not raise; must not invent a link.
    await ToolExecutionLogger().backfill_message_id(call_id, conv, msg_id)
    assert coord.queued == []
    assert fake_cxm.tool_call.filter_calls == 1


def test_call_row_key_requires_both_ids():
    """The registry key is None unless BOTH ids are present — a missing id must
    never collapse distinct calls onto one cache slot."""
    assert _call_row_key("c", "k") == "c:k"
    assert _call_row_key("c", None) is None
    assert _call_row_key(None, "k") is None
    assert _call_row_key("", "k") is None
