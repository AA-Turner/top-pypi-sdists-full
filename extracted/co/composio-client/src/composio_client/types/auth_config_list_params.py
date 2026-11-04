# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.auth_config_list_params."""

from __future__ import annotations

from typing import Optional, Union

from typing_extensions import TypedDict


class AuthConfigListParams(TypedDict, total=False):
    is_composio_managed: Union[str, bool]
    "Whether to filter by composio managed auth configs"
    toolkit_slug: str
    "Comma-separated list of toolkit slugs to filter auth configs by"
    deprecated_app_id: str
    "The app id to filter by"
    deprecated_status: str
    "DEPRECATED: This parameter will be removed in a future version."
    show_disabled: Optional[bool]
    "Show disabled auth configs"
    search: str
    "Search auth configs by name or id"
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "AuthConfigListParams",
]
