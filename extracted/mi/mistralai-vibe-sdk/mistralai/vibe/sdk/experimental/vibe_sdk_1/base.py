"""Shared primitives for the experimental Vibe SDK v1 protocol."""

from typing import Any

from pydantic import BaseModel, ConfigDict

type JsonSchema = dict[str, Any]


class ProtocolModel(BaseModel):
    """Base model for serializable Vibe SDK v1 protocol data."""

    model_config = ConfigDict(
        extra="ignore",
        validate_by_alias=True,
        validate_by_name=True,
    )
