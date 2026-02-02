"""Validation helpers for system/snmp/sysinfo - Auto-generated"""

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
    "engine-id-type": "text",
    "engine-id": "",
    "trap-high-cpu-threshold": 80,
    "trap-low-memory-threshold": 80,
    "trap-log-full-threshold": 90,
    "trap-free-memory-threshold": 5,
    "trap-freeable-memory-threshold": 60,
    "append-index": "disable",
    "non-mgmt-vdom-query": "disable",
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
    "status": "option",  # Enable/disable SNMP.
    "engine-id-type": "option",  # Local SNMP engineID type (text/hex/mac).
    "engine-id": "string",  # Local SNMP engineID string (maximum 27 characters).
    "description": "var-string",  # System description.
    "contact-info": "var-string",  # Contact information.
    "location": "var-string",  # System location.
    "trap-high-cpu-threshold": "integer",  # CPU usage when trap is sent.
    "trap-low-memory-threshold": "integer",  # Memory usage when trap is sent.
    "trap-log-full-threshold": "integer",  # Log disk usage when trap is sent.
    "trap-free-memory-threshold": "integer",  # Free memory usage when trap is sent.
    "trap-freeable-memory-threshold": "integer",  # Freeable memory usage when trap is sent.
    "append-index": "option",  # Enable/disable allowance of appending vdom or interface inde
    "non-mgmt-vdom-query": "option",  # Enable/disable allowance of SNMPv3 query from non-management
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable SNMP.",
    "engine-id-type": "Local SNMP engineID type (text/hex/mac).",
    "engine-id": "Local SNMP engineID string (maximum 27 characters).",
    "description": "System description.",
    "contact-info": "Contact information.",
    "location": "System location.",
    "trap-high-cpu-threshold": "CPU usage when trap is sent.",
    "trap-low-memory-threshold": "Memory usage when trap is sent.",
    "trap-log-full-threshold": "Log disk usage when trap is sent.",
    "trap-free-memory-threshold": "Free memory usage when trap is sent.",
    "trap-freeable-memory-threshold": "Freeable memory usage when trap is sent.",
    "append-index": "Enable/disable allowance of appending vdom or interface index in some RFC tables.",
    "non-mgmt-vdom-query": "Enable/disable allowance of SNMPv3 query from non-management vdoms.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "engine-id": {"type": "string", "max_length": 54},
    "trap-high-cpu-threshold": {"type": "integer", "min": 1, "max": 100},
    "trap-low-memory-threshold": {"type": "integer", "min": 1, "max": 100},
    "trap-log-full-threshold": {"type": "integer", "min": 1, "max": 100},
    "trap-free-memory-threshold": {"type": "integer", "min": 1, "max": 100},
    "trap-freeable-memory-threshold": {"type": "integer", "min": 1, "max": 100},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ENGINE_ID_TYPE = [
    "text",
    "hex",
    "mac",
]
VALID_BODY_APPEND_INDEX = [
    "enable",
    "disable",
]
VALID_BODY_NON_MGMT_VDOM_QUERY = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_snmp_sysinfo_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/snmp/sysinfo."""
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


def validate_system_snmp_sysinfo_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/snmp/sysinfo object."""
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
    if "engine-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "engine-id-type",
            payload["engine-id-type"],
            VALID_BODY_ENGINE_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "append-index" in payload:
        is_valid, error = _validate_enum_field(
            "append-index",
            payload["append-index"],
            VALID_BODY_APPEND_INDEX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "non-mgmt-vdom-query" in payload:
        is_valid, error = _validate_enum_field(
            "non-mgmt-vdom-query",
            payload["non-mgmt-vdom-query"],
            VALID_BODY_NON_MGMT_VDOM_QUERY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_snmp_sysinfo_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/snmp/sysinfo."""
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
    if "engine-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "engine-id-type",
            payload["engine-id-type"],
            VALID_BODY_ENGINE_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "append-index" in payload:
        is_valid, error = _validate_enum_field(
            "append-index",
            payload["append-index"],
            VALID_BODY_APPEND_INDEX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "non-mgmt-vdom-query" in payload:
        is_valid, error = _validate_enum_field(
            "non-mgmt-vdom-query",
            payload["non-mgmt-vdom-query"],
            VALID_BODY_NON_MGMT_VDOM_QUERY,
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
    "endpoint": "system/snmp/sysinfo",
    "category": "cmdb",
    "api_path": "system.snmp/sysinfo",
    "help": "SNMP system info configuration.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 10,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
