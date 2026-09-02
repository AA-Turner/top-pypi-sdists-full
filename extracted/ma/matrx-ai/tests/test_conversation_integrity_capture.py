from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.db import _cx_managers_impl as managers


@pytest.mark.parametrize(
    ("status", "completed_at", "metadata", "expected"),
    [
        ("abandoned", None, {}, True),
        ("abandoned", "2026-08-29T13:00:00Z", {}, True),
        ("abandoned", None, {"watchdog_at": "2026-08-29T13:00:00Z"}, False),
        ("abandoned", None, {"watchdog_reason": "timeout"}, False),
        ("failed", None, {}, True),
        ("failed", "2026-08-29T13:00:00Z", {}, False),
        ("completed", "2026-08-29T13:00:00Z", {}, False),
        ("processing", None, {}, False),
    ],
)
def test_incomplete_request_requires_missing_terminal_persistence(
    status: str,
    completed_at: str | None,
    metadata: dict[str, str],
    expected: bool,
) -> None:
    row = SimpleNamespace(status=status, completed_at=completed_at, metadata=metadata)

    assert managers._is_incomplete_request(row) is expected


@pytest.mark.asyncio
async def test_incomplete_request_reload_creates_structured_system_error(monkeypatch) -> None:
    captured: list[tuple[BaseException, dict[str, object]]] = []

    async def fake_capture_error(exc: BaseException, **fields: object) -> None:
        captured.append((exc, fields))

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        fake_capture_error,
    )

    conversation = SimpleNamespace(id="conversation-1", message_count=17)
    incomplete = SimpleNamespace(id="request-1", user_id="user-1", status="failed")

    await managers._capture_incomplete_request_integrity(
        conversation=conversation,
        incomplete_rows=[incomplete],
    )

    assert len(captured) == 1
    error, fields = captured[0]
    assert isinstance(error, RuntimeError)
    assert fields == {
        "kind": "conversation_integrity_incomplete_request",
        "request_id": "request-1",
        "user_id": "user-1",
        "conversation_id": "conversation-1",
        "route": "matrx_ai.db.cx_managers.get_conversation_data",
        "error_type": "IncompleteConversationRequest",
        "payload": {
            "incomplete_request_ids": ["request-1"],
            "incomplete_request_count": 1,
            "committed_message_count": 17,
        },
    }
