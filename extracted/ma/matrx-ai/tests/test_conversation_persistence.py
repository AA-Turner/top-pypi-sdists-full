"""CxmConversationPersistence — the native ConversationRunner's cx_ write/read bridge.
Injected fakes (ensure / queue / data / rebuild); no DB, no configure().
"""

from __future__ import annotations

import types

from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION
from matrx_ai.orchestrator.conversation_persistence import CxmConversationPersistence


class _Recorder:
    def __init__(self, messages=None):
        self.ensured: list[tuple[str, str]] = []
        self.queued: list[dict] = []
        self._messages = messages or []

    async def ensure(self, conversation_id, user_id):
        self.ensured.append((conversation_id, user_id))

    def queue(self, **kwargs):
        self.queued.append(kwargs)

    async def data(self, conversation_id):
        return {"messages": self._messages, "tool_calls": [], "media": []}

    async def rebuild(self, messages, tool_calls, media):
        # echo back the messages already shaped as {role, content}-bearing objects
        return messages


def _msg(role, text, position=0):
    return types.SimpleNamespace(
        role=role,
        content=[{"type": "text", "text": text}],
        position=position,
    )


def _adapter(rec, **kw):
    return CxmConversationPersistence(
        user_id="u-1",
        ensure_conversation=rec.ensure,
        queue_message=rec.queue,
        conversation_data=rec.data,
        rebuild_messages=rec.rebuild,
        id_factory=lambda: "fixed-id",
        **kw,
    )


async def test_append_turn_ensures_once_and_queues_for_atomic_append():
    rec = _Recorder(messages=[])
    cx = _adapter(rec)
    await cx.append_turn(conversation_id="c1", execution_id="e1", role="user", content="hello")
    await cx.append_turn(
        conversation_id="c1",
        execution_id="e1",
        role="assistant",
        content="hi there",
    )

    assert rec.ensured == [("c1", "u-1")]  # ensure happens exactly once per conversation
    assert [q["position"] for q in rec.queued] == [
        APPEND_MESSAGE_POSITION,
        APPEND_MESSAGE_POSITION,
    ]
    assert [q["role"] for q in rec.queued] == ["user", "assistant"]
    first = rec.queued[0]
    assert first["conversation_id"] == "c1" and first["status"] == "active"
    assert first["content"] == [{"type": "text", "text": "hello"}]  # str → text block
    assert first["metadata"] == {"execution_id": "e1", "source": "user"}


async def test_append_does_not_guess_position_from_existing_history():
    rec = _Recorder(messages=[_msg("user", "old", position=4)])
    cx = _adapter(rec)
    await cx.append_turn(conversation_id="c1", execution_id="e1", role="user", content="new")
    assert rec.queued[0]["position"] == APPEND_MESSAGE_POSITION


async def test_dict_content_becomes_single_block():
    rec = _Recorder()
    cx = _adapter(rec)
    payload = {"call_id": "t1", "result": {"ok": True}}
    await cx.append_turn(conversation_id="c1", execution_id="e1", role="tool", content=payload)
    assert rec.queued[0]["content"] == [payload]


async def test_history_maps_rebuilt_messages_to_role_content_dicts():
    rec = _Recorder(messages=[_msg("user", "hi"), _msg("assistant", "hello back")])
    cx = _adapter(rec)
    hist = await cx.history("c1")
    assert hist == [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello back"},
    ]


async def test_history_handles_enum_role_and_plain_string_content():
    rec = _Recorder(messages=[
        types.SimpleNamespace(role=types.SimpleNamespace(value="assistant"), content="plain"),
    ])
    cx = _adapter(rec)
    hist = await cx.history("c1")
    assert hist == [{"role": "assistant", "content": "plain"}]
