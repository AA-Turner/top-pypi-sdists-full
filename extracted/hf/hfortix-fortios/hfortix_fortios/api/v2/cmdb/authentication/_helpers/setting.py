"""Validation helpers for authentication/setting - Auto-generated"""

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
    "active-auth-scheme": "",
    "sso-auth-scheme": "",
    "update-time": "",
    "persistent-cookie": "enable",
    "ip-auth-cookie": "disable",
    "cookie-max-age": 480,
    "cookie-refresh-div": 2,
    "captive-portal-type": "fqdn",
    "captive-portal-ip": "0.0.0.0",
    "captive-portal-ip6": "::",
    "captive-portal": "",
    "captive-portal6": "",
    "cert-auth": "disable",
    "cert-captive-portal": "",
    "cert-captive-portal-ip": "0.0.0.0",
    "cert-captive-portal-port": 7832,
    "captive-portal-port": 7830,
    "auth-https": "enable",
    "captive-portal-ssl-port": 7831,
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
    "active-auth-scheme": "string",  # Active authentication method (scheme name).
    "sso-auth-scheme": "string",  # Single-Sign-On authentication method (scheme name).
    "update-time": "user",  # Time of the last update.
    "persistent-cookie": "option",  # Enable/disable persistent cookie on web portal authenticatio
    "ip-auth-cookie": "option",  # Enable/disable persistent cookie on IP based web portal auth
    "cookie-max-age": "integer",  # Persistent web portal cookie maximum age in minutes (30 - 10
    "cookie-refresh-div": "integer",  # Refresh rate divider of persistent web portal cookie (defaul
    "captive-portal-type": "option",  # Captive portal type.
    "captive-portal-ip": "ipv4-address-any",  # Captive portal IP address.
    "captive-portal-ip6": "ipv6-address",  # Captive portal IPv6 address.
    "captive-portal": "string",  # Captive portal host name.
    "captive-portal6": "string",  # IPv6 captive portal host name.
    "cert-auth": "option",  # Enable/disable redirecting certificate authentication to HTT
    "cert-captive-portal": "string",  # Certificate captive portal host name.
    "cert-captive-portal-ip": "ipv4-address-any",  # Certificate captive portal IP address.
    "cert-captive-portal-port": "integer",  # Certificate captive portal port number (1 - 65535, default =
    "captive-portal-port": "integer",  # Captive portal port number (1 - 65535, default = 7830).
    "auth-https": "option",  # Enable/disable redirecting HTTP user authentication to HTTPS
    "captive-portal-ssl-port": "integer",  # Captive portal SSL port number (1 - 65535, default = 7831).
    "user-cert-ca": "string",  # CA certificate used for client certificate verification.
    "dev-range": "string",  # Address range for the IP based device query.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "active-auth-scheme": "Active authentication method (scheme name).",
    "sso-auth-scheme": "Single-Sign-On authentication method (scheme name).",
    "update-time": "Time of the last update.",
    "persistent-cookie": "Enable/disable persistent cookie on web portal authentication (default = enable).",
    "ip-auth-cookie": "Enable/disable persistent cookie on IP based web portal authentication (default = disable).",
    "cookie-max-age": "Persistent web portal cookie maximum age in minutes (30 - 10080 (1 week), default = 480 (8 hours)).",
    "cookie-refresh-div": "Refresh rate divider of persistent web portal cookie (default = 2). Refresh value = cookie-max-age/cookie-refresh-div.",
    "captive-portal-type": "Captive portal type.",
    "captive-portal-ip": "Captive portal IP address.",
    "captive-portal-ip6": "Captive portal IPv6 address.",
    "captive-portal": "Captive portal host name.",
    "captive-portal6": "IPv6 captive portal host name.",
    "cert-auth": "Enable/disable redirecting certificate authentication to HTTPS portal.",
    "cert-captive-portal": "Certificate captive portal host name.",
    "cert-captive-portal-ip": "Certificate captive portal IP address.",
    "cert-captive-portal-port": "Certificate captive portal port number (1 - 65535, default = 7832).",
    "captive-portal-port": "Captive portal port number (1 - 65535, default = 7830).",
    "auth-https": "Enable/disable redirecting HTTP user authentication to HTTPS.",
    "captive-portal-ssl-port": "Captive portal SSL port number (1 - 65535, default = 7831).",
    "user-cert-ca": "CA certificate used for client certificate verification.",
    "dev-range": "Address range for the IP based device query.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "active-auth-scheme": {"type": "string", "max_length": 35},
    "sso-auth-scheme": {"type": "string", "max_length": 35},
    "cookie-max-age": {"type": "integer", "min": 30, "max": 10080},
    "cookie-refresh-div": {"type": "integer", "min": 2, "max": 4},
    "captive-portal": {"type": "string", "max_length": 255},
    "captive-portal6": {"type": "string", "max_length": 255},
    "cert-captive-portal": {"type": "string", "max_length": 255},
    "cert-captive-portal-port": {"type": "integer", "min": 1, "max": 65535},
    "captive-portal-port": {"type": "integer", "min": 1, "max": 65535},
    "captive-portal-ssl-port": {"type": "integer", "min": 1, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "user-cert-ca": {
        "name": {
            "type": "string",
            "help": "CA certificate list.",
            "default": "",
            "max_length": 79,
        },
    },
    "dev-range": {
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
VALID_BODY_PERSISTENT_COOKIE = [
    "enable",
    "disable",
]
VALID_BODY_IP_AUTH_COOKIE = [
    "enable",
    "disable",
]
VALID_BODY_CAPTIVE_PORTAL_TYPE = [
    "fqdn",
    "ip",
]
VALID_BODY_CERT_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_HTTPS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_authentication_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for authentication/setting."""
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


def validate_authentication_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new authentication/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "persistent-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "persistent-cookie",
            payload["persistent-cookie"],
            VALID_BODY_PERSISTENT_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "ip-auth-cookie",
            payload["ip-auth-cookie"],
            VALID_BODY_IP_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-type" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-type",
            payload["captive-portal-type"],
            VALID_BODY_CAPTIVE_PORTAL_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "cert-auth",
            payload["cert-auth"],
            VALID_BODY_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "auth-https",
            payload["auth-https"],
            VALID_BODY_AUTH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_authentication_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update authentication/setting."""
    # Validate enum values using central function
    if "persistent-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "persistent-cookie",
            payload["persistent-cookie"],
            VALID_BODY_PERSISTENT_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-auth-cookie" in payload:
        is_valid, error = _validate_enum_field(
            "ip-auth-cookie",
            payload["ip-auth-cookie"],
            VALID_BODY_IP_AUTH_COOKIE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-type" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-type",
            payload["captive-portal-type"],
            VALID_BODY_CAPTIVE_PORTAL_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "cert-auth",
            payload["cert-auth"],
            VALID_BODY_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "auth-https",
            payload["auth-https"],
            VALID_BODY_AUTH_HTTPS,
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
    "endpoint": "authentication/setting",
    "category": "cmdb",
    "api_path": "authentication/setting",
    "help": "Configure authentication setting.",
    "total_fields": 21,
    "required_fields_count": 0,
    "fields_with_defaults_count": 19,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
