"""Validation helpers for system/sdn_vpn - Auto-generated"""

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
    "sdn",  # SDN connector name.
    "vgw-id",  # Virtual private gateway id.
    "tgw-id",  # Transit gateway id.
    "tunnel-interface",  # Tunnel interface with public IP.
    "internal-interface",  # Internal interface with local subnet.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "sdn": "",
    "remote-type": "vgw",
    "routing-type": "dynamic",
    "vgw-id": "",
    "tgw-id": "",
    "subnet-id": "",
    "bgp-as": 65000,
    "cgw-gateway": "0.0.0.0",
    "nat-traversal": "enable",
    "tunnel-interface": "",
    "internal-interface": "",
    "local-cidr": "0.0.0.0 0.0.0.0",
    "remote-cidr": "0.0.0.0 0.0.0.0",
    "cgw-name": "",
    "type": 0,
    "status": 0,
    "code": 0,
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
    "name": "string",  # Public cloud VPN name.
    "sdn": "string",  # SDN connector name.
    "remote-type": "option",  # Type of remote device.
    "routing-type": "option",  # Type of routing.
    "vgw-id": "string",  # Virtual private gateway id.
    "tgw-id": "string",  # Transit gateway id.
    "subnet-id": "string",  # AWS subnet id for TGW route propagation.
    "bgp-as": "integer",  # BGP Router AS number.
    "cgw-gateway": "ipv4-address-any",  # Public IP address of the customer gateway.
    "nat-traversal": "option",  # Enable/disable use for NAT traversal. Please enable if your 
    "tunnel-interface": "string",  # Tunnel interface with public IP.
    "internal-interface": "string",  # Internal interface with local subnet.
    "local-cidr": "ipv4-classnet",  # Local subnet address and subnet mask.
    "remote-cidr": "ipv4-classnet",  # Remote subnet address and subnet mask.
    "cgw-name": "string",  # AWS customer gateway name to be created.
    "psksecret": "password-3",  # Pre-shared secret for PSK authentication. Auto-generated if 
    "type": "integer",  # SDN VPN type.
    "status": "integer",  # SDN VPN status.
    "code": "integer",  # SDN VPN error code.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Public cloud VPN name.",
    "sdn": "SDN connector name.",
    "remote-type": "Type of remote device.",
    "routing-type": "Type of routing.",
    "vgw-id": "Virtual private gateway id.",
    "tgw-id": "Transit gateway id.",
    "subnet-id": "AWS subnet id for TGW route propagation.",
    "bgp-as": "BGP Router AS number.",
    "cgw-gateway": "Public IP address of the customer gateway.",
    "nat-traversal": "Enable/disable use for NAT traversal. Please enable if your FortiGate device is behind a NAT/PAT device.",
    "tunnel-interface": "Tunnel interface with public IP.",
    "internal-interface": "Internal interface with local subnet.",
    "local-cidr": "Local subnet address and subnet mask.",
    "remote-cidr": "Remote subnet address and subnet mask.",
    "cgw-name": "AWS customer gateway name to be created.",
    "psksecret": "Pre-shared secret for PSK authentication. Auto-generated if not specified",
    "type": "SDN VPN type.",
    "status": "SDN VPN status.",
    "code": "SDN VPN error code.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "sdn": {"type": "string", "max_length": 35},
    "vgw-id": {"type": "string", "max_length": 63},
    "tgw-id": {"type": "string", "max_length": 63},
    "subnet-id": {"type": "string", "max_length": 63},
    "bgp-as": {"type": "integer", "min": 1, "max": 4294967295},
    "tunnel-interface": {"type": "string", "max_length": 15},
    "internal-interface": {"type": "string", "max_length": 15},
    "cgw-name": {"type": "string", "max_length": 35},
    "type": {"type": "integer", "min": 0, "max": 65535},
    "status": {"type": "integer", "min": 0, "max": 255},
    "code": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_REMOTE_TYPE = [
    "vgw",
    "tgw",
]
VALID_BODY_ROUTING_TYPE = [
    "static",
    "dynamic",
]
VALID_BODY_NAT_TRAVERSAL = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_sdn_vpn_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/sdn_vpn."""
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


def validate_system_sdn_vpn_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/sdn_vpn object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "remote-type" in payload:
        is_valid, error = _validate_enum_field(
            "remote-type",
            payload["remote-type"],
            VALID_BODY_REMOTE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "routing-type" in payload:
        is_valid, error = _validate_enum_field(
            "routing-type",
            payload["routing-type"],
            VALID_BODY_ROUTING_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat-traversal" in payload:
        is_valid, error = _validate_enum_field(
            "nat-traversal",
            payload["nat-traversal"],
            VALID_BODY_NAT_TRAVERSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_sdn_vpn_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/sdn_vpn."""
    # Validate enum values using central function
    if "remote-type" in payload:
        is_valid, error = _validate_enum_field(
            "remote-type",
            payload["remote-type"],
            VALID_BODY_REMOTE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "routing-type" in payload:
        is_valid, error = _validate_enum_field(
            "routing-type",
            payload["routing-type"],
            VALID_BODY_ROUTING_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat-traversal" in payload:
        is_valid, error = _validate_enum_field(
            "nat-traversal",
            payload["nat-traversal"],
            VALID_BODY_NAT_TRAVERSAL,
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
    "endpoint": "system/sdn_vpn",
    "category": "cmdb",
    "api_path": "system/sdn-vpn",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure public cloud VPN service.",
    "total_fields": 19,
    "required_fields_count": 5,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
