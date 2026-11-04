# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.org.owner.project_list_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class ProjectListParams(TypedDict, total=False):
    limit: NotRequired[float | None]
    cursor: NotRequired[str]


__all__ = [
    "ProjectListParams",
]
