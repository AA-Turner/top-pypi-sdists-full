from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

from connector.oai.capabilities.errors import (
    CapabilityError,
    CapabilityExecutionError,
    CapabilityRequestAuthenticationError,
    CapabilityRequestSettingsError,
    CapabilityRequestValidationError,
    CapabilityResponseError,
)
from connector.oai.capabilities.executor import CapabilityExecutor
from connector.observability.instrument import Instrument
from connector.utils.rate_limit_context import RATE_LIMIT_CONTEXT, RATE_LIMIT_RESULT_CONTEXT
from connector_sdk_types.generated import (
    AuthCredential,
    BasicCredential,
    Error,
    ErrorCode,
    ErrorResponse,
    JWTCredential,
    KeyPairCredential,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    RateLimitRequestInfo,
    RateLimitStateSnapshot,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenCredential,
)
from connector_sdk_types.oai.modules.credentials_module_types import (
    AuthModel,
    AuthSetting,
    CredentialConfig,
    CredentialIdCombination,
    EmptySettings,
    OAuthConfig,
)
from pydantic import BaseModel


@dataclass
class CaseCapabilityExecutorSuccessMode:
    executor: CapabilityExecutor[Any, BaseModel]
    serialized_request: str
    expected_response: str


@dataclass
class CaseCapabilityExecutorFailureMode:
    executor: CapabilityExecutor[Any, BaseModel]
    serialized_request: str
    expected_exception_type: type[CapabilityError]
    expected_exception_contains: str | None = None


FAKE_APP_ID = "app_id"


class ExecutorNoFrillsRequest(BaseModel):
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class RequiresAuthenticationRequest(BaseModel):
    credentials: None = None
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class BothAuthRequest(BaseModel):
    auth: str = "auth"
    credentials: str = "credentials"
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class ExecutorSettingsRequest(BaseModel):
    settings: Any = None
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class RequiredSettings(BaseModel):
    data: str


class ValidCredentialsRequest(BaseModel):
    credentials: list[AuthCredential]
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class ValidAuthRequest(BaseModel):
    auth: AuthCredential
    rate_limit: RateLimitRequestInfo | None = None
    request: Any = None


class RateLimitAwareRequest(BaseModel):
    request: ExecutorNoFrillsRequest
    rate_limit: RateLimitRequestInfo | None = None


class RateLimitContextResponse(BaseModel):
    capability_name: str
    capability_level: str
    has_deadline: bool
    last_known_limit: int | None = None


class RateLimitAwareResponse(BaseModel):
    ok: bool
    rate_limit: Any = None


class Fixtures:
    def build_executor(
        self,
        *,
        capability: Callable[..., Any],
        request_validate_json: Callable[[Any], Any],
        capability_name: StandardCapabilityName = StandardCapabilityName.LIST_ACCOUNTS,
        settings_model: type[BaseModel] = EmptySettings,
        auth_setting: AuthSetting | None = None,
        exception_handle: Callable[[Exception], ErrorResponse] | None = None,
        credentials_by_id: dict[str, CredentialConfig | OAuthConfig] | None = None,
        allowed_credentials: list[CredentialIdCombination] | None = None,
    ) -> CapabilityExecutor[Any, BaseModel]:
        return CapabilityExecutor(
            app_id=FAKE_APP_ID,
            capability_name=capability_name,
            capability=capability,
            settings_model=settings_model,
            auth_setting=auth_setting,
            exception_handle=exception_handle or self.exception_handle_simple,
            credentials_by_id=credentials_by_id or {},
            allowed_credentials=allowed_credentials,
            request_validate_json=request_validate_json,
            instrument=Instrument.testing.with_default_rate(
                counter=0,
                timer=0,
                gauge=0,
            ),
        )

    def capability_simple(self, req: ExecutorNoFrillsRequest) -> ExecutorNoFrillsRequest:
        return req

    def capability_requires_auth(
        self, req: RequiresAuthenticationRequest
    ) -> RequiresAuthenticationRequest:
        return req

    def exception_handle_simple(self, exc: Exception) -> ErrorResponse:
        return ErrorResponse(
            is_error=True,
            error=Error(
                message=exc.__class__.__name__,
                error_code=ErrorCode.UNKNOWN_VALUE,
                app_id=FAKE_APP_ID,
            ),
        )


