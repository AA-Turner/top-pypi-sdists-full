"""Shared validation and wire behavior for the Session API."""

from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

type JsonSchema = dict[str, Any]


class SessionModel(BaseModel):
    """Camel-case Session wire model with forward-compatible client parsing."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="ignore",
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )
