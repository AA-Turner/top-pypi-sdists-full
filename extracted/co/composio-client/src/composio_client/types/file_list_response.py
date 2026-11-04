# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.file_list_response."""

from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    filename: str
    "Name of the original file. Example: \"document.docx\" "
    md5: str
    "MD5 hash of the file for integrity verification.\n\nExample: \"d41d8cd98f00b204e9800998ecf8427e\""
    mimetype: str
    "Mime type of the original file.\n\nExample:\n\"application/vnd.openxmlformats-officedocument.wordprocessingml.document\""
    tool_slug: str
    "Slug of the action where this file belongs to. Example: \"convert-to-pdf\" "
    toolkit_slug: str
    "Slug of the app where this file belongs to. Example: \"file-converter\" "


class FileListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "FileListResponse",
    "Item",
]
