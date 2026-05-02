import json
import re
from collections.abc import Callable, Mapping, Sequence
from functools import cached_property
from inspect import isawaitable
from typing import Any, ClassVar, Generic, Literal, TypeVar, cast

from connector_sdk_types.generated import (
    AuthCredential,
    BasicCredential,
    ErrorResponse,
    JWTCredential,
    KeyPairCredential,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenCredential,
)
from connector_sdk_types.oai.capability import Request
from connector_sdk_types.oai.modules.credentials_module_types import (
    AuthSetting,
    CredentialConfig,
    CredentialIdCombination,
    EmptySettings,
    OAuthConfig,
)
from pydantic import BaseModel, ValidationError

from connector.oai.capability import (
    CapabilityCallableProto,
    Response,
    capability_requires_authentication,
)
from connector.observability.instrument import Instrument
from connector.utils.validation_utils import get_missing_field_titles

from .errors import (
    CapabilityExecutionError,
    CapabilityRequestAuthenticationError,
    CapabilityRequestSettingsError,
    CapabilityRequestValidationError,
    CapabilityResponseError,
)

REQUEST = TypeVar("REQUEST", bound=Request)
SETTINGS = TypeVar("SETTINGS", bound=BaseModel)


CredentialAttrName = Literal[
    "oauth",
    "oauth_client_credentials",
    "oauth1",
    "basic",
    "token",
    "jwt",
    "service_account",
    "key_pair",
]
"""A literal of the attribute names for supported auth credential types."""


AuthSettingCredentialMap = Mapping[AuthSetting | None, CredentialAttrName]
"""A mapping from supported credential types to the name of the attribute storing that credential.

Note that `None` should not map to a value, but is added to the type to allow for simplified `get()` operations.
"""


def pascalcase_to_snakecase(value: str) -> str:
    """
    Convert a PascalCase or camelCase string to snake_case.
    """
    # Insert underscore before capital letters and lowercase the string
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    snake = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


