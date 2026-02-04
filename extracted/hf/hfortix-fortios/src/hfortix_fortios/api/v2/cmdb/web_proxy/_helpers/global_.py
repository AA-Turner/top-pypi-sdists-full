"""Validation helpers for web_proxy/global_ - Auto-generated"""

from typing import Any, TypedDict, Literal
from typing_extensions import NotRequired

# Import common validators from central _helpers module
from hfortix_fortios._helpers import (
    validate_enable_disable,
    validate_integer_range,
    validate_string_length,
    validate_port_number,
    validate_ip_address,
    validate_ipv6_address,
    validate_mac_address,
)

# Import central validation functions (avoid duplication across 1,062 files)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields,
    validate_enum_field as _validate_enum_field,
    validate_query_parameter as _validate_query_parameter,
)

# ============================================================================
# Required Fields Validation
# Auto-generated from schema
# ============================================================================

# ⚠️  IMPORTANT: FortiOS schemas have known issues with required field marking:

# Do NOT use this list for strict validation - test with the actual FortiOS API!

# Fields marked as required (after filtering false positives)
REQUIRED_FIELDS = [
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ssl-cert": "Fortinet_Factory",
    "ssl-ca-cert": "Fortinet_CA_SSL",
    "fast-policy-match": "enable",
    "ldap-user-cache": "disable",
    "proxy-fqdn": "default.fqdn",
    "max-request-length": 8,
    "max-message-length": 32,
    "http2-client-window-size": 1048576,
    "http2-server-window-size": 1048576,
    "auth-sign-timeout": 120,
    "strict-web-check": "disable",
    "forward-proxy-auth": "disable",
    "forward-server-affinity-timeout": 30,
    "max-waf-body-cache-length": 1,
    "webproxy-profile": "",
    "learn-client-ip": "disable",
    "always-learn-client-ip": "disable",
    "learn-client-ip-from-header": "",
    "src-affinity-exempt-addr": "",
    "src-affinity-exempt-addr6": "",
    "policy-partial-match": "enable",
    "log-policy-pending": "disable",
    "log-forward-server": "disable",
    "log-app-id": "disable",
    "proxy-transparent-cert-inspection": "disable",
    "request-obs-fold": "keep",
}

# ============================================================================
# Deprecated Fields
# Auto-generated from schema - warns users about deprecated fields
# ============================================================================

# Deprecated fields with migration guidance
DEPRECATED_FIELDS = {
}

# ============================================================================
# Field Metadata (Type Information & Descriptions)
# Auto-generated from schema - use for IDE autocomplete and documentation
# ============================================================================

