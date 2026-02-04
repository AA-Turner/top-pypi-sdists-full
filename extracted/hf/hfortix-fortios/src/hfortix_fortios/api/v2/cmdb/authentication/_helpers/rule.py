"""Validation helpers for authentication/rule - Auto-generated"""

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
    "status": "enable",
    "protocol": "http",
    "ip-based": "enable",
    "active-auth-method": "",
    "sso-auth-method": "",
    "web-auth-cookie": "disable",
    "cors-stateful": "disable",
    "cors-depth": 3,
    "cert-auth-cookie": "enable",
    "transaction-based": "disable",
    "web-portal": "enable",
    "session-logout": "disable",
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
    "name": "string",  # Authentication rule name.
    "status": "option",  # Enable/disable this authentication rule.
    "protocol": "option",  # Authentication is required for the selected protocol (default = HTTP).
    "srcintf": "string",  # Incoming (ingress) interface.
    "srcaddr": "string",  # Authentication is required for the selected IPv4 source address.
    "dstaddr": "string",  # Select an IPv4 destination address from available options. Required for web prox
    "srcaddr6": "string",  # Authentication is required for the selected IPv6 source address.
    "dstaddr6": "string",  # Select an IPv6 destination address from available options. Required for web prox
    "ip-based": "option",  # Enable/disable IP-based authentication. When enabled, previously authenticated u
    "active-auth-method": "string",  # Select an active authentication method.
    "sso-auth-method": "string",  # Select a single-sign on (SSO) authentication method.
    "web-auth-cookie": "option",  # Enable/disable Web authentication cookies (default = disable).
    "cors-stateful": "option",  # Enable/disable allowance of CORS access (default = disable).
    "cors-depth": "integer",  # Depth to allow CORS access (default = 3).
    "cert-auth-cookie": "option",  # Enable/disable to use device certificate as authentication cookie (default = ena
    "transaction-based": "option",  # Enable/disable transaction based authentication (default = disable).
    "web-portal": "option",  # Enable/disable web portal for proxy transparent policy (default = enable).
    "comments": "var-string",  # Comment.
    "session-logout": "option",  # Enable/disable logout of a user from the current session.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Authentication rule name.",
    "status": "Enable/disable this authentication rule.",
    "protocol": "Authentication is required for the selected protocol (default = HTTP).",
    "srcintf": "Incoming (ingress) interface.",
    "srcaddr": "Authentication is required for the selected IPv4 source address.",
    "dstaddr": "Select an IPv4 destination address from available options. Required for web proxy authentication.",
    "srcaddr6": "Authentication is required for the selected IPv6 source address.",
    "dstaddr6": "Select an IPv6 destination address from available options. Required for web proxy authentication.",
    "ip-based": "Enable/disable IP-based authentication. When enabled, previously authenticated users from the same IP address will be exempted.",
    "active-auth-method": "Select an active authentication method.",
    "sso-auth-method": "Select a single-sign on (SSO) authentication method.",
    "web-auth-cookie": "Enable/disable Web authentication cookies (default = disable).",
    "cors-stateful": "Enable/disable allowance of CORS access (default = disable).",
    "cors-depth": "Depth to allow CORS access (default = 3).",
    "cert-auth-cookie": "Enable/disable to use device certificate as authentication cookie (default = enable).",
    "transaction-based": "Enable/disable transaction based authentication (default = disable).",
    "web-portal": "Enable/disable web portal for proxy transparent policy (default = enable).",
    "comments": "Comment.",
    "session-logout": "Enable/disable logout of a user from the current session.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "active-auth-method": {"type": "string", "max_length": 35},
    "sso-auth-method": {"type": "string", "max_length": 35},
    "cors-depth": {"type": "integer", "min": 1, "max": 8},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr6": {
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
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_PROTOCOL = [
    "http",
    "ftp",
    "socks",
    "ssh",
    "ztna-portal",
]
VALID_BODY_IP_BASED = [
    "enable",
    "disable",
]
VALID_BODY_WEB_AUTH_COOKIE = [
    "enable",
    "disable",
]
VALID_BODY_CORS_STATEFUL = [
    "enable",
    "disable",
]
VALID_BODY_CERT_AUTH_COOKIE = [
    "enable",
    "disable",
]
VALID_BODY_TRANSACTION_BASED = [
    "enable",
    "disable",
]
VALID_BODY_WEB_PORTAL = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_LOGOUT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_authentication_rule_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for authentication/rule."""
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


def validate_authentication_rule_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new authentication/rule object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-based" in payload:
        is_valid, error = _validate_enum_field(
            "ip-based",
            payload["ip-based"],
            VALID_BODY_IP_BASED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "web-auth-cookie",
            payload["web-auth-cookie"],
            VALID_BODY_WEB_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cors-stateful" in payload:
        is_valid, error = _validate_enum_field(
            "cors-stateful",
            payload["cors-stateful"],
            VALID_BODY_CORS_STATEFUL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "cert-auth-cookie",
            payload["cert-auth-cookie"],
            VALID_BODY_CERT_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transaction-based" in payload:
        is_valid, error = _validate_enum_field(
            "transaction-based",
            payload["transaction-based"],
            VALID_BODY_TRANSACTION_BASED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-portal" in payload:
        is_valid, error = _validate_enum_field(
            "web-portal",
            payload["web-portal"],
            VALID_BODY_WEB_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-logout" in payload:
        is_valid, error = _validate_enum_field(
            "session-logout",
            payload["session-logout"],
            VALID_BODY_SESSION_LOGOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_authentication_rule_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update authentication/rule."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-based" in payload:
        is_valid, error = _validate_enum_field(
            "ip-based",
            payload["ip-based"],
            VALID_BODY_IP_BASED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "web-auth-cookie",
            payload["web-auth-cookie"],
            VALID_BODY_WEB_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cors-stateful" in payload:
        is_valid, error = _validate_enum_field(
            "cors-stateful",
            payload["cors-stateful"],
            VALID_BODY_CORS_STATEFUL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "cert-auth-cookie",
            payload["cert-auth-cookie"],
            VALID_BODY_CERT_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transaction-based" in payload:
        is_valid, error = _validate_enum_field(
            "transaction-based",
            payload["transaction-based"],
            VALID_BODY_TRANSACTION_BASED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-portal" in payload:
        is_valid, error = _validate_enum_field(
            "web-portal",
            payload["web-portal"],
            VALID_BODY_WEB_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-logout" in payload:
        is_valid, error = _validate_enum_field(
            "session-logout",
            payload["session-logout"],
            VALID_BODY_SESSION_LOGOUT,
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
    "endpoint": "authentication/rule",
    "category": "cmdb",
    "api_path": "authentication/rule",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Authentication Rules.",
    "total_fields": 19,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
