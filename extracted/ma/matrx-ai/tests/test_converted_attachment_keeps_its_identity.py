"""A converted attachment keeps the identity label every other attachment carries.

Real test PB-05 (2026-11-08, snapshot a0b089e6): Claude Haiku 5.5 cannot read a .docx
(Anthropic document blocks take PDF and plain text only; the catalog lists input image + text),
so the media fallback extracts it to text: correct, and announced (``media_converted`` streamed,
``media_notices`` stored). But the PDF, photo, CSV and log each arrived behind
``<attachment kind name id/>`` while the converted .docx arrived as bare text with no kind and
no file id: the serializers label only MEDIA parts, and a conversion turns the item into text.

The law: every item the fallback converts, on every provider style, fresh or reused from an
earlier turn's conversion, opens with the same ``<attachment kind name id …/>`` label built
from the ORIGINAL item (its file id, its file name), saying it was converted.
"""

from __future__ import annotations

import base64
import io
from types import SimpleNamespace

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.media_config import DocumentContent
from matrx_ai.processing.media_fallback import preprocess_unsupported_media

DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
FILE_ID = "e820ba04-0fdc-4adf-a139-e98601e6339a"
# One endpoint per serializer style: anthropic, openai_responses, google, openai_chat, moonshot_chat.
ENDPOINTS = ["anthropic_chat", "openai_chat", "google_chat", "groq_chat", "moonshot_chat"]


def _docx() -> bytes:
    import docx

    d = docx.Document()
    d.add_paragraph("Shift handover — receiving")
    d.add_paragraph("Clerk code for receiving lines this week: RC-618.")
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


@pytest.fixture
def ambient(monkeypatch):
    import matrx_connect
    from matrx_connect.context import app_context

    class _Emitter:
        async def send_data(self, payload):
            return None

    ctx = SimpleNamespace(emitter=_Emitter(), metadata={}, request_id="req-1")
    monkeypatch.setattr(matrx_connect, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)
    return ctx


def _doc() -> DocumentContent:
    return DocumentContent(
        file_id=FILE_ID,
        base64_data=base64.b64encode(_docx()).decode("ascii"),
        mime_type=DOCX,
        metadata={"file_name": "handover-note.docx"},
    )


async def _converted(endpoint: str, doc: DocumentContent) -> TextContent:
    ml = MessageList(_messages=[UnifiedMessage(role="user", content=[doc])])
    out, _ = await preprocess_unsupported_media(
        ml, endpoint, model_name="claude-haiku-5-5", model_supports_vision=True
    )
    (only,) = [c for m in out.to_list() for c in m.content]
    assert isinstance(only, TextContent) and "RC-618" in only.text
    return only


def _assert_labelled(text: str, endpoint: str) -> None:
    head = text.strip().splitlines()[0]
    assert head.startswith("<attachment "), f"{endpoint}: converted docx has no identity label: {head!r}"
    assert 'kind="document"' in head, head
    assert 'name="handover-note.docx"' in head, head
    assert f'id="{FILE_ID}"' in head, head
    assert "converted" in head, f"{endpoint}: the label does not say the file was converted: {head!r}"


@pytest.mark.parametrize("endpoint", ENDPOINTS)
async def test_a_converted_docx_opens_with_its_identity_label(ambient, endpoint):
    _assert_labelled((await _converted(endpoint, _doc())).text, endpoint)


@pytest.mark.parametrize("endpoint", ENDPOINTS)
async def test_a_reused_conversion_keeps_the_label_exactly_once(ambient, endpoint):
    doc = _doc()
    await _converted(endpoint, doc)  # first turn: converts and caches on the item
    again = (await _converted(endpoint, doc)).text  # later turn: reuses the stored text
    _assert_labelled(again, endpoint)
    assert again.count("<attachment ") == 1, again


