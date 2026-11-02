"""PDF Studio preset catalog — backs ``GET /utilities/pdf/studio/presets``.

Mirrors the shape of ``image_studio_presets.py``: stable string ids, grouped
into categories, with default operation + params + tags. The FE consumes the
returned JSON and decorates with icons / accent colors by category id.

If a preset is added / removed / changed here, keep the FE catalog in sync —
ids must stay stable across both sides.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field


OperationId = Literal[
    "render_page",
    "render_all",
    "render_thumbnail",
    "extract_pages",
    "crop_pages",
    "rotate_pages",
    "delete_pages",
    "reorder_pages",
    "insert_pages",
    "duplicate_pages",
    "merge",
    "split",
    "compress",
    "extract_text",
    "extract_tables",
    "full_pipeline",
]

OutputKind = Literal["pdf", "image", "text", "csv", "json", "archive"]


# Internal TypedDicts (dict-literal authoring). Keep these for the in-process
# catalog so adding a preset stays a one-liner.
class PdfStudioPreset(TypedDict, total=False):
    id: str
    name: str
    usage: str
    operation: OperationId
    params: dict[str, object]
    output_kind: OutputKind
    spec: str
    tags: list[str]


class PdfStudioCategory(TypedDict):
    id: str
    name: str
    description: str
    accent: str
    presets: list[PdfStudioPreset]


class PdfStudioBundle(TypedDict):
    id: str
    name: str
    description: str
    preset_ids: list[str]


# Pydantic mirrors — these are the wire types FastAPI emits to OpenAPI.
class PdfStudioPresetSchema(BaseModel):
    id: str
    name: str
    usage: str
    operation: OperationId
    params: dict[str, Any] = Field(default_factory=dict)
    output_kind: OutputKind
    spec: str | None = None
    tags: list[str] = Field(default_factory=list)


class PdfStudioCategorySchema(BaseModel):
    id: str
    name: str
    description: str
    accent: str
    presets: list[PdfStudioPresetSchema]


class PdfStudioBundleSchema(BaseModel):
    id: str
    name: str
    description: str
    preset_ids: list[str]


class PdfStudioCatalog(BaseModel):
    """Wire shape for ``GET /utilities/pdf/studio/presets``."""

    categories: list[PdfStudioCategorySchema]
    bundles: list[PdfStudioBundleSchema]


# ── Render presets (page → image) ────────────────────────────────────────
_RENDER: list[PdfStudioPreset] = [
    {
        "id": "render-page-72",
        "name": "Page → PNG @ 72 DPI",
        "usage": "Quick screen-resolution page render.",
        "operation": "render_page",
        "params": {"dpi": 72, "fmt": "png"},
        "output_kind": "image",
        "tags": ["render", "screen"],
    },
    {
        "id": "render-page-150",
        "name": "Page → PNG @ 150 DPI",
        "usage": "Default crisp-on-retina page render.",
        "operation": "render_page",
        "params": {"dpi": 150, "fmt": "png"},
        "output_kind": "image",
        "tags": ["render", "default"],
    },
    {
        "id": "render-page-300",
        "name": "Page → PNG @ 300 DPI",
        "usage": "Print-quality page render.",
        "operation": "render_page",
        "params": {"dpi": 300, "fmt": "png"},
        "output_kind": "image",
        "tags": ["render", "print"],
    },
    {
        "id": "render-page-jpeg",
        "name": "Page → JPEG @ 150 DPI",
        "usage": "Compact lossy render, good for previews.",
        "operation": "render_page",
        "params": {"dpi": 150, "fmt": "jpeg", "jpeg_quality": 85},
        "output_kind": "image",
        "tags": ["render", "preview"],
    },
    {
        "id": "render-page-webp",
        "name": "Page → WebP @ 150 DPI",
        "usage": "Modern lossy render — ~30% smaller than JPEG.",
        "operation": "render_page",
        "params": {"dpi": 150, "fmt": "webp", "jpeg_quality": 85},
        "output_kind": "image",
        "tags": ["render", "modern"],
    },
    {
        "id": "render-all-150",
        "name": "All pages → PNG @ 150 DPI",
        "usage": "One image per page bundled into an archive.",
        "operation": "render_all",
        "params": {"dpi": 150, "fmt": "png"},
        "output_kind": "archive",
        "tags": ["render", "bulk"],
    },
    {
        "id": "render-thumbnail",
        "name": "Cover thumbnail (256 px)",
        "usage": "Grid-view thumbnail for cld_files.",
        "operation": "render_thumbnail",
        "params": {"max_side": 256, "fmt": "jpeg", "jpeg_quality": 80},
        "output_kind": "image",
        "tags": ["render", "thumbnail"],
    },
]

# ── Page operations ──────────────────────────────────────────────────────
_PAGES: list[PdfStudioPreset] = [
    {
        "id": "extract-first-page",
        "name": "Extract first page",
        "usage": "Pull page 1 into its own PDF (handy for cover sheets).",
        "operation": "extract_pages",
        "params": {"pages": [1]},
        "output_kind": "pdf",
        "tags": ["pages", "extract"],
    },
    {
        "id": "extract-last-page",
        "name": "Extract last page",
        "usage": "Pull the final page into its own PDF.",
        "operation": "extract_pages",
        "params": {"pages_relative_to_end": [1]},
        "output_kind": "pdf",
        "tags": ["pages", "extract"],
    },
    {
        "id": "rotate-90-cw",
        "name": "Rotate 90° clockwise (all pages)",
        "usage": "Fix landscape scans saved as portrait.",
        "operation": "rotate_pages",
        "params": {"rotation": 90},
        "output_kind": "pdf",
        "tags": ["pages", "rotate"],
    },
    {
        "id": "rotate-180",
        "name": "Flip 180° (all pages)",
        "usage": "Correct upside-down scans.",
        "operation": "rotate_pages",
        "params": {"rotation": 180},
        "output_kind": "pdf",
        "tags": ["pages", "rotate"],
    },
    {
        "id": "split-per-page",
        "name": "Split into one-page files",
        "usage": "Burst a PDF into per-page PDFs (ZIP archive).",
        "operation": "split",
        "params": {},
        "output_kind": "archive",
        "tags": ["pages", "split"],
    },
    {
        "id": "split-every-10",
        "name": "Split every 10 pages",
        "usage": "Cut a large document into 10-page chunks.",
        "operation": "split",
        "params": {"max_pages_per_part": 10},
        "output_kind": "archive",
        "tags": ["pages", "split"],
    },
]

# ── Compression ──────────────────────────────────────────────────────────
_COMPRESS: list[PdfStudioPreset] = [
    {
        "id": "compress-lossless",
        "name": "Compress (lossless)",
        "usage": "Garbage-collect + deflate, no quality loss.",
        "operation": "compress",
        "params": {"level": 1},
        "output_kind": "pdf",
        "tags": ["compress", "lossless"],
    },
    {
        "id": "compress-balanced",
        "name": "Compress (balanced)",
        "usage": "Re-encode images at q=80 + ~50% resize. Good general default.",
        "operation": "compress",
        "params": {"level": 2},
        "output_kind": "pdf",
        "tags": ["compress", "balanced"],
    },
    {
        "id": "compress-aggressive",
        "name": "Compress (aggressive)",
        "usage": "Strong image recompression + metadata strip. Smallest output.",
        "operation": "compress",
        "params": {"level": 3},
        "output_kind": "pdf",
        "tags": ["compress", "small"],
    },
]

# ── Extract ──────────────────────────────────────────────────────────────
_EXTRACT: list[PdfStudioPreset] = [
    {
        "id": "extract-text",
        "name": "Extract text",
        "usage": "Plain text only — strips structure.",
        "operation": "extract_text",
        "params": {},
        "output_kind": "text",
        "tags": ["extract", "text"],
    },
    {
        "id": "extract-text-page-aware",
        "name": "Extract text (page-aware)",
        "usage": "Per-page text + bbox metadata for RAG ingestion.",
        "operation": "extract_text",
        "params": {
            "include_page_metadata": True,
            "include_block_metadata": True,
        },
        "output_kind": "json",
        "tags": ["extract", "rag"],
    },
    {
        "id": "extract-tables-csv",
        "name": "Extract tables → CSV",
        "usage": "Pull tabular data from every page (requires Java + tabula-py).",
        "operation": "extract_tables",
        "params": {"output_format": "csv"},
        "output_kind": "csv",
        "tags": ["extract", "tables"],
    },
]


PRESET_CATEGORIES: list[PdfStudioCategory] = [
    {
        "id": "render",
        "name": "Render",
        "description": "Turn any page into an image — screen, retina, print, or thumbnail.",
        "accent": "cyan",
        "presets": _RENDER,
    },
    {
        "id": "pages",
        "name": "Pages",
        "description": "Extract, split, rotate, reorder — the daily-driver page operations.",
        "accent": "blue",
        "presets": _PAGES,
    },
    {
        "id": "compress",
        "name": "Compress",
        "description": "Shrink files without re-uploading. Three quality tiers.",
        "accent": "emerald",
        "presets": _COMPRESS,
    },
    {
        "id": "extract",
        "name": "Extract",
        "description": "Pull text and tables out for downstream RAG, search, or analysis.",
        "accent": "amber",
        "presets": _EXTRACT,
    },
]


ALL_PDF_PRESETS: list[PdfStudioPreset] = [
    p for category in PRESET_CATEGORIES for p in category["presets"]
]

PDF_PRESETS_BY_ID: dict[str, PdfStudioPreset] = {p["id"]: p for p in ALL_PDF_PRESETS}


RECOMMENDED_PDF_BUNDLES: list[PdfStudioBundle] = [
    {
        "id": "legal-intake",
        "name": "Legal intake",
        "description": "Extract first page + page-aware text + thumbnail — ready for case ingestion.",
        "preset_ids": ["extract-first-page", "extract-text-page-aware", "render-thumbnail"],
    },
    {
        "id": "preview-pack",
        "name": "Preview pack",
        "description": "Thumbnail + page-1 JPEG + first 3 pages text — for quick FE preview UIs.",
        "preset_ids": ["render-thumbnail", "render-page-jpeg", "extract-text"],
    },
    {
        "id": "shrink-and-keep",
        "name": "Shrink & keep",
        "description": "Compress balanced + page-aware text for RAG; keeps a small archival copy.",
        "preset_ids": ["compress-balanced", "extract-text-page-aware"],
    },
]


def get_pdf_preset_by_id(preset_id: str) -> PdfStudioPreset | None:
    return PDF_PRESETS_BY_ID.get(preset_id)


__all__ = [
    "OperationId",
    "OutputKind",
    "PdfStudioPreset",
    "PdfStudioCategory",
    "PdfStudioBundle",
    "PdfStudioPresetSchema",
    "PdfStudioCategorySchema",
    "PdfStudioBundleSchema",
    "PdfStudioCatalog",
    "PRESET_CATEGORIES",
    "ALL_PDF_PRESETS",
    "PDF_PRESETS_BY_ID",
    "RECOMMENDED_PDF_BUNDLES",
    "get_pdf_preset_by_id",
]
