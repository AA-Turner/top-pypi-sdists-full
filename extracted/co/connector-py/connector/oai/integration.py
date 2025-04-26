"""Utility class to manage connector implementation.

:py:class:`Integration` provides a single point to register Integration
capabilities.

By instantiating the :py:class:`Integration` you simply create a basic
integration without any real implementation. To actually implement any
capability, you have to define (async) function outside the class and
register them to the integration instance by decorating the
implementation with ``@integration.register_capability(name)``.

Capability function has to:
    * accept only one argument
    * return scalar response

The :py:class:`Integration` is as much type-hinted as possible and also
does several checks to ensure that the implementation "is correct".
Incorrect implementation should raise an error during application start
(fail fast).

What is checked (at application start):
    * capability name is known (defined in ``StandardCapabilityName`` enum)
    * the types of accepted argument and returned value matches the
    capability interface
"""

import inspect
import json
import logging
import re
import typing as t
from dataclasses import asdict, dataclass

from pydantic import BaseModel, ValidationError

from connector.generated import (
    AppCategory,
    AuthCredential,
    AuthModel,
    BasicCredential,
    CapabilitySchema,
    CredentialConfig,
    EntitlementType,
    Error,
    ErrorCode,
    ErrorResponse,
    Info,
    InfoResponse,
    JWTCredential,
    OAuth1Credential,
    OAuthClientCredential,
    OAuthCredential,
    ResourceType,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenCredential,
)
from connector.oai.capability import (
    CapabilityCallableProto,
    capability_requires_authentication,
    generate_capability_schema,
    get_capability_annotations,
    validate_capability,
)
from connector.oai.errors import ErrorMap, handle_exception
from connector.oai.modules.base_module import BaseIntegrationModule
from connector.oai.modules.info_module import InfoModule
from connector.oai.modules.oauth_module import OAuthModule
from connector.oai.modules.oauth_module_types import OAuthConfig, OAuthSettings

AuthSetting: t.TypeAlias = (
    type[OAuthCredential]
    | type[OAuthClientCredential]
    | type[OAuth1Credential]
    | type[BasicCredential]
    | type[TokenCredential]
    | type[JWTCredential]
    | type[ServiceAccountCredential]
)


AUTH_TYPE_MAP = {
    AuthModel.OAUTH: OAuthCredential,
    AuthModel.OAUTH_CLIENT_CREDENTIALS: OAuthClientCredential,
    AuthModel.BASIC: BasicCredential,
    AuthModel.TOKEN: TokenCredential,
    AuthModel.JWT: JWTCredential,
    AuthModel.SERVICE_ACCOUNT: ServiceAccountCredential,
}


logger = logging.getLogger("integration-connectors.sdk")


class IntegrationError(Exception):
    """Base class for exceptions raised by Integration."""


class DuplicateCapabilityError(IntegrationError):
    """Raised when registering the same capability repeatedly."""

    def __init__(self, capability_name: str) -> None:
        super().__init__(f"{capability_name} already registered")


class ReservedCapabilityNameError(IntegrationError):
    """
    Raised when registering a custom capability, using a name reserved for standard capabilities
    """

    def __init__(self, capability_name: str) -> None:
        super().__init__(
            f"Cannot register {capability_name} as a custom capability. This name is reserved for "
            f"the standard {capability_name} capability."
        )


class InvalidCapabilityNameError(IntegrationError):
    """
    Raised when registering a custom capability, using a name that violates our naming conventions
    """

    def __init__(self, capability_name: str, reason: str | None) -> None:
        msg = f"Cannot register {capability_name} as a custom capability."
        if reason is None:
            msg += (
                " Name violates our naming conventions. Please make sure it is snake cased,"
                " does not contain numbers or special characters."
            )
        else:
            msg += f" {reason}"
        super().__init__(msg)


class InvalidAppIdError(IntegrationError):
    """Raised when app_id is not valid.

    Most probably, empty or containing only whitespaces.
    """


@dataclass
class DescriptionData:
    user_friendly_name: str
    categories: list[AppCategory]
    description: str | None = None
    logo_url: str | None = None


@dataclass
class CapabilityMetadata:
    display_name: str | None = None
    description: str | None = None


class EmptySettings(BaseModel):
    pass


def _is_snake_case(text: str) -> bool:
    snake_case_pattern = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    return bool(snake_case_pattern.match(text))


