from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_RESOLVE_IP: Literal["enable", "disable"]
VALID_BODY_RESOLVE_PORT: Literal["enable", "disable"]
VALID_BODY_LOG_USER_IN_UPPER: Literal["enable", "disable"]
VALID_BODY_FWPOLICY_IMPLICIT_LOG: Literal["enable", "disable"]
VALID_BODY_FWPOLICY6_IMPLICIT_LOG: Literal["enable", "disable"]
VALID_BODY_EXTENDED_LOG: Literal["enable", "disable"]
VALID_BODY_LOCAL_IN_ALLOW: Literal["enable", "disable"]
VALID_BODY_LOCAL_IN_DENY_UNICAST: Literal["enable", "disable"]
VALID_BODY_LOCAL_IN_DENY_BROADCAST: Literal["enable", "disable"]
VALID_BODY_LOCAL_IN_POLICY_LOG: Literal["enable", "disable"]
VALID_BODY_LOCAL_OUT: Literal["enable", "disable"]
VALID_BODY_LOCAL_OUT_IOC_DETECTION: Literal["enable", "disable"]
VALID_BODY_DAEMON_LOG: Literal["enable", "disable"]
VALID_BODY_NEIGHBOR_EVENT: Literal["enable", "disable"]
VALID_BODY_BRIEF_TRAFFIC_FORMAT: Literal["enable", "disable"]
VALID_BODY_USER_ANONYMIZE: Literal["enable", "disable"]
VALID_BODY_EXPOLICY_IMPLICIT_LOG: Literal["enable", "disable"]
VALID_BODY_LOG_POLICY_COMMENT: Literal["enable", "disable"]
VALID_BODY_FAZ_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_SYSLOG_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_REST_API_SET: Literal["enable", "disable"]
VALID_BODY_REST_API_GET: Literal["enable", "disable"]
VALID_BODY_REST_API_PERFORMANCE: Literal["enable", "disable"]
VALID_BODY_LONG_LIVE_SESSION_STAT: Literal["enable", "disable"]
VALID_BODY_EXTENDED_UTM_LOG: Literal["enable", "disable"]
VALID_BODY_ZONE_NAME: Literal["enable", "disable"]
VALID_BODY_WEB_SVC_PERF: Literal["enable", "disable"]

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
    "VALID_BODY_RESOLVE_IP",
    "VALID_BODY_RESOLVE_PORT",
    "VALID_BODY_LOG_USER_IN_UPPER",
    "VALID_BODY_FWPOLICY_IMPLICIT_LOG",
    "VALID_BODY_FWPOLICY6_IMPLICIT_LOG",
    "VALID_BODY_EXTENDED_LOG",
    "VALID_BODY_LOCAL_IN_ALLOW",
    "VALID_BODY_LOCAL_IN_DENY_UNICAST",
    "VALID_BODY_LOCAL_IN_DENY_BROADCAST",
    "VALID_BODY_LOCAL_IN_POLICY_LOG",
    "VALID_BODY_LOCAL_OUT",
    "VALID_BODY_LOCAL_OUT_IOC_DETECTION",
    "VALID_BODY_DAEMON_LOG",
    "VALID_BODY_NEIGHBOR_EVENT",
    "VALID_BODY_BRIEF_TRAFFIC_FORMAT",
    "VALID_BODY_USER_ANONYMIZE",
    "VALID_BODY_EXPOLICY_IMPLICIT_LOG",
    "VALID_BODY_LOG_POLICY_COMMENT",
    "VALID_BODY_FAZ_OVERRIDE",
    "VALID_BODY_SYSLOG_OVERRIDE",
    "VALID_BODY_REST_API_SET",
    "VALID_BODY_REST_API_GET",
    "VALID_BODY_REST_API_PERFORMANCE",
    "VALID_BODY_LONG_LIVE_SESSION_STAT",
    "VALID_BODY_EXTENDED_UTM_LOG",
    "VALID_BODY_ZONE_NAME",
    "VALID_BODY_WEB_SVC_PERF",
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