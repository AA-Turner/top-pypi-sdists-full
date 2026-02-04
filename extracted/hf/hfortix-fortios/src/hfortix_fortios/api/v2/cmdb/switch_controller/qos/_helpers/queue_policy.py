"""Validation helpers for switch_controller/qos/queue_policy - Auto-generated"""

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
    "name",  # QoS policy name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "schedule": "round-robin",
    "rate-by": "kbps",
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
    "name": "string",  # QoS policy name.
    "schedule": "option",  # COS queue scheduling.
    "rate-by": "option",  # COS queue rate by kbps or percent.
    "cos-queue": "string",  # COS queue configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "QoS policy name.",
    "schedule": "COS queue scheduling.",
    "rate-by": "COS queue rate by kbps or percent.",
    "cos-queue": "COS queue configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "cos-queue": {
        "name": {
            "type": "string",
            "help": "Cos queue ID.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "description": {
            "type": "string",
            "help": "Description of the COS queue.",
            "default": "",
            "max_length": 63,
        },
        "min-rate": {
            "type": "integer",
            "help": "Minimum rate (0 - 4294967295 kbps, 0 to disable).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-rate": {
            "type": "integer",
            "help": "Maximum rate (0 - 4294967295 kbps, 0 to disable).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "min-rate-percent": {
            "type": "integer",
            "help": "Minimum rate (% of link speed).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-rate-percent": {
            "type": "integer",
            "help": "Maximum rate (% of link speed).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "drop-policy": {
            "type": "option",
            "help": "COS queue drop policy.",
            "default": "taildrop",
            "options": ["taildrop", "weighted-random-early-detection"],
        },
        "ecn": {
            "type": "option",
            "help": "Enable/disable ECN packet marking to drop eligible packets.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "weight": {
            "type": "integer",
            "help": "Weight of weighted round robin scheduling.",
            "default": 1,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SCHEDULE = [
    "strict",
    "round-robin",
    "weighted",
]
VALID_BODY_RATE_BY = [
    "kbps",
    "percent",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_qos_queue_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/qos/queue_policy."""
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


def validate_switch_controller_qos_queue_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/qos/queue_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "schedule" in payload:
        is_valid, error = _validate_enum_field(
            "schedule",
            payload["schedule"],
            VALID_BODY_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rate-by" in payload:
        is_valid, error = _validate_enum_field(
            "rate-by",
            payload["rate-by"],
            VALID_BODY_RATE_BY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_qos_queue_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/qos/queue_policy."""
    # Validate enum values using central function
    if "schedule" in payload:
        is_valid, error = _validate_enum_field(
            "schedule",
            payload["schedule"],
            VALID_BODY_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rate-by" in payload:
        is_valid, error = _validate_enum_field(
            "rate-by",
            payload["rate-by"],
            VALID_BODY_RATE_BY,
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
    "endpoint": "switch_controller/qos/queue_policy",
    "category": "cmdb",
    "api_path": "switch-controller.qos/queue-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure FortiSwitch QoS egress queue policy.",
    "total_fields": 4,
    "required_fields_count": 1,
    "fields_with_defaults_count": 3,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
