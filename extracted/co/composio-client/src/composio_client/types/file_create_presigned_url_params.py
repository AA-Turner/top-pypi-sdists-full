# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.file_create_presigned_url_params."""

from __future__ import annotations

from typing_extensions import Required, TypedDict


class FileCreatePresignedURLParams(TypedDict, total=False):
    toolkit_slug: Required[str]
    "Slug of the app where this file belongs to. Example: \"gmail\", \"slack\", \"github\" "
    tool_slug: Required[str]
    "Slug of the action where this file belongs to.\n\nExample: \"GMAIL_SEND_EMAIL\", \"SLACK_UPLOAD_FILE\""
    filename: Required[str]
    "Name of the original file. Example: \"quarterly_report.pdf\" "
    mimetype: Required[str]
    "Mime type of the original file. Example: \"application/pdf\", \"image/png\" "
    md5: Required[str]
    "MD5 hash of the file for deduplication and integrity verification.\n\nExample: \"a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6\""


__all__ = [
    "FileCreatePresignedURLParams",
]
