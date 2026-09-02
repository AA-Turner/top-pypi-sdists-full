"""THE GUARD: a tool output's media blob becomes an IDENTITY, never a signed URL.

Third sibling of ``test_media_output_durability.py`` (the media blocks) and
``test_media_identity_consumers.py`` (the two consumers that dropped the id).
This file guards the last producer that still manufactured one.

``persist_media_blobs_async`` used to rewrite ``{x}_base64`` into ``{x}_url``
by way of the url-only persist shim. For any feature that is not ``ai_audio``
that url is a ~1-hour signed S3 link, and this path is reached for EVERY
client-delegated tool result (matrx-local desktop, the Chrome extension)
carrying a non-image blob. The url then landed in three places at once:

  (a) ``cx_tool_call.output`` — a DB column, permanently;
  (b) the rendered tool card;
  (c) the model's context, where it can be pasted into the answer — which is
      exactly how expiring URLs got frozen into ``chat.message``.

The fix emits the same ``{kind, media_ref: {file_id}, media_type, size_bytes}``
envelope the image funnel emits. If a test here fails, do NOT relax it.
"""

from __future__ import annotations

import json

import pytest
from matrx_files import is_signed_url

from matrx_ai.media import media_persistence
from matrx_ai.media.media_persistence import (
    MediaPersistResult,
    _ref_kind_and_feature,
    persist_media_blobs_async,
)

FILE_ID = "6feae31a-945b-4dcc-8fc0-2041bb76c6b1"
OWNER = "4cf62e4e-2679-484f-b652-034e697418df"

SIGNED_URL = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?X-Amz-Credential=AKIA%2F20260811%2Fus-west-1%2Fs3%2Faws4_request"
    "&X-Amz-Date=20260811T000000Z&X-Amz-Expires=3600&X-Amz-Signature=deadbeef"
)

# "matrx" in ascii, base64 — real base64 so the size math is checkable.
BLOB = "bWF0cng="


def _envelope(file_id: str | None = FILE_ID, mime: str = "audio/mpeg") -> MediaPersistResult:
    """An envelope whose every URL flavour is a signed, expiring link — the
    realistic case for any feature that is not ``ai_audio``. Nothing here may
    survive into the rewritten output except the id."""
    return MediaPersistResult(
        file_id=file_id,
        storage_uri=f"s3://matrx-user-files/{OWNER}/{FILE_ID}",
        mime_type=mime,
        file_path=f"{OWNER}/{FILE_ID}",
        url=SIGNED_URL,
        cdn_url=None,
        download_url=SIGNED_URL,
        visibility="personal",
        file_name="clip.mp3",
        size_bytes=6,
    )


@pytest.fixture
def persisted(monkeypatch):
    """Record every persist call and hand back a signed-url-only envelope."""
    calls: list[dict] = []

    async def _fake(content, mime_type, **kwargs):
        calls.append({"content": content, "mime_type": mime_type, **kwargs})
        return _envelope(mime=mime_type)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", _fake)
    return calls


def _walk_strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _walk_strings(v)]
    if isinstance(value, list | tuple):
        return [s for v in value for s in _walk_strings(v)]
    return []


# ===========================================================================
# 1. Mime → kind routing
# ===========================================================================


class TestRefKindRouting:
    @pytest.mark.parametrize(
        ("mime", "kind", "feature"),
        [
            ("audio/mpeg", "audio_ref", "ai_audio"),
            ("audio/wav; codecs=1", "audio_ref", "ai_audio"),
            ("video/mp4", "video_ref", "ai_video"),
            ("application/pdf", "document_ref", "ai_documents"),
            ("image/png", "image_ref", "ai_images"),
        ],
    )
    def test_known_families(self, mime: str, kind: str, feature: str) -> None:
        assert _ref_kind_and_feature(mime) == (kind, feature)

    @pytest.mark.parametrize(
        "mime",
        [
            "application/octet-stream",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/csv",
            "",
        ],
    )
    def test_everything_else_is_a_plain_file_ref(self, mime: str) -> None:
        # Deliberate: no provider has a native content block for these, so the
        # envelope reaches the model as JSON carrying the file_id — the handle
        # a file-reading tool needs. Calling a .docx a `document_ref` would
        # build a DocumentContent no provider can send.
        assert _ref_kind_and_feature(mime)[0] == "file_ref"


# ===========================================================================
# 2. The rewrite — identity in, blob and url out
# ===========================================================================


