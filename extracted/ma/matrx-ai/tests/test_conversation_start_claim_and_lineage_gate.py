"""A run-less conversation writes no 'pending' start claim; a parentless child is never 'subagent'."""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate


async def _create(monkeypatch, **kwargs):
    queued: list[dict] = []

    class _Conversation:
        async def filter_conversations(self, **_kw):
            return []

    class _Coordinator:
        def set_correlation(self, **_kw):
            return None

        async def finalize(self, *, reason):
            return None

    async def _no_parent(*_a):
        return None

    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw))
    monkeypatch.setattr(gate, "stamp_org_id", lambda *_a, **_k: None)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", _no_parent)
    gate._known_conversation_ids.clear()
    await gate.create_new_conversation(str(uuid4()), str(uuid4()), **kwargs)
    return queued[0]


@pytest.mark.asyncio
async def test_default_create_writes_the_pending_start_claim(monkeypatch):
    row = await _create(monkeypatch)
    assert row["last_request_status"] == "pending"


@pytest.mark.asyncio
async def test_runless_create_writes_no_claim(monkeypatch):
    row = await _create(monkeypatch, start_claim=False)
    assert row.get("last_request_status") is None
    assert row.get("last_request_id") is None


@pytest.mark.asyncio
async def test_unverified_parent_never_leaves_a_subagent_label(monkeypatch):
    from matrx_connect.context.app_context import clear_app_context, set_app_context
    from matrx_connect import AppContext
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    ctx = AppContext(
        emitter=ConsoleEmitter("t", accumulate=False),
        conversation_type="subagent",
        is_internal_agent=True,
    )
    token = set_app_context(ctx)
    try:
        row = await _create(monkeypatch, parent_conversation_id=str(uuid4()))
    finally:
        clear_app_context(token)
    # the parent row was not on disk (resolver returned None): this is a root run
    assert row["conversation_type"] == "auto"
