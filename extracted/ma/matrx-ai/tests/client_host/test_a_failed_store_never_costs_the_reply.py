"""A PERSON'S ATTACHMENT NEVER STANDS IN FRONT OF THE ANSWER, AND A FAILED ONE NEVER COSTS IT
(CGU-10 AND-IMG14, 2026-11-11 — findings 1-5 of the AND-V IMG13 checker pass).

Every test runs the REAL executor (in-repo mock provider, a stub coordinator so the reservation runs). What
each is FOR — the plant that turns it red:
* ``test_one_of_two_uploads_fails_the_good_one_is_stored_once`` — uploads gathered so one failure throws
  away the other's id (the good picture re-uploaded by the send step and the end save: 3 files, 2 orphans).
* ``test_storage_down_is_tried_once_per_attachment`` — the send-step backstop or the end save trying an
  attachment whose store already failed this turn (storage that is down waited on twice or more).
* ``test_the_upload_runs_beside_the_provider_call`` — the upload awaited before the provider call (the first
  token waits for storage), or uploads made one after another instead of side by side.
The REAL ``persist_completed_request`` half (storage down the whole turn: both rows still saved) lives in
``tests/test_a_failed_attachment_store_never_costs_the_reply.py`` (the server save, not the client store).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

#: ``sealed.UNAVAILABLE_ATTACHMENT_KEY`` — spelled out so this guard also runs (red) against code without it.
_UNAVAILABLE = "attachment_unavailable"

from test_a_turn_only_change_is_never_stored import _scripted_model  # noqa: E402
from test_one_attachment_is_one_file import (  # noqa: E402
    _KINDS,
    _configure,
    _end_save,
    _media_ids,
    _persons_turn,
    _set_context,
    _StubCoordinator,
)

_BAD = _KINDS[1][2]  # the audio clip's bytes: the one whose store fails


@pytest.fixture
def reserved(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_ai.persistence.queue_helpers as qh

    rows: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: rows.append({"op": "create", **kw}) or "id")
    monkeypatch.setattr(
        qh, "queue_message_update", lambda id, **kw: rows.append({"op": "update", "id": id, **kw}) or id
    )
    return rows


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_connect.streaming.error_capture as error_capture

    seen: list[dict[str, Any]] = []

    async def capture(exc: BaseException, **kw: Any) -> None:
        seen.append({"exc": exc, **kw})

    monkeypatch.setattr(error_capture, "capture_error", capture)
    return seen


def _storage(monkeypatch: pytest.MonkeyPatch, *, fails: set[str], delay: float = 0.0, gate: asyncio.Event | None = None):
    import matrx_ai.media.media_persistence as media_persistence

    calls: list[dict[str, Any]] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, **_: Any) -> SimpleNamespace:
        call = {"blob": blob, "file_id": file_id, "done": False}
        calls.append(call)
        if gate is not None:
            await gate.wait()
        if delay:
            await asyncio.sleep(delay)
        call["done"] = True
        if blob in fails:
            raise ConnectionError("storage is down")
        return SimpleNamespace(file_id=file_id, url=f"https://files.example/{file_id}", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    return calls


def _stand_ins(parts: list[Any]) -> list[dict[str, Any]]:
    return [p for p in parts if isinstance(p, dict) and _UNAVAILABLE in (p.get("metadata") or {})]


@pytest.mark.asyncio
async def test_one_of_two_uploads_fails_the_good_one_is_stored_once(monkeypatch, reserved, captured) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    calls = _storage(monkeypatch, fails={_BAD})
    _configure()
    _set_context(store=True)
    _scripted_model(monkeypatch, [])
    completed = await execute_ai_request(_persons_turn(), max_iterations=2)
    saved = await _end_save(completed)

    by_blob: dict[str, int] = {}
    for c in calls:
        by_blob[c["blob"]] = by_blob.get(c["blob"], 0) + 1
    assert by_blob == {k[2]: 1 for k in _KINDS}, f"an attachment was stored more than once: {by_blob}"
    good = {c["file_id"] for c in calls if c["blob"] != _BAD}
    assert set(_media_ids(saved)) == good, f"a good attachment lost its id or a row names the failed one: {saved}"
    assert len(_stand_ins(saved)) == 2, f"the failed attachment is not marked in content AND user_content: {saved}"
    assert not [c for c in captured if c.get("kind") == "media_reference_resolution_failed"], (
        "the send tried to fetch an attachment by an id whose upload was still running"
    )
    failures = [c for c in captured if c.get("kind") == "person_inline_media_store_failed"]
    assert len(failures) == 1, f"the one failed store was captured {len(failures)} times"


@pytest.mark.asyncio
async def test_storage_down_is_tried_once_per_attachment(monkeypatch, reserved, captured) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    everything = {k[2] for k in _KINDS}
    calls = _storage(monkeypatch, fails=everything)
    _configure()
    _set_context(store=True)
    seen = _scripted_model(monkeypatch, [])
    completed = await execute_ai_request(_persons_turn(), max_iterations=2)
    saved = await _end_save(completed)
    assert seen, "the send never happened"
    assert len(calls) == len(_KINDS), f"{len(calls)} store attempts for {len(_KINDS)} attachments: storage down was retried"
    assert not _media_ids(saved), f"a row names a file that was never stored: {saved}"
    lost = {p["metadata"]["attachment_unavailable"]["mime_type"] for p in _stand_ins(saved)}
    assert lost == {k[1] for k in _KINDS}, f"an attachment that failed is not marked: {lost}"


@pytest.mark.asyncio
async def test_the_upload_runs_beside_the_provider_call(monkeypatch, reserved, captured) -> None:
    from matrx_ai.config.message_config import _media_identity_label
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers.mock.mock_api import MockChat

    gate = asyncio.Event()
    calls = _storage(monkeypatch, fails=set(), gate=gate)
    _configure()
    _set_context(store=True)
    _scripted_model(monkeypatch, [])
    at_send: list[dict[str, Any]] = []
    scripted = MockChat._raw_spec

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        picture = unified_config.messages[0].content[1]
        at_send.append(
            {
                "started": len(calls),
                "finished": sum(1 for c in calls if c["done"]),
                "label": _media_identity_label(picture, "user") or "",
                "file_id": picture.file_id,
            }
        )
        gate.set()  # storage may finish now — the answer is already on its way
        return scripted(unified_config)

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    config = _persons_turn()
    completed = await asyncio.wait_for(execute_ai_request(config, max_iterations=2), timeout=20)
    saved = await _end_save(completed)

    assert at_send, "the provider was never called"
    first = at_send[0]
    assert first["finished"] == 0, f"the provider call waited for {first['finished']} upload(s) to finish"
    assert first["started"] == len(_KINDS), (
        f"only {first['started']} of {len(_KINDS)} uploads had started at the send: they run one after another"
    )
    assert first["file_id"] and f'id="{first["file_id"]}"' in first["label"], first
    assert set(_media_ids(saved)) == {c["file_id"] for c in calls}, saved
    assert len(calls) == len(_KINDS)


@pytest.mark.asyncio
async def test_an_authored_picture_is_stored_once_under_its_own_source(monkeypatch, reserved, captured) -> None:
    """An inline picture inside an earlier ASSISTANT turn a client sends as its own history is client-authored
    content, not the person's attachment (AND-V IMG13 #6): stored once (a stored media part must name its
    file), under ``authored_inline_media`` — never ``inline_media_part``, the person's source."""
    import matrx_ai.media.media_persistence as media_persistence
    from matrx_ai.config import MessageList, TextContent, UnifiedMessage
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.orchestrator.executor import execute_ai_request
    from test_the_iteration_ceiling_ends_with_an_answer import _config

    stored: list[dict[str, Any]] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, extra_metadata: dict | None = None, **_: Any):
        stored.append({"blob": blob, "file_id": file_id, "source": (extra_metadata or {}).get("source")})
        return SimpleNamespace(file_id=file_id, url=f"https://files.example/{file_id}", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    _configure()
    _set_context(store=True)
    _scripted_model(monkeypatch, [])
    config = _config()
    config.tools = []
    drawn = "QXV0aG9yZWQgcGljdHVyZQ=="
    config.messages = MessageList(_messages=[
        UnifiedMessage(role="user", content=[TextContent(text="draw me a cat")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="here"), ImageContent(base64_data=drawn, mime_type="image/png")]),
        UnifiedMessage(role="user", content=[TextContent(text="now a dog")]),
    ])
    completed = await execute_ai_request(config, max_iterations=2)
    await _end_save(completed)

    authored = [s for s in stored if s["blob"] == drawn]
    assert len(authored) == 1, f"the authored picture was stored {len(authored)} times: {authored}"
    assert authored[0]["source"] == "authored_inline_media", authored[0]