class TestPersistMediaBlobs:
    @pytest.mark.asyncio
    async def test_single_blob_becomes_the_media_envelope(self, persisted) -> None:
        out = await persist_media_blobs_async(
            {"audio_base64": BLOB, "media_type": "audio/mpeg", "transcript": "hi"}
        )

        assert out["kind"] == "audio_ref"
        assert out["media_ref"] == {"file_id": FILE_ID, "mime_type": "audio/mpeg"}
        assert out["file_id"] == FILE_ID
        assert out["media_type"] == "audio/mpeg"
        assert out["size_bytes"] == 6
        # The tool's own payload is untouched.
        assert out["transcript"] == "hi"
        # The blob never reaches the model.
        assert "audio_base64" not in out

    @pytest.mark.asyncio
    async def test_the_persist_call_is_routed_to_the_right_feature(self, persisted) -> None:
        await persist_media_blobs_async({"video_base64": BLOB, "media_type": "video/mp4"})
        assert persisted[0]["feature"] == "ai_video"
        assert persisted[0]["content"] == BLOB

    @pytest.mark.asyncio
    async def test_mime_falls_back_to_the_blob_key_name(self, persisted) -> None:
        out = await persist_media_blobs_async({"pdf_base64": BLOB})
        assert out["kind"] == "document_ref"
        assert persisted[0]["mime_type"] == "application/pdf"

    @pytest.mark.asyncio
    async def test_a_producer_supplied_url_is_dropped_with_its_blob(self, persisted) -> None:
        # A client that sent BOTH a blob and its own expiring link must not
        # leave the link behind as the durable-looking survivor.
        out = await persist_media_blobs_async(
            {"audio_base64": BLOB, "audio_url": SIGNED_URL, "media_type": "audio/mpeg"}
        )
        assert "audio_url" not in out
        assert out["file_id"] == FILE_ID

    @pytest.mark.asyncio
    async def test_several_blobs_all_survive_as_a_list(self, persisted) -> None:
        out = await persist_media_blobs_async(
            {"audio_base64": BLOB, "pdf_base64": BLOB, "note": "two attachments"}
        )
        assert out["kind"] == "media_ref_list"
        assert out["count"] == 2
        assert {item["source_key"] for item in out["items"]} == {"audio_base64", "pdf_base64"}
        assert all(item["media_ref"]["file_id"] == FILE_ID for item in out["items"])
        assert out["note"] == "two attachments"
        assert not any(k.endswith("_base64") for k in out)

    @pytest.mark.asyncio
    async def test_non_blob_output_is_returned_untouched(self, persisted) -> None:
        original = {"rows": [1, 2, 3], "status": "ok"}
        assert await persist_media_blobs_async(original) == original
        assert persisted == []


# ===========================================================================
# 3. The failure branch — mirrors upload_image_master exactly
# ===========================================================================


class TestPersistFailure:
    @pytest.mark.asyncio
    async def test_upload_failure_strips_the_blob_and_reports_it(self, monkeypatch) -> None:
        async def _boom(content, mime_type, **kwargs):
            raise RuntimeError("s3 down")

        monkeypatch.setattr(media_persistence, "save_media_envelope_async", _boom)

        out = await persist_media_blobs_async({"audio_base64": BLOB, "media_type": "audio/mpeg"})

        # Never ship raw base64 into the context window, even on failure.
        assert "audio_base64" not in out
        assert BLOB not in json.dumps(out)
        assert out["media_ref"] is None
        assert "s3 down" in out["media_ref_error"]
        assert out["kind"] == "audio_ref"

    @pytest.mark.asyncio
    async def test_an_envelope_without_a_file_id_is_refused(self, monkeypatch) -> None:
        # A reference with no identity is worse than an honest failure: it
        # looks durable and re-mints nothing.
        async def _idless(content, mime_type, **kwargs):
            return _envelope(file_id=None, mime=mime_type)

        monkeypatch.setattr(media_persistence, "save_media_envelope_async", _idless)

        out = await persist_media_blobs_async({"audio_base64": BLOB, "media_type": "audio/mpeg"})
        assert out["media_ref"] is None
        assert out["media_ref_error"] == "persist_returned_no_file_id"


# ===========================================================================
# 4. THE REGRESSION LOCK — no signed URL can reach cx_tool_call.output
# ===========================================================================


