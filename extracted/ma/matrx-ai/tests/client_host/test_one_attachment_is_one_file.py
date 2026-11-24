"""ONE ATTACHMENT IS ONE FILE, THROUGH THE EXECUTOR'S REAL ORDER (CGU-10 AND-IMG13 #1, #2, #4; 2026-11-11).

Live (AND-V IMG12, run 98b365e5): one pasted picture made 4 stored files, 1 used. The executor reserved the
person's row BEFORE the loop on storage-dict COPIES of ``content`` and of the pristine ``user_content`` (each
uploaded, neither wrote the id back), the send boundary uploaded the id-less part again, and the end save
uploaded the pristine copy again. The IMG12 test called the send step first and the save second — not the
executor's order — so it passed while live failed.

These run the REAL executor (the in-repo mock provider, a stub coordinator so the reservation runs), then the
end save's own step (``stored_message_content`` over every stored message's content AND user_content, as
``db/persistence.persist_completed_request`` does), and count uploads. What each is FOR:
* the executor stops storing once before the reservation, or stops writing the id back → upload count > 1
  (``test_one_upload_per_attachment_through_the_executor``);
* the pristine copy stops sharing the id → its stored id differs / count > 1 (same test);
* an unsaved run stores the person's media → ``test_an_unsaved_run_stores_nothing``;
* storage down blocks the send or stops being captured → ``test_storage_down_the_send_continues_and_is_captured``.
"""

from __future__ import annotations

import copy
from types import SimpleNamespace
from typing import Any

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_a_turn_only_change_is_never_stored import _scripted_model  # noqa: E402
from test_execute_with_store import _MOCK_MODEL, InMemoryStore, StaticCatalog  # noqa: E402
from test_the_iteration_ceiling_ends_with_an_answer import _config  # noqa: E402

_KINDS = [
    ("image", "image/png", "UGljdHVyZSBieXRlcw=="),
    ("audio", "audio/mpeg", "QXVkaW8gYnl0ZXM="),
    ("video", "video/mp4", "VmlkZW8gYnl0ZXM="),
    ("document", "application/pdf", "UERGIGJ5dGVz"),
]


def _configure() -> None:
    """A model that reads every kind it is sent, so no attachment is converted on the way (the count is the
    person's attachments, nothing else)."""
    from matrx_ai._ext import configure_ext

    reader = dict(_MOCK_MODEL, capabilities={**_MOCK_MODEL["capabilities"], "input": ["text", *[k[0] for k in _KINDS]]})
    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([reader]),
        api_key_resolver=lambda name: "not-a-real-key",
    )


def _part(kind: str, mime: str, blob: str) -> Any:
    from matrx_ai.config.media_config import AudioContent, DocumentContent, ImageContent, VideoContent

    cls = {"image": ImageContent, "audio": AudioContent, "video": VideoContent, "document": DocumentContent}[kind]
    return cls(base64_data=blob, mime_type=mime)


def _set_context(*, store: bool) -> None:
    import uuid

    from matrx_connect.context.app_context import AppContext, set_app_context
    from test_execute_with_store import FakeEmitter

    set_app_context(
        AppContext(
            emitter=FakeEmitter(),
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            store=store,
            source_app="client_host_tests",
            source_feature="test",
            metadata={},
        )
    )


class _StubCoordinator:
    """Truthy stand-in for the streaming lane's WriteCoordinator: the reservation runs only with one."""

    def queue(self, *a: Any, **k: Any) -> str:
        return ""

    def commit_async(self, *a: Any, **k: Any) -> None:
        return None

    async def check_pending(self, *a: Any, **k: Any) -> None:
        return None

    async def finalize(self, *a: Any, **k: Any) -> None:
        return None

    async def drain_and_confirm(self, *a: Any, **k: Any) -> list[Any]:
        return []

    async def seal(self, *a: Any, **k: Any) -> None:
        return None


