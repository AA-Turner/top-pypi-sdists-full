"""Neutral data shapes for the Office (OpenXML) codec.

Two directions, one vocabulary:

  IN  (extract)  — bytes -> ``OfficeExtraction`` : a converged, AI-facing
                   representation (full ``markdown`` + per-``portion`` markdown,
                   where a portion is a slide / sheet / logical section). The
                   host persists these portions as ``processed_document_pages``
                   exactly like PDF pages, so everything downstream (clean ->
                   chunk -> embed -> ner) is identical for Office and PDF.

  OUT (generate) — a structured spec (``DocumentSpec`` / ``PresentationSpec`` /
                   ``SpreadsheetSpec``) -> bytes. These specs ARE "what we want a
                   Word doc / deck / sheet to be": the minimal, AI-authorable
                   structure the platform generates from. An agent produces one
                   of these (structured output), the codec renders real bytes.

Nothing here imports a host module or the ORM — this is a pure format codec.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

# --- MIME constants (the canonical strings; every routing table imports these) ---

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
DOC_MIME = "application/msword"
PPT_MIME = "application/vnd.ms-powerpoint"
XLS_MIME = "application/vnd.ms-excel"


class OfficeKind(str, Enum):
    """The document family a set of Office bytes belongs to."""

    docx = "docx"
    pptx = "pptx"
    xlsx = "xlsx"
    # Legacy binary (OLE/CFB) formats. The pure-python codec cannot read these;
    # they require a LibreOffice conversion step (standalone-only). Classified
    # so callers can route/deny explicitly instead of silently mis-parsing.
    doc = "doc"
    ppt = "ppt"
    xls = "xls"

    @property
    def is_legacy_binary(self) -> bool:
        return self in (OfficeKind.doc, OfficeKind.ppt, OfficeKind.xls)


# --------------------------------------------------------------------------- #
# IN — extraction result
# --------------------------------------------------------------------------- #


class OfficePortion(BaseModel):
    """One converged unit of an Office document — the Office analogue of a PDF
    page. A pptx slide, an xlsx sheet, or a docx logical section is one portion.
    ``markdown`` is the AI-facing body; ``text`` is the plain-text fallback."""

    index: int  # 0-based
    number: int  # 1-based (page_number equivalent)
    kind: Literal["page", "slide", "sheet", "section"]
    title: str | None = None
    markdown: str = ""
    text: str = ""
    # Free-form per-portion facts (slide notes present, sheet dims, truncation…).
    meta: dict[str, str | int | bool] = Field(default_factory=dict)

    @property
    def char_count(self) -> int:
        return len(self.text or self.markdown or "")


class OfficeExtraction(BaseModel):
    """The full result of reading Office bytes."""

    office_kind: OfficeKind
    mime_type: str
    markdown: str = ""  # whole-document markdown (portions joined)
    portions: list[OfficePortion] = Field(default_factory=list)
    metadata: dict[str, str | int | bool] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    @property
    def raw_chars(self) -> int:
        return sum(p.char_count for p in self.portions)


# --------------------------------------------------------------------------- #
# OUT — generation specs ("what we want a Word doc / deck / sheet to be")
# --------------------------------------------------------------------------- #


class DocBlock(BaseModel):
    """One block of a generated Word document."""

    type: Literal["heading", "paragraph", "bullet", "numbered", "table", "page_break", "quote"] = (
        Field(
            description=(
                "Block kind: 'heading'/'paragraph'/'bullet'/'numbered'/'quote' render "
                "`text`; 'table' renders `rows`; 'page_break' starts a new page and "
                "uses no other field."
            )
        )
    )
    text: str = Field(
        default="",
        description=(
            "Body text for heading/paragraph/quote blocks, or ONE list line for a "
            "bullet/numbered block (one block per line). Ignored by table/page_break."
        ),
    )
    level: int = Field(
        default=1,
        description="Heading depth 1-6 for 'heading' blocks (1 = chapter title). Ignored elsewhere.",
    )
    rows: list[list[str]] = Field(
        default_factory=list,
        description=(
            "Table cells for 'table' blocks, outer list = rows, inner list = one "
            "row's cell strings. The first row is styled as the header when "
            "`header` is true."
        ),
    )
    header: bool = Field(
        default=True,
        description="For 'table' blocks: treat the first row of `rows` as a styled header row.",
    )


class DocumentSpec(BaseModel):
    """Canonical AI-authorable shape for a Word document (.docx)."""

    title: str | None = Field(
        default=None,
        description="Document title rendered as the top-level heading. Omit for an untitled document.",
    )
    blocks: list[DocBlock] = Field(
        default_factory=list,
        description="Ordered content blocks (headings, paragraphs, lists, tables, quotes, page breaks) rendered top to bottom.",
    )


class SlideSpec(BaseModel):
    """One slide of a generated presentation."""

    title: str | None = Field(
        default=None, description="Slide title shown in the slide's title placeholder."
    )
    # Bullets support simple indentation via leading "- " nesting is out of scope;
    # a bullet string is one line. `body` is used when there are no bullets.
    bullets: list[str] = Field(
        default_factory=list,
        description=(
            "Bullet lines for the slide body, one string per bullet (no nesting). "
            "When set, `body` is not used."
        ),
    )
    body: str = Field(
        default="",
        description="Free-text slide body used when `bullets` is empty.",
    )
    notes: str = Field(
        default="",
        description="Speaker notes attached to the slide (visible in presenter view only).",
    )
    layout: Literal["title", "title_content", "section", "blank"] = Field(
        default="title_content",
        description=(
            "Slide layout: 'title' (title slide), 'title_content' (title + body/"
            "bullets), 'section' (section divider), or 'blank'."
        ),
    )


class PresentationSpec(BaseModel):
    """Canonical AI-authorable shape for a PowerPoint deck (.pptx)."""

    title: str | None = Field(
        default=None,
        description="Deck title rendered on the opening title slide.",
    )
    subtitle: str | None = Field(
        default=None,
        description="Subtitle rendered under the title on the opening slide.",
    )
    slides: list[SlideSpec] = Field(
        default_factory=list,
        description="Ordered slides after the title slide, rendered in list order.",
    )


class SheetSpec(BaseModel):
    """One sheet of a generated workbook."""

    name: str = Field(
        default="Sheet1",
        description="Worksheet tab name shown at the bottom of the workbook.",
    )
    columns: list[str] = Field(
        default_factory=list,
        description="Column header labels written as the sheet's first row.",
    )
    rows: list[list[str | int | float | bool | None]] = Field(
        default_factory=list,
        description=(
            "Data rows below the header, outer list = rows, inner list = one row's "
            "cell values in column order (strings, numbers, booleans, or null for blank)."
        ),
    )
    freeze_header: bool = Field(
        default=True,
        description="Freeze the header row so it stays visible while scrolling.",
    )


class SpreadsheetSpec(BaseModel):
    """Canonical AI-authorable shape for an Excel workbook (.xlsx)."""

    sheets: list[SheetSpec] = Field(
        default_factory=list,
        description="Worksheets of the workbook, one tab per entry, in tab order.",
    )


class OfficeGenerationResult(BaseModel):
    """Bytes + how to store them (the codec never touches storage itself)."""

    office_kind: OfficeKind
    mime_type: str
    extension: str  # ".docx" / ".pptx" / ".xlsx"
    # base64 so the model can round-trip through JSON tool results / persistence
    # without a bytes field. The host decodes before writing to /assets.
    base64_data: str
    byte_size: int


__all__ = [
    "DOCX_MIME",
    "PPTX_MIME",
    "XLSX_MIME",
    "DOC_MIME",
    "PPT_MIME",
    "XLS_MIME",
    "OfficeKind",
    "OfficePortion",
    "OfficeExtraction",
    "DocBlock",
    "DocumentSpec",
    "SlideSpec",
    "PresentationSpec",
    "SheetSpec",
    "SpreadsheetSpec",
    "OfficeGenerationResult",
]
