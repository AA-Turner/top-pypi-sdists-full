from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_LOG_ALL_DOMAIN: Literal["enable", "disable"]
VALID_BODY_SDNS_FTGD_ERR_LOG: Literal["enable", "disable"]
VALID_BODY_SDNS_DOMAIN_LOG: Literal["enable", "disable"]
VALID_BODY_BLOCK_ACTION: Literal["block", "redirect", "block-sevrfail"]
VALID_BODY_BLOCK_BOTNET: Literal["disable", "enable"]
VALID_BODY_SAFE_SEARCH: Literal["disable", "enable"]
VALID_BODY_YOUTUBE_RESTRICT: Literal["strict", "moderate", "none"]
VALID_BODY_STRIP_ECH: Literal["disable", "enable"]

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
    "VALID_BODY_LOG_ALL_DOMAIN",
    "VALID_BODY_SDNS_FTGD_ERR_LOG",
    "VALID_BODY_SDNS_DOMAIN_LOG",
    "VALID_BODY_BLOCK_ACTION",
    "VALID_BODY_BLOCK_BOTNET",
    "VALID_BODY_SAFE_SEARCH",
    "VALID_BODY_YOUTUBE_RESTRICT",
    "VALID_BODY_STRIP_ECH",
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