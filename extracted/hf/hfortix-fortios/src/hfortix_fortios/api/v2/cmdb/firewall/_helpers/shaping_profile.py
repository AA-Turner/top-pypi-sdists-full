"""Validation helpers for firewall/shaping_profile - Auto-generated"""

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
    "profile-name",  # Shaping profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "profile-name": "",
    "type": "policing",
    "npu-offloading": "enable",
    "default-class-id": 0,
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
    "profile-name": "string",  # Shaping profile name.
    "comment": "var-string",  # Comment.
    "type": "option",  # Select shaping profile type: policing / queuing.
    "npu-offloading": "option",  # Enable/disable NPU offloading.
    "default-class-id": "integer",  # Default class ID to handle unclassified packets (including all local traffic).
    "shaping-entries": "string",  # Define shaping entries of this shaping profile.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "profile-name": "Shaping profile name.",
    "comment": "Comment.",
    "type": "Select shaping profile type: policing / queuing.",
    "npu-offloading": "Enable/disable NPU offloading.",
    "default-class-id": "Default class ID to handle unclassified packets (including all local traffic).",
    "shaping-entries": "Define shaping entries of this shaping profile.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "profile-name": {"type": "string", "max_length": 35},
    "default-class-id": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "shaping-entries": {
        "id": {
            "type": "integer",
            "help": "ID number.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "class-id": {
            "type": "integer",
            "help": "Class ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "priority": {
            "type": "option",
            "help": "Priority.",
            "default": "high",
            "options": ["top", "critical", "high", "medium", "low"],
        },
        "guaranteed-bandwidth-percentage": {
            "type": "integer",
            "help": "Guaranteed bandwidth in percentage.",
            "default": 0,
            "min_value": 0,
            "max_value": 100,
        },
        "maximum-bandwidth-percentage": {
            "type": "integer",
            "help": "Maximum bandwidth in percentage.",
            "default": 1,
            "min_value": 1,
            "max_value": 100,
        },
        "limit": {
            "type": "integer",
            "help": "Hard limit on the real queue size in packets.",
            "default": 100,
            "min_value": 5,
            "max_value": 10000,
        },
        "burst-in-msec": {
            "type": "integer",
            "help": "Number of bytes that can be burst at maximum-bandwidth speed. Formula: burst = maximum-bandwidth*burst-in-msec.",
            "default": 0,
            "min_value": 0,
            "max_value": 2000,
        },
        "cburst-in-msec": {
            "type": "integer",
            "help": "Number of bytes that can be burst as fast as the interface can transmit. Formula: cburst = maximum-bandwidth*cburst-in-msec.",
            "default": 0,
            "min_value": 0,
            "max_value": 2000,
        },
        "red-probability": {
            "type": "integer",
            "help": "Maximum probability (in percentage) for RED marking.",
            "default": 0,
            "min_value": 0,
            "max_value": 20,
        },
        "min": {
            "type": "integer",
            "help": "Average queue size in packets at which RED drop becomes a possibility.",
            "default": 83,
            "min_value": 3,
            "max_value": 3000,
        },
        "max": {
            "type": "integer",
            "help": "Average queue size in packets at which RED drop probability is maximal.",
            "default": 250,
            "min_value": 3,
            "max_value": 3000,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "policing",
    "queuing",
]
VALID_BODY_NPU_OFFLOADING = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_shaping_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/shaping_profile."""
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


def validate_firewall_shaping_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/shaping_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offloading" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offloading",
            payload["npu-offloading"],
            VALID_BODY_NPU_OFFLOADING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_shaping_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/shaping_profile."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offloading" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offloading",
            payload["npu-offloading"],
            VALID_BODY_NPU_OFFLOADING,
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
    "endpoint": "firewall/shaping_profile",
    "category": "cmdb",
    "api_path": "firewall/shaping-profile",
    "mkey": "profile-name",
    "mkey_type": "string",
    "help": "Configure shaping profiles.",
    "total_fields": 6,
    "required_fields_count": 1,
    "fields_with_defaults_count": 4,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
