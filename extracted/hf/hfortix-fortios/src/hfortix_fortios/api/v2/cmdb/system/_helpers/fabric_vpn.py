"""Validation helpers for system/fabric_vpn - Auto-generated"""

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
    "psksecret",  # Pre-shared secret for ADVPN.
    "bgp-as",  # BGP Router AS number, asplain/asdot/asdot+ format.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "sync-mode": "enable",
    "branch-name": "",
    "policy-rule": "health-check",
    "vpn-role": "hub",
    "loopback-address-block": "0.0.0.0 0.0.0.0",
    "loopback-interface": "",
    "loopback-advertised-subnet": 0,
    "bgp-as": "",
    "sdwan-zone": "",
    "health-checks": "",
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
    "status": "option",  # Enable/disable Fabric VPN.
    "sync-mode": "option",  # Setting synchronized by fabric or manual.
    "branch-name": "string",  # Branch name.
    "policy-rule": "option",  # Policy creation rule.
    "vpn-role": "option",  # Fabric VPN role.
    "overlays": "string",  # Local overlay interfaces table.
    "advertised-subnets": "string",  # Local advertised subnets.
    "loopback-address-block": "ipv4-classnet-host",  # IPv4 address and subnet mask for hub's loopback address, syntax: X.X.X.X/24.
    "loopback-interface": "string",  # Loopback interface.
    "loopback-advertised-subnet": "integer",  # Loopback advertised subnet reference.
    "psksecret": "password-3",  # Pre-shared secret for ADVPN.
    "bgp-as": "user",  # BGP Router AS number, asplain/asdot/asdot+ format.
    "sdwan-zone": "string",  # Reference to created SD-WAN zone.
    "health-checks": "string",  # Underlying health checks.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable Fabric VPN.",
    "sync-mode": "Setting synchronized by fabric or manual.",
    "branch-name": "Branch name.",
    "policy-rule": "Policy creation rule.",
    "vpn-role": "Fabric VPN role.",
    "overlays": "Local overlay interfaces table.",
    "advertised-subnets": "Local advertised subnets.",
    "loopback-address-block": "IPv4 address and subnet mask for hub's loopback address, syntax: X.X.X.X/24.",
    "loopback-interface": "Loopback interface.",
    "loopback-advertised-subnet": "Loopback advertised subnet reference.",
    "psksecret": "Pre-shared secret for ADVPN.",
    "bgp-as": "BGP Router AS number, asplain/asdot/asdot+ format.",
    "sdwan-zone": "Reference to created SD-WAN zone.",
    "health-checks": "Underlying health checks.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "branch-name": {"type": "string", "max_length": 35},
    "loopback-interface": {"type": "string", "max_length": 15},
    "loopback-advertised-subnet": {"type": "integer", "min": 0, "max": 4294967295},
    "sdwan-zone": {"type": "string", "max_length": 35},
    "health-checks": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "overlays": {
        "name": {
            "type": "string",
            "help": "Overlay name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "ipsec-network-id": {
            "type": "integer",
            "help": "VPN gateway network ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "overlay-tunnel-block": {
            "type": "ipv4-classnet-host",
            "help": "IPv4 address and subnet mask for the overlay tunnel , syntax: X.X.X.X/24.",
            "default": "0.0.0.0 0.0.0.0",
        },
        "remote-gw": {
            "type": "ipv4-address-any",
            "help": "IP address of the hub gateway (Set by hub).",
            "default": "0.0.0.0",
        },
        "interface": {
            "type": "string",
            "help": "Underlying interface name.",
            "default": "",
            "max_length": 15,
        },
        "bgp-neighbor": {
            "type": "string",
            "help": "Underlying BGP neighbor entry.",
            "default": "",
            "max_length": 45,
        },
        "overlay-policy": {
            "type": "integer",
            "help": "The overlay policy to allow ADVPN thru traffic.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "bgp-network": {
            "type": "integer",
            "help": "Underlying BGP network.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "route-policy": {
            "type": "integer",
            "help": "Underlying router policy.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "bgp-neighbor-group": {
            "type": "string",
            "help": "Underlying BGP neighbor group entry.",
            "default": "",
            "max_length": 45,
        },
        "bgp-neighbor-range": {
            "type": "integer",
            "help": "Underlying BGP neighbor range entry.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ipsec-phase1": {
            "type": "string",
            "help": "IPsec interface.",
            "default": "",
            "max_length": 35,
        },
        "sdwan-member": {
            "type": "integer",
            "help": "Reference to SD-WAN member entry.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "advertised-subnets": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967294,
        },
        "prefix": {
            "type": "ipv4-classnet",
            "help": "Network prefix.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "access": {
            "type": "option",
            "help": "Access policy direction.",
            "required": True,
            "default": "inbound",
            "options": ["inbound", "bidirectional"],
        },
        "bgp-network": {
            "type": "integer",
            "help": "Underlying BGP network.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "firewall-address": {
            "type": "string",
            "help": "Underlying firewall address.",
            "default": "",
            "max_length": 79,
        },
        "policies": {
            "type": "integer",
            "help": "Underlying policies.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SYNC_MODE = [
    "enable",
    "disable",
]
VALID_BODY_POLICY_RULE = [
    "health-check",
    "manual",
    "auto",
]
VALID_BODY_VPN_ROLE = [
    "hub",
    "spoke",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_fabric_vpn_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/fabric_vpn."""
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


def validate_system_fabric_vpn_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/fabric_vpn object."""
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
    if "sync-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sync-mode",
            payload["sync-mode"],
            VALID_BODY_SYNC_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-rule" in payload:
        is_valid, error = _validate_enum_field(
            "policy-rule",
            payload["policy-rule"],
            VALID_BODY_POLICY_RULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn-role" in payload:
        is_valid, error = _validate_enum_field(
            "vpn-role",
            payload["vpn-role"],
            VALID_BODY_VPN_ROLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_fabric_vpn_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/fabric_vpn."""
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
    if "sync-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sync-mode",
            payload["sync-mode"],
            VALID_BODY_SYNC_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-rule" in payload:
        is_valid, error = _validate_enum_field(
            "policy-rule",
            payload["policy-rule"],
            VALID_BODY_POLICY_RULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn-role" in payload:
        is_valid, error = _validate_enum_field(
            "vpn-role",
            payload["vpn-role"],
            VALID_BODY_VPN_ROLE,
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
    "endpoint": "system/fabric_vpn",
    "category": "cmdb",
    "api_path": "system/fabric-vpn",
    "help": "Setup for self orchestrated fabric auto discovery VPN.",
    "total_fields": 14,
    "required_fields_count": 2,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
