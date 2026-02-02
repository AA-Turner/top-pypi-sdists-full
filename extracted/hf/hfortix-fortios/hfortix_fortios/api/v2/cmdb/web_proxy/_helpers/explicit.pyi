from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["enable", "disable"]
VALID_BODY_SECURE_WEB_PROXY: Literal["disable", "enable", "secure"]
VALID_BODY_FTP_OVER_HTTP: Literal["enable", "disable"]
VALID_BODY_SOCKS: Literal["enable", "disable"]
VALID_BODY_HTTP_CONNECTION_MODE: Literal["static", "multiplex", "serverpool"]
VALID_BODY_CLIENT_CERT: Literal["disable", "enable"]
VALID_BODY_USER_AGENT_DETECT: Literal["disable", "enable"]
VALID_BODY_EMPTY_CERT_ACTION: Literal["accept", "block", "accept-unmanageable"]
VALID_BODY_SSL_DH_BITS: Literal["768", "1024", "1536", "2048"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["sdwan", "specify"]
VALID_BODY_IPV6_STATUS: Literal["enable", "disable"]
VALID_BODY_STRICT_GUEST: Literal["enable", "disable"]
VALID_BODY_PREF_DNS_RESULT: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"]
VALID_BODY_UNKNOWN_HTTP_VERSION: Literal["reject", "best-effort"]
VALID_BODY_SEC_DEFAULT_ACTION: Literal["accept", "deny"]
VALID_BODY_HTTPS_REPLACEMENT_MESSAGE: Literal["enable", "disable"]
VALID_BODY_MESSAGE_UPON_SERVER_ERROR: Literal["enable", "disable"]
VALID_BODY_PAC_FILE_SERVER_STATUS: Literal["enable", "disable"]
VALID_BODY_PAC_FILE_THROUGH_HTTPS: Literal["enable", "disable"]
VALID_BODY_SSL_ALGORITHM: Literal["high", "medium", "low"]
VALID_BODY_TRACE_AUTH_NO_RSP: Literal["enable", "disable"]

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
    "VALID_BODY_SECURE_WEB_PROXY",
    "VALID_BODY_FTP_OVER_HTTP",
    "VALID_BODY_SOCKS",
    "VALID_BODY_HTTP_CONNECTION_MODE",
    "VALID_BODY_CLIENT_CERT",
    "VALID_BODY_USER_AGENT_DETECT",
    "VALID_BODY_EMPTY_CERT_ACTION",
    "VALID_BODY_SSL_DH_BITS",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
    "VALID_BODY_IPV6_STATUS",
    "VALID_BODY_STRICT_GUEST",
    "VALID_BODY_PREF_DNS_RESULT",
    "VALID_BODY_UNKNOWN_HTTP_VERSION",
    "VALID_BODY_SEC_DEFAULT_ACTION",
    "VALID_BODY_HTTPS_REPLACEMENT_MESSAGE",
    "VALID_BODY_MESSAGE_UPON_SERVER_ERROR",
    "VALID_BODY_PAC_FILE_SERVER_STATUS",
    "VALID_BODY_PAC_FILE_THROUGH_HTTPS",
    "VALID_BODY_SSL_ALGORITHM",
    "VALID_BODY_TRACE_AUTH_NO_RSP",
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