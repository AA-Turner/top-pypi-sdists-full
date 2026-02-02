from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FILTER_MODE: Literal["category", "threshold"]
VALID_BODY_IPS_LOGS: Literal["enable", "disable"]
VALID_BODY_FIREWALL_AUTHENTICATION_FAILURE_LOGS: Literal["enable", "disable"]
VALID_BODY_HA_LOGS: Literal["enable", "disable"]
VALID_BODY_IPSEC_ERRORS_LOGS: Literal["enable", "disable"]
VALID_BODY_FDS_UPDATE_LOGS: Literal["enable", "disable"]
VALID_BODY_PPP_ERRORS_LOGS: Literal["enable", "disable"]
VALID_BODY_SSLVPN_AUTHENTICATION_ERRORS_LOGS: Literal["enable", "disable"]
VALID_BODY_ANTIVIRUS_LOGS: Literal["enable", "disable"]
VALID_BODY_WEBFILTER_LOGS: Literal["enable", "disable"]
VALID_BODY_CONFIGURATION_CHANGES_LOGS: Literal["enable", "disable"]
VALID_BODY_VIOLATION_TRAFFIC_LOGS: Literal["enable", "disable"]
VALID_BODY_ADMIN_LOGIN_LOGS: Literal["enable", "disable"]
VALID_BODY_FDS_LICENSE_EXPIRING_WARNING: Literal["enable", "disable"]
VALID_BODY_LOG_DISK_USAGE_WARNING: Literal["enable", "disable"]
VALID_BODY_FORTIGUARD_LOG_QUOTA_WARNING: Literal["enable", "disable"]
VALID_BODY_AMC_INTERFACE_BYPASS_MODE: Literal["enable", "disable"]
VALID_BODY_FIPS_CC_ERRORS: Literal["enable", "disable"]
VALID_BODY_FSSO_DISCONNECT_LOGS: Literal["enable", "disable"]
VALID_BODY_SSH_LOGS: Literal["enable", "disable"]
VALID_BODY_SEVERITY: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]

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
    "VALID_BODY_FILTER_MODE",
    "VALID_BODY_IPS_LOGS",
    "VALID_BODY_FIREWALL_AUTHENTICATION_FAILURE_LOGS",
    "VALID_BODY_HA_LOGS",
    "VALID_BODY_IPSEC_ERRORS_LOGS",
    "VALID_BODY_FDS_UPDATE_LOGS",
    "VALID_BODY_PPP_ERRORS_LOGS",
    "VALID_BODY_SSLVPN_AUTHENTICATION_ERRORS_LOGS",
    "VALID_BODY_ANTIVIRUS_LOGS",
    "VALID_BODY_WEBFILTER_LOGS",
    "VALID_BODY_CONFIGURATION_CHANGES_LOGS",
    "VALID_BODY_VIOLATION_TRAFFIC_LOGS",
    "VALID_BODY_ADMIN_LOGIN_LOGS",
    "VALID_BODY_FDS_LICENSE_EXPIRING_WARNING",
    "VALID_BODY_LOG_DISK_USAGE_WARNING",
    "VALID_BODY_FORTIGUARD_LOG_QUOTA_WARNING",
    "VALID_BODY_AMC_INTERFACE_BYPASS_MODE",
    "VALID_BODY_FIPS_CC_ERRORS",
    "VALID_BODY_FSSO_DISCONNECT_LOGS",
    "VALID_BODY_SSH_LOGS",
    "VALID_BODY_SEVERITY",
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