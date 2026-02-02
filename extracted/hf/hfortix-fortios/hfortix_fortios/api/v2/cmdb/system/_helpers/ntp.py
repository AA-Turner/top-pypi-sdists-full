"""Validation helpers for system/ntp - Auto-generated"""

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
    "key",  # Key for authentication.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ntpsync": "disable",
    "type": "fortiguard",
    "syncinterval": 60,
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "server-mode": "disable",
    "authentication": "disable",
    "key-type": "MD5",
    "key-id": 0,
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
    "ntpsync": "option",  # Enable/disable setting the FortiGate system time by synchron
    "type": "option",  # Use the FortiGuard NTP server or any other available NTP Ser
    "syncinterval": "integer",  # NTP synchronization interval (1 - 1440 min).
    "ntpserver": "string",  # Configure the FortiGate to connect to any available third-pa
    "source-ip": "ipv4-address",  # Source IP address for communication to the NTP server.
    "source-ip6": "ipv6-address",  # Source IPv6 address for communication to the NTP server.
    "server-mode": "option",  # Enable/disable FortiGate NTP Server Mode. Your FortiGate bec
    "authentication": "option",  # Enable/disable authentication.
    "key-type": "option",  # Key type for authentication (MD5, SHA1, SHA256).
    "key": "password",  # Key for authentication.
    "key-id": "integer",  # Key ID for authentication.
    "interface": "string",  # FortiGate interface(s) with NTP server mode enabled. Devices
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ntpsync": "Enable/disable setting the FortiGate system time by synchronizing with an NTP Server.",
    "type": "Use the FortiGuard NTP server or any other available NTP Server.",
    "syncinterval": "NTP synchronization interval (1 - 1440 min).",
    "ntpserver": "Configure the FortiGate to connect to any available third-party NTP server.",
    "source-ip": "Source IP address for communication to the NTP server.",
    "source-ip6": "Source IPv6 address for communication to the NTP server.",
    "server-mode": "Enable/disable FortiGate NTP Server Mode. Your FortiGate becomes an NTP server for other devices on your network. The FortiGate relays NTP requests to its configured NTP server.",
    "authentication": "Enable/disable authentication.",
    "key-type": "Key type for authentication (MD5, SHA1, SHA256).",
    "key": "Key for authentication.",
    "key-id": "Key ID for authentication.",
    "interface": "FortiGate interface(s) with NTP server mode enabled. Devices on your network can contact these interfaces for NTP services.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "syncinterval": {"type": "integer", "min": 1, "max": 1440},
    "key-id": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ntpserver": {
        "id": {
            "type": "integer",
            "help": "NTP server ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "server": {
            "type": "string",
            "help": "IP address or hostname of the NTP Server.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "ntpv3": {
            "type": "option",
            "help": "Enable to use NTPv3 instead of NTPv4.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "authentication": {
            "type": "option",
            "help": "Enable/disable authentication.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "key-type": {
            "type": "option",
            "help": "Select NTP authentication type.",
            "default": "MD5",
            "options": ["MD5", "SHA1", "SHA256"],
        },
        "key": {
            "type": "password",
            "help": "Key for MD5(NTPv3)/SHA1(NTPv4)/SHA256(NTPv4) authentication.",
            "required": True,
            "max_length": 64,
        },
        "key-id": {
            "type": "integer",
            "help": "Key ID for authentication.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip-type": {
            "type": "option",
            "help": "Choose to connect to IPv4 or/and IPv6 NTP server.",
            "default": "Both",
            "options": ["IPv6", "IPv4", "Both"],
        },
        "interface-select-method": {
            "type": "option",
            "help": "Specify how to select outgoing interface to reach server.",
            "default": "auto",
            "options": ["auto", "sdwan", "specify"],
        },
        "interface": {
            "type": "string",
            "help": "Specify outgoing interface to reach server.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "vrf-select": {
            "type": "integer",
            "help": "VRF ID used for connection to server.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
    },
    "interface": {
        "interface-name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_NTPSYNC = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "fortiguard",
    "custom",
]
VALID_BODY_SERVER_MODE = [
    "enable",
    "disable",
]
VALID_BODY_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_KEY_TYPE = [
    "MD5",
    "SHA1",
    "SHA256",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ntp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ntp."""
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


def validate_system_ntp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ntp object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ntpsync" in payload:
        is_valid, error = _validate_enum_field(
            "ntpsync",
            payload["ntpsync"],
            VALID_BODY_NTPSYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-mode",
            payload["server-mode"],
            VALID_BODY_SERVER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "key-type" in payload:
        is_valid, error = _validate_enum_field(
            "key-type",
            payload["key-type"],
            VALID_BODY_KEY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ntp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ntp."""
    # Validate enum values using central function
    if "ntpsync" in payload:
        is_valid, error = _validate_enum_field(
            "ntpsync",
            payload["ntpsync"],
            VALID_BODY_NTPSYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-mode" in payload:
        is_valid, error = _validate_enum_field(
            "server-mode",
            payload["server-mode"],
            VALID_BODY_SERVER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "key-type" in payload:
        is_valid, error = _validate_enum_field(
            "key-type",
            payload["key-type"],
            VALID_BODY_KEY_TYPE,
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
    "endpoint": "system/ntp",
    "category": "cmdb",
    "api_path": "system/ntp",
    "help": "Configure system NTP information.",
    "total_fields": 12,
    "required_fields_count": 1,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
