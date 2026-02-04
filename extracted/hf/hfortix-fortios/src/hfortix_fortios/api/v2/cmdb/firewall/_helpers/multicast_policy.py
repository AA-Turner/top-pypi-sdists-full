"""Validation helpers for firewall/multicast_policy - Auto-generated"""

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
    "srcintf",  # Source interface name.
    "dstintf",  # Destination interface name.
    "srcaddr",  # Source address objects.
    "dstaddr",  # Destination address objects.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "name": "",
    "status": "enable",
    "srcintf": "",
    "dstintf": "",
    "snat": "disable",
    "snat-ip": "0.0.0.0",
    "dnat": "0.0.0.0",
    "action": "accept",
    "protocol": 0,
    "start-port": 1,
    "end-port": 65535,
    "utm-status": "disable",
    "ips-sensor": "",
    "logtraffic": "utm",
    "auto-asic-offload": "enable",
    "traffic-shaper": "",
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
    "id": "integer",  # Policy ID ((0 - 4294967294).
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "name": "string",  # Policy name.
    "comments": "var-string",  # Comment.
    "status": "option",  # Enable/disable this policy.
    "srcintf": "string",  # Source interface name.
    "dstintf": "string",  # Destination interface name.
    "srcaddr": "string",  # Source address objects.
    "dstaddr": "string",  # Destination address objects.
    "snat": "option",  # Enable/disable substitution of the outgoing interface IP address for the origina
    "snat-ip": "ipv4-address",  # IPv4 address to be used as the source address for NATed traffic.
    "dnat": "ipv4-address-any",  # IPv4 DNAT address used for multicast destination addresses.
    "action": "option",  # Accept or deny traffic matching the policy.
    "protocol": "integer",  # Integer value for the protocol type as defined by IANA (0 - 255, default = 0).
    "start-port": "integer",  # Integer value for starting TCP/UDP/SCTP destination port in range (1 - 65535, de
    "end-port": "integer",  # Integer value for ending TCP/UDP/SCTP destination port in range (1 - 65535, defa
    "utm-status": "option",  # Enable to add an IPS security profile to the policy.
    "ips-sensor": "string",  # Name of an existing IPS sensor.
    "logtraffic": "option",  # Enable or disable logging. Log all sessions or security profile sessions.
    "auto-asic-offload": "option",  # Enable/disable offloading policy traffic for hardware acceleration.
    "traffic-shaper": "string",  # Traffic shaper to apply to traffic forwarded by the multicast policy.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Policy ID ((0 - 4294967294).",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "name": "Policy name.",
    "comments": "Comment.",
    "status": "Enable/disable this policy.",
    "srcintf": "Source interface name.",
    "dstintf": "Destination interface name.",
    "srcaddr": "Source address objects.",
    "dstaddr": "Destination address objects.",
    "snat": "Enable/disable substitution of the outgoing interface IP address for the original source IP address (called source NAT or SNAT).",
    "snat-ip": "IPv4 address to be used as the source address for NATed traffic.",
    "dnat": "IPv4 DNAT address used for multicast destination addresses.",
    "action": "Accept or deny traffic matching the policy.",
    "protocol": "Integer value for the protocol type as defined by IANA (0 - 255, default = 0).",
    "start-port": "Integer value for starting TCP/UDP/SCTP destination port in range (1 - 65535, default = 1).",
    "end-port": "Integer value for ending TCP/UDP/SCTP destination port in range (1 - 65535, default = 1).",
    "utm-status": "Enable to add an IPS security profile to the policy.",
    "ips-sensor": "Name of an existing IPS sensor.",
    "logtraffic": "Enable or disable logging. Log all sessions or security profile sessions.",
    "auto-asic-offload": "Enable/disable offloading policy traffic for hardware acceleration.",
    "traffic-shaper": "Traffic shaper to apply to traffic forwarded by the multicast policy.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967294},
    "name": {"type": "string", "max_length": 35},
    "srcintf": {"type": "string", "max_length": 35},
    "dstintf": {"type": "string", "max_length": 35},
    "protocol": {"type": "integer", "min": 0, "max": 255},
    "start-port": {"type": "integer", "min": 0, "max": 65535},
    "end-port": {"type": "integer", "min": 0, "max": 65535},
    "ips-sensor": {"type": "string", "max_length": 47},
    "traffic-shaper": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Source address objects.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Destination address objects.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SNAT = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "accept",
    "deny",
]
VALID_BODY_UTM_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_LOGTRAFFIC = [
    "all",
    "utm",
    "disable",
]
VALID_BODY_AUTO_ASIC_OFFLOAD = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_multicast_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/multicast_policy."""
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


def validate_firewall_multicast_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/multicast_policy object."""
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
    if "snat" in payload:
        is_valid, error = _validate_enum_field(
            "snat",
            payload["snat"],
            VALID_BODY_SNAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-status" in payload:
        is_valid, error = _validate_enum_field(
            "utm-status",
            payload["utm-status"],
            VALID_BODY_UTM_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_multicast_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/multicast_policy."""
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
    if "snat" in payload:
        is_valid, error = _validate_enum_field(
            "snat",
            payload["snat"],
            VALID_BODY_SNAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-status" in payload:
        is_valid, error = _validate_enum_field(
            "utm-status",
            payload["utm-status"],
            VALID_BODY_UTM_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
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
    "endpoint": "firewall/multicast_policy",
    "category": "cmdb",
    "api_path": "firewall/multicast-policy",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure multicast NAT policies.",
    "total_fields": 21,
    "required_fields_count": 4,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
