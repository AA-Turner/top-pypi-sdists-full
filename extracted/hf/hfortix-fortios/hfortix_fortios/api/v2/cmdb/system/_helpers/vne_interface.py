"""Validation helpers for system/vne_interface - Auto-generated"""

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
    "interface",  # Interface name.
    "bmr-hostname",  # BMR hostname.
    "br",  # IPv6 address or FQDN of the border relay.
    "update-url",  # URL of provisioning server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "interface": "",
    "ssl-certificate": "Fortinet_Factory",
    "auto-asic-offload": "enable",
    "ipv4-address": "0.0.0.0 0.0.0.0",
    "br": "",
    "update-url": "",
    "mode": "map-e",
    "http-username": "",
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
    "name": "string",  # VNE tunnel name.
    "interface": "string",  # Interface name.
    "ssl-certificate": "string",  # Name of local certificate for SSL connections.
    "bmr-hostname": "password",  # BMR hostname.
    "auto-asic-offload": "option",  # Enable/disable tunnel ASIC offloading.
    "ipv4-address": "ipv4-classnet-host",  # Tunnel IPv4 address and netmask.
    "br": "string",  # IPv6 address or FQDN of the border relay.
    "update-url": "string",  # URL of provisioning server.
    "mode": "option",  # VNE tunnel mode.
    "http-username": "string",  # HTTP authentication user name.
    "http-password": "password",  # HTTP authentication password.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "VNE tunnel name.",
    "interface": "Interface name.",
    "ssl-certificate": "Name of local certificate for SSL connections.",
    "bmr-hostname": "BMR hostname.",
    "auto-asic-offload": "Enable/disable tunnel ASIC offloading.",
    "ipv4-address": "Tunnel IPv4 address and netmask.",
    "br": "IPv6 address or FQDN of the border relay.",
    "update-url": "URL of provisioning server.",
    "mode": "VNE tunnel mode.",
    "http-username": "HTTP authentication user name.",
    "http-password": "HTTP authentication password.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "interface": {"type": "string", "max_length": 15},
    "ssl-certificate": {"type": "string", "max_length": 35},
    "br": {"type": "string", "max_length": 255},
    "update-url": {"type": "string", "max_length": 511},
    "http-username": {"type": "string", "max_length": 64},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_AUTO_ASIC_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_MODE = [
    "map-e",
    "fixed-ip",
    "ds-lite",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_vne_interface_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/vne_interface."""
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


def validate_system_vne_interface_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/vne_interface object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
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


def validate_system_vne_interface_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/vne_interface."""
    # Validate enum values using central function
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
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
    "endpoint": "system/vne_interface",
    "category": "cmdb",
    "api_path": "system/vne-interface",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure virtual network enabler tunnels.",
    "total_fields": 11,
    "required_fields_count": 4,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
