"""Utilities for describing capabilities.

Each known capability is assigned a base class for request and response.
The actual request and response types in a integration implementation
can either use the base classes directly or create subclasses, however,
those bases are enforced to be used.
"""

import inspect
import logging
import typing as t
from dataclasses import dataclass

from connector_sdk_types.generated import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    AppInfoRequest,
    AppInfoResponse,
    AssignApplicationEntitlementRequest,
    AssignApplicationEntitlementResponse,
    AssignApplicationRequest,
    AssignApplicationResponse,
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
    DowngradeLicenseRequest,
    DowngradeLicenseResponse,
    ExecutionSummary,
    FindEntitlementAssignmentsRequest,
    FindEntitlementAssignmentsResponse,
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    FindEntitlementGraphRequest,
    FindEntitlementGraphResponse,
    FindResourceGraphRequest,
    FindResourceGraphResponse,
    GetAccountEntitlementAssociationsRequest,
    GetAccountEntitlementAssociationsResponse,
    GetAccountRequest,
    GetAccountResponse,
    GetApplicationAccountRequest,
    GetApplicationAccountResponse,
    GetApplicationRequest,
    GetApplicationResponse,
    GetAuthorizationUrlRequest,
    GetAuthorizationUrlResponse,
    GetDataRecencyRequest,
    GetDataRecencyResponse,
    GetLastActivityRequest,
    GetLastActivityResponse,
    HandleAuthorizationCallbackRequest,
    HandleAuthorizationCallbackResponse,
    HandleClientCredentialsRequest,
    HandleClientCredentialsResponse,
    JWTCredential,
    KeyPairCredential,
    ListAccountsRequest,
    ListAccountsResponse,
    ListActivityRecordsRequest,
    ListActivityRecordsResponse,
    ListApplicationsAccountsRequest,
    ListApplicationsAccountsResponse,
    ListApplicationsActivityRecordsRequest,
    ListApplicationsActivityRecordsResponse,
    ListApplicationsEntitlementAssociationsRequest,
    ListApplicationsEntitlementAssociationsResponse,
    ListApplicationsEntitlementsRequest,
    ListApplicationsEntitlementsResponse,
    ListApplicationsRequest,
    ListApplicationsResourcesRequest,
    ListApplicationsResourcesResponse,
    ListApplicationsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListExpensesRequest,
    ListExpensesResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    ListUpdatedAccountsRequest,
    ListUpdatedAccountsResponse,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    Page,
    RateLimitRequestInfo,
    RateLimitResponseInfo,
    RefreshAccessTokenRequest,
    RefreshAccessTokenResponse,
    ReleaseResourcesRequest,
    ReleaseResourcesResponse,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenCredential,
    TransferDataRequest,
    TransferDataResponse,
    UnassignApplicationEntitlementRequest,
    UnassignApplicationEntitlementResponse,
    UnassignApplicationRequest,
    UnassignApplicationResponse,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    UpdateAccountRequest,
    UpdateAccountResponse,
    ValidateCredentialConfigRequest,
    ValidateCredentialConfigResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
)
from connector_sdk_types.oai.capability import AuthRequest, Request
from pydantic import BaseModel, ValidationError

from connector.oai.errors import InternalError, InvalidConfigurationError, MissingParameterError
from connector.oai.fingerprint import request_fingerprint

BaseModelType = t.TypeVar("BaseModelType", bound=BaseModel)

logger = logging.getLogger("connector.oai.capability")

CredentialType = t.TypeVar(
    "CredentialType",
    OAuthCredential,
    OAuthClientCredential,
    OAuth1Credential,
    BasicCredential,
    TokenCredential,
    JWTCredential,
    KeyPairCredential,
    ServiceAccountCredential,
)

DEFAULT_AUTH_MISSING_MESSAGE = (
    "Wrong auth: required credential for {auth_type} authentication is missing or not configured."
)


