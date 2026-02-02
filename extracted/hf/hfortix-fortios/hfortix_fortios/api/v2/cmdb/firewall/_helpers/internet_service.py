"""Validation helpers for firewall/internet_service - Auto-generated"""

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
    "id": 0,
    "name": "",
    "icon-id": 0,
    "direction": "both",
    "database": "isdb",
    "ip-range-number": 0,
    "extra-ip-range-number": 0,
    "ip-number": 0,
    "ip6-range-number": 0,
    "extra-ip6-range-number": 0,
    "singularity": 0,
    "obsolete": 0,
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
    "id": "integer",  # Internet Service ID.
    "name": "string",  # Internet Service name.
    "icon-id": "integer",  # Icon ID of Internet Service.
    "direction": "option",  # How this service may be used in a firewall policy (source, d
    "database": "option",  # Database name this Internet Service belongs to.
    "ip-range-number": "integer",  # Number of IPv4 ranges.
    "extra-ip-range-number": "integer",  # Extra number of IPv4 ranges.
    "ip-number": "integer",  # Total number of IPv4 addresses.
    "ip6-range-number": "integer",  # Number of IPv6 ranges.
    "extra-ip6-range-number": "integer",  # Extra number of IPv6 ranges.
    "singularity": "integer",  # Singular level of the Internet Service.
    "obsolete": "integer",  # Indicates whether the Internet Service can be used.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Internet Service ID.",
    "name": "Internet Service name.",
    "icon-id": "Icon ID of Internet Service.",
    "direction": "How this service may be used in a firewall policy (source, destination or both).",
    "database": "Database name this Internet Service belongs to.",
    "ip-range-number": "Number of IPv4 ranges.",
    "extra-ip-range-number": "Extra number of IPv4 ranges.",
    "ip-number": "Total number of IPv4 addresses.",
    "ip6-range-number": "Number of IPv6 ranges.",
    "extra-ip6-range-number": "Extra number of IPv6 ranges.",
    "singularity": "Singular level of the Internet Service.",
    "obsolete": "Indicates whether the Internet Service can be used.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 63},
    "icon-id": {"type": "integer", "min": 0, "max": 4294967295},
    "ip-range-number": {"type": "integer", "min": 0, "max": 4294967295},
    "extra-ip-range-number": {"type": "integer", "min": 0, "max": 4294967295},
    "ip-number": {"type": "integer", "min": 0, "max": 4294967295},
    "ip6-range-number": {"type": "integer", "min": 0, "max": 4294967295},
    "extra-ip6-range-number": {"type": "integer", "min": 0, "max": 4294967295},
    "singularity": {"type": "integer", "min": 0, "max": 65535},
    "obsolete": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_DIRECTION = [
    "src",
    "dst",
    "both",
]
VALID_BODY_DATABASE = [
    "isdb",
    "irdb",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_internet_service_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/internet_service."""
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


def validate_firewall_internet_service_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/internet_service object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "direction" in payload:
        is_valid, error = _validate_enum_field(
            "direction",
            payload["direction"],
            VALID_BODY_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database" in payload:
        is_valid, error = _validate_enum_field(
            "database",
            payload["database"],
            VALID_BODY_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_internet_service_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/internet_service."""
    # Validate enum values using central function
    if "direction" in payload:
        is_valid, error = _validate_enum_field(
            "direction",
            payload["direction"],
            VALID_BODY_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database" in payload:
        is_valid, error = _validate_enum_field(
            "database",
            payload["database"],
            VALID_BODY_DATABASE,
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
    "endpoint": "firewall/internet_service",
    "category": "cmdb",
    "api_path": "firewall/internet-service",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Show Internet Service application.",
    "total_fields": 12,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
