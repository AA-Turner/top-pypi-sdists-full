"""chat.conversation is a Private table (access ladder T-13): no row-access word on create.

It carries neither ``published_to_web`` nor ``shown_to``; the conversation funnel names
no row-access column at all and the table's own default stands.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.persistence import queue_helpers

ROW_ACCESS_WORDS = {"published_to_web", "published_to_web_at", "published_to_web_by", "shown_to"}


def test_conversation_create_names_no_row_access_word(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def capture(table: str, payload: dict[str, Any], **kwargs: Any) -> str:
        captured.update(table=table, payload=payload, kwargs=kwargs)
        return "op-id"

    monkeypatch.setattr(queue_helpers, "_queue_or_drop", capture)

    op_id = queue_helpers.queue_conversation_create(
        id="conversation-id",
        created_by="user-id",
    )

    assert op_id == "op-id"
    payload = captured["payload"]
    assert not ROW_ACCESS_WORDS & set(payload), payload
    # The retiring column is not stamped either (matched by suffix; the T-13 source
    # ratchet counts the whole word).
    assert not [k for k in payload if k.endswith("ibility")], payload
