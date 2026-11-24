"""AN ATTACHMENT'S ID IS THE SERVER'S OWN, AND ITS STORED PART TELLS THE TRUTH (CGU-10 AND-IMG15, 2026-11-11).

The AND-V IMG14 checker pass found four claims any revert left green, and two stored-part defects. Each test
names the plant that turns it red:

* ``test_a_client_id_is_never_lent_to_other_content`` — a part carrying bytes AND a client-given ``file_id``
  lends that id to every other part with the same bytes (adoption of any id, not only server-minted ones):
  the other part names a file the person never stored and nothing is uploaded for it (#3).
* ``test_the_files_service_stores_under_the_minted_id`` — ``media_persistence`` ignores the caller's
  ``file_id`` (the row and its key minted afresh). Runs the REAL handler against an in-memory files service
  that mints its own id exactly as the real one does when none is given (#4, plant 8).
* ``test_a_file_stored_under_another_id_becomes_the_stand_in`` — the "stored under another id" check removed:
  the row would name the minted id while the file lives under another (#4, plant 9).
* ``test_an_uploading_document_is_sent_from_its_own_bytes`` — the document own-bytes skip removed: the media
  pass fetches an uploading PDF by an id with no stored file (#4, plant 6).
* ``test_a_stored_picture_names_its_files_mime_and_the_class_used`` — the stored part says ``image/jpeg``
  (the wire variant's mime) for a PNG file, or names a vision class whose encode failed (#2).
"""

from __future__ import annotations

import asyncio
import base64
import uuid
from io import BytesIO
from types import SimpleNamespace
from typing import Any

import pytest
from PIL import Image

from matrx_ai import _ext
from matrx_ai.config.media_config import DocumentContent, ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.persistence import sealed
from matrx_ai.providers.unified_client import UnifiedAIClient

_UNAVAILABLE = "attachment_unavailable"


def _png(size: tuple[int, int] = (3000, 2000)) -> str:
    buf = BytesIO()
    Image.new("RGB", size, (40, 120, 200)).save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages

    def __iter__(self):
        return iter(self._messages)


# ---------------------------------------------------------------------------------------------------------
# #3 — a client-supplied id is never adopted by other content
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_client_id_is_never_lent_to_other_content(monkeypatch) -> None:
    import matrx_ai.media.media_persistence as media_persistence

    uploads: list[str | None] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, **_: Any) -> SimpleNamespace:
        uploads.append(file_id)
        return SimpleNamespace(file_id=file_id, url=f"https://files.example/{file_id}", size_bytes=4)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    monkeypatch.setattr(sealed, "stores_person_media", lambda _ctx: True)
    monkeypatch.setattr(sealed, "blanks_content", lambda _ctx: False)

    blob = _png((8, 8))
    client_id = "c11e0700-0000-4000-8000-0000000000aa"  # a file id the CLIENT chose
    claimed = ImageContent(base64_data=blob, mime_type="image/png", file_id=client_id)
    other = ImageContent(base64_data=blob, mime_type="image/png")
    message = UnifiedMessage(role="user", content=[claimed, other])

    started = await sealed.keep_inline_person_media_on_server([message], SimpleNamespace(store=True, request_id="r"))
    await sealed.settle_person_media_uploads()

    assert claimed.file_id == client_id, "the client's own part lost the id it carries"
    assert other.file_id and other.file_id != client_id, (
        f"another part with the same bytes adopted the client-given id {client_id} without an upload"
    )
    assert started == 1 and uploads == [other.file_id], f"the other part was not stored under a minted id: {uploads}"
    assert sealed.server_minted_attachment_id(other.file_id)
    assert not sealed.server_minted_attachment_id(client_id)


@pytest.mark.asyncio
async def test_a_minted_id_is_still_shared_with_the_pristine_copy(monkeypatch) -> None:
    """The adoption stays for what it is FOR: a second pass over the same bytes (the pristine copy) takes the id
    THIS server minted, never a second upload."""
    import matrx_ai.media.media_persistence as media_persistence

    uploads: list[str | None] = []

    async def save(blob: str, mime: str, *, file_id: str | None = None, **_: Any) -> SimpleNamespace:
        uploads.append(file_id)
        return SimpleNamespace(file_id=file_id, url="u", size_bytes=4)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", save)
    monkeypatch.setattr(sealed, "stores_person_media", lambda _ctx: True)
    monkeypatch.setattr(sealed, "blanks_content", lambda _ctx: False)
    blob = _png((8, 8))
    first = ImageContent(base64_data=blob, mime_type="image/png")
    await sealed.keep_inline_person_media_on_server([UnifiedMessage(role="user", content=[first])], SimpleNamespace(store=True))
    copy_ = ImageContent(base64_data=blob, mime_type="image/png")
    message = UnifiedMessage(role="user", content=[first])
    message.user_content = [copy_]
    await sealed.keep_inline_person_media_on_server([message], SimpleNamespace(store=True))
    await sealed.settle_person_media_uploads()
    assert copy_.file_id == first.file_id and uploads == [first.file_id], uploads


