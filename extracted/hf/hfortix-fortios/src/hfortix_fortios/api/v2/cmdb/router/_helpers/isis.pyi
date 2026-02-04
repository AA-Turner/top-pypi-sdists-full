from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_IS_TYPE: Literal["level-1-2", "level-1", "level-2-only"]
VALID_BODY_ADV_PASSIVE_ONLY: Literal["enable", "disable"]
VALID_BODY_ADV_PASSIVE_ONLY6: Literal["enable", "disable"]
VALID_BODY_AUTH_MODE_L1: Literal["password", "md5"]
VALID_BODY_AUTH_MODE_L2: Literal["password", "md5"]
VALID_BODY_AUTH_SENDONLY_L1: Literal["enable", "disable"]
VALID_BODY_AUTH_SENDONLY_L2: Literal["enable", "disable"]
VALID_BODY_IGNORE_LSP_ERRORS: Literal["enable", "disable"]
VALID_BODY_DYNAMIC_HOSTNAME: Literal["enable", "disable"]
VALID_BODY_ADJACENCY_CHECK: Literal["enable", "disable"]
VALID_BODY_ADJACENCY_CHECK6: Literal["enable", "disable"]
VALID_BODY_OVERLOAD_BIT: Literal["enable", "disable"]
VALID_BODY_OVERLOAD_BIT_SUPPRESS: Literal["external", "interlevel"]
VALID_BODY_DEFAULT_ORIGINATE: Literal["enable", "disable"]
VALID_BODY_DEFAULT_ORIGINATE6: Literal["enable", "disable"]
VALID_BODY_METRIC_STYLE: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"]
VALID_BODY_REDISTRIBUTE_L1: Literal["enable", "disable"]
VALID_BODY_REDISTRIBUTE_L2: Literal["enable", "disable"]
VALID_BODY_REDISTRIBUTE6_L1: Literal["enable", "disable"]
VALID_BODY_REDISTRIBUTE6_L2: Literal["enable", "disable"]

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
    "VALID_BODY_IS_TYPE",
    "VALID_BODY_ADV_PASSIVE_ONLY",
    "VALID_BODY_ADV_PASSIVE_ONLY6",
    "VALID_BODY_AUTH_MODE_L1",
    "VALID_BODY_AUTH_MODE_L2",
    "VALID_BODY_AUTH_SENDONLY_L1",
    "VALID_BODY_AUTH_SENDONLY_L2",
    "VALID_BODY_IGNORE_LSP_ERRORS",
    "VALID_BODY_DYNAMIC_HOSTNAME",
    "VALID_BODY_ADJACENCY_CHECK",
    "VALID_BODY_ADJACENCY_CHECK6",
    "VALID_BODY_OVERLOAD_BIT",
    "VALID_BODY_OVERLOAD_BIT_SUPPRESS",
    "VALID_BODY_DEFAULT_ORIGINATE",
    "VALID_BODY_DEFAULT_ORIGINATE6",
    "VALID_BODY_METRIC_STYLE",
    "VALID_BODY_REDISTRIBUTE_L1",
    "VALID_BODY_REDISTRIBUTE_L2",
    "VALID_BODY_REDISTRIBUTE6_L1",
    "VALID_BODY_REDISTRIBUTE6_L2",
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