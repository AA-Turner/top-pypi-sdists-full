"""Utilities for describing capabilities.

Each known capability is assigned a base class for request and response.
The actual request and response types in a integration implementation
can either use the base classes directly or create subclasses, however,
those bases are enforced to be used.
"""

import inspect
import typing as t
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError

from connector.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AppInfoRequest,
    AppInfoResponse,
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    AuthCredential,
    BasicCredential,
    CapabilitySchema,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    ErrorCode,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    GetAuthorizationUrlRequest,
    GetAuthorizationUrlResponse,
    GetLastActivityRequest,
    GetLastActivityResponse,
    HandleAuthorizationCallbackRequest,
    HandleAuthorizationCallbackResponse,
    HandleClientCredentialsRequest,
    HandleClientCredentialsResponse,
    JWTCredential,
    ListAccountsRequest,
    ListAccountsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListExpensesRequest,
    ListExpensesResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    Page,
    RefreshAccessTokenRequest,
    RefreshAccessTokenResponse,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenCredential,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    UpdateAccountRequest,
    UpdateAccountResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
)
from connector.oai.errors import ConnectorError

BaseModelType = t.TypeVar("BaseModelType", bound=BaseModel)


class Request(t.Protocol):
    """
    A generic request to any capability.

    Useful as a type for calling request helpers on, e.g. get_token_auth, get_settings.

    Will match all AuthenticatedRequest capability inputs.
    """

    auth: t.Any
    """
    The connector.generated.AuthCredential attached to this request.
    """

    credentials: t.Any

    request: t.Any
    """
    The payload of this request. The type depends on the request type.
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """


class AuthRequest(t.Protocol):
    """
    A request being used as part of an authentication flow.

    These requests must have settings, but they don't have credentials.
    """

    request: t.Any
    """
    The payload of this request
    """

    page: t.Any
    """
    Page data. May be None
    """

    include_raw_data: bool | None = None

    settings: t.Any
    """
    User-configured settings for the integration.
    """


CredentialType = t.TypeVar(
    "CredentialType",
    OAuthCredential,
    OAuthClientCredential,
    BasicCredential,
    TokenCredential,
    JWTCredential,
)


def get_credential(
    request: Request, credential_id: str, credential_type: type[CredentialType]
) -> CredentialType:
    """
    Return the particular credential from the request.
    Similarly to get_settings, the credential is identified by the credential_id and the root credentials model.
    eg. OAuthCredential, OAuthClientCredential, BasicCredential, TokenCredential, JWTCredential
    """
    if request.credentials and isinstance(request.credentials, list):
        for credential in request.credentials:
            if credential.id == credential_id:
                # Find the credential from the request
                if credential.oauth and isinstance(credential.oauth, credential_type):
                    return credential.oauth
                elif credential.oauth_client_credentials and isinstance(
                    credential.oauth_client_credentials, credential_type
                ):
                    return credential.oauth_client_credentials
                elif credential.basic and isinstance(credential.basic, credential_type):
                    return credential.basic
                elif credential.token and isinstance(credential.token, credential_type):
                    return credential.token
                elif credential.jwt and isinstance(credential.jwt, credential_type):
                    return credential.jwt

                raise ConnectorError(
                    message=f"Credential '{credential_id}' found but is not of type {credential_type}.",
                    error_code=ErrorCode.BAD_REQUEST,
                )

    raise ConnectorError(
        message=f"Credential '{credential_id}' not provided in credentials.",
        error_code=ErrorCode.BAD_REQUEST,
    )


