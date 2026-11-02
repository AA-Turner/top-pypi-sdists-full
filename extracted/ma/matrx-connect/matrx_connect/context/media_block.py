"""UnifiedMediaBlock — canonical wire shape for every media reference.

One Pydantic model represents an image / video / audio / document /
youtube reference everywhere it appears: in a stream event, in a
``cx_message.content[]`` item, in a render-block payload, in a tool
result. Replaces the four hand-built dict shapes that previously drifted
out of sync (``image_output``, ``partial_image``, ``render_block:image``,
``cx_message`` media parts).

Discriminator: ``kind`` (image | video | audio | document | youtube).
Origin is a per-instance field, not a class split: an ``ImageBlock`` is
the same shape whether the bytes came from our cld_files or from an
external URL — the ``origin`` field tells consumers which fields are
populated.

Validation: ``extra="forbid"`` on every shape so any new field added by
a drifting emission site fails immediately rather than slipping through
as a typed unknown.
"""

from __future__ import annotations

from typing import Annotated, Any, Generic, Literal, Union

from typing_extensions import TypeVar

from matrx_utils import LEGACY_VISIBILITY_MAP, VisibilityLiteral
from matrx_utils.row_access import ShownToLiteral, legacy_level_echo
from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

# Office (Word/PowerPoint/Excel) MIME strings, both OpenXML and legacy binary.
# matrx-connect is BELOW matrx-files in the dep graph, so it cannot import the
# codec — these MIRROR matrx_files.specific_handlers.office.models (DOCX_MIME,
# PPTX_MIME, XLSX_MIME, DOC_MIME, PPT_MIME, XLS_MIME), which stays the source of
# truth. Kept here only so mime_to_media_kind reads as named constants, not six
# magic strings. If Office MIME strings ever change, change them in the codec.
_OFFICE_DOCUMENT_MIME_TYPES = frozenset(
    {
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    }
)


# ---------------------------------------------------------------------------
# Shared base — fields every kind carries
# ---------------------------------------------------------------------------


MediaOrigin = TypeVar("MediaOrigin", bound=Literal["matrx", "external"], default=Literal["matrx", "external"])


class MediaBlockShared(BaseModel, Generic[MediaOrigin]):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    # Discriminator between matrx-owned files and external URLs / inline bytes.
    # The matrx-owned branch carries file_id + the durable URL contract built
    # by SyncEngine (never a signed URL — a signed URL is a handoff, never an
    # identity); the external branch carries an external_url (or base64 for
    # transient/inline media).
    origin: MediaOrigin

    # ---- matrx-origin fields (populated when origin == "matrx") ----
    file_id: str | None = None
    # NO file_uri: this is a CLIENT-facing wire shape. The native storage
    # location (s3://bucket/owner/key) is server-only; a matrx file is
    # identified by file_id + the URL contract, an external one by external_url.
    # A stale file_uri on a historical cx_message.content[] item is dropped by
    # the mode="before" validator below (extra="forbid" would otherwise reject it).
    # The file's row-access words (access ladder T-13): published_to_web is the
    # public lane (a public CDN url exists); shown_to is the list filter.
    published_to_web: bool | None = None
    shown_to: ShownToLiteral | None = None
    visibility: VisibilityLiteral | None = None  # T-13 transitional wire echo (matrx-frontend from-media-block.ts reads it)
    cdn_url: str | None = None
    download_url: str | None = None
    parent_file_id: str | None = None
    derivation_kind: str | None = None
    # Phase 1b (2026-05-16) removed the legacy ``thumbnail_url`` /
    # ``thumbnail_uri`` fields from this shape. The recommended source-
    # of-truth for thumbnails is ``Asset.variants["thumbnail_url"].url``
    # via ``GET /assets/{file_id}``, populated by the universal variants
    # pipeline introduced in Phase 1.

    # ---- external-origin fields (populated when origin == "external") ----
    external_url: str | None = None
    source_label: str | None = None

    # ---- universal fields (populated for both origins when known) ----
    base64: str | None = None
    mime_type: str | None = None
    file_name: str | None = None
    size_bytes: int | None = None

    # ---- streaming-state fields (set during in-progress generation) ----
    status: Literal["complete", "streaming", "error"] = "complete"
    progress: float | None = None
    error_message: str | None = None

    # ---- free-form metadata (Phase 2 stamps generation metadata here) ----
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _drop_storage_location(cls, data: Any) -> Any:
        # The block no longer HAS a file_uri field (it's a client-facing wire
        # shape — the native storage location is server-only). Historical
        # cx_message.content[] items may still carry file_uri; pop it before
        # extra="forbid" validation so old rows keep parsing. This is the
        # structural guarantee that no construction path leaks the storage URI.
        if isinstance(data, dict) and "file_uri" in data:
            data = {k: v for k, v in data.items() if k != "file_uri"}
        # signed_url / signed_url_expires_at were removed from this shape
        # (2026-08-26 — nothing returns a signed URL; the durable
        # /files/{id}/download route + file-session cookie replaced them).
        # Historical cx_message.content[] items still carry them; drop
        # silently so old rows keep parsing under extra="forbid".
        if isinstance(data, dict) and (
            "signed_url" in data or "signed_url_expires_at" in data
        ):
            data = {
                k: v
                for k, v in data.items()
                if k not in ("signed_url", "signed_url_expires_at")
            }
        # Same rule for the retiring level word: this is a PERSISTED shape, so a
        # historical item may carry a spelling the DB enum has since retired
        # ('shared', 'private'), and items written before T-13 carry only the old
        # word. Reconcile both — a display field must NEVER raise on a rebuild path
        # and brick a conversation — and derive the new words when they are absent.
        if isinstance(data, dict):
            legacy = data.get("visibility")  # T-13 transitional wire input (persisted items)
            if legacy in LEGACY_VISIBILITY_MAP:
                legacy = LEGACY_VISIBILITY_MAP[legacy]
                data = {**data, "visibility": legacy}  # T-13 transitional wire echo
            if legacy is not None and data.get("published_to_web") is None:
                data = {**data, "published_to_web": legacy == "public"}
        return data

    @model_validator(mode="after")
    def _enforce_origin_contract(self) -> "MediaBlockShared":
        # During streaming we may not yet have a file_id (the master row is
        # written after the final byte chunk arrives). Only enforce the
        # file_id requirement for complete-state matrx blocks.
        if (
            self.origin == "matrx"
            and self.status == "complete"
            and not self.file_id
        ):
            raise ValueError(
                "origin='matrx' with status='complete' requires file_id"
            )
        if (
            self.origin == "external"
            and not (self.external_url or self.base64)
        ):
            raise ValueError(
                "origin='external' requires external_url or base64"
            )
        return self


