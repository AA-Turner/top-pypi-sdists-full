from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SSL_MODE: Literal["half", "full"]
VALID_BODY_ADD_HEADER_X_FORWARDED_PROTO: Literal["enable", "disable"]
VALID_BODY_SSL_DH_BITS: Literal["768", "1024", "1536", "2048"]
VALID_BODY_SSL_ALGORITHM: Literal["high", "medium", "low"]
VALID_BODY_SSL_CLIENT_RENEGOTIATION: Literal["allow", "deny", "secure"]
VALID_BODY_SSL_MIN_VERSION: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
VALID_BODY_SSL_MAX_VERSION: Literal["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]
VALID_BODY_SSL_SEND_EMPTY_FRAGS: Literal["enable", "disable"]
VALID_BODY_URL_REWRITE: Literal["enable", "disable"]

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
    "VALID_BODY_SSL_MODE",
    "VALID_BODY_ADD_HEADER_X_FORWARDED_PROTO",
    "VALID_BODY_SSL_DH_BITS",
    "VALID_BODY_SSL_ALGORITHM",
    "VALID_BODY_SSL_CLIENT_RENEGOTIATION",
    "VALID_BODY_SSL_MIN_VERSION",
    "VALID_BODY_SSL_MAX_VERSION",
    "VALID_BODY_SSL_SEND_EMPTY_FRAGS",
    "VALID_BODY_URL_REWRITE",
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