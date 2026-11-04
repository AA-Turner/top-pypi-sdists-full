# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_list_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class FileListParams(TypedDict, total=False):
    session_id: Required[str]
    "The unique identifier of the tool router session"
    cursor: str
    "Pagination cursor from the previous response next_cursor field"
    limit: float
    "Maximum number of files to return per page (1-500)"
    mount_relative_prefix: str
    "Relative path prefix within the mount for filtering"


__all__ = [
    "FileListParams",
]
