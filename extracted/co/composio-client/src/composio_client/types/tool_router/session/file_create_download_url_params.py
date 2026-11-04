# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session.file_create_download_url_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class FileCreateDownloadURLParams(TypedDict, total=False):
    session_id: Required[str]
    "The unique identifier of the tool router session"
    mount_relative_path: Required[str]
    "Relative file path within the mount"


__all__ = [
    "FileCreateDownloadURLParams",
]
