# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_retrieve_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class AuthConfigDetailDeprecatedAuthProviderDetails(BaseModel):
    "Authentication URL fields for OAuth 2.0 and OAuth 1.0.\n\nWe don't recommend using this field for authentication and might break post Aug 31 2025."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None


class AuthConfigDetailFieldsAuthConfigCreationOptional(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    default: Optional[str] = None
    description: str
    display_name: str = Field(alias="displayName")
    is_secret: Optional[bool] = None
    legacy_template_name: Optional[str] = None
    name: str
    required: bool
    type: str
    user_visible: bool


class AuthConfigDetailFieldsAuthConfigCreationRequired(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    default: Optional[str] = None
    description: str
    display_name: str = Field(alias="displayName")
    is_secret: Optional[bool] = None
    legacy_template_name: Optional[str] = None
    name: str
    required: bool
    type: str
    user_visible: bool


class AuthConfigDetailFieldsAuthConfigCreation(BaseModel):
    "Form fields needed when creating an authentication configuration"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    optional: list[AuthConfigDetailFieldsAuthConfigCreationOptional]
    required: list[AuthConfigDetailFieldsAuthConfigCreationRequired]


class AuthConfigDetailFieldsConnectedAccountInitiationOptional(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    default: Optional[str] = None
    description: str
    display_name: str = Field(alias="displayName")
    is_secret: Optional[bool] = None
    legacy_template_name: Optional[str] = None
    name: str
    required: bool
    type: str
    user_visible: bool


class AuthConfigDetailFieldsConnectedAccountInitiationRequired(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    default: Optional[str] = None
    description: str
    display_name: str = Field(alias="displayName")
    is_secret: Optional[bool] = None
    legacy_template_name: Optional[str] = None
    name: str
    required: bool
    type: str
    user_visible: bool


class AuthConfigDetailFieldsConnectedAccountInitiation(BaseModel):
    "Form fields needed when connecting a user account with this authentication method"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    optional: list[AuthConfigDetailFieldsConnectedAccountInitiationOptional]
    required: list[AuthConfigDetailFieldsConnectedAccountInitiationRequired]


class AuthConfigDetailFields(BaseModel):
    "Field groups required for different authentication stages"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_config_creation: AuthConfigDetailFieldsAuthConfigCreation
    "Form fields needed when creating an authentication configuration"
    connected_account_initiation: AuthConfigDetailFieldsConnectedAccountInitiation
    "Form fields needed when connecting a user account with this authentication\nmethod"


class AuthConfigDetailProxy(BaseModel):
    "Configuration for proxying authentication requests to external services"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    base_url: str
    "URL to which authentication requests will be proxied"


class AuthConfigDetail(BaseModel):
    "Detailed configuration for an authentication method"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_hint_url: Optional[str] = None
    "URL to a page where users can obtain or configure credentials for this\nauthentication method"
    deprecated_auth_provider_details: Optional[AuthConfigDetailDeprecatedAuthProviderDetails] = None
    "Authentication URL fields for OAuth 2.0 and OAuth 1.0.\n\nWe don't recommend using this field for authentication and might break post Aug\n31 2025."
    fields: AuthConfigDetailFields
    "Field groups required for different authentication stages"
    mode: str
    "The type of authentication mode (e.g., oauth2, basic_auth, api_key)"
    name: str
    "Display name for this authentication method"
    proxy: Optional[AuthConfigDetailProxy] = None
    "Configuration for proxying authentication requests to external services"
    required_scopes: list[str]


class ComposioManagedAuthScopes(BaseModel):
    "OAuth scopes available in the Composio-managed auth config for this auth mode."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    available: list[str]
    "Available OAuth scopes"


class ComposioManagedAuthUserScopes(BaseModel):
    "OAuth user scopes available in the Composio-managed auth config for this auth mode. Only present for Slack toolkits."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    available: list[str]
    "Available OAuth user scopes"


class ComposioManagedAuth(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    mode: str
    "Authentication mode for the Composio-managed auth config"
    scopes: ComposioManagedAuthScopes
    "OAuth scopes available in the Composio-managed auth config for this auth mode."
    user_scopes: Optional[ComposioManagedAuthUserScopes] = None
    "OAuth user scopes available in the Composio-managed auth config for this auth\nmode. Only present for Slack toolkits."
    managed_app_id: str
    is_default: bool


class Deprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    get_current_user_endpoint: Optional[str] = Field(default=None, alias="getCurrentUserEndpoint")
    raw_proxy_info_by_auth_schemes: list[Dict[str, Optional[object]]] = Field(alias="rawProxyInfoByAuthSchemes")
    toolkit_id: str = Field(alias="toolkitId")


class MetaCategory(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str
    "Human-readable category name"
    slug: str
    "URL-friendly identifier for the category"


class Meta(BaseModel):
    "Comprehensive metadata for the toolkit including dates, descriptions, and statistics"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    app_url: Optional[str] = None
    "Link to the toolkit's main application or service website"
    available_versions: list[str]
    "Available versions of the toolkit"
    categories: list[MetaCategory]
    "List of categories associated with this toolkit"
    created_at: str
    "Creation date and time of the toolkit"
    description: str
    "Human-readable description explaining the toolkit's purpose and functionality"
    logo: str
    "Image URL for the toolkit's branding"
    tools_count: float
    "Count of available tools in this toolkit"
    triggers_count: float
    "Count of available triggers in this toolkit"
    updated_at: str
    "Last modification date and time of the toolkit"
    version: str
    "Version of the toolkit"


class ToolkitRetrieveResponse(BaseModel):
    "Detailed information about a single toolkit"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_config_details: Optional[list[AuthConfigDetail]] = None
    "Complete authentication configuration details for each supported auth method"
    auth_guide_url: Optional[str] = None
    "URL to a guide page with authentication setup instructions for this toolkit"
    base_url: Optional[str] = None
    "If evaluation of base URL needs some connection info (like shopify), please\ncreate the connection and get the base URL from there"
    composio_managed_auth: list[ComposioManagedAuth]
    "Managed-auth-only metadata, including the supported OAuth scope ceiling."
    composio_managed_auth_schemes: Optional[list[str]] = None
    "List of authentication methods that Composio manages for this toolkit"
    deprecated: Deprecated
    enabled: bool
    "Indicates if this toolkit is currently enabled and available for use"
    get_current_user_endpoint: Optional[str] = None
    "Endpoint to get the current user"
    get_current_user_endpoint_method: Optional[str] = None
    "HTTP method to use when calling the get current user endpoint (e.g., GET, POST)"
    is_local_toolkit: bool
    "DEPRECATED: This field is no longer meaningful and will always return false.\n\nIt was previously used to indicate if a toolkit is specific to the current\nproject."
    meta: Meta
    "Comprehensive metadata for the toolkit including dates, descriptions, and\nstatistics"
    name: str
    "Human-readable name of the toolkit"
    slug: str
    "URL-friendly unique identifier for the toolkit"
    type: Literal['native', 'custom']
    "Toolkit provenance: \"native\" for Composio-managed toolkits, \"custom\" for a\nproject-registered custom (MCP) toolkit"
    access: Literal["all", "user"] | None = None


__all__ = [
    "ToolkitRetrieveResponse",
    "ComposioManagedAuth",
    "ComposioManagedAuthScopes",
    "ComposioManagedAuthUserScopes",
    "Deprecated",
    "Meta",
    "MetaCategory",
    "AuthConfigDetail",
    "AuthConfigDetailFields",
    "AuthConfigDetailFieldsAuthConfigCreation",
    "AuthConfigDetailFieldsAuthConfigCreationOptional",
    "AuthConfigDetailFieldsAuthConfigCreationRequired",
    "AuthConfigDetailFieldsConnectedAccountInitiation",
    "AuthConfigDetailFieldsConnectedAccountInitiationOptional",
    "AuthConfigDetailFieldsConnectedAccountInitiationRequired",
    "AuthConfigDetailDeprecatedAuthProviderDetails",
    "AuthConfigDetailProxy",
]
