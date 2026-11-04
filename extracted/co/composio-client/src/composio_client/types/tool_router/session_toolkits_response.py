# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_toolkits_response."""

from __future__ import annotations

import datetime
from typing import Optional

from pydantic import ConfigDict, Field
from ..._base_model import BaseModel


class ItemConnectedAccountAuthConfig(BaseModel):
    "Auth config details"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: str
    "Authentication scheme type"
    id: str
    "Auth config identifier"
    is_composio_managed: bool
    "Whether this is a Composio-managed auth config"


class ItemConnectedAccount(BaseModel):
    "Connected account if available"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_config: ItemConnectedAccountAuthConfig
    "Auth config details"
    created_at: datetime.datetime
    "Creation timestamp"
    id: str
    "Connected account identifier"
    status: str
    "Connection status"
    user_id: str
    "User identifier"


class ItemMeta(BaseModel):
    "Toolkit metadata"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    description: str
    "Description of the toolkit"
    logo: str
    "URL to the toolkit logo"
    is_no_auth: bool | None = Field(default=None, alias="isNoAuth")


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    composio_managed_auth_schemes: list[str]
    "Available Composio-managed auth schemes"
    connected_account: Optional[ItemConnectedAccount] = None
    "Connected account if available"
    enabled: bool
    "Whether the toolkit is enabled"
    is_no_auth: bool
    "Whether the toolkit is no-auth"
    meta: ItemMeta
    "Toolkit metadata"
    name: str
    "Display name of the toolkit"
    slug: str
    "Unique slug identifier"


class SessionToolkitsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "SessionToolkitsResponse",
    "Item",
    "ItemConnectedAccount",
    "ItemConnectedAccountAuthConfig",
    "ItemMeta",
]
