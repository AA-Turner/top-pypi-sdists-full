# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.tool_proxy_params."""

from __future__ import annotations

from typing import Annotated, Dict, Iterable, Literal, Optional, TypeAlias, Union

from typing_extensions import NotRequired, Required, TypedDict
from .._types import PropertyInfo, SequenceNotStr


class BinaryBodyUnionMember0(TypedDict, total=False):
    content_type: str
    "Content-Type header to use for the request"
    url: Required[str]
    "URL to fetch binary content from"


class BinaryBodyUnionMember1(TypedDict, total=False):
    base64: Required[str]
    "Base64-encoded binary data"
    content_type: str
    "Content-Type header to use for the request"


class Parameter(TypedDict, total=False):
    name: Required[str]
    "Parameter name"
    type: Required[Literal['header', 'query']]
    "Parameter type (header or query)"
    value: Required[str]
    "Parameter value"


class CustomConnectionDataUnionMember0ValAuthedUser(TypedDict, total=False):
    "for slack user scopes"

    access_token: str
    scope: str


class CustomConnectionDataUnionMember0Val(TypedDict, total=False):
    access_token: Required[str]
    account_id: str
    account_url: str
    api_url: str
    authed_user: CustomConnectionDataUnionMember0ValAuthedUser
    "for slack user scopes"
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    expires_in: Union[float, str, None]
    extension: str
    extra_token_data: Dict[str, Optional[object]]
    form_api_base_url: str
    id_token: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    long_redirect_url: bool
    "Whether to return the redirect url without shortening"
    proxy_password: str
    proxy_username: str
    refresh_token: Optional[str]
    region: str
    scope: Union[str, SequenceNotStr[str], None]
    server_location: str
    shop: str
    site_name: str
    state_prefix: str
    "The oauth2 state prefix for the connection"
    subdomain: str
    token_type: str
    version: str
    webhook_signature: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember0(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['OAUTH2'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember0Val]


class CustomConnectionDataUnionMember1Val(TypedDict, total=False):
    access_token: Required[str]
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    client_id: Required[str]
    "Dynamically registered client ID"
    client_id_issued_at: float
    client_secret: str
    "Dynamically registered client secret"
    client_secret_expires_at: float
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    expires_in: Union[float, str, None]
    extension: str
    form_api_base_url: str
    id_token: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    long_redirect_url: bool
    "Whether to return the redirect url without shortening"
    proxy_password: str
    proxy_username: str
    refresh_token: Optional[str]
    region: str
    scope: Union[str, SequenceNotStr[str], None]
    server_location: str
    shop: str
    site_name: str
    state_prefix: str
    "The oauth2 state prefix for the connection"
    subdomain: str
    token_type: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember1(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['DCR_OAUTH'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember1Val]


class CustomConnectionDataUnionMember2Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_key: str
    api_url: str
    base_url: str
    basic_encoded: str
    bearer_token: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    generic_api_key: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember2(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['API_KEY'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember2Val]


class CustomConnectionDataUnionMember3Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    password: Required[str]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    username: Required[str]
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember3(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['BASIC_WITH_JWT'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember3Val]


class CustomConnectionDataUnionMember4Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    password: str
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    username: Required[str]
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember4(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['BASIC'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember4Val]


class CustomConnectionDataUnionMember5Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    token: Required[str]
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember5(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['BEARER_TOKEN'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember5Val]


class CustomConnectionDataUnionMember6Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    callback_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    consumer_key: str
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    oauth_token: Required[str]
    oauth_token_secret: Required[str]
    oauth_verifier: str
    proxy_password: str
    proxy_username: str
    redirect_url: Annotated[str, PropertyInfo(alias='redirectUrl')]
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember6(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['OAUTH1'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember6Val]


class CustomConnectionDataUnionMember7Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember7(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['NO_AUTH'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember7Val]


class CustomConnectionDataUnionMember8Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    application_id: Required[str]
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    installation_id: Required[str]
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    private_key: Required[str]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember8(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['SERVICE_ACCOUNT'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember8Val]


class CustomConnectionDataUnionMember9Val(TypedDict, total=False):
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    credentials_json: Required[str]
    dc: str
    domain: str
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    proxy_password: str
    proxy_username: str
    region: str
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember9(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['GOOGLE_SERVICE_ACCOUNT'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember9Val]


class CustomConnectionDataUnionMember10Val(TypedDict, total=False):
    access_token: Required[str]
    account_id: str
    account_url: str
    api_url: str
    base_url: str
    borneo_dashboard_url: str
    client_id: str
    client_secret: str
    companydomain: Annotated[str, PropertyInfo(alias='COMPANYDOMAIN')]
    dc: str
    domain: str
    expires_at: str
    expires_in: Union[float, str, None]
    extension: str
    form_api_base_url: str
    instance_endpoint: Annotated[str, PropertyInfo(alias='instanceEndpoint')]
    instance_name: Annotated[str, PropertyInfo(alias='instanceName')]
    proxy_password: str
    proxy_username: str
    region: str
    scope: Union[str, SequenceNotStr[str], None]
    server_location: str
    shop: str
    site_name: str
    subdomain: str
    token_type: str
    version: str
    your_domain: Annotated[str, PropertyInfo(alias='your-domain')]
    your_server: str


class CustomConnectionDataUnionMember10(TypedDict, total=False):
    auth_scheme: Required[Annotated[Literal['S2S_OAUTH2'], PropertyInfo(alias='authScheme')]]
    toolkit_slug: Required[Annotated[str, PropertyInfo(alias='toolkitSlug')]]
    val: Required[CustomConnectionDataUnionMember10Val]


class ToolProxyParams(TypedDict, total=False):
    connected_account_id: str
    "The ID of the connected account to use for authentication (if not provided, will\nuse the default account for the project)"
    user_id: NotRequired[str]
    endpoint: Required[str]
    "The API endpoint to call (absolute URL or path relative to base URL of the\nconnected account)"
    method: Required[Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']]
    "The HTTP method to use for the request"
    body: object
    "The request body (for POST, PUT, and PATCH requests)"
    binary_body: Union[BinaryBodyUnionMember0, BinaryBodyUnionMember1]
    "Binary body to send.\n\nFor binary upload via URL: use {url: \"https://...\", content_type?: \"...\"}. For\nbinary upload via base64: use {base64: \"...\", content_type?: \"...\"}."
    parameters: Iterable[Parameter]
    "Additional HTTP headers or query parameters to include in the request"
    custom_connection_data: Union[CustomConnectionDataUnionMember0, CustomConnectionDataUnionMember1, CustomConnectionDataUnionMember2, CustomConnectionDataUnionMember3, CustomConnectionDataUnionMember4, CustomConnectionDataUnionMember5, CustomConnectionDataUnionMember6, CustomConnectionDataUnionMember7, CustomConnectionDataUnionMember8, CustomConnectionDataUnionMember9, CustomConnectionDataUnionMember10]


BinaryBody: TypeAlias = Union[BinaryBodyUnionMember0, BinaryBodyUnionMember1]

CustomConnectionData: TypeAlias = Union[CustomConnectionDataUnionMember0, CustomConnectionDataUnionMember1, CustomConnectionDataUnionMember2, CustomConnectionDataUnionMember3, CustomConnectionDataUnionMember4, CustomConnectionDataUnionMember5, CustomConnectionDataUnionMember6, CustomConnectionDataUnionMember7, CustomConnectionDataUnionMember8, CustomConnectionDataUnionMember9, CustomConnectionDataUnionMember10]

__all__ = [
    "ToolProxyParams",
    "BinaryBody",
    "BinaryBodyUnionMember0",
    "BinaryBodyUnionMember1",
    "CustomConnectionData",
    "CustomConnectionDataUnionMember0",
    "CustomConnectionDataUnionMember0Val",
    "CustomConnectionDataUnionMember0ValAuthedUser",
    "CustomConnectionDataUnionMember1",
    "CustomConnectionDataUnionMember1Val",
    "CustomConnectionDataUnionMember2",
    "CustomConnectionDataUnionMember2Val",
    "CustomConnectionDataUnionMember3",
    "CustomConnectionDataUnionMember3Val",
    "CustomConnectionDataUnionMember4",
    "CustomConnectionDataUnionMember4Val",
    "CustomConnectionDataUnionMember5",
    "CustomConnectionDataUnionMember5Val",
    "CustomConnectionDataUnionMember6",
    "CustomConnectionDataUnionMember6Val",
    "CustomConnectionDataUnionMember7",
    "CustomConnectionDataUnionMember7Val",
    "CustomConnectionDataUnionMember8",
    "CustomConnectionDataUnionMember8Val",
    "CustomConnectionDataUnionMember9",
    "CustomConnectionDataUnionMember9Val",
    "CustomConnectionDataUnionMember10",
    "CustomConnectionDataUnionMember10Val",
    "Parameter",
]
