# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_create_upload_url_response."""

from __future__ import annotations

from pydantic import ConfigDict
from ...._base_model import BaseModel


class FileCreateUploadURLResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    expires_at: str
    "ISO 8601 timestamp when the upload URL expires"
    mount_relative_path: str
    "Relative file path within the mount (e.g. \"report.pdf\")"
    sandbox_mount_prefix: str
    "Absolute mount path inside the sandbox (e.g. /mnt/files)"
    upload_url: str
    "Presigned upload URL — PUT the file content here"


__all__ = [
    "FileCreateUploadURLResponse",
]
