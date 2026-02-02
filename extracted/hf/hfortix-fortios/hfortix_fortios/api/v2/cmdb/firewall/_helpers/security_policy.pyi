from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_SRCADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_DSTADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_SRCADDR6_NEGATE: Literal["enable", "disable"]
VALID_BODY_DSTADDR6_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_SRC: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_SRC_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_SRC: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE: Literal["enable", "disable"]
VALID_BODY_ENFORCE_DEFAULT_APP_PORT: Literal["enable", "disable"]
VALID_BODY_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_ACTION: Literal["accept", "deny"]
VALID_BODY_SEND_DENY_PACKET: Literal["disable", "enable"]
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_LOGTRAFFIC: Literal["all", "utm", "disable"]
VALID_BODY_LEARNING_MODE: Literal["enable", "disable"]
VALID_BODY_NAT46: Literal["enable", "disable"]
VALID_BODY_NAT64: Literal["enable", "disable"]
VALID_BODY_PROFILE_TYPE: Literal["single", "group"]

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
    "VALID_BODY_SRCADDR_NEGATE",
    "VALID_BODY_DSTADDR_NEGATE",
    "VALID_BODY_SRCADDR6_NEGATE",
    "VALID_BODY_DSTADDR6_NEGATE",
    "VALID_BODY_INTERNET_SERVICE",
    "VALID_BODY_INTERNET_SERVICE_NEGATE",
    "VALID_BODY_INTERNET_SERVICE_SRC",
    "VALID_BODY_INTERNET_SERVICE_SRC_NEGATE",
    "VALID_BODY_INTERNET_SERVICE6",
    "VALID_BODY_INTERNET_SERVICE6_NEGATE",
    "VALID_BODY_INTERNET_SERVICE6_SRC",
    "VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE",
    "VALID_BODY_ENFORCE_DEFAULT_APP_PORT",
    "VALID_BODY_SERVICE_NEGATE",
    "VALID_BODY_ACTION",
    "VALID_BODY_SEND_DENY_PACKET",
    "VALID_BODY_STATUS",
    "VALID_BODY_LOGTRAFFIC",
    "VALID_BODY_LEARNING_MODE",
    "VALID_BODY_NAT46",
    "VALID_BODY_NAT64",
    "VALID_BODY_PROFILE_TYPE",
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