@pytest.fixture
def uploads(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    import matrx_ai.media.media_persistence as media_persistence

    made: list[tuple[str, str]] = []

    async def fake_save(blob: str, mime: str, *, file_id: str | None = None, **_: Any) -> SimpleNamespace:
        # The files service stores under the id the caller minted (``save_media_envelope_async(file_id=)``).
        made.append((file_id or f"8a1f4320-0000-4000-8000-{len(made):012d}", blob))
        return SimpleNamespace(file_id=made[-1][0], url=f"https://files.example/{made[-1][0]}", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", fake_save)
    return made


@pytest.fixture
def reserved(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    import matrx_ai.persistence.queue_helpers as qh

    rows: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: rows.append(kw) or "id")
    return rows


def _persons_turn() -> Any:
    from matrx_ai.config import TextContent

    config = _config()
    config.tools = []
    message = config.messages[-1]
    parts = [_part(*k) for k in _KINDS]
    # The pristine copy is its own objects with the same bytes — as a deserialized request carries it.
    message.content = [TextContent(text="what is in these?"), *parts]
    message.user_content = [TextContent(text="what is in these?"), *copy.deepcopy(parts)]
    return config


async def _end_save(completed: Any) -> list[dict[str, Any]]:
    """The end save's own step over every stored message (``db/persistence.persist_completed_request``)."""
    from matrx_ai.persistence.sealed import stored_message_content

    saved: list[dict[str, Any]] = []
    for message in completed.request.config.messages:
        storage = message.to_storage_dict()
        saved.extend(await stored_message_content(storage.get("content") or []))
        if storage.get("user_content") is not None:
            saved.extend(await stored_message_content(storage["user_content"]))
    return saved


def _media_ids(parts: list[Any]) -> list[str]:
    return [str(p.get("file_id")) for p in parts if isinstance(p, dict) and p.get("type") == "media"]


@pytest.mark.asyncio
async def test_one_upload_per_attachment_through_the_executor(monkeypatch, uploads, reserved) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    _configure()
    _set_context(store=True)
    _scripted_model(monkeypatch, [])
    completed = await execute_ai_request(_persons_turn(), max_iterations=2)
    saved = await _end_save(completed)

    assert len(uploads) == len(_KINDS), f"{len(uploads)} uploads for {len(_KINDS)} attachments: {uploads}"
    assert sorted(b for _i, b in uploads) == sorted(k[2] for k in _KINDS), "an attachment was uploaded twice"
    ids = {i for i, _b in uploads}
    # The reservation, the end save (content AND pristine user_content) all name exactly those files.
    user_rows = [r for r in reserved if r.get("role") == "user"]
    assert user_rows, "the person's row was never reserved — this test did not drive the reservation"
    for row in user_rows:
        assert set(_media_ids(row.get("content") or [])) == ids, row.get("content")
        assert set(_media_ids(row.get("user_content") or [])) == ids, row.get("user_content")
    assert set(_media_ids(saved)) == ids, saved


@pytest.mark.asyncio
async def test_an_unsaved_run_stores_nothing(monkeypatch, uploads, reserved) -> None:
    """``store: false`` writes no conversation, no message, no request — and now no file either. The web
    sends a file it already uploaded (its attach flow stores first); an inline part here goes out as it
    arrived, its label saying ``id=""``: there is no file to name."""
    from matrx_ai.config.message_config import _media_identity_label
    from matrx_ai.orchestrator.executor import execute_ai_request

    _configure()
    _set_context(store=False)
    _scripted_model(monkeypatch, [])
    config = _persons_turn()
    await execute_ai_request(config, max_iterations=2)
    assert uploads == [], f"an unsaved run stored the person's media: {uploads}"
    picture = config.messages[0].content[1]
    assert picture.file_id is None and 'id=""' in (_media_identity_label(picture, "user") or "")


@pytest.mark.asyncio
async def test_storage_down_the_send_continues_and_is_captured(monkeypatch, reserved) -> None:
    import matrx_ai.media.media_persistence as media_persistence
    import matrx_connect.streaming.error_capture as error_capture
    from matrx_ai.orchestrator.executor import execute_ai_request

    async def down(*_a: Any, **_k: Any) -> Any:
        raise ConnectionError("storage is down")

    captured: list[dict[str, Any]] = []

    async def capture(exc: BaseException, **kw: Any) -> None:
        captured.append({"exc": exc, **kw})

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", down)
    monkeypatch.setattr(error_capture, "capture_error", capture)
    _configure()
    _set_context(store=True)
    seen = _scripted_model(monkeypatch, [])
    config = _persons_turn()
    completed = await execute_ai_request(config, max_iterations=2)
    assert seen, "the send never happened: storage down blocked it"
    assert completed is not None
    kinds = [c.get("kind") for c in captured]
    assert "person_inline_media_store_failed" in kinds, kinds
    # The part kept its bytes; the id it was minted names no stored file, and every save says so.
    from matrx_ai.persistence.sealed import UNAVAILABLE_ATTACHMENT_KEY, person_media_upload_failed

    picture = config.messages[0].content[1]
    assert picture.base64_data and person_media_upload_failed(picture.file_id)
    saved = await _end_save(completed)
    assert not _media_ids(saved), f"a row names a file that was never stored: {saved}"
    assert [p for p in saved if UNAVAILABLE_ATTACHMENT_KEY in (p.get("metadata") or {})], saved
