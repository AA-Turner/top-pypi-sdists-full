"""PDF subsystem for matrx-utils.

This package replaced the historical monolithic ``pdf_handler.py``. That module's
re-export shim was removed in PDF-PLAN U3: import every PDF symbol from
``matrx_files.specific_handlers.pdf`` (this package).

Layout (Stage 2, design §4.1):

- ``models``         — Pydantic types and the AiChunkProcessor protocol
- ``internal``       — private helpers (lazy pymupdf, info-payload builder,
                       page-range normalizer, optimized save)
- ``concurrency``    — ThreadPoolExecutors for CPU and OCR work + asyncio wrappers
- ``tmp``            — namespaced temp-file management + startup cleanup hook
- ``ops/``           — page operations: extract, crop, rotate, delete, merge,
                       split, compress
- ``extract/``       — text, OCR, tables, chunking
- ``pipelines/``     — AI chunk processing and the full ingestion pipeline
- ``analyze/``       — (Phase 3) repeated-region detection, layout classifier,
                       reading order
- ``studio/``        — (Phase 2) preset catalog and render-spec dispatcher
- ``ml/``            — (Phase 7) pluggable layout providers (Docling, MinerU, …)
- ``cloud_ocr/``     — (Phase 7) pluggable OCR providers (Mistral, Azure, …)
- ``generate/``      — (Phase 8) HTML/Markdown/URL → PDF

Per CLAUDE.md, every submodule respects the package-independence rule — no
top-level imports of any sibling matrx-* package or aidream/ module.
"""

from __future__ import annotations