class ExecutorFailureModeCases(Fixtures):
    def case_request_validation_error(self) -> CaseCapabilityExecutorFailureMode:
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_simple,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request="",
            expected_exception_type=CapabilityRequestValidationError,
        )

    def case_request_no_authentication_error(self) -> CaseCapabilityExecutorFailureMode:
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=RequiresAuthenticationRequest.model_validate_json,
            ),
            serialized_request="{}",
            expected_exception_type=CapabilityRequestAuthenticationError,
        )

    def capability_both_auth(self, req: BothAuthRequest) -> BothAuthRequest:
        return req

    def case_both_auth_error(self) -> CaseCapabilityExecutorFailureMode:
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_both_auth,
                request_validate_json=BothAuthRequest.model_validate_json,
            ),
            serialized_request=BothAuthRequest(
                auth="Something",
                credentials="Other",
            ).model_dump_json(),
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Cannot pass credentials and auth in the same request",
        )

    def case_authenticate_unloadable(self) -> CaseCapabilityExecutorFailureMode:
        # This can only happen with patching. We need to use a mock for the
        # request_validate_json to work, but pass in an invalid json object.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request="",
            expected_exception_type=CapabilityRequestValidationError,
            expected_exception_contains="Invalid request, expected JSON input.",
        )

    def case_authenticate_non_object(self) -> CaseCapabilityExecutorFailureMode:
        # This can only happen with patching. We need to use a mock for the
        # request_validate_json to work, but pass in a non-json object.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request="[]",
            expected_exception_type=CapabilityRequestValidationError,
            expected_exception_contains="Invalid request, expected JSON input.",
        )

    def case_credentials_missing_in_request(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a request requires credential authentication but provides
        # an empty list.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request='{"credentials":[]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing credentials in request",
        )

    def case_credentials_malformed(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a specific credential in our list of credentials
        # is malformed.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request='{"credentials":[1]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Malformed credentials in request",
        )

    def case_credentials_missing_id(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a specific credential does not specify an ID.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request='{"credentials":[{}]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing ID in credential at index",
        )

    def case_credentials_unexpected(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a credential specifies an ID but it is not in our
        # executors credentials.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request='{"credentials":[{"id":"1"}]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Credential with id '1' not expected",
        )

    def case_credentials_missing(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a credential specifies an ID and is in our executors
        # credentials, but then the request is missing that credentials data.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                        optional=False,
                    )
                },
            ),
            serialized_request='{"credentials":[{"id":"cred_1"}]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'basic' credential in request",
        )

    def case_allowed_credentials_tuple_unsatisfied_raises_missing(
        self,
    ) -> CaseCapabilityExecutorFailureMode:
        # If an allowed credential combination is expected and required credential
        # auth payloads are missing, the request should be rejected.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                    ),
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="My Other Test Cred",
                    ),
                },
                allowed_credentials=[("cred_1", "cred_2")],
            ),
            serialized_request=(
                '{"credentials":[{"id":"cred_1","basic":{"username":"username","password":"password"}},'
                '{"id":"cred_2"}]}'
            ),
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'token' credential in request",
        )

    def case_allowed_credentials_tuple_unsatisfied_raises_missing_multiple_credentials(
        self,
    ) -> CaseCapabilityExecutorFailureMode:
        # Case like the above, but testing with multiple missing credentials in a combo
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                    ),
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="My Other Test Cred",
                    ),
                    # Not sent at all
                    "cred_3": CredentialConfig(
                        id="cred_3",
                        type=AuthModel.JWT,
                        description="My Third Test Cred",
                    ),
                },
                allowed_credentials=[("cred_1", "cred_2", "cred_3")],
            ),
            serialized_request=(
                '{"credentials":[{"id":"cred_1","basic":{"username":"username","password":"password"}},'
                '{"id":"cred_2"}]}'
            ),
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'token, jwt' credential in request",
        )

    def case_allowed_combinations_fallback_validation_triggered(
        self,
    ) -> CaseCapabilityExecutorFailureMode:
        # Force the executor into the fallback "non-optional must be complete"
        # validation branch.
        executor = self.build_executor(
            capability=self.capability_requires_auth,
            request_validate_json=MagicMock(),
            credentials_by_id={
                "cred_1": CredentialConfig(
                    id="cred_1",
                    type=AuthModel.BASIC,
                    description="My Test Cred",
                    optional=False,
                ),
            },
            allowed_credentials=["cred_1"],
        )
        executor._allowed_credential_id_combinations = []

        return CaseCapabilityExecutorFailureMode(
            executor=executor,
            serialized_request='{"credentials":[{"id":"cred_1"}]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'basic' credential in request",
        )

    def case_allowed_credential_tuple_request_missing_credential(
        self,
    ) -> CaseCapabilityExecutorFailureMode:
        # Covers the `_is_allowed_credential_id_combination_satisfied()` path where
        # connector credential exists, but request did not include it.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                        optional=False,
                    ),
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="My Other Test Cred",
                        optional=False,
                    ),
                },
                allowed_credentials=["cred_2"],
            ),
            serialized_request=(
                '{"credentials":[{"id":"cred_1","basic":{"username":"username","password":"password"}}]}'
            ),
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'token' credential in request",
        )

    def case_allowed_combination_unknown_credential_id_is_skipped(
        self,
    ) -> CaseCapabilityExecutorFailureMode:
        # Covers `_get_allowed_credential_id_combination_missing_types()` where
        # the allowed combo references a credential id not declared on the connector.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                credentials_by_id={
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="My Other Test Cred",
                        optional=False,
                    ),
                },
                allowed_credentials=[("cred_unknown", "cred_2")],
            ),
            serialized_request='{"credentials":[{"id":"cred_2"}]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'token' credential in request",
        )

    def case_auth_malformed(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when there is an "auth" field in the request, but
        # the data is malformed.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
            ),
            serialized_request='{"auth":[]}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Malformed credentials in request",
        )

    def case_auth_missing_oauth(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for oauth credentials, but
        # the oauth field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=OAuthCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'oauth' auth in request",
        )

    def case_auth_missing_oauth_client_credentials(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for oauth credentials, but
        # the oauth field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=OAuthClientCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'oauth_client_credentials' auth in request",
        )

    def case_auth_missing_oauth1(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for oauth credentials, but
        # the oauth field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=OAuth1Credential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'oauth1' auth in request",
        )

    def case_auth_missing_basic(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for basic credentials, but
        # the basic field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=BasicCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'basic' auth in request",
        )

    def case_auth_missing_token(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for basic credentials, but
        # the basic field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=TokenCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'token' auth in request",
        )

    def case_auth_missing_jwt(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for basic credentials, but
        # the basic field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=JWTCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'jwt' auth in request",
        )

    def case_auth_missing_service_account(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for basic credentials, but
        # the basic field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=ServiceAccountCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'service_account' auth in request",
        )

    def case_auth_missing_key_pair(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when the auth setting is for key-pair credentials, but
        # the key_pair field is missing.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=MagicMock(),
                auth_setting=KeyPairCredential,
            ),
            serialized_request='{"auth": {}}',
            expected_exception_type=CapabilityRequestAuthenticationError,
            expected_exception_contains="Missing 'key_pair' auth in request",
        )

    def case_settings_not_in_request(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when setting validation is required, but there is no
        # data in the settings of the request.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_simple,
                request_validate_json=ExecutorSettingsRequest.model_validate_json,
                settings_model=BaseModel,
            ),
            serialized_request="{}",
            expected_exception_type=CapabilityRequestSettingsError,
            expected_exception_contains="No settings passed on request",
        )

    def case_settings_invalid(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when setting validation is required and there is
        # data in the settings of the request, but the data is invalid.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_simple,
                request_validate_json=ExecutorSettingsRequest.model_validate_json,
                settings_model=RequiredSettings,
            ),
            serialized_request='{"settings":{"data":1}}',
            expected_exception_type=CapabilityRequestSettingsError,
            expected_exception_contains="Invalid settings passed on request.",
        )

    def case_settings_missing_titles(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when setting validation is required and there is
        # data in the settings of the request, but the data is Invalid
        # because of missing required fields.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_simple,
                request_validate_json=ExecutorSettingsRequest.model_validate_json,
                settings_model=RequiredSettings,
            ),
            serialized_request='{"settings":{}}',
            expected_exception_type=CapabilityRequestSettingsError,
            expected_exception_contains="Missing required settings:",
        )

    def capability_raises(self, _: ExecutorNoFrillsRequest) -> RequiresAuthenticationRequest:
        raise NameError("Whoops")

    def case_execution_exception(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a capability is executed and fails.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_raises,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request="{}",
            expected_exception_type=CapabilityExecutionError,
            expected_exception_contains="NameError",
        )

    def capability_bad_response(self, _: ExecutorNoFrillsRequest) -> str:
        return "whoops"

    def case_execution_response_invalid(self) -> CaseCapabilityExecutorFailureMode:
        # This happens when a capability is executed successfully, but its response
        # is not a pydantic model.
        return CaseCapabilityExecutorFailureMode(
            executor=self.build_executor(
                capability=self.capability_bad_response,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request="{}",
            expected_exception_type=CapabilityResponseError,
        )


class ExecutorSuccessModeCases(Fixtures):
    def case_valid_sync_request(self) -> CaseCapabilityExecutorSuccessMode:
        req = ExecutorNoFrillsRequest().model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_simple,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request=req,
            expected_response=req,
        )

    async def capability_simple_async(
        self, req: ExecutorNoFrillsRequest
    ) -> ExecutorNoFrillsRequest:
        return req

    def case_valid_async_request(self) -> CaseCapabilityExecutorSuccessMode:
        req = ExecutorNoFrillsRequest().model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_simple_async,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_valid_no_verification_request(self) -> CaseCapabilityExecutorSuccessMode:
        req = ExecutorNoFrillsRequest().model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_simple_async,
                capability_name=StandardCapabilityName.APP_INFO,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_valid_settings_request(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_simple_async,
                capability_name=StandardCapabilityName.APP_INFO,
                request_validate_json=ExecutorSettingsRequest.model_validate_json,
                settings_model=RequiredSettings,
            ),
            serialized_request='{"settings":{"data":"setting_1"}}',
            expected_response='{"settings":{"data":"setting_1"},"rate_limit":null,"request":null}',
        )

    def capability_valid_credentials(self, req: ValidCredentialsRequest) -> ValidCredentialsRequest:
        return req

    def case_valid_credentials_request(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        req = ValidCredentialsRequest(
            credentials=[
                AuthCredential(
                    id="cred_1",
                    basic=BasicCredential(
                        username="username",
                        password="password",
                    ),
                )
            ]
        ).model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=ValidCredentialsRequest.model_validate_json,
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                        optional=False,
                    )
                },
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_allowed_credentials_satisfied_ignores_incomplete_other_credentials(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        # When a satisfied allowed combination exists, the executor should accept
        # the request even if other provided credential objects are incomplete.
        req = ValidCredentialsRequest(
            credentials=[
                AuthCredential(
                    id="cred_1",
                    basic=BasicCredential(
                        username="username",
                        password="password",
                    ),
                ),
                AuthCredential(
                    id="cred_2",
                ),
            ]
        ).model_dump_json()

        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_valid_credentials,
                request_validate_json=ValidCredentialsRequest.model_validate_json,
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                        optional=False,
                    ),
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="My Other Test Cred",
                        optional=False,
                    ),
                },
                allowed_credentials=["cred_1"],
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_duplicate_credentials_prefers_complete_payload(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        # Covers the duplicate-credential replacement logic: if the request includes
        # two entries for the same credential id, prefer the one that includes the
        # required auth payload.
        req = ValidCredentialsRequest(
            credentials=[
                AuthCredential(id="cred_1"),
                AuthCredential(
                    id="cred_1",
                    basic=BasicCredential(
                        username="username",
                        password="password",
                    ),
                ),
            ]
        ).model_dump_json()

        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_valid_credentials,
                request_validate_json=ValidCredentialsRequest.model_validate_json,
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="My Test Cred",
                        optional=False,
                    ),
                },
                allowed_credentials=["cred_1"],
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_inferred_allowed_credentials_allows_optional_singleton(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        # If `allowed_credentials` is not provided, we infer combinations from
        # `CredentialConfig.optional` (mirroring the schema behavior).
        req = ValidCredentialsRequest(
            credentials=[
                AuthCredential(
                    id="cred_2",
                    token=TokenCredential(token="some_token"),
                )
            ]
        ).model_dump_json()

        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_valid_credentials,
                request_validate_json=ValidCredentialsRequest.model_validate_json,
                credentials_by_id={
                    "cred_1": CredentialConfig(
                        id="cred_1",
                        type=AuthModel.BASIC,
                        description="Required Test Cred",
                        optional=False,
                    ),
                    "cred_2": CredentialConfig(
                        id="cred_2",
                        type=AuthModel.TOKEN,
                        description="Optional Test Cred",
                        optional=True,
                    ),
                },
                allowed_credentials=[],
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_valid_auth_basic_request(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        req = ValidAuthRequest(
            auth=AuthCredential(
                id="cred_1",
                basic=BasicCredential(
                    username="username",
                    password="password",
                ),
            )
        ).model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=ValidAuthRequest.model_validate_json,
                auth_setting=BasicCredential,
            ),
            serialized_request=req,
            expected_response=req,
        )

    def case_valid_auth_oauth_request(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        req = ValidAuthRequest(
            auth=AuthCredential(
                id="cred_1", oauth=OAuthCredential(access_token="some_access_token")
            )
        ).model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_requires_auth,
                request_validate_json=ValidAuthRequest.model_validate_json,
                auth_setting=OAuthCredential,
            ),
            serialized_request=req,
            expected_response=req,
        )

    def capability_reports_rate_limit_context(
        self, req: RateLimitAwareRequest
    ) -> RateLimitContextResponse:
        del req
        context = RATE_LIMIT_CONTEXT.get()
        assert context is not None

        last_known_limit = None
        if context.last_known_state is not None:
            first = next(iter(context.last_known_state.values()), None)
            last_known_limit = first.limit if first is not None else None

        return RateLimitContextResponse(
            capability_name=str(context.capability_name),
            capability_level=context.capability_level,
            has_deadline=context.deadline is not None,
            last_known_limit=last_known_limit,
        )

    def case_request_rate_limit_context_is_available_to_capability(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        req = RateLimitAwareRequest(
            request=ExecutorNoFrillsRequest(),
            rate_limit=RateLimitRequestInfo(
                max_execution_time=15,
                last_known_state={
                    FAKE_APP_ID: RateLimitStateSnapshot(
                        limit=123,
                        window_seconds=60,
                        current_delay=2,
                    )
                },
            ),
        ).model_dump_json()
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_reports_rate_limit_context,
                request_validate_json=RateLimitAwareRequest.model_validate_json,
            ),
            serialized_request=req,
            expected_response=(
                '{"capability_name":"StandardCapabilityName.LIST_ACCOUNTS",'
                '"capability_level":"read",'
                '"has_deadline":true,"last_known_limit":123}'
            ),
        )

    def capability_sets_rate_limit_result(
        self, req: ExecutorNoFrillsRequest
    ) -> RateLimitAwareResponse:
        del req
        RATE_LIMIT_RESULT_CONTEXT.set(
            {
                FAKE_APP_ID: RateLimitStateSnapshot(
                    remaining=7,
                    limit=50,
                    window_seconds=30,
                    current_delay=1,
                )
            }
        )
        return RateLimitAwareResponse(ok=True)

    def case_rate_limit_result_context_is_attached_to_response(
        self,
    ) -> CaseCapabilityExecutorSuccessMode:
        snapshot_json = '"remaining":7,"limit":50,"reset":null,"window_seconds":30,"current_delay":1,"source":null'
        expected = f'{{"ok":true,"rate_limit":{{"current_state":{{"{FAKE_APP_ID}":{{{snapshot_json}}}}}}}}}'
        return CaseCapabilityExecutorSuccessMode(
            executor=self.build_executor(
                capability=self.capability_sets_rate_limit_result,
                request_validate_json=ExecutorNoFrillsRequest.model_validate_json,
            ),
            serialized_request=ExecutorNoFrillsRequest().model_dump_json(),
            expected_response=expected,
        )
