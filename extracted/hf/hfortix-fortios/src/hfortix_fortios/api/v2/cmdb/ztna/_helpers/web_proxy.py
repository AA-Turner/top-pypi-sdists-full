"""Validation helpers for ztna/web_proxy - Auto-generated"""

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
    "name": "",
    "vip": "",
    "host": "",
    "decrypted-traffic-mirror": "",
    "log-blocked-traffic": "enable",
    "auth-portal": "disable",
    "auth-virtual-host": "",
    "vip6": "",
    "svr-pool-multiplex": "disable",
    "svr-pool-ttl": 15,
    "svr-pool-server-max-request": 0,
    "svr-pool-server-max-concurrent-request": 0,
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
    "name": "string",  # ZTNA proxy name.
    "vip": "string",  # Virtual IP name.
    "host": "string",  # Virtual or real host name.
    "decrypted-traffic-mirror": "string",  # Decrypted traffic mirror.
    "log-blocked-traffic": "option",  # Enable/disable logging of blocked traffic.
    "auth-portal": "option",  # Enable/disable authentication portal.
    "auth-virtual-host": "string",  # Virtual host for authentication portal.
    "vip6": "string",  # Virtual IPv6 name.
    "svr-pool-multiplex": "option",  # Enable/disable server pool multiplexing (default = disable). Share connected ser
    "svr-pool-ttl": "integer",  # Time-to-live in the server pool for idle connections to servers.
    "svr-pool-server-max-request": "integer",  # Maximum number of requests that servers in the server pool handle before disconn
    "svr-pool-server-max-concurrent-request": "integer",  # Maximum number of concurrent requests that servers in the server pool could hand
    "api-gateway": "string",  # Set IPv4 API Gateway.
    "api-gateway6": "string",  # Set IPv6 API Gateway.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "ZTNA proxy name.",
    "vip": "Virtual IP name.",
    "host": "Virtual or real host name.",
    "decrypted-traffic-mirror": "Decrypted traffic mirror.",
    "log-blocked-traffic": "Enable/disable logging of blocked traffic.",
    "auth-portal": "Enable/disable authentication portal.",
    "auth-virtual-host": "Virtual host for authentication portal.",
    "vip6": "Virtual IPv6 name.",
    "svr-pool-multiplex": "Enable/disable server pool multiplexing (default = disable). Share connected server in HTTP and HTTPS api-gateways.",
    "svr-pool-ttl": "Time-to-live in the server pool for idle connections to servers.",
    "svr-pool-server-max-request": "Maximum number of requests that servers in the server pool handle before disconnecting (default = unlimited).",
    "svr-pool-server-max-concurrent-request": "Maximum number of concurrent requests that servers in the server pool could handle (default = unlimited).",
    "api-gateway": "Set IPv4 API Gateway.",
    "api-gateway6": "Set IPv6 API Gateway.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "vip": {"type": "string", "max_length": 79},
    "host": {"type": "string", "max_length": 79},
    "decrypted-traffic-mirror": {"type": "string", "max_length": 35},
    "auth-virtual-host": {"type": "string", "max_length": 79},
    "vip6": {"type": "string", "max_length": 79},
    "svr-pool-ttl": {"type": "integer", "min": 0, "max": 2147483647},
    "svr-pool-server-max-request": {"type": "integer", "min": 0, "max": 2147483647},
    "svr-pool-server-max-concurrent-request": {"type": "integer", "min": 0, "max": 2147483647},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "api-gateway": {
        "id": {
            "type": "integer",
            "help": "API Gateway ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "url-map": {
            "type": "string",
            "help": "URL pattern to match.",
            "required": True,
            "default": "/",
            "max_length": 511,
        },
        "service": {
            "type": "option",
            "help": "Service.",
            "required": True,
            "default": "https",
            "options": ["http", "https"],
        },
        "ldb-method": {
            "type": "option",
            "help": "Method used to distribute sessions to real servers.",
            "default": "static",
            "options": ["static", "round-robin", "weighted", "first-alive", "http-host"],
        },
        "url-map-type": {
            "type": "option",
            "help": "Type of url-map.",
            "required": True,
            "default": "sub-string",
            "options": ["sub-string", "wildcard", "regex"],
        },
        "h2-support": {
            "type": "option",
            "help": "HTTP2 support, default=Enable.",
            "required": True,
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "h3-support": {
            "type": "option",
            "help": "HTTP3/QUIC support, default=Disable.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "quic": {
            "type": "string",
            "help": "QUIC setting.",
        },
        "realservers": {
            "type": "string",
            "help": "Select the real servers that this Access Proxy will distribute traffic to.",
        },
        "persistence": {
            "type": "option",
            "help": "Configure how to make sure that clients connect to the same server every time they make a request that is part of the same session.",
            "default": "none",
            "options": ["none", "http-cookie"],
        },
        "http-cookie-domain-from-host": {
            "type": "option",
            "help": "Enable/disable use of HTTP cookie domain from host field in HTTP.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "http-cookie-domain": {
            "type": "string",
            "help": "Domain that HTTP cookie persistence should apply to.",
            "default": "",
            "max_length": 35,
        },
        "http-cookie-path": {
            "type": "string",
            "help": "Limit HTTP cookie persistence to the specified path.",
            "default": "",
            "max_length": 35,
        },
        "http-cookie-generation": {
            "type": "integer",
            "help": "Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "http-cookie-age": {
            "type": "integer",
            "help": "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.",
            "default": 60,
            "min_value": 0,
            "max_value": 525600,
        },
        "http-cookie-share": {
            "type": "option",
            "help": "Control sharing of cookies across API Gateway. Use of same-ip means a cookie from one virtual server can be used by another. Disable stops cookie sharing.",
            "default": "same-ip",
            "options": ["disable", "same-ip"],
        },
        "https-cookie-secure": {
            "type": "option",
            "help": "Enable/disable verification that inserted HTTPS cookies are secure.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "ssl-dh-bits": {
            "type": "option",
            "help": "Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions.",
            "default": "2048",
            "options": ["768", "1024", "1536", "2048", "3072", "4096"],
        },
        "ssl-algorithm": {
            "type": "option",
            "help": "Permitted encryption algorithms for the server side of SSL full mode sessions according to encryption strength.",
            "default": "high",
            "options": ["high", "medium", "low"],
        },
        "ssl-cipher-suites": {
            "type": "string",
            "help": "SSL/TLS cipher suites to offer to a server, ordered by priority.",
        },
        "ssl-min-version": {
            "type": "option",
            "help": "Lowest SSL/TLS version acceptable from a server.",
            "default": "tls-1.1",
            "options": ["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-max-version": {
            "type": "option",
            "help": "Highest SSL/TLS version acceptable from a server.",
            "default": "tls-1.3",
            "options": ["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-renegotiation": {
            "type": "option",
            "help": "Enable/disable secure renegotiation to comply with RFC 5746.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "api-gateway6": {
        "id": {
            "type": "integer",
            "help": "API Gateway ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "url-map": {
            "type": "string",
            "help": "URL pattern to match.",
            "required": True,
            "default": "/",
            "max_length": 511,
        },
        "service": {
            "type": "option",
            "help": "Service.",
            "required": True,
            "default": "https",
            "options": ["http", "https"],
        },
        "ldb-method": {
            "type": "option",
            "help": "Method used to distribute sessions to real servers.",
            "default": "static",
            "options": ["static", "round-robin", "weighted", "first-alive", "http-host"],
        },
        "url-map-type": {
            "type": "option",
            "help": "Type of url-map.",
            "required": True,
            "default": "sub-string",
            "options": ["sub-string", "wildcard", "regex"],
        },
        "h2-support": {
            "type": "option",
            "help": "HTTP2 support, default=Enable.",
            "required": True,
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "h3-support": {
            "type": "option",
            "help": "HTTP3/QUIC support, default=Disable.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "quic": {
            "type": "string",
            "help": "QUIC setting.",
        },
        "realservers": {
            "type": "string",
            "help": "Select the real servers that this Access Proxy will distribute traffic to.",
        },
        "persistence": {
            "type": "option",
            "help": "Configure how to make sure that clients connect to the same server every time they make a request that is part of the same session.",
            "default": "none",
            "options": ["none", "http-cookie"],
        },
        "http-cookie-domain-from-host": {
            "type": "option",
            "help": "Enable/disable use of HTTP cookie domain from host field in HTTP.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "http-cookie-domain": {
            "type": "string",
            "help": "Domain that HTTP cookie persistence should apply to.",
            "default": "",
            "max_length": 35,
        },
        "http-cookie-path": {
            "type": "string",
            "help": "Limit HTTP cookie persistence to the specified path.",
            "default": "",
            "max_length": 35,
        },
        "http-cookie-generation": {
            "type": "integer",
            "help": "Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "http-cookie-age": {
            "type": "integer",
            "help": "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.",
            "default": 60,
            "min_value": 0,
            "max_value": 525600,
        },
        "http-cookie-share": {
            "type": "option",
            "help": "Control sharing of cookies across API Gateway. Use of same-ip means a cookie from one virtual server can be used by another. Disable stops cookie sharing.",
            "default": "same-ip",
            "options": ["disable", "same-ip"],
        },
        "https-cookie-secure": {
            "type": "option",
            "help": "Enable/disable verification that inserted HTTPS cookies are secure.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "ssl-dh-bits": {
            "type": "option",
            "help": "Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions.",
            "default": "2048",
            "options": ["768", "1024", "1536", "2048", "3072", "4096"],
        },
        "ssl-algorithm": {
            "type": "option",
            "help": "Permitted encryption algorithms for the server side of SSL full mode sessions according to encryption strength.",
            "default": "high",
            "options": ["high", "medium", "low"],
        },
        "ssl-cipher-suites": {
            "type": "string",
            "help": "SSL/TLS cipher suites to offer to a server, ordered by priority.",
        },
        "ssl-min-version": {
            "type": "option",
            "help": "Lowest SSL/TLS version acceptable from a server.",
            "default": "tls-1.1",
            "options": ["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-max-version": {
            "type": "option",
            "help": "Highest SSL/TLS version acceptable from a server.",
            "default": "tls-1.3",
            "options": ["tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
        "ssl-renegotiation": {
            "type": "option",
            "help": "Enable/disable secure renegotiation to comply with RFC 5746.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_LOG_BLOCKED_TRAFFIC = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_PORTAL = [
    "disable",
    "enable",
]
VALID_BODY_SVR_POOL_MULTIPLEX = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ztna_web_proxy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ztna/web_proxy."""
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


def validate_ztna_web_proxy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ztna/web_proxy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "log-blocked-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "log-blocked-traffic",
            payload["log-blocked-traffic"],
            VALID_BODY_LOG_BLOCKED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-portal" in payload:
        is_valid, error = _validate_enum_field(
            "auth-portal",
            payload["auth-portal"],
            VALID_BODY_AUTH_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "svr-pool-multiplex" in payload:
        is_valid, error = _validate_enum_field(
            "svr-pool-multiplex",
            payload["svr-pool-multiplex"],
            VALID_BODY_SVR_POOL_MULTIPLEX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ztna_web_proxy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ztna/web_proxy."""
    # Validate enum values using central function
    if "log-blocked-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "log-blocked-traffic",
            payload["log-blocked-traffic"],
            VALID_BODY_LOG_BLOCKED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-portal" in payload:
        is_valid, error = _validate_enum_field(
            "auth-portal",
            payload["auth-portal"],
            VALID_BODY_AUTH_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "svr-pool-multiplex" in payload:
        is_valid, error = _validate_enum_field(
            "svr-pool-multiplex",
            payload["svr-pool-multiplex"],
            VALID_BODY_SVR_POOL_MULTIPLEX,
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
    "endpoint": "ztna/web_proxy",
    "category": "cmdb",
    "api_path": "ztna/web-proxy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure ZTNA web-proxy.",
    "total_fields": 14,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