class CapabilityExecutor(Generic[REQUEST, SETTINGS]):
    """Executes an integration capability."""

    CREDENTIAL_TYPE_TO_ATTR_NAME: ClassVar[AuthSettingCredentialMap] = {
        OAuthCredential: "oauth",
        OAuthClientCredential: "oauth_client_credentials",
        OAuth1Credential: "oauth1",
        BasicCredential: "basic",
        TokenCredential: "token",
        JWTCredential: "jwt",
        ServiceAccountCredential: "service_account",
        KeyPairCredential: "key_pair",
    }
    """An exhaustive mapping from supported credential types to the name
    of the attribute storing that credential.
    """

    def __init__(
        self,
        *,
        app_id: str,
        capability_name: str,
        capability: CapabilityCallableProto[REQUEST],
        credentials_by_id: dict[str, CredentialConfig | OAuthConfig],
        allowed_credentials: Sequence[CredentialIdCombination] | None,
        settings_model: type[SETTINGS],
        auth_setting: AuthSetting | None,
        exception_handle: Callable[[Exception], ErrorResponse],
        request_validate_json: Callable[[Any], REQUEST],
        instrument: Instrument,
    ) -> None:
        self._app_id = app_id
        self._name = capability_name
        self._capability = capability
        self._credentials_by_id = credentials_by_id
        self._allowed_credential_id_combinations = self._get_allowed_credential_id_combinations(
            allowed_credentials=allowed_credentials
        )
        self._settings_model = settings_model
        self._auth_setting = auth_setting
        self._exception_handle = exception_handle
        self._request_validate_json = request_validate_json
        self._instrument = instrument

    def _normalize_allowed_credential_id_combinations(
        self,
        allowed_credentials: Sequence[CredentialIdCombination],
    ) -> list[CredentialIdCombination]:
        """
        Normalize `allowed_credentials` into a list of CredentialIdCombination.
        """
        normalized_allowed_credentials: list[CredentialIdCombination] = []
        for allowed_credential_combination in allowed_credentials:
            if isinstance(allowed_credential_combination, str):
                normalized_allowed_credentials.append((allowed_credential_combination,))
            else:
                normalized_allowed_credentials.append(allowed_credential_combination)
        return normalized_allowed_credentials

    def _get_allowed_credential_id_combinations(
        self,
        allowed_credentials: Sequence[CredentialIdCombination] | None,
    ) -> list[CredentialIdCombination]:
        """
        Normalize explicit `allowed_credentials` into combinations.
        If `allowed_credentials` is empty, infer combinations from
        `CredentialConfig.optional` to match the schema logic in `info_module.py`.
        """
        if allowed_credentials:
            return self._normalize_allowed_credential_id_combinations(allowed_credentials)

        required_credential_ids: list[str] = []
        optional_credential_ids: list[str] = []
        for credential_id, connector_credential in self._credentials_by_id.items():
            if connector_credential.optional:
                optional_credential_ids.append(credential_id)
                continue

            required_credential_ids.append(credential_id)

        allowed_combinations: list[CredentialIdCombination] = []
        if required_credential_ids:
            allowed_combinations.append(tuple(required_credential_ids))
        for credential_id in optional_credential_ids:
            allowed_combinations.append((credential_id,))

        return allowed_combinations

    def _is_credential_complete_for_connector_config(
        self,
        *,
        connector_credential: CredentialConfig | OAuthConfig,
        request_credential: AuthCredential,
    ) -> bool:
        """A connector credential is complete if its auth payload is present."""
        return getattr(request_credential, connector_credential.type) is not None

    def _is_allowed_credential_id_combination_satisfied(
        self,
        *,
        allowed_combination: CredentialIdCombination,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> bool:
        for credential_id in allowed_combination:
            connector_credential = self._credentials_by_id.get(credential_id)
            if connector_credential is None:
                return False

            request_credential = request_credentials_by_id.get(credential_id)
            if request_credential is None:
                return False

            if not self._is_credential_complete_for_connector_config(
                connector_credential=connector_credential,
                request_credential=request_credential,
            ):
                return False

        return True

    def _get_allowed_credential_id_combination_missing_types(
        self,
        *,
        allowed_combination: CredentialIdCombination,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> list[str]:
        missing: list[str] = []
        for credential_id in allowed_combination:
            connector_credential = self._credentials_by_id.get(credential_id)
            if connector_credential is None:
                continue
            request_credential = request_credentials_by_id.get(credential_id)
            if request_credential is None or not self._is_credential_complete_for_connector_config(
                connector_credential=connector_credential,
                request_credential=request_credential,
            ):
                missing.append(connector_credential.type.value)

        return missing

    @cached_property
    def _requires_authentication(self) -> bool:
        """Determines if this capability requires authentication."""

        # WARN: AUTHENTICATION IS NOT ENABLED FOR THE APP INFO CAPABILITY!
        # Since this is not migrated yet, we just flat out skip is_app_info_call
        # In the future we can re-instate the is_required() checks inside this
        # validation and make this work for is_app_info_call automatically (its
        # not required for is_app_info_call)
        if self._name == StandardCapabilityName.APP_INFO:
            return False

        return capability_requires_authentication(self._capability)

    @cached_property
    def _requires_settings_validation(self) -> bool:
        """Determines if this capability requires settings validation."""

        # WARN: SETTINGS VALIDATION IS NOT ENABLED FOR THE APP INFO CAPABILITY!
        # Since this is not migrated yet, we just flat out skip is_app_info_call
        # In the future we can re-instate the is_required() checks inside this
        # validation and make this work for is_app_info_call automatically (its
        # not required for is_app_info_call)
        if self._name == StandardCapabilityName.APP_INFO:
            return False

        return self._settings_model != EmptySettings

    # TODO: Capture observability stats on errors.
    async def execute(self, serialized_request: str) -> str:
        """
        Executes the capability for the provided request.

        Raises:
            CapabilityError: If the capability could not be executed sucessfully.
        """
        self._instrument.calls.incr()

        self._instrument.request.bytes.distribution(len(serialized_request.encode()))
        with self._instrument.request.parse.latency_ms.timer():
            request = self._parse_request(serialized_request)

        with self._instrument.settings.validate.latency_ms.timer():
            if self._requires_settings_validation:
                self._validate_settings(request.settings)

        try:
            with self._instrument.execute.latency_ms.timer():
                response = await self._execute(request)
        except Exception as exc:
            self._instrument.errors.tags(
                stage="execution",
                error_code=pascalcase_to_snakecase(exc.__class__.__name__),
            ).incr()
            handled_exception_response = self._exception_handle(exc)
            raise CapabilityExecutionError(error_response=handled_exception_response) from exc

        if not isinstance(response, BaseModel):
            self._instrument.errors.tags(
                stage="response_validation",
                error_code="invalid",
            ).incr()
            raise CapabilityResponseError(self._app_id)

        with self._instrument.response.serialization.timer():
            serialized_response = response.model_dump_json()

        self._instrument.response.bytes.distribution(len(serialized_response.encode()))
        return serialized_response

    async def _execute(self, request: REQUEST) -> Response:
        """A light-weight wrapper for capability execution."""
        result = self._capability(request)
        if isawaitable(result):
            return await result

        return cast(Response, result)

    def _validate_settings(self, request_settings: Any) -> None:
        """Validates the request settings based on the integrations requirements."""

        if request_settings is None:
            self._instrument.errors.tags(
                stage="settings_validation",
                error_code="missing",
            ).incr()
            raise CapabilityRequestSettingsError(
                self._app_id,
                message=(
                    f"No settings passed on request: {self._app_id} "
                    f"requires {self._settings_model.__name__}"
                ),
            )

        try:
            self._settings_model.model_validate(request_settings)
        except ValidationError as exc:
            self._instrument.errors.tags(
                stage="settings_validation",
                error_code="invalid",
            ).incr()
            message = "Invalid settings passed on request."

            # Check if the validation error is due to missing required fields
            missing_titles, _ = get_missing_field_titles(exc, self._settings_model)
            if missing_titles:
                missing = ", ".join(missing_titles)
                message = f"{message} Missing required settings: {missing}"

            raise CapabilityRequestSettingsError(self._app_id, message=message) from exc

    def _parse_request(self, serialized_request: str) -> REQUEST:
        """Parses a json-compatible string into an instance of this capabilities
        request type.

        Raises:
            CapabilityRequestDecodeError: If the capability request cannot be decoded.
        """
        try:
            request = self._request_validate_json(serialized_request)
        except ValidationError as exc:
            self._instrument.errors.tags(
                stage="parsing",
                error_code="invalid",
            ).incr()
            raise CapabilityRequestValidationError(
                self._app_id,
                message=f"Invalid request - {repr(exc.errors())}",
            ) from exc

        if self._requires_authentication:
            self._authenticate_request(serialized_request)

        return request

    def _authenticate_request(self, serialized_request: str) -> None:
        """Authenticates a capability request.

        Raises:
            CapabilityRequestDecodeError: If the capability request cannot be decoded.
            CapabilityAuthenticationError: If the request could not be authenticated.
        """

        # PERF: (Austin Ward | 10-01-25)
        # Since the `Request` type expects each capability request to have
        # an `auth` and `credentials` field, it's unlikely we need to perform
        # this duplicate deserialization (first on the model, then into
        # json-compatible python). However, for backwards compatibility, we'll
        # continue performing authentication against the json object.
        # The only way this would not be backwards compatible is if the
        # serialized request contains credentials and auth data, but the fields
        # do not exist in the model. However, if that was the case, then the
        # request would not require authentication, based on the logic in
        # `capability_requires_authentication`.
        try:
            deserialized_request = json.loads(serialized_request)
        except json.JSONDecodeError as exc:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="unloadable",
            ).incr()
            raise CapabilityRequestValidationError(self._app_id) from exc

        if not isinstance(deserialized_request, dict):
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="non_object",
            ).incr()
            raise CapabilityRequestValidationError(self._app_id)

        request_credentials = deserialized_request.get("credentials")
        request_auth = deserialized_request.get("auth")

        # If the request includes both credentials and auth fields, it's
        # considered invalid.
        if request_credentials is not None and request_auth is not None:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="both_creds_and_auth",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message=(
                    "Cannot pass credentials and auth in the same request, "
                    "if you've meant to make this connector multi-auth "
                    "compatible, please remove the auth field."
                ),
            )

        if request_credentials is not None:
            self._validate_request_credentials(request_credentials)
            return

        if request_auth is not None:
            self._validate_request_auth(request_auth)
            return

        # If the request includes neither credentials or auth fields, it's
        # considered invalid.
        raise CapabilityRequestAuthenticationError(self._app_id)

    def _validate_request_credentials(self, request_credentials: Any) -> Any:
        """Authenticates the request credentials."""

        if len(request_credentials) == 0:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="credentials.missing",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id, message="Missing credentials in request"
            )

        request_credentials_by_id: dict[str, AuthCredential] = {}
        for index, serialized_credential in enumerate(request_credentials):
            credential_id, credential = self._validate_request_credential(
                index, serialized_credential
            )
            connector_credential = self._credentials_by_id[credential_id]

            existing = request_credentials_by_id.get(credential_id)
            if existing is None:
                request_credentials_by_id[credential_id] = credential
                continue

            # If a duplicate credential object is provided, prefer the one that is complete
            # for its configured type.
            if (
                getattr(existing, connector_credential.type) is None
                and getattr(credential, connector_credential.type) is not None
            ):
                request_credentials_by_id[credential_id] = credential

        self._validate_allowed_credential_id_combinations(request_credentials_by_id)

    def _validate_allowed_credential_id_combinations(
        self,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> None:
        """Validate request credentials against allowed credential combinations."""
        if not self._allowed_credential_id_combinations:
            # Fallback to validating based on `optional` flag
            self._validate_required_credentials_without_combinations(request_credentials_by_id)
            return

        # If at least one allowed combination is satisfied, it is valid
        if self._has_satisfied_allowed_combination(request_credentials_by_id):
            return

        # If no allowed combination is satisfied, raise an error with the missing credential types
        self._raise_missing_credentials_for_closest_combination(request_credentials_by_id)

    def _validate_required_credentials_without_combinations(
        self,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> None:
        """Fallback validation when there are no allowed credential combinations."""
        for credential_id, request_credential in request_credentials_by_id.items():
            connector_credential = self._credentials_by_id.get(credential_id)
            if connector_credential is None:
                continue

            if (
                not connector_credential.optional
                and getattr(request_credential, connector_credential.type) is None
            ):
                self._instrument.errors.tags(
                    stage="auth_validation",
                    error_code=f"credentials.missing.{connector_credential.type.value}",
                ).incr()
                raise CapabilityRequestAuthenticationError(
                    self._app_id,
                    message=f"Missing '{connector_credential.type.value}' credential in request",
                )

    def _has_satisfied_allowed_combination(
        self,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> bool:
        """Return True when at least one allowed combination is fully satisfied."""
        for allowed_combination in self._allowed_credential_id_combinations:
            if self._is_allowed_credential_id_combination_satisfied(
                allowed_combination=allowed_combination,
                request_credentials_by_id=request_credentials_by_id,
            ):
                return True
        return False

    def _get_primary_missing_types_for_allowed_combinations(
        self,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> list[str]:
        """Find the smallest set of missing credential types across combinations."""
        primary_missing_types: list[str] = []
        for allowed_combination in self._allowed_credential_id_combinations:
            missing_types = self._get_allowed_credential_id_combination_missing_types(
                allowed_combination=allowed_combination,
                request_credentials_by_id=request_credentials_by_id,
            )
            if not primary_missing_types or len(missing_types) < len(primary_missing_types):
                primary_missing_types = missing_types
        return primary_missing_types

    def _raise_missing_credentials_for_closest_combination(
        self,
        request_credentials_by_id: dict[str, AuthCredential],
    ) -> None:
        """Raise an auth error with missing types for the closest allowed combination."""
        primary_missing_types = self._get_primary_missing_types_for_allowed_combinations(
            request_credentials_by_id
        )
        if not primary_missing_types:
            raise CapabilityRequestAuthenticationError(self._app_id)

        self._instrument.errors.tags(
            stage="auth_validation",
            error_code=f"credentials.missing.{primary_missing_types[0]}",
        ).incr()
        missing_type = ", ".join(primary_missing_types)
        raise CapabilityRequestAuthenticationError(
            self._app_id,
            message=f"Missing '{missing_type}' credential in request",
        )

    def _validate_request_credential(
        self,
        credential_index: int,
        serialized_credential: Any,
    ) -> tuple[str, AuthCredential]:
        """Parses a serialized credential into an auth credential, validating
        against the expected credential identifiers.

        Raises:
            CapabilityAuthenticationError: If the credential is invalid.
        """
        try:
            credential = AuthCredential.model_validate(serialized_credential)
        except ValidationError as exc:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="credentials.malformed",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message="Malformed credentials in request",
            ) from exc

        if not credential.id:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="credentials.missing_id",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message=f"Missing ID in credential at index {credential_index}",
            )

        # All request credentials must exist on the connector.
        connector_credential = self._credentials_by_id.get(credential.id)
        if connector_credential is None:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="credentials.invalid_id",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message=f"Credential with id '{credential.id}' not expected",
            )

        return credential.id, credential

    def _validate_request_auth(self, request_auth: Any) -> None:
        """Authenticates the request auth."""
        # PERF: As I understand it, this credential validation should
        # occur on the request model itself. If this is true, then this
        # extra validation is unecessary. We can add instrumentation to
        # validate this.
        try:
            auth_credential = AuthCredential.model_validate(request_auth)
        except ValidationError as exc:
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="auth.malformed",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message="Malformed credentials in request",
            ) from exc

        credential_attr_name = self.CREDENTIAL_TYPE_TO_ATTR_NAME.get(
            self._auth_setting,
        )
        if credential_attr_name and not getattr(auth_credential, credential_attr_name):
            self._instrument.errors.tags(
                stage="auth_validation",
                error_code="auth.missing",
            ).incr()
            raise CapabilityRequestAuthenticationError(
                self._app_id,
                message=f"Missing '{credential_attr_name}' auth in request",
            )
