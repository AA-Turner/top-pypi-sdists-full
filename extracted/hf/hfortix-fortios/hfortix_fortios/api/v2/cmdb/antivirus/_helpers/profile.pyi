from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FEATURE_SET: Literal["flow", "proxy"]
VALID_BODY_FORTISANDBOX_MODE: Literal["inline", "analytics-suspicious", "analytics-everything"]
VALID_BODY_ANALYTICS_DB: Literal["disable", "enable"]
VALID_BODY_MOBILE_MALWARE_DB: Literal["disable", "enable"]
VALID_BODY_OUTBREAK_PREVENTION_ARCHIVE_SCAN: Literal["disable", "enable"]
VALID_BODY_EXTERNAL_BLOCKLIST_ENABLE_ALL: Literal["disable", "enable"]
VALID_BODY_EMS_THREAT_FEED: Literal["disable", "enable"]
VALID_BODY_FORTINDR_ERROR_ACTION: Literal["log-only", "block", "ignore"]
VALID_BODY_FORTINDR_TIMEOUT_ACTION: Literal["log-only", "block", "ignore"]
VALID_BODY_FORTISANDBOX_ERROR_ACTION: Literal["log-only", "block", "ignore"]
VALID_BODY_FORTISANDBOX_TIMEOUT_ACTION: Literal["log-only", "block", "ignore"]
VALID_BODY_AV_VIRUS_LOG: Literal["enable", "disable"]
VALID_BODY_EXTENDED_LOG: Literal["enable", "disable"]
VALID_BODY_SCAN_MODE: Literal["default", "legacy"]

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
    "VALID_BODY_FEATURE_SET",
    "VALID_BODY_FORTISANDBOX_MODE",
    "VALID_BODY_ANALYTICS_DB",
    "VALID_BODY_MOBILE_MALWARE_DB",
    "VALID_BODY_OUTBREAK_PREVENTION_ARCHIVE_SCAN",
    "VALID_BODY_EXTERNAL_BLOCKLIST_ENABLE_ALL",
    "VALID_BODY_EMS_THREAT_FEED",
    "VALID_BODY_FORTINDR_ERROR_ACTION",
    "VALID_BODY_FORTINDR_TIMEOUT_ACTION",
    "VALID_BODY_FORTISANDBOX_ERROR_ACTION",
    "VALID_BODY_FORTISANDBOX_TIMEOUT_ACTION",
    "VALID_BODY_AV_VIRUS_LOG",
    "VALID_BODY_EXTENDED_LOG",
    "VALID_BODY_SCAN_MODE",
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