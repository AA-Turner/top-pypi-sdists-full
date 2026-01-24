from __future__ import annotations

import typing as t
from collections.abc import Awaitable, Callable
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, StrictBool, StrictStr

# Import directly from modules to avoid circular import through generated/__init__.py
from connector_sdk_types.generated.models.basic_credential import BasicCredential
from connector_sdk_types.generated.models.jwt_credential import JWTCredential
from connector_sdk_types.generated.models.key_pair_credential import KeyPairCredential
from connector_sdk_types.generated.models.o_auth1_credential import OAuth1Credential
from connector_sdk_types.generated.models.o_auth_client_credential import OAuthClientCredential
from connector_sdk_types.generated.models.o_auth_credential import OAuthCredential
from connector_sdk_types.generated.models.service_account_credential import ServiceAccountCredential
from connector_sdk_types.generated.models.token_credential import TokenCredential

if TYPE_CHECKING:
    from connector_sdk_types.generated import (
        ErrorResponse,
        ValidateCredentialConfigRequest,
        ValidateCredentialConfigResponse,
    )

from connector_sdk_types.oai.modules.oauth_module_types import OAuthSettings

ValidateCredentialConfigCallable: t.TypeAlias = Callable[
    ["ValidateCredentialConfigRequest"],
    "ValidateCredentialConfigResponse | ErrorResponse | Awaitable[ValidateCredentialConfigResponse] | Awaitable[ErrorResponse]",
]

# Tuple of credential IDs, at least one credential ID is required
CredentialIdCombination: t.TypeAlias = tuple[str, ...] | tuple[str] | str


class CredentialsSettings(BaseModel):
    """
    Settings for the CredentialsModule.
    """

    register_validation_capability: bool = Field(
        default=True,
        description="Flag that indicates whether the CredentialsModule should register the validate_credential_config capability. Set to `False` to skip registration and implement the capability manually.",
    )

    """
    Example:
    ```python
    allowed_credentials = [("credential_id_1", "credential_id_2")]
    ```
    This means that the credentials with the IDs `credential_id_1` and `credential_id_2` are expected to be used together.

    If you don't supply any allowed credentials, and all of your credentials are optional, the connector will offer the following authentication options:
    1. credential_id_1
    2. credential_id_2

    If you don't supply any allowed credentials, and both are required, the connector will offer the following authentication options:
    1. credential_id_1, credential_id_2

    In essence, optional = True means the credential can be used on its own. On the other hand, optional = False means the credential must always be supplied.
    """
    allowed_credentials: list[CredentialIdCombination] = Field(
        default=[],
        description="List of credential IDs that are expected to be used together. If empty, `optional` argument of CredentialConfig denotes requirements and all non-required credentials are considered singular. If a tuple is provided, the credentials in the tuple will be used together.",
    )

    @classmethod
    def default(cls) -> CredentialsSettings:
        return cls(register_validation_capability=True, allowed_credentials=[])


class CredentialConfig(BaseModel):
    """
    Configuration of a single credential, used in the end Integration.

    id: string - The ID of the authentication schema. Must be unique within one app - no two credentials should share the same ID.
    type: AuthModel - The authentication type, simplified identificator, like `oauth`, `basic`, `token`, `jwt`, `service_account`, `key_pair`.
    description: string - The markdown description of the authentication. Used primarily for instructions provided to customers.
    optional: boolean | None - Denotes whether this credential is optional, for example, if the integration can function just fine with one credential, and another credential is not strictly required, eg. the app will operate under a limited scope.
    input_model: BaseModel | None - The input model expected by the app to authenticate against the 3rd party service. This is provided so that the default model can be overriden by the app.
    oauth_settings: OAuthSettings | None - Oauth settings OAuth settings define the behavior of the OAuth Module, each credential can then have its own specific settings. This is a way to configure multiple OAuth credentials. Use the built-in OAuthConfig model (connector.oai.modules.oauth_module_types) to define the config object.
    validation: ValidateCredentialConfigCallable | None - Validation function. Pass a function that will be registered as a capability/validator on the connector. This function will be called to validate this particular credential. Expects a `ValidateCredentialConfigCallable` using standard request and response types.
    """

    id: StrictStr = Field(
        description="The ID of the authentication schema. Must be unique within one app - no two credentials should share the same ID."
    )
    type: AuthModel = Field(description="The authentication type, simplified identificator.")
    description: StrictStr = Field(
        description="The markdown description of the authentication. Used primarily for instructions provided to customers."
    )
    optional: StrictBool | None = Field(
        default=False,
        description=(
            """Denotes whether this credential is optional, for example, if the integration can function just fine with one credential, and another credential is not strictly required, eg. the app will operate under a limited scope.
        If you don't supply any allowed credentials (as part of credentials settings), and all of your credentials are optional, the connector will offer the following authentication options:
        1. credential_id_1
        2. credential_id_2

        If you don't supply any allowed credentials, and both are required, the connector will offer the following authentication options:
        1. credential_id_1, credential_id_2
        """
        ),
    )
    input_model: t.Any | None = Field(
        default=None,
        description="The input model expected by the app to authenticate against the 3rd party service. This is provided so that the default model can be overriden by the app.",
    )
    oauth_settings: t.Any | None = Field(
        default=None,
        description="Oauth settings OAuth settings define the behavior of the OAuth Module, each credential can then have its own specific settings This is a way to configure multiple OAuth credentials.  Use the built-in OAuthConfig model (connector.oai.modules.oauth_module_types) to define the config object.",
    )
    validation: ValidateCredentialConfigCallable | None = Field(
        default=None,
        description="Validation function. Pass a function that will be registered as a capability/validator on the connector. This function will be called to validate this particular credential. Expects a `ValidateCredentialConfigCallable` using standard request and response types.",
    )


class OAuthConfig(CredentialConfig):
    """
    OAuth config, this is a CredentialConfig, used when needing to configure OAuth for an apps credentials list.
    """

    oauth_settings: t.Annotated[
        OAuthSettings | None,
        Field(
            default=None,
            description="The OAuth settings to use, defaults to all capabilities enabled.",
        ),
    ] = None


AuthSetting: t.TypeAlias = (
    type[OAuthCredential]
    | type[OAuthClientCredential]
    | type[OAuth1Credential]
    | type[BasicCredential]
    | type[TokenCredential]
    | type[JWTCredential]
    | type[ServiceAccountCredential]
    | type[KeyPairCredential]
)


class EmptySettings(BaseModel):
    pass


class AuthModel(str, Enum):
    """
    Enum representing different authentication models.
    This was moved from TSP, as by default unused enums are not generated into python.
    """

    OAUTH = "oauth"
    OAUTH_CLIENT_CREDENTIALS = "oauth_client_credentials"
    OAUTH1 = "oauth1"
    BASIC = "basic"
    TOKEN = "token"
    JWT = "jwt"
    SERVICE_ACCOUNT = "service_account"
    KEY_PAIR = "key_pair"
