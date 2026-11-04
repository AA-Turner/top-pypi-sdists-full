# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_retrieve_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class AuthConfigDeprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    uuid: str
    "The uuid of the auth config"


class AuthConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH2', 'OAUTH1', 'API_KEY', 'BASIC', 'BILLCOM_AUTH', 'BEARER_TOKEN', 'GOOGLE_SERVICE_ACCOUNT', 'NO_AUTH', 'BASIC_WITH_JWT', 'CALCOM_AUTH', 'SERVICE_ACCOUNT', 'SAML', 'DCR_OAUTH', 'S2S_OAUTH2']
    "the authScheme is part of the connection state use it there"
    deprecated: Optional[AuthConfigDeprecated] = None
    id: str
    "The id of the auth config"
    is_composio_managed: bool
    "Whether the auth config is managed by Composio"
    is_disabled: bool
    "Whether the auth config is disabled"


class Deprecated(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    labels: list[str]
    "The labels of the connection"
    uuid: str
    "The uuid of the connection"


class ExperimentalACLConfigForShared(BaseModel):
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers; non-creator cookie callers receive the response without this block."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allow_all_users: bool
    allowed_user_ids: list[str]
    not_allowed_user_ids: list[str]


class Experimental(BaseModel):
    "Experimental features - not stable, may be modified or removed in future versions."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    account_type: Literal['PRIVATE', 'SHARED']
    "Sharing model for this connected account.\n\nPRIVATE is usable only by the owning user_id. SHARED is reachable from a\ntool-router session only when explicitly pinned in the session config."
    acl_config_for_shared: Optional[ExperimentalACLConfigForShared] = None
    "Access control for SHARED connections.\n\nVisible only to the connection creator and project/org API key callers;\nnon-creator cookie callers receive the response without this block."


class StateUnionMember0ValUnionMember0(BaseModel):
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


class StateUnionMember0ValUnionMember1(BaseModel):
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


class StateUnionMember0ValUnionMember2(BaseModel):
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


class StateUnionMember0ValUnionMember3(BaseModel):
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


class StateUnionMember0ValUnionMember4(BaseModel):
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


class StateUnionMember0ValUnionMember5(BaseModel):
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


class StateUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH1'] = Field(alias="authScheme")
    val: Union[StateUnionMember0ValUnionMember0, StateUnionMember0ValUnionMember1, StateUnionMember0ValUnionMember2, StateUnionMember0ValUnionMember3, StateUnionMember0ValUnionMember4, StateUnionMember0ValUnionMember5]


class StateUnionMember1ValUnionMember0(BaseModel):
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


class StateUnionMember1ValUnionMember1(BaseModel):
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


class StateUnionMember1ValUnionMember2AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class StateUnionMember1ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[StateUnionMember1ValUnionMember2AuthedUser] = None
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


class StateUnionMember1ValUnionMember3AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class StateUnionMember1ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[StateUnionMember1ValUnionMember3AuthedUser] = None
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


class StateUnionMember1ValUnionMember4(BaseModel):
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


class StateUnionMember1ValUnionMember5(BaseModel):
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


class StateUnionMember1ValUnionMember6(BaseModel):
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


class StateUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH2'] = Field(alias="authScheme")
    val: Union[StateUnionMember1ValUnionMember0, StateUnionMember1ValUnionMember1, StateUnionMember1ValUnionMember2, StateUnionMember1ValUnionMember3, StateUnionMember1ValUnionMember4, StateUnionMember1ValUnionMember5, StateUnionMember1ValUnionMember6]


class StateUnionMember2ValUnionMember0(BaseModel):
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


class StateUnionMember2ValUnionMember1(BaseModel):
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


class StateUnionMember2ValUnionMember2(BaseModel):
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


class StateUnionMember2ValUnionMember3(BaseModel):
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


class StateUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['API_KEY'] = Field(alias="authScheme")
    val: Union[StateUnionMember2ValUnionMember0, StateUnionMember2ValUnionMember1, StateUnionMember2ValUnionMember2, StateUnionMember2ValUnionMember3]


class StateUnionMember3ValUnionMember0(BaseModel):
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


class StateUnionMember3ValUnionMember1(BaseModel):
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


class StateUnionMember3ValUnionMember2(BaseModel):
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


class StateUnionMember3ValUnionMember3(BaseModel):
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


class StateUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC'] = Field(alias="authScheme")
    val: Union[StateUnionMember3ValUnionMember0, StateUnionMember3ValUnionMember1, StateUnionMember3ValUnionMember2, StateUnionMember3ValUnionMember3]


class StateUnionMember4ValUnionMember0(BaseModel):
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


class StateUnionMember4ValUnionMember1(BaseModel):
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


class StateUnionMember4ValUnionMember2(BaseModel):
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


class StateUnionMember4ValUnionMember3(BaseModel):
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


class StateUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BEARER_TOKEN'] = Field(alias="authScheme")
    val: Union[StateUnionMember4ValUnionMember0, StateUnionMember4ValUnionMember1, StateUnionMember4ValUnionMember2, StateUnionMember4ValUnionMember3]


class StateUnionMember5ValUnionMember0(BaseModel):
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


class StateUnionMember5ValUnionMember1(BaseModel):
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


class StateUnionMember5ValUnionMember2(BaseModel):
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


class StateUnionMember5ValUnionMember3(BaseModel):
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


class StateUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['GOOGLE_SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[StateUnionMember5ValUnionMember0, StateUnionMember5ValUnionMember1, StateUnionMember5ValUnionMember2, StateUnionMember5ValUnionMember3]


class StateUnionMember6ValUnionMember0(BaseModel):
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


class StateUnionMember6ValUnionMember1(BaseModel):
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


class StateUnionMember6ValUnionMember2(BaseModel):
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


class StateUnionMember6ValUnionMember3(BaseModel):
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


class StateUnionMember6ValUnionMember4(BaseModel):
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


class StateUnionMember6ValUnionMember5(BaseModel):
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


class StateUnionMember6(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['NO_AUTH'] = Field(alias="authScheme")
    val: Union[StateUnionMember6ValUnionMember0, StateUnionMember6ValUnionMember1, StateUnionMember6ValUnionMember2, StateUnionMember6ValUnionMember3, StateUnionMember6ValUnionMember4, StateUnionMember6ValUnionMember5]


class StateUnionMember7ValUnionMember0(BaseModel):
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


class StateUnionMember7ValUnionMember1(BaseModel):
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


class StateUnionMember7ValUnionMember2(BaseModel):
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


class StateUnionMember7ValUnionMember3(BaseModel):
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


class StateUnionMember7ValUnionMember4(BaseModel):
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


class StateUnionMember7ValUnionMember5(BaseModel):
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


class StateUnionMember7(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['CALCOM_AUTH'] = Field(alias="authScheme")
    val: Union[StateUnionMember7ValUnionMember0, StateUnionMember7ValUnionMember1, StateUnionMember7ValUnionMember2, StateUnionMember7ValUnionMember3, StateUnionMember7ValUnionMember4, StateUnionMember7ValUnionMember5]


class StateUnionMember8ValUnionMember0(BaseModel):
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


class StateUnionMember8ValUnionMember1(BaseModel):
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


class StateUnionMember8ValUnionMember2(BaseModel):
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


class StateUnionMember8ValUnionMember3(BaseModel):
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


class StateUnionMember8ValUnionMember4(BaseModel):
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


class StateUnionMember8ValUnionMember5(BaseModel):
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


class StateUnionMember8(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BILLCOM_AUTH'] = Field(alias="authScheme")
    val: Union[StateUnionMember8ValUnionMember0, StateUnionMember8ValUnionMember1, StateUnionMember8ValUnionMember2, StateUnionMember8ValUnionMember3, StateUnionMember8ValUnionMember4, StateUnionMember8ValUnionMember5]


class StateUnionMember9ValUnionMember0(BaseModel):
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


class StateUnionMember9ValUnionMember1(BaseModel):
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


class StateUnionMember9ValUnionMember2(BaseModel):
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


class StateUnionMember9ValUnionMember3(BaseModel):
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


class StateUnionMember9ValUnionMember4(BaseModel):
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


class StateUnionMember9ValUnionMember5(BaseModel):
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


class StateUnionMember9(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC_WITH_JWT'] = Field(alias="authScheme")
    val: Union[StateUnionMember9ValUnionMember0, StateUnionMember9ValUnionMember1, StateUnionMember9ValUnionMember2, StateUnionMember9ValUnionMember3, StateUnionMember9ValUnionMember4, StateUnionMember9ValUnionMember5]


class StateUnionMember10ValUnionMember0(BaseModel):
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


class StateUnionMember10ValUnionMember1(BaseModel):
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


class StateUnionMember10ValUnionMember2(BaseModel):
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


class StateUnionMember10ValUnionMember3(BaseModel):
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


class StateUnionMember10(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[StateUnionMember10ValUnionMember0, StateUnionMember10ValUnionMember1, StateUnionMember10ValUnionMember2, StateUnionMember10ValUnionMember3]


class StateUnionMember11ValUnionMember0(BaseModel):
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


class StateUnionMember11ValUnionMember1(BaseModel):
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


class StateUnionMember11ValUnionMember2(BaseModel):
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


class StateUnionMember11ValUnionMember3(BaseModel):
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


class StateUnionMember11ValUnionMember4(BaseModel):
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


class StateUnionMember11ValUnionMember5(BaseModel):
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


class StateUnionMember11(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SAML'] = Field(alias="authScheme")
    val: Union[StateUnionMember11ValUnionMember0, StateUnionMember11ValUnionMember1, StateUnionMember11ValUnionMember2, StateUnionMember11ValUnionMember3, StateUnionMember11ValUnionMember4, StateUnionMember11ValUnionMember5]


class StateUnionMember12ValUnionMember0(BaseModel):
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


class StateUnionMember12ValUnionMember1(BaseModel):
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


class StateUnionMember12ValUnionMember2(BaseModel):
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


class StateUnionMember12ValUnionMember3(BaseModel):
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


class StateUnionMember12ValUnionMember4(BaseModel):
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


class StateUnionMember12ValUnionMember5(BaseModel):
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


class StateUnionMember12(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['DCR_OAUTH'] = Field(alias="authScheme")
    val: Union[StateUnionMember12ValUnionMember0, StateUnionMember12ValUnionMember1, StateUnionMember12ValUnionMember2, StateUnionMember12ValUnionMember3, StateUnionMember12ValUnionMember4, StateUnionMember12ValUnionMember5]


class StateUnionMember13ValUnionMember0(BaseModel):
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


class StateUnionMember13ValUnionMember1(BaseModel):
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


class StateUnionMember13ValUnionMember2(BaseModel):
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


class StateUnionMember13ValUnionMember3(BaseModel):
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


class StateUnionMember13ValUnionMember4(BaseModel):
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


class StateUnionMember13ValUnionMember5(BaseModel):
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


class StateUnionMember13(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['S2S_OAUTH2'] = Field(alias="authScheme")
    val: Union[StateUnionMember13ValUnionMember0, StateUnionMember13ValUnionMember1, StateUnionMember13ValUnionMember2, StateUnionMember13ValUnionMember3, StateUnionMember13ValUnionMember4, StateUnionMember13ValUnionMember5]


class Toolkit(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    slug: str
    "The slug of the toolkit"


class ConnectedAccountRetrieveResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    alias: Optional[str] = None
    "A user-defined alias for the connected account"
    auth_config: AuthConfig
    created_at: str
    "The created at of the connection"
    data: Dict[str, Optional[object]]
    "This is deprecated, use `state` instead"
    deprecated: Optional[Deprecated] = None
    experimental: Optional[Experimental] = None
    "Experimental features - not stable, may be modified or removed in future\nversions."
    id: str
    "The id of the connection"
    is_disabled: bool
    "Whether the connection is disabled"
    params: Dict[str, Optional[object]]
    "The initialization data of the connection, including configuration parameters"
    requested_scopes: Optional[list[str]] = None
    "OAuth scopes requested when this connection was most recently initiated (create\nor refresh). Absent for connections created before scope snapshots were captured\nand for non-OAuth auth schemes."
    requested_user_scopes: Optional[list[str]] = None
    "OAuth user-token scopes requested at the most recent initiation.\n\nOnly meaningful for Slackbot auth configs (user-token scopes); absent otherwise."
    state: Union[StateUnionMember0, StateUnionMember1, StateUnionMember2, StateUnionMember3, StateUnionMember4, StateUnionMember5, StateUnionMember6, StateUnionMember7, StateUnionMember8, StateUnionMember9, StateUnionMember10, StateUnionMember11, StateUnionMember12, StateUnionMember13]
    "The state of the connection"
    status: Literal['INITIALIZING', 'INITIATED', 'ACTIVE', 'FAILED', 'EXPIRED', 'INACTIVE', 'REVOKED']
    "The status of the connection"
    status_reason: Optional[str] = None
    "The reason the connection status changed.\n\nPossible reasons: Connection initiation did not complete within 10 minutes,\nPermanent auth error during token refresh, Max auth failures reached, OAuth\ncallback failed during token exchange, Connection status updated by user, Auth\nconfig is disabled, Revoked via user-initiated revoke endpoint, Revoked via\nadmin tool, Revoked as part of connection delete"
    test_request_endpoint: Optional[str] = None
    "The endpoint to make test request for verification"
    toolkit: Toolkit
    updated_at: str
    "The updated at of the connection"
    user_id: str
    "This is deprecated, we will not be providing userId from this api anymore, you\nwill only be able to read via userId not get it back"
    word_id: Optional[str] = None
    "A short, token-friendly identifier for multi-account disambiguation, typically\ntoolkit-prefixed with 1-2 words (e.g., \"gmail_red-castle\")"
    auth_scheme: Literal["OAUTH2", "OAUTH1", "API_KEY", "BASIC", "BILLCOM_AUTH", "BEARER_TOKEN", "GOOGLE_SERVICE_ACCOUNT", "NO_AUTH", "BASIC_WITH_JWT", "CALCOM_AUTH", "SERVICE_ACCOUNT", "SAML", "DCR_OAUTH", "CIMD_OAUTH", "S2S_OAUTH2"] | None = Field(default=None, alias="authScheme")


State: TypeAlias = Union[StateUnionMember0, StateUnionMember1, StateUnionMember2, StateUnionMember3, StateUnionMember4, StateUnionMember5, StateUnionMember6, StateUnionMember7, StateUnionMember8, StateUnionMember9, StateUnionMember10, StateUnionMember11, StateUnionMember12, StateUnionMember13]

StateUnionMember0Val: TypeAlias = Union[StateUnionMember0ValUnionMember0, StateUnionMember0ValUnionMember1, StateUnionMember0ValUnionMember2, StateUnionMember0ValUnionMember3, StateUnionMember0ValUnionMember4, StateUnionMember0ValUnionMember5]

StateUnionMember10Val: TypeAlias = Union[StateUnionMember10ValUnionMember0, StateUnionMember10ValUnionMember1, StateUnionMember10ValUnionMember2, StateUnionMember10ValUnionMember3]

StateUnionMember11Val: TypeAlias = Union[StateUnionMember11ValUnionMember0, StateUnionMember11ValUnionMember1, StateUnionMember11ValUnionMember2, StateUnionMember11ValUnionMember3, StateUnionMember11ValUnionMember4, StateUnionMember11ValUnionMember5]

StateUnionMember12Val: TypeAlias = Union[StateUnionMember12ValUnionMember0, StateUnionMember12ValUnionMember1, StateUnionMember12ValUnionMember2, StateUnionMember12ValUnionMember3, StateUnionMember12ValUnionMember4, StateUnionMember12ValUnionMember5]

StateUnionMember13Val: TypeAlias = Union[StateUnionMember13ValUnionMember0, StateUnionMember13ValUnionMember1, StateUnionMember13ValUnionMember2, StateUnionMember13ValUnionMember3, StateUnionMember13ValUnionMember4, StateUnionMember13ValUnionMember5]

StateUnionMember1Val: TypeAlias = Union[StateUnionMember1ValUnionMember0, StateUnionMember1ValUnionMember1, StateUnionMember1ValUnionMember2, StateUnionMember1ValUnionMember3, StateUnionMember1ValUnionMember4, StateUnionMember1ValUnionMember5, StateUnionMember1ValUnionMember6]

StateUnionMember2Val: TypeAlias = Union[StateUnionMember2ValUnionMember0, StateUnionMember2ValUnionMember1, StateUnionMember2ValUnionMember2, StateUnionMember2ValUnionMember3]

StateUnionMember3Val: TypeAlias = Union[StateUnionMember3ValUnionMember0, StateUnionMember3ValUnionMember1, StateUnionMember3ValUnionMember2, StateUnionMember3ValUnionMember3]

StateUnionMember4Val: TypeAlias = Union[StateUnionMember4ValUnionMember0, StateUnionMember4ValUnionMember1, StateUnionMember4ValUnionMember2, StateUnionMember4ValUnionMember3]

StateUnionMember5Val: TypeAlias = Union[StateUnionMember5ValUnionMember0, StateUnionMember5ValUnionMember1, StateUnionMember5ValUnionMember2, StateUnionMember5ValUnionMember3]

StateUnionMember6Val: TypeAlias = Union[StateUnionMember6ValUnionMember0, StateUnionMember6ValUnionMember1, StateUnionMember6ValUnionMember2, StateUnionMember6ValUnionMember3, StateUnionMember6ValUnionMember4, StateUnionMember6ValUnionMember5]

StateUnionMember7Val: TypeAlias = Union[StateUnionMember7ValUnionMember0, StateUnionMember7ValUnionMember1, StateUnionMember7ValUnionMember2, StateUnionMember7ValUnionMember3, StateUnionMember7ValUnionMember4, StateUnionMember7ValUnionMember5]

StateUnionMember8Val: TypeAlias = Union[StateUnionMember8ValUnionMember0, StateUnionMember8ValUnionMember1, StateUnionMember8ValUnionMember2, StateUnionMember8ValUnionMember3, StateUnionMember8ValUnionMember4, StateUnionMember8ValUnionMember5]

StateUnionMember9Val: TypeAlias = Union[StateUnionMember9ValUnionMember0, StateUnionMember9ValUnionMember1, StateUnionMember9ValUnionMember2, StateUnionMember9ValUnionMember3, StateUnionMember9ValUnionMember4, StateUnionMember9ValUnionMember5]

__all__ = [
    "ConnectedAccountRetrieveResponse",
    "AuthConfig",
    "AuthConfigDeprecated",
    "State",
    "StateUnionMember0",
    "StateUnionMember0Val",
    "StateUnionMember0ValUnionMember0",
    "StateUnionMember0ValUnionMember1",
    "StateUnionMember0ValUnionMember2",
    "StateUnionMember0ValUnionMember3",
    "StateUnionMember0ValUnionMember4",
    "StateUnionMember0ValUnionMember5",
    "StateUnionMember1",
    "StateUnionMember1Val",
    "StateUnionMember1ValUnionMember0",
    "StateUnionMember1ValUnionMember1",
    "StateUnionMember1ValUnionMember2",
    "StateUnionMember1ValUnionMember2AuthedUser",
    "StateUnionMember1ValUnionMember3",
    "StateUnionMember1ValUnionMember3AuthedUser",
    "StateUnionMember1ValUnionMember4",
    "StateUnionMember1ValUnionMember5",
    "StateUnionMember1ValUnionMember6",
    "StateUnionMember2",
    "StateUnionMember2Val",
    "StateUnionMember2ValUnionMember0",
    "StateUnionMember2ValUnionMember1",
    "StateUnionMember2ValUnionMember2",
    "StateUnionMember2ValUnionMember3",
    "StateUnionMember3",
    "StateUnionMember3Val",
    "StateUnionMember3ValUnionMember0",
    "StateUnionMember3ValUnionMember1",
    "StateUnionMember3ValUnionMember2",
    "StateUnionMember3ValUnionMember3",
    "StateUnionMember4",
    "StateUnionMember4Val",
    "StateUnionMember4ValUnionMember0",
    "StateUnionMember4ValUnionMember1",
    "StateUnionMember4ValUnionMember2",
    "StateUnionMember4ValUnionMember3",
    "StateUnionMember5",
    "StateUnionMember5Val",
    "StateUnionMember5ValUnionMember0",
    "StateUnionMember5ValUnionMember1",
    "StateUnionMember5ValUnionMember2",
    "StateUnionMember5ValUnionMember3",
    "StateUnionMember6",
    "StateUnionMember6Val",
    "StateUnionMember6ValUnionMember0",
    "StateUnionMember6ValUnionMember1",
    "StateUnionMember6ValUnionMember2",
    "StateUnionMember6ValUnionMember3",
    "StateUnionMember6ValUnionMember4",
    "StateUnionMember6ValUnionMember5",
    "StateUnionMember7",
    "StateUnionMember7Val",
    "StateUnionMember7ValUnionMember0",
    "StateUnionMember7ValUnionMember1",
    "StateUnionMember7ValUnionMember2",
    "StateUnionMember7ValUnionMember3",
    "StateUnionMember7ValUnionMember4",
    "StateUnionMember7ValUnionMember5",
    "StateUnionMember8",
    "StateUnionMember8Val",
    "StateUnionMember8ValUnionMember0",
    "StateUnionMember8ValUnionMember1",
    "StateUnionMember8ValUnionMember2",
    "StateUnionMember8ValUnionMember3",
    "StateUnionMember8ValUnionMember4",
    "StateUnionMember8ValUnionMember5",
    "StateUnionMember9",
    "StateUnionMember9Val",
    "StateUnionMember9ValUnionMember0",
    "StateUnionMember9ValUnionMember1",
    "StateUnionMember9ValUnionMember2",
    "StateUnionMember9ValUnionMember3",
    "StateUnionMember9ValUnionMember4",
    "StateUnionMember9ValUnionMember5",
    "StateUnionMember10",
    "StateUnionMember10Val",
    "StateUnionMember10ValUnionMember0",
    "StateUnionMember10ValUnionMember1",
    "StateUnionMember10ValUnionMember2",
    "StateUnionMember10ValUnionMember3",
    "StateUnionMember11",
    "StateUnionMember11Val",
    "StateUnionMember11ValUnionMember0",
    "StateUnionMember11ValUnionMember1",
    "StateUnionMember11ValUnionMember2",
    "StateUnionMember11ValUnionMember3",
    "StateUnionMember11ValUnionMember4",
    "StateUnionMember11ValUnionMember5",
    "StateUnionMember12",
    "StateUnionMember12Val",
    "StateUnionMember12ValUnionMember0",
    "StateUnionMember12ValUnionMember1",
    "StateUnionMember12ValUnionMember2",
    "StateUnionMember12ValUnionMember3",
    "StateUnionMember12ValUnionMember4",
    "StateUnionMember12ValUnionMember5",
    "StateUnionMember13",
    "StateUnionMember13Val",
    "StateUnionMember13ValUnionMember0",
    "StateUnionMember13ValUnionMember1",
    "StateUnionMember13ValUnionMember2",
    "StateUnionMember13ValUnionMember3",
    "StateUnionMember13ValUnionMember4",
    "StateUnionMember13ValUnionMember5",
    "Toolkit",
    "Deprecated",
    "Experimental",
    "ExperimentalACLConfigForShared",
]
