"""Validation helpers for switch_controller/dynamic_port_policy - Auto-generated"""

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
    "fortilink",  # FortiLink interface for which this Dynamic port policy belongs to.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "description": "",
    "fortilink": "",
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
    "name": "string",  # Dynamic port policy name.
    "description": "string",  # Description for the Dynamic port policy.
    "fortilink": "string",  # FortiLink interface for which this Dynamic port policy belongs to.
    "policy": "string",  # Port policies with matching criteria and actions.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Dynamic port policy name.",
    "description": "Description for the Dynamic port policy.",
    "fortilink": "FortiLink interface for which this Dynamic port policy belongs to.",
    "policy": "Port policies with matching criteria and actions.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "description": {"type": "string", "max_length": 63},
    "fortilink": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "policy": {
        "name": {
            "type": "string",
            "help": "Policy name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "description": {
            "type": "string",
            "help": "Description for the policy.",
            "default": "",
            "max_length": 63,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable policy.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "category": {
            "type": "option",
            "help": "Category of Dynamic port policy.",
            "default": "device",
            "options": ["device", "interface-tag"],
        },
        "match-type": {
            "type": "option",
            "help": "Match and retain the devices based on the type.",
            "default": "dynamic",
            "options": ["dynamic", "override"],
        },
        "match-period": {
            "type": "integer",
            "help": "Number of days the matched devices will be retained (0 - 120, 0 = always retain).",
            "default": 0,
            "min_value": 0,
            "max_value": 120,
        },
        "match-remove": {
            "type": "option",
            "help": "Options to remove the matched override devices.",
            "default": "default",
            "options": ["default", "link-down"],
        },
        "interface-tags": {
            "type": "string",
            "help": "Match policy based on the FortiSwitch interface object tags.",
        },
        "mac": {
            "type": "string",
            "help": "Match policy based on MAC address.",
            "default": "",
            "max_length": 17,
        },
        "hw-vendor": {
            "type": "string",
            "help": "Match policy based on hardware vendor.",
            "default": "",
            "max_length": 15,
        },
        "type": {
            "type": "string",
            "help": "Match policy based on type.",
            "default": "",
            "max_length": 15,
        },
        "family": {
            "type": "string",
            "help": "Match policy based on family.",
            "default": "",
            "max_length": 31,
        },
        "host": {
            "type": "string",
            "help": "Match policy based on host.",
            "default": "",
            "max_length": 64,
        },
        "lldp-profile": {
            "type": "string",
            "help": "LLDP profile to be applied when using this policy.",
            "default": "",
            "max_length": 63,
        },
        "qos-policy": {
            "type": "string",
            "help": "QoS policy to be applied when using this policy.",
            "default": "",
            "max_length": 63,
        },
        "802-1x": {
            "type": "string",
            "help": "802.1x security policy to be applied when using this policy.",
            "default": "",
            "max_length": 31,
        },
        "vlan-policy": {
            "type": "string",
            "help": "VLAN policy to be applied when using this policy.",
            "default": "",
            "max_length": 63,
        },
        "bounce-port-link": {
            "type": "option",
            "help": "Enable/disable bouncing (administratively bring the link down, up) of a switch port where this policy is applied. Helps to clear and reassign VLAN from lldp-profile.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "bounce-port-duration": {
            "type": "integer",
            "help": "Bounce duration in seconds of a switch port where this policy is applied.",
            "default": 5,
            "min_value": 1,
            "max_value": 30,
        },
        "poe-reset": {
            "type": "option",
            "help": "Enable/disable POE reset of a switch port where this policy is applied.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_dynamic_port_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/dynamic_port_policy."""
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


def validate_switch_controller_dynamic_port_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/dynamic_port_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_dynamic_port_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/dynamic_port_policy."""
    # Validate enum values using central function

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
    "endpoint": "switch_controller/dynamic_port_policy",
    "category": "cmdb",
    "api_path": "switch-controller/dynamic-port-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Dynamic port policy to be applied on the managed FortiSwitch ports through DPP device.",
    "total_fields": 4,
    "required_fields_count": 1,
    "fields_with_defaults_count": 3,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
