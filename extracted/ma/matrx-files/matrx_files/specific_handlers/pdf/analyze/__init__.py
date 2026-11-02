"""Layout-analysis primitives + the auto-analysis detector battery.

Importing this module registers every PDF detector with the analysis dispatcher.

- ``models`` — Pydantic types for detector / classifier / reading-order output
- ``repeated_regions`` — DBSCAN-style header/footer/watermark detector
- ``layout`` — rule-based page classifier (cover / TOC / body / exhibit / billing / signature / appendix / blank / image-only / footer-only)
- ``reading_order`` — multi-column → linear reading order
- ``metadata`` — PDF info dict + per-page dimensions
- ``text_extraction`` — native + OCR text detectors
- ``embedded_images`` — XObject image enumeration
- ``duplicate_pages`` — five-way duplicate-page detection
- ``pattern_candidates`` — discover-only PII/regex spans
- ``page_classification`` / ``repeated_regions_detector`` / ``tables_detector`` —
  Detector-protocol wrappers around the layout/repeated-regions/table primitives.
"""

from .layout import classify_pages, classify_pages_async, classify_pages_stream
from .models import (
    LayoutClassificationReport,
    PageClass,
    PageClassification,
    ReadingOrderBlock,
    ReadingOrderPage,
    ReadingOrderReport,
    RegionKind,
    RepeatedRegion,
    RepeatedRegionBbox,
    RepeatedRegionsReport,
)
from .reading_order import (
    extract_reading_order,
    extract_reading_order_async,
    extract_reading_order_stream,
)
from .repeated_regions import (
    detect_repeated_regions,
    detect_repeated_regions_async,
    detect_repeated_regions_stream,
    normalize_block_text,
    strip_repeated_regions_text,
)

# Detector modules — importing them registers their factories with the analysis dispatcher.
from . import metadata as _metadata_module  # noqa: F401
from . import text_extraction as _text_module  # noqa: F401
from . import embedded_images as _images_module  # noqa: F401
from . import duplicate_pages as _dupes_module  # noqa: F401
from . import page_classification as _pgclass_module  # noqa: F401
from . import repeated_regions_detector as _rr_module  # noqa: F401
from . import tables_detector as _tables_module  # noqa: F401
from . import pattern_candidates as _patterns_module  # noqa: F401
from . import outline as _outline_module  # noqa: F401

# Re-export key functions for convenience.
from .metadata import extract_pdf_metadata, PdfFileMetadata, PdfPageDimensions


__all__ = [
    # Models
    "RegionKind",
    "PageClass",
    "RepeatedRegionBbox",
    "RepeatedRegion",
    "RepeatedRegionsReport",
    "PageClassification",
    "LayoutClassificationReport",
    "ReadingOrderBlock",
    "ReadingOrderPage",
    "ReadingOrderReport",
    "PdfFileMetadata",
    "PdfPageDimensions",
    # Detectors / primitives
    "detect_repeated_regions",
    "detect_repeated_regions_async",
    "detect_repeated_regions_stream",
    "normalize_block_text",
    "strip_repeated_regions_text",
    "classify_pages",
    "classify_pages_async",
    "classify_pages_stream",
    "extract_reading_order",
    "extract_reading_order_async",
    "extract_reading_order_stream",
    "extract_pdf_metadata",
]
