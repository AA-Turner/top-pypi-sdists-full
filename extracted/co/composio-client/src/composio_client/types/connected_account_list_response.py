# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_list_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class ItemAuthConfigDeprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    uuid: str
    "The uuid of the auth config"


class ItemAuthConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH2', 'OAUTH1', 'API_KEY', 'BASIC', 'BILLCOM_AUTH', 'BEARER_TOKEN', 'GOOGLE_SERVICE_ACCOUNT', 'NO_AUTH', 'BASIC_WITH_JWT', 'CALCOM_AUTH', 'SERVICE_ACCOUNT', 'SAML', 'DCR_OAUTH', 'S2S_OAUTH2']
    "the authScheme is part of the connection state use it there"
    deprecated: Optional[ItemAuthConfigDeprecated] = None
    id: str
    "The id of the auth config"
    is_composio_managed: bool
    "Whether the auth config is managed by Composio"
    is_disabled: bool
    "Whether the auth config is disabled"


class ItemDeprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    labels: list[str]
    "The labels of the connection"
    uuid: str
    "The uuid of the connection"


class ItemExperimentalACLConfigForShared(BaseModel):
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers; non-creator cookie callers receive the response without this block."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allow_all_users: bool
    allowed_user_ids: list[str]
    not_allowed_user_ids: list[str]


class ItemExperimental(BaseModel):
    "Experimental features - not stable, may be modified or removed in future versions."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_type: Literal['PRIVATE', 'SHARED']
    "Sharing model for this connected account.\n\nPRIVATE is usable only by the owning user_id. SHARED is reachable from a\ntool-router session only when explicitly pinned in the session config."
    acl_config_for_shared: Optional[ItemExperimentalACLConfigForShared] = None
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers;\nnon-creator cookie callers receive the response without this block."