@t.overload
def get_credential(
    request: Request,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: t.Literal[False],
) -> CredentialType | None:
    ...


@t.overload
def get_credential(
    request: Request,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: t.Literal[True] = True,
) -> CredentialType:
    ...


@t.overload
def get_credential(
    request: ValidateCredentialConfigRequest,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: t.Literal[False],
) -> CredentialType | None:
    ...


@t.overload
def get_credential(
    request: ValidateCredentialConfigRequest,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: t.Literal[True] = True,
) -> CredentialType:
    ...


def get_credential(
    request: Request | ValidateCredentialConfigRequest,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: bool = True,
) -> CredentialType | None:
    """
    Return the particular credential from the request.
    Similarly to get_settings, the credential is identified by the credential_id and the root credentials model.

    For regular capability requests (Request), this reads request.credentials.
    For validate-config requests (ValidateCredentialConfigRequest), this reads
    request.request.credential.

    When strict=True (default), raises if the credential is missing or has the wrong type.
    When strict=False, returns None instead.

    For validate-config requests specifically, credential ID mismatches are treated
    as invariant violations and always raise InternalError, regardless of strict.
    """
    if isinstance(request, ValidateCredentialConfigRequest):
        return _get_credential_from_validate_config_request(
            request, credential_id, credential_type, strict
        )

    return _get_credential_from_capability_request(request, credential_id, credential_type, strict)


def _extract_typed_credential_payload(
    credential: AuthCredential,
    credential_type: type[CredentialType],
) -> CredentialType | None:
    if credential.oauth and isinstance(credential.oauth, credential_type):
        return credential.oauth
    if credential.oauth_client_credentials and isinstance(
        credential.oauth_client_credentials, credential_type
    ):
        return credential.oauth_client_credentials
    if credential.oauth1 and isinstance(credential.oauth1, credential_type):
        return credential.oauth1
    if credential.basic and isinstance(credential.basic, credential_type):
        return credential.basic
    if credential.token and isinstance(credential.token, credential_type):
        return credential.token
    if credential.jwt and isinstance(credential.jwt, credential_type):
        return credential.jwt
    if credential.service_account and isinstance(credential.service_account, credential_type):
        return credential.service_account
    if credential.key_pair and isinstance(credential.key_pair, credential_type):
        return credential.key_pair
    return None


def _get_credential_from_capability_request(
    request: Request,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: bool,
) -> CredentialType | None:
    if not request.credentials or not isinstance(request.credentials, list):
        logger.warning(f"Credential '{credential_id}' not provided in credentials.")

        if strict:
            raise InvalidConfigurationError(
                message=f"Credential '{credential_id}' not provided in credentials."
            )

        return None

    for credential in request.credentials:
        # Find the credential from the request
        if credential.id != credential_id:
            continue

        payload = _extract_typed_credential_payload(credential, credential_type)
        if payload is not None:
            return payload

        logger.warning(f"Credential '{credential_id}' found but is not of type {credential_type}.")

        if strict:
            raise InvalidConfigurationError(
                message=f"Credential '{credential_id}' found but is not of type {credential_type.__name__}."
            )

        return None

    logger.warning(f"Credential '{credential_id}' not provided in credentials.")

    if strict:
        raise MissingParameterError(
            message=f"Credential '{credential_id}' not provided in credentials."
        )

    return None


def _get_credential_from_validate_config_request(
    request: ValidateCredentialConfigRequest,
    credential_id: str,
    credential_type: type[CredentialType],
    strict: bool,
) -> CredentialType | None:
    credential = request.request.credential

    if not credential.id:
        raise InternalError(
            message=(
                "Credential validation invariant breached: received credential "
                f"without ID, expected '{credential_id}'."
            )
        )

    if credential.id != credential_id:
        raise InternalError(
            message=(
                "Credential validation invariant breached: received credential "
                f"ID '{credential.id}', expected '{credential_id}'."
            )
        )

    payload = _extract_typed_credential_payload(credential, credential_type)
    if payload is not None:
        return payload

    if strict:
        raise InternalError(
            message=(
                "Credential validation invariant breached for "
                f"'{credential_id}': expected payload type '{credential_type.__name__}'."
            )
        )

    logger.warning(
        "Credential '%s' does not contain expected payload type '%s'.",
        credential_id,
        credential_type.__name__,
    )

    return None


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

    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="OAuth 2.0"))


