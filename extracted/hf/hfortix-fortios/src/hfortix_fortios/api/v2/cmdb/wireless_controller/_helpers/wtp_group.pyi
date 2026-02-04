from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_PLATFORM_TYPE: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]

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
    "VALID_BODY_PLATFORM_TYPE",
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