def get_oauth(request: Request) -> OAuthCredential | OAuthClientCredential:
    """
    Either get the (valid) request.auth as an OAuth credential, or throw an error.
    """
    if request.auth and request.auth.oauth and isinstance(request.auth.oauth, OAuthCredential):
        return request.auth.oauth
    if (
        request.auth
        and request.auth.oauth_client_credentials
        and isinstance(request.auth.oauth_client_credentials, OAuthClientCredential)
    ):
        return request.auth.oauth_client_credentials

    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_oauth_1(request: Request) -> OAuth1Credential:
    """
    Either get the (valid) request.auth as an OAuth1 credential, or throw an error.
    """
    if request.auth and request.auth.oauth1 and isinstance(request.auth.oauth1, OAuth1Credential):
        return request.auth.oauth1
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_basic_auth(request: Request) -> BasicCredential:
    """
    Either get the (valid) request.auth as a basic credential, or throw an error.
    """
    if request.auth and request.auth.basic and isinstance(request.auth.basic, BasicCredential):
        return request.auth.basic
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_token_auth(request: Request) -> TokenCredential:
    """
    Either get the (valid) request.auth as a token credential, or throw an error.
    """
    if request.auth and request.auth.token and isinstance(request.auth.token, TokenCredential):
        return request.auth.token
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_jwt_auth(request: Request) -> JWTCredential:
    """
    Either get the (valid) request.auth as a JWT credential, or throw an error.
    """
    if request.auth and request.auth.jwt and isinstance(request.auth.jwt, JWTCredential):
        return request.auth.jwt
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_service_account_auth(request: Request) -> ServiceAccountCredential:
    """
    Either get the (valid) request.auth as a service account credential, or throw an error.
    """
    if (
        request.auth
        and request.auth.service_account
        and isinstance(request.auth.service_account, ServiceAccountCredential)
    ):
        return request.auth.service_account
    raise ConnectorError(message="Wrong auth", error_code=ErrorCode.BAD_REQUEST)


def get_page(request: Request) -> Page:
    """
    Get request.page or a blank one if it isn't set.
    """
    if request.page:
        return request.page
    return Page()


SettingsType = t.TypeVar("SettingsType", bound=BaseModel)


def get_settings(
    request: Request | AuthRequest | AppInfoRequest, model: type[SettingsType]
) -> SettingsType:
    """
    Get a validated Settings type from request.settings.
    """
    try:
        return model.model_validate(request.settings or {})
    except ValidationError as err:
        raise ConnectorError(
            message="Invalid request settings", error_code=ErrorCode.BAD_REQUEST
        ) from err


def extra_data(extra: dict[str, t.Any]) -> dict[str, str]:
    """
    Generate a str:str dict out of arbitrary data for a response.raw_data.
    """
    ret: dict[str, str] = {}
    for key, value in extra.items():
        if value:
            ret[key] = str(value)
    return ret


T = t.TypeVar("T")


class Response(t.Protocol):
    response: t.Any
    raw_data: t.Any | None


_Request = t.TypeVar("_Request", bound=Request, contravariant=True)


class CapabilityCallableProto(t.Protocol, t.Generic[_Request]):
    def __call__(self, args: _Request) -> Response | t.Awaitable[Response]:
        ...

    __name__: str


class CustomRequest(BaseModel, t.Generic[BaseModelType]):
    """
    Generic Request type, extendable for customized capability inputs.

    Example:

    class MyAppCreateAccount(CreateAccount):
      birthday: str

    def create_account(args: CustomRequest[MyAppCreateAccount]) -> CreateAccountResponse:
       ...
    """

    auth: AuthCredential
    credentials: t.Any = None
    page: Page | None = None
    include_raw_data: bool | None = None
    settings: t.Any

    request: BaseModelType


class CustomResponse(BaseModel, t.Generic[BaseModelType]):
    page: Page | None = None
    raw_data: t.Any | None = None

    response: BaseModelType


class Empty(BaseModel):
    pass


def generate_capability_schema(
    impl: (CapabilityCallableProto[t.Any]),
    capability_description: str | None = None,
    full_schema: bool = False,
) -> CapabilitySchema:
    request_annotation, response_annotation = get_capability_annotations(impl)
    request_type = _request_payload_type(request_annotation)
    response_type = _response_payload_type(response_annotation)

    # Old behavior: use Empty for list types when full_schema is False
    if not full_schema:
        request_type = Empty if _is_list(request_type) else request_type
        response_type = Empty if _is_list(response_type) else response_type
        return CapabilitySchema(
            argument=request_type.model_json_schema(),
            output=response_type.model_json_schema(),
            description=capability_description,
        )

    # Get the full payload type
    request_type = _full_payload_type(request_annotation)
    response_type = _full_payload_type(response_annotation)

    # New behavior: handle full schema generation for both simple and list types
    base_request_type = request_type.__args__[0] if _is_list(request_type) else request_type
    base_response_type = response_type.__args__[0] if _is_list(response_type) else response_type

    base_request_schema = base_request_type.model_json_schema(
        ref_template="#/components/schemas/{model}"
    )
    base_response_schema = base_response_type.model_json_schema(
        ref_template="#/components/schemas/{model}"
    )

    request_schema = (
        {
            "type": "array",
            "items": base_request_schema,
            "title": f"Array of {getattr(base_request_type, '__name__', 'Items')}",
        }
        if _is_list(request_type)
        else base_request_schema
    )

    response_schema = (
        {
            "type": "array",
            "items": base_response_schema,
            "title": f"Array of {getattr(base_response_type, '__name__', 'Items')}",
        }
        if _is_list(response_type)
        else base_response_schema
    )

    return CapabilitySchema(
        argument=request_schema,
        output=response_schema,
        description=capability_description,
    )