# Field types mapping
FIELD_TYPES = {
    "ssl-cert": "string",  # SSL certificate for SSL interception.
    "ssl-ca-cert": "string",  # SSL CA certificate for SSL interception.
    "fast-policy-match": "option",  # Enable/disable fast matching algorithm for explicit and transparent proxy policy
    "ldap-user-cache": "option",  # Enable/disable LDAP user cache for explicit and transparent proxy user.
    "proxy-fqdn": "string",  # Fully Qualified Domain Name of the explicit web proxy (default = default.fqdn) t
    "max-request-length": "integer",  # Maximum length of HTTP request line (2 - 64 Kbytes, default = 8).
    "max-message-length": "integer",  # Maximum length of HTTP message, not including body (16 - 256 Kbytes, default = 3
    "http2-client-window-size": "integer",  # HTTP/2 client initial window size in bytes (65535 - 2147483647, default = 104857
    "http2-server-window-size": "integer",  # HTTP/2 server initial window size in bytes (65535 - 2147483647, default = 104857
    "auth-sign-timeout": "integer",  # Proxy auth query sign timeout in seconds (30 - 3600, default = 120).
    "strict-web-check": "option",  # Enable/disable strict web checking to block web sites that send incorrect header
    "forward-proxy-auth": "option",  # Enable/disable forwarding proxy authentication headers.
    "forward-server-affinity-timeout": "integer",  # Period of time before the source IP's traffic is no longer assigned to the forwa
    "max-waf-body-cache-length": "integer",  # Maximum length of HTTP messages processed by Web Application Firewall (WAF) (1 -
    "webproxy-profile": "string",  # Name of the web proxy profile to apply when explicit proxy traffic is allowed by
    "learn-client-ip": "option",  # Enable/disable learning the client's IP address from headers.
    "always-learn-client-ip": "option",  # Enable/disable learning the client's IP address from headers for every request.
    "learn-client-ip-from-header": "option",  # Learn client IP address from the specified headers.
    "learn-client-ip-srcaddr": "string",  # Source address name (srcaddr or srcaddr6 must be set).
    "learn-client-ip-srcaddr6": "string",  # IPv6 Source address name (srcaddr or srcaddr6 must be set).
    "src-affinity-exempt-addr": "ipv4-address-any",  # IPv4 source addresses to exempt proxy affinity.
    "src-affinity-exempt-addr6": "ipv6-address",  # IPv6 source addresses to exempt proxy affinity.
    "policy-partial-match": "option",  # Enable/disable policy partial matching.
    "log-policy-pending": "option",  # Enable/disable logging sessions that are pending on policy matching.
    "log-forward-server": "option",  # Enable/disable forward server name logging in forward traffic log.
    "log-app-id": "option",  # Enable/disable always log application type in traffic log.
    "proxy-transparent-cert-inspection": "option",  # Enable/disable transparent proxy certificate inspection.
    "request-obs-fold": "option",  # Action when HTTP/1.x request header contains obs-fold (default = keep).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ssl-cert": "SSL certificate for SSL interception.",
    "ssl-ca-cert": "SSL CA certificate for SSL interception.",
    "fast-policy-match": "Enable/disable fast matching algorithm for explicit and transparent proxy policy.",
    "ldap-user-cache": "Enable/disable LDAP user cache for explicit and transparent proxy user.",
    "proxy-fqdn": "Fully Qualified Domain Name of the explicit web proxy (default = default.fqdn) that clients connect to.",
    "max-request-length": "Maximum length of HTTP request line (2 - 64 Kbytes, default = 8).",
    "max-message-length": "Maximum length of HTTP message, not including body (16 - 256 Kbytes, default = 32).",
    "http2-client-window-size": "HTTP/2 client initial window size in bytes (65535 - 2147483647, default = 1048576 (1MB)).",
    "http2-server-window-size": "HTTP/2 server initial window size in bytes (65535 - 2147483647, default = 1048576 (1MB)).",
    "auth-sign-timeout": "Proxy auth query sign timeout in seconds (30 - 3600, default = 120).",
    "strict-web-check": "Enable/disable strict web checking to block web sites that send incorrect headers that don't conform to HTTP.",
    "forward-proxy-auth": "Enable/disable forwarding proxy authentication headers.",
    "forward-server-affinity-timeout": "Period of time before the source IP's traffic is no longer assigned to the forwarding server (6 - 60 min, default = 30).",
    "max-waf-body-cache-length": "Maximum length of HTTP messages processed by Web Application Firewall (WAF) (1 - 1024 Kbytes, default = 1).",
    "webproxy-profile": "Name of the web proxy profile to apply when explicit proxy traffic is allowed by default and traffic is accepted that does not match an explicit proxy policy.",
    "learn-client-ip": "Enable/disable learning the client's IP address from headers.",
    "always-learn-client-ip": "Enable/disable learning the client's IP address from headers for every request.",
    "learn-client-ip-from-header": "Learn client IP address from the specified headers.",
    "learn-client-ip-srcaddr": "Source address name (srcaddr or srcaddr6 must be set).",
    "learn-client-ip-srcaddr6": "IPv6 Source address name (srcaddr or srcaddr6 must be set).",
    "src-affinity-exempt-addr": "IPv4 source addresses to exempt proxy affinity.",
    "src-affinity-exempt-addr6": "IPv6 source addresses to exempt proxy affinity.",
    "policy-partial-match": "Enable/disable policy partial matching.",
    "log-policy-pending": "Enable/disable logging sessions that are pending on policy matching.",
    "log-forward-server": "Enable/disable forward server name logging in forward traffic log.",
    "log-app-id": "Enable/disable always log application type in traffic log.",
    "proxy-transparent-cert-inspection": "Enable/disable transparent proxy certificate inspection.",
    "request-obs-fold": "Action when HTTP/1.x request header contains obs-fold (default = keep).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "ssl-cert": {"type": "string", "max_length": 35},
    "ssl-ca-cert": {"type": "string", "max_length": 35},
    "proxy-fqdn": {"type": "string", "max_length": 255},
    "max-request-length": {"type": "integer", "min": 2, "max": 64},
    "max-message-length": {"type": "integer", "min": 16, "max": 256},
    "http2-client-window-size": {"type": "integer", "min": 65535, "max": 2147483647},
    "http2-server-window-size": {"type": "integer", "min": 65535, "max": 2147483647},
    "auth-sign-timeout": {"type": "integer", "min": 30, "max": 3600},
    "forward-server-affinity-timeout": {"type": "integer", "min": 6, "max": 60},
    "max-waf-body-cache-length": {"type": "integer", "min": 1, "max": 1024},
    "webproxy-profile": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "learn-client-ip-srcaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "learn-client-ip-srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FAST_POLICY_MATCH = [
    "enable",
    "disable",
]
VALID_BODY_LDAP_USER_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_STRICT_WEB_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_FORWARD_PROXY_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_LEARN_CLIENT_IP = [
    "enable",
    "disable",
]
VALID_BODY_ALWAYS_LEARN_CLIENT_IP = [
    "enable",
    "disable",
]
VALID_BODY_LEARN_CLIENT_IP_FROM_HEADER = [
    "true-client-ip",
    "x-real-ip",
    "x-forwarded-for",
]
VALID_BODY_POLICY_PARTIAL_MATCH = [
    "enable",
    "disable",
]
VALID_BODY_LOG_POLICY_PENDING = [
    "enable",
    "disable",
]
VALID_BODY_LOG_FORWARD_SERVER = [
    "enable",
    "disable",
]
VALID_BODY_LOG_APP_ID = [
    "enable",
    "disable",
]
VALID_BODY_PROXY_TRANSPARENT_CERT_INSPECTION = [
    "enable",
    "disable",
]
VALID_BODY_REQUEST_OBS_FOLD = [
    "replace-with-sp",
    "block",
    "keep",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_web_proxy_global_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for web_proxy/global_."""
    # Validate query parameters using central function
    if "action" in params:
        is_valid, error = _validate_query_parameter(
            "action",
            params.get("action"),
            VALID_QUERY_ACTION
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# POST Validation
# ============================================================================


def validate_web_proxy_global_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new web_proxy/global_ object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "fast-policy-match" in payload:
        is_valid, error = _validate_enum_field(
            "fast-policy-match",
            payload["fast-policy-match"],
            VALID_BODY_FAST_POLICY_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldap-user-cache" in payload:
        is_valid, error = _validate_enum_field(
            "ldap-user-cache",
            payload["ldap-user-cache"],
            VALID_BODY_LDAP_USER_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-web-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-web-check",
            payload["strict-web-check"],
            VALID_BODY_STRICT_WEB_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forward-proxy-auth" in payload:
        is_valid, error = _validate_enum_field(
            "forward-proxy-auth",
            payload["forward-proxy-auth"],
            VALID_BODY_FORWARD_PROXY_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learn-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "learn-client-ip",
            payload["learn-client-ip"],
            VALID_BODY_LEARN_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "always-learn-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "always-learn-client-ip",
            payload["always-learn-client-ip"],
            VALID_BODY_ALWAYS_LEARN_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learn-client-ip-from-header" in payload:
        is_valid, error = _validate_enum_field(
            "learn-client-ip-from-header",
            payload["learn-client-ip-from-header"],
            VALID_BODY_LEARN_CLIENT_IP_FROM_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-partial-match" in payload:
        is_valid, error = _validate_enum_field(
            "policy-partial-match",
            payload["policy-partial-match"],
            VALID_BODY_POLICY_PARTIAL_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-policy-pending" in payload:
        is_valid, error = _validate_enum_field(
            "log-policy-pending",
            payload["log-policy-pending"],
            VALID_BODY_LOG_POLICY_PENDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-forward-server" in payload:
        is_valid, error = _validate_enum_field(
            "log-forward-server",
            payload["log-forward-server"],
            VALID_BODY_LOG_FORWARD_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-app-id" in payload:
        is_valid, error = _validate_enum_field(
            "log-app-id",
            payload["log-app-id"],
            VALID_BODY_LOG_APP_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-transparent-cert-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-transparent-cert-inspection",
            payload["proxy-transparent-cert-inspection"],
            VALID_BODY_PROXY_TRANSPARENT_CERT_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-obs-fold" in payload:
        is_valid, error = _validate_enum_field(
            "request-obs-fold",
            payload["request-obs-fold"],
            VALID_BODY_REQUEST_OBS_FOLD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_web_proxy_global_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update web_proxy/global_."""
    # Validate enum values using central function
    if "fast-policy-match" in payload:
        is_valid, error = _validate_enum_field(
            "fast-policy-match",
            payload["fast-policy-match"],
            VALID_BODY_FAST_POLICY_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldap-user-cache" in payload:
        is_valid, error = _validate_enum_field(
            "ldap-user-cache",
            payload["ldap-user-cache"],
            VALID_BODY_LDAP_USER_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-web-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-web-check",
            payload["strict-web-check"],
            VALID_BODY_STRICT_WEB_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forward-proxy-auth" in payload:
        is_valid, error = _validate_enum_field(
            "forward-proxy-auth",
            payload["forward-proxy-auth"],
            VALID_BODY_FORWARD_PROXY_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learn-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "learn-client-ip",
            payload["learn-client-ip"],
            VALID_BODY_LEARN_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "always-learn-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "always-learn-client-ip",
            payload["always-learn-client-ip"],
            VALID_BODY_ALWAYS_LEARN_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learn-client-ip-from-header" in payload:
        is_valid, error = _validate_enum_field(
            "learn-client-ip-from-header",
            payload["learn-client-ip-from-header"],
            VALID_BODY_LEARN_CLIENT_IP_FROM_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-partial-match" in payload:
        is_valid, error = _validate_enum_field(
            "policy-partial-match",
            payload["policy-partial-match"],
            VALID_BODY_POLICY_PARTIAL_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-policy-pending" in payload:
        is_valid, error = _validate_enum_field(
            "log-policy-pending",
            payload["log-policy-pending"],
            VALID_BODY_LOG_POLICY_PENDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-forward-server" in payload:
        is_valid, error = _validate_enum_field(
            "log-forward-server",
            payload["log-forward-server"],
            VALID_BODY_LOG_FORWARD_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-app-id" in payload:
        is_valid, error = _validate_enum_field(
            "log-app-id",
            payload["log-app-id"],
            VALID_BODY_LOG_APP_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-transparent-cert-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-transparent-cert-inspection",
            payload["proxy-transparent-cert-inspection"],
            VALID_BODY_PROXY_TRANSPARENT_CERT_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-obs-fold" in payload:
        is_valid, error = _validate_enum_field(
            "request-obs-fold",
            payload["request-obs-fold"],
            VALID_BODY_REQUEST_OBS_FOLD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# Metadata Access Functions
# Imported from central module to avoid duplication across 1,062 files
# Bound to this endpoint's data using functools.partial (saves ~7KB per file)
# ============================================================================

from functools import partial
from hfortix_fortios._helpers.metadata import (
    get_field_description,
    get_field_type,
    get_field_constraints,
    get_field_default,
    get_field_options,
    get_nested_schema,
    get_all_fields,
    get_field_metadata,
    validate_field_value,
)

# Bind module-specific data to central functions using partial application
get_field_description = partial(get_field_description, FIELD_DESCRIPTIONS)
get_field_type = partial(get_field_type, FIELD_TYPES)
get_field_constraints = partial(get_field_constraints, FIELD_CONSTRAINTS)
get_field_default = partial(get_field_default, FIELDS_WITH_DEFAULTS)
get_field_options = partial(get_field_options, globals())
get_nested_schema = partial(get_nested_schema, NESTED_SCHEMAS)
get_all_fields = partial(get_all_fields, FIELD_TYPES)
get_field_metadata = partial(get_field_metadata, FIELD_TYPES, FIELD_DESCRIPTIONS, 
                             FIELD_CONSTRAINTS, FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS,
                             NESTED_SCHEMAS, globals())
validate_field_value = partial(validate_field_value, FIELD_TYPES, FIELD_DESCRIPTIONS,
                               FIELD_CONSTRAINTS, globals())


# ============================================================================
# Schema Information
# Metadata about this endpoint schema
# ============================================================================

SCHEMA_INFO = {
    "endpoint": "web_proxy/global_",
    "category": "cmdb",
    "api_path": "web-proxy/global",
    "help": "Configure Web proxy global settings.",
    "total_fields": 28,
    "required_fields_count": 0,
    "fields_with_defaults_count": 26,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
