"""Validation helpers for switch_controller/vlan_policy - Auto-generated"""

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
    "fortilink",  # FortiLink interface for which this VLAN policy belongs to.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "description": "",
    "fortilink": "",
    "vlan": "",
    "allowed-vlans-all": "disable",
    "discard-mode": "none",
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
    "name": "string",  # VLAN policy name.
    "description": "string",  # Description for the VLAN policy.
    "fortilink": "string",  # FortiLink interface for which this VLAN policy belongs to.
    "vlan": "string",  # Native VLAN to be applied when using this VLAN policy.
    "allowed-vlans": "string",  # Allowed VLANs to be applied when using this VLAN policy.
    "untagged-vlans": "string",  # Untagged VLANs to be applied when using this VLAN policy.
    "allowed-vlans-all": "option",  # Enable/disable all defined VLANs when using this VLAN policy.
    "discard-mode": "option",  # Discard mode to be applied when using this VLAN policy.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "VLAN policy name.",
    "description": "Description for the VLAN policy.",
    "fortilink": "FortiLink interface for which this VLAN policy belongs to.",
    "vlan": "Native VLAN to be applied when using this VLAN policy.",
    "allowed-vlans": "Allowed VLANs to be applied when using this VLAN policy.",
    "untagged-vlans": "Untagged VLANs to be applied when using this VLAN policy.",
    "allowed-vlans-all": "Enable/disable all defined VLANs when using this VLAN policy.",
    "discard-mode": "Discard mode to be applied when using this VLAN policy.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "description": {"type": "string", "max_length": 63},
    "fortilink": {"type": "string", "max_length": 15},
    "vlan": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "allowed-vlans": {
        "vlan-name": {
            "type": "string",
            "help": "VLAN name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "untagged-vlans": {
        "vlan-name": {
            "type": "string",
            "help": "VLAN name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ALLOWED_VLANS_ALL = [
    "enable",
    "disable",
]
VALID_BODY_DISCARD_MODE = [
    "none",
    "all-untagged",
    "all-tagged",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_vlan_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/vlan_policy."""
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


def validate_switch_controller_vlan_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/vlan_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "allowed-vlans-all" in payload:
        is_valid, error = _validate_enum_field(
            "allowed-vlans-all",
            payload["allowed-vlans-all"],
            VALID_BODY_ALLOWED_VLANS_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "discard-mode" in payload:
        is_valid, error = _validate_enum_field(
            "discard-mode",
            payload["discard-mode"],
            VALID_BODY_DISCARD_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_vlan_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/vlan_policy."""
    # Validate enum values using central function
    if "allowed-vlans-all" in payload:
        is_valid, error = _validate_enum_field(
            "allowed-vlans-all",
            payload["allowed-vlans-all"],
            VALID_BODY_ALLOWED_VLANS_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "discard-mode" in payload:
        is_valid, error = _validate_enum_field(
            "discard-mode",
            payload["discard-mode"],
            VALID_BODY_DISCARD_MODE,
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
    "endpoint": "switch_controller/vlan_policy",
    "category": "cmdb",
    "api_path": "switch-controller/vlan-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VLAN policy to be applied on the managed FortiSwitch ports through dynamic-port-policy.",
    "total_fields": 8,
    "required_fields_count": 1,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
