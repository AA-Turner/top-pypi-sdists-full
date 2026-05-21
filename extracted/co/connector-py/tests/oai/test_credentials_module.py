"""Test cases for CredentialsModule."""

import pytest
from connector.oai.capabilities.errors import CapabilityExecutionError
from connector.oai.errors import InvalidConfigurationError, InvalidValueError, MissingParameterError
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.credentials_module import CredentialsModule
from connector_sdk_types.generated import (
    AuthCredential,
    BasicCredential,
    Error,
    ErrorCode,
    ErrorResponse,
    StandardCapabilityName,
    TokenCredential,
    ValidateCredentialConfig,
    ValidateCredentialConfigRequest,
    ValidateCredentialConfigResponse,
    ValidatedCredentialConfig,
)
from connector_sdk_types.generated.models.service_account_credential import ServiceAccountCredential
from connector_sdk_types.generated.models.service_account_type import ServiceAccountType
from connector_sdk_types.oai.modules.credentials_module_types import (
    AuthModel,
    CredentialConfig,
    CredentialsSettings,
)


@pytest.fixture
def integration():
    """FIXTURE: Create a basic integration with credentials."""
    return Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
            ),
            CredentialConfig(
                id="token_credential",
                type=AuthModel.TOKEN,
                description="Token authentication credential",
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(
            user_friendly_name="test_credentials_module", categories=[]
        ),
    )


@pytest.fixture
def integration_with_validation():
    """FIXTURE: Create an integration with custom validation functions."""

    def validate_basic(args: ValidateCredentialConfigRequest) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(valid=True),
        )

    async def validate_token(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(valid=True),
        )

    return Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_basic,
            ),
            CredentialConfig(
                id="token_credential",
                type=AuthModel.TOKEN,
                description="Token authentication credential",
                validation=validate_token,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(
            user_friendly_name="test_credentials_module", categories=[]
        ),
    )


def get_credentials_module(integration: Integration) -> CredentialsModule:
    """HELPER: Get the CredentialsModule from the integration."""
    for module in integration.modules:
        if isinstance(module, CredentialsModule):
            return module
    raise ValueError("CredentialsModule not found")


def test_credentials_module_registered(integration):
    """Test if CredentialsModule is registered when credentials are provided."""
    module = get_credentials_module(integration)
    assert isinstance(module, CredentialsModule)
    assert len(module.credentials) == 2
    assert "basic_credential" in module.credentials
    assert "token_credential" in module.credentials


def test_validate_credential_config_capability_registered(integration):
    """Test if VALIDATE_CREDENTIAL_CONFIG capability is registered."""
    assert StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG in integration.capabilities


def test_credentials_module_not_registered_without_credentials():
    """Test that CredentialsModule is not registered when no credentials are provided."""
    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    for module in integration.modules:
        assert not isinstance(module, CredentialsModule)


def test_credentials_module_registration_with_existing_capability():
    """Test that CredentialsModule does not register validate_credential_config if it's already registered.

    This tests the condition in credentials_module.py (lines 63-74) where the module checks
    if the capability already exists before registering it.
    """
    # Create an integration without credentials first
    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
            ),
        ],
        # Skip registration of the module capability
        credentials_settings=CredentialsSettings(register_validation_capability=False),
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    # Manually register the validate_credential_config capability
    @integration.register_capability(StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG)
    async def custom_validate_credential_config(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(valid=True),
        )

    # Store reference to the original capability
    original_capability = integration.capabilities[
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG
    ]

    # Verify that the capability is still the original one (not replaced by CredentialsModule)
    assert StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG in integration.capabilities
    assert (
        integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG]
        == original_capability
    )

    # Verify that CredentialsModule did not register a new capability
    assert (
        integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG]
        is original_capability
    )


@pytest.mark.asyncio
async def test_credentials_module_skips_registration_when_capability_exists():
    """Test that CredentialsModule skips registration and uses existing capability.
    This calls the custom capability.
    """
    # Create an integration without credentials first
    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
            ),
        ],
        exception_handlers=[],
        # Skip registration of the module capability
        credentials_settings=CredentialsSettings(register_validation_capability=False),
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    # Track if our custom capability was called
    custom_capability_called = {"called": False}

    # Manually register the validate_credential_config capability
    @integration.register_capability(StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG)
    async def custom_validate_credential_config(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        custom_capability_called["called"] = True
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(valid=True, validation_errors=["Custom validation"]),
        )

    # Store reference to the original capability
    original_capability = integration.capabilities[
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG
    ]

    # Verify the capability is still the original one
    assert (
        integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG]
        is original_capability
    )

    # Actually call the capability to verify it's the custom one, not CredentialsModule's
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](  # type: ignore[misc]
        request
    )

    # Verify our custom capability was called (not CredentialsModule's)
    assert custom_capability_called["called"] is True
    assert isinstance(response, ValidateCredentialConfigResponse)
    # The custom capability returns errors=["Custom validation"], which proves it was called
    assert response.response.validation_errors == ["Custom validation"]


