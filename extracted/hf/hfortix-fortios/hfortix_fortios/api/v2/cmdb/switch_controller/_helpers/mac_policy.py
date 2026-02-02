"""Validation helpers for switch_controller/mac_policy - Auto-generated"""

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
    "fortilink",  # FortiLink interface for which this MAC policy belongs to.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "description": "",
    "fortilink": "",
    "vlan": "",
    "traffic-policy": "",
    "count": "disable",
    "bounce-port-link": "enable",
    "bounce-port-duration": 5,
    "poe-reset": "disable",
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
    "name": "string",  # MAC policy name.
    "description": "string",  # Description for the MAC policy.
    "fortilink": "string",  # FortiLink interface for which this MAC policy belongs to.
    "vlan": "string",  # Ingress traffic VLAN assignment for the MAC address matching
    "traffic-policy": "string",  # Traffic policy to be applied when using this MAC policy.
    "count": "option",  # Enable/disable packet count on the NAC device.
    "bounce-port-link": "option",  # Enable/disable bouncing (administratively bring the link dow
    "bounce-port-duration": "integer",  # Bounce duration in seconds of a switch port where this mac-p
    "poe-reset": "option",  # Enable/disable POE reset of a switch port where this mac-pol
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "MAC policy name.",
    "description": "Description for the MAC policy.",
    "fortilink": "FortiLink interface for which this MAC policy belongs to.",
    "vlan": "Ingress traffic VLAN assignment for the MAC address matching this MAC policy.",
    "traffic-policy": "Traffic policy to be applied when using this MAC policy.",
    "count": "Enable/disable packet count on the NAC device.",
    "bounce-port-link": "Enable/disable bouncing (administratively bring the link down, up) of a switch port where this mac-policy is applied.",
    "bounce-port-duration": "Bounce duration in seconds of a switch port where this mac-policy is applied.",
    "poe-reset": "Enable/disable POE reset of a switch port where this mac-policy is applied.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "description": {"type": "string", "max_length": 63},
    "fortilink": {"type": "string", "max_length": 15},
    "vlan": {"type": "string", "max_length": 15},
    "traffic-policy": {"type": "string", "max_length": 63},
    "bounce-port-duration": {"type": "integer", "min": 1, "max": 30},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_COUNT = [
    "disable",
    "enable",
]
VALID_BODY_BOUNCE_PORT_LINK = [
    "disable",
    "enable",
]
VALID_BODY_POE_RESET = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_mac_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/mac_policy."""
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


def validate_switch_controller_mac_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/mac_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "count" in payload:
        is_valid, error = _validate_enum_field(
            "count",
            payload["count"],
            VALID_BODY_COUNT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-port-link" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-port-link",
            payload["bounce-port-link"],
            VALID_BODY_BOUNCE_PORT_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-reset" in payload:
        is_valid, error = _validate_enum_field(
            "poe-reset",
            payload["poe-reset"],
            VALID_BODY_POE_RESET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_mac_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/mac_policy."""
    # Validate enum values using central function
    if "count" in payload:
        is_valid, error = _validate_enum_field(
            "count",
            payload["count"],
            VALID_BODY_COUNT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-port-link" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-port-link",
            payload["bounce-port-link"],
            VALID_BODY_BOUNCE_PORT_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-reset" in payload:
        is_valid, error = _validate_enum_field(
            "poe-reset",
            payload["poe-reset"],
            VALID_BODY_POE_RESET,
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
    "endpoint": "switch_controller/mac_policy",
    "category": "cmdb",
    "api_path": "switch-controller/mac-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure MAC policy to be applied on the managed FortiSwitch devices through NAC device.",
    "total_fields": 9,
    "required_fields_count": 1,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
