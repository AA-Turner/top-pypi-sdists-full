from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_FEATURE_SET: Literal["flow", "proxy"]
VALID_BODY_OPTIONS: Literal["activexfilter", "cookiefilter", "javafilter", "block-invalid-url", "jscript", "js", "vbs", "unknown", "intrinsic", "wf-referer", "wf-cookie", "per-user-bal"]
VALID_BODY_HTTPS_REPLACEMSG: Literal["enable", "disable"]
VALID_BODY_WEB_FLOW_LOG_ENCODING: Literal["utf-8", "punycode"]
VALID_BODY_OVRD_PERM: Literal["bannedword-override", "urlfilter-override", "fortiguard-wf-override", "contenttype-check-override"]
VALID_BODY_POST_ACTION: Literal["normal", "block"]
VALID_BODY_WISP: Literal["enable", "disable"]
VALID_BODY_WISP_ALGORITHM: Literal["primary-secondary", "round-robin", "auto-learning"]
VALID_BODY_LOG_ALL_URL: Literal["enable", "disable"]
VALID_BODY_WEB_CONTENT_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_ACTIVEX_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_COMMAND_BLOCK_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_COOKIE_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_APPLET_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_JSCRIPT_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_JS_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_VBS_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_UNKNOWN_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_REFERER_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FILTER_COOKIE_REMOVAL_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_URL_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_INVALID_DOMAIN_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FTGD_ERR_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_FTGD_QUOTA_USAGE: Literal["enable", "disable"]
VALID_BODY_EXTENDED_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_EXTENDED_ALL_ACTION_LOG: Literal["enable", "disable"]
VALID_BODY_WEB_ANTIPHISHING_LOG: Literal["enable", "disable"]

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
    "VALID_BODY_OPTIONS",
    "VALID_BODY_HTTPS_REPLACEMSG",
    "VALID_BODY_WEB_FLOW_LOG_ENCODING",
    "VALID_BODY_OVRD_PERM",
    "VALID_BODY_POST_ACTION",
    "VALID_BODY_WISP",
    "VALID_BODY_WISP_ALGORITHM",
    "VALID_BODY_LOG_ALL_URL",
    "VALID_BODY_WEB_CONTENT_LOG",
    "VALID_BODY_WEB_FILTER_ACTIVEX_LOG",
    "VALID_BODY_WEB_FILTER_COMMAND_BLOCK_LOG",
    "VALID_BODY_WEB_FILTER_COOKIE_LOG",
    "VALID_BODY_WEB_FILTER_APPLET_LOG",
    "VALID_BODY_WEB_FILTER_JSCRIPT_LOG",
    "VALID_BODY_WEB_FILTER_JS_LOG",
    "VALID_BODY_WEB_FILTER_VBS_LOG",
    "VALID_BODY_WEB_FILTER_UNKNOWN_LOG",
    "VALID_BODY_WEB_FILTER_REFERER_LOG",
    "VALID_BODY_WEB_FILTER_COOKIE_REMOVAL_LOG",
    "VALID_BODY_WEB_URL_LOG",
    "VALID_BODY_WEB_INVALID_DOMAIN_LOG",
    "VALID_BODY_WEB_FTGD_ERR_LOG",
    "VALID_BODY_WEB_FTGD_QUOTA_USAGE",
    "VALID_BODY_EXTENDED_LOG",
    "VALID_BODY_WEB_EXTENDED_ALL_ACTION_LOG",
    "VALID_BODY_WEB_ANTIPHISHING_LOG",
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