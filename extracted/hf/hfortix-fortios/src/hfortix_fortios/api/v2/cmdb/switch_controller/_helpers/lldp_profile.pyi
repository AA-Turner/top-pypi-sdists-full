from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_MED_TLVS: Literal["inventory-management", "network-policy", "power-management", "location-identification"]
VALID_BODY_802_1_TLVS: Literal["port-vlan-id"]
VALID_BODY_802_3_TLVS: Literal["max-frame-size", "power-negotiation"]
VALID_BODY_AUTO_ISL: Literal["disable", "enable"]
VALID_BODY_AUTO_MCLAG_ICL: Literal["disable", "enable"]
VALID_BODY_AUTO_ISL_AUTH: Literal["legacy", "strict", "relax"]
VALID_BODY_AUTO_ISL_AUTH_ENCRYPT: Literal["none", "mixed", "must"]

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
    "VALID_BODY_MED_TLVS",
    "VALID_BODY_802_1_TLVS",
    "VALID_BODY_802_3_TLVS",
    "VALID_BODY_AUTO_ISL",
    "VALID_BODY_AUTO_MCLAG_ICL",
    "VALID_BODY_AUTO_ISL_AUTH",
    "VALID_BODY_AUTO_ISL_AUTH_ENCRYPT",
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