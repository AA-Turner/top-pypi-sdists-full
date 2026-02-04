from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_TYPE: Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
VALID_BODY_REFERRER: Literal["enable", "disable"]
VALID_BODY_METHOD: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "update", "patch", "other"]
VALID_BODY_UA: Literal["chrome", "ms", "firefox", "safari", "ie", "edge", "other"]
VALID_BODY_CASE_SENSITIVITY: Literal["disable", "enable"]

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
    "VALID_BODY_REFERRER",
    "VALID_BODY_METHOD",
    "VALID_BODY_UA",
    "VALID_BODY_CASE_SENSITIVITY",
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