def _validate_capability_name(capability_name: str) -> None:
    is_snake_case = _is_snake_case(capability_name)
    if not is_snake_case:
        raise InvalidCapabilityNameError(
            capability_name, reason="Capability names must use snake casing."
        )

    if not capability_name.replace("_", "").isalpha():
        raise InvalidCapabilityNameError(
            capability_name,
            reason="Capability names must only contain alphabetic characters and underscores",
        )


class Integration:
    # TODO: Remove this comment, just need to trigger an sdk change
    app_id: str
    settings_model: type[BaseModel]

    def __init__(
        self,
        *,
        app_id: str,
        version: str,
        exception_handlers: ErrorMap,
        description_data: DescriptionData,
        auth: AuthSetting | None = None,
        credentials: t.Sequence[CredentialConfig | OAuthConfig] | None = None,
        handle_errors: bool = True,
        resource_types: list[ResourceType] | None = None,
        entitlement_types: list[EntitlementType] | None = None,
        settings_model: type[BaseModel] | None = None,
        oauth_settings: OAuthSettings | None = None,
    ):
        self.app_id = app_id.strip()
        self.version = version
        self.auth = auth
        self.credentials = credentials or []
        self.exception_handlers = exception_handlers
        self.handle_errors = handle_errors
        self.description_data = description_data
        self.resource_types = resource_types or []
        self.entitlement_types = entitlement_types or []
        self.settings_model = settings_model or EmptySettings
        self.oauth_settings = oauth_settings

        if len(self.app_id) == 0:
            raise InvalidAppIdError

        self.capabilities: dict[str, CapabilityCallableProto[t.Any]] = {}
        self.capability_metadata: dict[str, CapabilityMetadata] = {}
        self.modules: list[BaseIntegrationModule] = []

        # Add OAuthModule if credentials contain OAuthConfig
        if self.credentials and any(isinstance(cred, OAuthConfig) for cred in self.credentials):
            oauth_credentials = [
                cred
                for cred in self.credentials
                if isinstance(cred, OAuthConfig) and cred.oauth_settings is not None
            ]
            self.add_module(OAuthModule(oauth_credentials))
        else:
            # Add OAuthModule if oauth_settings is provided (backwards compatibility, until phasing 'auth' out)
            if self.oauth_settings is not None:
                self.add_module(OAuthModule([self.oauth_settings]))

        # Attach the info module (app_info capability)
        self.add_module(InfoModule())

    def add_module(self, module: BaseIntegrationModule):
        self.modules.append(module)
        module.register(self)

    def register_capability(
        self,
        name: StandardCapabilityName,
        display_name: str | None = None,
        description: str | None = None,
    ) -> t.Callable[
        [CapabilityCallableProto[t.Any]],
        CapabilityCallableProto[t.Any],
    ]:
        """Add implementation of specified capability.

        This function is expected to be used as a decorator for a
        capability implementation.

        Display name is an optional text to display for the integration capability,
        in place of the default behavior with is to use the capability name.

        Description is an optional 1-2 sentence description of any unusual behaviors
        of the capability, rendered for the end user.

        Raises
        ------
        RuntimeError:
            When capability is registered more that once.
        """
        if name.value in self.capabilities:
            raise DuplicateCapabilityError(name.value)

        def decorator(
            func: CapabilityCallableProto[t.Any],
        ) -> CapabilityCallableProto[t.Any]:
            validate_capability(name, func)
            self.capabilities[name.value] = func
            self.capability_metadata[name.value] = CapabilityMetadata(
                display_name=display_name, description=description
            )
            return func

        return decorator

    def register_custom_capability(
        self,
        name: str,
        display_name: str | None = None,
        description: str | None = None,
    ) -> t.Callable[
        [CapabilityCallableProto[t.Any]],
        CapabilityCallableProto[t.Any],
    ]:
        """Add implementation of specified custom capability.

        This function is expected to be used as a decorator for a
        custom capability implementation.

        Custom capabilities differ from standard capabilities, because:
        - They can have any capability name (as long as it meets naming standards)
        - There is more flexibility around input and output types

        Display name is an optional text to display for the integration capability,
        in place of the default behavior with is to use the capability name.

        Description is an optional 1-2 sentence description of any unusual behaviors
        of the capability, rendered for the end user.

        Raises
        ------
        RuntimeError:
            When capability is registered more that once.
        """
        if name in {
            standard_capability_name.value for standard_capability_name in StandardCapabilityName
        }:
            raise ReservedCapabilityNameError(name)

        _validate_capability_name(name)

        if name in self.capabilities:
            raise DuplicateCapabilityError(name)

        def decorator(
            func: CapabilityCallableProto[t.Any],
        ) -> CapabilityCallableProto[t.Any]:
            self.capabilities[name] = func
            self.capability_metadata[name] = CapabilityMetadata(
                display_name=display_name,
                description=description,
            )
            return func

        return decorator

    def register_capabilities(
        self,
        capabilities: dict[
            StandardCapabilityName,
            CapabilityCallableProto[t.Any]
            | tuple[CapabilityCallableProto[t.Any], CapabilityMetadata],
        ],
    ):
        """
        Register a dictionary of capabilities.

        This is a convenience method to register multiple capabilities at once.
        You can pass a tuple of (capability, metadata) to register a capability, along with any
        configuration specific to that capability, such as display_name, description, etc

        eg.
        ```
        integration.register_capabilities({
            StandardCapabilityName.VALIDATE_CREDENTIALS: (
                validate_credentials, CapabilityMetadata(description="Test")
            ),
            StandardCapabilityName.LIST_ACCOUNTS: list_accounts,
        })
        ```
        """
        for name, capability in capabilities.items():
            if isinstance(capability, tuple):
                func, metadata = capability
                self.register_capability(name, **asdict(metadata))(func)
            else:
                self.register_capability(name)(capability)

    async def dispatch(self, name: str, request_string: str) -> str:
        """Call implemented capability, returning the result.

        Raises
        ------
        NotImplementedError:
            When capability is not implemented (or registered)
        """
        try:
            capability = self.capabilities[name]
        except KeyError:
            if self.handle_errors:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message=f"Capability '{name}' is not implemented.",
                        error_code=ErrorCode.NOT_IMPLEMENTED,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()
            raise NotImplementedError from None

        # JSON Input
        json_object = json.loads(request_string)
        if not json_object:
            return ErrorResponse(
                is_error=True,
                error=Error(
                    message="Invalid request, expected JSON input.",
                    error_code=ErrorCode.BAD_REQUEST,
                    app_id=self.app_id,
                ),
            ).model_dump_json()

        # Is this a call to the app_info capability?
        is_app_info_call = name == StandardCapabilityName.APP_INFO.value

        # Credentials parameter validation
        validated_credentials = False
        if "credentials" in json_object and json_object["credentials"] is not None:
            """
            TypeSpec does not support this level of union oneOf types,
            hence we do the validation here.
            At some point in the future, we should just remove 'auth', but for now we are
            backwards compatible and it is being kept.
            """
            if len(json_object["credentials"]) == 0 and self._is_using_credentials():
                if not is_app_info_call:
                    return ErrorResponse(
                        is_error=True,
                        error=Error(
                            message="Missing credentials in request",
                            error_code=ErrorCode.BAD_REQUEST,
                            app_id=self.app_id,
                        ),
                    ).model_dump_json()

            if "auth" in json_object and json_object["auth"] is not None:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Cannot pass credentials and auth in the same request, if you've meant to make this connector multi-auth compatible, please remove the auth field.",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()

            # Validate the credentials
            input_credentials: list[AuthCredential] = []
            try:
                for index, credential in enumerate(json_object["credentials"]):
                    auth_credential = AuthCredential.model_validate(credential)
                    if not auth_credential.id:
                        return ErrorResponse(
                            is_error=True,
                            error=Error(
                                message=f"Missing ID in credential at index {index}",
                                error_code=ErrorCode.BAD_REQUEST,
                                app_id=self.app_id,
                            ),
                        ).model_dump_json()
                    else:
                        # Validate that we are receiving expected credentials
                        if auth_credential.id not in [c.id for c in self.credentials]:
                            return ErrorResponse(
                                is_error=True,
                                error=Error(
                                    message=f"Credential with id '{auth_credential.id}' not expected",
                                    error_code=ErrorCode.BAD_REQUEST,
                                    app_id=self.app_id,
                                ),
                            ).model_dump_json()

                    input_credentials.append(auth_credential)
            except ValidationError:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Malformed credentials in request",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()

            for credential in input_credentials:
                # Grab its connector counterpart
                connector_credential = next(
                    (cred for cred in self.credentials if cred.id == credential.id), None
                )

                # If the credential is not expected, return an error
                if connector_credential is None:
                    return ErrorResponse(
                        is_error=True,
                        error=Error(
                            message=f"Credential with id '{credential.id}' not expected",
                            error_code=ErrorCode.BAD_REQUEST,
                            app_id=self.app_id,
                        ),
                    ).model_dump_json()

                # If the credential is optional, skip model validation
                if connector_credential.optional:
                    logger.info(
                        f"[{self.app_id}][INFO] Credential with id '{credential.id}' is optional, skipping model validation."
                    )
                    continue

                # Validate the credential type
                missing = "Nothing"
                if connector_credential.type == AuthModel.BASIC:
                    if not credential.basic:
                        missing = "basic"
                elif connector_credential.type == AuthModel.OAUTH:
                    if not credential.oauth:
                        missing = "oauth"
                elif connector_credential.type == AuthModel.OAUTH_CLIENT_CREDENTIALS:
                    if not credential.oauth_client_credentials:
                        missing = "oauth_client_credentials"
                elif connector_credential.type == AuthModel.TOKEN:
                    if not credential.token:
                        missing = "token"
                elif connector_credential.type == AuthModel.JWT:
                    if not credential.jwt:
                        missing = "jwt"
                elif connector_credential.type == AuthModel.SERVICE_ACCOUNT:
                    if not credential.service_account:
                        missing = "service_account"
                if missing != "Nothing":
                    return ErrorResponse(
                        is_error=True,
                        error=Error(
                            message=f"Missing '{missing}' credential in request",
                            error_code=ErrorCode.BAD_REQUEST,
                            app_id=self.app_id,
                        ),
                    ).model_dump_json()

            validated_credentials = True

        # TODO: Later on when "auth" is phased out, we can turn this on
        # elif capability_has_authenticated_request(capability):
        #    return ErrorResponse(
        #        is_error=True,
        #        error=Error(
        #            message="Missing credentials in request",
        #            error_code=ErrorCode.BAD_REQUEST,
        #            app_id=self.app_id,
        #        ),
        #    ).model_dump_json()

        # Auth parameter validation
        if "auth" in json_object and json_object["auth"] is not None:
            if "credentials" in json_object and json_object["credentials"] is not None:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Cannot pass credentials and auth in the same request, if you've meant to make this connector multi-auth compatible, please remove the auth field.",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()

            try:
                auth_credential = AuthCredential.model_validate(json_object["auth"])
            except ValidationError:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Malformed auth in request",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()
            missing = "Nothing"
            if self.auth == BasicCredential:
                if not auth_credential.basic:
                    missing = "basic"
            elif self.auth == OAuthCredential:
                if not auth_credential.oauth:
                    missing = "oauth"
            if missing != "Nothing":
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message=f"Missing '{missing}' auth in request",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()
        elif capability_requires_authentication(capability) and not validated_credentials:
            # Since this is not migrated yet, we just flat out skip is_app_info_call
            # In the future we can re-instate the is_required() checks inside this validation
            # and make this work for is_app_info_call automatically (its not required for is_app_info_call)
            if not is_app_info_call:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Missing auth/credentials in request",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()

        # Capability annotation validation
        request_annotation, _ = get_capability_annotations(capability)
        try:
            request = request_annotation.model_validate(json_object)
        except ValidationError as e:
            return ErrorResponse(
                is_error=True,
                error=Error(
                    message=f"Invalid request - {repr(e.errors())}",
                    error_code=ErrorCode.BAD_REQUEST,
                    app_id=self.app_id,
                ),
            ).model_dump_json()

        # Parse and validate the connector settings before dispatching
        if self.settings_model == EmptySettings:
            pass
        elif request.settings is None and self.handle_errors:
            if not is_app_info_call:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message=f"No settings passed on request: {self.app_id} requires {self.settings_model.__name__}",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()
        else:
            try:
                self.settings_model.model_validate(request.settings)
            except ValidationError:
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message="Invalid settings passed on request",
                        error_code=ErrorCode.BAD_REQUEST,
                        app_id=self.app_id,
                    ),
                ).model_dump_json()

        try:
            if inspect.iscoroutinefunction(capability):
                response = await capability(request)
            else:
                response = t.cast(
                    BaseModel,
                    capability(request),
                )

            return response.model_dump_json()
        except Exception as e:
            return handle_exception(
                self.exception_handlers, e, capability, self.app_id
            ).model_dump_json()

    def info(self) -> InfoResponse:
        """Provide information about implemented capabilities.

        Json schema describing implemented capabilities and their
        interface is returned. The authentication schema is also
        included.
        """
        logger.debug("Generating info response")
        capability_names = sorted(self.capabilities.keys())
        capability_schema: dict[str, CapabilitySchema] = {}
        for capability_name in capability_names:
            command_types = generate_capability_schema(self.capabilities[capability_name])

            capability_metadata: CapabilityMetadata | None = None
            if capability_name in self.capability_metadata:
                capability_metadata = self.capability_metadata[capability_name]

            display_name: str | None = capability_name.replace("_", " ").title()
            if (
                capability_metadata is not None
                and capability_metadata.display_name is not None
                and isinstance(capability_metadata.display_name, str)
            ):
                display_name = capability_metadata.display_name

            description = None
            if (
                capability_metadata is not None
                and capability_metadata.description is not None
                and isinstance(capability_metadata.description, str)
            ):
                description = capability_metadata.description

            capability_schema[capability_name] = CapabilitySchema(
                argument=command_types.argument,
                output=command_types.output,
                display_name=display_name,
                description=description,
            )

        oauth_scopes = None
        if self.oauth_settings:
            if not callable(self.oauth_settings.scopes) and isinstance(
                self.oauth_settings.scopes, dict
            ):
                oauth_scopes = {
                    capability: scope
                    for capability, scope in self.oauth_settings.scopes.items()
                    if scope is not None
                }

        return InfoResponse(
            response=Info(
                app_id=self.app_id,
                version=self.version,
                capabilities=capability_names,
                capability_schema=capability_schema,
                logo_url=self.description_data.logo_url,
                user_friendly_name=self.description_data.user_friendly_name,
                description=self.description_data.description,
                categories=self.description_data.categories,
                resource_types=self.resource_types,
                entitlement_types=self.entitlement_types,
                request_settings_schema=self.get_model_extended_json_schema(self.settings_model),
                authentication_schema=self.get_model_extended_json_schema(self.auth)
                if self.auth
                else {},
                credentials_schema=self.get_credentials_json_schema() if self.credentials else [],
                oauth_scopes=oauth_scopes,
            )
        )

    def _is_using_credentials(self) -> bool:
        return len(self.credentials) > 0

    def get_model_extended_json_schema(self, model: type[BaseModel]) -> dict[str, t.Any]:
        json_schema = model.model_json_schema()
        field_order = list(model.model_fields.keys())
        json_schema["field_order"] = field_order
        return json_schema

    def get_credentials_json_schema(self) -> list[dict[str, t.Any]]:
        credentials = []

        if self.credentials:
            for credential in self.credentials:
                credential_schema = {}

                if credential.input_model:
                    # Custom input model (override)
                    credential_schema = self.get_model_extended_json_schema(
                        t.cast(type[BaseModel], credential.input_model)
                    )
                else:
                    # Standard input model
                    credential_schema = self.get_model_extended_json_schema(
                        t.cast(type[BaseModel], AUTH_TYPE_MAP[credential.type])
                    )

                credential_schema["id"] = credential.id
                credential_schema["description"] = credential.description

                """
                Very basic extra oauth_settings info
                TODO:
                - The issue here still is that this does not support multiple oauth credentials (not like we need that right now)
                - This should later be handled exclusively in the new info module and its response
                """
                scopes = None
                if self.oauth_settings:
                    oauth = self.oauth_settings
                    if oauth.scopes is not None:
                        if not callable(oauth.scopes) and isinstance(oauth.scopes, dict):
                            scopes = {
                                capability: scope
                                for capability, scope in oauth.scopes.items()
                                if scope is not None
                            }

                    credential_schema["oauth_settings"] = {
                        "oauth_type": oauth.flow_type,
                        "scopes": scopes,
                        "pkce_enabled": oauth.pkce,
                    }

                credentials.append(credential_schema)

        return credentials
