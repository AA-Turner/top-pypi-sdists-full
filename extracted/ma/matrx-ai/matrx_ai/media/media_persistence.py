"""AI media persistence — routes through the cloud_sync FileManager.

Saves AI-generated media (audio, images, video, PDFs) to cloud storage
and returns the canonical asset envelope for the frontend.

Public API:
    save_media_envelope_async(content, mime_type, ..., visibility=None)
        -> MediaPersistResult — preferred. Returns the full envelope:
        {file_id, url, cdn_url, download_url, mime_type, storage_uri}.
        Every URL is durable; FE re-resolves by file_id via the
        /assets/{id} endpoint when it needs a fresh flavour.

    save_media(content, mime_type, audio_format=None) -> str
        — SYNC-ONLY shim returning just the inline URL, for the handful
        of sync provider adapters that cannot await. It is a HANDOFF
        url, never an identity: nothing may store what it returns. Any
        async caller uses save_media_envelope_async and keeps file_id.

    fetch_media(url, target_format="base64") -> str | bytes

URL contract: every URL comes from
``SyncEngine.build_urls_for_record_async`` — the single source of truth
that decides CDN vs authenticated-download based on the record's
visibility, and that returns only durable URLs (``url`` / ``cdn_url`` /
``download_url``). We **never** call ``_router.get_url_async``
directly here (banned anti-pattern per CLAUDE.md "Asset uploads" rule).

Audio pipeline stages:
    1. Base64 decode if needed
    2. PCM (audio/L16, audio/pcm) normalized to WAV with RIFF header
    3. Optional transcode via pydub
    4. Upload via FileService.upload_simple + canonical URL envelope
"""

from __future__ import annotations

import asyncio
import base64
import struct
import uuid
from dataclasses import dataclass
from typing import Literal

from matrx_utils import VisibilityLiteral, vcprint
from matrx_utils.ctx import public_media_scope as public_media_scope
from matrx_utils.ctx import public_media_scope_active as public_media_scope_active

from matrx_ai._ext import get_ext, has_ext

# Features whose generated assets are BORN PUBLIC (durable CDN URL, never an
# expiring signed URL) when the caller does not pass an explicit visibility.
#
# Why ``ai_audio``: agent-generated TTS/audio delivered into a conversation is
# content the user replays indefinitely — a personal file mints a signed S3 URL
# that expires days later and silently breaks playback (matrx-frontend
# FOUND_DEFECTS D1). This mirrors the podcast persist boundary
# (``_persist_episode`` → ``make_urls_durable``), scoped to audio only.
#
# Deliberately NOT ``ai_images`` / ``ai_video`` / ``ai_documents`` — flipping
# those would make every AI image/video on the platform public, a privacy
# regression. An explicit ``visibility=`` argument always wins over this map.
BORN_PUBLIC_FEATURES: frozenset[str] = frozenset({"ai_audio"})


# THE PUBLISHED-MEDIA SCOPE now lives in ``matrx_utils.ctx`` — one layer down,
# beside ``system_file_access`` and ``VisibilityLiteral``.
#
# It moved there because it was unreachable from where it was most needed. A
# publishing WORKFLOW (podcast W7's visual-asset fan-out) runs in matrx-graph,
# which cannot import matrx-ai; so a workflow had no way to say what
# ``podcast_generator.py`` says in Python, and every image it produced was born
# personal with an expiring URL that got frozen into ``workflow.node_outcome``.
# Re-exported here because ``matrx_ai.media`` is the import path every media
# caller already uses.


def resolve_default_visibility(
    feature: str,
    visibility: VisibilityLiteral | None,
) -> VisibilityLiteral:
    """Resolve the effective visibility for a persisted AI asset.

    Explicit caller choice always wins; otherwise, in precedence order:
    an active :func:`public_media_scope` → ``public``,
    ``BORN_PUBLIC_FEATURES`` → ``public``, everything else → ``personal``.
    """
    if visibility is not None:
        return visibility
    if public_media_scope_active():
        return "public"
    return "public" if feature in BORN_PUBLIC_FEATURES else "personal"


