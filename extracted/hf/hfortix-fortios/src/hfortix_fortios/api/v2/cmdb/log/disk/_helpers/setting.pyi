from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_IPS_ARCHIVE: Literal["enable", "disable"]
VALID_BODY_ROLL_SCHEDULE: Literal["daily", "weekly"]
VALID_BODY_ROLL_DAY: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
VALID_BODY_DISKFULL: Literal["overwrite", "nolog"]
VALID_BODY_UPLOAD: Literal["enable", "disable"]
VALID_BODY_UPLOAD_DESTINATION: Literal["ftp-server"]
VALID_BODY_UPLOADTYPE: Literal["traffic", "event", "virus", "webfilter", "IPS", "emailfilter", "dlp-archive", "anomaly", "voip", "dlp", "app-ctrl", "waf", "gtp", "dns", "ssh", "ssl", "file-filter", "icap", "virtual-patch", "debug"]
VALID_BODY_UPLOADSCHED: Literal["disable", "enable"]
VALID_BODY_UPLOAD_DELETE_FILES: Literal["enable", "disable"]
VALID_BODY_UPLOAD_SSL_CONN: Literal["default", "high", "low", "disable"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]

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
    "VALID_BODY_IPS_ARCHIVE",
    "VALID_BODY_ROLL_SCHEDULE",
    "VALID_BODY_ROLL_DAY",
    "VALID_BODY_DISKFULL",
    "VALID_BODY_UPLOAD",
    "VALID_BODY_UPLOAD_DESTINATION",
    "VALID_BODY_UPLOADTYPE",
    "VALID_BODY_UPLOADSCHED",
    "VALID_BODY_UPLOAD_DELETE_FILES",
    "VALID_BODY_UPLOAD_SSL_CONN",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
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