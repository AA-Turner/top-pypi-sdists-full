"""memory:update and task:update show the person what they replaced.

Found by the verifier (round 1, 2026-09-26): both overwrite text a person owns
(a remembered preference; a task's title and description) and neither carried a
surface-write receipt, so the chat card showed only the new text. Use case: a
clinic front-desk lead asked the assistant to remember her insurance-check
rule, then to reword the matching task.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest
from matrx_connect.context.app_context import AppContext, set_app_context

from matrx_ai.db import cxm
from matrx_ai.tools.implementations import memory as memory_module
from matrx_ai.tools.implementations.memory import memory_update
from matrx_ai.tools.implementations.tasks import task_update
from matrx_ai.tools.models import ToolContext

USER = "11111111-1111-4111-8111-111111111111"


class _Emitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.mark.asyncio
async def test_memory_update_receipt_carries_the_old_text(monkeypatch: pytest.MonkeyPatch) -> None:
    set_app_context(AppContext(emitter=_Emitter(), user_id=USER, organization_id="org-1"))
    row = type("Row", (), {"id": "mem-1", "content": "Check the insurance card front."})()
    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[row]))
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda *_a, **_kw: "queued")
    result = await memory_update(
        {"key": "insurance_rule", "scope": "user", "content": "Check the insurance card front AND back."},
        ToolContext(call_id="c1"),
    )
    assert result.success, result.error
    assert result.surface_write.before == "Check the insurance card front."
    assert result.surface_write.after == "Check the insurance card front AND back."
    assert "surface_write" not in result.model_dump()


@pytest.mark.asyncio
async def test_task_update_receipt_shows_only_the_changed_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.db.content_types import tasks as tasks_mod

    prior = {"id": "t1", "title": "Verify insurance", "description": "Front of card", "status": "open"}
    after = {**prior, "description": "Front and back of card"}

    class _Mgr:
        get_task = AsyncMock(return_value={"success": True, "task": prior})
        update_task = AsyncMock(return_value={"success": True, "task": after})

    monkeypatch.setattr(tasks_mod, "tasks_manager_instance", _Mgr(), raising=False)
    from contextlib import asynccontextmanager

    from matrx_ai import _ext

    @asynccontextmanager
    async def _as_the_person():  # the task tool runs as the person; pass-through here
        yield

    monkeypatch.setitem(_ext._registry, "acting_as_caller", _as_the_person)
    result = await task_update({"task_id": "t1", "description": "Front and back of card"}, ToolContext(call_id="c2"))
    assert result.success, result.error
    assert "Front of card" in result.surface_write.before
    assert "Front and back of card" in result.surface_write.after
    assert "status" not in result.surface_write.after


@pytest.mark.asyncio
async def test_memory_store_on_an_existing_key_is_an_overwrite_with_a_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations.memory import memory_store

    set_app_context(AppContext(emitter=_Emitter(), user_id=USER, organization_id="org-1"))
    row = type("Row", (), {"id": "mem-1", "content": "Call back within 12 hours."})()
    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[row]))
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda *_a, **_kw: "queued")
    result = await memory_store(
        {"key": "callback_rule", "scope": "user", "memory_type": "long_term", "content": "Call back within 6 hours."},
        ToolContext(call_id="c3"),
    )
    assert result.success, result.error
    assert result.surface_write.before == "Call back within 12 hours."
    assert result.surface_write.after == "Call back within 6 hours."


@pytest.mark.asyncio
async def test_memory_store_of_a_new_key_attaches_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.tools.implementations.memory import memory_store

    set_app_context(AppContext(emitter=_Emitter(), user_id=USER, organization_id="org-1"))
    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[]))
    monkeypatch.setattr(memory_module, "queue_agent_memory_create", lambda *_a, **_kw: "queued")
    result = await memory_store(
        {"key": "fresh", "scope": "user", "memory_type": "long_term", "content": "x"}, ToolContext(call_id="c4")
    )
    assert result.success, result.error
    assert result.surface_write is None
