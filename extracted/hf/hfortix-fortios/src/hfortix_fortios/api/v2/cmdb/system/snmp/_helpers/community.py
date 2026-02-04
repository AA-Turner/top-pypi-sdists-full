"""Validation helpers for system/snmp/community - Auto-generated"""

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
    "name",  # Community name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "name": "",
    "status": "enable",
    "query-v1-status": "enable",
    "query-v1-port": 161,
    "query-v2c-status": "enable",
    "query-v2c-port": 161,
    "trap-v1-status": "enable",
    "trap-v1-lport": 162,
    "trap-v1-rport": 162,
    "trap-v2c-status": "enable",
    "trap-v2c-lport": 162,
    "trap-v2c-rport": 162,
    "events": "cpu-high mem-low log-full intf-ip vpn-tun-up vpn-tun-down ha-switch ha-hb-failure ips-signature ips-anomaly av-virus av-oversize av-pattern av-fragmented fm-if-change bgp-established bgp-backward-transition ha-member-up ha-member-down ent-conf-change av-conserve av-bypass av-oversize-passed av-oversize-blocked ips-pkg-update ips-fail-open faz-disconnect faz wc-ap-up wc-ap-down fswctl-session-up fswctl-session-down load-balance-real-server-down per-cpu-high dhcp pool-usage ippool interface ospf-nbr-state-change ospf-virtnbr-state-change bfd",
    "mib-view": "",
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
    "id": "integer",  # Community ID.
    "name": "string",  # Community name.
    "status": "option",  # Enable/disable this SNMP community.
    "hosts": "string",  # Configure IPv4 SNMP managers (hosts).
    "hosts6": "string",  # Configure IPv6 SNMP managers.
    "query-v1-status": "option",  # Enable/disable SNMP v1 queries.
    "query-v1-port": "integer",  # SNMP v1 query port (default = 161).
    "query-v2c-status": "option",  # Enable/disable SNMP v2c queries.
    "query-v2c-port": "integer",  # SNMP v2c query port (default = 161).
    "trap-v1-status": "option",  # Enable/disable SNMP v1 traps.
    "trap-v1-lport": "integer",  # SNMP v1 trap local port (default = 162).
    "trap-v1-rport": "integer",  # SNMP v1 trap remote port (default = 162).
    "trap-v2c-status": "option",  # Enable/disable SNMP v2c traps.
    "trap-v2c-lport": "integer",  # SNMP v2c trap local port (default = 162).
    "trap-v2c-rport": "integer",  # SNMP v2c trap remote port (default = 162).
    "events": "option",  # SNMP trap events.
    "mib-view": "string",  # SNMP access control MIB view.
    "vdoms": "string",  # SNMP access control VDOMs.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "Community ID.",
    "name": "Community name.",
    "status": "Enable/disable this SNMP community.",
    "hosts": "Configure IPv4 SNMP managers (hosts).",
    "hosts6": "Configure IPv6 SNMP managers.",
    "query-v1-status": "Enable/disable SNMP v1 queries.",
    "query-v1-port": "SNMP v1 query port (default = 161).",
    "query-v2c-status": "Enable/disable SNMP v2c queries.",
    "query-v2c-port": "SNMP v2c query port (default = 161).",
    "trap-v1-status": "Enable/disable SNMP v1 traps.",
    "trap-v1-lport": "SNMP v1 trap local port (default = 162).",
    "trap-v1-rport": "SNMP v1 trap remote port (default = 162).",
    "trap-v2c-status": "Enable/disable SNMP v2c traps.",
    "trap-v2c-lport": "SNMP v2c trap local port (default = 162).",
    "trap-v2c-rport": "SNMP v2c trap remote port (default = 162).",
    "events": "SNMP trap events.",
    "mib-view": "SNMP access control MIB view.",
    "vdoms": "SNMP access control VDOMs.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 35},
    "query-v1-port": {"type": "integer", "min": 1, "max": 65535},
    "query-v2c-port": {"type": "integer", "min": 0, "max": 65535},
    "trap-v1-lport": {"type": "integer", "min": 1, "max": 65535},
    "trap-v1-rport": {"type": "integer", "min": 1, "max": 65535},
    "trap-v2c-lport": {"type": "integer", "min": 1, "max": 65535},
    "trap-v2c-rport": {"type": "integer", "min": 1, "max": 65535},
    "mib-view": {"type": "string", "max_length": 32},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "hosts": {
        "id": {
            "type": "integer",
            "help": "Host entry ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "source-ip": {
            "type": "ipv4-address",
            "help": "Source IPv4 address for SNMP traps.",
            "default": "0.0.0.0",
        },
        "ip": {
            "type": "user",
            "help": "IPv4 address of the SNMP manager (host).",
            "required": True,
            "default": "",
        },
        "ha-direct": {
            "type": "option",
            "help": "Enable/disable direct management of HA cluster members.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "host-type": {
            "type": "option",
            "help": "Control whether the SNMP manager sends SNMP queries, receives SNMP traps, or both. No traps will be sent when IP type is subnet.",
            "default": "any",
            "options": ["any", "query", "trap"],
        },
        "interface-select-method": {
            "type": "option",
            "help": "Specify how to select outgoing interface to reach server.",
            "default": "auto",
            "options": ["auto", "sdwan", "specify"],
        },
        "interface": {
            "type": "string",
            "help": "Specify outgoing interface to reach server.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "vrf-select": {
            "type": "integer",
            "help": "VRF ID used for connection to server.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
    },
    "hosts6": {
        "id": {
            "type": "integer",
            "help": "Host6 entry ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "source-ipv6": {
            "type": "ipv6-address",
            "help": "Source IPv6 address for SNMP traps.",
            "default": "::",
        },
        "ipv6": {
            "type": "ipv6-prefix",
            "help": "SNMP manager IPv6 address prefix.",
            "required": True,
            "default": "::/0",
        },
        "ha-direct": {
            "type": "option",
            "help": "Enable/disable direct management of HA cluster members.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "host-type": {
            "type": "option",
            "help": "Control whether the SNMP manager sends SNMP queries, receives SNMP traps, or both.",
            "default": "any",
            "options": ["any", "query", "trap"],
        },
        "interface-select-method": {
            "type": "option",
            "help": "Specify how to select outgoing interface to reach server.",
            "default": "auto",
            "options": ["auto", "sdwan", "specify"],
        },
        "interface": {
            "type": "string",
            "help": "Specify outgoing interface to reach server.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "vrf-select": {
            "type": "integer",
            "help": "VRF ID used for connection to server.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
    },
    "vdoms": {
        "name": {
            "type": "string",
            "help": "VDOM name.",
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
VALID_BODY_QUERY_V1_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_QUERY_V2C_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TRAP_V1_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TRAP_V2C_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_EVENTS = [
    "cpu-high",
    "mem-low",
    "log-full",
    "intf-ip",
    "vpn-tun-up",
    "vpn-tun-down",
    "ha-switch",
    "ha-hb-failure",
    "ips-signature",
    "ips-anomaly",
    "av-virus",
    "av-oversize",
    "av-pattern",
    "av-fragmented",
    "fm-if-change",
    "fm-conf-change",
    "bgp-established",
    "bgp-backward-transition",
    "ha-member-up",
    "ha-member-down",
    "ent-conf-change",
    "av-conserve",
    "av-bypass",
    "av-oversize-passed",
    "av-oversize-blocked",
    "ips-pkg-update",
    "ips-fail-open",
    "faz-disconnect",
    "faz",
    "wc-ap-up",
    "wc-ap-down",
    "fswctl-session-up",
    "fswctl-session-down",
    "load-balance-real-server-down",
    "device-new",
    "per-cpu-high",
    "dhcp",
    "pool-usage",
    "ippool",
    "interface",
    "ospf-nbr-state-change",
    "ospf-virtnbr-state-change",
    "bfd",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_snmp_community_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/snmp/community."""
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


def validate_system_snmp_community_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/snmp/community object."""
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
    if "query-v1-status" in payload:
        is_valid, error = _validate_enum_field(
            "query-v1-status",
            payload["query-v1-status"],
            VALID_BODY_QUERY_V1_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "query-v2c-status" in payload:
        is_valid, error = _validate_enum_field(
            "query-v2c-status",
            payload["query-v2c-status"],
            VALID_BODY_QUERY_V2C_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trap-v1-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-v1-status",
            payload["trap-v1-status"],
            VALID_BODY_TRAP_V1_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trap-v2c-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-v2c-status",
            payload["trap-v2c-status"],
            VALID_BODY_TRAP_V2C_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "events" in payload:
        is_valid, error = _validate_enum_field(
            "events",
            payload["events"],
            VALID_BODY_EVENTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_snmp_community_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/snmp/community."""
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
    if "query-v1-status" in payload:
        is_valid, error = _validate_enum_field(
            "query-v1-status",
            payload["query-v1-status"],
            VALID_BODY_QUERY_V1_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "query-v2c-status" in payload:
        is_valid, error = _validate_enum_field(
            "query-v2c-status",
            payload["query-v2c-status"],
            VALID_BODY_QUERY_V2C_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trap-v1-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-v1-status",
            payload["trap-v1-status"],
            VALID_BODY_TRAP_V1_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trap-v2c-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-v2c-status",
            payload["trap-v2c-status"],
            VALID_BODY_TRAP_V2C_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "events" in payload:
        is_valid, error = _validate_enum_field(
            "events",
            payload["events"],
            VALID_BODY_EVENTS,
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
    "endpoint": "system/snmp/community",
    "category": "cmdb",
    "api_path": "system.snmp/community",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "SNMP community configuration.",
    "total_fields": 18,
    "required_fields_count": 1,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
