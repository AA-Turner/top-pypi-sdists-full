from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ABR_TYPE: Literal["cisco", "ibm", "shortcut", "standard"]
VALID_BODY_DATABASE_OVERFLOW: Literal["enable", "disable"]
VALID_BODY_DEFAULT_INFORMATION_ORIGINATE: Literal["enable", "always", "disable"]
VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE: Literal["1", "2"]
VALID_BODY_RFC1583_COMPATIBLE: Literal["enable", "disable"]
VALID_BODY_BFD: Literal["enable", "disable"]
VALID_BODY_LOG_NEIGHBOUR_CHANGES: Literal["enable", "disable"]
VALID_BODY_RESTART_MODE: Literal["none", "lls", "graceful-restart"]
VALID_BODY_RESTART_ON_TOPOLOGY_CHANGE: Literal["enable", "disable"]

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
    "VALID_BODY_ABR_TYPE",
    "VALID_BODY_DATABASE_OVERFLOW",
    "VALID_BODY_DEFAULT_INFORMATION_ORIGINATE",
    "VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE",
    "VALID_BODY_RFC1583_COMPATIBLE",
    "VALID_BODY_BFD",
    "VALID_BODY_LOG_NEIGHBOUR_CHANGES",
    "VALID_BODY_RESTART_MODE",
    "VALID_BODY_RESTART_ON_TOPOLOGY_CHANGE",
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