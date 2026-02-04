"""Validation helpers for wireless_controller/lw_profile - Auto-generated"""

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
    "comment": "",
    "lw-protocol": "basics-station",
    "cups-server": "",
    "cups-server-port": 0,
    "tc-server": "",
    "tc-server-port": 0,
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
    "name": "string",  # LoRaWAN profile name.
    "comment": "string",  # Comment.
    "lw-protocol": "option",  # Configure LoRaWAN protocol (default = basics-station)
    "cups-server": "string",  # CUPS (Configuration and Update Server) domain name or IP address of LoRaWAN devi
    "cups-server-port": "integer",  # CUPS Port value of LoRaWAN device.
    "cups-api-key": "password",  # CUPS API key of LoRaWAN device.
    "tc-server": "string",  # TC (Traffic Controller) domain name or IP address of LoRaWAN device.
    "tc-server-port": "integer",  # TC Port value of LoRaWAN device.
    "tc-api-key": "password",  # TC API key of LoRaWAN device.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "LoRaWAN profile name.",
    "comment": "Comment.",
    "lw-protocol": "Configure LoRaWAN protocol (default = basics-station)",
    "cups-server": "CUPS (Configuration and Update Server) domain name or IP address of LoRaWAN device.",
    "cups-server-port": "CUPS Port value of LoRaWAN device.",
    "cups-api-key": "CUPS API key of LoRaWAN device.",
    "tc-server": "TC (Traffic Controller) domain name or IP address of LoRaWAN device.",
    "tc-server-port": "TC Port value of LoRaWAN device.",
    "tc-api-key": "TC API key of LoRaWAN device.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comment": {"type": "string", "max_length": 63},
    "cups-server": {"type": "string", "max_length": 255},
    "cups-server-port": {"type": "integer", "min": 0, "max": 65535},
    "tc-server": {"type": "string", "max_length": 255},
    "tc-server-port": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_LW_PROTOCOL = [
    "basics-station",
    "packet-forwarder",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_lw_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/lw_profile."""
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


def validate_wireless_controller_lw_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/lw_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "lw-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "lw-protocol",
            payload["lw-protocol"],
            VALID_BODY_LW_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_lw_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/lw_profile."""
    # Validate enum values using central function
    if "lw-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "lw-protocol",
            payload["lw-protocol"],
            VALID_BODY_LW_PROTOCOL,
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
    "endpoint": "wireless_controller/lw_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/lw-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure LoRaWAN profile.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 7,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
