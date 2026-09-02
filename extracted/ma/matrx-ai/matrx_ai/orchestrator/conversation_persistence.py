"""The production `ConversationPersistence` for the native ConversationRunner — over
the canonical cx_ write path (the fire-and-verify Coordinator), NOT hand-rolled writes.

This is the last bridge the native-loop cutover needs: it appends a conversation's
turns through `queue_message_create` (the managed cx_message write that flushes at the
request lane's barrier) and reads history back through `cxm.get_conversation_data` +
`rebuild_conversation_messages` (visibility-filtered, tool-content rebuilt). The runner
+ runtime engine own the envelope; this owns only the cx_* turn I/O.

🚨 TWO live-only invariants (see the matrx-persistence skill):
  1. `append_turn` writes via `queue_message_create`, which ONLY flushes inside an
     active RequestLane (opened by `create_streaming_response`). Call it INSIDE a
     streaming task — outside a lane the write SCREAMS "DATA LOSS" and drops.
  2. The cx_message content-block + tool-result SHAPE and the lane flush are validated
     on a real env (`verify_persistence_contract.py` + a real chat), never here.
Every I/O seam is injected (defaults lazy-resolved), so the orchestration is unit-
testable with fakes — no DB, no configure().
"""

from __future__ import annotations

from typing import Any

from matrx_utils.ids import new_hex

from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION


class CxmConversationPersistence:
    """`ConversationPersistence` over cxm + the managed cx_message write path."""

    def __init__(
        self,
        *,
        user_id: str,
        ensure_conversation: Any = None,
        queue_message: Any = None,
        conversation_data: Any = None,
        rebuild_messages: Any = None,
        id_factory: Any = None,
    ) -> None:
        self._user_id = user_id
        self._ensure = ensure_conversation
        self._queue = queue_message
        self._data = conversation_data
        self._rebuild = rebuild_messages
        self._id = id_factory or new_hex
        self._ensured: set[str] = set()

    # --- ConversationPersistence -------------------------------------------

    async def append_turn(
        self, *, conversation_id: str, execution_id: str, role: str, content: Any
    ) -> None:
        await self._ensure_conversation(conversation_id)
        self._queue_message(
            id=self._id(),
            conversation_id=conversation_id,
            role=role,
            position=APPEND_MESSAGE_POSITION,
            status="active",
            content=_to_content_blocks(content),
            metadata={"execution_id": execution_id, "source": role},
        )

    async def history(self, conversation_id: str) -> list[dict[str, Any]]:
        data = await self._conversation_data(conversation_id)
        rebuilt = await self._rebuild_messages(
            data.get("messages") or [],
            data.get("tool_calls") or [],
            data.get("media") or [],
        )
        return [{"role": _role_of(m), "content": _text_of(m)} for m in rebuilt]

    async def _ensure_conversation(self, conversation_id: str) -> None:
        if conversation_id in self._ensured:
            return
        await self._ensure_fn()(conversation_id, self._user_id)
        self._ensured.add(conversation_id)

    # --- seam resolution (injected, else lazy default) ---------------------

    def _ensure_fn(self):
        if self._ensure is not None:
            return self._ensure
        from matrx_ai.db.conversation_gate import ensure_conversation_exists

        return ensure_conversation_exists

    def _queue_message(self, **kwargs: Any) -> None:
        if self._queue is not None:
            self._queue(**kwargs)
            return
        from matrx_ai.persistence import queue_message_create

        queue_message_create(**kwargs)

    async def _conversation_data(self, conversation_id: str) -> dict[str, Any]:
        if self._data is not None:
            return await self._data(conversation_id)
        from matrx_ai.db import cxm

        return await cxm.get_conversation_data(conversation_id)

    async def _rebuild_messages(self, messages: Any, tool_calls: Any, media: Any) -> list[Any]:
        if self._rebuild is not None:
            return await self._rebuild(messages, tool_calls, media)
        from matrx_ai.db import rebuild_conversation_messages

        return await rebuild_conversation_messages(messages, tool_calls, media)


def _to_content_blocks(content: Any) -> list[Any]:
    """Normalise a turn's content into the cx_message content-block list shape.
    (The exact provider-faithful tool-result shape is validated on a real env.)"""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, list):
        return content
    if isinstance(content, dict):
        return [content]
    return [{"type": "text", "text": str(content)}]


def _role_of(message: Any) -> str:
    role = getattr(message, "role", None)
    return role.value if hasattr(role, "value") else (role or "user")


def _text_of(message: Any) -> Any:
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [
            (b.get("text", "") if isinstance(b, dict) else getattr(b, "text", ""))
            for b in content
            if (isinstance(b, dict) and b.get("type") == "text") or hasattr(b, "text")
        ]
        if parts:
            return "".join(parts)
    return content


__all__ = ["CxmConversationPersistence"]
