from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest


@pytest.mark.asyncio
async def test_cache_state_update_rejects_terminal_inherited_lane(monkeypatch):
    from matrx_ai.db import persistence

    queued: list[tuple[str, dict[str, object]]] = []
    scopes: list[str] = []

    class _Conversation:
        cache_state = {}

    @asynccontextmanager
    async def _standalone(*, reason, conversation_id):
        scopes.append(f"{reason}:{conversation_id}")
        yield object()

    monkeypatch.setattr(
        persistence,
        "get_current_lane",
        lambda: SimpleNamespace(phase="closed"),
    )
    monkeypatch.setattr(
        persistence,
        "_get_coordinator",
        lambda: pytest.fail("terminal lane must not materialize a request coordinator"),
    )
    monkeypatch.setattr(
        persistence,
        "_cxm",
        lambda: SimpleNamespace(
            conversation=SimpleNamespace(
                load_conversation_by_id=lambda _id: _async_value(_Conversation())
            )
        ),
    )
    monkeypatch.setattr(
        "matrx_ai.persistence.standalone_coordinator",
        _standalone,
    )
    monkeypatch.setattr(
        persistence,
        "_queue_conversation_update",
        lambda conversation_id, **fields: queued.append((conversation_id, fields)),
    )

    await persistence._refresh_cache_state(
        "conversation-1",
        [{"provider": "openai", "ai_model": "model-1", "raw_usage": {}}],
        None,
    )

    assert scopes == ["refresh_conversation_cache_state:conversation-1"]
    assert queued[0][0] == "conversation-1"
    assert "cache_state" in queued[0][1]


async def _async_value(value):
    return value
