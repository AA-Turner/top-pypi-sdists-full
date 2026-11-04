# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_list_params."""

from __future__ import annotations

from typing import Dict, Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict
from .._types import SequenceNotStr


class ToolListParams(TypedDict, total=False):
    toolkit_slug: str
    "The slug of the toolkit to filter by"
    tool_slugs: str
    "Comma-separated list of specific tool slugs to retrieve (overrides other\nfilters)"
    auth_config_ids: Union[str, SequenceNotStr[str]]
    "Comma-separated list of auth config IDs to filter tools by"
    important: Literal['true', 'false']
    "Filter to only show important/featured tools (set to \"true\" to enable)"
    tags: SequenceNotStr[str]
    "Filter tools by one or more tags (can be specified multiple times)"
    scopes: Optional[SequenceNotStr[str]]
    "Array of scopes to filter tools by)"
    query: str
    "Full-text search query to filter tools by name, slug, or description.\n\nApplied as a soft filter on top of other filters."
    search: str
    "Deprecated: use \"query\" instead.\n\nFree-text search query to find tools by name, description, or functionality."
    include_deprecated: bool
    "Include deprecated tools in the response"
    include_pricing: NotRequired[bool]
    toolkit_versions: Union[str, Dict[str, str]]
    "Toolkit version specification.\n\nUse \"latest\" for latest versions or bracket notation for specific versions per\ntoolkit."
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "ToolListParams",
]
