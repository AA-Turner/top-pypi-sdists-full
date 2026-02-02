"""Validation helpers for videofilter/profile - Auto-generated"""

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
    "name",  # Name.
    "filters",  # YouTube filter entries.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "youtube": "enable",
    "vimeo": "enable",
    "dailymotion": "enable",
    "replacemsg-group": "",
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
    "name": "string",  # Name.
    "comment": "var-string",  # Comment.
    "filters": "string",  # YouTube filter entries.
    "youtube": "option",  # Enable/disable YouTube video source.
    "vimeo": "option",  # Enable/disable Vimeo video source.
    "dailymotion": "option",  # Enable/disable Dailymotion video source.
    "replacemsg-group": "string",  # Replacement message group.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "comment": "Comment.",
    "filters": "YouTube filter entries.",
    "youtube": "Enable/disable YouTube video source.",
    "vimeo": "Enable/disable Vimeo video source.",
    "dailymotion": "Enable/disable Dailymotion video source.",
    "replacemsg-group": "Replacement message group.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "filters": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "comment": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
        "type": {
            "type": "option",
            "help": "Filter type.",
            "required": True,
            "default": "category",
            "options": ["category", "channel", "title", "description"],
        },
        "keyword": {
            "type": "integer",
            "help": "Video filter keyword ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "category": {
            "type": "string",
            "help": "FortiGuard category ID.",
            "required": True,
            "default": "",
            "max_length": 7,
        },
        "channel": {
            "type": "string",
            "help": "Channel ID.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
        "action": {
            "type": "option",
            "help": "Video filter action.",
            "default": "monitor",
            "options": ["allow", "monitor", "block"],
        },
        "log": {
            "type": "option",
            "help": "Enable/disable logging.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_YOUTUBE = [
    "enable",
    "disable",
]
VALID_BODY_VIMEO = [
    "enable",
    "disable",
]
VALID_BODY_DAILYMOTION = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_videofilter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for videofilter/profile."""
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


def validate_videofilter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new videofilter/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "youtube" in payload:
        is_valid, error = _validate_enum_field(
            "youtube",
            payload["youtube"],
            VALID_BODY_YOUTUBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vimeo" in payload:
        is_valid, error = _validate_enum_field(
            "vimeo",
            payload["vimeo"],
            VALID_BODY_VIMEO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dailymotion" in payload:
        is_valid, error = _validate_enum_field(
            "dailymotion",
            payload["dailymotion"],
            VALID_BODY_DAILYMOTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_videofilter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update videofilter/profile."""
    # Validate enum values using central function
    if "youtube" in payload:
        is_valid, error = _validate_enum_field(
            "youtube",
            payload["youtube"],
            VALID_BODY_YOUTUBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vimeo" in payload:
        is_valid, error = _validate_enum_field(
            "vimeo",
            payload["vimeo"],
            VALID_BODY_VIMEO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dailymotion" in payload:
        is_valid, error = _validate_enum_field(
            "dailymotion",
            payload["dailymotion"],
            VALID_BODY_DAILYMOTION,
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
    "endpoint": "videofilter/profile",
    "category": "cmdb",
    "api_path": "videofilter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VideoFilter profile.",
    "total_fields": 7,
    "required_fields_count": 2,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
