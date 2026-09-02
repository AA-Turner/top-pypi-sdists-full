"""Pydantic output models for SEO tools.

These models enforce schema-compliant output for the frontend. API responses
are normalized (null → defaults) before validation so we always produce
consistent types.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MonthlySearchItem(BaseModel):
    year: int = 0
    month: int = 0
    search_volume: int = 0


class SeoKeywordDataItem(BaseModel):
    """Single keyword result — schema matches DB output_schema for keywords_data items."""

    keyword: str = ""
    cpc: float = 0.0
    competition: str = ""
    search_volume: int = 0
    competition_index: int = 0
    monthly_searches: list[MonthlySearchItem] = Field(default_factory=list)


class SeoKeywordDataOutput(BaseModel):
    """Output shape for seo_get_keyword_data — matches DB output_schema."""

    keywords_data: list[SeoKeywordDataItem] = Field(default_factory=list)
    total_keywords: int = 0
    date_range: dict[str, str] = Field(default_factory=dict)
    search_parameters: dict[str, Any] = Field(default_factory=dict)


def normalize_keyword_item(raw: dict[str, Any]) -> SeoKeywordDataItem:
    """Convert raw DataForSEO API response to schema-compliant model.

    API returns null for fields when no data is available (e.g. niche keywords).
    We normalize to typed defaults so the frontend always receives consistent structure.
    """
    monthly = raw.get("monthly_searches") or []
    monthly_items = [
        MonthlySearchItem(
            year=item.get("year") or 0,
            month=item.get("month") or 0,
            search_volume=item.get("search_volume") or 0,
        )
        for item in monthly
        if isinstance(item, dict)
    ]
    return SeoKeywordDataItem(
        keyword=raw.get("keyword") or "",
        cpc=float(raw.get("cpc") or 0),
        competition=str(raw.get("competition") or ""),
        search_volume=int(raw.get("search_volume") or 0),
        competition_index=int(raw.get("competition_index") or 0),
        monthly_searches=monthly_items,
    )
