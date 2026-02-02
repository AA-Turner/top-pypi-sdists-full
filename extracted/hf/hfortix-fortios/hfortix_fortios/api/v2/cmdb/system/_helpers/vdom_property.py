"""Validation helpers for system/vdom_property - Auto-generated"""

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
    "description": "",
    "snmp-index": 0,
    "session": "",
    "ipsec-phase1": "",
    "ipsec-phase2": "",
    "ipsec-phase1-interface": "",
    "ipsec-phase2-interface": "",
    "dialup-tunnel": "",
    "firewall-policy": "",
    "firewall-address": "",
    "firewall-addrgrp": "",
    "custom-service": "",
    "service-group": "",
    "onetime-schedule": "",
    "recurring-schedule": "",
    "user": "",
    "user-group": "",
    "sslvpn": "",
    "proxy": "",
    "log-disk-quota": "",
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
    "name": "string",  # VDOM name.
    "description": "string",  # Description.
    "snmp-index": "integer",  # Permanent SNMP Index of the virtual domain (1 - 2147483647).
    "session": "user",  # Maximum guaranteed number of sessions.
    "ipsec-phase1": "user",  # Maximum guaranteed number of VPN IPsec phase 1 tunnels.
    "ipsec-phase2": "user",  # Maximum guaranteed number of VPN IPsec phase 2 tunnels.
    "ipsec-phase1-interface": "user",  # Maximum guaranteed number of VPN IPsec phase1 interface tunn
    "ipsec-phase2-interface": "user",  # Maximum guaranteed number of VPN IPsec phase2 interface tunn
    "dialup-tunnel": "user",  # Maximum guaranteed number of dial-up tunnels.
    "firewall-policy": "user",  # Maximum guaranteed number of firewall policies (policy, DoS-
    "firewall-address": "user",  # Maximum guaranteed number of firewall addresses (IPv4, IPv6,
    "firewall-addrgrp": "user",  # Maximum guaranteed number of firewall address groups (IPv4, 
    "custom-service": "user",  # Maximum guaranteed number of firewall custom services.
    "service-group": "user",  # Maximum guaranteed number of firewall service groups.
    "onetime-schedule": "user",  # Maximum guaranteed number of firewall one-time schedules..
    "recurring-schedule": "user",  # Maximum guaranteed number of firewall recurring schedules.
    "user": "user",  # Maximum guaranteed number of local users.
    "user-group": "user",  # Maximum guaranteed number of user groups.
    "sslvpn": "user",  # Maximum guaranteed number of Agentless VPNs.
    "proxy": "user",  # Maximum guaranteed number of concurrent proxy users.
    "log-disk-quota": "user",  # Log disk quota in megabytes (MB). Range depends on how much 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "VDOM name.",
    "description": "Description.",
    "snmp-index": "Permanent SNMP Index of the virtual domain (1 - 2147483647).",
    "session": "Maximum guaranteed number of sessions.",
    "ipsec-phase1": "Maximum guaranteed number of VPN IPsec phase 1 tunnels.",
    "ipsec-phase2": "Maximum guaranteed number of VPN IPsec phase 2 tunnels.",
    "ipsec-phase1-interface": "Maximum guaranteed number of VPN IPsec phase1 interface tunnels.",
    "ipsec-phase2-interface": "Maximum guaranteed number of VPN IPsec phase2 interface tunnels.",
    "dialup-tunnel": "Maximum guaranteed number of dial-up tunnels.",
    "firewall-policy": "Maximum guaranteed number of firewall policies (policy, DoS-policy4, DoS-policy6, multicast).",
    "firewall-address": "Maximum guaranteed number of firewall addresses (IPv4, IPv6, multicast).",
    "firewall-addrgrp": "Maximum guaranteed number of firewall address groups (IPv4, IPv6).",
    "custom-service": "Maximum guaranteed number of firewall custom services.",
    "service-group": "Maximum guaranteed number of firewall service groups.",
    "onetime-schedule": "Maximum guaranteed number of firewall one-time schedules..",
    "recurring-schedule": "Maximum guaranteed number of firewall recurring schedules.",
    "user": "Maximum guaranteed number of local users.",
    "user-group": "Maximum guaranteed number of user groups.",
    "sslvpn": "Maximum guaranteed number of Agentless VPNs.",
    "proxy": "Maximum guaranteed number of concurrent proxy users.",
    "log-disk-quota": "Log disk quota in megabytes (MB). Range depends on how much disk space is available.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 31},
    "description": {"type": "string", "max_length": 127},
    "snmp-index": {"type": "integer", "min": 1, "max": 2147483647},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_vdom_property_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/vdom_property."""
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


def validate_system_vdom_property_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/vdom_property object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_vdom_property_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/vdom_property."""
    # Validate enum values using central function

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
    "endpoint": "system/vdom_property",
    "category": "cmdb",
    "api_path": "system/vdom-property",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VDOM property.",
    "total_fields": 21,
    "required_fields_count": 0,
    "fields_with_defaults_count": 21,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
