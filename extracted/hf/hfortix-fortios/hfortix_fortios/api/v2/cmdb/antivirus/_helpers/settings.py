"""Validation helpers for antivirus/settings - Auto-generated"""

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
    "machine-learning-detection": "enable",
    "use-extreme-db": "disable",
    "grayware": "disable",
    "override-timeout": 0,
    "cache-infected-result": "enable",
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
    "machine-learning-detection": "option",  # Use machine learning based malware detection.
    "use-extreme-db": "option",  # Enable/disable the use of Extreme AVDB.
    "grayware": "option",  # Enable/disable grayware detection when an AntiVirus profile 
    "override-timeout": "integer",  # Override the large file scan timeout value in seconds (30 - 
    "cache-infected-result": "option",  # Enable/disable cache of infected scan results (default = ena
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "machine-learning-detection": "Use machine learning based malware detection.",
    "use-extreme-db": "Enable/disable the use of Extreme AVDB.",
    "grayware": "Enable/disable grayware detection when an AntiVirus profile is applied to traffic.",
    "override-timeout": "Override the large file scan timeout value in seconds (30 - 3600). Zero is the default value and is used to disable this command. When disabled, the daemon adjusts the large file scan timeout based on the file size.",
    "cache-infected-result": "Enable/disable cache of infected scan results (default = enable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "override-timeout": {"type": "integer", "min": 30, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_MACHINE_LEARNING_DETECTION = [
    "enable",
    "monitor",
    "disable",
]
VALID_BODY_USE_EXTREME_DB = [
    "enable",
    "disable",
]
VALID_BODY_GRAYWARE = [
    "enable",
    "disable",
]
VALID_BODY_CACHE_INFECTED_RESULT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_antivirus_settings_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for antivirus/settings."""
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


def validate_antivirus_settings_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new antivirus/settings object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "machine-learning-detection" in payload:
        is_valid, error = _validate_enum_field(
            "machine-learning-detection",
            payload["machine-learning-detection"],
            VALID_BODY_MACHINE_LEARNING_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-extreme-db" in payload:
        is_valid, error = _validate_enum_field(
            "use-extreme-db",
            payload["use-extreme-db"],
            VALID_BODY_USE_EXTREME_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "grayware" in payload:
        is_valid, error = _validate_enum_field(
            "grayware",
            payload["grayware"],
            VALID_BODY_GRAYWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-infected-result" in payload:
        is_valid, error = _validate_enum_field(
            "cache-infected-result",
            payload["cache-infected-result"],
            VALID_BODY_CACHE_INFECTED_RESULT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_antivirus_settings_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update antivirus/settings."""
    # Validate enum values using central function
    if "machine-learning-detection" in payload:
        is_valid, error = _validate_enum_field(
            "machine-learning-detection",
            payload["machine-learning-detection"],
            VALID_BODY_MACHINE_LEARNING_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-extreme-db" in payload:
        is_valid, error = _validate_enum_field(
            "use-extreme-db",
            payload["use-extreme-db"],
            VALID_BODY_USE_EXTREME_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "grayware" in payload:
        is_valid, error = _validate_enum_field(
            "grayware",
            payload["grayware"],
            VALID_BODY_GRAYWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-infected-result" in payload:
        is_valid, error = _validate_enum_field(
            "cache-infected-result",
            payload["cache-infected-result"],
            VALID_BODY_CACHE_INFECTED_RESULT,
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
    "endpoint": "antivirus/settings",
    "category": "cmdb",
    "api_path": "antivirus/settings",
    "help": "Configure AntiVirus settings.",
    "total_fields": 5,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
