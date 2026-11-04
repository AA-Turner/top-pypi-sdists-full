# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli_create_session_response."""

from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class CliCreateSessionResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    code: str
    "The 6-character hexadecimal code used for CLI login"
    expires_at: str = Field(alias="expiresAt")
    "The ISO timestamp when the session expires"
    id: str
    "Unique identifier for the CLI session.\n\nUUID v4 format used for tracking and retrieval."
    scope: Literal['project', 'user']
    "The key scope for this session"
    status: Literal['pending', 'linked']
    "The current status of the session"


__all__ = [
    "CliCreateSessionResponse",
]
