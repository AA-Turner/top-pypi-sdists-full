from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_UPLOAD_OPTION: Literal["store-and-upload", "realtime", "1-minute", "5-minute"]
VALID_BODY_UPLOAD_INTERVAL: Literal["daily", "weekly", "monthly"]
VALID_BODY_PRIORITY: Literal["default", "low"]
VALID_BODY_ACCESS_CONFIG: Literal["enable", "disable"]
VALID_BODY_ENC_ALGORITHM: Literal["high-medium", "high", "low"]
VALID_BODY_SSL_MIN_PROTO_VERSION: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]

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
    "VALID_BODY_UPLOAD_OPTION",
    "VALID_BODY_UPLOAD_INTERVAL",
    "VALID_BODY_PRIORITY",
    "VALID_BODY_ACCESS_CONFIG",
    "VALID_BODY_ENC_ALGORITHM",
    "VALID_BODY_SSL_MIN_PROTO_VERSION",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
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