from logging import Logger
from typing import Any, Union, Optional, Iterable, Callable

from saml2.mdstore import MetadataStore

from saml2 import SAMLError as SAMLError

logger: Logger
COMMON_ARGS: list[str]
SP_ARGS: list[str]
AA_IDP_ARGS: list[str]
PDP_ARGS: list[str]
AQ_ARGS: list[str]
AA_ARGS: list[str]
COMPLEX_ARGS: list[str]
ALL: set[str]
SPEC: dict[str, list[str]]
PREFERRED_BINDING: dict[str, list[str]]

class ConfigurationError(SAMLError): ...

class Config:
    def_context: str
    logging: Optional[dict[str, Any]]
    entityid: Optional[str]
    xmlsec_binary: Optional[str]
    xmlsec_path: Optional[list[Any]]
    debug: bool
    key_file: Optional[str]
    cert_file: Optional[str]
    encryption_keypairs: Optional[list[dict[str, str]]]
    additional_cert_files: Optional[list[str]]
    metadata_key_usage: str
    secret: Optional[str]
    accepted_time_diff: Optional[Any]
    name: Optional[str]
    ca_certs: Optional[Any]
    verify_ssl_cert: bool
    description: Optional[str]
    valid_for: Optional[int]
    organization: Optional[dict[str, list[tuple[str, str]]]]
    contact_person: Optional[list[dict[str, str]]]
    name_form: Optional[str]
    name_id_format: Optional[list[str]]
    name_id_policy_format: Optional[str]
    name_id_format_allow_create: Optional[bool]
    virtual_organization: Optional[dict[str, dict[str, str]]]
    only_use_keys_in_metadata: bool
    logout_requests_signed: Optional[bool]
    logout_responses_signed: Optional[bool]
    disable_ssl_certificate_validation: Optional[bool]
    context: str
    attribute_converters: Optional[Any]
    metadata: Optional[dict[str, list[dict[str, Any]]]]
    policy: Optional[dict[str, dict[str, dict[str, Any]]]]
    serves: list[Any]
    vorg: dict[str, Any]
    preferred_binding: dict[str, list[str]]
    domain: str
    name_qualifier: str
    assurance_certification: list[str]
    entity_attributes: dict[str, Any]
    entity_category: list[str]
    entity_category_support: list[str]
    crypto_backend: str
    scope: str
    allow_unknown_attributes: bool
    extension_schema: dict[str, Any]
    cert_handler_extra_class: Optional[Any]
    verify_encrypt_cert_advice: Union[bool, Callable[[], bool], None]
    verify_encrypt_cert_assertion: Union[bool, Callable[[], bool], None]
    generate_cert_func: Optional[Any]
    generate_cert_info: Optional[bool]
    tmp_cert_file: Optional[str]
    tmp_key_file: Optional[str]
    validate_certificate: Optional[bool]
    extensions: dict[str, Any]
    attribute: list[Any]
    attribute_profile: list[Any]
    requested_attribute_name_format: Optional[Any]
    delete_tmpfiles: bool
    signing_algorithm: Optional[str]
    digest_algorithm: Optional[str]

    def __init__(self, homedir: str = ...) -> None: ...
    def setattr(self, context: str, attr: str, val: Any) -> None: ...
    def getattr(self, attr: str, context: Optional[str] = ...) -> Any: ...
    def load_special(self, cnf: Any, typ: Any) -> None: ...
    def load_complex(self, cnf: Any) -> None: ...
    def load(self, cnf, metadata_construction: None = ...) -> Config: ...
    def load_file(self, config_filename: str, metadata_construction: None = ...) -> Config: ...
    def load_metadata(self, metadata_conf: Union[Iterable[Any], dict[str, Any]]) -> MetadataStore: ...
    def endpoint(self, service: str, binding: Optional[str] = ..., context: Optional[str] = ...) -> list[str]: ...
    def endpoint2service(self, endpoint: str, context: Optional[str] = ...) -> tuple[Optional[str], Optional[str]]: ...
    def do_extensions(self, extensions: dict[str, Any]) -> None: ...
    def service_per_endpoint(self, context: Optional[str] = ...) -> dict[str, tuple[str, str]]: ...

class SPConfig(Config):
    def_context: str

    def __init__(self) -> None: ...
    def vo_conf(self, vo_name: str) -> Optional[Any]: ...
    def ecp_endpoint(self, ipaddress: str) -> Optional[str]: ...

class IdPConfig(Config):
    def_context: str

    def __init__(self) -> None: ...

def config_factory(_type: str, config: Union[str, dict[str, Any]]) -> Config: ...
