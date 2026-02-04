from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_IMAGE_DOWNLOAD: Literal["enable", "disable"]
VALID_BODY_ROLLING_WTP_UPGRADE: Literal["enable", "disable"]
VALID_BODY_CONTROL_MESSAGE_OFFLOAD: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"]
VALID_BODY_DATA_ETHERNET_II: Literal["enable", "disable"]
VALID_BODY_LINK_AGGREGATION: Literal["enable", "disable"]
VALID_BODY_WTP_SHARE: Literal["enable", "disable"]
VALID_BODY_TUNNEL_MODE: Literal["compatible", "strict"]
VALID_BODY_AP_LOG_SERVER: Literal["enable", "disable"]

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
    "VALID_BODY_IMAGE_DOWNLOAD",
    "VALID_BODY_ROLLING_WTP_UPGRADE",
    "VALID_BODY_CONTROL_MESSAGE_OFFLOAD",
    "VALID_BODY_DATA_ETHERNET_II",
    "VALID_BODY_LINK_AGGREGATION",
    "VALID_BODY_WTP_SHARE",
    "VALID_BODY_TUNNEL_MODE",
    "VALID_BODY_AP_LOG_SERVER",
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