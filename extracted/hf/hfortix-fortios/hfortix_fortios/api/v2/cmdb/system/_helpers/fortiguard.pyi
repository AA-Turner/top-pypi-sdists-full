from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FORTIGUARD_ANYCAST: Literal["enable", "disable"]
VALID_BODY_FORTIGUARD_ANYCAST_SOURCE: Literal["fortinet", "aws", "debug"]
VALID_BODY_PROTOCOL: Literal["udp", "http", "https"]
VALID_BODY_PORT: Literal["8888", "53", "80", "443"]
VALID_BODY_AUTO_JOIN_FORTICLOUD: Literal["enable", "disable"]
VALID_BODY_UPDATE_SERVER_LOCATION: Literal["automatic", "usa", "eu"]
VALID_BODY_SANDBOX_INLINE_SCAN: Literal["enable", "disable"]
VALID_BODY_UPDATE_FFDB: Literal["enable", "disable"]
VALID_BODY_UPDATE_UWDB: Literal["enable", "disable"]
VALID_BODY_UPDATE_DLDB: Literal["enable", "disable"]
VALID_BODY_UPDATE_EXTDB: Literal["enable", "disable"]
VALID_BODY_UPDATE_BUILD_PROXY: Literal["enable", "disable"]
VALID_BODY_PERSISTENT_CONNECTION: Literal["enable", "disable"]
VALID_BODY_AUTO_FIRMWARE_UPGRADE: Literal["enable", "disable"]
VALID_BODY_AUTO_FIRMWARE_UPGRADE_DAY: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
VALID_BODY_SUBSCRIBE_UPDATE_NOTIFICATION: Literal["enable", "disable"]
VALID_BODY_ANTISPAM_FORCE_OFF: Literal["enable", "disable"]
VALID_BODY_ANTISPAM_CACHE: Literal["enable", "disable"]
VALID_BODY_OUTBREAK_PREVENTION_FORCE_OFF: Literal["enable", "disable"]
VALID_BODY_OUTBREAK_PREVENTION_CACHE: Literal["enable", "disable"]
VALID_BODY_WEBFILTER_FORCE_OFF: Literal["enable", "disable"]
VALID_BODY_WEBFILTER_CACHE: Literal["enable", "disable"]
VALID_BODY_SDNS_OPTIONS: Literal["include-question-section"]
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
    "VALID_BODY_FORTIGUARD_ANYCAST",
    "VALID_BODY_FORTIGUARD_ANYCAST_SOURCE",
    "VALID_BODY_PROTOCOL",
    "VALID_BODY_PORT",
    "VALID_BODY_AUTO_JOIN_FORTICLOUD",
    "VALID_BODY_UPDATE_SERVER_LOCATION",
    "VALID_BODY_SANDBOX_INLINE_SCAN",
    "VALID_BODY_UPDATE_FFDB",
    "VALID_BODY_UPDATE_UWDB",
    "VALID_BODY_UPDATE_DLDB",
    "VALID_BODY_UPDATE_EXTDB",
    "VALID_BODY_UPDATE_BUILD_PROXY",
    "VALID_BODY_PERSISTENT_CONNECTION",
    "VALID_BODY_AUTO_FIRMWARE_UPGRADE",
    "VALID_BODY_AUTO_FIRMWARE_UPGRADE_DAY",
    "VALID_BODY_SUBSCRIBE_UPDATE_NOTIFICATION",
    "VALID_BODY_ANTISPAM_FORCE_OFF",
    "VALID_BODY_ANTISPAM_CACHE",
    "VALID_BODY_OUTBREAK_PREVENTION_FORCE_OFF",
    "VALID_BODY_OUTBREAK_PREVENTION_CACHE",
    "VALID_BODY_WEBFILTER_FORCE_OFF",
    "VALID_BODY_WEBFILTER_CACHE",
    "VALID_BODY_SDNS_OPTIONS",
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