@dataclass(frozen=True)
class MediaPersistResult:
    """Canonical envelope returned by ``save_media_envelope_async``.

    Mirrors the AssetVariant URL contract (every URL flavour the FE
    might need) plus the ``file_id`` — the durable identity every
    consumer stores and re-resolves from.
    """

    file_id: str
    storage_uri: str
    mime_type: str
    file_path: str
    # URL flavours — populated by SyncEngine.build_urls_for_record_async.
    url: str | None = None  # inline-render URL (CDN if public, authenticated route otherwise)
    cdn_url: str | None = None  # permanent CDN URL (public only)
    download_url: str | None = None  # durable attachment-disposition URL
    visibility: str = "personal"
    file_name: str | None = None
    size_bytes: int | None = None
    # Phase 3b: intrinsic dimensions/duration/page_count probed at write
    # time so the content classes (ImageContent/AudioContent/etc.) carry
    # them straight through to cx_message storage without a follow-up
    # query.
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None
    page_count: int | None = None


class AIMediaHandler:
    """Persists AI-generated media through the cloud_sync FileManager."""

    _instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Public writes
    # ------------------------------------------------------------------

    def save_response_media(
        self,
        content: str | bytes,
        mime_type: str,
        audio_format: str | None = None,
    ) -> str:
        """Synchronous save — uses sync ``managed_write`` + the central
        URL builder. Blocks the event loop in async code; prefer
        ``save_response_media_async`` / ``save_response_media_envelope_async``.
        """
        raw_bytes = self._resolve_to_bytes_sync(content)
        body, effective_mime, path, new_file_id = self._prepare_media(
            raw_bytes,
            mime_type,
            audio_format,
        )

        fm = self._get_cloud_fm()
        # NOTE: managed_write (sync) doesn't yet accept the file_id pin
        # for the canonical-key scheme; sync callers stay on the legacy
        # path and rely on the fire-and-forget rekey backfill. Prefer
        # save_response_media_envelope_async whenever possible.
        result = fm.sync_engine.managed_write(
            path,
            body,
            mime_type=effective_mime,
            visibility="personal",
            change_summary="AI-generated media",
            metadata={"source": "ai_media", "mime_type": effective_mime},
        )
        # Central URL builder — no _router reach.
        urls = fm.sync_engine.build_urls_for_record(
            {
                "id": result.file_id,
                "visibility": "personal",
                "storage_uri": result.storage_uri,
                "checksum": result.checksum,
                "file_name": path.rsplit("/", 1)[-1],
                "mime_type": effective_mime,
                "deleted_at": None,
            },
        )
        return urls.get("url") or result.storage_uri

    async def save_response_media_envelope_async(
        self,
        content: str | bytes,
        mime_type: str,
        audio_format: str | None = None,
        *,
        visibility: VisibilityLiteral | None = None,
        prompt: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        feature: str = "ai_images",
        extra_metadata: dict | None = None,
    ) -> MediaPersistResult:
        """Persist + return the full envelope (file_id + URL flavours).

        Routes through ``FileService.upload_simple`` so the standard
        upload orchestration runs, then mints URLs through
        ``SyncEngine.build_urls_for_record_async`` so the FE gets the
        canonical inline + CDN + download trio.

        ``prompt`` is the natural-language description the user (or
        upstream agent) supplied. Used two ways:
          1. Drives a descriptive filename via
             ``naming.slugify_prompt(prompt, content_bytes=...)``.
          2. Persisted in metadata so audit / search / reviewer UIs
             can show "what made this".

        ``feature`` picks the canonical system folder
        (``ai_images`` / ``ai_audio`` / ``ai_video`` / ``ai_documents``).
        Defaults to ``ai_images``; callers MUST override for audio /
        video / document generation so the file lands under the right
        ``generations/<feature>/`` root.

        ``visibility=None`` (the default) resolves per feature via
        :func:`resolve_default_visibility` — ``ai_audio`` is born public
        (durable CDN URL; D1 chat-audio fix), everything else personal.
        """
        visibility = resolve_default_visibility(feature, visibility)
        raw_bytes = await self._resolve_to_bytes_async(content)
        loop = asyncio.get_event_loop()
        body, effective_mime, _legacy_path, new_file_id = await loop.run_in_executor(
            None,
            self._prepare_media,
            raw_bytes,
            mime_type,
            audio_format,
        )

        # Filename: prompt-derived slug if we have a prompt, otherwise
        # the file_id (legacy behavior). Both get the right extension
        # from the sniffed mime.
        from matrx_files import get_system_folder

        from .naming import slugify_prompt

        folder = get_system_folder(feature)
        ext = self._get_extension_from_mime(effective_mime) or ""
        if prompt:
            slug = slugify_prompt(prompt, content_bytes=body)
        else:
            slug = new_file_id
        filename = f"{slug}{ext}"
        path = folder.path(filename)

        fm = self._get_cloud_fm()
        from matrx_files import FileService

        file_service = FileService.for_file_manager(fm)

        # Compose metadata: keep `source` / `mime_type` for back-compat,
        # add prompt + model + provider so the FE / audit UI can render
        # provenance directly off the row.
        meta: dict = {
            "source": "ai_media",
            "mime_type": effective_mime,
            "feature": feature,
        }
        if prompt:
            # Keep prompts bounded — first 4 KB is plenty for context.
            meta["prompt"] = prompt[:4096]
        if model:
            meta["model"] = model
        if provider:
            meta["provider"] = provider
        if extra_metadata:
            for k, v in extra_metadata.items():
                meta.setdefault(k, v)

        # Pin the cld_files row id + S3 key to `new_file_id` so the row
        # is born canonical (storage_uri == canonical_storage_uri ==
        # <backend>://<bucket>/<owner>/<file_id>). Any URL the builder
        # mints therefore carries file_id in its path — no rekey
        # backfill, no dual-path confusion.
        result = await file_service.upload_simple(
            body,
            file_path=path,
            user_id=fm.sync_engine.user_id,
            mime_type=effective_mime,
            visibility=visibility,
            change_summary="AI-generated media",
            metadata=meta,
            auto_thumbnail=True,
            auto_rekey=False,  # already canonical; nothing to rekey
            file_id=new_file_id,
        )

        # Load the freshly-written record so build_urls_for_record_async
        # sees the same shape it sees everywhere else (no inferred values).
        record = await fm.sync_engine.db.get_file_async(result.file_id)
        if record is None:
            record = {
                "id": result.file_id,
                "visibility": visibility,
                "storage_uri": result.storage_uri,
                "canonical_storage_uri": result.storage_uri,
                "checksum": result.checksum,
                "file_name": filename,
                "mime_type": effective_mime,
                "deleted_at": None,
            }
        urls = await fm.sync_engine.build_urls_for_record_async(record)

        # Phase 1: render the SOCIAL_BASELINE variants (og / thumbnail /
        # tiny) for AI-generated media regardless of mime kind. Uses the
        # universal thumbnail dispatcher so PDFs/videos/audio get the
        # same treatment as images. Phase 1c: also render kind-specific
        # full-resolution variants (page1_url for PDFs, poster_url for
        # videos) so DocumentBlock / VideoBlock can carry a browser-
        # renderable primary representation. Best-effort: failures don't
        # block the master write.
        master_record_for_variants = (
            record
            if isinstance(record, dict)
            else {
                "id": result.file_id,
                "owner_id": fm.sync_engine.user_id,
                "storage_uri": result.storage_uri,
                "visibility": visibility,
            }
        )
        # Hoisted from inside the try-block (Phase 3b) so the probed
        # dimensions are visible to the MediaPersistResult construction
        # after the try/except even when variant rendering fails.
        probed: dict = {}
        try:
            from matrx_files import SOCIAL_BASELINE
            from matrx_files.specific_handlers.thumbnail_source import (
                probe_source_metadata,
                render_kind_specific_variants,
                render_thumbnail_source_bytes,
            )

            # Phase 1d.1: probe width/height/duration_ms/page_count and
            # persist to the cld_files row so DocumentBlock.page_count +
            # AudioBlock.duration_ms etc. populate from the row.
            probed = await probe_source_metadata(
                body,
                effective_mime,
                file_name=filename,
            )
            col_updates: dict = {}
            if probed.get("width") is not None:
                col_updates["width"] = probed["width"]
            if probed.get("height") is not None:
                col_updates["height"] = probed["height"]
            if probed.get("duration_ms") is not None:
                col_updates["duration_ms"] = probed["duration_ms"]
            if probed.get("page_count") is not None:
                # No dedicated column — stamp into metadata.
                base_meta = (record.get("metadata") or {}) if isinstance(record, dict) else {}
                col_updates["metadata"] = {
                    **base_meta,
                    "page_count": probed["page_count"],
                }
            if col_updates:
                try:
                    await fm.sync_engine.db.update_file_async(result.file_id, col_updates)
                except Exception:
                    pass  # Non-fatal — column stays null for this row.

            raster_bytes, _raster_mime = await render_thumbnail_source_bytes(
                body,
                effective_mime,
                file_name=filename,
            )
            await fm.sync_engine.variants.render_async(
                master_record_for_variants,
                variants_specs=list(SOCIAL_BASELINE),
                master_bytes=raster_bytes,
            )

            # Phase 1c — kind-specific full-res variants.
            kind_variants = await render_kind_specific_variants(
                body,
                effective_mime,
                file_name=filename,
            )
            for key, content, kmime, family in kind_variants:
                await fm.sync_engine.variants.persist_prerendered_async(
                    master_record_for_variants,
                    variant_key=key,
                    content=content,
                    mime_type=kmime,
                    variant_family=family,
                )
        except Exception:
            # Don't let variant rendering errors break the AI generation
            # response — the master write succeeded, which is what the
            # caller asked for.
            import logging

            logging.getLogger(__name__).debug(
                "save_response_media_envelope_async: variant render "
                "failed (master file_id=%s) — proceeding without variants",
                result.file_id,
                exc_info=True,
            )

        # Phase 3b: surface probed dimensions on the result envelope so
        # downstream content blocks (ImageContent / AudioContent / etc.)
        # carry them straight into cx_message storage without a follow-up
        # cld_files re-query. The ``probed`` dict was populated above in
        # the same execution path.
        return MediaPersistResult(
            file_id=result.file_id,
            storage_uri=result.storage_uri,
            mime_type=effective_mime,
            file_path=path,
            url=urls.get("url"),
            cdn_url=urls.get("cdn_url"),
            download_url=urls.get("download_url"),
            visibility=visibility,
            file_name=(record.get("file_name") if isinstance(record, dict) else None) or filename,
            size_bytes=(record.get("size_bytes") if isinstance(record, dict) else None),
            width=probed.get("width"),
            height=probed.get("height"),
            duration_ms=probed.get("duration_ms"),
            page_count=probed.get("page_count"),
        )

    # ------------------------------------------------------------------
    # Fetch
    # ------------------------------------------------------------------

    def fetch_media(
        self, url: str, target_format: Literal["base64", "bytes"] = "base64"
    ) -> str | bytes:
        # Resolve through the canonical FileManager primitive so one of OUR
        # share-link / /files/{id} URLs is read from S3 (never by scraping
        # share-page HTML); a genuinely-external URL falls back to a direct
        # fetch inside the helper. Used e.g. by Groq transcription to pull an
        # audio URL before sending bytes to the provider.
        content = AIMediaHandler._resolve_url_to_bytes_sync(url)
        if target_format == "base64":
            return base64.b64encode(content).decode("utf-8")
        return content

    # ==================================================================
    # Internals
    # ==================================================================

    def _get_cloud_fm(self):
        if not has_ext("get_cloud_file_manager"):
            raise RuntimeError(
                "matrx-ai media persistence requires the 'get_cloud_file_manager' "
                "extension. Ensure aidream.package_integration.configure_packages() "
                "has been called at startup."
            )
        return get_ext("get_cloud_file_manager")()

    # ------------------------------------------------------------------
    # Content → bytes resolution
    # ------------------------------------------------------------------
    # `save_media_async` historically accepted `str | bytes` where the string
    # was assumed to be bare base64. That broke for any provider whose
    # `GeneratedAsset` carries a `url` instead of inline bytes (Replicate
    # video/image, Together image, etc.) — those URLs reached `_prepare_media`
    # and got `b64decode`'d into "Incorrect padding" failures. The resolver
    # below makes the contract explicit: an http(s)/data URL is fetched, a
    # bare string is treated as base64. Bytes pass through.

    @staticmethod
    async def _resolve_to_bytes_async(content: str | bytes) -> bytes:
        if isinstance(content, bytes):
            return content
        if not isinstance(content, str):
            raise TypeError(f"save_media expected str or bytes, got {type(content).__name__}")

        s = content.strip()
        if s.startswith(("http://", "https://")):
            # Provider-output URLs (Replicate/Together image+video, etc.) and,
            # occasionally, one of OUR share links. NEVER fetch the URL by hand
            # here — route through the canonical FileManager resolver so an
            # internal share-link / /files/{id} URL is pulled from S3 (not by
            # scraping share-page HTML) and an external URL is fetched once,
            # size-capped and cached. Falls back to a raw fetch only on a
            # standalone install with no cloud FileManager injected.
            return await AIMediaHandler._resolve_url_to_bytes_async(s)
        if s.startswith("data:"):
            return AIMediaHandler._decode_data_url(s)
        return base64.b64decode(s)

    @staticmethod
    async def _resolve_url_to_bytes_async(url: str) -> bytes:
        if has_ext("get_cloud_file_manager"):
            from matrx_files.cloud_sync.media_ref import MediaRef

            fm = get_ext("get_cloud_file_manager")()
            ref = MediaRef(url=url)
            await fm.resolve_media_async(ref, needs_bytes=True)
            base64_data = getattr(ref, "base64_data", None)
            if base64_data:
                return base64.b64decode(base64_data)
            # Resolver couldn't produce bytes (e.g. an OWNED url whose S3 read
            # failed) — surface that instead of silently re-fetching the URL,
            # which for our share links would scrape share-page HTML.
            resolver_error = getattr(ref, "resolver_error", None)
            if getattr(ref, "is_ours", False) or resolver_error:
                raise RuntimeError(
                    f"resolve_media_async could not produce bytes for {url!r}: "
                    f"{resolver_error or 'no base64_data'}"
                )
            # Genuinely-external URL the resolver chose not to pre-fetch — fall
            # through to a direct fetch below.

        import httpx

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=30.0),
            follow_redirects=True,
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.content

    @staticmethod
    def _resolve_to_bytes_sync(content: str | bytes) -> bytes:
        if isinstance(content, bytes):
            return content
        if not isinstance(content, str):
            raise TypeError(f"save_media expected str or bytes, got {type(content).__name__}")

        s = content.strip()
        if s.startswith(("http://", "https://")):
            return AIMediaHandler._resolve_url_to_bytes_sync(s)
        if s.startswith("data:"):
            return AIMediaHandler._decode_data_url(s)
        return base64.b64decode(s)

    @staticmethod
    def _resolve_url_to_bytes_sync(url: str) -> bytes:
        # See _resolve_url_to_bytes_async. The sync resolver recognizes OUR
        # share-link / /files/{id} URLs and reads them from S3, but (by design,
        # to keep the per-provider serialisers sync-only) does NOT pre-fetch a
        # genuinely-external URL — so for an external provider URL we fall back
        # to a direct fetch below. The owned-URL case still goes through the
        # canonical resolver so we never scrape a share page for our own bytes.
        if has_ext("get_cloud_file_manager"):
            from matrx_files.cloud_sync.media_ref import MediaRef

            fm = get_ext("get_cloud_file_manager")()
            ref = MediaRef(url=url)
            fm.resolve_media(ref, needs_bytes=True)
            base64_data = getattr(ref, "base64_data", None)
            if base64_data:
                return base64.b64decode(base64_data)
            resolver_error = getattr(ref, "resolver_error", None)
            if getattr(ref, "is_ours", False) or resolver_error:
                raise RuntimeError(
                    f"resolve_media could not produce bytes for {url!r}: "
                    f"{resolver_error or 'no base64_data'}"
                )

        import requests

        resp = requests.get(url, timeout=(30.0, 300.0), allow_redirects=True)
        resp.raise_for_status()
        return resp.content

    @staticmethod
    def _decode_data_url(s: str) -> bytes:
        # Format: data:[<mediatype>][;base64],<data>
        try:
            header, payload = s.split(",", 1)
        except ValueError:
            raise ValueError("Malformed data URL: missing ',' separator")
        if ";base64" in header.lower():
            return base64.b64decode(payload)
        from urllib.parse import unquote_to_bytes

        return unquote_to_bytes(payload)

    def _prepare_media(
        self,
        content: bytes,
        mime_type: str,
        audio_format: str | None,
    ) -> tuple[bytes, str, str]:
        """Normalize inputs and return (bytes, effective_mime, logical_path).

        ``content`` MUST be raw bytes by the time it reaches this method —
        URL fetching / base64 decoding / data-URL parsing happens in the
        ``_resolve_to_bytes_*`` step ahead of the executor handoff.
        """
        # Step 1: Normalize raw PCM → WAV
        content, mime_type = self._normalize_audio(content, mime_type)

        # Step 2: Transcode audio if a specific output format is requested
        if audio_format and mime_type.startswith("audio/"):
            content, mime_type = self._transcode_audio(content, mime_type, audio_format)

        # The pre-generated UUID is BOTH the cld_files row id AND the
        # last segment of the logical path. Plumbed through
        # ``FileService.upload_simple(file_id=...)`` so the S3 key is
        # ``<owner>/<file_id>`` (the canonical scheme — no legacy/rekey
        # split) and any URL minted from the row carries file_id in its
        # path.
        new_file_id = str(uuid.uuid4())
        ext = self._get_extension_from_mime(mime_type)
        path = f"ai-media/{new_file_id}{ext}"
        return content, mime_type, path, new_file_id

    @staticmethod
    def _transcode_audio(content: bytes, source_mime: str, target_format: str) -> tuple[bytes, str]:
        format_to_mime = {
            "wav": "audio/wav",
            "mp3": "audio/mpeg",
            "ogg": "audio/ogg",
        }

        target_format = target_format.lower().strip()
        target_mime = format_to_mime.get(target_format)

        if not target_mime:
            vcprint(
                f"Unsupported audio_format '{target_format}' - supported: {list(format_to_mime)}. Keeping current format.",
                "AIMediaHandler",
                color="yellow",
            )
            return content, source_mime

        source_base = source_mime.split(";")[0].strip().lower()
        if source_base == target_mime:
            return content, source_mime

        try:
            import io

            from pydub import AudioSegment

            source_format = source_base.split("/")[-1]
            if source_format == "mpeg":
                source_format = "mp3"

            audio = AudioSegment.from_file(io.BytesIO(content), format=source_format)
            output = io.BytesIO()
            audio.export(output, format=target_format)
            return output.getvalue(), target_mime

        except Exception as e:
            vcprint(
                f"Audio transcoding to '{target_format}' failed: {e}. Keeping WAV.",
                "AIMediaHandler",
                color="red",
            )
            return content, source_mime

    def _get_extension_from_mime(self, mime_type: str) -> str:
        base = mime_type.split(";")[0].strip().lower()
        mime_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "video/mp4": ".mp4",
            "video/webm": ".webm",
            "audio/mpeg": ".mp3",
            "audio/mp3": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg",
            "audio/l16": ".wav",
            "audio/pcm": ".wav",
            "application/pdf": ".pdf",
            # Office (OpenXML) — document generation lands under ai_documents.
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        }
        return mime_map.get(base, "")

    @staticmethod
    def _parse_pcm_mime_params(mime_type: str) -> tuple[int, int]:
        bits_per_sample = 16
        sample_rate = 24000

        for part in mime_type.split(";"):
            part = part.strip()
            if part.lower().startswith("rate="):
                try:
                    sample_rate = int(part.split("=", 1)[1])
                except (ValueError, IndexError):
                    pass
            elif part.lower().startswith("audio/l"):
                try:
                    bits_per_sample = int(part.split("l", 1)[1])
                except (ValueError, IndexError):
                    pass

        return bits_per_sample, sample_rate

    @staticmethod
    def _pcm_to_wav(audio_data: bytes, bits_per_sample: int, sample_rate: int) -> bytes:
        num_channels = 1
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = sample_rate * block_align
        data_size = len(audio_data)
        chunk_size = 36 + data_size

        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            chunk_size,
            b"WAVE",
            b"fmt ",
            16,
            1,
            num_channels,
            sample_rate,
            byte_rate,
            block_align,
            bits_per_sample,
            b"data",
            data_size,
        )
        return header + audio_data

    def _normalize_audio(self, content: bytes, mime_type: str) -> tuple[bytes, str]:
        base = mime_type.split(";")[0].strip().lower()
        if base in ("audio/l16", "audio/pcm") or base.startswith("audio/l"):
            bits_per_sample, sample_rate = self._parse_pcm_mime_params(mime_type)
            content = self._pcm_to_wav(content, bits_per_sample, sample_rate)
            return content, "audio/wav"
        return content, mime_type


