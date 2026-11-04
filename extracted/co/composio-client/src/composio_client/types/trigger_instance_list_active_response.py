# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instance_list_active_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class ItemDeprecated(BaseModel):
    "Deprecated fields for the trigger instance"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    created_at: str = Field(alias="createdAt")
    "Deprecated created_at for the trigger instance"


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    connected_account_id: str = Field(alias="connectedAccountId")
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use connected_account_id instead."
    connected_account_uuid: str
    "UUID of the connected account this trigger is associated with"
    deprecated: Optional[ItemDeprecated] = None
    "Deprecated fields for the trigger instance"
    disabled_at: Optional[str] = Field(default=None, alias="disabledAt")
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use disabled_at instead."
    id: str
    "Nano ID of the trigger instance"
    state: Dict[str, Optional[object]]
    "DEPRECATED: This field exposes internal state and will be removed in a future\nversion."
    trigger_config: Dict[str, Optional[object]] = Field(alias="triggerConfig")
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use trigger_config instead."
    trigger_data: Optional[str] = None
    "Additional data associated with the trigger instance"
    trigger_name: str = Field(alias="triggerName")
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use trigger_name instead."
    updated_at: str = Field(alias="updatedAt")
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use updated_at instead."
    user_id: str
    "ID of the user this trigger is associated with"
    uuid: Optional[str] = None
    "Unique identifier of the trigger instance"
    version: str
    "Version of the trigger instance"
    type: Literal["webhook", "poll"]
    fallback_reason: str | None
    polling_interval: int | None
    egress_url: str | None


class TriggerInstanceListActiveResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "TriggerInstanceListActiveResponse",
    "Item",
    "ItemDeprecated",
]
