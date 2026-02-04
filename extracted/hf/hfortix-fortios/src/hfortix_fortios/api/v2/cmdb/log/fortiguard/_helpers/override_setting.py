"""Validation helpers for log/fortiguard/override_setting - Auto-generated"""

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
    "override": "disable",
    "status": "disable",
    "upload-option": "5-minute",
    "upload-interval": "daily",
    "upload-day": "",
    "upload-time": "",
    "priority": "default",
    "max-log-rate": 0,
    "access-config": "enable",
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
    "override": "option",  # Overriding FortiCloud settings for this VDOM or use global settings.
    "status": "option",  # Enable/disable logging to FortiCloud.
    "upload-option": "option",  # Configure how log messages are sent to FortiCloud.
    "upload-interval": "option",  # Frequency of uploading log files to FortiCloud.
    "upload-day": "user",  # Day of week to roll logs.
    "upload-time": "user",  # Time of day to roll logs (hh:mm).
    "priority": "option",  # Set log transmission priority.
    "max-log-rate": "integer",  # FortiCloud maximum log rate in MBps (0 = unlimited).
    "access-config": "option",  # Enable/disable FortiCloud access to configuration and data.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "override": "Overriding FortiCloud settings for this VDOM or use global settings.",
    "status": "Enable/disable logging to FortiCloud.",
    "upload-option": "Configure how log messages are sent to FortiCloud.",
    "upload-interval": "Frequency of uploading log files to FortiCloud.",
    "upload-day": "Day of week to roll logs.",
    "upload-time": "Time of day to roll logs (hh:mm).",
    "priority": "Set log transmission priority.",
    "max-log-rate": "FortiCloud maximum log rate in MBps (0 = unlimited).",
    "access-config": "Enable/disable FortiCloud access to configuration and data.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "max-log-rate": {"type": "integer", "min": 0, "max": 100000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_UPLOAD_OPTION = [
    "store-and-upload",
    "realtime",
    "1-minute",
    "5-minute",
]
VALID_BODY_UPLOAD_INTERVAL = [
    "daily",
    "weekly",
    "monthly",
]
VALID_BODY_PRIORITY = [
    "default",
    "low",
]
VALID_BODY_ACCESS_CONFIG = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_log_fortiguard_override_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/fortiguard/override_setting."""
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


def validate_log_fortiguard_override_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/fortiguard/override_setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "override" in payload:
        is_valid, error = _validate_enum_field(
            "override",
            payload["override"],
            VALID_BODY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-option" in payload:
        is_valid, error = _validate_enum_field(
            "upload-option",
            payload["upload-option"],
            VALID_BODY_UPLOAD_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-interval" in payload:
        is_valid, error = _validate_enum_field(
            "upload-interval",
            payload["upload-interval"],
            VALID_BODY_UPLOAD_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-config" in payload:
        is_valid, error = _validate_enum_field(
            "access-config",
            payload["access-config"],
            VALID_BODY_ACCESS_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_log_fortiguard_override_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/fortiguard/override_setting."""
    # Validate enum values using central function
    if "override" in payload:
        is_valid, error = _validate_enum_field(
            "override",
            payload["override"],
            VALID_BODY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-option" in payload:
        is_valid, error = _validate_enum_field(
            "upload-option",
            payload["upload-option"],
            VALID_BODY_UPLOAD_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-interval" in payload:
        is_valid, error = _validate_enum_field(
            "upload-interval",
            payload["upload-interval"],
            VALID_BODY_UPLOAD_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-config" in payload:
        is_valid, error = _validate_enum_field(
            "access-config",
            payload["access-config"],
            VALID_BODY_ACCESS_CONFIG,
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
    "endpoint": "log/fortiguard/override_setting",
    "category": "cmdb",
    "api_path": "log.fortiguard/override-setting",
    "help": "Override global FortiCloud logging settings for this VDOM.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
