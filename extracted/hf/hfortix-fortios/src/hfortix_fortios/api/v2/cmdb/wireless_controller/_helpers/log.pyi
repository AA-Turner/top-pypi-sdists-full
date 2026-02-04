from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_ADDRGRP_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_BLE_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_CLB_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_DHCP_STARV_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_LED_SCHED_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_RADIO_EVENT_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_ROGUE_EVENT_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_STA_EVENT_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_STA_LOCATE_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_WIDS_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_WTP_EVENT_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
VALID_BODY_WTP_FIPS_EVENT_LOG: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]

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
    "VALID_BODY_STATUS",
    "VALID_BODY_ADDRGRP_LOG",
    "VALID_BODY_BLE_LOG",
    "VALID_BODY_CLB_LOG",
    "VALID_BODY_DHCP_STARV_LOG",
    "VALID_BODY_LED_SCHED_LOG",
    "VALID_BODY_RADIO_EVENT_LOG",
    "VALID_BODY_ROGUE_EVENT_LOG",
    "VALID_BODY_STA_EVENT_LOG",
    "VALID_BODY_STA_LOCATE_LOG",
    "VALID_BODY_WIDS_LOG",
    "VALID_BODY_WTP_EVENT_LOG",
    "VALID_BODY_WTP_FIPS_EVENT_LOG",
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