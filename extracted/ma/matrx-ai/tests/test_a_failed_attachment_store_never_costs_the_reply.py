"""STORAGE DOWN THE WHOLE TURN: THE ANSWER IS STILL SAVED (CGU-10 AND-IMG14 #4, 2026-11-11).

AND-V IMG13 finding 4 (PLAUSIBLE, proven here): with storage down through the whole turn the answer streamed,
but ``persist_completed_request`` stored the person's message first, its inline attachment's upload raised
``ConnectionError`` (only ``ValueError`` was caught), and the save ended before the assistant row — both rows
stayed ``pending`` until they aged to ``abandoned``. A reload showed nothing of an answer the person read.

Seam: the REAL ``persist_completed_request`` (server path); only the queue writers, the model lookup and the
files service are stood in (``persist_harness`` from the control-token suite). The failed attachment is saved
as the marked stand-in and the failure is captured. Red when a failed store raises out of the person's row
save again (e.g. ``keep_inline_media_on_server`` re-raising instead of writing the stand-in).
"""

from __future__ import annotations

from typing import Any

import pytest

from test_control_token_persistence import (  # noqa: F401 — the harness fixture by name
    CONVERSATION_ID,
    _request,
    persist_harness,
)

from matrx_ai.config import TextContent
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.requests import CompletedRequest
from matrx_ai.orchestrator.execution_state import ExecutionState

#: ``sealed.UNAVAILABLE_ATTACHMENT_KEY`` — spelled out so this guard also runs (red) against code without it.
_UNAVAILABLE = "attachment_unavailable"


@pytest.fixture
def storage_down(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_ai.media.media_persistence as media_persistence
    import matrx_connect.streaming.error_capture as error_capture

    captured: list[dict[str, Any]] = []

    async def down(*_a: Any, **_k: Any) -> Any:
        raise ConnectionError("storage is down")

    async def capture(exc: BaseException, **kw: Any) -> None:
        captured.append({"exc": exc, **kw})

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", down)
    monkeypatch.setattr(error_capture, "capture_error", capture)
    return captured


@pytest.mark.asyncio
async def test_storage_down_the_whole_turn_both_rows_are_saved(persist_harness, storage_down) -> None:  # noqa: F811 — imported fixture, used by name
    persistence_mod, creates, updates = persist_harness
    person = UnifiedMessage(
        role="user",
        content=[TextContent(text="what is this?"), ImageContent(base64_data="UGljdHVyZQ==", mime_type="image/png")],
    )
    answer = UnifiedMessage(role="assistant", content=[TextContent(text="A picture of a cat.")])
    completed = CompletedRequest(
        request=_request(person, answer),
        iterations=1,
        final_response=UnifiedResponse(messages=[answer]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=1,
    )

    await persistence_mod.persist_completed_request(
        completed, conversation_id=CONVERSATION_ID, state=ExecutionState()
    )

    rows = creates + [fields for _mid, fields in updates]
    assistant = [r for r in rows if r.get("role") == "assistant"]
    assert assistant, "the answer streamed but its row was never saved: a failed attachment store ended the save"
    assert "A picture of a cat." in "".join(p.get("text", "") for p in assistant[0]["content"])
    user = [r for r in rows if r.get("role") == "user"]
    assert user, "the person's row was not saved"
    marked = [p for p in user[0]["content"] if _UNAVAILABLE in (p.get("metadata") or {})]
    assert marked and not [p for p in user[0]["content"] if p.get("type") == "media"], user[0]["content"]
    assert [c for c in storage_down if c.get("kind") == "person_inline_media_store_failed"], storage_down


@pytest.mark.asyncio
async def test_a_store_that_failed_is_not_tried_again_in_the_same_request(storage_down, monkeypatch) -> None:
    """An id-less inline part (an internal caller's bytes) whose store failed in a request is not uploaded
    again by a later save of the SAME request — storage that is down is waited on once (IMG13 #2)."""
    import uuid

    import matrx_ai.media.media_persistence as media_persistence
    from matrx_ai.persistence.sealed import stored_message_content

    attempts: list[str] = []

    async def down(blob: str, *_a: Any, **_k: Any) -> Any:
        attempts.append(blob)
        raise ConnectionError("storage is down")

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", down)
    ctx = type("Ctx", (), {"request_id": str(uuid.uuid4()), "store": True, "metadata": {}})()
    part = {"type": "media", "kind": "image", "mime_type": "image/png", "base64_data": "QnJpbmcgYmFjaw=="}
    first = await stored_message_content([dict(part)], ctx)
    second = await stored_message_content([dict(part)], ctx)
    assert len(attempts) == 1, f"the same failed bytes were tried {len(attempts)} times in one request"
    assert first == second and _UNAVAILABLE in (first[0].get("metadata") or {}), first
