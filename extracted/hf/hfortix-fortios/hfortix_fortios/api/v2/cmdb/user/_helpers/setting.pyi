from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_AUTH_TYPE: Literal["http", "https", "ftp", "telnet"]
VALID_BODY_AUTH_SECURE_HTTP: Literal["enable", "disable"]
VALID_BODY_AUTH_HTTP_BASIC: Literal["enable", "disable"]
VALID_BODY_AUTH_SSL_ALLOW_RENEGOTIATION: Literal["enable", "disable"]
VALID_BODY_AUTH_SRC_MAC: Literal["enable", "disable"]
VALID_BODY_AUTH_ON_DEMAND: Literal["always", "implicitly"]
VALID_BODY_AUTH_TIMEOUT_TYPE: Literal["idle-timeout", "hard-timeout", "new-session"]
VALID_BODY_RADIUS_SES_TIMEOUT_ACT: Literal["hard-timeout", "ignore-timeout"]
VALID_BODY_PER_POLICY_DISCLAIMER: Literal["enable", "disable"]
VALID_BODY_AUTH_SSL_MIN_PROTO_VERSION: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
VALID_BODY_AUTH_SSL_MAX_PROTO_VERSION: Literal["sslv3", "tlsv1", "tlsv1-1", "tlsv1-2", "tlsv1-3"]
VALID_BODY_AUTH_SSL_SIGALGS: Literal["no-rsa-pss", "all"]
VALID_BODY_CORS: Literal["disable", "enable"]

# Metadata dictionaries
FIELD_TYPES: dict[str, str]
FIELD_DESCRIPTIONS: dict[str, str]
FIELD_CONSTRAINTS: dict[str, dict[str, Any]]
NESTED_SCHEMAS: dict[str, dict[str, Any]]
FIELDS_WITH_DEFAULTS: dict[str, Any]
DEPRECATED_FIELDS: dict[str, dict[str, str]]
REQUIRED_FIELDS: list[str]

# Helper functions
def get_field_type(field_name: str) -> str | None: ...
def get_field_description(field_name: str) -> str | None: ...
def get_field_default(field_name: str) -> Any: ...
def get_field_constraints(field_name: str) -> dict[str, Any]: ...
def get_nested_schema(field_name: str) -> dict[str, Any] | None: ...
def get_field_metadata(field_name: str) -> dict[str, Any]: ...
def validate_field_value(field_name: str, value: Any) -> bool: ...
def get_all_fields() -> list[str]: ...
def get_required_fields() -> list[str]: ...
def get_schema_info() -> dict[str, Any]: ...


__all__ = [
    "VALID_BODY_AUTH_TYPE",
    "VALID_BODY_AUTH_SECURE_HTTP",
    "VALID_BODY_AUTH_HTTP_BASIC",
    "VALID_BODY_AUTH_SSL_ALLOW_RENEGOTIATION",
    "VALID_BODY_AUTH_SRC_MAC",
    "VALID_BODY_AUTH_ON_DEMAND",
    "VALID_BODY_AUTH_TIMEOUT_TYPE",
    "VALID_BODY_RADIUS_SES_TIMEOUT_ACT",
    "VALID_BODY_PER_POLICY_DISCLAIMER",
    "VALID_BODY_AUTH_SSL_MIN_PROTO_VERSION",
    "VALID_BODY_AUTH_SSL_MAX_PROTO_VERSION",
    "VALID_BODY_AUTH_SSL_SIGALGS",
    "VALID_BODY_CORS",
    "FIELD_TYPES",
    "FIELD_DESCRIPTIONS",
    "FIELD_CONSTRAINTS",
    "NESTED_SCHEMAS",
    "FIELDS_WITH_DEFAULTS",
    "DEPRECATED_FIELDS",
    "REQUIRED_FIELDS",
    "get_field_type",
    "get_field_description",
    "get_field_default",
    "get_field_constraints",
    "get_nested_schema",
    "get_field_metadata",
    "validate_field_value",
    "get_all_fields",
    "get_required_fields",
    "get_schema_info",
]