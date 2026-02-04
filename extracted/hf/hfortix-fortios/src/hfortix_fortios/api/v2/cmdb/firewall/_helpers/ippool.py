"""Validation helpers for firewall/ippool - Auto-generated"""

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
    "type": "overload",
    "startip": "0.0.0.0",
    "endip": "0.0.0.0",
    "startport": 5117,
    "endport": 65533,
    "source-startip": "0.0.0.0",
    "source-endip": "0.0.0.0",
    "block-size": 128,
    "port-per-user": 0,
    "num-blocks-per-user": 8,
    "pba-timeout": 30,
    "pba-interim-log": 0,
    "permit-any-host": "disable",
    "arp-reply": "enable",
    "arp-intf": "",
    "associated-interface": "",
    "nat64": "disable",
    "add-nat64-route": "enable",
    "source-prefix6": "::/0",
    "client-prefix-length": 64,
    "tcp-session-quota": 0,
    "udp-session-quota": 0,
    "icmp-session-quota": 0,
    "privileged-port-use-pba": "disable",
    "subnet-broadcast-in-ippool": "",
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
    "name": "string",  # IP pool name.
    "type": "option",  # IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn
    "startip": "ipv4-address-any",  # First IPv4 address (inclusive) in the range for the address pool (format xxx.xxx
    "endip": "ipv4-address-any",  # Final IPv4 address (inclusive) in the range for the address pool (format xxx.xxx
    "startport": "integer",  # First port number (inclusive) in the range for the address pool (1024 - 65535, D
    "endport": "integer",  # Final port number (inclusive) in the range for the address pool (1024 - 65535, D
    "source-startip": "ipv4-address-any",  # First IPv4 address (inclusive) in the range of the source addresses to be transl
    "source-endip": "ipv4-address-any",  # Final IPv4 address (inclusive) in the range of the source addresses to be transl
    "block-size": "integer",  # Number of addresses in a block (64 - 4096, default = 128).
    "port-per-user": "integer",  # Number of port for each user (32 - 60416, default = 0, which is auto).
    "num-blocks-per-user": "integer",  # Number of addresses blocks that can be used by a user (1 to 128, default = 8).
    "pba-timeout": "integer",  # Port block allocation timeout (seconds).
    "pba-interim-log": "integer",  # Port block allocation interim logging interval (600 - 86400 seconds, default = 0
    "permit-any-host": "option",  # Enable/disable fullcone NAT. Accept UDP packets from any host.
    "arp-reply": "option",  # Enable/disable replying to ARP requests when an IP Pool is added to a policy (de
    "arp-intf": "string",  # Select an interface from available options that will reply to ARP requests. (If 
    "associated-interface": "string",  # Associated interface name.
    "comments": "var-string",  # Comment.
    "nat64": "option",  # Enable/disable NAT64.
    "add-nat64-route": "option",  # Enable/disable adding NAT64 route.
    "source-prefix6": "ipv6-network",  # Source IPv6 network to be translated (format = xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxx
    "client-prefix-length": "integer",  # Subnet length of a single deterministic NAT64 client (1 - 128, default = 64).
    "tcp-session-quota": "integer",  # Maximum number of concurrent TCP sessions allowed per client (0 - 2097000, defau
    "udp-session-quota": "integer",  # Maximum number of concurrent UDP sessions allowed per client (0 - 2097000, defau
    "icmp-session-quota": "integer",  # Maximum number of concurrent ICMP sessions allowed per client (0 - 2097000, defa
    "privileged-port-use-pba": "option",  # Enable/disable selection of the external port from the port block allocation for
    "subnet-broadcast-in-ippool": "option",  # Enable/disable inclusion of the subnetwork address and broadcast IP address in t
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "IP pool name.",
    "type": "IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn-resource-allocation (hyperscale vdom only)",
    "startip": "First IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).",
    "endip": "Final IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).",
    "startport": "First port number (inclusive) in the range for the address pool (1024 - 65535, Default: 5117).",
    "endport": "Final port number (inclusive) in the range for the address pool (1024 - 65535, Default: 65533).",
    "source-startip": "First IPv4 address (inclusive) in the range of the source addresses to be translated (format = xxx.xxx.xxx.xxx, default = 0.0.0.0).",
    "source-endip": "Final IPv4 address (inclusive) in the range of the source addresses to be translated (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).",
    "block-size": "Number of addresses in a block (64 - 4096, default = 128).",
    "port-per-user": "Number of port for each user (32 - 60416, default = 0, which is auto).",
    "num-blocks-per-user": "Number of addresses blocks that can be used by a user (1 to 128, default = 8).",
    "pba-timeout": "Port block allocation timeout (seconds).",
    "pba-interim-log": "Port block allocation interim logging interval (600 - 86400 seconds, default = 0 which disables interim logging).",
    "permit-any-host": "Enable/disable fullcone NAT. Accept UDP packets from any host.",
    "arp-reply": "Enable/disable replying to ARP requests when an IP Pool is added to a policy (default = enable).",
    "arp-intf": "Select an interface from available options that will reply to ARP requests. (If blank, any is selected).",
    "associated-interface": "Associated interface name.",
    "comments": "Comment.",
    "nat64": "Enable/disable NAT64.",
    "add-nat64-route": "Enable/disable adding NAT64 route.",
    "source-prefix6": "Source IPv6 network to be translated (format = xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx, default = ::/0).",
    "client-prefix-length": "Subnet length of a single deterministic NAT64 client (1 - 128, default = 64).",
    "tcp-session-quota": "Maximum number of concurrent TCP sessions allowed per client (0 - 2097000, default = 0 which means no limit).",
    "udp-session-quota": "Maximum number of concurrent UDP sessions allowed per client (0 - 2097000, default = 0 which means no limit).",
    "icmp-session-quota": "Maximum number of concurrent ICMP sessions allowed per client (0 - 2097000, default = 0 which means no limit).",
    "privileged-port-use-pba": "Enable/disable selection of the external port from the port block allocation for NAT'ing privileged ports (deafult = disable).",
    "subnet-broadcast-in-ippool": "Enable/disable inclusion of the subnetwork address and broadcast IP address in the NAT64 IP pool.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "startport": {"type": "integer", "min": 1024, "max": 65535},
    "endport": {"type": "integer", "min": 1024, "max": 65535},
    "block-size": {"type": "integer", "min": 64, "max": 4096},
    "port-per-user": {"type": "integer", "min": 32, "max": 60417},
    "num-blocks-per-user": {"type": "integer", "min": 1, "max": 128},
    "pba-timeout": {"type": "integer", "min": 3, "max": 86400},
    "pba-interim-log": {"type": "integer", "min": 600, "max": 86400},
    "arp-intf": {"type": "string", "max_length": 15},
    "associated-interface": {"type": "string", "max_length": 15},
    "client-prefix-length": {"type": "integer", "min": 1, "max": 128},
    "tcp-session-quota": {"type": "integer", "min": 0, "max": 2097000},
    "udp-session-quota": {"type": "integer", "min": 0, "max": 2097000},
    "icmp-session-quota": {"type": "integer", "min": 0, "max": 2097000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "overload",
    "one-to-one",
    "fixed-port-range",
    "port-block-allocation",
]
VALID_BODY_PERMIT_ANY_HOST = [
    "disable",
    "enable",
]
VALID_BODY_ARP_REPLY = [
    "disable",
    "enable",
]
VALID_BODY_NAT64 = [
    "disable",
    "enable",
]
VALID_BODY_ADD_NAT64_ROUTE = [
    "disable",
    "enable",
]
VALID_BODY_PRIVILEGED_PORT_USE_PBA = [
    "disable",
    "enable",
]
VALID_BODY_SUBNET_BROADCAST_IN_IPPOOL = [
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_ippool_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/ippool."""
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


def validate_firewall_ippool_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/ippool object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-any-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-any-host",
            payload["permit-any-host"],
            VALID_BODY_PERMIT_ANY_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arp-reply" in payload:
        is_valid, error = _validate_enum_field(
            "arp-reply",
            payload["arp-reply"],
            VALID_BODY_ARP_REPLY,
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
    if "add-nat64-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-nat64-route",
            payload["add-nat64-route"],
            VALID_BODY_ADD_NAT64_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "privileged-port-use-pba" in payload:
        is_valid, error = _validate_enum_field(
            "privileged-port-use-pba",
            payload["privileged-port-use-pba"],
            VALID_BODY_PRIVILEGED_PORT_USE_PBA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subnet-broadcast-in-ippool" in payload:
        is_valid, error = _validate_enum_field(
            "subnet-broadcast-in-ippool",
            payload["subnet-broadcast-in-ippool"],
            VALID_BODY_SUBNET_BROADCAST_IN_IPPOOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_ippool_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/ippool."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-any-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-any-host",
            payload["permit-any-host"],
            VALID_BODY_PERMIT_ANY_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arp-reply" in payload:
        is_valid, error = _validate_enum_field(
            "arp-reply",
            payload["arp-reply"],
            VALID_BODY_ARP_REPLY,
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
    if "add-nat64-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-nat64-route",
            payload["add-nat64-route"],
            VALID_BODY_ADD_NAT64_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "privileged-port-use-pba" in payload:
        is_valid, error = _validate_enum_field(
            "privileged-port-use-pba",
            payload["privileged-port-use-pba"],
            VALID_BODY_PRIVILEGED_PORT_USE_PBA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subnet-broadcast-in-ippool" in payload:
        is_valid, error = _validate_enum_field(
            "subnet-broadcast-in-ippool",
            payload["subnet-broadcast-in-ippool"],
            VALID_BODY_SUBNET_BROADCAST_IN_IPPOOL,
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
    "endpoint": "firewall/ippool",
    "category": "cmdb",
    "api_path": "firewall/ippool",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure IPv4 IP pools.",
    "total_fields": 27,
    "required_fields_count": 0,
    "fields_with_defaults_count": 26,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