# ============================================================================
# Convenience functions (preserved signatures)
# ============================================================================


def save_media(
    content: str | bytes,
    mime_type: str,
    audio_format: str | None = None,
) -> str:
    """Save AI-generated media synchronously. Returns a durable inline URL."""
    return AIMediaHandler.get_instance().save_response_media(
        content, mime_type, audio_format=audio_format
    )


async def save_media_envelope_async(
    content: str | bytes,
    mime_type: str,
    *,
    audio_format: str | None = None,
    visibility: VisibilityLiteral | None = None,
    prompt: str | None = None,
    model: str | None = None,
    provider: str | None = None,
    feature: str = "ai_images",
    extra_metadata: dict | None = None,
) -> MediaPersistResult:
    """Async persist + return the canonical envelope.

    Preferred entry point for AI-generated media. The returned
    :class:`MediaPersistResult` carries ``file_id`` so the FE can
    re-resolve any URL flavour via ``GET /assets/{file_id}``.

    Pass ``prompt`` to get a descriptive filename
    (``sunset-rocky-mountains-a1b2c3d4.jpg``) instead of a UUID,
    and to persist the prompt in the cld_files metadata for audit.
    Pass ``feature`` to pick the right ``generations/<feature>/`` root
    (``ai_images`` / ``ai_audio`` / ``ai_video`` / ``ai_documents``).

    ``visibility=None`` (the default) resolves per feature —
    ``ai_audio`` is born public/durable (chat-audio D1 fix), all other
    features stay personal. Pass an explicit visibility to override.
    """
    return await AIMediaHandler.get_instance().save_response_media_envelope_async(
        content,
        mime_type,
        audio_format=audio_format,
        visibility=visibility,
        prompt=prompt,
        model=model,
        provider=provider,
        feature=feature,
        extra_metadata=extra_metadata,
    )


