# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli.realtime_auth_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from ..._base_model import BaseModel


class RealtimeAuthResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth: str
    "The authentication string for Pusher"
    channel_data: Optional[str] = None
    "Channel data for presence channels"


__all__ = [
    "RealtimeAuthResponse",
]
