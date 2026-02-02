"""Validation helpers for system/lldp/network_policy - Auto-generated"""

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
    "name",  # LLDP network policy name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
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
    "name": "string",  # LLDP network policy name.
    "comment": "var-string",  # Comment.
    "voice": "string",  # Voice.
    "voice-signaling": "string",  # Voice signaling.
    "guest": "string",  # Guest.
    "guest-voice-signaling": "string",  # Guest Voice Signaling.
    "softphone": "string",  # Softphone.
    "video-conferencing": "string",  # Video Conferencing.
    "streaming-video": "string",  # Streaming Video.
    "video-signaling": "string",  # Video Signaling.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "LLDP network policy name.",
    "comment": "Comment.",
    "voice": "Voice.",
    "voice-signaling": "Voice signaling.",
    "guest": "Guest.",
    "guest-voice-signaling": "Guest Voice Signaling.",
    "softphone": "Softphone.",
    "video-conferencing": "Video Conferencing.",
    "streaming-video": "Streaming Video.",
    "video-signaling": "Video Signaling.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "voice": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "voice-signaling": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "guest": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "guest-voice-signaling": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "softphone": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "video-conferencing": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "streaming-video": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "video-signaling": {
        "status": {
            "type": "option",
            "help": "Enable/disable advertising this policy.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "tag": {
            "type": "option",
            "help": "Advertise tagged or untagged traffic.",
            "default": "none",
            "options": ["none", "dot1q", "dot1p"],
        },
        "vlan": {
            "type": "integer",
            "help": "802.1Q VLAN ID to advertise (1 - 4094).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 4094,
        },
        "priority": {
            "type": "integer",
            "help": "802.1P CoS/PCP to advertise (0 - 7; from lowest to highest priority).",
            "default": 5,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Differentiated Services Code Point (DSCP) value to advertise.",
            "default": 46,
            "min_value": 0,
            "max_value": 63,
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_lldp_network_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/lldp/network_policy."""
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


def validate_system_lldp_network_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/lldp/network_policy object."""
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


def validate_system_lldp_network_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/lldp/network_policy."""
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
    "endpoint": "system/lldp/network_policy",
    "category": "cmdb",
    "api_path": "system.lldp/network-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure LLDP network policy.",
    "total_fields": 10,
    "required_fields_count": 1,
    "fields_with_defaults_count": 1,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
