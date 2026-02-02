from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_PROXY: Literal["explicit-web", "transparent-web", "ftp", "ssh", "ssh-tunnel", "access-proxy", "ztna-proxy", "wanopt"]
VALID_BODY_ZTNA_TAGS_MATCH_LOGIC: Literal["or", "and"]
VALID_BODY_DEVICE_OWNERSHIP: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6: Literal["enable", "disable"]
VALID_BODY_INTERNET_SERVICE6_NEGATE: Literal["enable", "disable"]
VALID_BODY_SRCADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_DSTADDR_NEGATE: Literal["enable", "disable"]
VALID_BODY_ZTNA_EMS_TAG_NEGATE: Literal["enable", "disable"]
VALID_BODY_SERVICE_NEGATE: Literal["enable", "disable"]
VALID_BODY_ACTION: Literal["accept", "deny", "redirect", "isolate"]
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_LOGTRAFFIC: Literal["all", "utm", "disable"]
VALID_BODY_HTTP_TUNNEL_AUTH: Literal["enable", "disable"]
VALID_BODY_SSH_POLICY_REDIRECT: Literal["enable", "disable"]
VALID_BODY_TRANSPARENT: Literal["enable", "disable"]
VALID_BODY_WEBCACHE: Literal["enable", "disable"]
VALID_BODY_WEBCACHE_HTTPS: Literal["disable", "enable"]
VALID_BODY_DISCLAIMER: Literal["disable", "domain", "policy", "user"]
VALID_BODY_UTM_STATUS: Literal["enable", "disable"]
VALID_BODY_PROFILE_TYPE: Literal["single", "group"]
VALID_BODY_LOGTRAFFIC_START: Literal["enable", "disable"]
VALID_BODY_LOG_HTTP_TRANSACTION: Literal["enable", "disable"]
VALID_BODY_BLOCK_NOTIFICATION: Literal["enable", "disable"]
VALID_BODY_HTTPS_SUB_CATEGORY: Literal["enable", "disable"]
VALID_BODY_DETECT_HTTPS_IN_HTTP_REQUEST: Literal["enable", "disable"]

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
    "VALID_BODY_PROXY",
    "VALID_BODY_ZTNA_TAGS_MATCH_LOGIC",
    "VALID_BODY_DEVICE_OWNERSHIP",
    "VALID_BODY_INTERNET_SERVICE",
    "VALID_BODY_INTERNET_SERVICE_NEGATE",
    "VALID_BODY_INTERNET_SERVICE6",
    "VALID_BODY_INTERNET_SERVICE6_NEGATE",
    "VALID_BODY_SRCADDR_NEGATE",
    "VALID_BODY_DSTADDR_NEGATE",
    "VALID_BODY_ZTNA_EMS_TAG_NEGATE",
    "VALID_BODY_SERVICE_NEGATE",
    "VALID_BODY_ACTION",
    "VALID_BODY_STATUS",
    "VALID_BODY_LOGTRAFFIC",
    "VALID_BODY_HTTP_TUNNEL_AUTH",
    "VALID_BODY_SSH_POLICY_REDIRECT",
    "VALID_BODY_TRANSPARENT",
    "VALID_BODY_WEBCACHE",
    "VALID_BODY_WEBCACHE_HTTPS",
    "VALID_BODY_DISCLAIMER",
    "VALID_BODY_UTM_STATUS",
    "VALID_BODY_PROFILE_TYPE",
    "VALID_BODY_LOGTRAFFIC_START",
    "VALID_BODY_LOG_HTTP_TRANSACTION",
    "VALID_BODY_BLOCK_NOTIFICATION",
    "VALID_BODY_HTTPS_SUB_CATEGORY",
    "VALID_BODY_DETECT_HTTPS_IN_HTTP_REQUEST",
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