def test_the_label_reaches_the_anthropic_wire_once():
    """End of the line: the serialized user turn carries the label once, as text, before the body."""
    label = '<attachment kind="document" name="handover-note.docx" id="x" converted_to="text"/>'
    msg = UnifiedMessage(role="user", content=[TextContent(text=f"{label}\n[Attached file: a]\nRC-618")])
    blocks = msg.to_anthropic_blocks()
    assert len(blocks) == 1 and blocks[0]["text"].count("<attachment ") == 1


# ---------------------------------------------------------------------------
# A resized / re-encoded variant never replaces the file the person attached.
# PB-05 (2026-11-08): the photo's label read id 86037423 (the Anthropic-sized
# copy) while the person attached 4e01f58b. The variant pivot in
# ``matrx_files`` rewrote ``ref.file_id`` and the copy-back carried it onto
# the message item. The bytes may come from a variant; the identity never does.
# ---------------------------------------------------------------------------

MASTER_ID = "4e01f58b-0000-4000-8000-000000000001"
VARIANT_ID = str(__import__("uuid").uuid4())  # fresh byte-cache key per process


@pytest.fixture
def variant_world(monkeypatch):
    from matrx_files.cloud_sync import _media_resolution as res
    from matrx_files.cloud_sync import variants

    async def render(fm, file_id, *, variant_key, family):
        assert file_id == MASTER_ID
        return {"file_id": VARIANT_ID, "storage_uri": "s3://b/variant.jpg",
                "mime_type": "image/jpeg", "size_bytes": 3}

    monkeypatch.setattr(variants, "has_variant_encoder", lambda family: True)
    monkeypatch.setattr(variants, "render_variant_async", render)

    async def allow(fm, ref, *, is_share_link):
        return None

    monkeypatch.setattr(res, "_authorized_or_error_async", allow)
    reads: list[str] = []

    class _DB:
        async def get_file_async(self, file_id):
            assert file_id == MASTER_ID, file_id
            return {"owner_id": "u", "mime_type": "image/png", "size_bytes": 9,
                    "storage_uri": "s3://b/master.png", "file_name": "IMG_2291.jpg",
                    "current_version": 1}

    class _Router:
        async def read_async(self, uri):
            reads.append(uri)
            return b"jpg"

    class _FM:
        _sync_engine = SimpleNamespace(db=_DB(), _router=_Router())

        async def resolve_media_async(self, ref, *, needs_bytes=False, **_):
            return await res._resolve_media_async_impl(
                self, ref, needs_bytes=needs_bytes, presigned_ttl_seconds=60
            )

    return SimpleNamespace(fm=_FM(), reads=reads)


@pytest.mark.parametrize("style", ["anthropic", "google", "openai_responses"])
async def test_a_resized_image_keeps_the_attached_file_id(variant_world, style):
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.providers.unified_client import _resolve_media_ref_item

    image = ImageContent(file_id=MASTER_ID, mime_type="image/png", vision_class="anthropic_standard")
    await _resolve_media_ref_item(variant_world.fm, image)
    assert variant_world.reads in ([], ["s3://b/variant.jpg"]), variant_world.reads  # [] = byte-cache hit
    assert base64.b64decode(image.base64_data) == b"jpg" and image.mime_type == "image/jpeg"
    assert image.file_id == MASTER_ID, f"identity replaced by the resized copy: {image.file_id}"
    msg = UnifiedMessage(role="user", content=[image])
    if style == "anthropic":
        parts = [b.get("text", "") for b in msg.to_anthropic_blocks()]
    elif style == "google":
        parts = [p.get("text", "") for p in (msg.to_google_content() or {}).get("parts", [])]
    else:
        items = msg.to_openai_items()
        items = items if isinstance(items, list) else [items]
        parts = [c.get("text", "") for it in items for c in (it.get("content") or []) if isinstance(c, dict)]
    labels = [p for p in parts if p.startswith("<attachment ")]
    assert labels and f'id="{MASTER_ID}"' in labels[0] and VARIANT_ID not in labels[0], labels
