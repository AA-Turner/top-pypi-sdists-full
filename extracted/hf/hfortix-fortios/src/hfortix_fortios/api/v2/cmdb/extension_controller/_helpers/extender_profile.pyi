from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_MODEL: Literal["FX201E", "FX211E", "FX200F", "FXA11F", "FXE11F", "FXA21F", "FXE21F", "FXA22F", "FXE22F", "FX212F", "FX311F", "FX312F", "FX511F", "FXR51G", "FXN51G", "FXW51G", "FVG21F", "FVA21F", "FVG22F", "FVA22F", "FX04DA", "FG", "BS10FW", "BS20GW", "BS20GN", "FVG51G", "FXE11G", "FX211G"]
VALID_BODY_EXTENSION: Literal["wan-extension", "lan-extension"]
VALID_BODY_ALLOWACCESS: Literal["ping", "telnet", "http", "https", "ssh", "snmp"]
VALID_BODY_LOGIN_PASSWORD_CHANGE: Literal["yes", "default", "no"]
VALID_BODY_ENFORCE_BANDWIDTH: Literal["enable", "disable"]

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
    "VALID_BODY_MODEL",
    "VALID_BODY_EXTENSION",
    "VALID_BODY_ALLOWACCESS",
    "VALID_BODY_LOGIN_PASSWORD_CHANGE",
    "VALID_BODY_ENFORCE_BANDWIDTH",
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