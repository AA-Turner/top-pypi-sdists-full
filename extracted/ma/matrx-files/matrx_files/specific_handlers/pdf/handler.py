"""``PDFHandler`` — the FileHandler-bound orchestrator.

This class is a thin wrapper around the standalone functions in the sibling
submodules. It exists for three reasons:

1. **Backwards compatibility.** Every caller in the aidream repo and downstream
   apps imports ``PDFHandler`` from this package; the class signature and
   method names must remain stable.
2. **FileHandler integration.** Methods that need cloud read/write, temp paths,
   or printing inherit those from ``FileHandler``. The free functions in
   ``ops/`` / ``extract/`` / ``pipelines/`` deliberately don't know about
   ``FileHandler``.
3. **Routing of the full pipeline.** ``full_pipeline`` resolves a remote source,
   runs extraction, optionally chunks and processes with AI, optionally
   uploads to cloud storage — it's the only place that touches all of those.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import pypdfium2 as pdfium

from matrx_files.file_handler import FileHandler

from .analyze import (
    LayoutClassificationReport,
    ReadingOrderReport,
    RepeatedRegionsReport,
    classify_pages,
    classify_pages_async,
    detect_repeated_regions,
    detect_repeated_regions_async,
    extract_reading_order,
    extract_reading_order_async,
    strip_repeated_regions_text,
)
from .extract.chunking import chunk_page_text, chunk_text
from .extract.tables import PdfTablesReport, extract_tables, extract_tables_async
from .extract.text import (
    extract_text_from_bytes_sync,
    extract_text_from_image_bytes,
    extract_text_pages,
    extract_text_pages_async,
    extract_text_pages_stream,
    extract_text_pages_from_bytes,
    extract_text_pages_from_bytes_async,
    format_page_text,
)
from .internal import build_info_payload
from .models import (
    PdfExtractStart,
    AiChunkProcessor,
    PdfBinaryResult,
    PdfChunkedTextResult,
    PdfCropBox,
    PdfPageRange,
    PdfPageText,
    PdfPipelineOptions,
    PdfResult,
    PdfSplitPart,
)
from .ops.compose import (
    merge_pdfs_from_bytes,
    merge_pdfs_from_bytes_async,
    split_pdf_bytes,
    split_pdf_bytes_async,
)
from .ops.compress import (
    CompressResult,
    compress_pdf_bytes,
    compress_pdf_bytes_async,
    compress_pdf_bytes_capped,
    compress_pdf_bytes_capped_async,
)
from .ops.compare import compare_pdf_bytes_async
from .ops.convert import convert_pdf_bytes_async
from .ops.ocr import ocr_pdf_bytes_async
from .ops.forms import (
    fill_form_bytes_async,
    flatten_form_bytes_async,
    list_form_fields_bytes_async,
    place_marks_bytes_async,
)
from .ops.redact_real import find_redaction_hits_bytes_async, redact_pdf_bytes_async, sanitize_report_bytes_async
from .ops.outline import read_outline_bytes_async, set_outline_bytes_async
from .ops.replace import find_replace_preview_async, replace_pdf_bytes_async
from .ops.properties import read_properties_bytes_async, set_properties_bytes_async
from .ops.protect import protect_pdf_bytes_async, unprotect_pdf_bytes_async
from .ops.stamp import apply_header_footer_bytes_async, stamp_pdf_bytes_async
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
    render_all_pages_to_image_bytes,
    render_all_pages_to_image_bytes_async,
    render_page_to_image_bytes,
    render_page_to_image_bytes_async,
    render_thumbnail_bytes,
    render_thumbnail_bytes_async,
)
from .pipelines.ai import process_chunks_with_ai
from .redact import (
    BUILTIN_PATTERNS,
    RedactionAudit,
    RedactionRegion,
    RedactionResult,
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
from .studio.render_spec import (
    PdfRenderSpec,
    PdfStudioRenderResult,
    render_studio_variant,
    render_studio_variant_async,
)
from .tmp import pdf_temp_file


class PDFHandler(FileHandler):
    def __init__(self, app_name: str, batch_print: bool = False):
        super().__init__(app_name, batch_print=batch_print)

    # ------------------------------------------------------------------
    # In-memory PDF manipulation — sync + async pairs
    # ------------------------------------------------------------------

    def extract_pages_from_bytes(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return extract_pages_from_bytes(pdf_bytes, pages, page_ranges)

    async def extract_pages_from_bytes_async(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return await extract_pages_from_bytes_async(pdf_bytes, pages, page_ranges)

    def extract_pages_from_path(
        self,
        pdf_path: str,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return extract_pages_from_path(pdf_path, pages, page_ranges)

    async def extract_pages_from_path_async(
        self,
        pdf_path: str,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return await extract_pages_from_path_async(pdf_path, pages, page_ranges)

    def crop_pages_in_bytes(
        self,
        pdf_bytes: bytes,
        crop_box: PdfCropBox | dict[str, Any],
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return crop_pages_in_bytes(pdf_bytes, crop_box, pages, page_ranges)

    async def crop_pages_in_bytes_async(
        self,
        pdf_bytes: bytes,
        crop_box: PdfCropBox | dict[str, Any],
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return await crop_pages_in_bytes_async(pdf_bytes, crop_box, pages, page_ranges)

    def rotate_pages_in_bytes(
        self,
        pdf_bytes: bytes,
        rotation: int,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return rotate_pages_in_bytes(pdf_bytes, rotation, pages, page_ranges)

    async def rotate_pages_in_bytes_async(
        self,
        pdf_bytes: bytes,
        rotation: int,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return await rotate_pages_in_bytes_async(
            pdf_bytes, rotation, pages, page_ranges
        )

    def delete_pages_from_bytes(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return delete_pages_from_bytes(pdf_bytes, pages, page_ranges)

    async def delete_pages_from_bytes_async(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
    ) -> PdfBinaryResult:
        return await delete_pages_from_bytes_async(pdf_bytes, pages, page_ranges)

    def merge_pdfs_from_bytes(
        self, sources: list[dict[str, Any]]
    ) -> PdfBinaryResult:
        return merge_pdfs_from_bytes(sources)

    async def merge_pdfs_from_bytes_async(
        self, sources: list[dict[str, Any]]
    ) -> PdfBinaryResult:
        return await merge_pdfs_from_bytes_async(sources)

    def split_pdf_bytes(
        self,
        pdf_bytes: bytes,
        parts: list[dict[str, Any]] | None = None,
        max_pages_per_part: int | None = None,
    ) -> list[PdfSplitPart]:
        return split_pdf_bytes(pdf_bytes, parts, max_pages_per_part)

    async def split_pdf_bytes_async(
        self,
        pdf_bytes: bytes,
        parts: list[dict[str, Any]] | None = None,
        max_pages_per_part: int | None = None,
    ) -> list[PdfSplitPart]:
        return await split_pdf_bytes_async(pdf_bytes, parts, max_pages_per_part)

    def compress_pdf_bytes(self, pdf_bytes: bytes, level: int = 2) -> bytes:
        return compress_pdf_bytes(pdf_bytes, level)

    async def compress_pdf_bytes_async(
        self, pdf_bytes: bytes, level: int = 2
    ) -> bytes:
        return await compress_pdf_bytes_async(pdf_bytes, level)

    def compress_pdf_bytes_capped(
        self,
        pdf_bytes: bytes,
        *,
        level: int = 2,
        max_size_bytes: int | None = None,
    ) -> CompressResult:
        return compress_pdf_bytes_capped(
            pdf_bytes, level=level, max_size_bytes=max_size_bytes
        )

    async def compress_pdf_bytes_capped_async(
        self,
        pdf_bytes: bytes,
        *,
        level: int = 2,
        max_size_bytes: int | None = None,
    ) -> CompressResult:
        return await compress_pdf_bytes_capped_async(
            pdf_bytes, level=level, max_size_bytes=max_size_bytes
        )

    # ------------------------------------------------------------------
    # U11: protect, stamp, bookmarks, properties, header/footer (pikepdf; never PyMuPDF)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # U12/U13: real redaction, forms, Fill and Sign (permissive stack; never PyMuPDF)
    # ------------------------------------------------------------------

    async def find_redaction_hits_bytes_async(self, pdf_bytes: bytes, spec: Any, **kwargs: Any) -> dict[str, Any]:
        return await find_redaction_hits_bytes_async(pdf_bytes, spec, **kwargs)

    async def redact_pdf_bytes_async(self, pdf_bytes: bytes, boxes: list[Any], **kwargs: Any) -> PdfBinaryResult:
        return await redact_pdf_bytes_async(pdf_bytes, boxes, **kwargs)

    async def sanitize_report_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
        return await sanitize_report_bytes_async(pdf_bytes, **kwargs)

    async def list_form_fields_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
        return await list_form_fields_bytes_async(pdf_bytes, **kwargs)

    async def fill_form_bytes_async(self, pdf_bytes: bytes, values: dict[str, Any], **kwargs: Any) -> PdfBinaryResult:
        return await fill_form_bytes_async(pdf_bytes, values, **kwargs)

    async def flatten_form_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await flatten_form_bytes_async(pdf_bytes, **kwargs)

    async def place_marks_bytes_async(self, pdf_bytes: bytes, marks: list[Any], **kwargs: Any) -> PdfBinaryResult:
        return await place_marks_bytes_async(pdf_bytes, marks, **kwargs)

    async def protect_pdf_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await protect_pdf_bytes_async(pdf_bytes, **kwargs)

    async def unprotect_pdf_bytes_async(self, pdf_bytes: bytes, *, password: str) -> PdfBinaryResult:
        return await unprotect_pdf_bytes_async(pdf_bytes, password=password)

    async def stamp_pdf_bytes_async(self, pdf_bytes: bytes, specs: list[Any], **kwargs: Any) -> PdfBinaryResult:
        return await stamp_pdf_bytes_async(pdf_bytes, specs, **kwargs)

    async def apply_header_footer_bytes_async(self, pdf_bytes: bytes, template: Any, **kwargs: Any) -> PdfBinaryResult:
        return await apply_header_footer_bytes_async(pdf_bytes, template, **kwargs)

    async def read_outline_bytes_async(self, pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
        return await read_outline_bytes_async(pdf_bytes, password=password)

    async def set_outline_bytes_async(self, pdf_bytes: bytes, items: list[Any], *, password: str = "") -> PdfBinaryResult:
        return await set_outline_bytes_async(pdf_bytes, items, password=password)

    async def read_properties_bytes_async(self, pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
        return await read_properties_bytes_async(pdf_bytes, password=password)

    async def set_properties_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await set_properties_bytes_async(pdf_bytes, **kwargs)

    # ------------------------------------------------------------------
    # U14: OCR to a searchable PDF, convert to Office, compare, find and replace (permissive stack)
    # ------------------------------------------------------------------

    async def ocr_pdf_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await ocr_pdf_bytes_async(pdf_bytes, **kwargs)

    async def convert_pdf_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await convert_pdf_bytes_async(pdf_bytes, **kwargs)

    async def compare_pdf_bytes_async(self, a_bytes: bytes, b_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
        return await compare_pdf_bytes_async(a_bytes, b_bytes, **kwargs)

    async def find_replace_preview_async(self, pdf_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
        return await find_replace_preview_async(pdf_bytes, **kwargs)

    async def replace_pdf_bytes_async(self, pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
        return await replace_pdf_bytes_async(pdf_bytes, **kwargs)

    # ------------------------------------------------------------------
    # Phase 2: page reorder / insert / duplicate
    # ------------------------------------------------------------------

    def reorder_pages_in_bytes(
        self, pdf_bytes: bytes, new_order: list[int]
    ) -> PdfBinaryResult:
        return reorder_pages_in_bytes(pdf_bytes, new_order)

    async def reorder_pages_in_bytes_async(
        self, pdf_bytes: bytes, new_order: list[int]
    ) -> PdfBinaryResult:
        return await reorder_pages_in_bytes_async(pdf_bytes, new_order)

    def insert_pages_in_bytes(
        self,
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
        return insert_pages_in_bytes(
            target_pdf_bytes,
            source_pdf_bytes,
            after_page=after_page,
            source_pages=source_pages,
            source_page_ranges=source_page_ranges,
            include_links=include_links,
            include_annotations=include_annotations,
            include_widgets=include_widgets,
            join_duplicates=join_duplicates,
        )

    async def insert_pages_in_bytes_async(
        self,
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
        return await insert_pages_in_bytes_async(
            target_pdf_bytes,
            source_pdf_bytes,
            after_page=after_page,
            source_pages=source_pages,
            source_page_ranges=source_page_ranges,
            include_links=include_links,
            include_annotations=include_annotations,
            include_widgets=include_widgets,
            join_duplicates=join_duplicates,
        )

    def duplicate_pages_in_bytes(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
        count: int = 1,
    ) -> PdfBinaryResult:
        return duplicate_pages_in_bytes(
            pdf_bytes, pages=pages, page_ranges=page_ranges, count=count
        )

    async def duplicate_pages_in_bytes_async(
        self,
        pdf_bytes: bytes,
        pages: list[int] | None = None,
        page_ranges: list[PdfPageRange | dict[str, Any]] | None = None,
        count: int = 1,
    ) -> PdfBinaryResult:
        return await duplicate_pages_in_bytes_async(
            pdf_bytes, pages=pages, page_ranges=page_ranges, count=count
        )

    # ------------------------------------------------------------------
    # Phase 2: render
    # ------------------------------------------------------------------

    def render_page_to_image_bytes(
        self,
        pdf_bytes: bytes,
        page: int = 1,
        dpi: int = 150,
        fmt: str = "png",
        colorspace: str = "rgb",
        alpha: bool = False,
        annotations: bool = True,
        jpeg_quality: int = 85,
        clip: tuple[float, float, float, float] | None = None,
    ) -> PdfPageRender:
        return render_page_to_image_bytes(
            pdf_bytes,
            page=page,
            dpi=dpi,
            fmt=fmt,
            colorspace=colorspace,
            alpha=alpha,
            annotations=annotations,
            jpeg_quality=jpeg_quality,
            clip=clip,
        )

    async def render_page_to_image_bytes_async(
        self,
        pdf_bytes: bytes,
        page: int = 1,
        dpi: int = 150,
        fmt: str = "png",
        colorspace: str = "rgb",
        alpha: bool = False,
        annotations: bool = True,
        jpeg_quality: int = 85,
        clip: tuple[float, float, float, float] | None = None,
    ) -> PdfPageRender:
        return await render_page_to_image_bytes_async(
            pdf_bytes,
            page=page,
            dpi=dpi,
            fmt=fmt,
            colorspace=colorspace,
            alpha=alpha,
            annotations=annotations,
            jpeg_quality=jpeg_quality,
            clip=clip,
        )

    def render_all_pages_to_image_bytes(
        self,
        pdf_bytes: bytes,
        dpi: int = 150,
        fmt: str = "png",
        colorspace: str = "rgb",
        alpha: bool = False,
        annotations: bool = True,
        jpeg_quality: int = 85,
        pages: list[int] | None = None,
    ) -> list[PdfPageRender]:
        return render_all_pages_to_image_bytes(
            pdf_bytes,
            dpi=dpi,
            fmt=fmt,
            colorspace=colorspace,
            alpha=alpha,
            annotations=annotations,
            jpeg_quality=jpeg_quality,
            pages=pages,
        )

    async def render_all_pages_to_image_bytes_async(
        self,
        pdf_bytes: bytes,
        dpi: int = 150,
        fmt: str = "png",
        colorspace: str = "rgb",
        alpha: bool = False,
        annotations: bool = True,
        jpeg_quality: int = 85,
        pages: list[int] | None = None,
    ) -> list[PdfPageRender]:
        return await render_all_pages_to_image_bytes_async(
            pdf_bytes,
            dpi=dpi,
            fmt=fmt,
            colorspace=colorspace,
            alpha=alpha,
            annotations=annotations,
            jpeg_quality=jpeg_quality,
            pages=pages,
        )

    def render_thumbnail_bytes(
        self,
        pdf_bytes: bytes,
        page: int = 1,
        max_side: int = 256,
        fmt: str = "jpeg",
        jpeg_quality: int = 80,
    ) -> PdfPageRender:
        return render_thumbnail_bytes(
            pdf_bytes,
            page=page,
            max_side=max_side,
            fmt=fmt,
            jpeg_quality=jpeg_quality,
        )

    async def render_thumbnail_bytes_async(
        self,
        pdf_bytes: bytes,
        page: int = 1,
        max_side: int = 256,
        fmt: str = "jpeg",
        jpeg_quality: int = 80,
    ) -> PdfPageRender:
        return await render_thumbnail_bytes_async(
            pdf_bytes,
            page=page,
            max_side=max_side,
            fmt=fmt,
            jpeg_quality=jpeg_quality,
        )

    def render_studio_variant(
        self,
        pdf_bytes: bytes,
        spec: PdfRenderSpec,
    ) -> PdfStudioRenderResult:
        return render_studio_variant(pdf_bytes, spec)

    async def render_studio_variant_async(
        self,
        pdf_bytes: bytes,
        spec: PdfRenderSpec,
    ) -> PdfStudioRenderResult:
        return await render_studio_variant_async(pdf_bytes, spec)

    # ------------------------------------------------------------------
    # Phase 3: layout analysis
    # ------------------------------------------------------------------

    def detect_repeated_regions(
        self,
        pdf_bytes: bytes,
        *,
        min_pages_ratio: float = 1 / 3,
        min_confidence: float = 0.5,
    ) -> RepeatedRegionsReport:
        return detect_repeated_regions(
            pdf_bytes,
            min_pages_ratio=min_pages_ratio,
            min_confidence=min_confidence,
        )

    async def detect_repeated_regions_async(
        self,
        pdf_bytes: bytes,
        *,
        min_pages_ratio: float = 1 / 3,
        min_confidence: float = 0.5,
    ) -> RepeatedRegionsReport:
        return await detect_repeated_regions_async(
            pdf_bytes,
            min_pages_ratio=min_pages_ratio,
            min_confidence=min_confidence,
        )

    def strip_repeated_regions_text(
        self,
        pages_text: list[str],
        regions,
        accepted_region_ids: set[str] | None = None,
    ) -> list[str]:
        return strip_repeated_regions_text(pages_text, regions, accepted_region_ids)

    def classify_pages(self, pdf_bytes: bytes) -> LayoutClassificationReport:
        return classify_pages(pdf_bytes)

    async def classify_pages_async(
        self, pdf_bytes: bytes
    ) -> LayoutClassificationReport:
        return await classify_pages_async(pdf_bytes)

    def extract_reading_order(self, pdf_bytes: bytes) -> ReadingOrderReport:
        return extract_reading_order(pdf_bytes)

    async def extract_reading_order_async(
        self, pdf_bytes: bytes
    ) -> ReadingOrderReport:
        return await extract_reading_order_async(pdf_bytes)

    # ------------------------------------------------------------------
    # Phase 4: redaction & privacy
    # ------------------------------------------------------------------

    def redact_regions(
        self,
        pdf_bytes: bytes,
        regions: list[RedactionRegion],
        *,
        reason: str,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
    ) -> RedactionResult:
        return redact_regions(
            pdf_bytes,
            regions,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
        )

    async def redact_regions_async(
        self,
        pdf_bytes: bytes,
        regions: list[RedactionRegion],
        *,
        reason: str,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
    ) -> RedactionResult:
        return await redact_regions_async(
            pdf_bytes,
            regions,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
        )

    def redact_pattern(
        self,
        pdf_bytes: bytes,
        pattern: str,
        *,
        reason: str,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
        flags: int = 0,
    ) -> RedactionResult:
        return redact_pattern(
            pdf_bytes,
            pattern,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
            flags=flags,
        )

    async def redact_pattern_async(
        self,
        pdf_bytes: bytes,
        pattern: str,
        *,
        reason: str,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
        flags: int = 0,
    ) -> RedactionResult:
        return await redact_pattern_async(
            pdf_bytes,
            pattern,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
            flags=flags,
        )

    def redact_repeated_regions(
        self,
        pdf_bytes: bytes,
        regions,
        *,
        reason: str,
        accepted_region_ids: set[str] | None = None,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
    ) -> RedactionResult:
        return redact_repeated_regions(
            pdf_bytes,
            regions,
            accepted_region_ids=accepted_region_ids,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
        )

    async def redact_repeated_regions_async(
        self,
        pdf_bytes: bytes,
        regions,
        *,
        reason: str,
        accepted_region_ids: set[str] | None = None,
        user_id: str | None = None,
        parent_file_id: str | None = None,
        scrub_metadata: bool = True,
    ) -> RedactionResult:
        return await redact_repeated_regions_async(
            pdf_bytes,
            regions,
            accepted_region_ids=accepted_region_ids,
            reason=reason,
            user_id=user_id,
            parent_file_id=parent_file_id,
            scrub_metadata=scrub_metadata,
        )

    def strip_metadata(self, pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
        return strip_metadata(pdf_bytes, **kwargs)

    async def strip_metadata_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await strip_metadata_async(pdf_bytes, **kwargs)

    def strip_attachments(self, pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
        return strip_attachments(pdf_bytes, **kwargs)

    async def strip_attachments_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await strip_attachments_async(pdf_bytes, **kwargs)

    def strip_javascript(self, pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
        return strip_javascript(pdf_bytes, **kwargs)

    async def strip_javascript_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await strip_javascript_async(pdf_bytes, **kwargs)

    def flatten_annotations(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return flatten_annotations(pdf_bytes, **kwargs)

    async def flatten_annotations_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await flatten_annotations_async(pdf_bytes, **kwargs)

    def strip_all_pii(self, pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
        return strip_all_pii(pdf_bytes, **kwargs)

    async def strip_all_pii_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await strip_all_pii_async(pdf_bytes, **kwargs)

    def scrub_categories(self, pdf_bytes: bytes, **kwargs: Any) -> RedactionResult:
        return scrub_categories(pdf_bytes, **kwargs)

    async def scrub_categories_async(
        self, pdf_bytes: bytes, **kwargs: Any
    ) -> RedactionResult:
        return await scrub_categories_async(pdf_bytes, **kwargs)

    # ------------------------------------------------------------------
    # Legacy pypdfium2-based read/write (kept for backwards compatibility)
    # ------------------------------------------------------------------

    def read_pdf_file(self, path: str) -> pdfium.PdfDocument | None:
        try:
            doc = pdfium.PdfDocument(path)
            self._print_link(path=path, message="Read PDF file")
            return doc
        except Exception as exc:
            self._print_link(path=path, message="Error reading PDF", color="red")
            print(f"Error: {exc}")
            return None

    def _return_if_pdf_valid(self, pdf: Any) -> pdfium.PdfDocument | None:
        if pdf and isinstance(pdf, pdfium.PdfDocument):
            return pdf
        return None

    def custom_read_pdf(self, path: str) -> pdfium.PdfDocument | None:
        doc = self.read_pdf_file(path)
        return self._return_if_pdf_valid(doc)

    def custom_delete_pdf(self, path: str) -> bool:
        return self.delete(path)

    def read_pdf(self, root: str, path: str) -> pdfium.PdfDocument | None:
        full_path = self._get_full_path(root, path)
        return self.read_pdf_file(str(full_path))

    def delete_pdf(self, root: str, path: str) -> bool:
        return self.delete_from_base(root, path)

    # ------------------------------------------------------------------
    # Remote fetch — URL, file descriptor, or local path
    # ------------------------------------------------------------------

    async def fetch_remote(self, source: str | dict) -> str | None:
        """Resolve *source* to a local temp file path.

        Accepts a plain URL string (downloaded via httpx), a file descriptor
        dict resolved from its URL, or a local file
        path string (returned as-is if the file exists).
        """
        if isinstance(source, dict):
            return await self._fetch_file_object(source)

        if isinstance(source, str):
            if source.startswith("http://") or source.startswith("https://"):
                return await self._download_url(source)
            if os.path.isfile(source):
                return source

        return None

    # Hard ceiling on remote downloads — without it a single request pointing
    # at a multi-GB URL buffered the whole body in memory (response.content).
    MAX_REMOTE_DOWNLOAD_BYTES = 200 * 1024 * 1024  # matches the upload cap

    async def _download_url(self, url: str, extension: str = "pdf") -> str | None:
        # If this is one of our S3 URLs or a native
        # URI — including an EXPIRED signed link), read it via cloud
        # credentials instead of a blind HTTP GET. A raw fetch of an expired
        # signed URL returns an error body, and a fetch of an internal share
        # page returns HTML — either way we'd write garbage and call it a PDF.
        # Genuinely-external URLs (is_storage_url == False) still take the
        # size-capped httpx stream below. Callers that hold one of our
        # share-link shapes should resolve a MediaRef at the boundary first.
        from matrx_files.backends import is_storage_url

        if self._cloud is not None and is_storage_url(url):
            try:
                content = await self.cloud_read_url_async(url)
                if content:
                    temp_filename = f"{uuid.uuid4()}.{extension}"
                    written = self.write_to_base(
                        root="temp", path=temp_filename, content=content,
                        clean=False, remove_html=False,
                    )
                    if written:
                        return str(self._get_full_path("temp", temp_filename))
            except Exception as exc:
                print(f"[PDFHandler] Cloud credential fetch failed: {exc}")
                return None

        from matrx_utils.outbound_guard import public_only_client

        try:
            # Genuinely external: no address inside our network, every hop.
            async with public_only_client(timeout=30, follow_redirects=True) as client:
                async with client.stream("GET", url) as response:
                    response.raise_for_status()
                    declared = response.headers.get("content-length")
                    if declared and declared.isdigit() and int(declared) > self.MAX_REMOTE_DOWNLOAD_BYTES:
                        print(
                            f"[PDFHandler] URL download refused: declared size "
                            f"{declared}B exceeds {self.MAX_REMOTE_DOWNLOAD_BYTES}B cap"
                        )
                        return None
                    chunks: list[bytes] = []
                    total = 0
                    async for chunk in response.aiter_bytes():
                        total += len(chunk)
                        if total > self.MAX_REMOTE_DOWNLOAD_BYTES:
                            print(
                                f"[PDFHandler] URL download aborted: body exceeded "
                                f"{self.MAX_REMOTE_DOWNLOAD_BYTES}B cap"
                            )
                            return None
                        chunks.append(chunk)
            temp_filename = f"{uuid.uuid4()}.{extension}"
            written = self.write_to_base(
                root="temp", path=temp_filename, content=b"".join(chunks)
            )
            if written:
                return str(self._get_full_path("temp", temp_filename))
        except Exception as exc:
            print(f"[PDFHandler] URL download failed: {exc}")
        return None

    async def _fetch_file_object(self, file_object: dict) -> str | None:
        url = file_object.get("url", "")
        details = file_object.get("details", {})
        extension = str(details.get("extension", "pdf"))
        # First attempt: when the URL is one of our S3
        # HTTPS or native URI, including an EXPIRED signed link), read via
        # cloud credentials. This MUST come before any raw HTTP GET — fetching
        # an expired signed URL or an internal share page returns an error body
        # / HTML that we'd otherwise write out and mislabel as a PDF.
        # ``cloud_read_url`` handles signed, expired, public, and native forms.
        from matrx_files.backends import is_storage_url

        if url and self._cloud is not None and is_storage_url(url):
            try:
                content = self.cloud_read_url(url)
                if content:
                    temp_filename = f"{uuid.uuid4()}.{extension}"
                    written = self.write_to_base(
                        root="temp",
                        path=temp_filename,
                        content=content,
                        clean=False,
                        remove_html=False,
                    )
                    if written:
                        return str(self._get_full_path("temp", temp_filename))
            except Exception as exc:
                print(f"[PDFHandler] Cloud credential fetch failed: {exc}")

        # Second attempt: genuinely-external URL — a plain HTTP download (skip
        # when url is empty to avoid httpx.UnsupportedProtocol churn).
        elif url:
            from matrx_utils.outbound_guard import public_only_client

            try:
                async with public_only_client(timeout=30) as client:
                    http_response = await client.get(url)
                    http_response.raise_for_status()
                    temp_filename = f"{uuid.uuid4()}.{extension}"
                    written = self.write_to_base(
                        root="temp", path=temp_filename, content=http_response.content
                    )
                    if written:
                        return str(self._get_full_path("temp", temp_filename))
            except Exception as exc:
                print(f"[PDFHandler] file-object download failed: {exc}")

        return None

    # ------------------------------------------------------------------
    # Text extraction
    # ------------------------------------------------------------------

    def extract_text_from_image_bytes(self, image_bytes: bytes) -> str:
        return extract_text_from_image_bytes(image_bytes)

    async def extract_text_from_bytes(
        self,
        pdf_bytes: bytes,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        emitter: Any | None = None,
        include_page_markers: bool = False,
    ) -> str:
        with pdf_temp_file(pdf_bytes) as tmp_path:
            return await self.extract_text(
                str(tmp_path),
                force_ocr=force_ocr,
                use_ocr_threshold=use_ocr_threshold,
                emitter=emitter,
                include_page_markers=include_page_markers,
            )

    def extract_text_from_bytes_sync(
        self,
        pdf_bytes: bytes,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
    ) -> str:
        return extract_text_from_bytes_sync(
            pdf_bytes,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
        )

    def extract_text_pages(
        self,
        path: str,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        include_blocks: bool = False,
        include_words: bool = False,
    ) -> list[PdfPageText]:
        return extract_text_pages(
            path,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )

    async def extract_text_pages_async(
        self,
        path: str,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        include_blocks: bool = False,
        include_words: bool = False,
    ) -> list[PdfPageText]:
        return await extract_text_pages_async(
            path,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )

    def extract_text_pages_stream(
        self,
        path: str,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        include_blocks: bool = False,
        include_words: bool = False,
        page_start: int | None = None,
        page_end: int | None = None,
    ) -> AsyncIterator[PdfExtractStart | PdfPageText]:
        """Async iterator of PdfExtractStart (page count) then each PdfPageText
        as its page is extracted — the real-time variant of
        ``extract_text_pages_async``. ``page_start``/``page_end`` (1-based,
        inclusive) limit extraction to that slice."""
        return extract_text_pages_stream(
            path,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
            page_start=page_start,
            page_end=page_end,
        )

    def extract_text_pages_from_bytes(
        self,
        pdf_bytes: bytes,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        include_blocks: bool = False,
        include_words: bool = False,
    ) -> list[PdfPageText]:
        return extract_text_pages_from_bytes(
            pdf_bytes,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )

    async def extract_text_pages_from_bytes_async(
        self,
        pdf_bytes: bytes,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        include_blocks: bool = False,
        include_words: bool = False,
    ) -> list[PdfPageText]:
        return await extract_text_pages_from_bytes_async(
            pdf_bytes,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )

    def format_page_text(
        self,
        pages: list[PdfPageText],
        include_page_markers: bool = False,
        document_label: str | None = None,
    ) -> str:
        return format_page_text(
            pages,
            include_page_markers=include_page_markers,
            document_label=document_label,
        )

    async def extract_text(
        self,
        path: str,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        emitter: Any | None = None,
        include_page_markers: bool = False,
        include_blocks: bool = False,
        include_words: bool = False,
    ) -> str:
        """Extract text from a PDF at *path*.

        Delegates to ``extract_text_pages_async`` so the executor-routing
        policy lives in exactly one place.
        """
        pages = await extract_text_pages_async(
            path,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            include_blocks=include_blocks,
            include_words=include_words,
        )
        page_count = len(pages)
        batch_size = 10

        for page_num in range(page_count):
            if emitter and (
                page_num % batch_size == batch_size - 1
                or page_num == page_count - 1
            ):
                await emitter.send_info(
                    build_info_payload(
                        code="pdf_page_progress",
                        system_message=f"pdf_extract page {page_num + 1}/{page_count}",
                        user_message=f"Processed page {page_num + 1} of {page_count}",
                    )
                )

        return format_page_text(
            pages,
            include_page_markers=include_page_markers,
            document_label=path,
        )

    async def extract_text_with_page_markers(
        self,
        path: str,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        emitter: Any | None = None,
    ) -> str:
        return await self.extract_text(
            path,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            emitter=emitter,
            include_page_markers=True,
        )

    async def extract_text_from_bytes_with_page_markers(
        self,
        pdf_bytes: bytes,
        force_ocr: bool = False,
        use_ocr_threshold: int = 100,
        emitter: Any | None = None,
    ) -> str:
        return await self.extract_text_from_bytes(
            pdf_bytes,
            force_ocr=force_ocr,
            use_ocr_threshold=use_ocr_threshold,
            emitter=emitter,
            include_page_markers=True,
        )

    # ------------------------------------------------------------------
    # Table extraction
    # ------------------------------------------------------------------

    def extract_tables(
        self,
        path: str,
        output_format: str = "csv",
        report: PdfTablesReport | None = None,
    ) -> str | None:
        return extract_tables(
            path, output_format=output_format, out_dir=self.temp_dir, report=report
        )

    async def extract_tables_async(
        self,
        path: str,
        output_format: str = "csv",
        report: PdfTablesReport | None = None,
    ) -> str | None:
        return await extract_tables_async(
            path, output_format=output_format, out_dir=self.temp_dir, report=report
        )

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 2000,
        overlap_size: int = 200,
    ) -> list[str]:
        return chunk_text(text, chunk_size=chunk_size, overlap_size=overlap_size)

    def chunk_page_text(
        self,
        pages: list[PdfPageText],
        chunk_size: int = 2000,
        overlap_size: int = 200,
        include_page_markers: bool = False,
        document_label: str | None = None,
        document_id: str | None = None,
    ) -> PdfChunkedTextResult:
        return chunk_page_text(
            pages,
            chunk_size=chunk_size,
            overlap_size=overlap_size,
            include_page_markers=include_page_markers,
            document_label=document_label,
            document_id=document_id,
        )

    # ------------------------------------------------------------------
    # AI chunk processing
    # ------------------------------------------------------------------

    async def process_chunks_with_ai(
        self,
        chunks: list[str],
        ai_processor: AiChunkProcessor,
        emitter: Any | None = None,
        max_concurrent: int | None = None,
    ) -> list[dict[str, Any]]:
        return await process_chunks_with_ai(
            chunks,
            ai_processor=ai_processor,
            emitter=emitter,
            max_concurrent=max_concurrent,
        )

    # ------------------------------------------------------------------
    # PDF write
    # ------------------------------------------------------------------

    def write_pdf(self, root: str, path: str, data: Any) -> bool:
        """Write PDF content to *path*.

        Accepts a ``pdfium.PdfDocument`` (saved via pypdfium2), raw ``bytes``,
        or ``str`` (UTF-8 encoded). Returns True on success.
        """
        full_path = self._get_full_path(root, path)
        self._ensure_directory(full_path)

        try:
            if isinstance(data, pdfium.PdfDocument):
                data.save(str(full_path))
                data.close()
                return True
            if isinstance(data, bytes):
                full_path.write_bytes(data)
                return True
            if isinstance(data, str):
                full_path.write_bytes(data.encode("utf-8"))
                return True
        except Exception as exc:
            print(f"[PDFHandler] write_pdf failed: {exc}")

        return False

    def write_pdf_file(self, path: str, content: Any) -> bool:
        p = Path(path)
        self._ensure_directory(p)
        try:
            if isinstance(content, pdfium.PdfDocument):
                content.save(str(p))
                content.close()
                return True
            if isinstance(content, bytes):
                p.write_bytes(content)
                return True
            if isinstance(content, str):
                p.write_bytes(content.encode("utf-8"))
                return True
        except Exception as exc:
            print(f"[PDFHandler] write_pdf_file failed: {exc}")
        return False

    # ------------------------------------------------------------------
    # Full pipeline
    # ------------------------------------------------------------------

    async def full_pipeline(
        self,
        source: str | dict,
        options: PdfPipelineOptions | None = None,
        emitter: Any | None = None,
        ai_processor: AiChunkProcessor | None = None,
    ) -> PdfResult:
        """Run the full PDF processing pipeline.

        *source* can be a URL, file dict (with "url"/"details" keys), or local
        file path. Each stage is independently opt-in via *options*.

        Set ``options.upload_result_to`` to a full cloud URI prefix to store
        the extracted text after processing, e.g. ``"s3://bucket/pdf/"``.

        When ``options.chunk_and_process_with_ai`` is True, *ai_processor*
        **must** be provided.
        """
        opts = options or PdfPipelineOptions()
        result = PdfResult()

        if opts.chunk_and_process_with_ai and ai_processor is None:
            raise ValueError(
                "[PDFHandler] options.chunk_and_process_with_ai is True but no "
                "ai_processor was provided. Pass an async callable that accepts "
                "a chunk string and returns a dict."
            )

        # 1. Resolve source to a local path
        local_path = await self.fetch_remote(source)
        if not local_path:
            raise ValueError(
                f"[PDFHandler] Could not resolve source to a local file: {source}"
            )

        # Clean up downloaded temp files when we owned the fetch. If the
        # caller passed an already-local path through, leave it alone.
        source_was_remote = isinstance(source, dict) or (
            isinstance(source, str) and source.startswith(("http://", "https://"))
        )
        cleanup_path = local_path if source_was_remote else None

        try:
            result = await self._run_pipeline_stages(
                local_path=local_path,
                options=opts,
                emitter=emitter,
                ai_processor=ai_processor,
                result=result,
            )
        finally:
            if cleanup_path:
                try:
                    Path(cleanup_path).unlink(missing_ok=True)
                except OSError as exc:
                    print(f"[PDFHandler] temp cleanup failed for {cleanup_path}: {exc}")
        return result

    async def _run_pipeline_stages(
        self,
        *,
        local_path: str,
        options: PdfPipelineOptions,
        emitter: Any | None,
        ai_processor: AiChunkProcessor | None,
        result: PdfResult,
    ) -> PdfResult:
        opts = options
        pages_for_chunking: list[PdfPageText] | None = None
        if opts.extract_text:
            wants_page_payload = (
                opts.include_page_metadata
                or opts.include_block_metadata
                or opts.include_word_metadata
                or opts.include_chunk_metadata
            )
            if wants_page_payload or opts.include_page_markers:
                pages = await self.extract_text_pages_async(
                    local_path,
                    force_ocr=opts.force_ocr,
                    use_ocr_threshold=opts.use_ocr_threshold,
                    include_blocks=opts.include_block_metadata,
                    include_words=opts.include_word_metadata,
                )
                result.raw_text = format_page_text(
                    pages,
                    include_page_markers=opts.include_page_markers,
                    document_label=local_path,
                )
                pages_for_chunking = pages
                if wants_page_payload:
                    result.pages = pages
            else:
                result.raw_text = await self.extract_text(
                    local_path,
                    force_ocr=opts.force_ocr,
                    use_ocr_threshold=opts.use_ocr_threshold,
                    emitter=emitter,
                )

        # 3. Table extraction
        if opts.extract_tables:
            result.tables_path = await self.extract_tables_async(local_path)

        # 4. Chunk + AI
        if opts.chunk_and_process_with_ai and result.raw_text and ai_processor:
            if pages_for_chunking is not None:
                chunked = self.chunk_page_text(
                    pages_for_chunking,
                    chunk_size=opts.chunk_size,
                    overlap_size=opts.overlap_size,
                    include_page_markers=opts.include_page_markers,
                    document_label=local_path,
                    document_id=result.file_id or result.storage_uri,
                )
                chunks = [chunk.text for chunk in chunked.chunks]
                if opts.include_chunk_metadata:
                    result.chunk_records = chunked.chunks
            else:
                chunks = self.chunk_text(
                    result.raw_text,
                    chunk_size=opts.chunk_size,
                    overlap_size=opts.overlap_size,
                )
            result.chunks = chunks
            result.ai_processed = await self.process_chunks_with_ai(
                chunks,
                ai_processor=ai_processor,
                emitter=emitter,
            )

        # 5. Upload result to cloud storage
        upload_prefix = opts.upload_result_to
        if upload_prefix and result.raw_text:
            try:
                dest_prefix = upload_prefix.rstrip("/")
                dest_uri = f"{dest_prefix}/{uuid.uuid4()}.txt"
                self.cloud_write(dest_uri, result.raw_text.encode("utf-8"))
                result.cloud_uri = dest_uri
                result.storage_uri = dest_uri
            except Exception as exc:
                print(f"[PDFHandler] Cloud upload failed: {exc}")

        return result


__all__ = ["PDFHandler"]
