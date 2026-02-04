"""Validation helpers for switch_controller/qos/dot1p_map - Auto-generated"""

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
    "name",  # Dot1p map name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "description": "",
    "egress-pri-tagging": "disable",
    "priority-0": "queue-0",
    "priority-1": "queue-0",
    "priority-2": "queue-0",
    "priority-3": "queue-0",
    "priority-4": "queue-0",
    "priority-5": "queue-0",
    "priority-6": "queue-0",
    "priority-7": "queue-0",
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
    "name": "string",  # Dot1p map name.
    "description": "string",  # Description of the 802.1p name.
    "egress-pri-tagging": "option",  # Enable/disable egress priority-tag frame.
    "priority-0": "option",  # COS queue mapped to dot1p priority number.
    "priority-1": "option",  # COS queue mapped to dot1p priority number.
    "priority-2": "option",  # COS queue mapped to dot1p priority number.
    "priority-3": "option",  # COS queue mapped to dot1p priority number.
    "priority-4": "option",  # COS queue mapped to dot1p priority number.
    "priority-5": "option",  # COS queue mapped to dot1p priority number.
    "priority-6": "option",  # COS queue mapped to dot1p priority number.
    "priority-7": "option",  # COS queue mapped to dot1p priority number.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Dot1p map name.",
    "description": "Description of the 802.1p name.",
    "egress-pri-tagging": "Enable/disable egress priority-tag frame.",
    "priority-0": "COS queue mapped to dot1p priority number.",
    "priority-1": "COS queue mapped to dot1p priority number.",
    "priority-2": "COS queue mapped to dot1p priority number.",
    "priority-3": "COS queue mapped to dot1p priority number.",
    "priority-4": "COS queue mapped to dot1p priority number.",
    "priority-5": "COS queue mapped to dot1p priority number.",
    "priority-6": "COS queue mapped to dot1p priority number.",
    "priority-7": "COS queue mapped to dot1p priority number.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "description": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_EGRESS_PRI_TAGGING = [
    "disable",
    "enable",
]
VALID_BODY_PRIORITY_0 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_1 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_2 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_3 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_4 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_5 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_6 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_BODY_PRIORITY_7 = [
    "queue-0",
    "queue-1",
    "queue-2",
    "queue-3",
    "queue-4",
    "queue-5",
    "queue-6",
    "queue-7",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_qos_dot1p_map_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/qos/dot1p_map."""
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


def validate_switch_controller_qos_dot1p_map_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/qos/dot1p_map object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "egress-pri-tagging" in payload:
        is_valid, error = _validate_enum_field(
            "egress-pri-tagging",
            payload["egress-pri-tagging"],
            VALID_BODY_EGRESS_PRI_TAGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-0" in payload:
        is_valid, error = _validate_enum_field(
            "priority-0",
            payload["priority-0"],
            VALID_BODY_PRIORITY_0,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-1" in payload:
        is_valid, error = _validate_enum_field(
            "priority-1",
            payload["priority-1"],
            VALID_BODY_PRIORITY_1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-2" in payload:
        is_valid, error = _validate_enum_field(
            "priority-2",
            payload["priority-2"],
            VALID_BODY_PRIORITY_2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-3" in payload:
        is_valid, error = _validate_enum_field(
            "priority-3",
            payload["priority-3"],
            VALID_BODY_PRIORITY_3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-4" in payload:
        is_valid, error = _validate_enum_field(
            "priority-4",
            payload["priority-4"],
            VALID_BODY_PRIORITY_4,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-5" in payload:
        is_valid, error = _validate_enum_field(
            "priority-5",
            payload["priority-5"],
            VALID_BODY_PRIORITY_5,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-6" in payload:
        is_valid, error = _validate_enum_field(
            "priority-6",
            payload["priority-6"],
            VALID_BODY_PRIORITY_6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-7" in payload:
        is_valid, error = _validate_enum_field(
            "priority-7",
            payload["priority-7"],
            VALID_BODY_PRIORITY_7,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_qos_dot1p_map_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/qos/dot1p_map."""
    # Validate enum values using central function
    if "egress-pri-tagging" in payload:
        is_valid, error = _validate_enum_field(
            "egress-pri-tagging",
            payload["egress-pri-tagging"],
            VALID_BODY_EGRESS_PRI_TAGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-0" in payload:
        is_valid, error = _validate_enum_field(
            "priority-0",
            payload["priority-0"],
            VALID_BODY_PRIORITY_0,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-1" in payload:
        is_valid, error = _validate_enum_field(
            "priority-1",
            payload["priority-1"],
            VALID_BODY_PRIORITY_1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-2" in payload:
        is_valid, error = _validate_enum_field(
            "priority-2",
            payload["priority-2"],
            VALID_BODY_PRIORITY_2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-3" in payload:
        is_valid, error = _validate_enum_field(
            "priority-3",
            payload["priority-3"],
            VALID_BODY_PRIORITY_3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-4" in payload:
        is_valid, error = _validate_enum_field(
            "priority-4",
            payload["priority-4"],
            VALID_BODY_PRIORITY_4,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-5" in payload:
        is_valid, error = _validate_enum_field(
            "priority-5",
            payload["priority-5"],
            VALID_BODY_PRIORITY_5,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-6" in payload:
        is_valid, error = _validate_enum_field(
            "priority-6",
            payload["priority-6"],
            VALID_BODY_PRIORITY_6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-7" in payload:
        is_valid, error = _validate_enum_field(
            "priority-7",
            payload["priority-7"],
            VALID_BODY_PRIORITY_7,
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
    "endpoint": "switch_controller/qos/dot1p_map",
    "category": "cmdb",
    "api_path": "switch-controller.qos/dot1p-map",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure FortiSwitch QoS 802.1p.",
    "total_fields": 11,
    "required_fields_count": 1,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