def fetch_media(url: str, target_format: Literal["base64", "bytes"] = "base64") -> str | bytes:
    return AIMediaHandler.get_instance().fetch_media(url, target_format)


# ============================================================================
# Generic tool-output blob normalizer
# ============================================================================

# Keys to probe for a MIME type hint inside the output dict.
_MIME_HINT_KEYS: tuple[str, ...] = ("media_type", "mime_type", "content_type")

# Fallback MIME by well-known base64 key name when no hint key is present.
_KEY_MIME_FALLBACKS: dict[str, str] = {
    "image_base64": "image/jpeg",
    "screenshot_base64": "image/png",
    "audio_base64": "audio/mpeg",
    "video_base64": "video/mp4",
    "pdf_base64": "application/pdf",
    "data_base64": "application/octet-stream",
    "file_base64": "application/octet-stream",
}

_BASE64_SUFFIX = "_base64"

# ---------------------------------------------------------------------------
# THE HANDOFF RULE for tool-output blobs
# ---------------------------------------------------------------------------
# A tool output dict is PERSISTED (``cx_tool_call.output``), RENDERED in the
# tool card, and REPLAYED into the model's context on every following turn.
# It is a record, not a handoff — so it carries the ``file_id`` and nothing
# that expires. Whoever needs bytes or a browser-loadable url mints one fresh
# from the id (``FileManager.resolve_media_async`` / ``GET /assets/{id}``).
#
# This boundary used to call the url-only persist shim and write a ~1-hour
# signed S3 link into all three of those places, with no id to re-mint from.
# The shape below is the SAME one the image funnel emits
# (``tools/image_outputs.py::upload_image_master``) — one canonical media
# envelope, four kinds. Guard: tests/test_tool_blob_media_identity.py.

