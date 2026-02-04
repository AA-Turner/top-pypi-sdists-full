"""Validation helpers for system/alarm - Auto-generated"""

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
    "status": "disable",
    "audible": "disable",
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
    "status": "option",  # Enable/disable alarm.
    "audible": "option",  # Enable/disable audible alarm.
    "groups": "string",  # Alarm groups.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable alarm.",
    "audible": "Enable/disable audible alarm.",
    "groups": "Alarm groups.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "groups": {
        "id": {
            "type": "integer",
            "help": "Group ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "period": {
            "type": "integer",
            "help": "Time period in seconds (0 = from start up).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "admin-auth-failure-threshold": {
            "type": "integer",
            "help": "Admin authentication failure threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "admin-auth-lockout-threshold": {
            "type": "integer",
            "help": "Admin authentication lockout threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "user-auth-failure-threshold": {
            "type": "integer",
            "help": "User authentication failure threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "user-auth-lockout-threshold": {
            "type": "integer",
            "help": "User authentication lockout threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "replay-attempt-threshold": {
            "type": "integer",
            "help": "Replay attempt threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "self-test-failure-threshold": {
            "type": "integer",
            "help": "Self-test failure threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "log-full-warning-threshold": {
            "type": "integer",
            "help": "Log full warning threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "encryption-failure-threshold": {
            "type": "integer",
            "help": "Encryption failure threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "decryption-failure-threshold": {
            "type": "integer",
            "help": "Decryption failure threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
        "fw-policy-violations": {
            "type": "string",
            "help": "Firewall policy violations.",
        },
        "fw-policy-id": {
            "type": "integer",
            "help": "Firewall policy ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "fw-policy-id-threshold": {
            "type": "integer",
            "help": "Firewall policy ID threshold.",
            "default": 0,
            "min_value": 0,
            "max_value": 1024,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_AUDIBLE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_alarm_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/alarm."""
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


def validate_system_alarm_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/alarm object."""
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
    if "audible" in payload:
        is_valid, error = _validate_enum_field(
            "audible",
            payload["audible"],
            VALID_BODY_AUDIBLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_alarm_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/alarm."""
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
    if "audible" in payload:
        is_valid, error = _validate_enum_field(
            "audible",
            payload["audible"],
            VALID_BODY_AUDIBLE,
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
    "endpoint": "system/alarm",
    "category": "cmdb",
    "api_path": "system/alarm",
    "help": "Configure alarm.",
    "total_fields": 3,
    "required_fields_count": 0,
    "fields_with_defaults_count": 2,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
