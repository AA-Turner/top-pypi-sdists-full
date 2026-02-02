"""Validation helpers for switch_controller/fortilink_settings - Auto-generated"""

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
    "name": "",
    "fortilink": "",
    "inactive-timer": 15,
    "link-down-flush": "enable",
    "access-vlan-mode": "legacy",
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
    "name": "string",  # FortiLink settings name.
    "fortilink": "string",  # FortiLink interface to which this fortilink-setting belongs.
    "inactive-timer": "integer",  # Time interval(minutes) to be included in the inactive device
    "link-down-flush": "option",  # Clear NAC and dynamic devices on switch ports on link down e
    "access-vlan-mode": "option",  # Intra VLAN traffic behavior with loss of connection to the F
    "nac-ports": "string",  # NAC specific configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "FortiLink settings name.",
    "fortilink": "FortiLink interface to which this fortilink-setting belongs.",
    "inactive-timer": "Time interval(minutes) to be included in the inactive devices expiry calculation (mac age-out + inactive-time + periodic scan interval).",
    "link-down-flush": "Clear NAC and dynamic devices on switch ports on link down event.",
    "access-vlan-mode": "Intra VLAN traffic behavior with loss of connection to the FortiGate.",
    "nac-ports": "NAC specific configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "fortilink": {"type": "string", "max_length": 15},
    "inactive-timer": {"type": "integer", "min": 1, "max": 1440},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "nac-ports": {
        "onboarding-vlan": {
            "type": "string",
            "help": "Default NAC Onboarding VLAN when NAC devices are discovered.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "lan-segment": {
            "type": "option",
            "help": "Enable/disable LAN segment feature on the FortiLink interface.",
            "default": "disabled",
            "options": ["enabled", "disabled"],
        },
        "nac-lan-interface": {
            "type": "string",
            "help": "Configure NAC LAN interface.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "nac-segment-vlans": {
            "type": "string",
            "help": "Configure NAC segment VLANs.",
            "required": True,
        },
        "parent-key": {
            "type": "string",
            "help": "Parent key name.",
            "default": "",
            "max_length": 35,
        },
        "member-change": {
            "type": "integer",
            "help": "Member change flag.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_LINK_DOWN_FLUSH = [
    "disable",
    "enable",
]
VALID_BODY_ACCESS_VLAN_MODE = [
    "legacy",
    "fail-open",
    "fail-close",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_fortilink_settings_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/fortilink_settings."""
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


def validate_switch_controller_fortilink_settings_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/fortilink_settings object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "link-down-flush" in payload:
        is_valid, error = _validate_enum_field(
            "link-down-flush",
            payload["link-down-flush"],
            VALID_BODY_LINK_DOWN_FLUSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-vlan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "access-vlan-mode",
            payload["access-vlan-mode"],
            VALID_BODY_ACCESS_VLAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_fortilink_settings_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/fortilink_settings."""
    # Validate enum values using central function
    if "link-down-flush" in payload:
        is_valid, error = _validate_enum_field(
            "link-down-flush",
            payload["link-down-flush"],
            VALID_BODY_LINK_DOWN_FLUSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-vlan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "access-vlan-mode",
            payload["access-vlan-mode"],
            VALID_BODY_ACCESS_VLAN_MODE,
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
    "endpoint": "switch_controller/fortilink_settings",
    "category": "cmdb",
    "api_path": "switch-controller/fortilink-settings",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure integrated FortiLink settings for FortiSwitch.",
    "total_fields": 6,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
