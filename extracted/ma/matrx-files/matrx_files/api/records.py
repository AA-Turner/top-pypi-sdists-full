"""Canonical client-facing file record shape + the ONE row→record mapper.

``FileRecord`` is the published wire contract for ``GET /files/{id}`` —
the shape matrx-frontend's generated types
(``types/python-generated/api-types.ts``) are built from. The retired
``GET /files/{id}/url`` mint endpoint (and its ``SignedUrlResponse``) is
GONE: nothing returns a signed URL (Arman 2026-08-21); clients bind the
durable ``url`` / ``download_url`` directly.

THIS MODULE IS THE ONLY DESERIALIZER for that contract. Both consumers —
aidream's in-process files router AND this package's own ``router_files``
(the standalone service at files.matrxserver.com) — import from here.
History: the standalone router carried a second, independent ``_FileRecord``
(``file_id``/``folder_id``/``version``, no URL contract) and a ``/url``
envelope with no ``expires_in``; the drift broke every cold FE file
hydration and killed the signed-URL cache (FE compensated defensively in
matrx-frontend bea07112c). A persisted/published shape has ONE deserializer.
"""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_utils.row_access import legacy_level_echo
from pydantic import BaseModel, Field, JsonValue

from ..cloud_sync.cdn import public_url_for
from ..cloud_sync.thumbnail_resolver import resolve_thumbnail_url_async


class FileRecord(BaseModel):
    id: str
    owner_id: str
    # The durable record identity is needed by the frontend's canonical
    # hydration path.  Keep these server-projected fields on the one published
    # record shape so an exact-id read never has to fall back to a second
    # browser-side RLS query merely to recover lineage or scope.
    organization_id: str | None = None
    file_path: str
    # NO storage_uri: the native s3://bucket/owner/key location is server-only
    # and must never reach a client (info-disclosure + unusable). Render or
    # download via the durable url/cdn_url/download_url contract below;
    # reference the file by `id`.
    file_name: str
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    published_to_web: bool = False
    shown_to: str | None = None
    visibility: str | None = None  # T-13 transitional wire echo (derived from the two words)
    current_version: int = 1
    parent_folder_id: str | None = None
    parent_file_id: str | None = None
    derivation_kind: str | None = None
    derivation_metadata: dict[str, JsonValue] | None = None
    duplicate_of_file_id: str | None = None
    canonical_processed_document_id: str | None = None
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict
    )  # api-any-ok: user-supplied per-file metadata blob (tags, processing hints) — free-form JSONB
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    # Populated only for files published to the web when the CDN is configured.
    # Carries a content-hashed ?v= cache-buster so a new version of the same
    # file invalidates instantly.
    public_url: str | None = None
    # Server-side generated thumbnail URL. Null when the file type isn't
    # supported or generation hasn't completed yet — the FE falls back to a
    # category icon. Public + CDN-configured files get a CDN URL; personal
    # files the durable authenticated route for the thumbnail variant.
    thumbnail_url: str | None = None
    # ------------------------------------------------------------------
    # Canonical DURABLE URL contract — same three flavours as Asset.
    # ``url``           always-usable browser-renderable URL (CDN if public,
    #                   /files/{id}/download?inline=1 otherwise).
    # ``cdn_url``       permanent CDN URL when public + CDN configured.
    # ``download_url``  attachment-disposition durable route — never
    #                   put this in <img src=...>.
    # 🚨 NO signed_url — a signed URL is a handoff, never an identity.
    # ------------------------------------------------------------------
    url: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None


def to_file_record(record: dict, *, thumbnail_url: str | None = None) -> FileRecord:
    """Build the client-visible FileRecord without minting signed URLs.

    Cheap path — used by list endpoints. Populates ``cdn_url`` /
    ``public_url`` for public files (CDN URL, free); ``url`` mirrors
    ``cdn_url`` when public; ``download_url`` stays null.
    Single-record handlers use ``to_file_record_with_urls_async``.
    """
    cdn = public_url_for(record)
    created_at = record.get("created_at")
    updated_at = record.get("updated_at")
    deleted_at = record.get("deleted_at")
    return FileRecord(
        id=str(record["id"]),
        owner_id=record.get("owner_id", ""),
        organization_id=(
            str(record["organization_id"])
            if record.get("organization_id") is not None
            else None
        ),
        file_path=record["file_path"],
        file_name=record.get("file_name") or record["file_path"].rsplit("/", 1)[-1],
        mime_type=record.get("mime_type"),
        size_bytes=record.get("size_bytes"),
        checksum=record.get("checksum"),
        published_to_web=bool(record.get("published_to_web")),
        shown_to=record.get("shown_to"),
        visibility=legacy_level_echo(record),
        current_version=record.get("current_version", 1),
        parent_folder_id=(
            str(record["parent_folder_id"]) if record.get("parent_folder_id") else None
        ),
        parent_file_id=(
            str(record["parent_file_id"]) if record.get("parent_file_id") else None
        ),
        derivation_kind=record.get("derivation_kind"),
        derivation_metadata=record.get("derivation_metadata"),
        duplicate_of_file_id=(
            str(record["duplicate_of_file_id"])
            if record.get("duplicate_of_file_id")
            else None
        ),
        canonical_processed_document_id=(
            str(record["canonical_processed_document_id"])
            if record.get("canonical_processed_document_id")
            else None
        ),
        metadata=record.get("metadata") or {},
        created_at=str(created_at) if created_at is not None else None,
        updated_at=str(updated_at) if updated_at is not None else None,
        deleted_at=str(deleted_at) if deleted_at is not None else None,
        public_url=cdn,
        cdn_url=cdn,
        url=cdn,
        thumbnail_url=thumbnail_url,
    )


async def to_file_record_with_urls_async(
    fm: Any,
    record: dict,
) -> FileRecord:
    """Single-file variant — populates the full durable URL contract + thumbnail.

    Builds the durable url/cdn_url/download_url via the engine's centralized
    builder (``SyncEngine.build_urls_for_record_async`` — no minting) and
    resolves the thumbnail variant in parallel.
    """
    thumbnail_url, urls = await asyncio.gather(
        resolve_thumbnail_url_async(fm, record),
        fm.sync_engine.build_urls_for_record_async(record),
    )
    base = to_file_record(record, thumbnail_url=thumbnail_url)
    return base.model_copy(
        update={
            "url": urls["url"],
            "cdn_url": urls["cdn_url"],
            "download_url": urls["download_url"],
        }
    )


__all__ = [
    "FileRecord",
    "to_file_record",
    "to_file_record_with_urls_async",
]