# ---------------------------------------------------------------------------------------------------------
# #4 plants 8 + 9 — the REAL media_persistence against an in-memory files service
# ---------------------------------------------------------------------------------------------------------


class _InMemoryFileService:
    """The files service's ``upload_simple`` contract: the row (and its key) under ``file_id`` when the caller
    gives one, else an id it mints itself. ``honours_caller_id=False`` is an older service that always mints."""

    rows: dict[str, dict[str, Any]]

    def __init__(self, rows: dict[str, dict[str, Any]], honours_caller_id: bool) -> None:
        self.rows = rows
        self.honours = honours_caller_id

    async def upload_simple(self, body: bytes, *, file_path: str, user_id: str, mime_type: str, file_id: str | None = None, **kw: Any) -> Any:
        row_id = file_id if (file_id and self.honours) else str(uuid.uuid4())
        uri = f"s3://bucket/{user_id}/{row_id}"
        self.rows[row_id] = {
            "id": row_id,
            "owner_id": user_id,
            "file_name": file_path.rsplit("/", 1)[-1],
            "mime_type": mime_type,
            "storage_uri": uri,
            "canonical_storage_uri": uri,
            "size_bytes": len(body),
            "metadata": kw.get("metadata") or {},
            "published_to_web": kw.get("published_to_web"),
            "shown_to": kw.get("shown_to"),
        }
        return SimpleNamespace(file_id=row_id, storage_uri=uri, checksum="c")

    async def read_record_unchecked(self, file_id: str) -> dict[str, Any] | None:
        return self.rows.get(file_id)


def _real_handler_over(monkeypatch, rows: dict[str, dict[str, Any]], *, honours_caller_id: bool) -> None:
    import matrx_files

    import matrx_ai.media.media_persistence as mp

    class _Sync:
        user_id = "0wner000-0000-4000-8000-000000000001"

        async def build_urls_for_record_async(self, record: dict[str, Any]) -> dict[str, str]:
            return {"url": f"https://files.example/{record['id']}"}

        class db:  # noqa: N801 — the attribute the handler reads
            @staticmethod
            async def update_file_async(*_a: Any, **_k: Any) -> None:
                return None

        variants = None  # variant render is best-effort; it fails and the master stands

    fm = SimpleNamespace(sync_engine=_Sync())

    class _FS(_InMemoryFileService):
        @classmethod
        def for_file_manager(cls, _fm: Any) -> _FS:
            return cls(rows, honours_caller_id)

    monkeypatch.setattr(mp.AIMediaHandler.get_instance(), "_get_cloud_fm", lambda: fm)
    monkeypatch.setattr(matrx_files, "FileService", _FS)


@pytest.mark.asyncio
async def test_the_files_service_stores_under_the_minted_id(monkeypatch) -> None:
    rows: dict[str, dict[str, Any]] = {}
    _real_handler_over(monkeypatch, rows, honours_caller_id=True)
    minted = str(uuid.uuid4())

    await sealed._upload_person_attachment(minted, _png((16, 16)), "image/png", SimpleNamespace(store=True))

    assert minted not in sealed._FAILED_UPLOADS, sealed._FAILED_UPLOADS.get(minted)
    assert list(rows) == [minted], f"the person's file was stored under {list(rows)}, not the id its label named"
    assert rows[minted]["storage_uri"].endswith(f"/{minted}"), rows[minted]["storage_uri"]
    assert rows[minted]["metadata"].get("source") == "inline_media_part"


@pytest.mark.asyncio
async def test_a_file_stored_under_another_id_becomes_the_stand_in(monkeypatch) -> None:
    rows: dict[str, dict[str, Any]] = {}
    _real_handler_over(monkeypatch, rows, honours_caller_id=False)
    captured: list[dict[str, Any]] = []

    async def capture(exc: BaseException, **kw: Any) -> None:
        captured.append(kw)

    import matrx_connect.streaming.error_capture as error_capture

    monkeypatch.setattr(error_capture, "capture_error", capture)
    minted = str(uuid.uuid4())

    await sealed._upload_person_attachment(minted, _png((16, 16)), "image/png", SimpleNamespace(store=True))

    assert minted not in rows and len(rows) == 1
    assert minted in sealed._FAILED_UPLOADS, "a file stored under another id was taken as stored under the minted one"
    stored = await sealed.stored_message_content(
        [{"type": "media", "kind": "image", "origin": "matrx", "file_id": minted, "mime_type": "image/png"}],
        SimpleNamespace(store=True),
    )
    assert _UNAVAILABLE in (stored[0].get("metadata") or {}), f"the row names a file that does not exist: {stored}"
    assert [c for c in captured if c.get("kind") == "person_inline_media_store_failed"]


