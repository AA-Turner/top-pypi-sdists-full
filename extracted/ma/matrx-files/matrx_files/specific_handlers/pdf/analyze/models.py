"""Phase 3 layout-analysis Pydantic models.

These types are the wire contract between the analyze primitives and any
consumer (RAG pipeline, redaction targets, studio presets, FE UIs).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


RegionKind = Literal[
    "header",
    "footer",
    "watermark",
    "side-margin",
    "logo",
    "page-number",
    "running-title",
    "unknown",
]


PageClass = Literal[
    "blank",
    "cover",
    "toc",
    "body",
    "exhibit",
    "billing",
    "signature",
    "appendix",
    "footer-only",
    "image-only",
    "unknown",
]


class RepeatedRegionBbox(BaseModel):
    """One occurrence of a repeated region on a single page."""

    page_number: int = Field(ge=1)
    x0: float
    y0: float
    x1: float
    y1: float
    raw_text: str


class RepeatedRegion(BaseModel):
    """A pattern detected across multiple pages.

    Stable across detector runs given the same input — the *region_id* is
    deterministic from the (kind, y_band, x_band, normalized_text_template)
    quadruple so consumers can reference a region by id when applying
    accept/reject decisions.
    """

    region_id: str
    kind: RegionKind
    text_template: str
    """Normalized template with page-number / date substitutions tokenised
    as ``{page}`` / ``{date}``. Useful for FE display and for showing the
    user "this is the pattern we detected" alongside the bboxes."""
    pages: list[int]
    """1-based page numbers where this region occurs."""
    bbox_per_page: list[RepeatedRegionBbox]
    confidence: float = Field(ge=0.0, le=1.0)
    """[0, 1] score combining frequency (across pages), geometric stability,
    and text similarity. >= 0.8 is high confidence; < 0.5 is suggest-only."""


class RepeatedRegionsReport(BaseModel):
    page_count: int
    regions: list[RepeatedRegion]
    detector_version: str = "v1"


class PageClassification(BaseModel):
    page_number: int = Field(ge=1)
    page_class: PageClass
    confidence: float = Field(ge=0.0, le=1.0)
    indicators: list[str] = Field(default_factory=list)
    """Free-text reasons the classifier picked this label — useful for
    debugging false positives and surfacing rationale to the FE."""


class LayoutClassificationReport(BaseModel):
    page_count: int
    pages: list[PageClassification]
    classifier_version: str = "v1"


class ReadingOrderBlock(BaseModel):
    block_index: int
    column_index: int = Field(ge=0)
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


class ReadingOrderPage(BaseModel):
    page_number: int = Field(ge=1)
    column_count: int = Field(ge=1)
    blocks_in_order: list[ReadingOrderBlock]


class ReadingOrderReport(BaseModel):
    page_count: int
    pages: list[ReadingOrderPage]


__all__ = [
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
]
