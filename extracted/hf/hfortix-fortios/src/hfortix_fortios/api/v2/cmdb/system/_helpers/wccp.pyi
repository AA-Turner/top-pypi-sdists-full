from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_PORTS_DEFINED: Literal["source", "destination"]
VALID_BODY_SERVER_TYPE: Literal["forward", "proxy"]
VALID_BODY_AUTHENTICATION: Literal["enable", "disable"]
VALID_BODY_FORWARD_METHOD: Literal["GRE", "L2", "any"]
VALID_BODY_CACHE_ENGINE_METHOD: Literal["GRE", "L2"]
VALID_BODY_SERVICE_TYPE: Literal["auto", "standard", "dynamic"]
VALID_BODY_PRIMARY_HASH: Literal["src-ip", "dst-ip", "src-port", "dst-port"]
VALID_BODY_ASSIGNMENT_BUCKET_FORMAT: Literal["wccp-v2", "cisco-implementation"]
VALID_BODY_RETURN_METHOD: Literal["GRE", "L2", "any"]
VALID_BODY_ASSIGNMENT_METHOD: Literal["HASH", "MASK", "any"]

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
    "VALID_BODY_PORTS_DEFINED",
    "VALID_BODY_SERVER_TYPE",
    "VALID_BODY_AUTHENTICATION",
    "VALID_BODY_FORWARD_METHOD",
    "VALID_BODY_CACHE_ENGINE_METHOD",
    "VALID_BODY_SERVICE_TYPE",
    "VALID_BODY_PRIMARY_HASH",
    "VALID_BODY_ASSIGNMENT_BUCKET_FORMAT",
    "VALID_BODY_RETURN_METHOD",
    "VALID_BODY_ASSIGNMENT_METHOD",
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