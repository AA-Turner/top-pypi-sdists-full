from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FASTPATH: Literal["disable", "enable"]
VALID_BODY_PER_SESSION_ACCOUNTING: Literal["disable", "traffic-log-only", "enable"]
VALID_BODY_IPSEC_INNER_FRAGMENT: Literal["disable", "enable"]
VALID_BODY_IPSEC_THROUGHPUT_MSG_FREQUENCY: Literal["disable", "32kb", "64kb", "128kb", "256kb", "512kb", "1mb", "2mb", "4mb", "8mb", "16mb", "32mb", "64mb", "128mb", "256mb", "512mb", "1gb"]
VALID_BODY_IPSEC_STS_TIMEOUT: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

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
    "VALID_BODY_FASTPATH",
    "VALID_BODY_PER_SESSION_ACCOUNTING",
    "VALID_BODY_IPSEC_INNER_FRAGMENT",
    "VALID_BODY_IPSEC_THROUGHPUT_MSG_FREQUENCY",
    "VALID_BODY_IPSEC_STS_TIMEOUT",
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