"""Validation helpers for system/ptp - Auto-generated"""

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
    "interface",  # PTP client will reply through this interface.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "mode": "multicast",
    "delay-mechanism": "E2E",
    "request-interval": 1,
    "interface": "",
    "server-mode": "disable",
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
    "status": "option",  # Enable/disable setting the FortiGate system time by synchronizing with an PTP Se
    "mode": "option",  # Multicast transmission or hybrid transmission.
    "delay-mechanism": "option",  # End to end delay detection or peer to peer delay detection.
    "request-interval": "integer",  # The delay request value is the logarithmic mean interval in seconds between the 
    "interface": "string",  # PTP client will reply through this interface.
    "server-mode": "option",  # Enable/disable FortiGate PTP server mode. Your FortiGate becomes an PTP server f
    "server-interface": "string",  # FortiGate interface(s) with PTP server mode enabled. Devices on your network can
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable setting the FortiGate system time by synchronizing with an PTP Server.",
    "mode": "Multicast transmission or hybrid transmission.",
    "delay-mechanism": "End to end delay detection or peer to peer delay detection.",
    "request-interval": "The delay request value is the logarithmic mean interval in seconds between the delay request messages sent by the slave to the master.",
    "interface": "PTP client will reply through this interface.",
    "server-mode": "Enable/disable FortiGate PTP server mode. Your FortiGate becomes an PTP server for other devices on your network.",
    "server-interface": "FortiGate interface(s) with PTP server mode enabled. Devices on your network can contact these interfaces for PTP services.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "request-interval": {"type": "integer", "min": 1, "max": 6},
    "interface": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-interface": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "server-interface-name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "delay-mechanism": {
            "type": "option",
            "help": "End to end delay detection or peer to peer delay detection.",
            "default": "E2E",
            "options": ["E2E", "P2P"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MODE = [
    "multicast",
    "hybrid",
]
VALID_BODY_DELAY_MECHANISM = [
    "E2E",
    "P2P",
]
VALID_BODY_SERVER_MODE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ptp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ptp."""
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


def validate_system_ptp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ptp object."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delay-mechanism" in payload:
        is_valid, error = _validate_enum_field(
            "delay-mechanism",
            payload["delay-mechanism"],
            VALID_BODY_DELAY_MECHANISM,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ptp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ptp."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delay-mechanism" in payload:
        is_valid, error = _validate_enum_field(
            "delay-mechanism",
            payload["delay-mechanism"],
            VALID_BODY_DELAY_MECHANISM,
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
    "endpoint": "system/ptp",
    "category": "cmdb",
    "api_path": "system/ptp",
    "help": "Configure system PTP information.",
    "total_fields": 7,
    "required_fields_count": 1,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
