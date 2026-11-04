# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_refresh_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class ConnectedAccountRefreshResponse(BaseModel):
    "Response schema for a refreshed connected account authentication"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    "The unique identifier of the connected account"
    redirect_url: Optional[str] = None
    "The URL to which the user should be redirected to complete the authentication\nprocess (null for auth schemes that do not require redirection)"
    status: Literal['INITIALIZING', 'INITIATED', 'ACTIVE', 'FAILED', 'EXPIRED', 'INACTIVE', 'REVOKED']
    "The current status of the connected account (e.g., active, pending, failed)"


__all__ = [
    "ConnectedAccountRefreshResponse",
]
