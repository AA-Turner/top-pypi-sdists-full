# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.connected_account_create_response."""

from __future__ import annotations

from typing import Dict, Literal, Optional, TypeAlias, Union

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class ConnectionDataUnionMember0ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember0ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember0ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember0ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember0ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember0ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember0(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH1'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember0ValUnionMember0, ConnectionDataUnionMember0ValUnionMember1, ConnectionDataUnionMember0ValUnionMember2, ConnectionDataUnionMember0ValUnionMember3, ConnectionDataUnionMember0ValUnionMember4, ConnectionDataUnionMember0ValUnionMember5]


class ConnectionDataUnionMember1ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember1ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember1ValUnionMember2AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class ConnectionDataUnionMember1ValUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[ConnectionDataUnionMember1ValUnionMember2AuthedUser] = None
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


class ConnectionDataUnionMember1ValUnionMember3AuthedUser(BaseModel):
    "for slack user scopes"

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: Optional[str] = None
    scope: Optional[str] = None


class ConnectionDataUnionMember1ValUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    access_token: str
    account_id: Optional[str] = None
    account_url: Optional[str] = None
    api_url: Optional[str] = None
    authed_user: Optional[ConnectionDataUnionMember1ValUnionMember3AuthedUser] = None
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


class ConnectionDataUnionMember1ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember1ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember1ValUnionMember6(BaseModel):
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


class ConnectionDataUnionMember1(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['OAUTH2'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember1ValUnionMember0, ConnectionDataUnionMember1ValUnionMember1, ConnectionDataUnionMember1ValUnionMember2, ConnectionDataUnionMember1ValUnionMember3, ConnectionDataUnionMember1ValUnionMember4, ConnectionDataUnionMember1ValUnionMember5, ConnectionDataUnionMember1ValUnionMember6]


class ConnectionDataUnionMember2ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember2ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember2ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember2ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember2(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['API_KEY'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember2ValUnionMember0, ConnectionDataUnionMember2ValUnionMember1, ConnectionDataUnionMember2ValUnionMember2, ConnectionDataUnionMember2ValUnionMember3]


class ConnectionDataUnionMember3ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember3ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember3ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember3ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember3(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember3ValUnionMember0, ConnectionDataUnionMember3ValUnionMember1, ConnectionDataUnionMember3ValUnionMember2, ConnectionDataUnionMember3ValUnionMember3]


class ConnectionDataUnionMember4ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember4ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember4ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember4ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember4(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BEARER_TOKEN'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember4ValUnionMember0, ConnectionDataUnionMember4ValUnionMember1, ConnectionDataUnionMember4ValUnionMember2, ConnectionDataUnionMember4ValUnionMember3]


class ConnectionDataUnionMember5ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember5ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember5ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember5ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember5(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['GOOGLE_SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember5ValUnionMember0, ConnectionDataUnionMember5ValUnionMember1, ConnectionDataUnionMember5ValUnionMember2, ConnectionDataUnionMember5ValUnionMember3]


class ConnectionDataUnionMember6ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember6ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember6ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember6ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember6ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember6ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember6(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['NO_AUTH'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember6ValUnionMember0, ConnectionDataUnionMember6ValUnionMember1, ConnectionDataUnionMember6ValUnionMember2, ConnectionDataUnionMember6ValUnionMember3, ConnectionDataUnionMember6ValUnionMember4, ConnectionDataUnionMember6ValUnionMember5]


class ConnectionDataUnionMember7ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember7ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember7ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember7ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember7ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember7ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember7(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['CALCOM_AUTH'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember7ValUnionMember0, ConnectionDataUnionMember7ValUnionMember1, ConnectionDataUnionMember7ValUnionMember2, ConnectionDataUnionMember7ValUnionMember3, ConnectionDataUnionMember7ValUnionMember4, ConnectionDataUnionMember7ValUnionMember5]


class ConnectionDataUnionMember8ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember8ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember8ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember8ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember8ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember8ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember8(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BILLCOM_AUTH'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember8ValUnionMember0, ConnectionDataUnionMember8ValUnionMember1, ConnectionDataUnionMember8ValUnionMember2, ConnectionDataUnionMember8ValUnionMember3, ConnectionDataUnionMember8ValUnionMember4, ConnectionDataUnionMember8ValUnionMember5]


class ConnectionDataUnionMember9ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember9ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember9ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember9ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember9ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember9ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember9(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['BASIC_WITH_JWT'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember9ValUnionMember0, ConnectionDataUnionMember9ValUnionMember1, ConnectionDataUnionMember9ValUnionMember2, ConnectionDataUnionMember9ValUnionMember3, ConnectionDataUnionMember9ValUnionMember4, ConnectionDataUnionMember9ValUnionMember5]


class ConnectionDataUnionMember10ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember10ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember10ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember10ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember10(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SERVICE_ACCOUNT'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember10ValUnionMember0, ConnectionDataUnionMember10ValUnionMember1, ConnectionDataUnionMember10ValUnionMember2, ConnectionDataUnionMember10ValUnionMember3]


class ConnectionDataUnionMember11ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember11ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember11ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember11ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember11ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember11ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember11(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['SAML'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember11ValUnionMember0, ConnectionDataUnionMember11ValUnionMember1, ConnectionDataUnionMember11ValUnionMember2, ConnectionDataUnionMember11ValUnionMember3, ConnectionDataUnionMember11ValUnionMember4, ConnectionDataUnionMember11ValUnionMember5]


class ConnectionDataUnionMember12ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember12ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember12ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember12ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember12ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember12ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember12(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['DCR_OAUTH'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember12ValUnionMember0, ConnectionDataUnionMember12ValUnionMember1, ConnectionDataUnionMember12ValUnionMember2, ConnectionDataUnionMember12ValUnionMember3, ConnectionDataUnionMember12ValUnionMember4, ConnectionDataUnionMember12ValUnionMember5]


class ConnectionDataUnionMember13ValUnionMember0(BaseModel):
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


class ConnectionDataUnionMember13ValUnionMember1(BaseModel):
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


class ConnectionDataUnionMember13ValUnionMember2(BaseModel):
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


class ConnectionDataUnionMember13ValUnionMember3(BaseModel):
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


class ConnectionDataUnionMember13ValUnionMember4(BaseModel):
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


class ConnectionDataUnionMember13ValUnionMember5(BaseModel):
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


class ConnectionDataUnionMember13(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_scheme: Literal['S2S_OAUTH2'] = Field(alias="authScheme")
    val: Union[ConnectionDataUnionMember13ValUnionMember0, ConnectionDataUnionMember13ValUnionMember1, ConnectionDataUnionMember13ValUnionMember2, ConnectionDataUnionMember13ValUnionMember3, ConnectionDataUnionMember13ValUnionMember4, ConnectionDataUnionMember13ValUnionMember5]


class Deprecated(BaseModel):
    "DEPRECATED: This field will be removed in a future version.\n\nPlease use id and auth_config.id instead."

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    auth_config_uuid: str = Field(alias="authConfigUuid")
    "The uuid of the auth config"
    uuid: str
    "The uuid of the connected account"


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


class ConnectedAccountCreateResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    connection_data: Union[ConnectionDataUnionMember0, ConnectionDataUnionMember1, ConnectionDataUnionMember2, ConnectionDataUnionMember3, ConnectionDataUnionMember4, ConnectionDataUnionMember5, ConnectionDataUnionMember6, ConnectionDataUnionMember7, ConnectionDataUnionMember8, ConnectionDataUnionMember9, ConnectionDataUnionMember10, ConnectionDataUnionMember11, ConnectionDataUnionMember12, ConnectionDataUnionMember13] = Field(alias="connectionData")
    "The connection data of the connected account"
    deprecated: Optional[Deprecated] = None
    "DEPRECATED: This field will be removed in a future version.\n\nPlease use id and auth_config.id instead."
    experimental: Optional[Experimental] = None
    "Experimental features - not stable, may be modified or removed in future\nversions."
    id: str
    "The id of the connected account"
    redirect_uri: Optional[str] = None
    "DEPRECATED: This field will be removed in a future version"
    redirect_url: Optional[str] = None
    "DEPRECATED: This field will be removed in a future version"
    status: Literal['INITIALIZING', 'INITIATED', 'ACTIVE', 'FAILED', 'EXPIRED', 'INACTIVE', 'REVOKED']
    "DEPRECATED: This field will be removed in a future version"


ConnectionData: TypeAlias = Union[ConnectionDataUnionMember0, ConnectionDataUnionMember1, ConnectionDataUnionMember2, ConnectionDataUnionMember3, ConnectionDataUnionMember4, ConnectionDataUnionMember5, ConnectionDataUnionMember6, ConnectionDataUnionMember7, ConnectionDataUnionMember8, ConnectionDataUnionMember9, ConnectionDataUnionMember10, ConnectionDataUnionMember11, ConnectionDataUnionMember12, ConnectionDataUnionMember13]

ConnectionDataUnionMember0Val: TypeAlias = Union[ConnectionDataUnionMember0ValUnionMember0, ConnectionDataUnionMember0ValUnionMember1, ConnectionDataUnionMember0ValUnionMember2, ConnectionDataUnionMember0ValUnionMember3, ConnectionDataUnionMember0ValUnionMember4, ConnectionDataUnionMember0ValUnionMember5]

ConnectionDataUnionMember10Val: TypeAlias = Union[ConnectionDataUnionMember10ValUnionMember0, ConnectionDataUnionMember10ValUnionMember1, ConnectionDataUnionMember10ValUnionMember2, ConnectionDataUnionMember10ValUnionMember3]

ConnectionDataUnionMember11Val: TypeAlias = Union[ConnectionDataUnionMember11ValUnionMember0, ConnectionDataUnionMember11ValUnionMember1, ConnectionDataUnionMember11ValUnionMember2, ConnectionDataUnionMember11ValUnionMember3, ConnectionDataUnionMember11ValUnionMember4, ConnectionDataUnionMember11ValUnionMember5]

ConnectionDataUnionMember12Val: TypeAlias = Union[ConnectionDataUnionMember12ValUnionMember0, ConnectionDataUnionMember12ValUnionMember1, ConnectionDataUnionMember12ValUnionMember2, ConnectionDataUnionMember12ValUnionMember3, ConnectionDataUnionMember12ValUnionMember4, ConnectionDataUnionMember12ValUnionMember5]

ConnectionDataUnionMember13Val: TypeAlias = Union[ConnectionDataUnionMember13ValUnionMember0, ConnectionDataUnionMember13ValUnionMember1, ConnectionDataUnionMember13ValUnionMember2, ConnectionDataUnionMember13ValUnionMember3, ConnectionDataUnionMember13ValUnionMember4, ConnectionDataUnionMember13ValUnionMember5]

ConnectionDataUnionMember1Val: TypeAlias = Union[ConnectionDataUnionMember1ValUnionMember0, ConnectionDataUnionMember1ValUnionMember1, ConnectionDataUnionMember1ValUnionMember2, ConnectionDataUnionMember1ValUnionMember3, ConnectionDataUnionMember1ValUnionMember4, ConnectionDataUnionMember1ValUnionMember5, ConnectionDataUnionMember1ValUnionMember6]

ConnectionDataUnionMember2Val: TypeAlias = Union[ConnectionDataUnionMember2ValUnionMember0, ConnectionDataUnionMember2ValUnionMember1, ConnectionDataUnionMember2ValUnionMember2, ConnectionDataUnionMember2ValUnionMember3]

ConnectionDataUnionMember3Val: TypeAlias = Union[ConnectionDataUnionMember3ValUnionMember0, ConnectionDataUnionMember3ValUnionMember1, ConnectionDataUnionMember3ValUnionMember2, ConnectionDataUnionMember3ValUnionMember3]

ConnectionDataUnionMember4Val: TypeAlias = Union[ConnectionDataUnionMember4ValUnionMember0, ConnectionDataUnionMember4ValUnionMember1, ConnectionDataUnionMember4ValUnionMember2, ConnectionDataUnionMember4ValUnionMember3]

ConnectionDataUnionMember5Val: TypeAlias = Union[ConnectionDataUnionMember5ValUnionMember0, ConnectionDataUnionMember5ValUnionMember1, ConnectionDataUnionMember5ValUnionMember2, ConnectionDataUnionMember5ValUnionMember3]

ConnectionDataUnionMember6Val: TypeAlias = Union[ConnectionDataUnionMember6ValUnionMember0, ConnectionDataUnionMember6ValUnionMember1, ConnectionDataUnionMember6ValUnionMember2, ConnectionDataUnionMember6ValUnionMember3, ConnectionDataUnionMember6ValUnionMember4, ConnectionDataUnionMember6ValUnionMember5]

ConnectionDataUnionMember7Val: TypeAlias = Union[ConnectionDataUnionMember7ValUnionMember0, ConnectionDataUnionMember7ValUnionMember1, ConnectionDataUnionMember7ValUnionMember2, ConnectionDataUnionMember7ValUnionMember3, ConnectionDataUnionMember7ValUnionMember4, ConnectionDataUnionMember7ValUnionMember5]

ConnectionDataUnionMember8Val: TypeAlias = Union[ConnectionDataUnionMember8ValUnionMember0, ConnectionDataUnionMember8ValUnionMember1, ConnectionDataUnionMember8ValUnionMember2, ConnectionDataUnionMember8ValUnionMember3, ConnectionDataUnionMember8ValUnionMember4, ConnectionDataUnionMember8ValUnionMember5]

ConnectionDataUnionMember9Val: TypeAlias = Union[ConnectionDataUnionMember9ValUnionMember0, ConnectionDataUnionMember9ValUnionMember1, ConnectionDataUnionMember9ValUnionMember2, ConnectionDataUnionMember9ValUnionMember3, ConnectionDataUnionMember9ValUnionMember4, ConnectionDataUnionMember9ValUnionMember5]

__all__ = [
    "ConnectedAccountCreateResponse",
    "ConnectionData",
    "ConnectionDataUnionMember0",
    "ConnectionDataUnionMember0Val",
    "ConnectionDataUnionMember0ValUnionMember0",
    "ConnectionDataUnionMember0ValUnionMember1",
    "ConnectionDataUnionMember0ValUnionMember2",
    "ConnectionDataUnionMember0ValUnionMember3",
    "ConnectionDataUnionMember0ValUnionMember4",
    "ConnectionDataUnionMember0ValUnionMember5",
    "ConnectionDataUnionMember1",
    "ConnectionDataUnionMember1Val",
    "ConnectionDataUnionMember1ValUnionMember0",
    "ConnectionDataUnionMember1ValUnionMember1",
    "ConnectionDataUnionMember1ValUnionMember2",
    "ConnectionDataUnionMember1ValUnionMember2AuthedUser",
    "ConnectionDataUnionMember1ValUnionMember3",
    "ConnectionDataUnionMember1ValUnionMember3AuthedUser",
    "ConnectionDataUnionMember1ValUnionMember4",
    "ConnectionDataUnionMember1ValUnionMember5",
    "ConnectionDataUnionMember1ValUnionMember6",
    "ConnectionDataUnionMember2",
    "ConnectionDataUnionMember2Val",
    "ConnectionDataUnionMember2ValUnionMember0",
    "ConnectionDataUnionMember2ValUnionMember1",
    "ConnectionDataUnionMember2ValUnionMember2",
    "ConnectionDataUnionMember2ValUnionMember3",
    "ConnectionDataUnionMember3",
    "ConnectionDataUnionMember3Val",
    "ConnectionDataUnionMember3ValUnionMember0",
    "ConnectionDataUnionMember3ValUnionMember1",
    "ConnectionDataUnionMember3ValUnionMember2",
    "ConnectionDataUnionMember3ValUnionMember3",
    "ConnectionDataUnionMember4",
    "ConnectionDataUnionMember4Val",
    "ConnectionDataUnionMember4ValUnionMember0",
    "ConnectionDataUnionMember4ValUnionMember1",
    "ConnectionDataUnionMember4ValUnionMember2",
    "ConnectionDataUnionMember4ValUnionMember3",
    "ConnectionDataUnionMember5",
    "ConnectionDataUnionMember5Val",
    "ConnectionDataUnionMember5ValUnionMember0",
    "ConnectionDataUnionMember5ValUnionMember1",
    "ConnectionDataUnionMember5ValUnionMember2",
    "ConnectionDataUnionMember5ValUnionMember3",
    "ConnectionDataUnionMember6",
    "ConnectionDataUnionMember6Val",
    "ConnectionDataUnionMember6ValUnionMember0",
    "ConnectionDataUnionMember6ValUnionMember1",
    "ConnectionDataUnionMember6ValUnionMember2",
    "ConnectionDataUnionMember6ValUnionMember3",
    "ConnectionDataUnionMember6ValUnionMember4",
    "ConnectionDataUnionMember6ValUnionMember5",
    "ConnectionDataUnionMember7",
    "ConnectionDataUnionMember7Val",
    "ConnectionDataUnionMember7ValUnionMember0",
    "ConnectionDataUnionMember7ValUnionMember1",
    "ConnectionDataUnionMember7ValUnionMember2",
    "ConnectionDataUnionMember7ValUnionMember3",
    "ConnectionDataUnionMember7ValUnionMember4",
    "ConnectionDataUnionMember7ValUnionMember5",
    "ConnectionDataUnionMember8",
    "ConnectionDataUnionMember8Val",
    "ConnectionDataUnionMember8ValUnionMember0",
    "ConnectionDataUnionMember8ValUnionMember1",
    "ConnectionDataUnionMember8ValUnionMember2",
    "ConnectionDataUnionMember8ValUnionMember3",
    "ConnectionDataUnionMember8ValUnionMember4",
    "ConnectionDataUnionMember8ValUnionMember5",
    "ConnectionDataUnionMember9",
    "ConnectionDataUnionMember9Val",
    "ConnectionDataUnionMember9ValUnionMember0",
    "ConnectionDataUnionMember9ValUnionMember1",
    "ConnectionDataUnionMember9ValUnionMember2",
    "ConnectionDataUnionMember9ValUnionMember3",
    "ConnectionDataUnionMember9ValUnionMember4",
    "ConnectionDataUnionMember9ValUnionMember5",
    "ConnectionDataUnionMember10",
    "ConnectionDataUnionMember10Val",
    "ConnectionDataUnionMember10ValUnionMember0",
    "ConnectionDataUnionMember10ValUnionMember1",
    "ConnectionDataUnionMember10ValUnionMember2",
    "ConnectionDataUnionMember10ValUnionMember3",
    "ConnectionDataUnionMember11",
    "ConnectionDataUnionMember11Val",
    "ConnectionDataUnionMember11ValUnionMember0",
    "ConnectionDataUnionMember11ValUnionMember1",
    "ConnectionDataUnionMember11ValUnionMember2",
    "ConnectionDataUnionMember11ValUnionMember3",
    "ConnectionDataUnionMember11ValUnionMember4",
    "ConnectionDataUnionMember11ValUnionMember5",
    "ConnectionDataUnionMember12",
    "ConnectionDataUnionMember12Val",
    "ConnectionDataUnionMember12ValUnionMember0",
    "ConnectionDataUnionMember12ValUnionMember1",
    "ConnectionDataUnionMember12ValUnionMember2",
    "ConnectionDataUnionMember12ValUnionMember3",
    "ConnectionDataUnionMember12ValUnionMember4",
    "ConnectionDataUnionMember12ValUnionMember5",
    "ConnectionDataUnionMember13",
    "ConnectionDataUnionMember13Val",
    "ConnectionDataUnionMember13ValUnionMember0",
    "ConnectionDataUnionMember13ValUnionMember1",
    "ConnectionDataUnionMember13ValUnionMember2",
    "ConnectionDataUnionMember13ValUnionMember3",
    "ConnectionDataUnionMember13ValUnionMember4",
    "ConnectionDataUnionMember13ValUnionMember5",
    "Deprecated",
    "Experimental",
    "ExperimentalACLConfigForShared",
]
