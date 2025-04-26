"""Test cases for ``Integration.info`` function."""

import typing as t

from connector.generated import (
    AuthModel,
    BasicCredential,
    CapabilitySchema,
    CredentialConfig,
    Info,
    InfoResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    OAuthCredential,
    StandardCapabilityName,
)
from connector.oai.capability import CustomRequest, CustomResponse
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.oauth_module_types import OAuthSettings

from .shared_types import (
    AccioRequest,
    AccioResponse,
)

Case: t.TypeAlias = tuple[
    Integration,
    InfoResponse,
]


def case_info() -> Case:
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        auth=BasicCredential,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="test_info_cases.py",
            categories=[],
        ),
    )

    @integration.register_capability(
        StandardCapabilityName.LIST_ACCOUNTS, description="List accounts capability description."
    )
    async def capability(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    @integration.register_custom_capability("accio", description="A summoning charm.")
    async def custom_capability(args: CustomRequest[AccioRequest]) -> CustomResponse[AccioResponse]:
        return CustomResponse[AccioResponse](
            response=AccioResponse(success=True),
        )

    expected_info = InfoResponse(
        response=Info(
            app_id="test",
            version="0.1.0",
            capabilities=[
                "accio",
                StandardCapabilityName.APP_INFO,
                StandardCapabilityName.LIST_ACCOUNTS,
            ],
            capability_schema={
                "accio": CapabilitySchema(
                    argument={
                        "properties": {
                            "object_name": {
                                "title": "Object Name",
                                "type": "string",
                            },
                        },
                        "required": ["object_name"],
                        "title": "AccioRequest",
                        "type": "object",
                    },
                    description="A summoning charm.",
                    display_name="Accio",
                    output={
                        "properties": {"success": {"title": "Success", "type": "boolean"}},
                        "required": ["success"],
                        "title": "AccioResponse",
                        "type": "object",
                    },
                ),
                StandardCapabilityName.APP_INFO.value: CapabilitySchema(
                    argument={
                        "description": "AppInfoRequestPayload",
                        "properties": {},
                        "title": "AppInfoRequestPayload",
                        "type": "object",
                        "x-capability-category": "specification",
                    },
                    description=None,
                    display_name="App Info",
                    output={
                        "description": "AppInfo",
                        "properties": {
                            "app_id": {
                                "title": "App Id",
                                "type": "string",
                            },
                            "app_schema": {
                                "description": "The connector OpenAPI specification",
                                "title": "App Schema",
                                "type": "object",
                            },
                        },
                        "required": [
                            "app_id",
                            "app_schema",
                        ],
                        "title": "AppInfo",
                        "type": "object",
                    },
                ),
                StandardCapabilityName.LIST_ACCOUNTS.value: CapabilitySchema(
                    argument={
                        "description": "Request parameters for listing accounts.",
                        "properties": {
                            "custom_attributes": {
                                "anyOf": [
                                    {"items": {"type": "string"}, "type": "array"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": (
                                    "Optional array of custom attribute names to "
                                    "include in the account data. Each string in "
                                    "this array represents a specific custom "
                                    "attribute to retrieve."
                                ),
                                "title": "Custom Attributes",
                            }
                        },
                        "title": "ListAccounts",
                        "type": "object",
                        "x-capability-level": "read",
                    },
                    output={"properties": {}, "title": "Empty", "type": "object"},
                    description="List accounts capability description.",
                    display_name="List Accounts",
                ),
            },
            authentication_schema={
                "description": "Basic authentication credentials.",
                "properties": {
                    "password": {
                        "description": "The password for basic auth.",
                        "title": "Password",
                        "type": "string",
                        "x-field_type": "SECRET",
                        "x-secret": True,
                    },
                    "username": {
                        "description": "The username for basic auth.",
                        "title": "Username",
                        "type": "string",
                    },
                },
                "required": [
                    "username",
                    "password",
                ],
                "title": "BasicCredential",
                "field_order": ["username", "password"],
                "type": "object",
                "x-credential-type": "basic",
            },
            credentials_schema=[],
            user_friendly_name="test_info_cases.py",
            categories=[],
            request_settings_schema={
                "properties": {},
                "title": "EmptySettings",
                "field_order": [],
                "type": "object",
            },
            entitlement_types=[],
            resource_types=[],
        )
    )
    return integration, expected_info


def case_info_with_credentials() -> Case:
    app_id = "test"

    credentials = [
        CredentialConfig(
            id="test",
            description="Test credential",
            type=AuthModel.BASIC,
        ),
        CredentialConfig(
            id="test2",
            description="Test credential 2",
            type=AuthModel.TOKEN,
        ),
    ]

    integration = Integration(
        app_id=app_id,
        version="0.1.0",
        credentials=credentials,
        exception_handlers=[],
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="test_info_cases.py",
            categories=[],
        ),
    )

    @integration.register_capability(
        StandardCapabilityName.LIST_ACCOUNTS,
        description="List accounts capability with credentials description.",
    )
    async def capability(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    @integration.register_custom_capability("accio", description="A summoning charm.")
    async def custom_capability(args: CustomRequest[AccioRequest]) -> CustomResponse[AccioResponse]:
        return CustomResponse[AccioResponse](
            response=AccioResponse(success=True),
        )

    expected_info = InfoResponse(
        response=Info(
            app_id="test",
            version="0.1.0",
            capabilities=[
                "accio",
                StandardCapabilityName.APP_INFO,
                StandardCapabilityName.LIST_ACCOUNTS,
            ],
            capability_schema={
                "accio": CapabilitySchema(
                    argument={
                        "properties": {
                            "object_name": {
                                "title": "Object Name",
                                "type": "string",
                            },
                        },
                        "required": ["object_name"],
                        "title": "AccioRequest",
                        "type": "object",
                    },
                    description="A summoning charm.",
                    display_name="Accio",
                    output={
                        "properties": {"success": {"title": "Success", "type": "boolean"}},
                        "required": ["success"],
                        "title": "AccioResponse",
                        "type": "object",
                    },
                ),
                StandardCapabilityName.APP_INFO.value: CapabilitySchema(
                    argument={
                        "description": "AppInfoRequestPayload",
                        "properties": {},
                        "title": "AppInfoRequestPayload",
                        "type": "object",
                        "x-capability-category": "specification",
                    },
                    description=None,
                    display_name="App Info",
                    output={
                        "description": "AppInfo",
                        "properties": {
                            "app_id": {
                                "title": "App Id",
                                "type": "string",
                            },
                            "app_schema": {
                                "description": "The connector OpenAPI specification",
                                "title": "App Schema",
                                "type": "object",
                            },
                        },
                        "required": [
                            "app_id",
                            "app_schema",
                        ],
                        "title": "AppInfo",
                        "type": "object",
                    },
                ),
                StandardCapabilityName.LIST_ACCOUNTS.value: CapabilitySchema(
                    argument={
                        "description": "Request parameters for listing accounts.",
                        "properties": {
                            "custom_attributes": {
                                "anyOf": [
                                    {"items": {"type": "string"}, "type": "array"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": (
                                    "Optional array of custom attribute names to "
                                    "include in the account data. Each string in "
                                    "this array represents a specific custom "
                                    "attribute to retrieve."
                                ),
                                "title": "Custom Attributes",
                            }
                        },
                        "title": "ListAccounts",
                        "type": "object",
                        "x-capability-level": "read",
                    },
                    output={"properties": {}, "title": "Empty", "type": "object"},
                    description="List accounts capability with credentials description.",
                    display_name="List Accounts",
                ),
            },
            authentication_schema={},
            credentials_schema=[
                {
                    "id": "test",
                    "description": "Test credential",
                    "properties": {
                        "username": {
                            "title": "Username",
                            "description": "The username for basic auth.",
                            "type": "string",
                        },
                        "password": {
                            "title": "Password",
                            "description": "The password for basic auth.",
                            "type": "string",
                            "x-field_type": "SECRET",
                            "x-secret": True,
                        },
                    },
                    "required": ["username", "password"],
                    "title": "BasicCredential",
                    "field_order": ["username", "password"],
                    "type": "object",
                    "x-credential-type": "basic",
                },
                {
                    "id": "test2",
                    "description": "Test credential 2",
                    "properties": {
                        "token": {
                            "title": "Token",
                            "description": "The token for token-based auth.",
                            "type": "string",
                            "x-field_type": "SECRET",
                            "x-secret": True,
                        },
                    },
                    "required": ["token"],
                    "title": "TokenCredential",
                    "field_order": ["token"],
                    "type": "object",
                    "x-credential-type": "token",
                },
            ],
            user_friendly_name="test_info_cases.py",
            categories=[],
            request_settings_schema={
                "properties": {},
                "title": "EmptySettings",
                "field_order": [],
                "type": "object",
            },
            entitlement_types=[],
            resource_types=[],
        )
    )
    return integration, expected_info


def case_info_with_scopes() -> Case:
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        auth=OAuthCredential,
        version="0.1.0",
        exception_handlers=[],
        oauth_settings=OAuthSettings(
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token",
            scopes={
                StandardCapabilityName.LIST_ACCOUNTS: "test:scope another:scope",
            },
        ),
        handle_errors=True,
        description_data=DescriptionData(
            user_friendly_name="test_info_cases.py",
            categories=[],
        ),
    )

    @integration.register_capability(
        StandardCapabilityName.LIST_ACCOUNTS, description="List accounts capability description."
    )
    async def capability(
        args: ListAccountsRequest,
    ) -> ListAccountsResponse:
        return ListAccountsResponse(
            response=[],
            raw_data=None,
        )

    expected_info = InfoResponse(
        response=Info(
            app_id="test",
            version="0.1.0",
            capabilities=[
                StandardCapabilityName.APP_INFO,
                StandardCapabilityName.GET_AUTHORIZATION_URL,
                StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK,
                StandardCapabilityName.LIST_ACCOUNTS,
                StandardCapabilityName.REFRESH_ACCESS_TOKEN,
            ],
            capability_schema={
                StandardCapabilityName.APP_INFO.value: CapabilitySchema(
                    argument={
                        "description": "AppInfoRequestPayload",
                        "properties": {},
                        "title": "AppInfoRequestPayload",
                        "type": "object",
                        "x-capability-category": "specification",
                    },
                    description=None,
                    display_name="App Info",
                    output={
                        "description": "AppInfo",
                        "properties": {
                            "app_id": {
                                "title": "App Id",
                                "type": "string",
                            },
                            "app_schema": {
                                "description": "The connector OpenAPI specification",
                                "title": "App Schema",
                                "type": "object",
                            },
                        },
                        "required": [
                            "app_id",
                            "app_schema",
                        ],
                        "title": "AppInfo",
                        "type": "object",
                    },
                ),
                StandardCapabilityName.GET_AUTHORIZATION_URL.value: CapabilitySchema(
                    argument={
                        "description": "Parameters for generating an OAuth authorization URL.",
                        "properties": {
                            "credential_id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                                "default": None,
                                "description": "The credential ID assigned to these credentials.",
                                "title": "Credential Id",
                            },
                            "client_id": {
                                "description": (
                                    "OAuth client ID provided by the third-party service."
                                ),
                                "title": "Client Id",
                                "type": "string",
                            },
                            "scopes": {
                                "description": "List of OAuth scopes to request.",
                                "items": {"type": "string"},
                                "title": "Scopes",
                                "type": "array",
                            },
                            "redirect_uri": {
                                "description": (
                                    "URL where the user will be redirected after authorization. "
                                    "Must match the connector settings."
                                ),
                                "title": "Redirect Uri",
                                "type": "string",
                            },
                            "state": {
                                "description": "State parameter for security validation.",
                                "title": "State",
                                "type": "string",
                            },
                            "form_data": {
                                "anyOf": [
                                    {"additionalProperties": {"type": "string"}, "type": "object"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": "Form data to include in the authorization request.",
                                "title": "Form Data",
                            },
                        },
                        "required": ["client_id", "scopes", "redirect_uri", "state"],
                        "title": "GetAuthorizationUrl",
                        "type": "object",
                        "x-capability-category": "authorization",
                    },
                    output={
                        "description": "OAuth authorization URL details.",
                        "properties": {
                            "authorization_url": {
                                "description": "The authorization URL to redirect the user to.",
                                "title": "Authorization Url",
                                "type": "string",
                            },
                            "code_verifier": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "A code verifier for PKCE. This is the challenge that was "
                                    "sent in the authorization URL when using PKCE."
                                ),
                                "title": "Code Verifier",
                            },
                        },
                        "required": ["authorization_url"],
                        "title": "AuthorizationUrl",
                        "type": "object",
                    },
                    description=None,
                    display_name="Get Authorization Url",
                ),
                StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK.value: CapabilitySchema(
                    argument={
                        "description": "Parameters for handling an OAuth2 authorization callback.",
                        "properties": {
                            "credential_id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                                "default": None,
                                "description": "The credential ID assigned to these credentials.",
                                "title": "Credential Id",
                            },
                            "client_id": {
                                "description": (
                                    "The OAuth client ID provided by the third-party service."
                                ),
                                "title": "Client Id",
                                "type": "string",
                            },
                            "client_secret": {
                                "description": (
                                    "The OAuth client secret associated with the client ID."
                                ),
                                "title": "Client Secret",
                                "type": "string",
                            },
                            "redirect_uri_with_code": {
                                "description": (
                                    "The redirect URI containing the authorization code "
                                    "returned by the OAuth provider."
                                ),
                                "title": "Redirect Uri With Code",
                                "type": "string",
                            },
                            "state": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A state parameter for security validation."
                                ),
                                "title": "State",
                            },
                            "code_verifier": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "A code verifier for PKCE. This is returned from the "
                                    "get_authorization_url operation if PKCE is enabled."
                                ),
                                "title": "Code Verifier",
                            },
                        },
                        "required": ["client_id", "client_secret", "redirect_uri_with_code"],
                        "title": "HandleAuthorizationCallback",
                        "type": "object",
                        "x-capability-category": "authorization",
                    },
                    output={
                        "$defs": {
                            "TokenType": {
                                "const": "bearer",
                                "description": "TokenType",
                                "enum": ["bearer"],
                                "title": "TokenType",
                                "type": "string",
                            }
                        },
                        "description": "OAuth credentials model.  Enough authentication material to enable a capability, e.g. List Accounts, for an OAuth-based connector.",
                        "properties": {
                            "access_token": {
                                "description": (
                                    "The token used for authenticating API requests, "
                                    "providing access to the API."
                                ),
                                "title": "Access Token",
                                "type": "string",
                            },
                            "refresh_token": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A token used to refresh the access token, "
                                    "extending the session without re-authentication."
                                ),
                                "title": "Refresh Token",
                            },
                            "token_type": {
                                "$ref": "#/$defs/TokenType",
                                "description": (
                                    'The type of token, usually "bearer", indicating how '
                                    "the token should be used."
                                ),
                            },
                            "state": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A state parameter for security validation, "
                                    "ensuring the response matches the request."
                                ),
                                "title": "State",
                            },
                        },
                        "required": ["access_token", "token_type"],
                        "title": "OauthCredentials",
                        "type": "object",
                    },
                    description=None,
                    display_name="Handle Authorization Callback",
                ),
                StandardCapabilityName.LIST_ACCOUNTS.value: CapabilitySchema(
                    argument={
                        "description": "Request parameters for listing accounts.",
                        "properties": {
                            "custom_attributes": {
                                "anyOf": [
                                    {"items": {"type": "string"}, "type": "array"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": (
                                    "Optional array of custom attribute names to include in "
                                    "the account data. Each string in this array represents "
                                    "a specific custom attribute to retrieve."
                                ),
                                "title": "Custom Attributes",
                            }
                        },
                        "title": "ListAccounts",
                        "type": "object",
                        "x-capability-level": "read",
                    },
                    output={"properties": {}, "title": "Empty", "type": "object"},
                    description="List accounts capability description.",
                    display_name="List Accounts",
                ),
                StandardCapabilityName.REFRESH_ACCESS_TOKEN.value: CapabilitySchema(
                    argument={
                        "description": "RefreshAccessToken Model",
                        "properties": {
                            "credential_id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "null",
                                    },
                                ],
                                "default": None,
                                "description": "The credential ID assigned to these credentials.",
                                "title": "Credential Id",
                            },
                            "client_id": {
                                "description": (
                                    "The OAuth client ID provided by the third-party service."
                                ),
                                "title": "Client Id",
                                "type": "string",
                            },
                            "client_secret": {
                                "description": (
                                    "The OAuth client secret associated with the client ID."
                                ),
                                "title": "Client Secret",
                                "type": "string",
                            },
                            "refresh_token": {
                                "description": (
                                    "The token used to obtain a new access token, extending the "
                                    "session."
                                ),
                                "title": "Refresh Token",
                                "type": "string",
                            },
                            "state": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A state parameter for security validation."
                                ),
                                "title": "State",
                            },
                        },
                        "required": ["client_id", "client_secret", "refresh_token"],
                        "title": "RefreshAccessToken",
                        "type": "object",
                        "x-capability-category": "authorization",
                    },
                    output={
                        "$defs": {
                            "TokenType": {
                                "const": "bearer",
                                "description": "TokenType",
                                "enum": ["bearer"],
                                "title": "TokenType",
                                "type": "string",
                            }
                        },
                        "description": (
                            "OAuth credentials model.  Enough authentication material to enable a "
                            "capability, e.g. List Accounts, for an OAuth-based connector."
                        ),
                        "properties": {
                            "access_token": {
                                "description": (
                                    "The token used for authenticating API requests, providing "
                                    "access to the API."
                                ),
                                "title": "Access Token",
                                "type": "string",
                            },
                            "refresh_token": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A token used to refresh the access token, "
                                    "extending the session without re-authentication."
                                ),
                                "title": "Refresh Token",
                            },
                            "token_type": {
                                "$ref": "#/$defs/TokenType",
                                "description": (
                                    'The type of token, usually "bearer", indicating how the '
                                    "token should be used."
                                ),
                            },
                            "state": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "default": None,
                                "description": (
                                    "(Optional) A state parameter for security validation, "
                                    "ensuring the response matches the request."
                                ),
                                "title": "State",
                            },
                        },
                        "required": ["access_token", "token_type"],
                        "title": "OauthCredentials",
                        "type": "object",
                    },
                    description=None,
                    display_name="Refresh Access Token",
                ),
            },
            authentication_schema={
                "description": "OAuth access token and related authentication data.",
                "properties": {
                    "access_token": {
                        "description": "The OAuth access token.",
                        "title": "Access Token",
                        "type": "string",
                        "x-field_type": "HIDDEN",
                        "x-hidden": True,
                    },
                },
                "required": ["access_token"],
                "title": "OAuthCredential",
                "field_order": ["access_token"],
                "type": "object",
                "x-credential-type": "oauth",
            },
            credentials_schema=[],
            oauth_scopes={
                "list_accounts": "test:scope another:scope",
            },
            user_friendly_name="test_info_cases.py",
            description=None,
            categories=[],
            request_settings_schema={
                "properties": {},
                "title": "EmptySettings",
                "field_order": [],
                "type": "object",
            },
            entitlement_types=[],
            resource_types=[],
            logo_url=None,
        )
    )
    return integration, expected_info
