# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli.realtime_credentials_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ..._base_model import BaseModel


class RealtimeCredentialsResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    project_id: str
    "The project nanoId associated with the API Key provided.\n\nUsed as part of the CLI channel name: private-cli-{project_id}"
    pusher_cluster: str
    "The Pusher cluster for subscribing to the trigger"
    pusher_key: str
    "The Pusher client key for subscribing to the trigger"


__all__ = [
    "RealtimeCredentialsResponse",
]
