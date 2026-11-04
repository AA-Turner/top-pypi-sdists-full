# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_patch_response."""

from __future__ import annotations

from pydantic import ConfigDict
from .._base_model import BaseModel


class ConnectedAccountPatchResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    "The unique identifier of the updated connected account"
    status: str
    "The current status of the connected account after the update (ACTIVE, EXPIRED,\nINACTIVE, etc.)"
    success: bool
    "Whether the update was successful"


__all__ = [
    "ConnectedAccountPatchResponse",
]
