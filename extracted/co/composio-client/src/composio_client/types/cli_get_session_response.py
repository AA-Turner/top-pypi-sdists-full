# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.cli_get_session_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class Account(BaseModel):
    "Information about the linked account, if any.\n\nNull if the session status is \"pending\"."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    email: str
    "The email address of the linked account"
    id: str
    "The ID of the linked account"
    name: str
    "The display name of the linked account"


class CliGetSessionResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account: Optional[Account] = None
    "Information about the linked account, if any.\n\nNull if the session status is \"pending\"."
    api_key: Optional[str] = None
    "The API key for the linked account"
    code: str
    "The 6-character hexadecimal code used for CLI login"
    expires_at: str = Field(alias="expiresAt")
    "The ISO timestamp when the session expires"
    id: str
    "The unique identifier for the CLI session"
    scope: Optional[Literal['project', 'user']] = None
    "The key scope for this session"
    status: Literal['pending', 'linked']
    "The current status of the session"


__all__ = [
    "CliGetSessionResponse",
    "Account",
]
