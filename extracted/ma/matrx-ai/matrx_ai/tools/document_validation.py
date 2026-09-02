"""Shared lineage contract for drilling from processed text to physical pages."""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

MAX_PHYSICAL_PAGE_REF_PAGES = 10

PHYSICAL_PAGE_VALIDATION_GUIDANCE = (
    "Use processed clean/raw text and RAG chunks for normal reading and reasoning. "
    "When exact visual truth matters (poor OCR, handwriting, scans, tables, "
    "signatures, or a high-stakes claim), call document_content with "
    "action='images' and the referenced pages. It returns one PDF containing "
    "only those physical source pages; do not request the whole document."
)


def normalize_physical_pages(
    page_numbers: Iterable[Any] | None,
    *,
    limit: int = MAX_PHYSICAL_PAGE_REF_PAGES,
) -> list[int]:
    """Return unique positive 1-based pages in source order, bounded for vision."""
    if isinstance(page_numbers, str):
        try:
            decoded = json.loads(page_numbers)
            page_numbers = decoded if isinstance(decoded, list) else [decoded]
        except json.JSONDecodeError:
            page_numbers = page_numbers.split(",")
    normalized: list[int] = []
    seen: set[int] = set()
    for raw in page_numbers or ():
        try:
            page = int(raw)
        except (TypeError, ValueError):
            continue
        if page < 1 or page in seen:
            continue
        seen.add(page)
        normalized.append(page)
        if len(normalized) >= limit:
            break
    return normalized


def build_physical_page_ref(
    processed_document_id: Any,
    page_numbers: Iterable[Any] | None,
) -> dict[str, Any] | None:
    """Build the canonical agent handoff from text lineage to selected PDF pages."""
    document_id = str(processed_document_id).strip() if processed_document_id else ""
    pages = normalize_physical_pages(page_numbers)
    if not document_id or not pages:
        return None
    return {
        "document_id": document_id,
        "pages": pages,
        "suggested_tool": "document_content",
        "suggested_arguments": {
            "action": "images",
            "document_id": document_id,
            "pages": pages,
        },
        "purpose": "Selective visual validation against the original physical pages.",
    }


__all__ = [
    "MAX_PHYSICAL_PAGE_REF_PAGES",
    "PHYSICAL_PAGE_VALIDATION_GUIDANCE",
    "build_physical_page_ref",
    "normalize_physical_pages",
]
