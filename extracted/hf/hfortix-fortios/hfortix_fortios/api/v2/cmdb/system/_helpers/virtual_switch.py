"""Validation helpers for system/virtual_switch - Auto-generated"""

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
    "name": "string",  # Name of the virtual switch.
    "physical-switch": "string",  # Physical switch parent.
    "vlan": "integer",  # VLAN.
    "port": "table",  # Configure member ports.
    "span": "option",  # Enable/disable SPAN.   
disable:Disable SPAN.   
enable:Enab
    "span-source-port": "string",  # SPAN source port.
    "span-dest-port": "string",  # SPAN destination port.
    "span-direction": "option",  # SPAN direction.   
rx:SPAN receive direction only.   
tx:SPA
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name of the virtual switch.",
    "physical-switch": "Physical switch parent.",
    "vlan": "VLAN.",
    "port": "Configure member ports.",
    "span": "Enable/disable SPAN.    disable:Disable SPAN.    enable:Enable SPAN.",
    "span-source-port": "SPAN source port.",
    "span-dest-port": "SPAN destination port.",
    "span-direction": "SPAN direction.    rx:SPAN receive direction only.    tx:SPAN transmit direction only.    both:SPAN both directions.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "port": {
        "name": {
            "type": "string",
            "help": "Physical interface name.",
        },
        "alias": {
            "type": "string",
            "help": "Alias.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SPAN = [
    "disable",
    "enable",
]
VALID_BODY_SPAN_DIRECTION = [
    "rx",
    "tx",
    "both",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_virtual_switch_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/virtual_switch."""
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


def validate_system_virtual_switch_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/virtual_switch object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "span" in payload:
        is_valid, error = _validate_enum_field(
            "span",
            payload["span"],
            VALID_BODY_SPAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "span-direction" in payload:
        is_valid, error = _validate_enum_field(
            "span-direction",
            payload["span-direction"],
            VALID_BODY_SPAN_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_virtual_switch_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/virtual_switch."""
    # Validate enum values using central function
    if "span" in payload:
        is_valid, error = _validate_enum_field(
            "span",
            payload["span"],
            VALID_BODY_SPAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "span-direction" in payload:
        is_valid, error = _validate_enum_field(
            "span-direction",
            payload["span-direction"],
            VALID_BODY_SPAN_DIRECTION,
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
    "endpoint": "system/virtual_switch",
    "category": "cmdb",
    "api_path": "system/virtual-switch",
    "help": "Configuration for system/virtual_switch",
    "total_fields": 8,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
