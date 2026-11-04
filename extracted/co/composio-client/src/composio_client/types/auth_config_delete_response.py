# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.auth_config_delete_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class AuthConfigDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    revoke_job_id: Optional[str] = None
    "Identifier of the background revoke job started for this delete.\n\nPresent only when `revoke_on_delete=true`. Track the job and its per-connection\nresults from the Composio dashboard — a programmatic endpoint to poll this job\nis not yet generally available."
    success: bool
    message: str


__all__ = [
    "AuthConfigDeleteResponse",
]
