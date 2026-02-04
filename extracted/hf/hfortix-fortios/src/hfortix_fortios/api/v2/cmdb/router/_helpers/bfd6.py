"""Validation helpers for router/bfd6 - Auto-generated"""

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
    "neighbor": "string",  # Configure neighbor of IPv6 BFD.
    "multihop-template": "string",  # BFD IPv6 multi-hop template table.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "neighbor": "Configure neighbor of IPv6 BFD.",
    "multihop-template": "BFD IPv6 multi-hop template table.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "neighbor": {
        "ip6-address": {
            "type": "ipv6-address",
            "help": "IPv6 address of the BFD neighbor.",
            "required": True,
            "default": "::",
        },
        "interface": {
            "type": "string",
            "help": "Interface to the BFD neighbor.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "multihop-template": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "src": {
            "type": "ipv6-network",
            "help": "Source prefix.",
            "required": True,
            "default": "::/0",
        },
        "dst": {
            "type": "ipv6-network",
            "help": "Destination prefix.",
            "required": True,
            "default": "::/0",
        },
        "bfd-desired-min-tx": {
            "type": "integer",
            "help": "BFD desired minimal transmit interval (milliseconds).",
            "default": 250,
            "min_value": 100,
            "max_value": 30000,
        },
        "bfd-required-min-rx": {
            "type": "integer",
            "help": "BFD required minimal receive interval (milliseconds).",
            "default": 250,
            "min_value": 100,
            "max_value": 30000,
        },
        "bfd-detect-mult": {
            "type": "integer",
            "help": "BFD detection multiplier.",
            "default": 3,
            "min_value": 3,
            "max_value": 50,
        },
        "auth-mode": {
            "type": "option",
            "help": "Authentication mode.",
            "default": "none",
            "options": ["none", "md5"],
        },
        "md5-key": {
            "type": "password",
            "help": "MD5 key of key ID 1.",
            "max_length": 16,
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_bfd6_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/bfd6."""
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


def validate_router_bfd6_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/bfd6 object."""
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


def validate_router_bfd6_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/bfd6."""
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
    "endpoint": "router/bfd6",
    "category": "cmdb",
    "api_path": "router/bfd6",
    "help": "Configure IPv6 BFD.",
    "total_fields": 2,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
