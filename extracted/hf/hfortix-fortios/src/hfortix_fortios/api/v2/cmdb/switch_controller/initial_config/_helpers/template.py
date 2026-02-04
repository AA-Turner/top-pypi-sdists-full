"""Validation helpers for switch_controller/initial_config/template - Auto-generated"""

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
    "name",  # Initial config template name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "vlanid": 0,
    "ip": "0.0.0.0 0.0.0.0",
    "allowaccess": "",
    "auto-ip": "enable",
    "dhcp-server": "disable",
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
    "name": "string",  # Initial config template name.
    "vlanid": "integer",  # Unique VLAN ID.
    "ip": "ipv4-classnet-host",  # Interface IPv4 address and subnet mask.
    "allowaccess": "option",  # Permitted types of management access to this interface.
    "auto-ip": "option",  # Automatically allocate interface address and subnet block.
    "dhcp-server": "option",  # Enable/disable a DHCP server on this interface.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Initial config template name.",
    "vlanid": "Unique VLAN ID.",
    "ip": "Interface IPv4 address and subnet mask.",
    "allowaccess": "Permitted types of management access to this interface.",
    "auto-ip": "Automatically allocate interface address and subnet block.",
    "dhcp-server": "Enable/disable a DHCP server on this interface.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "vlanid": {"type": "integer", "min": 1, "max": 4094},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_ALLOWACCESS = [
    "ping",
    "https",
    "ssh",
    "snmp",
    "http",
    "telnet",
    "fgfm",
    "radius-acct",
    "probe-response",
    "fabric",
    "ftm",
]
VALID_BODY_AUTO_IP = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_SERVER = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_initial_config_template_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/initial_config/template."""
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


def validate_switch_controller_initial_config_template_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/initial_config/template object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-ip" in payload:
        is_valid, error = _validate_enum_field(
            "auto-ip",
            payload["auto-ip"],
            VALID_BODY_AUTO_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server",
            payload["dhcp-server"],
            VALID_BODY_DHCP_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_initial_config_template_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/initial_config/template."""
    # Validate enum values using central function
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-ip" in payload:
        is_valid, error = _validate_enum_field(
            "auto-ip",
            payload["auto-ip"],
            VALID_BODY_AUTO_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server",
            payload["dhcp-server"],
            VALID_BODY_DHCP_SERVER,
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
    "endpoint": "switch_controller/initial_config/template",
    "category": "cmdb",
    "api_path": "switch-controller.initial-config/template",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure template for auto-generated VLANs.",
    "total_fields": 6,
    "required_fields_count": 1,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