def get_oauth_1(request: Request) -> OAuth1Credential:
    """
    Either get the (valid) request.auth as an OAuth1 credential, or throw an error.
    """
    if request.auth and request.auth.oauth1 and isinstance(request.auth.oauth1, OAuth1Credential):
        return request.auth.oauth1
    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="OAuth 1.0"))


def get_basic_auth(request: Request) -> BasicCredential:
    """
    Either get the (valid) request.auth as a basic credential, or throw an error.
    """
    if request.auth and request.auth.basic and isinstance(request.auth.basic, BasicCredential):
        return request.auth.basic
    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="Basic"))


def get_token_auth(request: Request) -> TokenCredential:
    """
    Either get the (valid) request.auth as a token credential, or throw an error.
    """
    if request.auth and request.auth.token and isinstance(request.auth.token, TokenCredential):
        return request.auth.token
    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="Token"))


def get_jwt_auth(request: Request) -> JWTCredential:
    """
    Either get the (valid) request.auth as a JWT credential, or throw an error.
    """
    if request.auth and request.auth.jwt and isinstance(request.auth.jwt, JWTCredential):
        return request.auth.jwt
    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="JWT"))


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
    raise MissingParameterError(
        message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="Service Account")
    )


def get_key_pair_auth(request: Request) -> KeyPairCredential:
    """
    Either get the (valid) request.auth as a key pair credential, or throw an error.
    """
    if (
        request.auth
        and request.auth.key_pair
        and isinstance(request.auth.key_pair, KeyPairCredential)
    ):
        return request.auth.key_pair
    raise MissingParameterError(message=DEFAULT_AUTH_MISSING_MESSAGE.format(auth_type="Key Pair"))


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
        raise InvalidConfigurationError(message=f"Invalid request settings: {err}") from err


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
    rate_limit: RateLimitResponseInfo | None


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

    auth: AuthCredential | None = None
    credentials: list[AuthCredential] | None = None
    page: Page | None = None
    include_raw_data: bool | None = None
    settings: t.Any
    rate_limit: RateLimitRequestInfo | None = None

    request: BaseModelType

    def fingerprint(self) -> str:
        """
        Generate a stable SHA256 fingerprint of the custom request.
        Only encodes the request payload, excluding page and settings.
        """
        return request_fingerprint(self.request)

    @classmethod
    def model_json_schema(cls, **kwargs) -> dict[str, t.Any]:  # type: ignore[override]
        """
        We need to add x-capability-level to the request model in a way that is compatible with the
        info_module.py. Since the request_model is contained here, we find the ref and add the
        capability leve that way.
        """
        schema = super().model_json_schema(**kwargs)

        request_ref = schema.get("properties", {}).get("request", {}).get("$ref")
        if request_ref and "$defs" in schema:
            request_model_name = request_ref.split("/")[-1]

            # only add to the specific request model
            if request_model_name in schema["$defs"]:
                schema["$defs"][request_model_name]["x-capability-level"] = "write"

        return schema


