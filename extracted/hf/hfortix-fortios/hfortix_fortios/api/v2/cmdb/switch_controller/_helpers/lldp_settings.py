"""Validation helpers for switch_controller/lldp_settings - Auto-generated"""

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
    "tx-hold": 4,
    "tx-interval": 30,
    "fast-start-interval": 2,
    "management-interface": "internal",
    "device-detection": "enable",
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
    "tx-hold": "integer",  # Number of tx-intervals before local LLDP data expires (1 - 1
    "tx-interval": "integer",  # Frequency of LLDP PDU transmission from FortiSwitch (5 - 409
    "fast-start-interval": "integer",  # Frequency of LLDP PDU transmission from FortiSwitch for the 
    "management-interface": "option",  # Primary management interface to be advertised in LLDP and CD
    "device-detection": "option",  # Enable/disable dynamic detection of LLDP neighbor devices fo
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "tx-hold": "Number of tx-intervals before local LLDP data expires (1 - 16, default = 4). Packet TTL is tx-hold * tx-interval.",
    "tx-interval": "Frequency of LLDP PDU transmission from FortiSwitch (5 - 4095 sec, default = 30). Packet TTL is tx-hold * tx-interval.",
    "fast-start-interval": "Frequency of LLDP PDU transmission from FortiSwitch for the first 4 packets when the link is up (2 - 5 sec, default = 2, 0 = disable fast start).",
    "management-interface": "Primary management interface to be advertised in LLDP and CDP PDUs.",
    "device-detection": "Enable/disable dynamic detection of LLDP neighbor devices for VLAN assignment.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "tx-hold": {"type": "integer", "min": 1, "max": 16},
    "tx-interval": {"type": "integer", "min": 5, "max": 4095},
    "fast-start-interval": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_MANAGEMENT_INTERFACE = [
    "internal",
    "mgmt",
]
VALID_BODY_DEVICE_DETECTION = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_lldp_settings_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/lldp_settings."""
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


def validate_switch_controller_lldp_settings_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/lldp_settings object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "management-interface" in payload:
        is_valid, error = _validate_enum_field(
            "management-interface",
            payload["management-interface"],
            VALID_BODY_MANAGEMENT_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-detection" in payload:
        is_valid, error = _validate_enum_field(
            "device-detection",
            payload["device-detection"],
            VALID_BODY_DEVICE_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_lldp_settings_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/lldp_settings."""
    # Validate enum values using central function
    if "management-interface" in payload:
        is_valid, error = _validate_enum_field(
            "management-interface",
            payload["management-interface"],
            VALID_BODY_MANAGEMENT_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-detection" in payload:
        is_valid, error = _validate_enum_field(
            "device-detection",
            payload["device-detection"],
            VALID_BODY_DEVICE_DETECTION,
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
    "endpoint": "switch_controller/lldp_settings",
    "category": "cmdb",
    "api_path": "switch-controller/lldp-settings",
    "help": "Configure FortiSwitch LLDP settings.",
    "total_fields": 5,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
