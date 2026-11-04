# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.trigger_instance_list_active_params."""

from __future__ import annotations

from typing import Annotated, Optional

from typing_extensions import TypedDict
from .._types import PropertyInfo, SequenceNotStr


class TriggerInstanceListActiveParams(TypedDict, total=False):
    user_ids: Optional[SequenceNotStr[str]]
    "Array of user IDs to filter triggers by"
    query_connected_account_ids_1: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='connected_account_ids')]
    "Array of connected account IDs to filter triggers by"
    query_auth_config_ids_1: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='auth_config_ids')]
    "Array of auth config IDs to filter triggers by"
    query_trigger_ids_1: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='trigger_ids')]
    "Array of trigger IDs to filter triggers by"
    query_trigger_names_1: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='trigger_names')]
    "Array of trigger names to filter triggers by.\n\nCase-insensitive (internally normalized to uppercase)."
    query_connected_account_ids_2: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='connectedAccountIds')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use connected_account_ids instead."
    query_auth_config_ids_2: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='authConfigIds')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use auth_config_ids instead."
    query_trigger_ids_2: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='triggerIds')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use trigger_ids instead."
    query_show_disabled_1: Annotated[Optional[bool], PropertyInfo(alias='show_disabled')]
    "When set to true, includes disabled triggers in the response."
    query_trigger_names_2: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='triggerNames')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use trigger_names instead."
    query_show_disabled_2: Annotated[Optional[bool], PropertyInfo(alias='showDisabled')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use show_disabled instead."
    deprecated_connected_account_uuids: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='deprecatedConnectedAccountUuids')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use connected_account_ids instead."
    deprecated_auth_config_uuids: Annotated[Optional[SequenceNotStr[str]], PropertyInfo(alias='deprecatedAuthConfigUuids')]
    "DEPRECATED: This parameter will be removed in a future version.\n\nPlease use auth_config_ids instead."
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "TriggerInstanceListActiveParams",
]
