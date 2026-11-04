# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_create_download_url_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ...._base_model import BaseModel


class FileCreateDownloadURLResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    download_url: str
    "Presigned download URL for the file"
    expires_at: str
    "ISO 8601 timestamp when the download URL expires"
    mount_relative_path: str
    "Relative file path within the mount (e.g. \"report.pdf\")"
    sandbox_mount_prefix: str
    "Absolute mount path inside the sandbox (e.g. /mnt/files)"


__all__ = [
    "FileCreateDownloadURLResponse",
]