# Blob mime → (output ``kind``, persistence ``feature``).
#
# ``file_ref`` is the deliberate catch-all: no provider has a native content
# block for a .docx or an opaque octet-stream, so the model receives the
# envelope as ordinary JSON carrying the ``file_id`` — which is exactly what a
# file-reading tool needs to fetch it. Only ``application/pdf`` becomes a
# ``document_ref``; that is the one document type the document content block
# can actually send natively.
_REF_KIND_BY_MIME_PREFIX: tuple[tuple[str, str, str], ...] = (
    ("image/", "image_ref", "ai_images"),
    ("audio/", "audio_ref", "ai_audio"),
    ("video/", "video_ref", "ai_video"),
)
_PDF_MIMES: frozenset[str] = frozenset({"application/pdf", "application/x-pdf"})


def _ref_kind_and_feature(mime_type: str) -> tuple[str, str]:
    """Map a blob's mime type onto its canonical ``*_ref`` kind + feature root."""
    norm = (mime_type or "").lower().split(";", 1)[0].strip()
    if norm in _PDF_MIMES:
        return "document_ref", "ai_documents"
    for prefix, kind, feature in _REF_KIND_BY_MIME_PREFIX:
        if norm.startswith(prefix):
            return kind, feature
    return "file_ref", "ai_documents"


