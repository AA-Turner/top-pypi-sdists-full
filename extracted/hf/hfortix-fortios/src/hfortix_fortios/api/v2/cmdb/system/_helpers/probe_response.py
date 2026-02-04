"""Validation helpers for system/probe_response - Auto-generated"""

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
    "port": 8008,
    "http-probe-value": "OK",
    "ttl-mode": "retain",
    "mode": "none",
    "security-mode": "none",
    "timeout": 300,
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
    "port": "integer",  # Port number to response.
    "http-probe-value": "string",  # Value to respond to the monitoring server.
    "ttl-mode": "option",  # Mode for TWAMP packet TTL modification.
    "mode": "option",  # SLA response mode.
    "security-mode": "option",  # TWAMP responder security mode.
    "password": "password",  # TWAMP responder password in authentication mode.
    "timeout": "integer",  # An inactivity timer for a twamp test session.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "port": "Port number to response.",
    "http-probe-value": "Value to respond to the monitoring server.",
    "ttl-mode": "Mode for TWAMP packet TTL modification.",
    "mode": "SLA response mode.",
    "security-mode": "TWAMP responder security mode.",
    "password": "TWAMP responder password in authentication mode.",
    "timeout": "An inactivity timer for a twamp test session.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "port": {"type": "integer", "min": 1, "max": 65535},
    "http-probe-value": {"type": "string", "max_length": 1024},
    "timeout": {"type": "integer", "min": 10, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TTL_MODE = [
    "reinit",
    "decrease",
    "retain",
]
VALID_BODY_MODE = [
    "none",
    "http-probe",
    "twamp",
]
VALID_BODY_SECURITY_MODE = [
    "none",
    "authentication",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_probe_response_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/probe_response."""
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


def validate_system_probe_response_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/probe_response object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ttl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ttl-mode",
            payload["ttl-mode"],
            VALID_BODY_TTL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_probe_response_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/probe_response."""
    # Validate enum values using central function
    if "ttl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ttl-mode",
            payload["ttl-mode"],
            VALID_BODY_TTL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
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
    "endpoint": "system/probe_response",
    "category": "cmdb",
    "api_path": "system/probe-response",
    "help": "Configure system probe response.",
    "total_fields": 7,
    "required_fields_count": 0,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
