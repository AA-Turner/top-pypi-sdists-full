"""Private helpers shared across the pdf/ submodules.

This module intentionally has no external dependencies on sibling matrx-*
packages. Optional integrations (matrx_connect.context.events.InfoPayload)
are deferred to function-local imports so the package remains usable when
matrx-connect is not installed.
"""

from __future__ import annotations

from typing import Any

from .models import PdfPageRange


def load_pymupdf() -> Any:
    """Resolve PyMuPDF as either the modern `pymupdf` import or legacy `fitz`."""
    try:
        import pymupdf

        return pymupdf
    except ImportError:
        try:
            import fitz as pymupdf

            return pymupdf
        except ImportError as exc:
            from matrx_files._extras import MissingExtraError

            raise MissingExtraError("pdf", "pymupdf", "PDF manipulation") from exc


def build_info_payload(code: str, system_message: str, user_message: str) -> Any:
    """Build an info-event payload, preferring matrx-connect's typed model when present.

    Falls back to a plain dict with identical field names so emitters that
    accept dict-shaped payloads still work when matrx-connect is absent.
    """
    try:
        from matrx_connect.context.events import InfoPayload  # type: ignore

        return InfoPayload(
            code=code,
            system_message=system_message,
            user_message=user_message,
        )
    except ImportError:
        return {
            "code": code,
            "system_message": system_message,
            "user_message": user_message,
        }


def normalise_page_ranges(
    page_count: int,
    pages: list[int] | None = None,
    page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    default_all: bool = False,
) -> list[int]:
    """Resolve a mix of single pages + ranges into a sorted-unique list of 1-based page numbers.

    Returns the union of *pages* and the inclusive integer expansion of *page_ranges*,
    de-duplicated while preserving first-occurrence order. If neither is provided and
    *default_all* is True, returns every page in the document.
    """
    selected: list[int] = []

    if pages:
        selected.extend(int(page) for page in pages)

    if page_ranges:
        for page_range in page_ranges:
            start = getattr(page_range, "start", None)
            end = getattr(page_range, "end", None)
            if start is None and isinstance(page_range, dict):
                start = page_range.get("start")
                end = page_range.get("end")
            if start is None or end is None:
                raise ValueError("Page ranges must contain start and end.")
            start_int = int(start)
            end_int = int(end)
            if start_int > end_int:
                raise ValueError("Page range start must be <= end.")
            selected.extend(range(start_int, end_int + 1))

    if not selected and default_all:
        selected = list(range(1, page_count + 1))

    normalised: list[int] = []
    seen: set[int] = set()
    for page in selected:
        if page < 1 or page > page_count:
            raise ValueError(
                f"Page {page} is outside the document range 1..{page_count}."
            )
        if page not in seen:
            normalised.append(page)
            seen.add(page)
    return normalised


PROTECTED_PDF_MESSAGE = "This PDF is password protected. Give its password to continue."


def open_unprotected(pymupdf: Any, pdf_bytes: bytes) -> Any:
    """Open PDF bytes for a page operation, or say in a sentence why it cannot be (MuPDF only says "document
    closed or encrypted"). An open-password PDF is opened first with the password through the protect/unprotect
    tools; a page tool cannot read it."""
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    if getattr(doc, "needs_pass", False) or getattr(doc, "is_encrypted", False) and doc.page_count == 0:
        doc.close()
        raise ValueError(PROTECTED_PDF_MESSAGE)
    return doc


def save_pymupdf_doc(doc: Any) -> bytes:
    """Serialize a PyMuPDF Document to bytes for a page operation (crop, rotate, delete, reorder, merge...).

    ``garbage=4, deflate=True`` only. NOT ``clean=True``: MuPDF's content-stream sanitizer rewrites ``72 760 Td
    24 TL`` into ``72 760 TD`` and every following ``T*`` line lands 760 points down the page, so a valid
    hand-made PDF came back with all its text off the page (blank) after one crop or rotate (live walk 3).
    A page operation does not edit content streams, so it has nothing to sanitize. The redaction paths keep
    ``clean=True`` themselves (they must rewrite the content streams that held the removed text).
    """
    return doc.tobytes(garbage=4, deflate=True)


__all__ = [
    "load_pymupdf",
    "build_info_payload",
    "normalise_page_ranges",
    "open_unprotected",
    "PROTECTED_PDF_MESSAGE",
    "save_pymupdf_doc",
]
