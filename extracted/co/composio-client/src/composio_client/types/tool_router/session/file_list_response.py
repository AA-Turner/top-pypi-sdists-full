# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_list_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from ...._base_model import BaseModel


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    last_modified: str
    "ISO 8601 timestamp of last modification"
    mount_relative_path: str
    "Relative file path within the mount (e.g. \"report.pdf\")"
    sandbox_mount_prefix: str
    "Absolute mount path inside the sandbox (e.g. /mnt/files)"
    size: float
    "File size in bytes"


class FileListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    items: list[Item]
    "List of files in the mount"
    next_cursor: Optional[str] = None
    "Cursor for the next page of results. If absent, there are no more pages."


__all__ = [
    "FileListResponse",
    "Item",
]
