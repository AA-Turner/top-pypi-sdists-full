"""Press-clip render kind — what ``cloud_browser.render_clip`` produced.

ONE kind shared by the ``cloud_browser.render_clip`` workflow node and the
``cloud_browser`` tool's ``render_clip`` action (the media_forensics / fact_check
precedent), so node, tool and registry row cannot drift apart. It lives in the
package because the tool implementation's arg model and this shape must be
importable without aidream (``scripts/check_package_boundaries.py``).

Every file is a ``file_id`` in the organization's file store — never a URL (a
signed URL is a handoff, never an identity). ``headline``, ``byline`` and
``published_at`` are READ from the page and null when absent; nothing here is
ever filled in. ``logo_source == "text_wordmark"`` means no real logo was found
and the clip is not shippable.

Publish with::

    uv run python scripts/publish_kind_catalog.py matrx_ai.tools.kinds.press_clip --apply
"""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import Field

PressClipLogoSource = Literal[
    "explicit", "article_masthead", "home_masthead", "og_logo_or_favicon", "text_wordmark"
]


@kind(
    "press_clip_render",
    disposition="record",
    label="Press Clip Render",
    family="press",
    # A REAL measured render: Waste Dive, 2026-09-27, client "Recycle Coach",
    # section scope requested (no heading starts with the name, so it fell back).
    example={
        "__kind": "press_clip_render",
        "pdf_file_id": "5b0e0c5e-3f4f-4b8e-9d1c-6a3a9f2f7c11",
        "preview_file_id": "0d7f2a41-8c55-4a51-a5a0-2b9c6f3e1d22",
        "page_raster_file_ids": [
            "a1f0c2d3-1111-4c4c-9a9a-000000000001",
            "a1f0c2d3-1111-4c4c-9a9a-000000000002",
            "a1f0c2d3-1111-4c4c-9a9a-000000000003",
            "a1f0c2d3-1111-4c4c-9a9a-000000000004",
        ],
        "logo_source": "article_masthead",
        "logo_url": "https://d12v9rtnomnebu.cloudfront.net/logo/publications/waste_black.svg",
        "root_selector_used": "article.brief",
        "removed_placeholders": [],
        "blocked_request_count": 3,
        "outlet_name": "Waste Dive",
        "headline": "Kanopy integrates recycling monitoring and AI tools under new parent company",
        "byline": "Megan Quinn",
        "published_at": "2026-09-25",
        "source_url": "https://www.wastedive.com/news/kanopy-integrates-recycling-monitoring-tools-recycle-coach-re-trac/831358/",
        "client_found_in_text": True,
        "scope": "whole",
        "notes": [
            "No heading in the article starts with 'Recycle Coach', so section scope could not "
            "apply; the clip is the whole article."
        ],
    },
    # DISTILLED — logo_source and client_found_in_text are the load-bearing fields:
    # a text wordmark is not shippable, and a clip of an article that never names
    # the client must not be made. removed_placeholders is the audit trail that
    # lets a reviewer prove no real photo vanished.
    maturity="distilled",
)
class PressClipRender(KindModel):
    """One live article rendered as a press clip: PDF, preview and page rasters."""

    pdf_file_id: str = Field(description="The A4 clip PDF, in the organization's file store.")
    preview_file_id: str = Field(description="A full-page PNG screenshot of the clipped page.")
    page_raster_file_ids: list[str] = Field(
        default_factory=list,
        description=(
            "Every PDF page rasterized to PNG, in page order — every page borders a page break "
            "and the last page is always included. Review THESE, not the preview: trailing bands "
            "and content cut at a break exist only in the PDF."
        ),
    )
    logo_source: PressClipLogoSource = Field(
        description=(
            "Where the stamped logo came from, in ladder order. 'text_wordmark' means no real "
            "logo was found anywhere and the clip is NOT shippable."
        )
    )
    logo_url: str | None = Field(
        default=None,
        description="The logo image stamped at the top; null for an inline SVG or a wordmark.",
    )
    root_selector_used: str = Field(
        description="The article container the surgery kept (the caller's root, or the one picked structurally)."
    )
    removed_placeholders: list[str] = Field(
        default_factory=list,
        description="Every empty placeholder box swept from the article, as 'tag.class [W×H]'.",
    )
    blocked_request_count: int = Field(
        default=0,
        ge=0,
        description="Requests aborted because they went to an ad/recirculation/comment network.",
    )
    outlet_name: str | None = Field(
        default=None, description="The publication's name as the page states it."
    )
    headline: str | None = Field(default=None, description="Read from the page; null when absent.")
    byline: str | None = Field(default=None, description="Read from the page; null when absent.")
    published_at: str | None = Field(
        default=None,
        description="Read from the page as written (ISO or visible text); null when absent.",
    )
    source_url: str = Field(description="The URL the browser ended on.")
    client_found_in_text: bool = Field(
        description="Whether the client's name appears in the article text (plain, case-insensitive search)."
    )
    scope: Literal["whole", "section"] = Field(
        description="The scope actually applied; a requested section with no matching heading falls back to 'whole'."
    )
    notes: list[str] = Field(
        default_factory=list,
        description="Every fallback, override miss and late-overlay removal, said out loud.",
    )


__all__ = ["PressClipLogoSource", "PressClipRender"]
