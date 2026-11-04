# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instance_upsert_response."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class Deprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    uuid: str
    "ID of the updated trigger"


class TriggerInstanceUpsertResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    deprecated: Optional[Deprecated] = None
    trigger_id: str
    "ID of the updated trigger"
    type: Literal["webhook", "poll"]
    fallback_reason: str | None
    polling_interval: int | None


__all__ = [
    "TriggerInstanceUpsertResponse",
    "Deprecated",
]
