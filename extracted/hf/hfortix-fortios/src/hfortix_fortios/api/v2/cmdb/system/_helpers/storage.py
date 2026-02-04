"""Validation helpers for system/storage - Auto-generated"""

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
    "name": "default_n",
    "status": "enable",
    "media-status": "disable",
    "order": 0,
    "partition": "\u003cunknown\u003e",
    "device": "?",
    "size": 0,
    "usage": "log",
    "wanopt-mode": "mix",
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
    "name": "string",  # Storage name.
    "status": "option",  # Enable/disable storage.
    "media-status": "option",  # The physical status of current media.
    "order": "integer",  # Set storage order.
    "partition": "string",  # Label of underlying partition.
    "device": "string",  # Partition device.
    "size": "integer",  # Partition size.
    "usage": "option",  # Use hard disk for logging or WAN Optimization (default = log).
    "wanopt-mode": "option",  # WAN Optimization mode (default = mix).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Storage name.",
    "status": "Enable/disable storage.",
    "media-status": "The physical status of current media.",
    "order": "Set storage order.",
    "partition": "Label of underlying partition.",
    "device": "Partition device.",
    "size": "Partition size.",
    "usage": "Use hard disk for logging or WAN Optimization (default = log).",
    "wanopt-mode": "WAN Optimization mode (default = mix).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "order": {"type": "integer", "min": 0, "max": 255},
    "partition": {"type": "string", "max_length": 16},
    "device": {"type": "string", "max_length": 19},
    "size": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MEDIA_STATUS = [
    "enable",
    "disable",
    "fail",
]
VALID_BODY_USAGE = [
    "log",
    "wanopt",
]
VALID_BODY_WANOPT_MODE = [
    "mix",
    "wanopt",
    "webcache",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_storage_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/storage."""
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


def validate_system_storage_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/storage object."""
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
    if "media-status" in payload:
        is_valid, error = _validate_enum_field(
            "media-status",
            payload["media-status"],
            VALID_BODY_MEDIA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "usage" in payload:
        is_valid, error = _validate_enum_field(
            "usage",
            payload["usage"],
            VALID_BODY_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-mode",
            payload["wanopt-mode"],
            VALID_BODY_WANOPT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_storage_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/storage."""
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
    if "media-status" in payload:
        is_valid, error = _validate_enum_field(
            "media-status",
            payload["media-status"],
            VALID_BODY_MEDIA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "usage" in payload:
        is_valid, error = _validate_enum_field(
            "usage",
            payload["usage"],
            VALID_BODY_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-mode",
            payload["wanopt-mode"],
            VALID_BODY_WANOPT_MODE,
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
    "endpoint": "system/storage",
    "category": "cmdb",
    "api_path": "system/storage",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure logical storage.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
