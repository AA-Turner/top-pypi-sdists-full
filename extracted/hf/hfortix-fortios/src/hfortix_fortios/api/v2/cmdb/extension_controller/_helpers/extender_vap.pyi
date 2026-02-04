from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_TYPE: Literal["local-vap", "lan-ext-vap"]
VALID_BODY_BROADCAST_SSID: Literal["disable", "enable"]
VALID_BODY_SECURITY: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"]
VALID_BODY_PMF: Literal["disabled", "optional", "required"]
VALID_BODY_TARGET_WAKE_TIME: Literal["disable", "enable"]
VALID_BODY_BSS_COLOR_PARTIAL: Literal["disable", "enable"]
VALID_BODY_MU_MIMO: Literal["disable", "enable"]
VALID_BODY_ALLOWACCESS: Literal["ping", "telnet", "http", "https", "ssh", "snmp"]

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
    "VALID_BODY_TYPE",
    "VALID_BODY_BROADCAST_SSID",
    "VALID_BODY_SECURITY",
    "VALID_BODY_PMF",
    "VALID_BODY_TARGET_WAKE_TIME",
    "VALID_BODY_BSS_COLOR_PARTIAL",
    "VALID_BODY_MU_MIMO",
    "VALID_BODY_ALLOWACCESS",
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