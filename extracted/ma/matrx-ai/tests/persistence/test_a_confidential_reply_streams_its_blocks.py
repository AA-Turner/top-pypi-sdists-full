"""FORCING TEST — a confidential reply's stream hears its blocks before the row is blanked (PF-1 D5, P3b advisory).

A sealed run's server row carries no text, so blocks annotated AFTER sealing were empty and the stream sent no
``message_blocks``: the device copy (the only place the words live) drew from a client split instead of the saved
shape. The blocks are now built from the reply as written, BEFORE sealing, and only announced; the stored row stays
blank (no text, no blocks). Lane: common-docs/systems/chat/projects/chat-ground-up/cgu-m3-lanes/L13-blocks.md.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace

import pytest

_REPLY = 'Here you go.\n\n```json\n{"__kind": "flashcard_set", "cards": []}\n```\n\nDone.'


class _MessageMeta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "message"
    db_schema = "chat"


class _PackageMessage:
    _meta = _MessageMeta()

_ORG = "66666666-6666-4666-8666-666666666666"
_USER = "11111111-1111-4111-8111-111111111111"


class _Emitter:
    def __init__(self) -> None:
        self.sent: list = []

    async def send_data(self, payload) -> None:
        self.sent.append(payload)


def _run(keeps_content: bool) -> tuple[list, dict]:
    from matrx_orm.session.coalesce import coalesce_ops

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import Coordinator
    from matrx_ai.persistence.registry import override_table
    from matrx_ai.processing.blocks import saved_blocks

    conv, reply = str(uuid.uuid4()), str(uuid.uuid4())
    emitter = _Emitter()
    ctx = SimpleNamespace(
        organization_id=_ORG, request_id=str(uuid.uuid4()), user_id=_USER, conversation_id=conv,
        sealed_conversation_id=conv, sealed_keeps_content=keeps_content, emitter=emitter,
    )

    async def body() -> dict:
        mp = pytest.MonkeyPatch()
        mp.setattr(queue_helpers, "_resolve_app_context", lambda: ctx)
        saved_blocks.configure_blocks_save(lambda: True)
        coord = Coordinator(request_id=str(uuid.uuid4()))
        token = queue_helpers._coordinator_cv.set(coord)
        stand_in = override_table("chat.message", _PackageMessage)
        stand_in.__enter__()
        try:
            queue_helpers.queue_message_create(
                id=reply, conversation_id=conv, role="assistant", content=[{"type": "text", "text": _REPLY}]
            )
            await asyncio.sleep(0)
            await asyncio.sleep(0)
            return {op.pk_value: (op.payload or {}) for op in coalesce_ops(list(coord._session._ops))}.get(reply, {})
        finally:
            stand_in.__exit__(None, None, None)
            queue_helpers._coordinator_cv.reset(token)
            coord._session._ops.clear()
            saved_blocks.configure_blocks_save(None)
            mp.undo()

    stored = asyncio.run(body())
    return emitter.sent, stored


def test_a_blanked_confidential_reply_still_streams_its_blocks() -> None:
    sent, stored = _run(keeps_content=False)
    assert len(sent) == 1, "the stream must hear the reply's blocks"
    (part,) = [p.model_dump() for p in sent[0].parts]
    assert part["text"] == _REPLY and part["blocks"], "built from the reply as written"
    assert "kind" in [b["type"] for b in part["blocks"]]
    # The stored row stays blank: no text, no blocks.
    assert not any(isinstance(p, dict) and (p.get("text") or p.get("blocks")) for p in stored.get("content") or [])


def test_a_confidential_reply_that_keeps_its_content_streams_its_blocks_once() -> None:
    sent, stored = _run(keeps_content=True)
    assert len(sent) == 1
    assert sent[0].parts[0].text == _REPLY
