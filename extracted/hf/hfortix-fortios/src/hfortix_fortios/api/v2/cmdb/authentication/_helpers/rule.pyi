from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_PROTOCOL: Literal["http", "ftp", "socks", "ssh", "ztna-portal"]
VALID_BODY_IP_BASED: Literal["enable", "disable"]
VALID_BODY_WEB_AUTH_COOKIE: Literal["enable", "disable"]
VALID_BODY_CORS_STATEFUL: Literal["enable", "disable"]
VALID_BODY_CERT_AUTH_COOKIE: Literal["enable", "disable"]
VALID_BODY_TRANSACTION_BASED: Literal["enable", "disable"]
VALID_BODY_WEB_PORTAL: Literal["enable", "disable"]
VALID_BODY_SESSION_LOGOUT: Literal["enable", "disable"]

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
    "VALID_BODY_STATUS",
    "VALID_BODY_PROTOCOL",
    "VALID_BODY_IP_BASED",
    "VALID_BODY_WEB_AUTH_COOKIE",
    "VALID_BODY_CORS_STATEFUL",
    "VALID_BODY_CERT_AUTH_COOKIE",
    "VALID_BODY_TRANSACTION_BASED",
    "VALID_BODY_WEB_PORTAL",
    "VALID_BODY_SESSION_LOGOUT",
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