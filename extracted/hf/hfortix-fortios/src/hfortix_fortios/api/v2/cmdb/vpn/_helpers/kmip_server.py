"""Validation helpers for vpn/kmip_server - Auto-generated"""

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
    "server-list",  # KMIP server list.
    "username",  # User name to use for connectivity to the KMIP server.
    "password",  # Password to use for connectivity to the KMIP server.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "username": "",
    "ssl-min-proto-version": "default",
    "server-identity-check": "disable",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "source-ip": "",
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
    "name": "string",  # KMIP server entry name.
    "server-list": "string",  # KMIP server list.
    "username": "string",  # User name to use for connectivity to the KMIP server.
    "password": "password",  # Password to use for connectivity to the KMIP server.
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "server-identity-check": "option",  # Enable/disable KMIP server identity check (verify server FQDN/IP address against
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "source-ip": "string",  # FortiGate IP address to be used for communication with the KMIP server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "KMIP server entry name.",
    "server-list": "KMIP server list.",
    "username": "User name to use for connectivity to the KMIP server.",
    "password": "Password to use for connectivity to the KMIP server.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "server-identity-check": "Enable/disable KMIP server identity check (verify server FQDN/IP address against the server certificate).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "source-ip": "FortiGate IP address to be used for communication with the KMIP server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "username": {"type": "string", "max_length": 63},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "source-ip": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-list": {
        "id": {
            "type": "integer",
            "help": "ID",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable KMIP server.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "server": {
            "type": "string",
            "help": "KMIP server FQDN or IP address.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "port": {
            "type": "integer",
            "help": "KMIP server port.",
            "required": True,
            "default": 5696,
            "min_value": 0,
            "max_value": 65535,
        },
        "cert": {
            "type": "string",
            "help": "Client certificate to use for connectivity to the KMIP server.",
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_SERVER_IDENTITY_CHECK = [
    "enable",
    "disable",
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


def validate_vpn_kmip_server_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/kmip_server."""
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


def validate_vpn_kmip_server_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/kmip_server object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
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


def validate_vpn_kmip_server_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/kmip_server."""
    # Validate enum values using central function
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-identity-check" in payload:
        is_valid, error = _validate_enum_field(
            "server-identity-check",
            payload["server-identity-check"],
            VALID_BODY_SERVER_IDENTITY_CHECK,
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
    "endpoint": "vpn/kmip_server",
    "category": "cmdb",
    "api_path": "vpn/kmip-server",
    "mkey": "name",
    "mkey_type": "string",
    "help": "KMIP server entry configuration.",
    "total_fields": 10,
    "required_fields_count": 4,
    "fields_with_defaults_count": 8,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
