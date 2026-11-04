# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.file_list_params."""

from __future__ import annotations

from typing import Optional

from typing_extensions import TypedDict


class FileListParams(TypedDict, total=False):
    toolkit_slug: str
    "Filter files by app slug. Example: \"file-converter\" "
    tool_slug: str
    "Filter files by action slug. Example: \"convert-to-pdf\" "
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "FileListParams",
]