# ---------------------------------------------------------------------------
# Per-kind blocks
# ---------------------------------------------------------------------------


class ImageBlock(MediaBlockShared):
    kind: Literal["image"] = "image"
    width: int | None = None
    height: int | None = None
    # Provider serialization hint (e.g. "anthropic_opus_hires", "gemini3_high").
    # Same field as on matrx_ai.ImageContent — keep the name aligned.
    vision_class: str | None = None


class VideoBlock(MediaBlockShared):
    kind: Literal["video"] = "video"
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None
    # Full-resolution representative frame (Phase 1 universal-thumbnail work).
    poster_url: str | None = None


class AudioBlock(MediaBlockShared):
    kind: Literal["audio"] = "audio"
    duration_ms: int | None = None
    # Optional transcription result (matches matrx_ai.AudioContent shape).
    transcript: str | None = None


class DocumentBlock(MediaBlockShared):
    kind: Literal["document"] = "document"
    page_count: int | None = None
    # Full-resolution first-page render (Phase 1 universal-thumbnail work).
    page1_url: str | None = None


class YouTubeBlock(MediaBlockShared[Literal["external"]]):
    kind: Literal["youtube"] = "youtube"
    # YouTube is always external — there is no matrx-owned YouTube file.
    origin: Literal["external"] = "external"
    video_id: str | None = None


UnifiedMediaBlock = Annotated[
    Union[ImageBlock, VideoBlock, AudioBlock, DocumentBlock, YouTubeBlock],
    Field(discriminator="kind"),
]


# ---------------------------------------------------------------------------
# Mime → kind dispatcher
# ---------------------------------------------------------------------------


MediaKind = Literal["image", "video", "audio", "document", "youtube"]


def mime_to_media_kind(mime_type: str | None) -> MediaKind | None:
    if not mime_type:
        return None
    mt = mime_type.lower().strip()
    if mt.startswith("image/"):
        return "image"
    if mt.startswith("video/"):
        return "video"
    if mt.startswith("audio/"):
        return "audio"
    # PDFs and word-processing documents are the common "document" cases.
    if mt == "application/pdf":
        return "document"
    if mt in _OFFICE_DOCUMENT_MIME_TYPES:
        return "document"
    return None


