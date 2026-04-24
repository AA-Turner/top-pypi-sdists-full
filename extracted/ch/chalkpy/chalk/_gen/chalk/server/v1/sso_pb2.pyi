from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class CreateScimTokenRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateScimTokenResponse(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class SignOnProviderSamlConfig(_message.Message):
    __slots__ = ("issuer", "idp_login_url", "idp_logout_url", "certificate", "is_primary_sso_config")
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    IDP_LOGIN_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_LOGOUT_URL_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_SSO_CONFIG_FIELD_NUMBER: _ClassVar[int]
    issuer: str
    idp_login_url: str
    idp_logout_url: str
    certificate: str
    is_primary_sso_config: bool
    def __init__(
        self,
        issuer: _Optional[str] = ...,
        idp_login_url: _Optional[str] = ...,
        idp_logout_url: _Optional[str] = ...,
        certificate: _Optional[str] = ...,
        is_primary_sso_config: bool = ...,
    ) -> None: ...

class SignOnProviderOidcConfig(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...) -> None: ...

class SignOnProviderConfiguration(_message.Message):
    __slots__ = ("name", "id", "idp_type", "saml_config", "oidc_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IDP_TYPE_FIELD_NUMBER: _ClassVar[int]
    SAML_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OIDC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    idp_type: str
    saml_config: SignOnProviderSamlConfig
    oidc_config: SignOnProviderOidcConfig
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        idp_type: _Optional[str] = ...,
        saml_config: _Optional[_Union[SignOnProviderSamlConfig, _Mapping]] = ...,
        oidc_config: _Optional[_Union[SignOnProviderOidcConfig, _Mapping]] = ...,
    ) -> None: ...

class ListSignOnProviderConfigurationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSignOnProviderConfigurationsResponse(_message.Message):
    __slots__ = ("configurations",)
    CONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    configurations: _containers.RepeatedCompositeFieldContainer[SignOnProviderConfiguration]
    def __init__(
        self, configurations: _Optional[_Iterable[_Union[SignOnProviderConfiguration, _Mapping]]] = ...
    ) -> None: ...

class CreateSignOnProviderConfigurationRequest(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: SignOnProviderConfiguration
    def __init__(self, configuration: _Optional[_Union[SignOnProviderConfiguration, _Mapping]] = ...) -> None: ...

class CreateSignOnProviderConfigurationResponse(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: SignOnProviderConfiguration
    def __init__(self, configuration: _Optional[_Union[SignOnProviderConfiguration, _Mapping]] = ...) -> None: ...

class UpdateSignOnProviderConfigurationRequest(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: SignOnProviderConfiguration
    def __init__(self, configuration: _Optional[_Union[SignOnProviderConfiguration, _Mapping]] = ...) -> None: ...

class UpdateSignOnProviderConfigurationResponse(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: SignOnProviderConfiguration
    def __init__(self, configuration: _Optional[_Union[SignOnProviderConfiguration, _Mapping]] = ...) -> None: ...

class DeleteSignOnProviderConfigurationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSignOnProviderConfigurationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSamlConfigurationByIssuerRequest(_message.Message):
    __slots__ = ("issuer",)
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    issuer: str
    def __init__(self, issuer: _Optional[str] = ...) -> None: ...

class GetSamlConfigurationByIssuerResponse(_message.Message):
    __slots__ = ("configuration", "team_id")
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    configuration: SignOnProviderSamlConfig
    team_id: str
    def __init__(
        self, configuration: _Optional[_Union[SignOnProviderSamlConfig, _Mapping]] = ..., team_id: _Optional[str] = ...
    ) -> None: ...
