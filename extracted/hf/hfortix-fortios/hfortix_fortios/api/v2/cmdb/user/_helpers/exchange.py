"""Validation helpers for user/exchange - Auto-generated"""

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
    "server-name",  # MS Exchange server hostname.
    "domain-name",  # MS Exchange server fully qualified domain name.
    "username",  # User name used to sign in to the server. Must have proper permissions for service.
    "password",  # Password for the specified username.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "server-name": "",
    "domain-name": "",
    "username": "",
    "ip": "0.0.0.0",
    "connect-protocol": "rpc-over-https",
    "validate-server-certificate": "disable",
    "auth-type": "kerberos",
    "auth-level": "privacy",
    "http-auth-type": "ntlm",
    "ssl-min-proto-version": "default",
    "auto-discover-kdc": "enable",
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
    "name": "string",  # MS Exchange server entry name.
    "server-name": "string",  # MS Exchange server hostname.
    "domain-name": "string",  # MS Exchange server fully qualified domain name.
    "username": "string",  # User name used to sign in to the server. Must have proper pe
    "password": "password",  # Password for the specified username.
    "ip": "ipv4-address-any",  # Server IPv4 address.
    "connect-protocol": "option",  # Connection protocol used to connect to MS Exchange service.
    "validate-server-certificate": "option",  # Enable/disable exchange server certificate validation.
    "auth-type": "option",  # Authentication security type used for the RPC protocol layer
    "auth-level": "option",  # Authentication security level used for the RPC protocol laye
    "http-auth-type": "option",  # Authentication security type used for the HTTP transport.
    "ssl-min-proto-version": "option",  # Minimum SSL/TLS protocol version for HTTPS transport (defaul
    "auto-discover-kdc": "option",  # Enable/disable automatic discovery of KDC IP addresses.
    "kdc-ip": "string",  # KDC IPv4 addresses for Kerberos authentication.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "MS Exchange server entry name.",
    "server-name": "MS Exchange server hostname.",
    "domain-name": "MS Exchange server fully qualified domain name.",
    "username": "User name used to sign in to the server. Must have proper permissions for service.",
    "password": "Password for the specified username.",
    "ip": "Server IPv4 address.",
    "connect-protocol": "Connection protocol used to connect to MS Exchange service.",
    "validate-server-certificate": "Enable/disable exchange server certificate validation.",
    "auth-type": "Authentication security type used for the RPC protocol layer.",
    "auth-level": "Authentication security level used for the RPC protocol layer.",
    "http-auth-type": "Authentication security type used for the HTTP transport.",
    "ssl-min-proto-version": "Minimum SSL/TLS protocol version for HTTPS transport (default is to follow system global setting).",
    "auto-discover-kdc": "Enable/disable automatic discovery of KDC IP addresses.",
    "kdc-ip": "KDC IPv4 addresses for Kerberos authentication.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "server-name": {"type": "string", "max_length": 63},
    "domain-name": {"type": "string", "max_length": 79},
    "username": {"type": "string", "max_length": 64},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "kdc-ip": {
        "ipv4": {
            "type": "string",
            "help": "KDC IPv4 addresses for Kerberos authentication.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_CONNECT_PROTOCOL = [
    "rpc-over-tcp",
    "rpc-over-http",
    "rpc-over-https",
]
VALID_BODY_VALIDATE_SERVER_CERTIFICATE = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_TYPE = [
    "spnego",
    "ntlm",
    "kerberos",
]
VALID_BODY_AUTH_LEVEL = [
    "connect",
    "call",
    "packet",
    "integrity",
    "privacy",
]
VALID_BODY_HTTP_AUTH_TYPE = [
    "basic",
    "ntlm",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_AUTO_DISCOVER_KDC = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_exchange_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/exchange."""
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


def validate_user_exchange_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/exchange object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "connect-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "connect-protocol",
            payload["connect-protocol"],
            VALID_BODY_CONNECT_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "validate-server-certificate" in payload:
        is_valid, error = _validate_enum_field(
            "validate-server-certificate",
            payload["validate-server-certificate"],
            VALID_BODY_VALIDATE_SERVER_CERTIFICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-level" in payload:
        is_valid, error = _validate_enum_field(
            "auth-level",
            payload["auth-level"],
            VALID_BODY_AUTH_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "http-auth-type",
            payload["http-auth-type"],
            VALID_BODY_HTTP_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-discover-kdc" in payload:
        is_valid, error = _validate_enum_field(
            "auto-discover-kdc",
            payload["auto-discover-kdc"],
            VALID_BODY_AUTO_DISCOVER_KDC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_exchange_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/exchange."""
    # Validate enum values using central function
    if "connect-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "connect-protocol",
            payload["connect-protocol"],
            VALID_BODY_CONNECT_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "validate-server-certificate" in payload:
        is_valid, error = _validate_enum_field(
            "validate-server-certificate",
            payload["validate-server-certificate"],
            VALID_BODY_VALIDATE_SERVER_CERTIFICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-level" in payload:
        is_valid, error = _validate_enum_field(
            "auth-level",
            payload["auth-level"],
            VALID_BODY_AUTH_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "http-auth-type",
            payload["http-auth-type"],
            VALID_BODY_HTTP_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-discover-kdc" in payload:
        is_valid, error = _validate_enum_field(
            "auto-discover-kdc",
            payload["auto-discover-kdc"],
            VALID_BODY_AUTO_DISCOVER_KDC,
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
    "endpoint": "user/exchange",
    "category": "cmdb",
    "api_path": "user/exchange",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure MS Exchange server entries.",
    "total_fields": 14,
    "required_fields_count": 4,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
