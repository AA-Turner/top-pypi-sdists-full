# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.org_list_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class OrgListParams(TypedDict, total=False):
    limit: NotRequired[int]
    cursor: NotRequired[str]


__all__ = [
    "OrgListParams",
]
