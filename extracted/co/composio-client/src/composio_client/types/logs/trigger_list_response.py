# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.logs.trigger_list_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from ..._base_model import BaseModel


class DataMeta(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    client_id: str = Field(alias="clientId")
    connection_id: str = Field(alias="connectionId")
    created_at: str = Field(alias="createdAt")
    id: str
    provider: str
    trigger_client_error: Optional[str] = Field(default=None, alias="triggerClientError")
    trigger_client_payload: Optional[str] = Field(default=None, alias="triggerClientPayload")
    trigger_client_response: Optional[str] = Field(default=None, alias="triggerClientResponse")
    trigger_id: Optional[str] = Field(default=None, alias="triggerId")
    trigger_name: Optional[str] = Field(default=None, alias="triggerName")
    trigger_nano_id: Optional[str] = Field(default=None, alias="triggerNanoId")
    trigger_provider_payload: Optional[str] = Field(default=None, alias="triggerProviderPayload")
    type: Literal['trigger', 'action']
    "Log entity type (trigger or action)"
    updated_at: str = Field(alias="updatedAt")


class Data(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    app_name: str = Field(alias="appName")
    client_id: str = Field(alias="clientId")
    connection_id: str = Field(alias="connectionId")
    created_at: str = Field(alias="createdAt")
    entity_id: str = Field(alias="entityId")
    id: str
    meta: DataMeta
    status: str
    type: Literal['trigger', 'action']
    "Log entity type (trigger or action)"


class TriggerListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    data: Optional[list[Data]] = None
    next_cursor: Optional[str] = Field(default=None, alias="nextCursor")


__all__ = [
    "TriggerListResponse",
    "Data",
    "DataMeta",
]
