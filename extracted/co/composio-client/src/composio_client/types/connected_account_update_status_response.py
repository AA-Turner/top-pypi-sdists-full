# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_update_status_response."""

from __future__ import annotations

from pydantic import ConfigDict
from .._base_model import BaseModel


class ConnectedAccountUpdateStatusResponse(BaseModel):
    "Response returned after successfully updating a connected account status"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    success: bool
    "Indicates whether the connected account status was successfully updated"


__all__ = [
    "ConnectedAccountUpdateStatusResponse",
]
