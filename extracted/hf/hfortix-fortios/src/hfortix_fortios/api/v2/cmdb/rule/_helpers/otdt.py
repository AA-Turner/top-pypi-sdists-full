"""Validation helpers for rule/otdt - Auto-generated"""

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
    "id": 0,
    "category": 0,
    "popularity": 0,
    "risk": 0,
    "weight": 0,
    "protocol": "",
    "technology": "",
    "behavior": "",
    "vendor": "",
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
    "name": "string",  # Application name.
    "id": "integer",  # Application ID.
    "category": "integer",  # Application category ID.
    "popularity": "integer",  # Application popularity.
    "risk": "integer",  # Application risk.
    "weight": "integer",  # Application weight.
    "protocol": "user",  # Application protocol.
    "technology": "user",  # Application technology.
    "behavior": "user",  # Application behavior.
    "vendor": "user",  # Application vendor.
    "parameters": "string",  # Application parameters.
    "metadata": "string",  # Meta data.
    "status": "key",  # Print all OT detection rules information.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Application name.",
    "id": "Application ID.",
    "category": "Application category ID.",
    "popularity": "Application popularity.",
    "risk": "Application risk.",
    "weight": "Application weight.",
    "protocol": "Application protocol.",
    "technology": "Application technology.",
    "behavior": "Application behavior.",
    "vendor": "Application vendor.",
    "parameters": "Application parameters.",
    "metadata": "Meta data.",
    "status": "Print all OT detection rules information.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "category": {"type": "integer", "min": 0, "max": 4294967295},
    "popularity": {"type": "integer", "min": 0, "max": 255},
    "risk": {"type": "integer", "min": 0, "max": 255},
    "weight": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "parameters": {
        "name": {
            "type": "string",
            "help": "Parameter name.",
            "default": "",
            "max_length": 31,
        },
        "default value": {
            "type": "string",
            "help": "Parameter default value.",
            "default": "",
            "max_length": 199,
        },
    },
    "metadata": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "metaid": {
            "type": "integer",
            "help": "Meta ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "valueid": {
            "type": "integer",
            "help": "Value ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_rule_otdt_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for rule/otdt."""
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


def validate_rule_otdt_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new rule/otdt object."""
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


def validate_rule_otdt_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update rule/otdt."""
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
    "endpoint": "rule/otdt",
    "category": "cmdb",
    "api_path": "rule/otdt",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Show OT detection signatures.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 10,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
