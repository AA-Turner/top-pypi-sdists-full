# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_retrieve_categories_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class Item(BaseModel):
    "Information about a single toolkit category"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    "URL-friendly unique identifier for the category, used for filtering toolkits"
    name: str
    "Display name of the toolkit category"


class ToolkitRetrieveCategoriesResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "ToolkitRetrieveCategoriesResponse",
    "Item",
]
