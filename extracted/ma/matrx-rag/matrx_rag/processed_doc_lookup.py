"""Shared helpers for resolving cld_files <-> processed_documents.

Both `aidream/api/routers/files.py` (the cloud-files surface) and
`aidream/api/routers/document.py` (the RAG processed-document surface)
need to map a cld_files.id to the most recent processed_documents row
anchored to it. Keeping the query in one place avoids drift between
the two routers.

Closes Item 14a (the rich `GET /files/{file_id}/document` lookup) and
backs the existing `GET /api/document/by-cld-file/{cld_file_id}`.
"""

from __future__ import annotations

import uuid
from typing import Any

from matrx_rag._ext import get_db_model

#: THE ONE LIST of derivation kinds that ARE a source's text — an extraction (everything
#: else derives from one). ``initial_extract`` is the first reading, ``re_extract`` a
#: replacement extraction (dedup ``replace_extract``), ``recapture`` a newer captured
#: version, ``legacy_import`` text imported before extraction existed. Every caller that
#: asks "is this an extraction?" imports this; a guard test fails on any other copy.
EXTRACTION_DERIVATION_KINDS: tuple[str, ...] = (
    "initial_extract",
    "re_extract",
    "recapture",
    "legacy_import",
)


async def find_processed_document_by_cld_file(
    cld_file_id: str,
) -> dict[str, Any] | None:
    """Return the newest live (not deleted, not archived) EXTRACTION
    (:data:`EXTRACTION_DERIVATION_KINDS`) anchored to a cld_file — never one of its
    derivatives.

    The row carries owner_id (read from created_by) + organization_id so callers can apply
    their own ACL on top of this. RLS on `processed_documents` is the
    second line of defense.

    Returns None when the file has never been processed for RAG.
    """
    ProcessedDocuments = get_db_model("ProcessedDocuments")
    rows = await (
        ProcessedDocuments.filter(
            source_kind="cld_file",
            source_id=cld_file_id,
            deleted_at__isnull=True,
            archived_at__isnull=True,
            # The file's own extraction — never a derivative (clean_v1, table_row,
            # section_summary, synthetic_qa, agent_structured_json, chunked_*): those
            # copy the parent's file id, have no pages, and are often NEWER.
            derivation_kind__in=list(EXTRACTION_DERIVATION_KINDS),
        )
        .order_by("-created_at")
        .limit(1)
        .values(
            "id",
            "name",
            "created_by",
            "organization_id",
            "source_kind",
            "derivation_kind",
            "total_pages",
            "clean_content",
            "updated_at",
        )
    )
    if not rows:
        return None
    row = rows[0]
    clean_content = row["clean_content"]
    return {
        "id": str(row["id"]),
        "name": row["name"],
        "owner_id": str(row["created_by"]) if row["created_by"] else None,
        "organization_id": str(row["organization_id"]) if row["organization_id"] else None,
        "source_kind": row["source_kind"],
        "derivation_kind": row["derivation_kind"],
        "total_pages": row["total_pages"],
        "has_clean_content": bool(clean_content is not None and len(clean_content) > 0),
        "updated_at": row["updated_at"],
    }


async def count_chunks_for_processed_document(processed_document_id: str) -> int:
    """Count rag.kg_chunks for a given processed_documents row.

    Returns 0 when there are no chunks (typical for a doc that ingested
    with no extractable text).
    """
    KgChunks = get_db_model("KgChunks")
    return int(
        await KgChunks.count(processed_document_id=processed_document_id, deleted_at__isnull=True)
        or 0
    )


async def count_chunks_for_source(source_kind: str, source_id: str) -> int:
    """Count current chunks for a canonical source.

    Flat sources such as uploaded ``text/*`` files can be chunked directly
    without creating a ``processed_documents`` row. Status surfaces must use
    this source-level count when no processed-document anchor exists.
    """
    KgChunks = get_db_model("KgChunks")
    return int(
        await KgChunks.count(
            source_kind=source_kind,
            source_id=source_id,
            valid_to__isnull=True,
            deleted_at__isnull=True,
        )
        or 0
    )


async def get_lineage_summary_for_cld_file(
    cld_file_id: str,
) -> dict[str, Any] | None:
    """Light lineage summary for the FE PreviewPane.

    Single query returning parent_file_id, derivation_kind, and the
    descendant count. The PreviewPane shows a compact "this file is
    derived from..." chip without paying for the full /api/document/{id}/lineage walk.

    Returns None if the file does not exist.
    """
    Files = get_db_model("Files")
    file_uuid = uuid.UUID(cld_file_id)
    rows = await Files.filter(id=file_uuid).values(
        "id", "parent_file_id", "derivation_kind", "derivation_metadata"
    )
    if not rows:
        return None
    file_row = rows[0]
    descendant_count = await Files.count(parent_file_id=file_row["id"], deleted_at__isnull=True)
    return {
        "parent_file_id": str(file_row["parent_file_id"]) if file_row["parent_file_id"] else None,
        "derivation_kind": file_row["derivation_kind"],
        "derivation_metadata": file_row["derivation_metadata"],
        "descendant_count": descendant_count,
        "has_descendants": descendant_count > 0,
    }


__all__ = [
    "EXTRACTION_DERIVATION_KINDS",
    "find_processed_document_by_cld_file",
    "count_chunks_for_processed_document",
    "count_chunks_for_source",
    "get_lineage_summary_for_cld_file",
]