# ---------------------------------------------------------------------------------------------------------
# #4 plant 6 — an uploading document is sent from its own bytes, never fetched by id
# ---------------------------------------------------------------------------------------------------------


class _StorageThatHasNoSuchFile:
    def __init__(self) -> None:
        self.lookups: list[str] = []

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        self.lookups.append(str(ref.file_id))
        raise FileNotFoundError(f"no stored file {ref.file_id}")


@pytest.mark.asyncio
@pytest.mark.parametrize("state", ["uploading", "failed"])
async def test_an_uploading_document_is_sent_from_its_own_bytes(monkeypatch, state) -> None:
    storage = _StorageThatHasNoSuchFile()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: storage)
    minted = str(uuid.uuid4())
    never = asyncio.get_running_loop().create_future()
    if state == "uploading":
        monkeypatch.setitem(sealed._IN_FLIGHT, minted, never)
    else:
        monkeypatch.setitem(sealed._FAILED_UPLOADS, minted, "ConnectionError")
    pdf = base64.b64encode(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF").decode("ascii")
    document = DocumentContent(file_id=minted, base64_data=pdf, mime_type="application/pdf")
    messages = _Messages([UnifiedMessage(role="user", content=[document])])

    await asyncio.wait_for(
        UnifiedAIClient()._annotate_and_resolve_image_refs(
            messages, model_name="mock-model", wire_format="anthropic", supports_vision=True
        ),
        timeout=10,
    )
    never.cancel()

    assert storage.lookups == [], f"the media pass fetched an uploading document by id: {storage.lookups}"
    assert document.base64_data == pdf and document.file_id == minted


# ---------------------------------------------------------------------------------------------------------
# #2 — the stored part names its file's mime and the class actually used
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_stored_picture_names_its_files_mime_and_the_class_used(monkeypatch) -> None:
    storage = _StorageThatHasNoSuchFile()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: storage)
    minted = str(uuid.uuid4())
    never = asyncio.get_running_loop().create_future()
    monkeypatch.setitem(sealed._IN_FLIGHT, minted, never)
    picture = ImageContent(file_id=minted, base64_data=_png(), mime_type="image/png")
    messages = _Messages([UnifiedMessage(role="user", content=[picture])])

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages, model_name="gpt-5.5", wire_format="openai", supports_vision=True
    )
    never.cancel()

    assert picture.mime_type == "image/jpeg", "the wire bytes are the class's JPEG (precondition)"
    stored = picture.to_storage_dict()
    assert stored["mime_type"] == "image/png", f"the stored part says {stored['mime_type']} for a PNG file"
    assert (stored.get("metadata") or {}).get("vision_class") == "openai_original"


@pytest.mark.asyncio
async def test_a_variant_fetched_by_id_keeps_the_files_mime(monkeypatch) -> None:
    class _StorageWithAJpegVariant:
        async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
            ref.base64_data = base64.b64encode(b"\xff\xd8jpeg").decode()
            ref.mime_type = "image/jpeg"
            ref.is_resolved = True
            return ref

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _StorageWithAJpegVariant())
    picture = ImageContent(file_id=str(uuid.uuid4()), mime_type="image/png")
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[picture])]),
        model_name="gpt-5.5",
        wire_format="openai",
        supports_vision=True,
    )
    assert picture.mime_type == "image/jpeg"
    assert picture.to_storage_dict()["mime_type"] == "image/png"


@pytest.mark.asyncio
async def test_a_failed_encode_names_no_class(monkeypatch) -> None:
    storage = _StorageThatHasNoSuchFile()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: storage)
    import matrx_connect.streaming.error_capture as error_capture

    async def capture(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(error_capture, "capture_error", capture)
    minted = str(uuid.uuid4())
    monkeypatch.setitem(sealed._FAILED_UPLOADS, minted, "ConnectionError")
    not_a_picture = base64.b64encode(b"not an image at all").decode()
    picture = ImageContent(file_id=minted, base64_data=not_a_picture, mime_type="image/png")
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[picture])]),
        model_name="gpt-5.5",
        wire_format="openai",
        supports_vision=True,
    )
    stored = picture.to_storage_dict()
    assert picture.base64_data == not_a_picture and stored["mime_type"] == "image/png"
    assert "vision_class" not in (stored.get("metadata") or {}), f"a class that was never applied is recorded: {stored}"
