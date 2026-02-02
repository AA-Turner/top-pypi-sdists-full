from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_MODE: Literal["normal", "backup"]
VALID_BODY_TYPE: Literal["fortimanager", "fortiguard", "none"]
VALID_BODY_SCHEDULE_CONFIG_RESTORE: Literal["enable", "disable"]
VALID_BODY_SCHEDULE_SCRIPT_RESTORE: Literal["enable", "disable"]
VALID_BODY_ALLOW_PUSH_CONFIGURATION: Literal["enable", "disable"]
VALID_BODY_ALLOW_PUSH_FIRMWARE: Literal["enable", "disable"]
VALID_BODY_ALLOW_REMOTE_FIRMWARE_UPGRADE: Literal["enable", "disable"]
VALID_BODY_ALLOW_MONITOR: Literal["enable", "disable"]
VALID_BODY_FMG_UPDATE_PORT: Literal["8890", "443"]
VALID_BODY_FMG_UPDATE_HTTP_HEADER: Literal["enable", "disable"]
VALID_BODY_INCLUDE_DEFAULT_SERVERS: Literal["enable", "disable"]
VALID_BODY_ENC_ALGORITHM: Literal["default", "high", "low"]
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
    "VALID_BODY_MODE",
    "VALID_BODY_TYPE",
    "VALID_BODY_SCHEDULE_CONFIG_RESTORE",
    "VALID_BODY_SCHEDULE_SCRIPT_RESTORE",
    "VALID_BODY_ALLOW_PUSH_CONFIGURATION",
    "VALID_BODY_ALLOW_PUSH_FIRMWARE",
    "VALID_BODY_ALLOW_REMOTE_FIRMWARE_UPGRADE",
    "VALID_BODY_ALLOW_MONITOR",
    "VALID_BODY_FMG_UPDATE_PORT",
    "VALID_BODY_FMG_UPDATE_HTTP_HEADER",
    "VALID_BODY_INCLUDE_DEFAULT_SERVERS",
    "VALID_BODY_ENC_ALGORITHM",
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