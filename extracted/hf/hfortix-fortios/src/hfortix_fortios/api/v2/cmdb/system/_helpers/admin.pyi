from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_REMOTE_AUTH: Literal["enable", "disable"]
VALID_BODY_WILDCARD: Literal["enable", "disable"]
VALID_BODY_PEER_AUTH: Literal["enable", "disable"]
VALID_BODY_ALLOW_REMOVE_ADMIN_SESSION: Literal["enable", "disable"]
VALID_BODY_ACCPROFILE_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_VDOM_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_FORCE_PASSWORD_CHANGE: Literal["enable", "disable"]
VALID_BODY_TWO_FACTOR: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"]
VALID_BODY_TWO_FACTOR_AUTHENTICATION: Literal["fortitoken", "email", "sms"]
VALID_BODY_TWO_FACTOR_NOTIFICATION: Literal["email", "sms"]
VALID_BODY_SMS_SERVER: Literal["fortiguard", "custom"]
VALID_BODY_GUEST_AUTH: Literal["disable", "enable"]

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
    "VALID_BODY_REMOTE_AUTH",
    "VALID_BODY_WILDCARD",
    "VALID_BODY_PEER_AUTH",
    "VALID_BODY_ALLOW_REMOVE_ADMIN_SESSION",
    "VALID_BODY_ACCPROFILE_OVERRIDE",
    "VALID_BODY_VDOM_OVERRIDE",
    "VALID_BODY_FORCE_PASSWORD_CHANGE",
    "VALID_BODY_TWO_FACTOR",
    "VALID_BODY_TWO_FACTOR_AUTHENTICATION",
    "VALID_BODY_TWO_FACTOR_NOTIFICATION",
    "VALID_BODY_SMS_SERVER",
    "VALID_BODY_GUEST_AUTH",
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