from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class SsoEmailDomain(_message.Message):
    __slots__ = ("id", "team_id", "email_domain", "chalk_approved", "provider_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    CHALK_APPROVED_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    email_domain: str
    chalk_approved: bool
    provider_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        email_domain: _Optional[str] = ...,
        chalk_approved: bool = ...,
        provider_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListSsoEmailDomainsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSsoEmailDomainsResponse(_message.Message):
    __slots__ = ("email_domains",)
    EMAIL_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    email_domains: _containers.RepeatedCompositeFieldContainer[SsoEmailDomain]
    def __init__(self, email_domains: _Optional[_Iterable[_Union[SsoEmailDomain, _Mapping]]] = ...) -> None: ...

class CreateSsoEmailDomainRequest(_message.Message):
    __slots__ = ("email_domain",)
    EMAIL_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    email_domain: SsoEmailDomain
    def __init__(self, email_domain: _Optional[_Union[SsoEmailDomain, _Mapping]] = ...) -> None: ...

class CreateSsoEmailDomainResponse(_message.Message):
    __slots__ = ("email_domain",)
    EMAIL_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    email_domain: SsoEmailDomain
    def __init__(self, email_domain: _Optional[_Union[SsoEmailDomain, _Mapping]] = ...) -> None: ...

class UpdateSsoEmailDomainRequest(_message.Message):
    __slots__ = ("email_domain",)
    EMAIL_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    email_domain: SsoEmailDomain
    def __init__(self, email_domain: _Optional[_Union[SsoEmailDomain, _Mapping]] = ...) -> None: ...

class UpdateSsoEmailDomainResponse(_message.Message):
    __slots__ = ("email_domain",)
    EMAIL_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    email_domain: SsoEmailDomain
    def __init__(self, email_domain: _Optional[_Union[SsoEmailDomain, _Mapping]] = ...) -> None: ...

class DeleteSsoEmailDomainRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSsoEmailDomainResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

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
    __slots__ = ("name", "id", "idp_type", "team_id", "saml_config", "oidc_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IDP_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SAML_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OIDC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: str
    idp_type: str
    team_id: str
    saml_config: SignOnProviderSamlConfig
    oidc_config: SignOnProviderOidcConfig
    def __init__(
        self,
        name: _Optional[str] = ...,
        id: _Optional[str] = ...,
        idp_type: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
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

class GetSignOnProvidersForEmailRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class GetSignOnProvidersForEmailResponse(_message.Message):
    __slots__ = ("providers",)
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[SignOnProviderConfiguration]
    def __init__(
        self, providers: _Optional[_Iterable[_Union[SignOnProviderConfiguration, _Mapping]]] = ...
    ) -> None: ...

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
