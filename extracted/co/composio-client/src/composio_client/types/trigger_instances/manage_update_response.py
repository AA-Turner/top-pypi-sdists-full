# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instances.manage_update_response."""

from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict
from ..._base_model import BaseModel


class ManageUpdateResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: Literal['success']
    "Status of the operation"


__all__ = [
    "ManageUpdateResponse",
]
