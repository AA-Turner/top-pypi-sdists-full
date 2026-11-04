# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.auth_config_list_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict
from .._base_model import BaseModel


class ItemDeprecatedParams(BaseModel):
    "DEPRECATED: This parameter will be removed in a future version."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    default_connector_id: Optional[str] = None
    "Deprecated: Default connector ID"
    expected_input_fields: Optional[list[Dict[str, Optional[object]]]] = None
    "Deprecated: Fields expected during connection initialization"
    member_uuid: Optional[str] = None
    "Deprecated: Member UUID"
    toolkit_id: Optional[str] = None
    "Deprecated: Toolkit ID"


class ItemProxyConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    proxy_auth_key: Optional[str] = None
    "The auth key for the auth proxy"
    proxy_url: str
    "The url of the auth proxy"


class ItemToolAccessConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    tools_available_for_execution: Optional[list[str]] = None
    "The actions that the user can perform on the auth config.\n\nIf passed, this will update the actions that the user can perform on the auth\nconfig."
    tools_for_connected_account_creation: Optional[list[str]] = None
    "Tools used to generate the minimum required scopes for the auth config (only\nvalid for OAuth). If passed, this will update the scopes."


class ItemToolkit(BaseModel):
    "Information about the associated integration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_guide_url: Optional[str] = None
    "URL to a guide page with authentication setup instructions"
    auth_hint_url: Optional[str] = None
    "URL to a page where users can obtain or configure credentials"
    logo: str
    "The URL to the integration app's logo image"
    slug: str
    "The unique identifier of the integration app"


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Optional[Literal['OAUTH2', 'OAUTH1', 'API_KEY', 'BASIC', 'BILLCOM_AUTH', 'BEARER_TOKEN', 'GOOGLE_SERVICE_ACCOUNT', 'NO_AUTH', 'BASIC_WITH_JWT', 'CALCOM_AUTH', 'SERVICE_ACCOUNT', 'SAML', 'DCR_OAUTH', 'S2S_OAUTH2']] = None
    "The authentication scheme used (e.g., OAuth2, API Key, etc.)"
    created_at: Optional[str] = None
    "ISO 8601 date-time when the auth config was created"
    created_by: Optional[str] = None
    "The identifier of the user who created the auth config"
    credentials: Optional[Dict[str, Optional[object]]] = None
    "The authentication credentials (tokens, keys, etc.) - may be partially hidden\nfor security"
    deprecated_params: Optional[ItemDeprecatedParams] = None
    "DEPRECATED: This parameter will be removed in a future version."
    expected_input_fields: Optional[list[Optional[object]]] = None
    "Fields expected during connection initialization"
    id: str
    "The unique ID of the authentication configuration"
    is_composio_managed: Optional[bool] = None
    "Whether this authentication configuration is managed by Composio or the user"
    is_enabled_for_tool_router: Optional[bool] = None
    "Whether this auth config is enabled for tool router"
    last_updated_at: Optional[str] = None
    "ISO 8601 date-time when the auth config was last updated"
    name: str
    "The display name of the authentication configuration"
    no_of_connections: float
    "The number of active connections using this auth config"
    proxy_config: Optional[ItemProxyConfig] = None
    restrict_to_following_tools: Optional[list[str]] = None
    "Use tool_access_config instead. This field will be deprecated in the future."
    shared_credentials: Optional[Dict[str, Optional[object]]] = None
    "[EXPERIMENTAL] Shared credentials that will be inherited by all connected\naccounts using this auth config"
    status: Literal['ENABLED', 'DISABLED']
    "Current status of the authentication configuration"
    tool_access_config: ItemToolAccessConfig
    toolkit: ItemToolkit
    "Information about the associated integration"
    type: Literal['default', 'custom']
    "The type of the authentication configuration (custom or default)"
    uuid: str
    "The UUID of the authentication configuration (for backward compatibility)"
    shared_connection_fields: dict[str, object | None] | None = None


class AuthConfigListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


__all__ = [
    "AuthConfigListResponse",
    "Item",
    "ItemToolAccessConfig",
    "ItemToolkit",
    "ItemDeprecatedParams",
    "ItemProxyConfig",
]
