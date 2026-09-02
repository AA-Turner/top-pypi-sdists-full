from __future__ import annotations

from typing import Any

from matrx_ai.persistence import queue_helpers


def test_conversation_create_stamps_canonical_visibility(monkeypatch) -> None:
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
    assert captured["payload"]["visibility"] == "personal"


def test_conversation_create_preserves_explicit_visibility(monkeypatch) -> None:
    captured: dict[str, Any] = {}

    def capture(table: str, payload: dict[str, Any], **kwargs: Any) -> str:
        captured.update(payload)
        return "op-id"

    monkeypatch.setattr(queue_helpers, "_queue_or_drop", capture)

    queue_helpers.queue_conversation_create(
        id="conversation-id",
        created_by="user-id",
        visibility="internal",
    )

    assert captured["visibility"] == "internal"
