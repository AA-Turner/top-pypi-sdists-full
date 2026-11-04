# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_retrieve_params."""

from __future__ import annotations

from typing_extensions import TypedDict


class ToolkitRetrieveParams(TypedDict, total=False):
    version: str
    "Version of the toolkit"


__all__ = [
    "ToolkitRetrieveParams",
]
