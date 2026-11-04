# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_list_params."""

from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import NotRequired, TypedDict


class ToolkitListParams(TypedDict, total=False):
    category: str
    "Filter toolkits by category"
    managed_by: Literal['composio', 'all', 'project']
    "Filter toolkits by who manages them"
    type: Literal['native', 'custom', 'all']
    "Filter toolkits by provenance (alias over managed_by)"
    sort_by: Literal['usage', 'alphabetically']
    "Sort order for returned toolkits"
    include_deprecated: Optional[bool]
    "Include deprecated toolkits in the response"
    search: str
    "Search query to filter toolkits by name, slug, or description"
    user_id: NotRequired[str]
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "ToolkitListParams",
]