def _decoded_size(blob: str) -> int | None:
    """Byte size a base64 string decodes to, without decoding it."""
    stripped = blob.strip()
    if not stripped:
        return None
    padding = len(stripped) - len(stripped.rstrip("="))
    size = (len(stripped) * 3) // 4 - padding
    return size if size > 0 else None


async def _persist_blob_as_ref(
    blob: str,
    mime_type: str,
    *,
    source_key: str,
) -> dict:
    """Persist one base64 blob and return its canonical media envelope.

    Mirrors ``image_outputs.upload_image_master``, including its failure
    branch: the blob is ALWAYS gone from the returned dict, and a failure is
    reported as ``media_ref=None`` + ``media_ref_error`` so the model can see
    that the media exists but could not be stored — never as raw base64
    surviving into the context window.
    """
    kind, feature = _ref_kind_and_feature(mime_type)
    ref: dict = {
        "kind": kind,
        "media_type": mime_type,
        "source_key": source_key,
    }
    size_bytes = _decoded_size(blob)
    if size_bytes is not None:
        ref["size_bytes"] = size_bytes

    try:
        envelope = await save_media_envelope_async(
            blob,
            mime_type,
            feature=feature,
            extra_metadata={"source": "tool_output_blob", "source_key": source_key},
        )
    except Exception as exc:
        vcprint(
            f"[media] Failed to persist tool blob {source_key} ({mime_type}): {exc!r} — "
            "the media is LOST for this tool result; the blob was stripped so it "
            "cannot reach the model context.",
            color="red",
        )
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind="media_persistence_failed",
            route="tool_output_blob",
            error_type=type(exc).__name__,
            payload={
                "source_key": source_key,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
            },
        )
        ref["media_ref"] = None
        ref["media_ref_error"] = f"upload_failed: {type(exc).__name__}: {exc}"
        return ref

    if not envelope.file_id:
        missing_identity = RuntimeError("media persistence returned no file_id")
        vcprint(
            f"[media] Persisted tool blob {source_key} ({mime_type}) came back with no "
            "file_id — refusing to emit a reference with no identity.",
            color="red",
        )
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            missing_identity,
            kind="media_persistence_failed",
            route="tool_output_blob",
            error_type="missing_file_id",
            payload={
                "source_key": source_key,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
            },
        )
        ref["media_ref"] = None
        ref["media_ref_error"] = "persist_returned_no_file_id"
        return ref

    ref["media_ref"] = {
        "file_id": envelope.file_id,
        "mime_type": envelope.mime_type or mime_type,
    }
    ref["file_id"] = envelope.file_id
    if envelope.file_name:
        ref["file_name"] = envelope.file_name
    if envelope.size_bytes:
        ref["size_bytes"] = envelope.size_bytes
    if envelope.duration_ms is not None:
        ref["duration_ms"] = envelope.duration_ms
    if envelope.page_count is not None:
        ref["page_count"] = envelope.page_count
    return ref


