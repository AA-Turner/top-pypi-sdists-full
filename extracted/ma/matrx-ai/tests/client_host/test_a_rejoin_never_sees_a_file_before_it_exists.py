"""A REJOINING CLIENT NEVER SEES A FILE BEFORE IT EXISTS (CGU-10 AND-IMG15 #1, #4; 2026-11-11).

AND-V IMG14 finding 1: the person's ``record_reserved`` frame echoes ``user_content`` with the minted file id
0.5-2 s before the file row exists. A page that rejoins mid-answer (reload, second tab) seeds the bubble from
that echo — a broken picture, and if the upload fails, a file that never exists until the turn settles.

These run the REAL executor (mock provider, a stub coordinator so the reservation runs, storage held at a gate
until the provider has been called). What each is FOR — the plant that turns it red:
* ``test_the_echo_marks_an_uploading_picture_then_names_the_stored_file`` — the echo naming the minted id with
  no pending mark, or no follow-up frame once the file is stored;
* ``test_a_failed_upload_is_echoed_as_the_stand_in`` — the follow-up still naming the file that was never
  stored (or never sent);
* ``test_an_authored_picture_keeps_its_source_at_the_reservation`` — the reservation dropping the authored
  source (AND-V IMG14 plant 11): with the person's upload start failed, the reservation is where an authored
  picture is stored, and it must say ``authored_inline_media``.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_a_turn_only_change_is_never_stored import _scripted_model  # noqa: E402
from test_execute_with_store import FakeEmitter  # noqa: E402
from test_one_attachment_is_one_file import _configure, _StubCoordinator  # noqa: E402

_PENDING = "attachment_pending"
_UNAVAILABLE = "attachment_unavailable"
_PICTURE = "UGljdHVyZSBieXRlcw=="


class _Recorder(FakeEmitter):
    def __init__(self) -> None:
        super().__init__()
        self.reserved: list[Any] = []

    async def send_record_reserved(self, payload: Any) -> None:
        self.reserved.append(payload)


@pytest.fixture
def reserved(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_ai.persistence.queue_helpers as qh

    rows: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: rows.append(kw) or "id")
    monkeypatch.setattr(qh, "queue_message_update", lambda id, **kw: id)
    return rows


@pytest.fixture
def quiet_capture(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_connect.streaming.error_capture as error_capture

    async def capture(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(error_capture, "capture_error", capture)


def _context() -> _Recorder:
    import uuid

    from matrx_connect.context.app_context import AppContext, set_app_context

    emitter = _Recorder()
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            store=True,
            source_app="client_host_tests",
            source_feature="test",
            metadata={},
        )
    )
    return emitter


def _turn() -> Any:
    from matrx_ai.config import TextContent
    from matrx_ai.config.media_config import ImageContent
    from test_the_iteration_ceiling_ends_with_an_answer import _config

    config = _config()
    config.tools = []
    message = config.messages[-1]
    message.content = [TextContent(text="what is this?"), ImageContent(base64_data=_PICTURE, mime_type="image/png")]
    message.user_content = [TextContent(text="what is this?"), ImageContent(base64_data=_PICTURE, mime_type="image/png")]
    return config


def _gated_storage(monkeypatch: pytest.MonkeyPatch, gate: asyncio.Event, *, fails: bool) -> list[str]:
    import matrx_ai.media.media_persistence as media_persistence

    stored: list[str] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, **_: Any) -> SimpleNamespace:
        await gate.wait()
        if fails:
            raise ConnectionError("storage is down")
        stored.append(str(file_id))
        return SimpleNamespace(file_id=file_id, url=f"https://files.example/{file_id}", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    return stored


def _open_gate_at_the_send(monkeypatch: pytest.MonkeyPatch, gate: asyncio.Event) -> None:
    from matrx_ai.providers.mock.mock_api import MockChat

    scripted = MockChat._raw_spec

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        gate.set()
        return scripted(unified_config)

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))


def _user_frames(emitter: _Recorder) -> list[Any]:
    return [p for p in emitter.reserved if getattr(p, "table", None) == "message" and p.metadata.get("role") == "user"]


def _media(frame: Any) -> list[dict[str, Any]]:
    return [b for b in frame.metadata.get("user_content") or [] if isinstance(b, dict) and b.get("type") == "media"]


async def _settle() -> None:
    from matrx_ai.persistence.sealed import settle_person_media_uploads

    await settle_person_media_uploads()
    for _ in range(20):
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_the_echo_marks_an_uploading_picture_then_names_the_stored_file(monkeypatch, reserved) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    gate = asyncio.Event()
    stored = _gated_storage(monkeypatch, gate, fails=False)
    _configure()
    emitter = _context()
    _scripted_model(monkeypatch, [])
    _open_gate_at_the_send(monkeypatch, gate)
    await asyncio.wait_for(execute_ai_request(_turn(), max_iterations=2), timeout=20)
    await _settle()

    frames = _user_frames(emitter)
    assert frames, "the person's row was never announced"
    first = _media(frames[0])
    assert len(first) == 1 and first[0].get("file_id"), frames[0].metadata
    assert _PENDING in (first[0].get("metadata") or {}), (
        f"the echo named file {first[0].get('file_id')} before it existed, with no pending mark: {first[0]}"
    )
    assert len(frames) >= 2, "no follow-up frame once the file was stored — a rejoined bubble stays a placeholder"
    last = frames[-1]
    assert last.record_id == frames[0].record_id
    settled = _media(last)
    assert [p.get("file_id") for p in settled] == stored, (settled, stored)
    assert _PENDING not in (settled[0].get("metadata") or {}), f"the stored file is still marked pending: {settled}"


@pytest.mark.asyncio
async def test_a_failed_upload_is_echoed_as_the_stand_in(monkeypatch, reserved, quiet_capture) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    gate = asyncio.Event()
    _gated_storage(monkeypatch, gate, fails=True)
    _configure()
    emitter = _context()
    _scripted_model(monkeypatch, [])
    _open_gate_at_the_send(monkeypatch, gate)
    await asyncio.wait_for(execute_ai_request(_turn(), max_iterations=2), timeout=20)
    await _settle()

    frames = _user_frames(emitter)
    assert len(frames) >= 2, "no follow-up frame once the upload failed — the bubble names a file that never exists"
    last = frames[-1].metadata.get("user_content") or []
    assert not _media(frames[-1]), f"the follow-up still names a file that was never stored: {last}"
    assert [b for b in last if _UNAVAILABLE in ((b or {}).get("metadata") or {})], f"no stand-in in the echo: {last}"


@pytest.mark.asyncio
async def test_an_authored_picture_keeps_its_source_at_the_reservation(monkeypatch, reserved, quiet_capture) -> None:
    import matrx_ai.media.media_persistence as media_persistence
    from matrx_ai.config import MessageList, TextContent, UnifiedMessage
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.persistence import sealed
    from test_the_iteration_ceiling_ends_with_an_answer import _config

    async def start_fails(*_a: Any, **_k: Any) -> int:
        raise RuntimeError("could not start the person's uploads")

    monkeypatch.setattr(sealed, "keep_inline_person_media_on_server", start_fails)
    stored: list[dict[str, Any]] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, extra_metadata: dict | None = None, **_: Any):
        stored.append({"blob": blob, "source": (extra_metadata or {}).get("source")})
        return SimpleNamespace(file_id=file_id or "f1e00000-0000-4000-8000-000000000001", url="u", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    _configure()
    _context()
    _scripted_model(monkeypatch, [])
    config = _config()
    config.tools = []
    drawn = "QXV0aG9yZWQgcGljdHVyZQ=="
    config.messages = MessageList(_messages=[
        UnifiedMessage(role="user", content=[TextContent(text="draw me a cat")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="here"), ImageContent(base64_data=drawn, mime_type="image/png")]),
        UnifiedMessage(role="user", content=[TextContent(text="now a dog")]),
    ])
    await execute_ai_request(config, max_iterations=2)

    authored = [s for s in stored if s["blob"] == drawn]
    assert authored, "the reservation never stored the authored picture — this test did not reach its door"
    assert authored[0]["source"] == "authored_inline_media", f"stored as {authored[0]['source']}, not authored"