# ---------------------------------------------------------------------------
# Conversion helpers — single source of truth for "build a wire block"
# ---------------------------------------------------------------------------
#
# Every code path that needs to ship a media reference on the wire goes
# through one of these helpers. Hand-construction of UnifiedMediaBlock
# from a cld_files row OR an AssetVariant is forbidden (the audit script
# will reject `emitter.send_data({...})` dict literals that look like
# media content — see scripts/audit_api_types.py).


def _coerce_dict(record: Any) -> dict[str, Any]:
    """Accept either a cld_files row dict OR a Pydantic CloudFile-shaped model."""
    if isinstance(record, dict):
        return record
    if hasattr(record, "model_dump"):
        return record.model_dump()
    return dict(record)  # last-ditch — raises if it isn't dict-like


def _legacy_echo(published_to_web: Any, shown_to: Any) -> VisibilityLiteral | None:
    """The old single level word for clients that still read it, derived from the new words."""
    if published_to_web is None:
        return None
    return legacy_level_echo({"published_to_web": published_to_web, "shown_to": shown_to})  # type: ignore[return-value]


def cloud_file_to_media_block(
    record: Any,
    *,
    url_set: dict[str, Any] | None = None,
    kind_override: MediaKind | None = None,
    kind_variant_urls: dict[str, str] | None = None,
) -> UnifiedMediaBlock:
    """Build a UnifiedMediaBlock from a cld_files row (or CloudFile model).

    ``url_set`` is the dict returned by
    ``SyncEngine.build_urls_for_record_async`` (``{url, cdn_url,
    download_url}`` — all durable, never signed). Pass it when you've
    already built URLs for this record so we don't build twice.

    ``kind_override`` forces a specific kind when the mime alone is
    ambiguous (e.g. SVG documents you want treated as image).

    ``kind_variant_urls`` (Phase 1c) supplies kind-specific full-res
    variant URLs the block should carry. Recognized keys:

      - ``"page1_url"`` → DocumentBlock.page1_url (PDF page 1 at full DPI)
      - ``"poster_url"`` → VideoBlock.poster_url (video frame at native res)

    Other keys are ignored. Callers typically derive this map from the
    Asset envelope's ``variants`` dict or the variants-service catalog.
    """
    rec = _coerce_dict(record)
    mime = rec.get("mime_type")
    kind: MediaKind | None = kind_override or mime_to_media_kind(mime)
    if kind is None:
        # Unknown mime — fall back to "document" so we still produce a
        # valid block. Renderers that don't recognize the document mime
        # show a generic file representation.
        kind = "document"

    file_id = rec.get("id") or rec.get("file_id")
    # NOTE: no file_uri — the block has no such field. The native storage
    # location (rec["storage_uri"]) is server-only; identify by file_id + URLs.
    common: dict[str, Any] = {
        "origin": "matrx",
        "file_id": file_id,
        "published_to_web": rec.get("published_to_web"),
        "shown_to": rec.get("shown_to"),
        "visibility": _legacy_echo(rec.get("published_to_web"), rec.get("shown_to")),  # T-13 transitional wire echo
        "parent_file_id": rec.get("parent_file_id"),
        "derivation_kind": rec.get("derivation_kind"),
        # Phase 1b removed the legacy thumbnail_url / thumbnail_uri
        # fields — see Phase 1b notes on the MediaBlockShared model.
        "mime_type": mime,
        "file_name": rec.get("file_name"),
        "size_bytes": rec.get("size_bytes") or rec.get("file_size"),  # tolerate pre-migration rows
        "metadata": rec.get("metadata") or {},
    }
    if url_set:
        common.update(
            url=url_set.get("url"),
            cdn_url=url_set.get("cdn_url"),
            download_url=url_set.get("download_url"),
        )
    kv_urls = kind_variant_urls or {}

    if kind == "image":
        return ImageBlock(
            **{k: v for k, v in common.items() if k != "url"},
            width=rec.get("width"),
            height=rec.get("height"),
        )
    if kind == "video":
        return VideoBlock(
            **{k: v for k, v in common.items() if k != "url"},
            width=rec.get("width"),
            height=rec.get("height"),
            duration_ms=rec.get("duration_ms"),
            poster_url=kv_urls.get("poster_url"),
        )
    if kind == "audio":
        return AudioBlock(
            **{k: v for k, v in common.items() if k != "url"},
            duration_ms=rec.get("duration_ms"),
        )
    if kind == "document":
        # page_count lives in metadata (no dedicated DB column) — surface
        # it as a first-class block field for the FE.
        page_count = None
        meta = common.get("metadata") or {}
        if isinstance(meta, dict) and meta.get("page_count") is not None:
            try:
                page_count = int(meta["page_count"])
            except (TypeError, ValueError):
                page_count = None
        return DocumentBlock(
            **{k: v for k, v in common.items() if k != "url"},
            page_count=page_count,
            page1_url=kv_urls.get("page1_url"),
        )
    # YouTube can't come from a cld_files row — caller must use
    # external_url_to_media_block(kind='youtube', ...).
    raise ValueError(f"cloud_file_to_media_block: unexpected kind {kind!r}")


