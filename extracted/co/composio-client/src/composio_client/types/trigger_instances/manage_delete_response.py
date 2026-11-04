# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instances.manage_delete_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ..._base_model import BaseModel


class ManageDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    trigger_id: str
    "The ID of the deleted trigger instance"


__all__ = [
    "ManageDeleteResponse",
]