from .analyze import (
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
    classify_pages,
    classify_pages_async,
    classify_pages_stream,
    detect_repeated_regions,
    detect_repeated_regions_async,
    detect_repeated_regions_stream,
    extract_reading_order,
    extract_reading_order_async,
    extract_reading_order_stream,
    normalize_block_text,
    strip_repeated_regions_text,
)
from .extract.chunking import chunk_page_text, chunk_text
from .extract.tables import (
    PdfExtractedTable,
    PdfTableBbox,
    PdfTablesPageScanned,
    PdfTablesReport,
    extract_tables_structured,
    extract_tables_structured_async,
    extract_tables_structured_stream,
)
from .redact import (
    BUILTIN_PATTERNS,
    RedactionAudit,
    RedactionKind,
    RedactionRegion,
    RedactionResult,
    RedactionStatus,
    RedactionTier,
    Replacement,
    flatten_annotations,
    flatten_annotations_async,
    list_builtin_patterns,
    redact_pattern,
    redact_pattern_async,
    redact_regions,
    redact_regions_async,
    redact_repeated_regions,
    redact_repeated_regions_async,
    scrub_categories,
    scrub_categories_async,
    strip_all_pii,
    strip_all_pii_async,
    strip_attachments,
    strip_attachments_async,
    strip_javascript,
    strip_javascript_async,
    strip_metadata,
    strip_metadata_async,
)
from .extract.ocr import ocr_image_bytes, ocr_pymupdf_page
from .extract.tables import extract_tables, extract_tables_async
from .extract.text import (
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
from .handler import PDFHandler
from .internal import (
    build_info_payload,
    load_pymupdf,
    normalise_page_ranges,
    save_pymupdf_doc,
)
from .models import (
    AiChunkProcessor,
    PdfBinaryResult,
    PdfChunkedTextResult,
    PdfCropBox,
    PdfPageRange,
    PdfPageSpan,
    PdfExtractStart,
    PdfPageScanned,
    PdfPageText,
    PdfPipelineOptions,
    PdfResult,
    PdfSplitPart,
    PdfTextBlock,
    PdfTextChunk,
    PdfTextWord,
)
from .ops.compose import (
    merge_pdfs_from_bytes,
    merge_pdfs_from_bytes_async,
    split_pdf_bytes,
    split_pdf_bytes_async,
)
from .ops.compress import (
    MAX_LEVEL as COMPRESS_MAX_LEVEL,
    MIN_LEVEL as COMPRESS_MIN_LEVEL,
    TIERS as COMPRESS_TIERS,
    CompressResult,
    CompressTier,
    compress_pdf_bytes,
    compress_pdf_bytes_async,
    compress_pdf_bytes_capped,
    compress_pdf_bytes_capped_async,
)
from .ops.forms import (
    PdfMark,
    fill_form_bytes,
    flatten_form_bytes,
    list_form_fields_bytes,
    list_marks_bytes,
    place_marks_bytes,
    read_form_values_bytes,
)
from .ops.redact_real import (
    RedactBox,
    RedactFindSpec,
    RedactSanitize,
    find_redaction_hits_bytes,
    redact_pdf_bytes,
    sanitize_report_bytes,
)
from .ops.outline import PdfOutlineNode, read_outline_bytes, set_outline_bytes
from .ops.properties import read_properties_bytes, set_properties_bytes
from .ops.protect import protect_pdf_bytes, unprotect_pdf_bytes
from .ops.stamp import (
    BUILTIN_HEADER_FOOTER_TEMPLATES,
    PdfHeaderFooterTemplate,
    PdfStampSpec,
    apply_header_footer_bytes,
    stamp_pdf_bytes,
)
from .ops.pages import (
    crop_pages_in_bytes,
    crop_pages_in_bytes_async,
    delete_pages_from_bytes,
    delete_pages_from_bytes_async,
    duplicate_pages_in_bytes,
    duplicate_pages_in_bytes_async,
    extract_pages_from_bytes,
    extract_pages_from_bytes_async,
    extract_pages_from_path,
    extract_pages_from_path_async,
    insert_pages_in_bytes,
    insert_pages_in_bytes_async,
    reorder_pages_in_bytes,
    reorder_pages_in_bytes_async,
    rotate_pages_in_bytes,
    rotate_pages_in_bytes_async,
)
from .ops.render import (
    PdfPageRender,
    iter_render_pages_to_image_bytes,
    render_all_pages_to_image_bytes,
    render_all_pages_to_image_bytes_async,
    render_page_to_image_bytes,
    render_page_to_image_bytes_async,
    render_thumbnail_bytes,
    render_thumbnail_bytes_async,
)
from .pipelines.ai import process_chunks_with_ai
from .studio import (
    ALL_PDF_PRESETS,
    PDF_PRESETS_BY_ID,
    PRESET_CATEGORIES,
    PdfRenderSpec,
    PdfStudioBundle,
    PdfStudioCategory,
    PdfStudioPreset,
    PdfStudioRenderResult,
    RECOMMENDED_PDF_BUNDLES,
    get_pdf_preset_by_id,
    render_studio_variant,
    render_studio_variant_async,
)
from .studio.presets import (
    PdfStudioBundleSchema,
    PdfStudioCatalog,
    PdfStudioCategorySchema,
    PdfStudioPresetSchema,
)
from .wire import (
    PdfRedactionPatternCatalog,
    PdfRedactionPatternEntry,
    PersistedPdfFile,
    PersistedRedactionResult,
    StripRepeatedRegionsResultSchema,
)
from .tmp import (
    cleanup_tmp_older_than,
    install_startup_cleanup_hook,
    pdf_temp_dir,
    pdf_temp_file,
    write_pdf_bytes_to_temp,
)


# Legacy alias — the original module exposed this symbol verbatim.
extract_text_from_pdf_bytes_sync = extract_text_from_bytes_sync


__all__ = [
    # Models (stable wire contracts)
    "AiChunkProcessor",
    "PdfBinaryResult",
    "PdfChunkedTextResult",
    "PdfCropBox",
    "PdfPageRange",
    "PdfPageSpan",
    "PdfExtractStart",
    "PdfPageScanned",
    "PdfPageText",
    "PdfPipelineOptions",
    "PdfResult",
    "PdfSplitPart",
    "PdfTextBlock",
    "PdfTextChunk",
    "PdfTextWord",
    # Handler
    "PDFHandler",
    # Public function surface (mirrors handler methods for non-FileHandler callers)
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
    "merge_pdfs_from_bytes",
    "merge_pdfs_from_bytes_async",
    "split_pdf_bytes",
    "split_pdf_bytes_async",
    "compress_pdf_bytes",
    "compress_pdf_bytes_async",
    "compress_pdf_bytes_capped",
    "compress_pdf_bytes_capped_async",
    "PdfMark",
    "fill_form_bytes",
    "flatten_form_bytes",
    "list_form_fields_bytes",
    "list_marks_bytes",
    "place_marks_bytes",
    "read_form_values_bytes",
    "RedactBox",
    "RedactFindSpec",
    "RedactSanitize",
    "find_redaction_hits_bytes",
    "redact_pdf_bytes",
    "sanitize_report_bytes",
    "PdfOutlineNode",
    "read_outline_bytes",
    "set_outline_bytes",
    "read_properties_bytes",
    "set_properties_bytes",
    "protect_pdf_bytes",
    "unprotect_pdf_bytes",
    "BUILTIN_HEADER_FOOTER_TEMPLATES",
    "PdfHeaderFooterTemplate",
    "PdfStampSpec",
    "apply_header_footer_bytes",
    "stamp_pdf_bytes",
    "CompressResult",
    "CompressTier",
    "COMPRESS_TIERS",
    "COMPRESS_MIN_LEVEL",
    "COMPRESS_MAX_LEVEL",
    # Render
    "PdfPageRender",
    "render_page_to_image_bytes",
    "render_page_to_image_bytes_async",
    "iter_render_pages_to_image_bytes",
    "render_all_pages_to_image_bytes",
    "render_all_pages_to_image_bytes_async",
    "render_thumbnail_bytes",
    "render_thumbnail_bytes_async",
    # Studio
    "PdfRenderSpec",
    "PdfStudioBundle",
    "PdfStudioCategory",
    "PdfStudioPreset",
    "PdfStudioRenderResult",
    "PRESET_CATEGORIES",
    "ALL_PDF_PRESETS",
    "PDF_PRESETS_BY_ID",
    "RECOMMENDED_PDF_BUNDLES",
    "get_pdf_preset_by_id",
    "render_studio_variant",
    "render_studio_variant_async",
    # Analyze (Phase 3)
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
    "extract_text_pages",
    "extract_text_pages_async",
    "extract_text_pages_stream",
    "PdfPageRangeError",
    "resolve_page_range",
    "extract_text_pages_from_bytes",
    "extract_text_pages_from_bytes_async",
    "format_page_text",
    "extract_text_from_image_bytes",
    "extract_text_from_bytes_sync",
    "extract_text_from_pdf_bytes_sync",
    "ocr_pymupdf_page",
    "ocr_image_bytes",
    "extract_tables",
    "extract_tables_async",
    "chunk_text",
    "chunk_page_text",
    "process_chunks_with_ai",
    # Internal helpers (re-exported because Stage 2 phases use them)
    "load_pymupdf",
    "build_info_payload",
    "normalise_page_ranges",
    "save_pymupdf_doc",
    # Temp management
    "pdf_temp_dir",
    "pdf_temp_file",
    "write_pdf_bytes_to_temp",
    "cleanup_tmp_older_than",
    "install_startup_cleanup_hook",
    # Redact (Phase 4)
    "Replacement",
    "RedactionKind",
    "RedactionStatus",
    "RedactionTier",
    "RedactionRegion",
    "RedactionAudit",
    "RedactionResult",
    "redact_regions",
    "redact_regions_async",
    "redact_pattern",
    "redact_pattern_async",
    "BUILTIN_PATTERNS",
    "list_builtin_patterns",
    "redact_repeated_regions",
    "redact_repeated_regions_async",
    "strip_metadata",
    "strip_metadata_async",
    "strip_attachments",
    "strip_attachments_async",
    "strip_javascript",
    "strip_javascript_async",
    "flatten_annotations",
    "flatten_annotations_async",
    "strip_all_pii",
    "strip_all_pii_async",
    "scrub_categories",
    "scrub_categories_async",
    # Phase 5 table extraction (structured)
    "PdfExtractedTable",
    "PdfTableBbox",
    "PdfTablesPageScanned",
    "PdfTablesReport",
    "extract_tables_structured",
    "extract_tables_structured_async",
    "extract_tables_structured_stream",
    # Studio wire schemas
    "PdfStudioCatalog",
    "PdfStudioPresetSchema",
    "PdfStudioCategorySchema",
    "PdfStudioBundleSchema",
    # Wire schemas for endpoint responses
    "PdfRedactionPatternCatalog",
    "PdfRedactionPatternEntry",
    "PersistedPdfFile",
    "PersistedRedactionResult",
    "StripRepeatedRegionsResultSchema",
]
