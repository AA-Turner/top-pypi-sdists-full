# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.logs.tool_list_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from ..._base_model import BaseModel


class DataApp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    icon: str
    name: str


class DataMetadata(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    recipe_id: Optional[str] = None


class Data(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    action_key: str = Field(alias="actionKey")
    app: DataApp
    app_key: str = Field(alias="appKey")
    connected_account_id: str = Field(alias="connectedAccountId")
    created_at: float = Field(alias="createdAt")
    entity_id: str = Field(alias="entityId")
    execution_time: float = Field(alias="executionTime")
    id: str
    metadata: Optional[DataMetadata] = None
    minimal_response: str = Field(alias="minimalResponse")
    status: Literal['success', 'failed']
    credential_source: Literal["connected_account", "instant_account", "custom_auth", "no_auth"] | None = Field(default=None, alias="credentialSource")
    instant_charge: str | None = Field(default=None, alias="instantCharge")


class ToolListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    data: list[Data]
    next_cursor: Optional[float] = Field(default=None, alias="nextCursor")


__all__ = [
    "ToolListResponse",
    "Data",
    "DataApp",
    "DataMetadata",
]
