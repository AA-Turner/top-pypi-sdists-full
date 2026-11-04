# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_retrieve_multi_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, TypedDict
from .._types import SequenceNotStr


class ToolkitRetrieveMultiParams(TypedDict, total=False):
    toolkits: NotRequired[SequenceNotStr[str]]
    category: NotRequired[str]
    managed_by: NotRequired[Literal["composio", "all", "project"]]
    sort_by: NotRequired[Literal["usage", "alphabetically"]]
    limit: NotRequired[float | None]
    cursor: NotRequired[str]


__all__ = [
    "ToolkitRetrieveMultiParams",
]
