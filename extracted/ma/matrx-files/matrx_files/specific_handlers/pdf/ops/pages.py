"""Single-document page operations: extract, crop, rotate, delete.

All functions take raw PDF bytes and return a ``PdfBinaryResult``. The async
variants run the sync function on the matrx-pdf CPU executor.
"""

from __future__ import annotations

from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import open_unprotected, load_pymupdf, normalise_page_ranges, save_pymupdf_doc
from ..models import PdfBinaryResult, PdfCropBox, PdfPageRange


def extract_pages_from_bytes(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as src, pymupdf.open() as out:
        selected = normalise_page_ranges(
            src.page_count, pages, page_ranges, default_all=False
        )
        if not selected:
            raise ValueError("Provide at least one page or page range to extract.")
        for page_num in selected:
            page_idx = page_num - 1
            out.insert_pdf(src, from_page=page_idx, to_page=page_idx)
        return PdfBinaryResult(
            content=save_pymupdf_doc(out),
            page_count=out.page_count,
            operation="extract_pages",
            metadata={"source_pages": selected},
        )


def extract_pages_from_path(
    pdf_path: str,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    """Extract pages from a local PDF without buffering the source in memory."""
    pymupdf = load_pymupdf()
    with pymupdf.open(pdf_path) as src, pymupdf.open() as out:
        selected = normalise_page_ranges(
            src.page_count, pages, page_ranges, default_all=False
        )
        if not selected:
            raise ValueError("Provide at least one page or page range to extract.")
        for page_num in selected:
            page_idx = page_num - 1
            out.insert_pdf(src, from_page=page_idx, to_page=page_idx)
        return PdfBinaryResult(
            content=save_pymupdf_doc(out),
            page_count=out.page_count,
            operation="extract_pages",
            metadata={
                "source_pages": selected,
                "source_page_count": src.page_count,
            },
        )


async def extract_pages_from_path_async(
    pdf_path: str,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        extract_pages_from_path, pdf_path, pages, page_ranges
    )


async def extract_pages_from_bytes_async(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        extract_pages_from_bytes, pdf_bytes, pages, page_ranges
    )


def _visual_rect_to_page_space(page: Any, rect: Any) -> Any:
    """Map a rectangle drawn on the rotated (visual) page into unrotated page space."""
    if not page.rotation:
        return rect
    mapped = rect * page.derotation_matrix
    mapped.normalize()
    return mapped


# A client may send a page edge rounded UP by a hair (595.2756 against 595.27557);
# a box that pokes out by less than this is the page edge, not a wrong box.
_BOX_EDGE_EPSILON = 0.01


def clamp_box_to_page(page: Any, rect: Any, epsilon: float = _BOX_EDGE_EPSILON) -> Any:
    """Return ``rect`` pulled onto ``page.rect`` when it overshoots by <= ``epsilon``.

    A box that is genuinely outside the page is returned unchanged so the caller
    can refuse it. Shared by every op that takes page coordinates.
    """
    bounds = page.rect
    if (
        rect.x0 >= bounds.x0 - epsilon
        and rect.y0 >= bounds.y0 - epsilon
        and rect.x1 <= bounds.x1 + epsilon
        and rect.y1 <= bounds.y1 + epsilon
    ):
        return type(rect)(
            max(rect.x0, bounds.x0),
            max(rect.y0, bounds.y0),
            min(rect.x1, bounds.x1),
            min(rect.y1, bounds.y1),
        )
    return rect


def crop_pages_in_bytes(
    pdf_bytes: bytes,
    crop_box: PdfCropBox | dict[str, Any],
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as doc:
        box = crop_box if isinstance(crop_box, PdfCropBox) else PdfCropBox(**crop_box)
        rect = pymupdf.Rect(box.x0, box.y0, box.x1, box.y1)
        if rect.is_empty or rect.is_infinite:
            raise ValueError("Crop box must describe a finite non-empty rectangle.")

        selected = normalise_page_ranges(
            doc.page_count, pages, page_ranges, default_all=True
        )
        for page_num in selected:
            page = doc[page_num - 1]
            page_rect = clamp_box_to_page(page, rect)
            if not page.rect.contains(page_rect):
                raise ValueError(
                    f"Crop box is outside page {page_num} bounds: {page.rect}."
                )
            # The box arrives in the VISUAL space the person sees (page.rect,
            # rotation applied). PDF CropBox lives in unrotated page space, so
            # map the rectangle back through /Rotate before storing it.
            page.set_cropbox(_visual_rect_to_page_space(page, page_rect))

        return PdfBinaryResult(
            content=save_pymupdf_doc(doc),
            page_count=doc.page_count,
            operation="crop_pages",
            metadata={"pages": selected, "crop_box": box.model_dump()},
        )


async def crop_pages_in_bytes_async(
    pdf_bytes: bytes,
    crop_box: PdfCropBox | dict[str, Any],
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        crop_pages_in_bytes, pdf_bytes, crop_box, pages, page_ranges
    )


def rotate_pages_in_bytes(
    pdf_bytes: bytes,
    rotation: int,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    if rotation % 90 != 0:
        raise ValueError("Rotation must be a multiple of 90 degrees.")

    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as doc:
        selected = normalise_page_ranges(
            doc.page_count, pages, page_ranges, default_all=True
        )
        for page_num in selected:
            page = doc[page_num - 1]
            page.set_rotation((page.rotation + rotation) % 360)

        return PdfBinaryResult(
            content=save_pymupdf_doc(doc),
            page_count=doc.page_count,
            operation="rotate_pages",
            metadata={"pages": selected, "rotation": rotation},
        )


async def rotate_pages_in_bytes_async(
    pdf_bytes: bytes,
    rotation: int,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        rotate_pages_in_bytes, pdf_bytes, rotation, pages, page_ranges
    )


def delete_pages_from_bytes(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as doc:
        selected = normalise_page_ranges(
            doc.page_count, pages, page_ranges, default_all=False
        )
        if not selected:
            raise ValueError("Provide at least one page or page range to delete.")
        if len(selected) >= doc.page_count:
            raise ValueError("Cannot delete every page from a PDF.")

        for page_idx in sorted((page - 1 for page in selected), reverse=True):
            doc.delete_page(page_idx)

        return PdfBinaryResult(
            content=save_pymupdf_doc(doc),
            page_count=doc.page_count,
            operation="delete_pages",
            metadata={"deleted_pages": selected},
        )


async def delete_pages_from_bytes_async(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        delete_pages_from_bytes, pdf_bytes, pages, page_ranges
    )


def reorder_pages_in_bytes(
    pdf_bytes: bytes,
    new_order: list[int],
) -> PdfBinaryResult:
    """Reorder pages to match *new_order* (1-based list of every page exactly once).

    Wraps PyMuPDF's ``Document.select`` which preserves bookmarks, links,
    annotations, and form widgets across the rewrite.
    """
    if not new_order:
        raise ValueError("new_order must contain at least one page.")
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as doc:
        page_count = doc.page_count
        unique = sorted(set(new_order))
        if unique != list(range(1, page_count + 1)):
            raise ValueError(
                f"new_order must include every page 1..{page_count} exactly once; "
                f"got {new_order!r}."
            )
        zero_based = [p - 1 for p in new_order]
        doc.select(zero_based)
        return PdfBinaryResult(
            content=save_pymupdf_doc(doc),
            page_count=doc.page_count,
            operation="reorder_pages",
            metadata={"new_order": list(new_order)},
        )


async def reorder_pages_in_bytes_async(
    pdf_bytes: bytes,
    new_order: list[int],
) -> PdfBinaryResult:
    return await run_in_cpu_executor(reorder_pages_in_bytes, pdf_bytes, new_order)


def insert_pages_in_bytes(
    target_pdf_bytes: bytes,
    source_pdf_bytes: bytes,
    after_page: int = 0,
    source_pages: list[int] | None = None,
    source_page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    include_links: bool = True,
    include_annotations: bool = True,
    include_widgets: bool = True,
    join_duplicates: bool = False,
) -> PdfBinaryResult:
    """Insert pages from *source_pdf_bytes* into *target_pdf_bytes* after *after_page*.

    *after_page* is 1-based; ``0`` prepends to the front. Wraps
    ``Document.insert_pdf`` (PyMuPDF >= 1.27) which preserves links,
    annotations, and form widgets when the respective flags are True.

    *join_duplicates* hands the corresponding flag to PyMuPDF — when True,
    matching xrefs are merged across the boundary (smaller output, slower).
    """
    pymupdf = load_pymupdf()
    with pymupdf.open(stream=target_pdf_bytes, filetype="pdf") as dst, pymupdf.open(
        stream=source_pdf_bytes, filetype="pdf"
    ) as src:
        if after_page < 0 or after_page > dst.page_count:
            raise ValueError(
                f"after_page {after_page} must be in 0..{dst.page_count}."
            )
        selected = normalise_page_ranges(
            src.page_count,
            source_pages,
            source_page_ranges,
            default_all=True,
        )
        insertion_idx = after_page  # 0-based start_at position
        for i, page_num in enumerate(selected):
            page_idx = page_num - 1
            dst.insert_pdf(
                src,
                from_page=page_idx,
                to_page=page_idx,
                start_at=insertion_idx + i,
                links=int(include_links),
                annots=int(include_annotations),
                widgets=int(include_widgets),
                join_duplicates=int(join_duplicates),
            )
        return PdfBinaryResult(
            content=save_pymupdf_doc(dst),
            page_count=dst.page_count,
            operation="insert_pages",
            metadata={
                "after_page": after_page,
                "source_pages": selected,
                "include_links": include_links,
                "include_annotations": include_annotations,
                "include_widgets": include_widgets,
                "join_duplicates": join_duplicates,
            },
        )


async def insert_pages_in_bytes_async(
    target_pdf_bytes: bytes,
    source_pdf_bytes: bytes,
    after_page: int = 0,
    source_pages: list[int] | None = None,
    source_page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    include_links: bool = True,
    include_annotations: bool = True,
    include_widgets: bool = True,
    join_duplicates: bool = False,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        insert_pages_in_bytes,
        target_pdf_bytes,
        source_pdf_bytes,
        after_page,
        source_pages,
        source_page_ranges,
        include_links,
        include_annotations,
        include_widgets,
        join_duplicates,
    )


def duplicate_pages_in_bytes(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    count: int = 1,
) -> PdfBinaryResult:
    """Append *count* copies of each selected page directly after the original.

    Uses ``Document.fullcopy_page`` so the duplicates do not share xrefs with
    the source — safe for downstream edits (annotation, redaction, etc.) on
    the duplicate without affecting the original.
    """
    if count < 1:
        raise ValueError("count must be >= 1.")
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as doc:
        selected = normalise_page_ranges(
            doc.page_count, pages, page_ranges, default_all=False
        )
        if not selected:
            raise ValueError("Provide at least one page or page range to duplicate.")

        # Process highest-page-first so inserts don't shift downstream indexes.
        for page_num in sorted(selected, reverse=True):
            source_idx = page_num - 1
            for _ in range(count):
                doc.fullcopy_page(source_idx, to=source_idx)

        return PdfBinaryResult(
            content=save_pymupdf_doc(doc),
            page_count=doc.page_count,
            operation="duplicate_pages",
            metadata={
                "duplicated_pages": selected,
                "count": count,
            },
        )


async def duplicate_pages_in_bytes_async(
    pdf_bytes: bytes,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    count: int = 1,
) -> PdfBinaryResult:
    return await run_in_cpu_executor(
        duplicate_pages_in_bytes, pdf_bytes, pages, page_ranges, count
    )


__all__ = [
    "extract_pages_from_bytes",
    "extract_pages_from_bytes_async",
    "extract_pages_from_path",
    "extract_pages_from_path_async",
    "crop_pages_in_bytes",
    "crop_pages_in_bytes_async",
    "rotate_pages_in_bytes",
    "rotate_pages_in_bytes_async",
    "delete_pages_from_bytes",
    "delete_pages_from_bytes_async",
    "reorder_pages_in_bytes",
    "reorder_pages_in_bytes_async",
    "insert_pages_in_bytes",
    "insert_pages_in_bytes_async",
    "duplicate_pages_in_bytes",
    "duplicate_pages_in_bytes_async",
]