class ItemStateUnionMember0ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    auth_uri: str = Field(alias="authUri")
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    callback_url: Optional[str] = Field(default=None, alias="callbackUrl")
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    oauth_token: str
    oauth_token_secret: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: str = Field(alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    callback_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    consumer_key: Optional[str] = None
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    oauth_token: str
    oauth_token_secret: str
    oauth_verifier: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: Optional[str] = Field(default=None, alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    callback_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    consumer_key: Optional[str] = None
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    oauth_token: str
    oauth_token_secret: str
    oauth_verifier: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: Optional[str] = Field(default=None, alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH1'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember0ValUnionMember0, ItemStateUnionMember0ValUnionMember1, ItemStateUnionMember0ValUnionMember2, ItemStateUnionMember0ValUnionMember3, ItemStateUnionMember0ValUnionMember4, ItemStateUnionMember0ValUnionMember5]


class ItemStateUnionMember1ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    callback_url: Optional[str] = None
    code_verifier: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    final_redirect_uri: Optional[str] = Field(default=None, alias="finalRedirectUri")
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: str = Field(alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    webhook_signature: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember2AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class ItemStateUnionMember1ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[ItemStateUnionMember1ValUnionMember2AuthedUser] = None
    "for slack user scopes"
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    extra_token_data: Optional[Dict[str, Optional[object]]] = None
    form_api_base_url: Optional[str] = None
    id_token: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    refresh_token: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    webhook_signature: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember3AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class ItemStateUnionMember1ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[ItemStateUnionMember1ValUnionMember3AuthedUser] = None
    "for slack user scopes"
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    extra_token_data: Optional[Dict[str, Optional[object]]] = None
    form_api_base_url: Optional[str] = None
    id_token: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    refresh_token: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    webhook_signature: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1ValUnionMember6(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    revoked_at: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['REVOKED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH2'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember1ValUnionMember0, ItemStateUnionMember1ValUnionMember1, ItemStateUnionMember1ValUnionMember2, ItemStateUnionMember1ValUnionMember3, ItemStateUnionMember1ValUnionMember4, ItemStateUnionMember1ValUnionMember5, ItemStateUnionMember1ValUnionMember6]


class ItemStateUnionMember2ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember2ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember2ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    basic_encoded: Optional[str] = None
    bearer_token: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    generic_api_key: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember2ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    basic_encoded: Optional[str] = None
    bearer_token: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    generic_api_key: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['API_KEY'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember2ValUnionMember0, ItemStateUnionMember2ValUnionMember1, ItemStateUnionMember2ValUnionMember2, ItemStateUnionMember2ValUnionMember3]


class ItemStateUnionMember3ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember3ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember3ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember3ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember3ValUnionMember0, ItemStateUnionMember3ValUnionMember1, ItemStateUnionMember3ValUnionMember2, ItemStateUnionMember3ValUnionMember3]


class ItemStateUnionMember4ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember4ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember4ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    token: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember4ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    token: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BEARER_TOKEN'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember4ValUnionMember0, ItemStateUnionMember4ValUnionMember1, ItemStateUnionMember4ValUnionMember2, ItemStateUnionMember4ValUnionMember3]


class ItemStateUnionMember5ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember5ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    composio_link_redirect_url: Optional[str] = None
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: str = Field(alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember5ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    credentials_json: str
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember5ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    credentials_json: str
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['GOOGLE_SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember5ValUnionMember0, ItemStateUnionMember5ValUnionMember1, ItemStateUnionMember5ValUnionMember2, ItemStateUnionMember5ValUnionMember3]


class ItemStateUnionMember6ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember6(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['NO_AUTH'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember6ValUnionMember0, ItemStateUnionMember6ValUnionMember1, ItemStateUnionMember6ValUnionMember2, ItemStateUnionMember6ValUnionMember3, ItemStateUnionMember6ValUnionMember4, ItemStateUnionMember6ValUnionMember5]


class ItemStateUnionMember7ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember7(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['CALCOM_AUTH'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember7ValUnionMember0, ItemStateUnionMember7ValUnionMember1, ItemStateUnionMember7ValUnionMember2, ItemStateUnionMember7ValUnionMember3, ItemStateUnionMember7ValUnionMember4, ItemStateUnionMember7ValUnionMember5]


class ItemStateUnionMember8ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: str = Field(alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    dev_key: str = Field(alias="devKey")
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    session_id: str = Field(alias="sessionId")
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    dev_key: str = Field(alias="devKey")
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    session_id: str = Field(alias="sessionId")
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember8(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BILLCOM_AUTH'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember8ValUnionMember0, ItemStateUnionMember8ValUnionMember1, ItemStateUnionMember8ValUnionMember2, ItemStateUnionMember8ValUnionMember3, ItemStateUnionMember8ValUnionMember4, ItemStateUnionMember8ValUnionMember5]


class ItemStateUnionMember9ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    password: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    username: str
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember9(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC_WITH_JWT'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember9ValUnionMember0, ItemStateUnionMember9ValUnionMember1, ItemStateUnionMember9ValUnionMember2, ItemStateUnionMember9ValUnionMember3, ItemStateUnionMember9ValUnionMember4, ItemStateUnionMember9ValUnionMember5]


class ItemStateUnionMember10ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember10ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember10ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    application_id: str
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    installation_id: str
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    private_key: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember10ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    application_id: str
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    installation_id: str
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    private_key: str
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember10(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember10ValUnionMember0, ItemStateUnionMember10ValUnionMember1, ItemStateUnionMember10ValUnionMember2, ItemStateUnionMember10ValUnionMember3]


class ItemStateUnionMember11ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember11(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SAML'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember11ValUnionMember0, ItemStateUnionMember11ValUnionMember1, ItemStateUnionMember11ValUnionMember2, ItemStateUnionMember11ValUnionMember3, ItemStateUnionMember11ValUnionMember4, ItemStateUnionMember11ValUnionMember5]


class ItemStateUnionMember12ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    callback_url: Optional[str] = None
    client_id: str
    "Dynamically registered client ID"
    client_id_issued_at: Optional[float] = None
    client_secret: Optional[str] = None
    "Dynamically registered client secret"
    client_secret_expires_at: Optional[float] = None
    code_verifier: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    final_redirect_uri: Optional[str] = Field(default=None, alias="finalRedirectUri")
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    redirect_url: str = Field(alias="redirectUrl")
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    client_id: str
    "Dynamically registered client ID"
    client_id_issued_at: Optional[float] = None
    client_secret: Optional[str] = None
    "Dynamically registered client secret"
    client_secret_expires_at: Optional[float] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    id_token: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    refresh_token: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    client_id: str
    "Dynamically registered client ID"
    client_id_issued_at: Optional[float] = None
    client_secret: Optional[str] = None
    "Dynamically registered client secret"
    client_secret_expires_at: Optional[float] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    id_token: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    refresh_token: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    long_redirect_url: Optional[bool] = None
    "Whether to return the redirect url without shortening"
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    state_prefix: Optional[str] = None
    "The oauth2 state prefix for the connection"
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember12(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['DCR_OAUTH'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember12ValUnionMember0, ItemStateUnionMember12ValUnionMember1, ItemStateUnionMember12ValUnionMember2, ItemStateUnionMember12ValUnionMember3, ItemStateUnionMember12ValUnionMember4, ItemStateUnionMember12ValUnionMember5]


class ItemStateUnionMember13ValUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIALIZING']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13ValUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INITIATED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_at: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['ACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expires_at: Optional[str] = None
    expires_in: Union[float, str, None] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    scope: Union[str, list[str], None] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['INACTIVE']
    subdomain: Optional[str] = None
    token_type: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13ValUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['FAILED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13ValUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    base_url: Optional[str] = None
    borneo_dashboard_url: Optional[str] = None
    companydomain: Optional[str] = Field(default=None, alias="COMPANYDOMAIN")
    dc: Optional[str] = None
    domain: Optional[str] = None
    expired_at: Optional[str] = None
    extension: Optional[str] = None
    form_api_base_url: Optional[str] = None
    instance_endpoint: Optional[str] = Field(default=None, alias="instanceEndpoint")
    instance_name: Optional[str] = Field(default=None, alias="instanceName")
    proxy_password: Optional[str] = None
    proxy_username: Optional[str] = None
    region: Optional[str] = None
    server_location: Optional[str] = None
    shop: Optional[str] = None
    site_name: Optional[str] = None
    status: Literal['EXPIRED']
    subdomain: Optional[str] = None
    version: Optional[str] = None
    your_domain: Optional[str] = Field(default=None, alias="your-domain")
    your_server: Optional[str] = None


class ItemStateUnionMember13(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['S2S_OAUTH2'] = Field(alias="authScheme")
    val: Union[ItemStateUnionMember13ValUnionMember0, ItemStateUnionMember13ValUnionMember1, ItemStateUnionMember13ValUnionMember2, ItemStateUnionMember13ValUnionMember3, ItemStateUnionMember13ValUnionMember4, ItemStateUnionMember13ValUnionMember5]


class ItemToolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    slug: str
    "The slug of the toolkit"


class Item(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    alias: Optional[str] = None
    "A user-defined alias for the connected account"
    auth_config: ItemAuthConfig
    created_at: str
    "The created at of the connection"
    data: Dict[str, Optional[object]]
    "This is deprecated, use `state` instead"
    deprecated: Optional[ItemDeprecated] = None
    experimental: Optional[ItemExperimental] = None
    "Experimental features - not stable, may be modified or removed in future\nversions."
    id: str
    "The id of the connection"
    is_disabled: bool
    "Whether the connection is disabled"
    state: Union[ItemStateUnionMember0, ItemStateUnionMember1, ItemStateUnionMember2, ItemStateUnionMember3, ItemStateUnionMember4, ItemStateUnionMember5, ItemStateUnionMember6, ItemStateUnionMember7, ItemStateUnionMember8, ItemStateUnionMember9, ItemStateUnionMember10, ItemStateUnionMember11, ItemStateUnionMember12, ItemStateUnionMember13]
    "The state of the connection"
    status: Literal['INITIALIZING', 'INITIATED', 'ACTIVE', 'FAILED', 'EXPIRED', 'INACTIVE', 'REVOKED']
    "The status of the connection"
    status_reason: Optional[str] = None
    "The reason the connection status changed.\n\nPossible reasons: Connection initiation did not complete within 10 minutes,\nPermanent auth error during token refresh, Max auth failures reached, OAuth\ncallback failed during token exchange, Connection status updated by user, Auth\nconfig is disabled, Revoked via user-initiated revoke endpoint, Revoked via\nadmin tool, Revoked as part of connection delete"
    test_request_endpoint: Optional[str] = None
    "The endpoint to make test request for verification"
    toolkit: ItemToolkit
    updated_at: str
    "The updated at of the connection"
    user_id: str
    "This is deprecated, we will not be providing userId from this api anymore, you\nwill only be able to read via userId not get it back"
    word_id: Optional[str] = None
    "A short, token-friendly identifier for multi-account disambiguation, typically\ntoolkit-prefixed with 1-2 words (e.g., \"gmail_red-castle\")"
    auth_scheme: Literal["OAUTH2", "OAUTH1", "API_KEY", "BASIC", "BILLCOM_AUTH", "BEARER_TOKEN", "GOOGLE_SERVICE_ACCOUNT", "NO_AUTH", "BASIC_WITH_JWT", "CALCOM_AUTH", "SERVICE_ACCOUNT", "SAML", "DCR_OAUTH", "CIMD_OAUTH", "S2S_OAUTH2"] | None = Field(default=None, alias="authScheme")


class ConnectedAccountListResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    current_page: float
    items: list[Item]
    next_cursor: Optional[str] = None
    total_items: float
    total_pages: float


ItemState: TypeAlias = Union[ItemStateUnionMember0, ItemStateUnionMember1, ItemStateUnionMember2, ItemStateUnionMember3, ItemStateUnionMember4, ItemStateUnionMember5, ItemStateUnionMember6, ItemStateUnionMember7, ItemStateUnionMember8, ItemStateUnionMember9, ItemStateUnionMember10, ItemStateUnionMember11, ItemStateUnionMember12, ItemStateUnionMember13]

ItemStateUnionMember0Val: TypeAlias = Union[ItemStateUnionMember0ValUnionMember0, ItemStateUnionMember0ValUnionMember1, ItemStateUnionMember0ValUnionMember2, ItemStateUnionMember0ValUnionMember3, ItemStateUnionMember0ValUnionMember4, ItemStateUnionMember0ValUnionMember5]

ItemStateUnionMember10Val: TypeAlias = Union[ItemStateUnionMember10ValUnionMember0, ItemStateUnionMember10ValUnionMember1, ItemStateUnionMember10ValUnionMember2, ItemStateUnionMember10ValUnionMember3]

ItemStateUnionMember11Val: TypeAlias = Union[ItemStateUnionMember11ValUnionMember0, ItemStateUnionMember11ValUnionMember1, ItemStateUnionMember11ValUnionMember2, ItemStateUnionMember11ValUnionMember3, ItemStateUnionMember11ValUnionMember4, ItemStateUnionMember11ValUnionMember5]

ItemStateUnionMember12Val: TypeAlias = Union[ItemStateUnionMember12ValUnionMember0, ItemStateUnionMember12ValUnionMember1, ItemStateUnionMember12ValUnionMember2, ItemStateUnionMember12ValUnionMember3, ItemStateUnionMember12ValUnionMember4, ItemStateUnionMember12ValUnionMember5]

ItemStateUnionMember13Val: TypeAlias = Union[ItemStateUnionMember13ValUnionMember0, ItemStateUnionMember13ValUnionMember1, ItemStateUnionMember13ValUnionMember2, ItemStateUnionMember13ValUnionMember3, ItemStateUnionMember13ValUnionMember4, ItemStateUnionMember13ValUnionMember5]

ItemStateUnionMember1Val: TypeAlias = Union[ItemStateUnionMember1ValUnionMember0, ItemStateUnionMember1ValUnionMember1, ItemStateUnionMember1ValUnionMember2, ItemStateUnionMember1ValUnionMember3, ItemStateUnionMember1ValUnionMember4, ItemStateUnionMember1ValUnionMember5, ItemStateUnionMember1ValUnionMember6]

ItemStateUnionMember2Val: TypeAlias = Union[ItemStateUnionMember2ValUnionMember0, ItemStateUnionMember2ValUnionMember1, ItemStateUnionMember2ValUnionMember2, ItemStateUnionMember2ValUnionMember3]

ItemStateUnionMember3Val: TypeAlias = Union[ItemStateUnionMember3ValUnionMember0, ItemStateUnionMember3ValUnionMember1, ItemStateUnionMember3ValUnionMember2, ItemStateUnionMember3ValUnionMember3]

ItemStateUnionMember4Val: TypeAlias = Union[ItemStateUnionMember4ValUnionMember0, ItemStateUnionMember4ValUnionMember1, ItemStateUnionMember4ValUnionMember2, ItemStateUnionMember4ValUnionMember3]

ItemStateUnionMember5Val: TypeAlias = Union[ItemStateUnionMember5ValUnionMember0, ItemStateUnionMember5ValUnionMember1, ItemStateUnionMember5ValUnionMember2, ItemStateUnionMember5ValUnionMember3]

ItemStateUnionMember6Val: TypeAlias = Union[ItemStateUnionMember6ValUnionMember0, ItemStateUnionMember6ValUnionMember1, ItemStateUnionMember6ValUnionMember2, ItemStateUnionMember6ValUnionMember3, ItemStateUnionMember6ValUnionMember4, ItemStateUnionMember6ValUnionMember5]

ItemStateUnionMember7Val: TypeAlias = Union[ItemStateUnionMember7ValUnionMember0, ItemStateUnionMember7ValUnionMember1, ItemStateUnionMember7ValUnionMember2, ItemStateUnionMember7ValUnionMember3, ItemStateUnionMember7ValUnionMember4, ItemStateUnionMember7ValUnionMember5]

ItemStateUnionMember8Val: TypeAlias = Union[ItemStateUnionMember8ValUnionMember0, ItemStateUnionMember8ValUnionMember1, ItemStateUnionMember8ValUnionMember2, ItemStateUnionMember8ValUnionMember3, ItemStateUnionMember8ValUnionMember4, ItemStateUnionMember8ValUnionMember5]

ItemStateUnionMember9Val: TypeAlias = Union[ItemStateUnionMember9ValUnionMember0, ItemStateUnionMember9ValUnionMember1, ItemStateUnionMember9ValUnionMember2, ItemStateUnionMember9ValUnionMember3, ItemStateUnionMember9ValUnionMember4, ItemStateUnionMember9ValUnionMember5]

__all__ = [
    "ConnectedAccountListResponse",
    "Item",
    "ItemAuthConfig",
    "ItemAuthConfigDeprecated",
    "ItemState",
    "ItemStateUnionMember0",
    "ItemStateUnionMember0Val",
    "ItemStateUnionMember0ValUnionMember0",
    "ItemStateUnionMember0ValUnionMember1",
    "ItemStateUnionMember0ValUnionMember2",
    "ItemStateUnionMember0ValUnionMember3",
    "ItemStateUnionMember0ValUnionMember4",
    "ItemStateUnionMember0ValUnionMember5",
    "ItemStateUnionMember1",
    "ItemStateUnionMember1Val",
    "ItemStateUnionMember1ValUnionMember0",
    "ItemStateUnionMember1ValUnionMember1",
    "ItemStateUnionMember1ValUnionMember2",
    "ItemStateUnionMember1ValUnionMember2AuthedUser",
    "ItemStateUnionMember1ValUnionMember3",
    "ItemStateUnionMember1ValUnionMember3AuthedUser",
    "ItemStateUnionMember1ValUnionMember4",
    "ItemStateUnionMember1ValUnionMember5",
    "ItemStateUnionMember1ValUnionMember6",
    "ItemStateUnionMember2",
    "ItemStateUnionMember2Val",
    "ItemStateUnionMember2ValUnionMember0",
    "ItemStateUnionMember2ValUnionMember1",
    "ItemStateUnionMember2ValUnionMember2",
    "ItemStateUnionMember2ValUnionMember3",
    "ItemStateUnionMember3",
    "ItemStateUnionMember3Val",
    "ItemStateUnionMember3ValUnionMember0",
    "ItemStateUnionMember3ValUnionMember1",
    "ItemStateUnionMember3ValUnionMember2",
    "ItemStateUnionMember3ValUnionMember3",
    "ItemStateUnionMember4",
    "ItemStateUnionMember4Val",
    "ItemStateUnionMember4ValUnionMember0",
    "ItemStateUnionMember4ValUnionMember1",
    "ItemStateUnionMember4ValUnionMember2",
    "ItemStateUnionMember4ValUnionMember3",
    "ItemStateUnionMember5",
    "ItemStateUnionMember5Val",
    "ItemStateUnionMember5ValUnionMember0",
    "ItemStateUnionMember5ValUnionMember1",
    "ItemStateUnionMember5ValUnionMember2",
    "ItemStateUnionMember5ValUnionMember3",
    "ItemStateUnionMember6",
    "ItemStateUnionMember6Val",
    "ItemStateUnionMember6ValUnionMember0",
    "ItemStateUnionMember6ValUnionMember1",
    "ItemStateUnionMember6ValUnionMember2",
    "ItemStateUnionMember6ValUnionMember3",
    "ItemStateUnionMember6ValUnionMember4",
    "ItemStateUnionMember6ValUnionMember5",
    "ItemStateUnionMember7",
    "ItemStateUnionMember7Val",
    "ItemStateUnionMember7ValUnionMember0",
    "ItemStateUnionMember7ValUnionMember1",
    "ItemStateUnionMember7ValUnionMember2",
    "ItemStateUnionMember7ValUnionMember3",
    "ItemStateUnionMember7ValUnionMember4",
    "ItemStateUnionMember7ValUnionMember5",
    "ItemStateUnionMember8",
    "ItemStateUnionMember8Val",
    "ItemStateUnionMember8ValUnionMember0",
    "ItemStateUnionMember8ValUnionMember1",
    "ItemStateUnionMember8ValUnionMember2",
    "ItemStateUnionMember8ValUnionMember3",
    "ItemStateUnionMember8ValUnionMember4",
    "ItemStateUnionMember8ValUnionMember5",
    "ItemStateUnionMember9",
    "ItemStateUnionMember9Val",
    "ItemStateUnionMember9ValUnionMember0",
    "ItemStateUnionMember9ValUnionMember1",
    "ItemStateUnionMember9ValUnionMember2",
    "ItemStateUnionMember9ValUnionMember3",
    "ItemStateUnionMember9ValUnionMember4",
    "ItemStateUnionMember9ValUnionMember5",
    "ItemStateUnionMember10",
    "ItemStateUnionMember10Val",
    "ItemStateUnionMember10ValUnionMember0",
    "ItemStateUnionMember10ValUnionMember1",
    "ItemStateUnionMember10ValUnionMember2",
    "ItemStateUnionMember10ValUnionMember3",
    "ItemStateUnionMember11",
    "ItemStateUnionMember11Val",
    "ItemStateUnionMember11ValUnionMember0",
    "ItemStateUnionMember11ValUnionMember1",
    "ItemStateUnionMember11ValUnionMember2",
    "ItemStateUnionMember11ValUnionMember3",
    "ItemStateUnionMember11ValUnionMember4",
    "ItemStateUnionMember11ValUnionMember5",
    "ItemStateUnionMember12",
    "ItemStateUnionMember12Val",
    "ItemStateUnionMember12ValUnionMember0",
    "ItemStateUnionMember12ValUnionMember1",
    "ItemStateUnionMember12ValUnionMember2",
    "ItemStateUnionMember12ValUnionMember3",
    "ItemStateUnionMember12ValUnionMember4",
    "ItemStateUnionMember12ValUnionMember5",
    "ItemStateUnionMember13",
    "ItemStateUnionMember13Val",
    "ItemStateUnionMember13ValUnionMember0",
    "ItemStateUnionMember13ValUnionMember1",
    "ItemStateUnionMember13ValUnionMember2",
    "ItemStateUnionMember13ValUnionMember3",
    "ItemStateUnionMember13ValUnionMember4",
    "ItemStateUnionMember13ValUnionMember5",
    "ItemToolkit",
    "ItemDeprecated",
    "ItemExperimental",
    "ItemExperimentalACLConfigForShared",
]