def get_capability_annotations(
    impl: CapabilityCallableProto[t.Any],
) -> tuple[t.Any, t.Any]:
    """Extract argument and return type annotations."""
    annotations = inspect.get_annotations(impl)
    try:
        response_annotation = annotations["return"]
        request_annotation_name = (set(annotations.keys()) - {"return"}).pop()
    except KeyError:
        raise TypeError(
            f"The capability function {impl.__name__} must have both request and return annotations."
        ) from None

    request_annotation = annotations[request_annotation_name]
    return request_annotation, response_annotation


@dataclass
class CapabilitySignature:
    @dataclass
    class Payload:
        _type: type[BaseModel]
        envelope_type: type[BaseModel]
        is_list: bool
        json_schema: t.Any
        may_be_customized: bool = False

    input_payload: Payload
    output_payload: Payload


def _payload_type_data(
    *, envelope_type: t.Any, is_request: bool, may_be_customized=False
) -> CapabilitySignature.Payload:
    if is_request:
        payload = _request_payload_type(envelope_type)
    else:
        payload = _response_payload_type(envelope_type)
    return CapabilitySignature.Payload(
        envelope_type=envelope_type,
        _type=_pluck_generic_parameter(payload),
        is_list=_is_list(payload),
        json_schema=_pluck_generic_parameter(payload).model_json_schema(),
        may_be_customized=may_be_customized,
    )


def get_capability_signature(
    impl: CapabilityCallableProto[t.Any],
) -> CapabilitySignature:
    """Extract input and return types from a capability impl function."""
    annotations = inspect.get_annotations(impl)
    try:
        response_type = annotations["return"]
        request_annotation_name = (set(annotations.keys()) - {"return"}).pop()
    except KeyError:
        raise TypeError(
            f"The capability function {impl.__name__} must have both request and return annotations."
        ) from None

    return CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=annotations[request_annotation_name], is_request=True
        ),
        output_payload=_payload_type_data(envelope_type=response_type, is_request=False),
    )


def validate_capability(
    capability_name: StandardCapabilityName,
    impl: (CapabilityCallableProto[t.Any]),
) -> None:
    """Make sure capability implementation is valid.

    Capability is marked as valid when:
        * is fully annotated, i.e., both argument and return value are
        type-hinted
        * type of accepted argument matches the expected one, i.e., is
        exactly the same class or a subclass
        * type of returned value matches the expected one, same
        mechanism as for argument
    """
    actual_signature = get_capability_signature(impl)
    expected_signature = _STANDARD_CAPABILITY_SIGNATURES[capability_name]
    for message_name, actual, expected in (
        ("input", actual_signature.input_payload, expected_signature.input_payload),
        ("output", actual_signature.output_payload, expected_signature.output_payload),
    ):
        if actual.is_list != expected.is_list:
            raise TypeError(
                f"{capability_name} {message_name} should {'not ' if not expected.is_list else ''}be a list"
            )
        if not expected.may_be_customized:
            if actual._type != expected._type:
                raise TypeError(
                    f"{capability_name} {message_name} can only be {expected._type.__name__}"
                )
            if actual.envelope_type != expected.envelope_type:
                raise TypeError(
                    f"{capability_name} {message_name} can only be {expected.envelope_type.__name__}"
                )
        else:
            actual_fields = actual.json_schema["properties"]
            expected_fields = expected.json_schema["properties"]
            for property in expected_fields:
                if property not in actual_fields:
                    raise TypeError(
                        f"{capability_name} {message_name} may not drop a field: {property}"
                    )
                if actual_fields[property].get("type", None) != expected_fields[property].get(
                    "type", None
                ):
                    raise TypeError(
                        f"{capability_name} {message_name} may not change the type of {property}"
                    )
            actual_required = set(actual.json_schema.get("required", []))
            expected_required = set(expected.json_schema.get("required", []))
            missing = expected_required - actual_required
            if missing:
                raise TypeError(
                    f"{capability_name} {message_name} doesn't keep as required: {', '.join(sorted(missing))}"
                )


