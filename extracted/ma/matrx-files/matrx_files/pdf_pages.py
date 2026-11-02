"""Authorized, cached PDF page-selection derivatives.

This is the cloud-file bridge around the byte-level PDF page operation. It
turns any ordered set of source pages into one normal PDF, persists it as a
lineage-aware file derivative, and returns the canonical client-safe FileRef.
Both agents and frontends consume the same derivative.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .asset_envelope import FileRef
from .derivations import FileDerivationKind
from .specific_handlers.pdf.models import PdfPageRange

if TYPE_CHECKING:
    from .service import FileService


MAX_SELECTED_PDF_PAGES = 100
PDF_PAGE_SELECTION_KIND = FileDerivationKind.PDF_PAGE_SELECTION.value


class PdfPageSelectionRequest(BaseModel):
    """Ordered 1-based pages/ranges to package into one derivative PDF."""

    model_config = ConfigDict(extra="forbid")

    pages: list[int] | None = None
    page_ranges: list[PdfPageRange] | None = None

    @model_validator(mode="after")
    def _validate_selection(self) -> PdfPageSelectionRequest:
        selected = requested_page_numbers(self.pages, self.page_ranges)
        if not selected:
            raise ValueError("Provide at least one page or page range.")
        if len(selected) > MAX_SELECTED_PDF_PAGES:
            raise ValueError(
                f"A page selection may contain at most {MAX_SELECTED_PDF_PAGES} pages."
            )
        return self


class PdfOutputPageMap(BaseModel):
    output_page: int = Field(ge=1)
    source_page: int = Field(ge=1)


class PdfPageSelectionResult(BaseModel):
    """One selected-page PDF plus lineage and transfer diagnostics."""

    source_file_id: str
    source_pages: list[int]
    output_page_map: list[PdfOutputPageMap]
    source_page_count: int = Field(ge=1)
    source_size_bytes: int | None = Field(default=None, ge=0)
    source_bytes_fetched: int = Field(default=0, ge=0)
    source_fetch_strategy: Literal["cache_hit", "full_object_stream_to_disk"]
    cache_hit: bool
    file: FileRef


def requested_page_numbers(
    pages: list[int] | None,
    page_ranges: list[PdfPageRange] | None,
) -> list[int]:
    """Expand pages/ranges, de-duplicating while preserving caller order."""
    raw: list[int] = []
    if pages:
        if len(pages) > MAX_SELECTED_PDF_PAGES * 2:
            raise ValueError(
                f"A page selection may contain at most {MAX_SELECTED_PDF_PAGES} pages."
            )
        raw.extend(int(page) for page in pages)
    if page_ranges:
        for page_range in page_ranges:
            if page_range.end - page_range.start + 1 > MAX_SELECTED_PDF_PAGES:
                raise ValueError(
                    f"A page selection may contain at most {MAX_SELECTED_PDF_PAGES} pages."
                )
            raw.extend(range(page_range.start, page_range.end + 1))

    selected: list[int] = []
    seen: set[int] = set()
    for page in raw:
        if page < 1:
            raise ValueError("PDF page numbers are 1-based and must be >= 1.")
        if page not in seen:
            selected.append(page)
            seen.add(page)
            if len(selected) > MAX_SELECTED_PDF_PAGES:
                raise ValueError(
                    f"A page selection may contain at most {MAX_SELECTED_PDF_PAGES} pages."
                )
    return selected


def selection_cache_key(source_record: dict[str, Any], pages: list[int]) -> str:
    """Stable key that invalidates automatically when the source changes."""
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
            "pages": pages,
            "format_version": 1,
        },
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


async def select_pdf_pages(
    service: FileService,
    *,
    file_id: str,
    user_id: str,
    request: PdfPageSelectionRequest,
) -> PdfPageSelectionResult:
    """Authorize, materialize, extract, cache, and return a sparse-page PDF."""
    if not isinstance(request, PdfPageSelectionRequest):
        request = PdfPageSelectionRequest.model_validate(request)

    source = await service.read_record(file_id, user_id=user_id, level="read")
    source_mime = (source.get("mime_type") or "").split(";", 1)[0].strip().lower()
    if source_mime != "application/pdf":
        raise ValueError(f"File {file_id!r} is not an application/pdf document.")

    pages = requested_page_numbers(request.pages, request.page_ranges)
    cache_key = selection_cache_key(source, pages)
    cached = await service.db.find_derivative_async(
        parent_file_id=str(source["id"]),
        derivation_kind=PDF_PAGE_SELECTION_KIND,
        metadata_key="selection_key",
        metadata_value=cache_key,
        owner_id=user_id,
    )
    if cached is not None:
        metadata = cached.get("derivation_metadata") or {}
        return _result_from_record(
            source=source,
            pages=pages,
            source_page_count=int(metadata.get("source_page_count") or max(pages)),
            source_bytes_fetched=0,
            source_fetch_strategy="cache_hit",
            cache_hit=True,
            file_ref=await service.build_file_ref(cached),
        )

    storage_uri = source.get("storage_uri")
    if not storage_uri:
        raise FileNotFoundError(f"File {file_id!r} has no readable storage object.")

    from .specific_handlers.pdf.ops.pages import extract_pages_from_path_async
    from .specific_handlers.pdf.tmp import pdf_temp_dir
    from .system_paths import PDF_PAGE_PDFS

    temp_path = pdf_temp_dir() / f"source-{uuid.uuid4().hex}.pdf"
    try:
        fetched = await service.router.download_to_path_async(
            storage_uri, str(temp_path)
        )
        extracted = await extract_pages_from_path_async(
            str(temp_path), pages=pages
        )
    finally:
        _unlink_quietly(temp_path)

    source_page_count = int(
        extracted.metadata.get("source_page_count") or max(pages)
    )
    metadata = {
        "selection_key": cache_key,
        "source_pages": pages,
        "source_page_count": source_page_count,
        "output_page_map": [
            {"output_page": index, "source_page": page}
            for index, page in enumerate(pages, start=1)
        ],
        "source_checksum": source.get("checksum"),
        "source_version": source.get("current_version"),
    }
    file_path = PDF_PAGE_PDFS.path(str(source["id"]), f"{cache_key}.pdf")
    written = await service.sync_engine.managed_write_async(
        file_path,
        extracted.content,
        mime_type="application/pdf",
        published_to_web=False,
        shown_to="only_me",
        change_summary=f"Selected PDF pages {pages}",
        metadata={
            "parent_file_id": str(source["id"]),
            "derivation_kind": PDF_PAGE_SELECTION_KIND,
            **metadata,
        },
        user_id=user_id,
        parent_file_id=str(source["id"]),
        derivation_kind=PDF_PAGE_SELECTION_KIND,
        derivation_metadata=metadata,
    )
    derivative = await service.db.get_file_async(written.file_id)
    if derivative is None:
        raise RuntimeError(
            f"PDF page derivative {written.file_id!r} was written but cannot be loaded."
        )

    return _result_from_record(
        source=source,
        pages=pages,
        source_page_count=source_page_count,
        source_bytes_fetched=int(fetched),
        source_fetch_strategy="full_object_stream_to_disk",
        cache_hit=False,
        file_ref=await service.build_file_ref(
            derivative
        ),
    )


def _result_from_record(
    *,
    source: dict[str, Any],
    pages: list[int],
    source_page_count: int,
    source_bytes_fetched: int,
    source_fetch_strategy: Literal["cache_hit", "full_object_stream_to_disk"],
    cache_hit: bool,
    file_ref: FileRef,
) -> PdfPageSelectionResult:
    return PdfPageSelectionResult(
        source_file_id=str(source["id"]),
        source_pages=pages,
        output_page_map=[
            PdfOutputPageMap(output_page=index, source_page=page)
            for index, page in enumerate(pages, start=1)
        ],
        source_page_count=source_page_count,
        source_size_bytes=source.get("size_bytes"),
        source_bytes_fetched=source_bytes_fetched,
        source_fetch_strategy=source_fetch_strategy,
        cache_hit=cache_hit,
        file=file_ref,
    )


def _unlink_quietly(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


__all__ = [
    "MAX_SELECTED_PDF_PAGES",
    "PDF_PAGE_SELECTION_KIND",
    "PdfOutputPageMap",
    "PdfPageSelectionRequest",
    "PdfPageSelectionResult",
    "requested_page_numbers",
    "selection_cache_key",
    "select_pdf_pages",
]
