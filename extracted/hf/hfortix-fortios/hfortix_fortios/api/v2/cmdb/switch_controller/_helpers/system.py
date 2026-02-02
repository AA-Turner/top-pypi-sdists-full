"""Validation helpers for switch_controller/system - Auto-generated"""

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
    "parallel-process-override": "disable",
    "parallel-process": 1,
    "data-sync-interval": 60,
    "iot-weight-threshold": 1,
    "iot-scan-interval": 60,
    "iot-holdoff": 5,
    "iot-mac-idle": 1440,
    "nac-periodic-interval": 60,
    "dynamic-periodic-interval": 60,
    "tunnel-mode": "compatible",
    "caputp-echo-interval": 30,
    "caputp-max-retransmit": 5,
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
    "parallel-process-override": "option",  # Enable/disable parallel process override.
    "parallel-process": "integer",  # Maximum number of parallel processes.
    "data-sync-interval": "integer",  # Time interval between collection of switch data (30 - 1800 s
    "iot-weight-threshold": "integer",  # MAC entry's confidence value. Value is re-queried when below
    "iot-scan-interval": "integer",  # IoT scan interval (2 - 10080 mins, default = 60 mins, 0 = di
    "iot-holdoff": "integer",  # MAC entry's creation time. Time must be greater than this va
    "iot-mac-idle": "integer",  # MAC entry's idle time. MAC entry is removed after this value
    "nac-periodic-interval": "integer",  # Periodic time interval to run NAC engine (5 - 180 sec, defau
    "dynamic-periodic-interval": "integer",  # Periodic time interval to run Dynamic port policy engine (5 
    "tunnel-mode": "option",  # Compatible/strict tunnel mode.
    "caputp-echo-interval": "integer",  # Echo interval for the caputp echo requests from swtp.
    "caputp-max-retransmit": "integer",  # Maximum retransmission count for the caputp tunnel packets.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "parallel-process-override": "Enable/disable parallel process override.",
    "parallel-process": "Maximum number of parallel processes.",
    "data-sync-interval": "Time interval between collection of switch data (30 - 1800 sec, default = 60, 0 = disable).",
    "iot-weight-threshold": "MAC entry's confidence value. Value is re-queried when below this value (default = 1, 0 = disable).",
    "iot-scan-interval": "IoT scan interval (2 - 10080 mins, default = 60 mins, 0 = disable).",
    "iot-holdoff": "MAC entry's creation time. Time must be greater than this value for an entry to be created (0 - 10080 mins, default = 5 mins).",
    "iot-mac-idle": "MAC entry's idle time. MAC entry is removed after this value (0 - 10080 mins, default = 1440 mins).",
    "nac-periodic-interval": "Periodic time interval to run NAC engine (5 - 180 sec, default = 60).",
    "dynamic-periodic-interval": "Periodic time interval to run Dynamic port policy engine (5 - 180 sec, default = 60).",
    "tunnel-mode": "Compatible/strict tunnel mode.",
    "caputp-echo-interval": "Echo interval for the caputp echo requests from swtp.",
    "caputp-max-retransmit": "Maximum retransmission count for the caputp tunnel packets.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "parallel-process": {"type": "integer", "min": 1, "max": 24},
    "data-sync-interval": {"type": "integer", "min": 30, "max": 1800},
    "iot-weight-threshold": {"type": "integer", "min": 0, "max": 255},
    "iot-scan-interval": {"type": "integer", "min": 2, "max": 10080},
    "iot-holdoff": {"type": "integer", "min": 0, "max": 10080},
    "iot-mac-idle": {"type": "integer", "min": 0, "max": 10080},
    "nac-periodic-interval": {"type": "integer", "min": 5, "max": 180},
    "dynamic-periodic-interval": {"type": "integer", "min": 5, "max": 180},
    "caputp-echo-interval": {"type": "integer", "min": 8, "max": 600},
    "caputp-max-retransmit": {"type": "integer", "min": 0, "max": 64},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_PARALLEL_PROCESS_OVERRIDE = [
    "disable",
    "enable",
]
VALID_BODY_TUNNEL_MODE = [
    "compatible",
    "moderate",
    "strict",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_system_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/system."""
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


def validate_switch_controller_system_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/system object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "parallel-process-override" in payload:
        is_valid, error = _validate_enum_field(
            "parallel-process-override",
            payload["parallel-process-override"],
            VALID_BODY_PARALLEL_PROCESS_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_system_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/system."""
    # Validate enum values using central function
    if "parallel-process-override" in payload:
        is_valid, error = _validate_enum_field(
            "parallel-process-override",
            payload["parallel-process-override"],
            VALID_BODY_PARALLEL_PROCESS_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
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
    "endpoint": "switch_controller/system",
    "category": "cmdb",
    "api_path": "switch-controller/system",
    "help": "Configure system-wide switch controller settings.",
    "total_fields": 12,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
