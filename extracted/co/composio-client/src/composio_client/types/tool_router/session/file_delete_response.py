# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_delete_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ...._base_model import BaseModel


class FileDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    mount_relative_path: str
    "Relative file path that was deleted"
    sandbox_mount_prefix: str
    "Absolute mount path inside the sandbox (e.g. /mnt/files)"


__all__ = [
    "FileDeleteResponse",
]