class CustomResponse(BaseModel, t.Generic[BaseModelType]):
    page: Page | None = None
    raw_data: t.Any | None = None
    execution_summary: ExecutionSummary | None = None
    rate_limit: RateLimitResponseInfo | None = None

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
    StandardCapabilityName.LIST_UPDATED_ACCOUNTS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListUpdatedAccountsRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=ListUpdatedAccountsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_ACTIVITY_RECORDS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListActivityRecordsRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=ListActivityRecordsResponse, is_request=False
        ),
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
    StandardCapabilityName.TRANSFER_DATA: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=TransferDataRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=TransferDataResponse, is_request=False),
    ),
    StandardCapabilityName.RELEASE_RESOURCES: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ReleaseResourcesRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ReleaseResourcesResponse, is_request=False),
    ),
    StandardCapabilityName.DOWNGRADE_LICENSE: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=DowngradeLicenseRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=DowngradeLicenseResponse, is_request=False),
    ),
    StandardCapabilityName.GET_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=GetAccountRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=GetAccountResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_APPLICATIONS: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=ListApplicationsRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=ListApplicationsResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_APPLICATIONS_ACCOUNTS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListApplicationsAccountsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListApplicationsAccountsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_APPLICATIONS_ACTIVITY_RECORDS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListApplicationsActivityRecordsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListApplicationsActivityRecordsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_APPLICATIONS_ENTITLEMENTS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListApplicationsEntitlementsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListApplicationsEntitlementsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.LIST_APPLICATIONS_RESOURCES: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListApplicationsResourcesRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListApplicationsResourcesResponse, is_request=False
        ),
    ),
    StandardCapabilityName.UNASSIGN_APPLICATION: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=UnassignApplicationRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=UnassignApplicationResponse, is_request=False
        ),
    ),
    StandardCapabilityName.ASSIGN_APPLICATION: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=AssignApplicationRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=AssignApplicationResponse, is_request=False
        ),
    ),
    StandardCapabilityName.GET_APPLICATION: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=GetApplicationRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=GetApplicationResponse, is_request=False),
    ),
    StandardCapabilityName.GET_APPLICATION_ACCOUNT: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=GetApplicationAccountRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=GetApplicationAccountResponse, is_request=False
        ),
    ),
    StandardCapabilityName.GET_ACCOUNT_ENTITLEMENT_ASSOCIATIONS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=GetAccountEntitlementAssociationsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=GetAccountEntitlementAssociationsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.GET_DATA_RECENCY: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=GetDataRecencyRequest, is_request=True),
        output_payload=_payload_type_data(envelope_type=GetDataRecencyResponse, is_request=False),
    ),
    StandardCapabilityName.LIST_APPLICATIONS_ENTITLEMENT_ASSOCIATIONS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ListApplicationsEntitlementAssociationsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=ListApplicationsEntitlementAssociationsResponse, is_request=False
        ),
    ),
    StandardCapabilityName.ASSIGN_APPLICATION_ENTITLEMENT: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=AssignApplicationEntitlementRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=AssignApplicationEntitlementResponse, is_request=False
        ),
    ),
    StandardCapabilityName.UNASSIGN_APPLICATION_ENTITLEMENT: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=UnassignApplicationEntitlementRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=UnassignApplicationEntitlementResponse, is_request=False
        ),
    ),
    # Per-credential validation capabilities
    StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=ValidateCredentialConfigRequest,
            is_request=True,
        ),
        output_payload=_payload_type_data(
            envelope_type=ValidateCredentialConfigResponse,
            is_request=False,
        ),
    ),
    # Access Graph capabilities
    StandardCapabilityName.FIND_RESOURCE_GRAPH: CapabilitySignature(
        input_payload=_payload_type_data(envelope_type=FindResourceGraphRequest, is_request=True),
        output_payload=_payload_type_data(
            envelope_type=FindResourceGraphResponse, is_request=False
        ),
    ),
    StandardCapabilityName.FIND_ENTITLEMENT_GRAPH: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=FindEntitlementGraphRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=FindEntitlementGraphResponse, is_request=False
        ),
    ),
    StandardCapabilityName.FIND_ENTITLEMENT_ASSIGNMENTS: CapabilitySignature(
        input_payload=_payload_type_data(
            envelope_type=FindEntitlementAssignmentsRequest, is_request=True
        ),
        output_payload=_payload_type_data(
            envelope_type=FindEntitlementAssignmentsResponse, is_request=False
        ),
    ),
}
