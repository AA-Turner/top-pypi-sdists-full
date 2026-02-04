"""Validation helpers for firewall/central_snat_map - Auto-generated"""

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
    "srcintf",  # Source interface name from available interfaces.
    "dstintf",  # Destination interface name from available interfaces.
    "orig-addr",  # IPv4 Original address.
    "orig-addr6",  # IPv6 Original address.
    "dst-addr",  # IPv4 Destination address.
    "dst-addr6",  # IPv6 Destination address.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "policyid": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "status": "enable",
    "type": "ipv4",
    "protocol": 0,
    "orig-port": "",
    "nat": "enable",
    "nat46": "disable",
    "nat64": "disable",
    "port-preserve": "enable",
    "port-random": "disable",
    "nat-port": "",
    "dst-port": "",
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
    "policyid": "integer",  # Policy ID.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "status": "option",  # Enable/disable the active status of this policy.
    "type": "option",  # IPv4/IPv6 source NAT.
    "srcintf": "string",  # Source interface name from available interfaces.
    "dstintf": "string",  # Destination interface name from available interfaces.
    "orig-addr": "string",  # IPv4 Original address.
    "orig-addr6": "string",  # IPv6 Original address.
    "dst-addr": "string",  # IPv4 Destination address.
    "dst-addr6": "string",  # IPv6 Destination address.
    "protocol": "integer",  # Integer value for the protocol type (0 - 255).
    "orig-port": "user",  # Original TCP port (1 to 65535, 0 means any port).
    "nat": "option",  # Enable/disable source NAT.
    "nat46": "option",  # Enable/disable NAT46.
    "nat64": "option",  # Enable/disable NAT64.
    "nat-ippool": "string",  # Name of the IP pools to be used to translate addresses from available IP Pools.
    "nat-ippool6": "string",  # IPv6 pools to be used for source NAT.
    "port-preserve": "option",  # Enable/disable preservation of the original source port from source NAT if it ha
    "port-random": "option",  # Enable/disable random source port selection for source NAT.
    "nat-port": "user",  # Translated port or port range (1 to 65535, 0 means any port).
    "dst-port": "user",  # Destination port or port range (1 to 65535, 0 means any port).
    "comments": "var-string",  # Comment.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "policyid": "Policy ID.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "status": "Enable/disable the active status of this policy.",
    "type": "IPv4/IPv6 source NAT.",
    "srcintf": "Source interface name from available interfaces.",
    "dstintf": "Destination interface name from available interfaces.",
    "orig-addr": "IPv4 Original address.",
    "orig-addr6": "IPv6 Original address.",
    "dst-addr": "IPv4 Destination address.",
    "dst-addr6": "IPv6 Destination address.",
    "protocol": "Integer value for the protocol type (0 - 255).",
    "orig-port": "Original TCP port (1 to 65535, 0 means any port).",
    "nat": "Enable/disable source NAT.",
    "nat46": "Enable/disable NAT46.",
    "nat64": "Enable/disable NAT64.",
    "nat-ippool": "Name of the IP pools to be used to translate addresses from available IP Pools.",
    "nat-ippool6": "IPv6 pools to be used for source NAT.",
    "port-preserve": "Enable/disable preservation of the original source port from source NAT if it has not been used.",
    "port-random": "Enable/disable random source port selection for source NAT.",
    "nat-port": "Translated port or port range (1 to 65535, 0 means any port).",
    "dst-port": "Destination port or port range (1 to 65535, 0 means any port).",
    "comments": "Comment.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967295},
    "protocol": {"type": "integer", "min": 0, "max": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dstintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "orig-addr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "orig-addr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dst-addr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dst-addr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "default": "",
            "max_length": 79,
        },
    },
    "nat-ippool": {
        "name": {
            "type": "string",
            "help": "IP pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "nat-ippool6": {
        "name": {
            "type": "string",
            "help": "IPv6 pool name.",
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
VALID_BODY_TYPE = [
    "ipv4",
    "ipv6",
]
VALID_BODY_NAT = [
    "disable",
    "enable",
]
VALID_BODY_NAT46 = [
    "enable",
    "disable",
]
VALID_BODY_NAT64 = [
    "enable",
    "disable",
]
VALID_BODY_PORT_PRESERVE = [
    "enable",
    "disable",
]
VALID_BODY_PORT_RANDOM = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_central_snat_map_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/central_snat_map."""
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


def validate_firewall_central_snat_map_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/central_snat_map object."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat" in payload:
        is_valid, error = _validate_enum_field(
            "nat",
            payload["nat"],
            VALID_BODY_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-preserve" in payload:
        is_valid, error = _validate_enum_field(
            "port-preserve",
            payload["port-preserve"],
            VALID_BODY_PORT_PRESERVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-random" in payload:
        is_valid, error = _validate_enum_field(
            "port-random",
            payload["port-random"],
            VALID_BODY_PORT_RANDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_central_snat_map_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/central_snat_map."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat" in payload:
        is_valid, error = _validate_enum_field(
            "nat",
            payload["nat"],
            VALID_BODY_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-preserve" in payload:
        is_valid, error = _validate_enum_field(
            "port-preserve",
            payload["port-preserve"],
            VALID_BODY_PORT_PRESERVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-random" in payload:
        is_valid, error = _validate_enum_field(
            "port-random",
            payload["port-random"],
            VALID_BODY_PORT_RANDOM,
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
    "endpoint": "firewall/central_snat_map",
    "category": "cmdb",
    "api_path": "firewall/central-snat-map",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure IPv4 and IPv6 central SNAT policies.",
    "total_fields": 22,
    "required_fields_count": 6,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
