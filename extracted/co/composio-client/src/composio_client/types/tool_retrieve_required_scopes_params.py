# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_retrieve_required_scopes_params."""

from __future__ import annotations

from typing_extensions import NotRequired, Required, TypedDict
from .._types import SequenceNotStr


class ToolRetrieveRequiredScopesParams(TypedDict, total=False):
    tools: Required[SequenceNotStr[str]]
    version: NotRequired[str]


__all__ = [
    "ToolRetrieveRequiredScopesParams",
]
