"""memory:forget archives; reads skip archived memories; storing the key again revives the row.

Chair round 3 (2026-09-26): every tool delete archives through the table's
soft-delete column where one exists. chat.agent_memory has deleted_at and a
unique (created_by, scope, scope_id, key) index that covers archived rows, so a
forgotten key must be REVIVED on the next store, never re-inserted. Use case: a
clinic front-desk lead tells the assistant to forget her old callback rule,
then later sets a new one under the same key.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.db import cxm
from matrx_ai.tools.implementations import memory as memory_module
from matrx_ai.tools.implementations.memory import memory_forget, memory_recall, memory_store
from matrx_ai.tools.models import ToolContext

USER = "11111111-1111-4111-8111-111111111111"


class _Emitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...


def _row(id: str, content: str, deleted_at: str | None = None) -> Any:
    fields = {"id": id, "key": "callback_rule", "content": content, "deleted_at": deleted_at,
              "memory_type": "long_term", "importance": 0.5, "scope": "user", "scope_id": None,
              "access_count": 0, "expires_at": None, "created_at": None, "updated_at": None}
    return type("Row", (), {**fields, "to_dict": lambda self: dict(fields)})()


def _no_removal(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_delete",
        lambda *_a, **_kw: pytest.fail("forget must archive, never remove the row"), raising=False,
    )


@pytest.fixture(autouse=True)
def _ctx() -> Any:
    token = set_app_context(AppContext(emitter=_Emitter(), user_id=USER, organization_id="org-1"))
    yield
    clear_app_context(token)


@pytest.mark.asyncio
async def test_forget_archives_and_never_queues_a_delete(monkeypatch: pytest.MonkeyPatch) -> None:
    updates: list[tuple[str, dict]] = []
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[_row("mem-1", "Call back within 12 hours.")])
    )
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda id, **kw: updates.append((id, kw)) or "q")
    _no_removal(monkeypatch)
    result = await memory_forget({"key": "callback_rule", "scope": "user"}, ToolContext(call_id="f1"))
    assert result.success, result.error
    assert result.output["deleted"] == 1
    assert updates and updates[0][0] == "mem-1" and updates[0][1]["deleted_at"]


@pytest.mark.asyncio
async def test_forget_skips_an_already_archived_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories",
        AsyncMock(return_value=[_row("mem-1", "old", deleted_at="2026-09-26T10:00:00+00:00")]),
    )
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda *_a, **_kw: pytest.fail("nothing live"))
    _no_removal(monkeypatch)
    result = await memory_forget({"key": "callback_rule", "scope": "user"}, ToolContext(call_id="f2"))
    assert result.success and result.output["deleted"] == 0


@pytest.mark.asyncio
async def test_recall_never_returns_an_archived_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories",
        AsyncMock(return_value=[_row("mem-1", "Forgotten rule", deleted_at="2026-09-26T10:00:00+00:00")]),
    )
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda *_a, **_kw: "q")
    monkeypatch.setattr("matrx_utils.detached_task", lambda *_a, **_kw: None)
    result = await memory_recall({"key": "callback_rule", "scope": "user"}, ToolContext(call_id="r1"))
    assert result.success, result.error
    assert "Forgotten rule" not in str(result.output)


@pytest.mark.asyncio
async def test_store_revives_the_archived_row_for_the_same_key(monkeypatch: pytest.MonkeyPatch) -> None:
    updates: list[tuple[str, dict]] = []
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories",
        AsyncMock(return_value=[_row("mem-1", "Call back within 12 hours.", deleted_at="2026-09-26T10:00:00+00:00")]),
    )
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda id, **kw: updates.append((id, kw)) or "q")
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_create",
        lambda *_a, **_kw: pytest.fail("the unique key index covers archived rows — revive, never insert"),
    )
    result = await memory_store(
        {"key": "callback_rule", "scope": "user", "memory_type": "long_term", "content": "Call back within 6 hours."},
        ToolContext(call_id="s1"),
    )
    assert result.success, result.error
    assert updates[0][0] == "mem-1" and updates[0][1]["deleted_at"] is None
    assert updates[0][1]["content"] == "Call back within 6 hours."
    assert result.surface_write is None  # the person forgot it: nothing live was replaced
