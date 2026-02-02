"""Validation helpers for system/lte_modem - Auto-generated"""

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
    "status": "option",  # Enable/disable USB LTE/WIMAX device.   
enable:Enable USB LT
    "extra-init": "string",  # Extra initialization string for USB LTE/WIMAX devices.
    "pdptype": "option",  # Packet Data Protocol (PDP) context type.   
IPv4:Only IPv4.
    "authtype": "option",  # Authentication type for PDP-IP packet data calls.   
none:Us
    "username": "string",  # Authentication username for PDP-IP packet data calls.
    "passwd": "string",  # Authentication password for PDP-IP packet data calls.
    "apn": "string",  # Login APN string for PDP-IP packet data calls.
    "modem-port": "integer",  # Modem port index (0 - 20).
    "mode": "option",  # Modem operation mode.   
standalone:Standalone modem operati
    "holddown-timer": "integer",  # Hold down timer (10 - 60 sec).
    "interface": "string",  # The interface that the modem is acting as a redundant interf
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable USB LTE/WIMAX device.    enable:Enable USB LTE/WIMA device.    disable:Disable USB LTE/WIMA device.",
    "extra-init": "Extra initialization string for USB LTE/WIMAX devices.",
    "pdptype": "Packet Data Protocol (PDP) context type.    IPv4:Only IPv4.",
    "authtype": "Authentication type for PDP-IP packet data calls.    none:Username and password not required.    pap:Use PAP authentication.    chap:Use CHAP authentication.",
    "username": "Authentication username for PDP-IP packet data calls.",
    "passwd": "Authentication password for PDP-IP packet data calls.",
    "apn": "Login APN string for PDP-IP packet data calls.",
    "modem-port": "Modem port index (0 - 20).",
    "mode": "Modem operation mode.    standalone:Standalone modem operation mode.    redundant:Redundant modem operation mode where the modem is used as a backup interface.",
    "holddown-timer": "Hold down timer (10 - 60 sec).",
    "interface": "The interface that the modem is acting as a redundant interface for.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_PDPTYPE = [
    "IPv4",
]
VALID_BODY_AUTHTYPE = [
    "none",
    "pap",
    "chap",
]
VALID_BODY_MODE = [
    "standalone",
    "redundant",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_lte_modem_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/lte_modem."""
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


def validate_system_lte_modem_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/lte_modem object."""
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
    if "pdptype" in payload:
        is_valid, error = _validate_enum_field(
            "pdptype",
            payload["pdptype"],
            VALID_BODY_PDPTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype" in payload:
        is_valid, error = _validate_enum_field(
            "authtype",
            payload["authtype"],
            VALID_BODY_AUTHTYPE,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_lte_modem_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/lte_modem."""
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
    if "pdptype" in payload:
        is_valid, error = _validate_enum_field(
            "pdptype",
            payload["pdptype"],
            VALID_BODY_PDPTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype" in payload:
        is_valid, error = _validate_enum_field(
            "authtype",
            payload["authtype"],
            VALID_BODY_AUTHTYPE,
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
    "endpoint": "system/lte_modem",
    "category": "cmdb",
    "api_path": "system/lte-modem",
    "help": "Configuration for system/lte_modem",
    "total_fields": 11,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
