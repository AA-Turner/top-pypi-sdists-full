from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_EGRESS_PRI_TAGGING: Literal["disable", "enable"]
VALID_BODY_PRIORITY_0: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_1: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_2: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_3: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_4: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_5: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_6: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]
VALID_BODY_PRIORITY_7: Literal["queue-0", "queue-1", "queue-2", "queue-3", "queue-4", "queue-5", "queue-6", "queue-7"]

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
    "VALID_BODY_EGRESS_PRI_TAGGING",
    "VALID_BODY_PRIORITY_0",
    "VALID_BODY_PRIORITY_1",
    "VALID_BODY_PRIORITY_2",
    "VALID_BODY_PRIORITY_3",
    "VALID_BODY_PRIORITY_4",
    "VALID_BODY_PRIORITY_5",
    "VALID_BODY_PRIORITY_6",
    "VALID_BODY_PRIORITY_7",
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