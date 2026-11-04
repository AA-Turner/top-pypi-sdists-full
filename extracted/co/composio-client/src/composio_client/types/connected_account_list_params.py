# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_list_params."""

from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import TypedDict
from .._types import SequenceNotStr


class ConnectedAccountListParams(TypedDict, total=False):
    toolkit_slugs: Optional[SequenceNotStr[str]]
    "The toolkit slugs of the connected accounts"
    statuses: Optional[list[Literal['INITIALIZING', 'INITIATED', 'ACTIVE', 'FAILED', 'EXPIRED', 'INACTIVE', 'REVOKED']]]
    "The status of the connected account"
    cursor: Optional[str]
    "The cursor to paginate through the connected accounts"
    limit: Optional[float]
    "The limit of the connected accounts to return"
    user_ids: Optional[SequenceNotStr[str]]
    "The user ids of the connected accounts"
    auth_config_ids: Optional[SequenceNotStr[str]]
    "The auth config ids of the connected accounts"
    connected_account_ids: Optional[SequenceNotStr[str]]
    "The connected account ids to filter by"
    order_by: Literal['created_at', 'updated_at']
    "The order by of the connected accounts"
    order_direction: Literal['asc', 'desc']
    "The order direction of the connected accounts"
    account_type: Literal['PRIVATE', 'SHARED', 'ALL']
    "[Experimental] Filter by sharing model.\n\nDefault (omitted) returns PRIVATE only — shared accounts must be requested\nexplicitly. Pass SHARED for only shared accounts, or ALL for PRIVATE + SHARED."


__all__ = [
    "ConnectedAccountListParams",
]
