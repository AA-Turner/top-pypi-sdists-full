"""Test cases for ``Integration.info`` function."""

import typing as t

from connector.oai.capability import CustomRequest, CustomResponse
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.oauth_module_types import OAuthSettings
from connector_sdk_types.generated import (
    BasicCredential,
    CapabilitySchema,
    Info,
    InfoResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    OAuthCredential,
    StandardCapabilityName,
)
from connector_sdk_types.oai.modules.credentials_module_types import AuthModel, CredentialConfig

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
            app_vendor_domain="test.com",
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
            app_vendor_domain="test.com",
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
            access_graph_entitlement_types=[],
            access_graph_entitlement_rules=[],
            implied_access_rules=[],
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
            app_vendor_domain="test.com",
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
            app_vendor_domain="test.com",
            version="0.1.0",
            capabilities=[
                "accio",
                StandardCapabilityName.APP_INFO,
                StandardCapabilityName.LIST_ACCOUNTS,
                StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG,
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
                StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG.value: CapabilitySchema(
                    argument={
                        "$defs": {
                            "AuthCredential": {
                                "description": "Authentication credentials, which can be one of several types.",
                                "properties": {
                                    "basic": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/BasicCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "Basic auth credentials, if using basic auth.",
                                    },
                                    "id": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "default": None,
                                        "description": "The ID of the authentication schema.",
                                        "title": "Id",
                                    },
                                    "jwt": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/JWTCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "JWT credentials, if using JWT.",
                                    },
                                    "key_pair": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/KeyPairCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "Key-pair credentials, if using key-pair auth.",
                                        "x-semantic": "key-pair",
                                    },
                                    "oauth": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/OAuthCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "OAuth credentials, if using OAuth.",
                                    },
                                    "oauth1": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/OAuth1Credential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "OAuth 1.0a credentials, if using OAuth 1.0a.",
                                    },
                                    "oauth_client_credentials": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/OAuthClientCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "OAuth client credentials, if using OAuth Client Credentials flow.",
                                    },
                                    "service_account": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/ServiceAccountCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "Service account credentials, if using service account.",
                                    },
                                    "token": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/TokenCredential"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "Token credentials, if using token-based auth.",
                                    },
                                },
                                "title": "AuthCredential",
                                "type": "object",
                            },
                            "BasicCredential": {
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
                                "required": ["username", "password"],
                                "title": "BasicCredential",
                                "type": "object",
                                "x-credential-type": "basic",
                            },
                            "JWTClaims": {
                                "description": "JWT payload model representing the claims in the JWT.",
                                "properties": {
                                    "act": {
                                        "description": "The Actor of the JWT.",
                                        "title": "Act",
                                        "type": "string",
                                    },
                                    "aud": {
                                        "description": "The audience of the JWT.",
                                        "title": "Aud",
                                        "type": "string",
                                    },
                                    "client_id": {
                                        "description": "The client ID of the JWT.",
                                        "title": "Client Id",
                                        "type": "string",
                                    },
                                    "exp": {
                                        "description": "The expiration time of the JWT in seconds since the Unix epoch.",
                                        "title": "Exp",
                                        "type": "integer",
                                    },
                                    "iat": {
                                        "description": "The issue time of the JWT in seconds since the Unix epoch.",
                                        "title": "Iat",
                                        "type": "integer",
                                    },
                                    "iss": {
                                        "description": "The issuer of the JWT.",
                                        "title": "Iss",
                                        "type": "string",
                                    },
                                    "jti": {
                                        "description": "The JWT ID.",
                                        "title": "Jti",
                                        "type": "string",
                                    },
                                    "may_act": {
                                        "description": "The may_act of the JWT.",
                                        "title": "May Act",
                                        "type": "string",
                                    },
                                    "nbf": {
                                        "description": "The not before time of the JWT in seconds since the Unix epoch.",
                                        "title": "Nbf",
                                        "type": "integer",
                                    },
                                    "scope": {
                                        "description": "Scopes granted to the JWT.",
                                        "items": {"type": "string"},
                                        "title": "Scope",
                                        "type": "array",
                                    },
                                    "sub": {
                                        "description": "The subject of the JWT.",
                                        "title": "Sub",
                                        "type": "string",
                                    },
                                },
                                "required": [
                                    "iss",
                                    "sub",
                                    "aud",
                                    "exp",
                                    "nbf",
                                    "iat",
                                    "jti",
                                    "act",
                                    "scope",
                                    "client_id",
                                    "may_act",
                                ],
                                "title": "JWTClaims",
                                "type": "object",
                            },
                            "JWTCredential": {
                                "description": "JWT credential model.",
                                "properties": {
                                    "claims": {
                                        "$ref": "#/$defs/JWTClaims",
                                        "description": "The JWT claims.",
                                    },
                                    "headers": {
                                        "$ref": "#/$defs/JWTHeaders",
                                        "description": "The JWT headers.",
                                    },
                                    "secret": {
                                        "description": "The JWT secret.",
                                        "title": "Secret",
                                        "type": "string",
                                    },
                                },
                                "required": ["headers", "claims", "secret"],
                                "title": "JWTCredential",
                                "type": "object",
                                "x-credential-type": "jwt",
                            },
                            "JWTHeaders": {
                                "description": "JWT headers model.",
                                "properties": {
                                    "alg": {
                                        "description": "The JWT algorithm.",
                                        "title": "Alg",
                                        "type": "string",
                                    },
                                    "crit": {
                                        "description": "The JWT critical extension.",
                                        "items": {"type": "string"},
                                        "title": "Crit",
                                        "type": "array",
                                    },
                                    "cty": {
                                        "description": "The content type of the JWT.",
                                        "title": "Cty",
                                        "type": "string",
                                    },
                                    "jku": {
                                        "description": "JWK Set URL.",
                                        "title": "Jku",
                                        "type": "string",
                                    },
                                    "jwk": {
                                        "description": "JWK.",
                                        "title": "Jwk",
                                        "type": "string",
                                    },
                                    "kid": {
                                        "description": "The JWT key ID.",
                                        "title": "Kid",
                                        "type": "string",
                                    },
                                    "typ": {
                                        "description": "The JWT type.",
                                        "title": "Typ",
                                        "type": "string",
                                    },
                                    "x5c": {
                                        "description": "The X509 certificate chain.",
                                        "title": "X5C",
                                        "type": "string",
                                    },
                                    "x5t": {
                                        "description": "The X509 certificate SHA-1 thumbprint.",
                                        "title": "X5T",
                                        "type": "string",
                                    },
                                    "x5t#S256": {
                                        "description": "The X509 certificate SHA-256 thumbprint.",
                                        "title": "X5T#S256",
                                        "type": "string",
                                    },
                                    "x5u": {
                                        "description": "The X509 URL.",
                                        "title": "X5U",
                                        "type": "string",
                                    },
                                },
                                "required": [
                                    "alg",
                                    "jku",
                                    "jwk",
                                    "typ",
                                    "kid",
                                    "x5u",
                                    "x5c",
                                    "x5t",
                                    "x5t#S256",
                                    "cty",
                                    "crit",
                                ],
                                "title": "JWTHeaders",
                                "type": "object",
                            },
                            "KeyPairCredential": {
                                "description": "Key-pair credential model.",
                                "properties": {
                                    "key_identifier": {
                                        "description": "The identifier for the key-pair.",
                                        "title": "Key Identifier",
                                        "type": "string",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                    },
                                    "private_key": {
                                        "description": "The private key used to authenticate with the server.",
                                        "title": "Private Key",
                                        "type": "string",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                        "x-secret": True,
                                    },
                                },
                                "required": ["key_identifier", "private_key"],
                                "title": "KeyPairCredential",
                                "type": "object",
                                "x-credential-type": "key_pair",
                                "x-keygen-type": "SSH",
                                "x-semantic": "key-pair",
                            },
                            "OAuth1Credential": {
                                "description": "OAuth 1.0a credential model. This auth type is not used much, handling is done per-connector.",
                                "properties": {
                                    "consumer_key": {
                                        "description": "Consumer Key",
                                        "title": "Consumer Key",
                                        "type": "string",
                                    },
                                    "consumer_secret": {
                                        "description": "Consumer Secret",
                                        "title": "Consumer Secret",
                                        "type": "string",
                                        "x-field_type": "SECRET",
                                        "x-secret": True,
                                    },
                                    "token_id": {
                                        "description": "Token ID",
                                        "title": "Token Id",
                                        "type": "string",
                                    },
                                    "token_secret": {
                                        "description": "Token Secret",
                                        "title": "Token Secret",
                                        "type": "string",
                                        "x-field_type": "SECRET",
                                        "x-secret": True,
                                    },
                                },
                                "required": [
                                    "consumer_key",
                                    "consumer_secret",
                                    "token_id",
                                    "token_secret",
                                ],
                                "title": "OAuth1Credential",
                                "type": "object",
                                "x-credential-type": "oauth1",
                            },
                            "OAuthClientCredential": {
                                "description": "OAuth Client Credentials",
                                "properties": {
                                    "access_token": {
                                        "description": "The OAuth access token.",
                                        "title": "Access Token",
                                        "type": "string",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                        "x-secret": True,
                                    },
                                    "client_id": {
                                        "description": "The OAuth client id.",
                                        "title": "Client Id",
                                        "type": "string",
                                    },
                                    "client_secret": {
                                        "description": "The OAuth client secret.",
                                        "title": "Client Secret",
                                        "type": "string",
                                        "x-field_type": "SECRET",
                                        "x-secret": True,
                                    },
                                    "scopes": {
                                        "description": "The OAuth scopes list.",
                                        "items": {"type": "string"},
                                        "title": "Scopes",
                                        "type": "array",
                                    },
                                },
                                "required": [
                                    "access_token",
                                    "client_id",
                                    "client_secret",
                                    "scopes",
                                ],
                                "title": "OAuthClientCredential",
                                "type": "object",
                                "x-credential-type": "oauth_client_credentials",
                            },
                            "OAuthCredential": {
                                "description": "OAuth access token and related authentication data.",
                                "properties": {
                                    "access_token": {
                                        "description": "The OAuth access token.",
                                        "title": "Access Token",
                                        "type": "string",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                        "x-secret": True,
                                    }
                                },
                                "required": ["access_token"],
                                "title": "OAuthCredential",
                                "type": "object",
                                "x-credential-type": "oauth",
                            },
                            "ServiceAccountCredential": {
                                "description": "ServiceAccountCredential",
                                "properties": {
                                    "impersonation_email": {
                                        "description": "The email of the user to impersonate.",
                                        "title": "Impersonation Email",
                                        "type": "string",
                                    },
                                    "key": {
                                        "description": "The JSON key file contents for the service account",
                                        "title": "Key",
                                        "type": "object",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                        "x-secret": True,
                                    },
                                    "scopes": {
                                        "description": "The scopes to request. Requested by connector. Define a default here.",
                                        "items": {"type": "string"},
                                        "title": "Scopes",
                                        "type": "array",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                    },
                                    "service_type": {
                                        "anyOf": [
                                            {"$ref": "#/$defs/ServiceAccountType"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "The type of service.",
                                        "x-field_type": "HIDDEN",
                                        "x-hidden": True,
                                    },
                                    "tenant_id": {
                                        "description": "Tenant ID",
                                        "title": "Tenant Id",
                                        "type": "string",
                                    },
                                },
                                "required": ["key", "impersonation_email", "tenant_id", "scopes"],
                                "title": "ServiceAccountCredential",
                                "type": "object",
                                "x-credential-type": "service_account",
                            },
                            "ServiceAccountType": {
                                "description": "ServiceAccountType",
                                "enum": ["google_cloud", "google_drive", "aws"],
                                "title": "ServiceAccountType",
                                "type": "string",
                            },
                            "TokenCredential": {
                                "description": "Token-based authentication credentials.",
                                "properties": {
                                    "token": {
                                        "description": "The token for token-based auth.",
                                        "title": "Token",
                                        "type": "string",
                                        "x-field_type": "SECRET",
                                        "x-secret": True,
                                    }
                                },
                                "required": ["token"],
                                "title": "TokenCredential",
                                "type": "object",
                                "x-credential-type": "token",
                            },
                        },
                        "description": "ValidateCredentialConfig",
                        "properties": {
                            "credential": {"$ref": "#/$defs/AuthCredential"},
                        },
                        "required": ["credential"],
                        "title": "ValidateCredentialConfig",
                        "type": "object",
                        "x-capability-level": "validation",
                    },
                    description=None,
                    display_name="Validate Credential Config",
                    output={
                        "description": "Result of credential validation containing validity and tenant information",
                        "properties": {
                            "validation_errors": {
                                "anyOf": [
                                    {"items": {"type": "string"}, "type": "array"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "description": '(Optional) List of errors that occurred during validation. This capability can return a list of validation errors, these should be displayed to a customer. An example of such an error is "Access Token is missing required scopes, please update your OAuth app."',
                                "title": "Validation Errors",
                            },
                            "valid": {
                                "description": "Indicates whether the provided credentials are valid and active.  - true: Credentials are valid and can be used for API operations, no validation errors expected. - false: Credentials are invalid, expired, or revoked. It is expected that the connector returns at least one validation error.",
                                "title": "Valid",
                                "type": "boolean",
                            },
                        },
                        "required": ["valid"],
                        "title": "ValidatedCredentialConfig",
                        "type": "object",
                    },
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
                    "x-optional": False,
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
                    "x-optional": False,
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
            access_graph_entitlement_types=[],
            access_graph_entitlement_rules=[],
            implied_access_rules=[],
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
            app_vendor_domain="test.com",
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
            app_vendor_domain="test.com",
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
                        "x-secret": True,
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
            access_graph_entitlement_types=[],
            access_graph_entitlement_rules=[],
            implied_access_rules=[],
            resource_types=[],
            logo_url=None,
        )
    )
    return integration, expected_info
