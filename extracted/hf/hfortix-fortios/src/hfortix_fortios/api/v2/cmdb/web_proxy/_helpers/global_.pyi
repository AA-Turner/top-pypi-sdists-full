from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FAST_POLICY_MATCH: Literal["enable", "disable"]
VALID_BODY_LDAP_USER_CACHE: Literal["enable", "disable"]
VALID_BODY_STRICT_WEB_CHECK: Literal["enable", "disable"]
VALID_BODY_FORWARD_PROXY_AUTH: Literal["enable", "disable"]
VALID_BODY_LEARN_CLIENT_IP: Literal["enable", "disable"]
VALID_BODY_ALWAYS_LEARN_CLIENT_IP: Literal["enable", "disable"]
VALID_BODY_LEARN_CLIENT_IP_FROM_HEADER: Literal["true-client-ip", "x-real-ip", "x-forwarded-for"]
VALID_BODY_POLICY_PARTIAL_MATCH: Literal["enable", "disable"]
VALID_BODY_LOG_POLICY_PENDING: Literal["enable", "disable"]
VALID_BODY_LOG_FORWARD_SERVER: Literal["enable", "disable"]
VALID_BODY_LOG_APP_ID: Literal["enable", "disable"]
VALID_BODY_PROXY_TRANSPARENT_CERT_INSPECTION: Literal["enable", "disable"]
VALID_BODY_REQUEST_OBS_FOLD: Literal["replace-with-sp", "block", "keep"]

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
    "VALID_BODY_FAST_POLICY_MATCH",
    "VALID_BODY_LDAP_USER_CACHE",
    "VALID_BODY_STRICT_WEB_CHECK",
    "VALID_BODY_FORWARD_PROXY_AUTH",
    "VALID_BODY_LEARN_CLIENT_IP",
    "VALID_BODY_ALWAYS_LEARN_CLIENT_IP",
    "VALID_BODY_LEARN_CLIENT_IP_FROM_HEADER",
    "VALID_BODY_POLICY_PARTIAL_MATCH",
    "VALID_BODY_LOG_POLICY_PENDING",
    "VALID_BODY_LOG_FORWARD_SERVER",
    "VALID_BODY_LOG_APP_ID",
    "VALID_BODY_PROXY_TRANSPARENT_CERT_INSPECTION",
    "VALID_BODY_REQUEST_OBS_FOLD",
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