def _full_payload_type(model: type[BaseModelType]) -> type[BaseModelType]:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model


def _request_payload_type(model: type[BaseModel]) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["request"].annotation


def _response_payload_type(model: type[BaseModel]) -> t.Any:
    if not hasattr(model, "model_fields"):
        raise TypeError(f"Not a pydantic model: {model}")
    return model.model_fields["response"].annotation


def _pluck_generic_parameter(type_annotation: t.Any) -> t.Any:
    if hasattr(type_annotation, "__args__"):
        value_type = type_annotation.__args__[-1]
        return value_type
    return type_annotation


def _is_list(type_annotation: t.Any) -> bool:
    """This function is compatible with both list and typing.List
    (which is used in the generated models)"""
    if origin := getattr(type_annotation, "__origin__", None):
        return origin is list
    return type_annotation is list


def capability_requires_authentication(capability: CapabilityCallableProto[t.Any]) -> bool:
    """Check if the capability requires authentication on the request."""
    expected_request, _ = get_capability_annotations(capability)

    # TODO: Later on when "auth" is phased out, we can add the .is_required() check back here
    if "auth" in expected_request.model_fields or "credentials" in expected_request.model_fields:
        return True
    return False


_STANDARD_CAPABILITY_SIGNATURES: dict[StandardCapabilityName, CapabilitySignature] = {
    StandardCapabilityName.APP_INFO: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=AppInfoRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=AppInfoResponse, is_request=False),
    ),
    StandardCapabilityName.GET_AUTHORIZATION_URL: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=GetAuthorizationUrlRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=GetAuthorizationUrlResponse, is_request=False
        ),
    ),
    StandardCapabilityName.GET_LAST_ACTIVITY: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=GetLastActivityRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=GetLastActivityResponse, is_request=False),
    ),
    StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=HandleAuthorizationCallbackRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=HandleAuthorizationCallbackResponse, is_request=False
        ),
    ),
    StandardCapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=HandleClientCredentialsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=HandleClientCredentialsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_ACCOUNTS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListAccountsRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ListAccountsResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_RESOURCES: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListResourcesRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ListResourcesResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_ENTITLEMENTS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListEntitlementsRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ListEntitlementsResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_EXPENSES: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListExpensesRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ListExpensesResponse, is_request=False),
    ),
    StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=FindEntitlementAssociationsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=FindEntitlementAssociationsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListCustomAttributesSchemaRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListCustomAttributesSchemaResponse, is_request=False
        ),
    ),
    StandardCapabilityName.REFRESH_ACCESS_TOKEN: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=RefreshAccessTokenRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=RefreshAccessTokenResponse, is_request=False
        ),
    ),
    StandardCapabilityName.CREATE_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=CreateAccountRequest,
            is_request=True,
            may_be_customized=True,
        ),
        output_payload=_payload_type_data(
            envelope_type=CreateAccountResponse,
            is_request=False,
            may_be_customized=True,
        ),
    ),
    StandardCapabilityName.DELETE_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=DeleteAccountRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=DeleteAccountResponse, is_request=False),
    ),
    StandardCapabilityName.ACTIVATE_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ActivateAccountRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ActivateAccountResponse, is_request=False),
    ),
    StandardCapabilityName.DEACTIVATE_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=DeactivateAccountRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=DeactivateAccountResponse, is_request=False
        ),
    ),
    StandardCapabilityName.ASSIGN_ENTITLEMENT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=AssignEntitlementRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=AssignEntitlementResponse, is_request=False
        ),
    ),
    StandardCapabilityName.UNASSIGN_ENTITLEMENT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=UnassignEntitlementRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=UnassignEntitlementResponse, is_request=False
        ),
    ),
    StandardCapabilityName.UPDATE_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=UpdateAccountRequest, is_request=True, may_be_customized=True
        ),
        output_payload=_payload_type_data(
            envelope_type=UpdateAccountResponse,
            is_request=False,
            may_be_customized=True,
        ),
    ),
    StandardCapabilityName.VALIDATE_CREDENTIALS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ValidateCredentialsRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=ValidateCredentialsResponse, is_request=False
        ),
    ),
}