async def persist_media_blobs_async(output: dict) -> dict:
    """Replace every ``*_base64`` blob field in a tool output dict with the
    canonical media envelope that carries its ``file_id``.

    Scans ``output`` for any key ending in ``_base64``, persists the blob via
    :func:`save_media_envelope_async`, removes the blob key, and rewrites the
    output into the same ``{kind, media_ref: {file_id}, media_type,
    size_bytes}`` shape the image funnel emits — so
    ``ToolResult.to_tool_result_content()`` can build a real audio/document
    content block, and so what lands in ``cx_tool_call.output`` is a durable
    identity rather than an expiring signed URL.

    This is the canonical way to prevent large binary payloads from
    inflating the LLM context window. Call it on any tool output that might
    carry raw media data — both client-delegated results (``POST /tool_results``)
    and server-side tool results.

    IMAGE-shaped outputs go through ``matrx_ai.tools.image_outputs`` FIRST and
    never reach here (see that module's ``_STRIP_ON_REWRITE`` note); the
    ``image/`` row above is only a defensive fallback so an image that somehow
    arrives here still keeps its identity.

    MIME type resolution order:
    1. ``media_type`` / ``mime_type`` / ``content_type`` key in the dict.
    2. Hard-coded fallback by blob key name (see ``_KEY_MIME_FALLBACKS``).
    3. ``"application/octet-stream"`` as a last resort.

    Exactly one blob (the overwhelming case) is promoted to the top level, so
    the output IS the media envelope. Several blobs in one output become a
    ``media_ref_list`` carrying every envelope in order — no blob is dropped
    and none of them shadows another.

    On persist failure the blob is **always stripped** (to prevent context
    explosion) and ``media_ref`` is set to ``None`` alongside a
    ``media_ref_error`` so the model can detect the failure.
    """
    result = dict(output)

    refs: list[dict] = []
    for key in list(result.keys()):
        if not key.endswith(_BASE64_SUFFIX):
            continue

        blob = result[key]
        if not isinstance(blob, str) or not blob:
            continue

        mime_type: str | None = None
        for hint_key in _MIME_HINT_KEYS:
            if hint_key in result:
                mime_type = result[hint_key]
                break
        mime_type = mime_type or _KEY_MIME_FALLBACKS.get(key, "application/octet-stream")

        del result[key]  # Always strip — never let the raw blob reach the model.
        # Drop any url the producer already attached under the matching name:
        # it is either the same bytes behind an expiring signature or a stale
        # link, and the ``media_ref`` below is now the answer.
        result.pop(key[: -len(_BASE64_SUFFIX)] + "_url", None)

        refs.append(await _persist_blob_as_ref(blob, mime_type, source_key=key))

    if not refs:
        return result

    if len(refs) == 1:
        ref = refs[0]
        result.update(ref)
        return result

    result["kind"] = "media_ref_list"
    result["items"] = refs
    result["count"] = len(refs)
    return result
