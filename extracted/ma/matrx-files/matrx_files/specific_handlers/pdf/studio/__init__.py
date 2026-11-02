"""PDF Studio preset catalog + render-spec dispatcher (Phase 2)."""

from .presets import (
    ALL_PDF_PRESETS,
    PDF_PRESETS_BY_ID,
    PRESET_CATEGORIES,
    PdfStudioBundle,
    PdfStudioCategory,
    PdfStudioPreset,
    RECOMMENDED_PDF_BUNDLES,
    get_pdf_preset_by_id,
)
from .render_spec import (
    PdfRenderSpec,
    PdfStudioRenderResult,
    render_studio_variant,
    render_studio_variant_async,
)


__all__ = [
    "PdfStudioPreset",
    "PdfStudioCategory",
    "PdfStudioBundle",
    "PRESET_CATEGORIES",
    "ALL_PDF_PRESETS",
    "PDF_PRESETS_BY_ID",
    "RECOMMENDED_PDF_BUNDLES",
    "get_pdf_preset_by_id",
    "PdfRenderSpec",
    "PdfStudioRenderResult",
    "render_studio_variant",
    "render_studio_variant_async",
]
