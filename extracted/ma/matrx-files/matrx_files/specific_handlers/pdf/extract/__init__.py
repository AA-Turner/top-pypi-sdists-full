"""PDF extraction: text, OCR, tables, chunking."""

from .text import (
    PdfPageRangeError,
    resolve_page_range,
    extract_text_from_bytes_sync,
    extract_text_from_image_bytes,
    extract_text_pages,
    extract_text_pages_async,
    extract_text_pages_stream,
    extract_text_pages_from_bytes,
    extract_text_pages_from_bytes_async,
    format_page_text,
)
from .ocr import ocr_pymupdf_page
from .tables import (
    PdfExtractedTable,
    PdfTableBbox,
    PdfTableCell,
    PdfTablesPageScanned,
    PdfTablesReport,
    extract_tables,
    extract_tables_async,
    extract_tables_structured,
    extract_tables_structured_async,
    extract_tables_structured_stream,
)
from .chunking import chunk_page_text, chunk_text
from .bbox import (
    BboxExtractionResult,
    BboxRect,
    IntersectingImage,
    extract_at_bbox,
    extract_at_bbox_async,
)


__all__ = [
    "extract_text_pages",
    "extract_text_pages_async",
    "extract_text_pages_stream",
    "PdfPageRangeError",
    "resolve_page_range",
    "extract_text_pages_from_bytes",
    "extract_text_pages_from_bytes_async",
    "extract_text_from_bytes_sync",
    "extract_text_from_image_bytes",
    "format_page_text",
    "ocr_pymupdf_page",
    "extract_tables",
    "extract_tables_async",
    "extract_tables_structured",
    "extract_tables_structured_async",
    "extract_tables_structured_stream",
    "extract_at_bbox",
    "extract_at_bbox_async",
    "BboxRect",
    "BboxExtractionResult",
    "IntersectingImage",
    "PdfExtractedTable",
    "PdfTableBbox",
    "PdfTableCell",
    "PdfTablesPageScanned",
    "PdfTablesReport",
    "chunk_text",
    "chunk_page_text",
]