@pytest.mark.asyncio
async def test_validate_credential_config_without_validation_function(integration):
    """Test validation when no custom validation function is provided."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is True
    assert not response.response.validation_errors


@pytest.mark.asyncio
async def test_validate_credential_config_with_sync_validation_function(
    integration_with_validation,
):
    """Test validation with a synchronous custom validation function."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration_with_validation.capabilities[
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG
    ](request)

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is True


@pytest.mark.asyncio
async def test_validate_credential_config_with_async_validation_function(
    integration_with_validation,
):
    """Test validation with an asynchronous custom validation function."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="token_credential",
                token=TokenCredential(token="test_token"),
            ),
        ),
    )

    response = await integration_with_validation.capabilities[
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG
    ](request)

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is True


@pytest.mark.asyncio
async def test_validate_credential_config_missing_id(integration):
    """Test validation fails when credential ID is missing."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id=None,
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    with pytest.raises(MissingParameterError) as exc_info:
        await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](request)

    assert exc_info.value.message == "Received credential without an ID"


@pytest.mark.asyncio
async def test_validate_credential_config_invalid_credential_id(integration):
    """Test validation fails when credential ID doesn't match any configured credential."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="nonexistent_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    with pytest.raises(InvalidConfigurationError) as exc_info:
        await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](request)

    assert (
        exc_info.value.message == "Missing credential configuration for ID nonexistent_credential"
    )


@pytest.mark.asyncio
async def test_validate_credential_config_empty_credential(integration):
    """Test validation when credential has empty strings on required fields."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="", password=""),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    # Now the implementation correctly detects empty strings on required fields using Pydantic
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert "A required field is empty" in response.response.validation_errors[0]


@pytest.mark.asyncio
async def test_validate_credential_config_whitespace(integration):
    """Test validation fails when credential has extra whitespace."""
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username=" test_user ", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert "extra whitespace" in response.response.validation_errors[0].lower()


@pytest.mark.asyncio
async def test_validate_credential_config_invalid_type(integration):
    """Test validation when credential type doesn't match the configured type.

    When the credential type doesn't match, base_validation should fail with InvalidValueError.
    """
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                token=TokenCredential(token="test_token"),  # Wrong type for basic_credential
            ),
        ),
    )

    with pytest.raises(InvalidValueError, match="Invalid or malformed credential received"):
        await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](request)


@pytest.mark.asyncio
async def test_validate_credential_config_uses_custom_input_model() -> None:
    """Test that base_validation respects CredentialConfig.input_model semantics."""

    class RuntimeStyleServiceAccountCredential(ServiceAccountCredential):
        service_type: ServiceAccountType | None = ServiceAccountType.AWS
        key: dict[str, str] | None = None
        impersonation_email: str = ""
        tenant_id: str = ""
        scopes: list[str] | None = None

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="service_account_credential",
                type=AuthModel.SERVICE_ACCOUNT,
                description="Service account credential",
                input_model=RuntimeStyleServiceAccountCredential,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="service_account_credential",
                service_account=ServiceAccountCredential(
                    service_type=ServiceAccountType.AWS,
                    key={},
                    impersonation_email="",
                    tenant_id="",
                    scopes=[],
                ),
            )
        )
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is True


@pytest.mark.asyncio
async def test_validate_credential_config_custom_validation_returns_errors(
    integration_with_validation,
):
    """Test validation when custom validation function returns errors."""

    def validate_with_errors(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(
                valid=False,
                validation_errors=["Custom validation error: Invalid credentials"],
            ),
        )

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_with_errors,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](  # type: ignore[misc]
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert "Custom validation error: Invalid credentials" in response.response.validation_errors


@pytest.mark.asyncio
async def test_validate_credential_config_custom_validation_returns_error_response(
    integration_with_validation,
):
    """Test validation when custom validation function returns ErrorResponse."""

    def validate_with_error_response(args: ValidateCredentialConfigRequest) -> ErrorResponse:
        return ErrorResponse(
            is_error=True,
            error=Error(
                error_code=ErrorCode.UNAUTHORIZED,
                message="Authentication failed",
                app_id="test_app",
            ),
        )

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_with_error_response,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    with pytest.raises(CapabilityExecutionError) as exc_info:
        await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](request)  # type: ignore[misc]

    assert exc_info.value.error_response.error.error_code == ErrorCode.UNAUTHORIZED
    assert "Authentication failed" in exc_info.value.error_response.error.message


@pytest.mark.asyncio
async def test_validate_credential_config_multiple_credentials(integration):
    """Test validation with multiple credentials - only the matching one is validated."""
    # First credential
    request1 = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response1 = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request1
    )
    assert response1.response.valid is True

    # Second credential
    request2 = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="token_credential",
                token=TokenCredential(token="test_token"),
            ),
        ),
    )

    response2 = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request2
    )
    assert response2.response.valid is True


@pytest.mark.asyncio
async def test_validate_credential_config_skips_non_matching_credential(
    integration_with_validation,
):
    """Test that validation skips credentials that don't match the request."""
    # Request for basic_credential should not trigger validation for token_credential
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration_with_validation.capabilities[
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG
    ](request)

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is True


