# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.link_create_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class ExperimentalACLConfigForShared(BaseModel):
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers; non-creator cookie callers receive the response without this block."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allow_all_users: bool
    allowed_user_ids: list[str]
    not_allowed_user_ids: list[str]


class Experimental(BaseModel):
    "Experimental features - not stable, may be modified or removed in future versions."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_type: Literal['PRIVATE', 'SHARED']
    "Sharing model for this connected account.\n\nPRIVATE is usable only by the owning user_id. SHARED is reachable from a\ntool-router session only when explicitly pinned in the session config."
    acl_config_for_shared: Optional[ExperimentalACLConfigForShared] = None
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers;\nnon-creator cookie callers receive the response without this block."


class LinkCreateResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    connected_account_id: str
    "The connected account ID that was created"
    experimental: Optional[Experimental] = None
    "Experimental features - not stable, may be modified or removed in future\nversions."
    expires_at: str
    "ISO timestamp when the link expires"
    link_token: str
    "The generated link token for the auth session"
    redirect_url: str
    "The redirect URI to send users to for authentication"


__all__ = [
    "LinkCreateResponse",
    "Experimental",
    "ExperimentalACLConfigForShared",
]
