"""Reusable Pydantic validators for LLMParams wire fields."""

from __future__ import annotations

import re
import uuid
from typing import Annotated

from pydantic import BeforeValidator, Field

_MODEL_SLUG_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:/-]{0,127}$")


def _validate_uuid_string(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("must be a UUID string")
    try:
        uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"invalid UUID: {value!r}") from exc
    return value


def _validate_uuid_list(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("must be a list of UUID strings")
    return [_validate_uuid_string(item) for item in value]


def _validate_model_reference(value: object) -> str:
    """Accept a DB model UUID or a provider-native model slug/name."""
    if not isinstance(value, str):
        raise ValueError("model must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("model must not be empty")
    try:
        uuid.UUID(cleaned)
        return cleaned
    except (ValueError, AttributeError):
        pass
    if _MODEL_SLUG_RE.match(cleaned):
        return cleaned
    raise ValueError(
        f"model {value!r} must be a UUID or provider model slug (letters, digits, . _ - / :)"
    )


UuidString = Annotated[str, BeforeValidator(_validate_uuid_string)]
UuidStringList = Annotated[list[str], BeforeValidator(_validate_uuid_list)]
ModelReference = Annotated[str, BeforeValidator(_validate_model_reference)]

PositiveInt = Annotated[int, Field(gt=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
