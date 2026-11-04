# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_list_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class ItemDeprecated(BaseModel):
    "Deprecated toolkit ID"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    toolkit_id: str = Field(alias="toolkitId")


class ItemMetaCategory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    "Category identifier"
    name: str
    "Human-readable category name"


class ItemMeta(BaseModel):
    "Additional metadata about the toolkit"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    app_url: Optional[str] = None
    "Link to the toolkit's main application or service website"
    categories: list[ItemMetaCategory]
    "List of categories associated with this toolkit"
    created_at: str
    "Creation date and time of the toolkit"
    description: str
    "Human-readable description explaining the toolkit's purpose and functionality"
    logo: str
    "Image URL for the toolkit's branding"
    tools_count: float
    "Count of available tools in this toolkit"
    triggers_count: float
    "Count of available triggers in this toolkit"
    updated_at: str
    "Last modification date and time of the toolkit"
    version: str
    "Version of the toolkit"


class CurrentItemInstant(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    supported: Literal[True]


class Item(BaseModel):
    "Detailed information about a toolkit"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_guide_url: Optional[str] = None
    "URL to a guide page with authentication setup instructions for this toolkit"
    auth_schemes: Optional[list[str]] = None
    "List of authentication methods supported by this toolkit"
    composio_managed_auth_schemes: Optional[list[str]] = None
    "List of authentication methods that Composio manages for this toolkit"
    deprecated: ItemDeprecated
    "Deprecated toolkit ID"
    is_local_toolkit: bool
    "DEPRECATED: This field is no longer meaningful and will always return false.\n\nIt was previously used to indicate if a toolkit is specific to the current\nproject."
    meta: ItemMeta
    "Additional metadata about the toolkit"
    name: str
    "Human-readable name of the toolkit"
    no_auth: Optional[bool] = None
    "When true, this toolkit can be used without authentication"
    slug: str
    "URL-friendly unique identifier for the toolkit"
    type: Literal['native', 'custom']
    "Toolkit provenance: \"native\" for Composio-managed toolkits, \"custom\" for a\nproject-registered custom (MCP) toolkit"
    instant: CurrentItemInstant | None = None
    access: Literal["all", "user"] | None = None


class ToolkitListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "ToolkitListResponse",
    "Item",
    "ItemDeprecated",
    "ItemMeta",
    "ItemMetaCategory",
    "CurrentItemInstant",
]
