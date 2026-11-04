# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.auth_config_create_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class AuthConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: str
    "The authentication mode of the toolkit"
    id: str
    "The auth config id of the toolkit (must be a valid auth config id)"
    is_composio_managed: bool
    "Whether the auth config is managed by Composio"
    restrict_to_following_tools: Optional[list[str]] = None
    "The tools that the user can use with the auth config"


class Toolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    slug: str
    "The unique key of the toolkit"


class AuthConfigCreateResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_config: AuthConfig
    toolkit: Toolkit


__all__ = [
    "AuthConfigCreateResponse",
    "AuthConfig",
    "Toolkit",
]
