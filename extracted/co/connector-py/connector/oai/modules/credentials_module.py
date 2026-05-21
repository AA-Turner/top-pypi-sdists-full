import inspect
from collections.abc import Awaitable, Sequence
from typing import TYPE_CHECKING, Any, cast

from connector_sdk_types.generated import (
    ErrorResponse,
    StandardCapabilityName,
    ValidateCredentialConfigRequest,
    ValidateCredentialConfigResponse,
    ValidatedCredentialConfig,
)
from connector_sdk_types.oai.modules.credentials_module_types import (
    AUTH_TYPE_MAP,
    CredentialConfig,
    CredentialsSettings,
    OAuthConfig,
    ValidateCredentialConfigCallable,
)
from pydantic import BaseModel, ValidationError

from connector.oai.capabilities.errors import CapabilityExecutionError
from connector.oai.errors import InvalidConfigurationError, InvalidValueError, MissingParameterError
from connector.oai.modules.base_module import BaseIntegrationModule

if TYPE_CHECKING:
    from connector.oai.integration import Integration


class CredentialsModule(BaseIntegrationModule):
    """
    Credentials module is responsible for handling the credentials for an Integration.
    It can register the following capabilities:
    - VALIDATE_CREDENTIAL_CONFIG

    It can be configured with the following settings:
    - register_validation_capability: bool - Flag that indicates whether the CredentialsModule should register the validate_credential_config capability. Set to `False` to skip registration and implement the capability manually.

    You can also call the base_validation method to perform base validation on a credential config request.

    Example usage when manually registering the capability:
        @integration.register_capability(StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG)
        async def validate_credential_config(
            args: ValidateCredentialConfigRequest,
        ) -> ValidateCredentialConfigResponse:
            # Use base validation
            errors = CredentialsModule.base_validation(integration, args)
            if errors:
                return ValidateCredentialConfigResponse(response=ValidatedCredentialConfig(valid=False, errors=errors))
            # Add custom validation logic here
            # ...
            return ValidateCredentialConfigResponse(response=ValidatedCredentialConfig(valid=True))
    """

    credentials: dict[str, CredentialConfig]
    settings: CredentialsSettings

    def __init__(self, settings: CredentialsSettings):
        super().__init__()
        self.credentials = {}
        self.settings = settings

    def add_capability(self, capability: str):
        """Add a capability to the module."""
        self.capabilities.append(capability)

    def get_capability(self, capability: str) -> StandardCapabilityName | str | None:
        """Get a capability from the module."""
        for cap in self.capabilities:
            if cap == capability:
                return cap
        return None

    def register(self, integration: "Integration"):
        """Register validate_credential_config capability for each credential config."""
        self.integration = integration
        validation_functions: dict[str, ValidateCredentialConfigCallable] = {}

        for credential in integration.credentials:
            self.credentials[credential.id] = credential
            validation_implementation = credential.validation
            if validation_implementation:
                validation_functions[credential.id] = cast(
                    ValidateCredentialConfigCallable, validation_implementation
                )

        if self.settings.register_validation_capability and (
            StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG.value
            not in self.integration.capabilities.keys()
        ):
            """
            If the Integration already registers a validate_credential_config capability,
            we don't register another one, as it would be a duplicate.
            """
            self.register_dynamic_validation_capability(
                StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG,
                validation_functions,
            )

    def register_dynamic_validation_capability(
        self,
        capability_name: StandardCapabilityName,
        validation_functions: dict[str, ValidateCredentialConfigCallable],
    ):
        @self.integration.register_capability(capability_name)
        async def validate_credential_config(
            args: ValidateCredentialConfigRequest,
        ) -> ValidateCredentialConfigResponse:
            is_valid = False
            errors = CredentialsModule.base_validation(
                self.integration.app_id, self.integration.credentials, args
            )

            if errors:
                return ValidateCredentialConfigResponse(
                    response=ValidatedCredentialConfig(
                        valid=is_valid,
                        validation_errors=errors,
                    ),
                )

            for credential_id, validation_function in validation_functions.items():
                if credential_id != args.request.credential.id:
                    # Skip validation for non-received credentials
                    continue

                """
                If this raises, it will bubble up just like any other capability error.
                """
                result = validation_function(args)
                if inspect.isawaitable(result):
                    result = await cast(
                        Awaitable[ValidateCredentialConfigResponse | ErrorResponse],
                        result,
                    )

                if isinstance(result, ErrorResponse):
                    raise CapabilityExecutionError(result)

                if isinstance(result, ValidateCredentialConfigResponse):
                    if not result.response.valid or result.response.validation_errors:
                        errors.extend(result.response.validation_errors or [])

                    if not result.response.valid and not result.response.validation_errors:
                        errors.append("Credential is invalid, unexpected error occurred")

            if not errors:
                is_valid = True

            return ValidateCredentialConfigResponse(
                response=ValidatedCredentialConfig(
                    valid=is_valid,
                    validation_errors=errors,
                ),
            )

        return validate_credential_config

    # Utility methods

    @staticmethod
    def _has_extra_whitespace(value: Any) -> bool:
        """
        Recursively check for extra whitespace in a credential field value.

        The approach of calling .strip() on all values fails for credential
        types like ServiceAccountCredential whose `key` field is a dict rather
        than a string. This handles dicts correctly by recursing into them.

        Ignores checking `private_key` fields.
        """
        if isinstance(value, str):
            return value.strip() != value
        if isinstance(value, dict):
            return any(
                CredentialsModule._has_extra_whitespace(v)
                for k, v in value.items()
                if "private_key" not in k
            )
        return False

    @classmethod
    def base_validation(
        cls,
        app_id: str,
        credentials: Sequence[CredentialConfig | OAuthConfig],
        request: ValidateCredentialConfigRequest,
    ) -> list[str]:
        """
        Perform base validation on a credential config request.

        This method can be called as a class method to reuse the base validation logic
        when manually implementing the validate_credential_config capability.

        Example usage when manually registering the capability:
            @integration.register_capability(StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG)
            async def validate_credential_config(
                args: ValidateCredentialConfigRequest,
            ) -> ValidateCredentialConfigResponse:
                # Use base validation
                errors = CredentialsModule.base_validation("app_id", CredentialConfigList, args)
                if errors:
                    return ValidateCredentialConfigResponse(
                        response=ValidatedCredentialConfig(valid=False, validation_errors=errors)
                    )
                # Add custom validation logic here
                # ...
                return ValidateCredentialConfigResponse(
                    response=ValidatedCredentialConfig(valid=True, validation_errors=[])
                )

        Args:
            app_id: The App ID of the integration
            credentials: The credentials (configs) to validate against
            request: The validation request to validate

        Returns:
            A list of error messages (empty if validation passes)

        Raises:
            CapabilityExecutionError: For critical validation failures (missing ID, invalid config, etc.)
        """
        errors: list[str] = []  # Customer facing errors
        credential_config_id = request.request.credential.id
        credential = request.request.credential
        credential_dict = credential.model_dump()

        if not credential_config_id:
            # This should not happen, and should in such case fail immediately
            raise MissingParameterError(message="Received credential without an ID")

        # Build credentials dict from integration.credentials
        credentials_dict = {cred.id: cred for cred in credentials}
        credential_config = credentials_dict.get(credential_config_id)

        if credential_config is None:
            # Should fail fast
            raise InvalidConfigurationError(
                message=f"Missing credential configuration for ID {credential_config_id}"
            )

        try:
            # Use the input model if provided, otherwise use the default model for the credential type
            credential_model_type = (
                credential_config.input_model or AUTH_TYPE_MAP[credential_config.type]
            )
            if not isinstance(credential_model_type, type) or not issubclass(
                credential_model_type, BaseModel
            ):
                raise InvalidConfigurationError(
                    message=f"Invalid input model configured for credential ID {credential_config_id}"
                )

            credential_payload = credential_dict.get(credential_config.type) or {}
            credential_model = credential_model_type(**credential_payload)

        except (ValidationError, TypeError) as e:
            raise InvalidValueError(message="Invalid or malformed credential received") from e

        # Dump the model
        credential_dict = credential_model.model_dump(exclude_none=True)

        # Check for empty models
        if credential_dict == {}:
            errors.append("Credential is missing required fields")
            return errors

        # Get the list of required fields from the model's JSON schema
        model_schema = credential_model.model_json_schema()
        required_fields = set(model_schema.get("required", []))

        # Check for empty strings on required fields
        for field_name, value in credential_dict.items():
            if field_name in required_fields and value == "":
                errors.append(
                    "A required field is empty, please provide a value before submitting again"
                )
                return errors

        # Check for extra whitespace
        if CredentialsModule._has_extra_whitespace(credential_dict):
            errors.append(
                "Credential has extra whitespace, please remove it before submitting it again"
            )
            return errors

        return errors
