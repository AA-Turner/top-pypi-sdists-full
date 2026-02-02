"""Validation helpers for switch_controller/initial_config/vlans - Auto-generated"""

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
    "optional-vlans": "enable",
    "default-vlan": "_default",
    "quarantine": "quarantine",
    "rspan": "rspan",
    "voice": "voice",
    "video": "video",
    "nac": "onboarding",
    "nac-segment": "nac_segment",
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
    "optional-vlans": "option",  # Auto-generate pre-configured VLANs upon switch discovery.
    "default-vlan": "string",  # Default VLAN (native) assigned to all switch ports upon disc
    "quarantine": "string",  # VLAN for quarantined traffic.
    "rspan": "string",  # VLAN for RSPAN/ERSPAN mirrored traffic.
    "voice": "string",  # VLAN dedicated for voice devices.
    "video": "string",  # VLAN dedicated for video devices.
    "nac": "string",  # VLAN for NAC onboarding devices.
    "nac-segment": "string",  # VLAN for NAC segment primary interface.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "optional-vlans": "Auto-generate pre-configured VLANs upon switch discovery.",
    "default-vlan": "Default VLAN (native) assigned to all switch ports upon discovery.",
    "quarantine": "VLAN for quarantined traffic.",
    "rspan": "VLAN for RSPAN/ERSPAN mirrored traffic.",
    "voice": "VLAN dedicated for voice devices.",
    "video": "VLAN dedicated for video devices.",
    "nac": "VLAN for NAC onboarding devices.",
    "nac-segment": "VLAN for NAC segment primary interface.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "default-vlan": {"type": "string", "max_length": 63},
    "quarantine": {"type": "string", "max_length": 63},
    "rspan": {"type": "string", "max_length": 63},
    "voice": {"type": "string", "max_length": 63},
    "video": {"type": "string", "max_length": 63},
    "nac": {"type": "string", "max_length": 63},
    "nac-segment": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_OPTIONAL_VLANS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_initial_config_vlans_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/initial_config/vlans."""
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


def validate_switch_controller_initial_config_vlans_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/initial_config/vlans object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "optional-vlans" in payload:
        is_valid, error = _validate_enum_field(
            "optional-vlans",
            payload["optional-vlans"],
            VALID_BODY_OPTIONAL_VLANS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_initial_config_vlans_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/initial_config/vlans."""
    # Validate enum values using central function
    if "optional-vlans" in payload:
        is_valid, error = _validate_enum_field(
            "optional-vlans",
            payload["optional-vlans"],
            VALID_BODY_OPTIONAL_VLANS,
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
    "endpoint": "switch_controller/initial_config/vlans",
    "category": "cmdb",
    "api_path": "switch-controller.initial-config/vlans",
    "help": "Configure initial template for auto-generated VLAN interfaces.",
    "total_fields": 8,
    "required_fields_count": 0,
    "fields_with_defaults_count": 8,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
