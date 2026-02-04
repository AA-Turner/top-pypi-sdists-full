from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_MONITOR_ALL_MESSAGES: Literal["disable", "enable"]
VALID_BODY_LOG_PACKET: Literal["disable", "enable"]
VALID_BODY_TRACK_REQUESTS_ANSWERS: Literal["disable", "enable"]
VALID_BODY_MISSING_REQUEST_ACTION: Literal["allow", "block", "reset", "monitor"]
VALID_BODY_PROTOCOL_VERSION_INVALID: Literal["allow", "block", "reset", "monitor"]
VALID_BODY_MESSAGE_LENGTH_INVALID: Literal["allow", "block", "reset", "monitor"]
VALID_BODY_REQUEST_ERROR_FLAG_SET: Literal["allow", "block", "reset", "monitor"]
VALID_BODY_CMD_FLAGS_RESERVE_SET: Literal["allow", "block", "reset", "monitor"]
VALID_BODY_COMMAND_CODE_INVALID: Literal["allow", "block", "reset", "monitor"]

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
    "VALID_BODY_MONITOR_ALL_MESSAGES",
    "VALID_BODY_LOG_PACKET",
    "VALID_BODY_TRACK_REQUESTS_ANSWERS",
    "VALID_BODY_MISSING_REQUEST_ACTION",
    "VALID_BODY_PROTOCOL_VERSION_INVALID",
    "VALID_BODY_MESSAGE_LENGTH_INVALID",
    "VALID_BODY_REQUEST_ERROR_FLAG_SET",
    "VALID_BODY_CMD_FLAGS_RESERVE_SET",
    "VALID_BODY_COMMAND_CODE_INVALID",
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