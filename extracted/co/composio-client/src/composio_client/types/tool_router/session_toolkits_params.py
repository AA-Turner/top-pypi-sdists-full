# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_toolkits_params."""

from __future__ import annotations

from typing import Optional

from typing_extensions import TypedDict
from ..._types import SequenceNotStr


class SessionToolkitsParams(TypedDict, total=False):
    limit: int
    "Number of items per page, max allowed is 50"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."
    toolkits: Optional[SequenceNotStr[str]]
    "Optional comma-separated list of toolkit slugs to filter by.\n\nIf provided, only these toolkits will be returned, overriding the session\nconfiguration."
    is_connected: Optional[bool]
    "Whether to filter by connected toolkits.\n\nIf provided, only connected toolkits will be returned."
    search: str
    "Search query to filter toolkits by name, slug, or description"


__all__ = [
    "SessionToolkitsParams",
]
