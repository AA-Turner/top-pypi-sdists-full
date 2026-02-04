"""Validation helpers for user/setting - Auto-generated"""

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
    "auth-type": "http https ftp telnet",
    "auth-cert": "",
    "auth-ca-cert": "",
    "auth-secure-http": "disable",
    "auth-http-basic": "disable",
    "auth-ssl-allow-renegotiation": "disable",
    "auth-src-mac": "enable",
    "auth-on-demand": "implicitly",
    "auth-timeout": 5,
    "auth-timeout-type": "idle-timeout",
    "auth-portal-timeout": 3,
    "radius-ses-timeout-act": "hard-timeout",
    "auth-blackout-time": 0,
    "auth-invalid-max": 5,
    "auth-lockout-threshold": 3,
    "auth-lockout-duration": 0,
    "per-policy-disclaimer": "disable",
    "auth-ssl-min-proto-version": "default",
    "auth-ssl-max-proto-version": "",
    "auth-ssl-sigalgs": "all",
    "default-user-password-policy": "",
    "cors": "disable",
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
    "auth-type": "option",  # Supported firewall policy authentication protocols/methods.
    "auth-cert": "string",  # HTTPS server certificate for policy authentication.
    "auth-ca-cert": "string",  # HTTPS CA certificate for policy authentication.
    "auth-secure-http": "option",  # Enable/disable redirecting HTTP user authentication to more secure HTTPS.
    "auth-http-basic": "option",  # Enable/disable use of HTTP basic authentication for identity-based firewall poli
    "auth-ssl-allow-renegotiation": "option",  # Allow/forbid SSL re-negotiation for HTTPS authentication.
    "auth-src-mac": "option",  # Enable/disable source MAC for user identity.
    "auth-on-demand": "option",  # Always/implicitly trigger firewall authentication on demand.
    "auth-timeout": "integer",  # Time in minutes before the firewall user authentication timeout requires the use
    "auth-timeout-type": "option",  # Control if authenticated users have to login again after a hard timeout, after a
    "auth-portal-timeout": "integer",  # Time in minutes before captive portal user have to re-authenticate (1 - 30 min, 
    "radius-ses-timeout-act": "option",  # Set the RADIUS session timeout to a hard timeout or to ignore RADIUS server sess
    "auth-blackout-time": "integer",  # Time in seconds an IP address is denied access after failing to authenticate fiv
    "auth-invalid-max": "integer",  # Maximum number of failed authentication attempts before the user is blocked.
    "auth-lockout-threshold": "integer",  # Maximum number of failed login attempts before login lockout is triggered.
    "auth-lockout-duration": "integer",  # Lockout period in seconds after too many login failures.
    "per-policy-disclaimer": "option",  # Enable/disable per policy disclaimer.
    "auth-ports": "string",  # Set up non-standard ports for authentication with HTTP, HTTPS, FTP, and TELNET.
    "auth-ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "auth-ssl-max-proto-version": "option",  # Maximum supported protocol version for SSL/TLS connections (default is no limit)
    "auth-ssl-sigalgs": "option",  # Set signature algorithms related to HTTPS authentication (affects TLS version <=
    "default-user-password-policy": "string",  # Default password policy to apply to all local users unless otherwise specified, 
    "cors": "option",  # Enable/disable allowed origins white list for CORS.
    "cors-allowed-origins": "string",  # Allowed origins white list for CORS.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "auth-type": "Supported firewall policy authentication protocols/methods.",
    "auth-cert": "HTTPS server certificate for policy authentication.",
    "auth-ca-cert": "HTTPS CA certificate for policy authentication.",
    "auth-secure-http": "Enable/disable redirecting HTTP user authentication to more secure HTTPS.",
    "auth-http-basic": "Enable/disable use of HTTP basic authentication for identity-based firewall policies.",
    "auth-ssl-allow-renegotiation": "Allow/forbid SSL re-negotiation for HTTPS authentication.",
    "auth-src-mac": "Enable/disable source MAC for user identity.",
    "auth-on-demand": "Always/implicitly trigger firewall authentication on demand.",
    "auth-timeout": "Time in minutes before the firewall user authentication timeout requires the user to re-authenticate.",
    "auth-timeout-type": "Control if authenticated users have to login again after a hard timeout, after an idle timeout, or after a session timeout.",
    "auth-portal-timeout": "Time in minutes before captive portal user have to re-authenticate (1 - 30 min, default 3 min).",
    "radius-ses-timeout-act": "Set the RADIUS session timeout to a hard timeout or to ignore RADIUS server session timeouts.",
    "auth-blackout-time": "Time in seconds an IP address is denied access after failing to authenticate five times within one minute.",
    "auth-invalid-max": "Maximum number of failed authentication attempts before the user is blocked.",
    "auth-lockout-threshold": "Maximum number of failed login attempts before login lockout is triggered.",
    "auth-lockout-duration": "Lockout period in seconds after too many login failures.",
    "per-policy-disclaimer": "Enable/disable per policy disclaimer.",
    "auth-ports": "Set up non-standard ports for authentication with HTTP, HTTPS, FTP, and TELNET.",
    "auth-ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "auth-ssl-max-proto-version": "Maximum supported protocol version for SSL/TLS connections (default is no limit).",
    "auth-ssl-sigalgs": "Set signature algorithms related to HTTPS authentication (affects TLS version <= 1.2 only, default is to enable all).",
    "default-user-password-policy": "Default password policy to apply to all local users unless otherwise specified, as defined in config user password-policy.",
    "cors": "Enable/disable allowed origins white list for CORS.",
    "cors-allowed-origins": "Allowed origins white list for CORS.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "auth-cert": {"type": "string", "max_length": 35},
    "auth-ca-cert": {"type": "string", "max_length": 35},
    "auth-timeout": {"type": "integer", "min": 1, "max": 1440},
    "auth-portal-timeout": {"type": "integer", "min": 1, "max": 30},
    "auth-blackout-time": {"type": "integer", "min": 0, "max": 3600},
    "auth-invalid-max": {"type": "integer", "min": 1, "max": 100},
    "auth-lockout-threshold": {"type": "integer", "min": 1, "max": 10},
    "auth-lockout-duration": {"type": "integer", "min": 0, "max": 4294967295},
    "default-user-password-policy": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "auth-ports": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "type": {
            "type": "option",
            "help": "Service type.",
            "default": "http",
            "options": ["http", "https", "ftp", "telnet"],
        },
        "port": {
            "type": "integer",
            "help": "Non-standard port for firewall user authentication.",
            "default": 1024,
            "min_value": 1,
            "max_value": 65535,
        },
    },
    "cors-allowed-origins": {
        "name": {
            "type": "string",
            "help": "Allowed origin for CORS.",
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_AUTH_TYPE = [
    "http",
    "https",
    "ftp",
    "telnet",
]
VALID_BODY_AUTH_SECURE_HTTP = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_HTTP_BASIC = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SSL_ALLOW_RENEGOTIATION = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SRC_MAC = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_ON_DEMAND = [
    "always",
    "implicitly",
]
VALID_BODY_AUTH_TIMEOUT_TYPE = [
    "idle-timeout",
    "hard-timeout",
    "new-session",
]
VALID_BODY_RADIUS_SES_TIMEOUT_ACT = [
    "hard-timeout",
    "ignore-timeout",
]
VALID_BODY_PER_POLICY_DISCLAIMER = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_AUTH_SSL_MAX_PROTO_VERSION = [
    "sslv3",
    "tlsv1",
    "tlsv1-1",
    "tlsv1-2",
    "tlsv1-3",
]
VALID_BODY_AUTH_SSL_SIGALGS = [
    "no-rsa-pss",
    "all",
]
VALID_BODY_CORS = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/setting."""
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


def validate_user_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-secure-http" in payload:
        is_valid, error = _validate_enum_field(
            "auth-secure-http",
            payload["auth-secure-http"],
            VALID_BODY_AUTH_SECURE_HTTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-http-basic" in payload:
        is_valid, error = _validate_enum_field(
            "auth-http-basic",
            payload["auth-http-basic"],
            VALID_BODY_AUTH_HTTP_BASIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-allow-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-allow-renegotiation",
            payload["auth-ssl-allow-renegotiation"],
            VALID_BODY_AUTH_SSL_ALLOW_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-src-mac" in payload:
        is_valid, error = _validate_enum_field(
            "auth-src-mac",
            payload["auth-src-mac"],
            VALID_BODY_AUTH_SRC_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "auth-on-demand",
            payload["auth-on-demand"],
            VALID_BODY_AUTH_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-timeout-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-timeout-type",
            payload["auth-timeout-type"],
            VALID_BODY_AUTH_TIMEOUT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-ses-timeout-act" in payload:
        is_valid, error = _validate_enum_field(
            "radius-ses-timeout-act",
            payload["radius-ses-timeout-act"],
            VALID_BODY_RADIUS_SES_TIMEOUT_ACT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-policy-disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "per-policy-disclaimer",
            payload["per-policy-disclaimer"],
            VALID_BODY_PER_POLICY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-min-proto-version",
            payload["auth-ssl-min-proto-version"],
            VALID_BODY_AUTH_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-max-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-max-proto-version",
            payload["auth-ssl-max-proto-version"],
            VALID_BODY_AUTH_SSL_MAX_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-sigalgs" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-sigalgs",
            payload["auth-ssl-sigalgs"],
            VALID_BODY_AUTH_SSL_SIGALGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cors" in payload:
        is_valid, error = _validate_enum_field(
            "cors",
            payload["cors"],
            VALID_BODY_CORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/setting."""
    # Validate enum values using central function
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-secure-http" in payload:
        is_valid, error = _validate_enum_field(
            "auth-secure-http",
            payload["auth-secure-http"],
            VALID_BODY_AUTH_SECURE_HTTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-http-basic" in payload:
        is_valid, error = _validate_enum_field(
            "auth-http-basic",
            payload["auth-http-basic"],
            VALID_BODY_AUTH_HTTP_BASIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-allow-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-allow-renegotiation",
            payload["auth-ssl-allow-renegotiation"],
            VALID_BODY_AUTH_SSL_ALLOW_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-src-mac" in payload:
        is_valid, error = _validate_enum_field(
            "auth-src-mac",
            payload["auth-src-mac"],
            VALID_BODY_AUTH_SRC_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "auth-on-demand",
            payload["auth-on-demand"],
            VALID_BODY_AUTH_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-timeout-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-timeout-type",
            payload["auth-timeout-type"],
            VALID_BODY_AUTH_TIMEOUT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-ses-timeout-act" in payload:
        is_valid, error = _validate_enum_field(
            "radius-ses-timeout-act",
            payload["radius-ses-timeout-act"],
            VALID_BODY_RADIUS_SES_TIMEOUT_ACT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-policy-disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "per-policy-disclaimer",
            payload["per-policy-disclaimer"],
            VALID_BODY_PER_POLICY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-min-proto-version",
            payload["auth-ssl-min-proto-version"],
            VALID_BODY_AUTH_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-max-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-max-proto-version",
            payload["auth-ssl-max-proto-version"],
            VALID_BODY_AUTH_SSL_MAX_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-ssl-sigalgs" in payload:
        is_valid, error = _validate_enum_field(
            "auth-ssl-sigalgs",
            payload["auth-ssl-sigalgs"],
            VALID_BODY_AUTH_SSL_SIGALGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cors" in payload:
        is_valid, error = _validate_enum_field(
            "cors",
            payload["cors"],
            VALID_BODY_CORS,
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
    "endpoint": "user/setting",
    "category": "cmdb",
    "api_path": "user/setting",
    "help": "Configure user authentication setting.",
    "total_fields": 24,
    "required_fields_count": 0,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
