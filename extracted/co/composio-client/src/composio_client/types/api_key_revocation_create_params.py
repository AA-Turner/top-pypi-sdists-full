# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.api_key_revocation_create_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict
from .._types import SequenceNotStr


class ApiKeyRevocationCreateParams(TypedDict, total=False):
    api_keys: Required[SequenceNotStr[str]]


__all__ = [
    "ApiKeyRevocationCreateParams",
]