def asset_variant_to_media_block(
    variant: Any,
    *,
    kind: MediaKind | None = None,
    published_to_web: bool | None = None,
    shown_to: ShownToLiteral | None = None,
) -> UnifiedMediaBlock:
    """Build a UnifiedMediaBlock from an AssetVariant (already URL-minted).

    Used by code that has the asset envelope in hand and wants to emit
    the primary or a specific variant as the wire block.
    """
    v = _coerce_dict(variant)
    mime = v.get("mime_type")
    if kind is None:
        kind = mime_to_media_kind(mime) or "document"
    # NOTE: no file_uri — the block has no such field (server-only location).
    common: dict[str, Any] = {
        "origin": "matrx",
        "file_id": v.get("file_id"),
        "published_to_web": published_to_web,
        "shown_to": shown_to,
        "visibility": _legacy_echo(published_to_web, shown_to),  # T-13 transitional wire echo
        "cdn_url": v.get("cdn_url"),
        "download_url": v.get("download_url"),
        "mime_type": mime,
        "file_name": v.get("file_name"),
        "size_bytes": v.get("size_bytes") or v.get("file_size"),
        "metadata": v.get("metadata") or {},
    }
    if kind == "image":
        return ImageBlock(
            **common,
            width=v.get("width"),
            height=v.get("height"),
        )
    if kind == "video":
        return VideoBlock(
            **common,
            width=v.get("width"),
            height=v.get("height"),
            duration_ms=v.get("duration_ms"),
        )
    if kind == "audio":
        return AudioBlock(
            **common,
            duration_ms=v.get("duration_ms"),
        )
    return DocumentBlock(**common)


def external_url_to_media_block(
    url: str,
    *,
    kind: MediaKind,
    source_label: str | None = None,
    mime_type: str | None = None,
    file_name: str | None = None,
    metadata: dict[str, JsonValue] | None = None,
) -> UnifiedMediaBlock:
    """Build a UnifiedMediaBlock for an external URL we don't own.

    YouTube videos extract their ``video_id`` from the URL when possible.
    """
    common: dict[str, Any] = {
        "origin": "external",
        "external_url": url,
        "source_label": source_label,
        "mime_type": mime_type,
        "file_name": file_name,
        "metadata": metadata or {},
    }
    if kind == "image":
        return ImageBlock(**common)
    if kind == "video":
        return VideoBlock(**common)
    if kind == "audio":
        return AudioBlock(**common)
    if kind == "document":
        return DocumentBlock(**common)
    if kind == "youtube":
        return YouTubeBlock(
            **common,
            video_id=_extract_youtube_id(url),
        )
    raise ValueError(f"external_url_to_media_block: unknown kind {kind!r}")


def streaming_partial_image_block(
    *,
    base64: str,
    progress: float,
    mime_type: str = "image/png",
    file_id: str | None = None,
) -> ImageBlock:
    """In-progress streaming image (provider partial during generation).

    Used by the OpenAI gpt-image-* partial-stream path and any other
    provider that ships progressive previews. ``status="streaming"``
    relaxes the origin contract — file_id may legitimately be absent
    until the final master row is written.
    """
    return ImageBlock(
        origin="matrx",
        status="streaming",
        progress=progress,
        base64=base64,
        mime_type=mime_type,
        file_id=file_id,
    )


def _extract_youtube_id(url: str) -> str | None:
    """Pull a YouTube video id out of a URL. None if the URL doesn't look like one."""
    import re

    # Covers youtu.be/<id>, youtube.com/watch?v=<id>, youtube.com/embed/<id>,
    # youtube.com/shorts/<id>. Restricts to the standard 11-char id charset.
    patterns = [
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


__all__ = [
    "MediaBlockShared",
    "ImageBlock",
    "VideoBlock",
    "AudioBlock",
    "DocumentBlock",
    "YouTubeBlock",
    "UnifiedMediaBlock",
    "MediaKind",
    "mime_to_media_kind",
    "cloud_file_to_media_block",
    "asset_variant_to_media_block",
    "external_url_to_media_block",
    "streaming_partial_image_block",
]
