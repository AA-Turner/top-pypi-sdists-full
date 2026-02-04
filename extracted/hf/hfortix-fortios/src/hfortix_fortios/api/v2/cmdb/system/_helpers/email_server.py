"""Validation helpers for system/email_server - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "type": "custom",
    "server": "",
    "port": 25,
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "authenticate": "disable",
    "validate-server": "disable",
    "username": "",
    "security": "none",
    "ssl-min-proto-version": "default",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "type": "option",  # Use FortiGuard Message service or custom email server.
    "server": "string",  # SMTP server IP address or hostname.
    "port": "integer",  # SMTP server port.
    "source-ip": "ipv4-address",  # SMTP server IPv4 source IP.
    "source-ip6": "ipv6-address",  # SMTP server IPv6 source IP.
    "authenticate": "option",  # Enable/disable authentication.
    "validate-server": "option",  # Enable/disable validation of server certificate.
    "username": "string",  # SMTP server user name for authentication.
    "password": "password",  # SMTP server user password for authentication.
    "security": "option",  # Connection security used by the email server.
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "type": "Use FortiGuard Message service or custom email server.",
    "server": "SMTP server IP address or hostname.",
    "port": "SMTP server port.",
    "source-ip": "SMTP server IPv4 source IP.",
    "source-ip6": "SMTP server IPv6 source IP.",
    "authenticate": "Enable/disable authentication.",
    "validate-server": "Enable/disable validation of server certificate.",
    "username": "SMTP server user name for authentication.",
    "password": "SMTP server user password for authentication.",
    "security": "Connection security used by the email server.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "server": {"type": "string", "max_length": 63},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "username": {"type": "string", "max_length": 255},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "custom",
]
VALID_BODY_AUTHENTICATE = [
    "enable",
    "disable",
]
VALID_BODY_VALIDATE_SERVER = [
    "enable",
    "disable",
]
VALID_BODY_SECURITY = [
    "none",
    "starttls",
    "smtps",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_email_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/email_server."""
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


def validate_system_email_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/email_server object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authenticate" in payload:
        is_valid, error = _validate_enum_field(
            "authenticate",
            payload["authenticate"],
            VALID_BODY_AUTHENTICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "validate-server" in payload:
        is_valid, error = _validate_enum_field(
            "validate-server",
            payload["validate-server"],
            VALID_BODY_VALIDATE_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
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
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_email_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/email_server."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authenticate" in payload:
        is_valid, error = _validate_enum_field(
            "authenticate",
            payload["authenticate"],
            VALID_BODY_AUTHENTICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "validate-server" in payload:
        is_valid, error = _validate_enum_field(
            "validate-server",
            payload["validate-server"],
            VALID_BODY_VALIDATE_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
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
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
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
    "endpoint": "system/email_server",
    "category": "cmdb",
    "api_path": "system/email-server",
    "help": "Configure the email server used by the FortiGate various things. For example, for sending email messages to users to support user authentication features.",
    "total_fields": 14,
    "required_fields_count": 1,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
