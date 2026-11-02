"""Authorized, cached PDF conversion of an Office file.

Converts an owned Office ``files.files`` row (docx/pptx/xlsx and their
legacy binary forms) into a standalone PDF derivative
(``derivation_kind='pdf_conversion'``) via the hardened LibreOffice lane.
Idempotent per ``(parent, kind, source revision)`` — repeat calls return
the existing child, so every consumer (the FE visual preview, agents,
the post-upload warmer) shares ONE converted PDF per source revision.

This is what makes uploaded decks and documents *visually* renderable:
the FE binds the derivative's file_id to the canonical PDF viewer, and
the whole existing PDF machinery (page renders, pdf-pages selection,
analysis) applies to the converted output for free.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from .asset_envelope import FileRef
from .derivations import FileDerivationKind, inherit_derived_file_policy
from .system_paths import OFFICE_PDFS

if TYPE_CHECKING:
    from .service import FileService

logger = logging.getLogger(__name__)

PDF_CONVERSION_KIND = FileDerivationKind.PDF_CONVERSION.value


class OfficePdfRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")


class OfficePdfResult(BaseModel):
    """One converted-PDF derivative plus lineage diagnostics."""

    source_file_id: str
    office_kind: str
    page_count: int | None = None
    cache_hit: bool
    file: FileRef


def conversion_cache_key(source_record: dict[str, Any]) -> str:
    """Stable key per (parent, source revision) — invalidates on re-upload."""
    source_revision = (
        source_record.get("checksum")
        or source_record.get("current_version")
        or source_record.get("updated_at")
        or "unknown"
    )
    payload = json.dumps(
        {
            "source_file_id": str(source_record["id"]),
            "source_revision": str(source_revision),
            "format_version": 1,
        },
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _pdf_page_count(pdf_bytes: bytes) -> int | None:
    """Best-effort page count of the converted PDF (slide count for decks)."""
    try:
        import pypdfium2 as pdfium

        doc = pdfium.PdfDocument(pdf_bytes)
        try:
            return int(len(doc))
        finally:
            doc.close()
    except Exception:  # noqa: BLE001 — diagnostics only, never blocks
        return None


async def convert_office_pdf(
    service: FileService,
    *,
    file_id: str,
    user_id: str,
    request: OfficePdfRequest | None = None,
) -> OfficePdfResult:
    """Authorize, convert (LibreOffice), persist, and return the PDF derivative."""
    from .specific_handlers.office import classify_office
    from .specific_handlers.office.convert import convert_to_pdf

    request = request or OfficePdfRequest()
    if not isinstance(request, OfficePdfRequest):
        request = OfficePdfRequest.model_validate(request)

    source = await service.read_record(file_id, user_id=user_id, level="read")
    source_mime = (source.get("mime_type") or "").split(";", 1)[0].strip().lower()
    kind = classify_office(source_mime, source.get("file_name"))
    if kind is None:
        raise ValueError(
            f"File {file_id!r} ({source_mime or 'unknown mime'}) is not an "
            "Office document — PDF conversion requires a docx/pptx/xlsx parent."
        )

    cache_key = conversion_cache_key(source)
    cached = await service.db.find_derivative_async(
        parent_file_id=str(source["id"]),
        derivation_kind=PDF_CONVERSION_KIND,
        metadata_key="conversion_key",
        metadata_value=cache_key,
    )
    if cached is not None:
        derivation_meta = cached.get("derivation_metadata") or {}
        return OfficePdfResult(
            source_file_id=str(source["id"]),
            office_kind=derivation_meta.get("source_office_kind") or kind.value,
            page_count=derivation_meta.get("page_count"),
            cache_hit=True,
            file=await service.build_file_ref(cached),
        )

    # Canonical-first, matching every other read path: legacy dedup-loser
    # rows point at the winner's object.
    storage_uri = source.get("canonical_storage_uri") or source.get("storage_uri")
    if not storage_uri:
        raise FileNotFoundError(f"File {file_id!r} has no readable storage object.")

    raw = await service.router.read_async(storage_uri)
    if not raw:
        raise FileNotFoundError(f"File {file_id!r}: storage object is empty or unreadable.")

    pdf_bytes = await asyncio.to_thread(convert_to_pdf, raw, source_kind=kind)
    page_count = await asyncio.to_thread(_pdf_page_count, pdf_bytes)

    source_name = source.get("file_name") or str(source["id"])
    stem = source_name.rsplit(".", 1)[0] or str(source["id"])
    derivation_metadata = {
        "conversion_key": cache_key,
        "source_office_kind": kind.value,
        "page_count": page_count,
        "source_checksum": source.get("checksum"),
        "source_version": source.get("current_version"),
    }
    file_path = OFFICE_PDFS.path(str(source["id"]), f"{stem}.pdf")
    # Inherit the parent's whole access context — web lane, list filter, contextual-access
    # policy keys, AND organization_id (the metadata org channel
    # managed_write_async reads; without it the derivative lands in the
    # writer's PERSONAL org — the wrong-tenant defect inherit_derived_file_policy
    # exists to prevent).
    owner_id = str(source.get("created_by") or user_id)
    access, write_metadata = inherit_derived_file_policy(
        source,
        {
            "parent_file_id": str(source["id"]),
            "derivation_kind": PDF_CONVERSION_KIND,
            **derivation_metadata,
        },
    )
    written = await service.sync_engine.managed_write_async(
        file_path,
        pdf_bytes,
        mime_type="application/pdf",
        published_to_web=access.published_to_web,
        shown_to=access.shown_to,
        change_summary=f"PDF conversion of {source_name}",
        metadata=write_metadata,
        user_id=owner_id,
        parent_file_id=str(source["id"]),
        derivation_kind=PDF_CONVERSION_KIND,
        derivation_metadata=derivation_metadata,
    )
    derivative = await service.db.get_file_async(written.file_id)
    if derivative is None:
        raise RuntimeError(
            f"PDF-conversion derivative {written.file_id!r} was written but cannot be loaded."
        )

    return OfficePdfResult(
        source_file_id=str(source["id"]),
        office_kind=kind.value,
        page_count=page_count,
        cache_hit=False,
        file=await service.build_file_ref(derivative),
    )


__all__ = [
    "PDF_CONVERSION_KIND",
    "OfficePdfRequest",
    "OfficePdfResult",
    "conversion_cache_key",
    "convert_office_pdf",
]