class TestNoSignedUrlReachesToolCallOutput:
    """``aidream/services/ai_execution/tool_results.py`` hands the rewritten
    dict straight to ``cx_tool_call.output`` (a DB column), the tool card, and
    the model's replayed context. Whatever this function returns is what lands
    there — so nothing it returns may be a signed URL."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "output",
        [
            {"audio_base64": BLOB, "media_type": "audio/mpeg"},
            {"video_base64": BLOB, "media_type": "video/mp4"},
            {"pdf_base64": BLOB, "media_type": "application/pdf"},
            {"file_base64": BLOB, "media_type": "application/octet-stream"},
            {"data_base64": BLOB},
            {"audio_base64": BLOB, "pdf_base64": BLOB},
            {"audio_base64": BLOB, "audio_url": SIGNED_URL, "media_type": "audio/mpeg"},
        ],
    )
    async def test_nothing_signed_survives_the_rewrite(self, persisted, output: dict) -> None:
        rewritten = await persist_media_blobs_async(output)

        for text in _walk_strings(rewritten):
            assert not is_signed_url(text), f"signed URL leaked into tool output: {text[:120]}"
        # Belt and braces: the envelope's url flavours are all this one string.
        assert SIGNED_URL not in json.dumps(rewritten)
        # And the identity IS there, so the FE/model can re-mint on demand.
        assert FILE_ID in json.dumps(rewritten)

    @pytest.mark.asyncio
    async def test_a_signed_url_the_tool_itself_reported_is_not_our_doing(
        self, persisted
    ) -> None:
        # Scope statement: this function owns what IT manufactures. A url the
        # tool put under an unrelated key is the tool's payload and is left
        # alone — the guard above must not be read as sanitising arbitrary
        # fields, or a future author will "fix" it in the wrong place.
        out = await persist_media_blobs_async(
            {"audio_base64": BLOB, "media_type": "audio/mpeg", "page_visited": SIGNED_URL}
        )
        assert out["page_visited"] == SIGNED_URL
        assert out["file_id"] == FILE_ID


# ===========================================================================
# 5. The model can actually CONSUME the shape
# ===========================================================================


class TestToolResultBlocks:
    def _content(self, output: dict):
        from matrx_ai.tools.models import ToolResult

        return ToolResult(
            success=True, output=output, tool_name="desktop_record", call_id="c1"
        ).to_tool_result_content()["content"]

    def test_audio_ref_becomes_an_audio_block_addressed_by_file_id(self) -> None:
        from matrx_ai.config import AudioContent

        blocks = self._content(
            {
                "kind": "audio_ref",
                "media_ref": {"file_id": FILE_ID, "mime_type": "audio/mpeg"},
                "media_type": "audio/mpeg",
                "size_bytes": 6,
            }
        )
        audio = [b for b in blocks if isinstance(b, AudioContent)]
        assert len(audio) == 1
        assert audio[0].file_id == FILE_ID
        assert audio[0].url is None  # identity only — never a handoff url

    def test_video_ref_becomes_a_video_block(self) -> None:
        from matrx_ai.config import VideoContent

        blocks = self._content(
            {
                "kind": "video_ref",
                "media_ref": {"file_id": FILE_ID, "mime_type": "video/mp4"},
                "media_type": "video/mp4",
            }
        )
        video = [b for b in blocks if isinstance(b, VideoContent)]
        assert len(video) == 1 and video[0].file_id == FILE_ID

    def test_a_failed_ref_tells_the_model_instead_of_pretending(self) -> None:
        from matrx_ai.config import AudioContent, TextContent

        blocks = self._content(
            {
                "kind": "audio_ref",
                "media_ref": None,
                "media_ref_error": "upload_failed: RuntimeError: s3 down",
                "media_type": "audio/mpeg",
            }
        )
        assert not any(isinstance(b, AudioContent) for b in blocks)
        assert any(
            isinstance(b, TextContent) and "audio attachment unavailable" in b.text
            for b in blocks
        )

    def test_the_details_block_carries_the_file_id_and_the_payload(self) -> None:
        from matrx_ai.config import TextContent

        blocks = self._content(
            {
                "kind": "audio_ref",
                "media_ref": {"file_id": FILE_ID, "mime_type": "audio/mpeg"},
                "media_type": "audio/mpeg",
                "transcript": "hello there",
            }
        )
        details = json.loads([b for b in blocks if isinstance(b, TextContent)][-1].text)
        assert details["attached_file_id"] == FILE_ID
        assert details["transcript"] == "hello there"

    def test_media_ref_list_gives_the_model_every_item(self) -> None:
        from matrx_ai.config import AudioContent, DocumentContent, TextContent

        blocks = self._content(
            {
                "kind": "media_ref_list",
                "count": 2,
                "items": [
                    {
                        "kind": "audio_ref",
                        "media_ref": {"file_id": FILE_ID, "mime_type": "audio/mpeg"},
                        "media_type": "audio/mpeg",
                    },
                    {
                        "kind": "document_ref",
                        "media_ref": {"file_id": FILE_ID, "mime_type": "application/pdf"},
                        "media_type": "application/pdf",
                    },
                ],
                "note": "two attachments",
            }
        )
        assert any(isinstance(b, AudioContent) for b in blocks)
        assert any(isinstance(b, DocumentContent) for b in blocks)
        rest = json.loads([b for b in blocks if isinstance(b, TextContent)][-1].text)
        assert rest["note"] == "two attachments"

    def test_a_file_ref_reaches_the_model_as_json_with_its_id(self) -> None:
        # No native block exists for an opaque file; the id must still be
        # readable so a file-reading tool can pick it up.
        content = self._content(
            {
                "kind": "file_ref",
                "media_ref": {"file_id": FILE_ID, "mime_type": "application/octet-stream"},
                "media_type": "application/octet-stream",
            }
        )
        assert isinstance(content, str) and FILE_ID in content


# ===========================================================================
# 6. The url-only contract is GONE, not deprecated
# ===========================================================================


def test_the_url_only_persist_shim_no_longer_exists() -> None:
    import matrx_ai.media as media_pkg

    assert not hasattr(media_pkg, "save_media_async")
    assert not hasattr(media_persistence, "save_media_async")
    assert not hasattr(media_persistence.AIMediaHandler, "save_response_media_async")
