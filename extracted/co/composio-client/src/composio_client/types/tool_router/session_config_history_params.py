# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_router.session_config_history_params."""

from __future__ import annotations

from typing_extensions import TypedDict


class SessionConfigHistoryParams(TypedDict, total=False):
    limit: int
    "Number of items per page, max allowed is 100"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "SessionConfigHistoryParams",
]
