"""Forcing-function: queued conversation memos belong to one coordinator."""

from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.db import conversation_gate as gate


@pytest.fixture(autouse=True)
def _clean_memo(monkeypatch):
    gate._known_conversation_ids.clear()
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    yield
    gate._known_conversation_ids.clear()


@pytest.mark.asyncio
async def test_sibling_coordinator_requeues_conversation_parent(monkeypatch):
    queued: list[str] = []
    conversation_id = str(uuid4())
    user_id = str(uuid4())
    current = {"coord": object()}

    class _Conversation:
        async def filter_conversations(self, **_kwargs):
            return []

    monkeypatch.setattr(gate, "_get_coordinator", lambda: current["coord"])
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **kw: queued.append(kw["id"]))
    monkeypatch.setattr(gate, "_require_valid_user_id", lambda value, _where: value)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", lambda *_args: _none())

    await gate.ensure_conversation_exists(conversation_id, user_id)
    current["coord"] = object()
    await gate.ensure_conversation_exists(conversation_id, user_id)

    assert queued == [conversation_id, conversation_id]


async def _none():
    return None


@pytest.mark.asyncio
async def test_new_conversation_is_published_before_streaming(monkeypatch):
    conversation_id = str(uuid4())
    user_id = str(uuid4())
    events: list[str] = []

    class _Conversation:
        async def filter_conversations(self, **_kwargs):
            events.append("checked")
            return []

    class _Coordinator:
        def set_correlation(self, *, user_id, conversation_id):
            assert user_id == user_id_expected
            assert conversation_id == conversation_id_expected
            events.append("correlated")

        async def finalize(self, *, reason):
            assert reason == "conversation_start"
            events.append("published")

    user_id_expected = user_id
    conversation_id_expected = conversation_id
    coordinator = _Coordinator()
    monkeypatch.setattr(gate, "_get_coordinator", lambda: coordinator)
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(
        gate,
        "_queue_conversation_create",
        lambda **_kwargs: events.append("queued"),
    )
    monkeypatch.setattr(gate, "stamp_org_id", lambda *_args, **_kwargs: None)

    await gate.create_new_conversation(conversation_id, user_id)

    assert events == ["checked", "correlated", "queued", "published"]
    assert gate._known_conversation_ids[conversation_id] is gate._ENSURED_DURABLE


@pytest.mark.asyncio
async def test_new_conversation_publish_failure_is_fatal(monkeypatch):
    conversation_id = str(uuid4())
    user_id = str(uuid4())

    class _Conversation:
        async def filter_conversations(self, **_kwargs):
            return []

    class _Coordinator:
        def set_correlation(self, **_kwargs):
            return None

        async def finalize(self, *, reason):
            assert reason == "conversation_start"
            raise RuntimeError("commit failed")

    monkeypatch.setattr(gate, "_get_coordinator", lambda: _Coordinator())
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_queue_conversation_create", lambda **_kwargs: None)
    monkeypatch.setattr(gate, "stamp_org_id", lambda *_args, **_kwargs: None)

    with pytest.raises(gate.ConversationGateError, match="before streaming"):
        await gate.create_new_conversation(conversation_id, user_id)

    assert conversation_id not in gate._known_conversation_ids


@pytest.mark.asyncio
async def test_out_of_lane_conversation_ensure_acknowledges_direct_write(monkeypatch):
    conversation_id = str(uuid4())
    user_id = str(uuid4())
    model_token = object()
    created: list[dict[str, object]] = []
    acknowledgements: list[tuple[object, str, str]] = []

    class _Conversation:
        model = model_token

        async def filter_conversations(self, **_kwargs):
            return []

        async def create_conversation(self, **kwargs):
            created.append(kwargs)

    class _Report:
        error = None

    class _Session:
        async def flush(self, *, reason):
            assert reason == "conversation_gate"
            return _Report()

    @asynccontextmanager
    async def _session():
        yield _Session()

    @contextmanager
    def _allow_direct(model_cls, *, reason, acknowledgement):
        acknowledgements.append((model_cls, reason, acknowledgement))
        yield

    import matrx_orm

    monkeypatch.setattr(gate, "_get_coordinator", lambda: None)
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_require_valid_user_id", lambda value, _where: value)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", lambda *_args: _none())
    monkeypatch.setattr(matrx_orm, "Session", _session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", _allow_direct)

    await gate.ensure_conversation_exists(conversation_id, user_id)

    assert len(created) == 1
    assert acknowledgements == [
        (
            model_token,
            "out-of-lane conversation ensure — no Coordinator exists in this scope",
            matrx_orm.COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        )
    ]


@pytest.mark.asyncio
async def test_closed_inherited_lane_uses_awaited_conversation_write(monkeypatch):
    """A delayed producer must not mint a Coordinator after lane drain."""
    conversation_id = str(uuid4())
    user_id = str(uuid4())
    created: list[str] = []

    class _Conversation:
        model = object()

        async def filter_conversations(self, **_kwargs):
            return []

        async def create_conversation(self, **kwargs):
            created.append(kwargs["id"])

    class _Report:
        error = None

    class _Session:
        async def flush(self, *, reason):
            assert reason == "conversation_gate"
            return _Report()

    @asynccontextmanager
    async def _session():
        yield _Session()

    @contextmanager
    def _allow_direct(*_args, **_kwargs):
        yield

    import matrx_connect.lane
    import matrx_orm

    monkeypatch.setattr(
        matrx_connect.lane,
        "get_current_lane",
        lambda: SimpleNamespace(phase="closed"),
    )
    monkeypatch.setattr(
        gate,
        "_get_coordinator",
        lambda: pytest.fail("closed lane must not materialize a request coordinator"),
    )
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(conversation=_Conversation()))
    monkeypatch.setattr(gate, "_require_valid_user_id", lambda value, _where: value)
    monkeypatch.setattr(gate, "resolve_parent_conversation_lineage", lambda *_args: _none())
    monkeypatch.setattr(matrx_orm, "Session", _session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", _allow_direct)

    await gate.ensure_conversation_exists(conversation_id, user_id)

    assert created == [conversation_id]
    assert gate._known_conversation_ids[conversation_id] is gate._ENSURED_DURABLE