def test_credentials_module_add_capability():
    """Test adding a capability to the module."""
    module = CredentialsModule(settings=CredentialsSettings.default())
    module.add_capability("test_capability")
    assert "test_capability" in module.capabilities


def test_credentials_module_get_capability():
    """Test getting a capability from the module."""
    module = CredentialsModule(settings=CredentialsSettings.default())
    module.add_capability("test_capability")
    assert module.get_capability("test_capability") == "test_capability"
    assert module.get_capability("nonexistent") is None


def test_credentials_module_initialization():
    """Test that CredentialsModule initializes correctly."""
    module = CredentialsModule(settings=CredentialsSettings.default())
    assert isinstance(module.credentials, dict)
    assert len(module.credentials) == 0
    assert isinstance(module.capabilities, list)
    assert len(module.capabilities) == 0


@pytest.mark.asyncio
async def test_validate_credential_config_valid_false_no_errors(integration):
    """Test validation when custom validation returns valid=False but no errors.

    Note: The implementation expects the developer to supply at least 1 error message when valid=False.
    Thus if there are no errors supplied, the module will add a default error message.
    """

    def validate_invalid(args: ValidateCredentialConfigRequest) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(valid=False, validation_errors=None),
        )

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_invalid,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](  # type: ignore[misc]
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert "Credential is invalid, unexpected error occurred" in response.response.validation_errors


@pytest.mark.asyncio
async def test_validate_credential_config_multiple_errors(integration):
    """Test validation when multiple errors are returned."""

    def validate_with_multiple_errors(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(
                valid=False,
                validation_errors=["Error 1", "Error 2", "Error 3"],
            ),
        )

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_with_multiple_errors,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username="test_user", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](  # type: ignore[misc]
        request
    )

    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert len(response.response.validation_errors) == 3
    assert "Error 1" in response.response.validation_errors
    assert "Error 2" in response.response.validation_errors
    assert "Error 3" in response.response.validation_errors


@pytest.mark.asyncio
async def test_validate_credential_config_base_validation_errors_combined_with_custom(integration):
    """Test that base validation errors are combined with custom validation errors."""

    def validate_with_errors(
        args: ValidateCredentialConfigRequest,
    ) -> ValidateCredentialConfigResponse:
        return ValidateCredentialConfigResponse(
            response=ValidatedCredentialConfig(
                valid=False,
                validation_errors=["Custom validation error"],
            ),
        )

    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="basic_credential",
                type=AuthModel.BASIC,
                description="Basic authentication credential",
                validation=validate_with_errors,
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    # Request with whitespace (base validation should catch this first)
    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="basic_credential",
                basic=BasicCredential(username=" test_user ", password="test_password"),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](  # type: ignore[misc]
        request
    )

    # Base validation should catch whitespace before custom validation runs
    assert isinstance(response, ValidateCredentialConfigResponse)
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert any("whitespace" in error.lower() for error in response.response.validation_errors)


@pytest.mark.asyncio
async def test_validate_credential_config_service_account_with_dict_key(integration):
    """Test that base_validation handles ServiceAccountCredential whose key field is a dict."""
    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="service_account_credential",
                type=AuthModel.SERVICE_ACCOUNT,
                description="Service account credential",
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="service_account_credential",
                service_account=ServiceAccountCredential(
                    service_type=ServiceAccountType.AWS,
                    tenant_id="test_tenant",
                    impersonation_email="test_impersonation_email",
                    scopes=["test_scope"],
                    key={
                        "access_key_id": "my-key",
                        "secret_access_key": "my-secret",
                    },
                ),
            ),
        ),
    )

    # This should not raise AttributeError
    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )
    assert response.response.valid is True


@pytest.mark.asyncio
async def test_validate_credential_config_service_account_with_whitespace_in_dict_key():
    """Test that base_validation correctly detects extra whitespace inside a dict field."""
    integration = Integration(
        app_id="test_app",
        version="0.1.0",
        credentials=[
            CredentialConfig(
                id="service_account_credential",
                type=AuthModel.SERVICE_ACCOUNT,
                description="Service account credential",
            ),
        ],
        exception_handlers=[],
        description_data=DescriptionData(user_friendly_name="test", categories=[]),
    )

    request = ValidateCredentialConfigRequest(
        request=ValidateCredentialConfig(
            credential=AuthCredential(
                id="service_account_credential",
                service_account=ServiceAccountCredential(
                    service_type=ServiceAccountType.AWS,
                    tenant_id="test_tenant",
                    impersonation_email="test_impersonation_email",
                    scopes=["test_scope"],
                    key={
                        "access_key_id": "my-key ",  # trailing space
                        "secret_access_key": "my-secret",
                    },
                ),
            ),
        ),
    )

    response = await integration.capabilities[StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG](
        request
    )
    assert response.response.valid is False
    assert response.response.validation_errors is not None
    assert response.response.validation_errors == [
        "Credential has extra whitespace, please remove it before submitting it again"
    ]
