"""Validation helpers for system/resource_limits - Auto-generated"""

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
    "log-disk-quota": 0,
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
    "session": "integer",  # Maximum number of sessions.
    "ipsec-phase1": "integer",  # Maximum number of VPN IPsec phase1 tunnels.
    "ipsec-phase2": "integer",  # Maximum number of VPN IPsec phase2 tunnels.
    "ipsec-phase1-interface": "integer",  # Maximum number of VPN IPsec phase1 interface tunnels.
    "ipsec-phase2-interface": "integer",  # Maximum number of VPN IPsec phase2 interface tunnels.
    "dialup-tunnel": "integer",  # Maximum number of dial-up tunnels.
    "firewall-policy": "integer",  # Maximum number of firewall policies (policy, DoS-policy4, DoS-policy6, multicast
    "firewall-address": "integer",  # Maximum number of firewall addresses (IPv4, IPv6, multicast).
    "firewall-addrgrp": "integer",  # Maximum number of firewall address groups (IPv4, IPv6).
    "custom-service": "integer",  # Maximum number of firewall custom services.
    "service-group": "integer",  # Maximum number of firewall service groups.
    "onetime-schedule": "integer",  # Maximum number of firewall one-time schedules.
    "recurring-schedule": "integer",  # Maximum number of firewall recurring schedules.
    "user": "integer",  # Maximum number of local users.
    "user-group": "integer",  # Maximum number of user groups.
    "sslvpn": "integer",  # Maximum number of Agentless VPN.
    "proxy": "integer",  # Maximum number of concurrent proxy users.
    "log-disk-quota": "integer",  # Log disk quota in megabytes (MB).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "session": "Maximum number of sessions.",
    "ipsec-phase1": "Maximum number of VPN IPsec phase1 tunnels.",
    "ipsec-phase2": "Maximum number of VPN IPsec phase2 tunnels.",
    "ipsec-phase1-interface": "Maximum number of VPN IPsec phase1 interface tunnels.",
    "ipsec-phase2-interface": "Maximum number of VPN IPsec phase2 interface tunnels.",
    "dialup-tunnel": "Maximum number of dial-up tunnels.",
    "firewall-policy": "Maximum number of firewall policies (policy, DoS-policy4, DoS-policy6, multicast).",
    "firewall-address": "Maximum number of firewall addresses (IPv4, IPv6, multicast).",
    "firewall-addrgrp": "Maximum number of firewall address groups (IPv4, IPv6).",
    "custom-service": "Maximum number of firewall custom services.",
    "service-group": "Maximum number of firewall service groups.",
    "onetime-schedule": "Maximum number of firewall one-time schedules.",
    "recurring-schedule": "Maximum number of firewall recurring schedules.",
    "user": "Maximum number of local users.",
    "user-group": "Maximum number of user groups.",
    "sslvpn": "Maximum number of Agentless VPN.",
    "proxy": "Maximum number of concurrent proxy users.",
    "log-disk-quota": "Log disk quota in megabytes (MB).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "session": {"type": "integer", "min": 0, "max": 4294967295},
    "ipsec-phase1": {"type": "integer", "min": 0, "max": 4294967295},
    "ipsec-phase2": {"type": "integer", "min": 0, "max": 4294967295},
    "ipsec-phase1-interface": {"type": "integer", "min": 0, "max": 4294967295},
    "ipsec-phase2-interface": {"type": "integer", "min": 0, "max": 4294967295},
    "dialup-tunnel": {"type": "integer", "min": 0, "max": 4294967295},
    "firewall-policy": {"type": "integer", "min": 0, "max": 4294967295},
    "firewall-address": {"type": "integer", "min": 0, "max": 4294967295},
    "firewall-addrgrp": {"type": "integer", "min": 0, "max": 4294967295},
    "custom-service": {"type": "integer", "min": 0, "max": 4294967295},
    "service-group": {"type": "integer", "min": 0, "max": 4294967295},
    "onetime-schedule": {"type": "integer", "min": 0, "max": 4294967295},
    "recurring-schedule": {"type": "integer", "min": 0, "max": 4294967295},
    "user": {"type": "integer", "min": 0, "max": 4294967295},
    "user-group": {"type": "integer", "min": 0, "max": 4294967295},
    "sslvpn": {"type": "integer", "min": 0, "max": 4294967295},
    "proxy": {"type": "integer", "min": 0, "max": 4294967295},
    "log-disk-quota": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_resource_limits_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/resource_limits."""
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


def validate_system_resource_limits_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/resource_limits object."""
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


def validate_system_resource_limits_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/resource_limits."""
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
    "endpoint": "system/resource_limits",
    "category": "cmdb",
    "api_path": "system/resource-limits",
    "help": "Configure resource limits.",
    "total_fields": 18,
    "required_fields_count": 0,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
