# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_retrieve_changelog_params."""

from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class ToolkitRetrieveChangelogParams(TypedDict, total=False):
    user_id: NotRequired[str]


__all__ = [
    "ToolkitRetrieveChangelogParams",
]
