from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FAIL_OPEN: Literal["enable", "disable"]
VALID_BODY_DATABASE: Literal["regular", "extended"]
VALID_BODY_TRAFFIC_SUBMIT: Literal["enable", "disable"]
VALID_BODY_ANOMALY_MODE: Literal["periodical", "continuous"]
VALID_BODY_SESSION_LIMIT_MODE: Literal["accurate", "heuristic"]
VALID_BODY_SYNC_SESSION_TTL: Literal["enable", "disable"]
VALID_BODY_EXCLUDE_SIGNATURES: Literal["none", "ot"]
VALID_BODY_MACHINE_LEARNING_DETECTION: Literal["enable", "disable"]

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
    "VALID_BODY_FAIL_OPEN",
    "VALID_BODY_DATABASE",
    "VALID_BODY_TRAFFIC_SUBMIT",
    "VALID_BODY_ANOMALY_MODE",
    "VALID_BODY_SESSION_LIMIT_MODE",
    "VALID_BODY_SYNC_SESSION_TTL",
    "VALID_BODY_EXCLUDE_SIGNATURES",
    "VALID_BODY_MACHINE_LEARNING_DETECTION",
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