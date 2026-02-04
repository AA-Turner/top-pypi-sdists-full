"""Validation helpers for webfilter/override - Auto-generated"""

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
    "user",  # Name of the user which the override applies.
    "user-group",  # Specify the user group for which the override applies.
    "old-profile",  # Name of the web filter profile which the override applies.
    "new-profile",  # Name of the new web filter profile used by the override.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "status": "disable",
    "scope": "user",
    "ip": "0.0.0.0",
    "user": "",
    "user-group": "",
    "old-profile": "",
    "new-profile": "",
    "ip6": "::",
    "expires": "1970/01/01 00:00:00",
    "initiator": "",
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
    "id": "integer",  # Override rule ID.
    "status": "option",  # Enable/disable override rule.
    "scope": "option",  # Override either the specific user, user group, IPv4 address, or IPv6 address.
    "ip": "ipv4-address",  # IPv4 address which the override applies.
    "user": "string",  # Name of the user which the override applies.
    "user-group": "string",  # Specify the user group for which the override applies.
    "old-profile": "string",  # Name of the web filter profile which the override applies.
    "new-profile": "string",  # Name of the new web filter profile used by the override.
    "ip6": "ipv6-address",  # IPv6 address which the override applies.
    "expires": "user",  # Override expiration date and time, from 5 minutes to 365 from now (format: yyyy/
    "initiator": "string",  # Initiating user of override (read-only setting).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Override rule ID.",
    "status": "Enable/disable override rule.",
    "scope": "Override either the specific user, user group, IPv4 address, or IPv6 address.",
    "ip": "IPv4 address which the override applies.",
    "user": "Name of the user which the override applies.",
    "user-group": "Specify the user group for which the override applies.",
    "old-profile": "Name of the web filter profile which the override applies.",
    "new-profile": "Name of the new web filter profile used by the override.",
    "ip6": "IPv6 address which the override applies.",
    "expires": "Override expiration date and time, from 5 minutes to 365 from now (format: yyyy/mm/dd hh:mm:ss).",
    "initiator": "Initiating user of override (read-only setting).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "user": {"type": "string", "max_length": 64},
    "user-group": {"type": "string", "max_length": 63},
    "old-profile": {"type": "string", "max_length": 47},
    "new-profile": {"type": "string", "max_length": 47},
    "initiator": {"type": "string", "max_length": 64},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SCOPE = [
    "user",
    "user-group",
    "ip",
    "ip6",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_webfilter_override_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for webfilter/override."""
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


def validate_webfilter_override_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new webfilter/override object."""
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
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_webfilter_override_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update webfilter/override."""
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
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
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
    "endpoint": "webfilter/override",
    "category": "cmdb",
    "api_path": "webfilter/override",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure FortiGuard Web Filter administrative overrides.",
    "total_fields": 11,
    "required_fields_count": 4,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
