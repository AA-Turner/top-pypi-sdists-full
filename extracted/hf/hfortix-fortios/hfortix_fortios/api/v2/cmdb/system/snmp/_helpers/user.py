"""Validation helpers for system/snmp/user - Auto-generated"""

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
    "name",  # SNMP user name.
    "auth-pwd",  # Password for authentication protocol.
    "priv-pwd",  # Password for privacy (encryption) protocol.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "status": "enable",
    "trap-status": "enable",
    "trap-lport": 162,
    "trap-rport": 162,
    "queries": "enable",
    "query-port": 161,
    "notify-hosts": "",
    "notify-hosts6": "",
    "source-ip": "0.0.0.0",
    "source-ipv6": "::",
    "ha-direct": "disable",
    "events": "cpu-high mem-low log-full intf-ip vpn-tun-up vpn-tun-down ha-switch ha-hb-failure ips-signature ips-anomaly av-virus av-oversize av-pattern av-fragmented fm-if-change bgp-established bgp-backward-transition ha-member-up ha-member-down ent-conf-change av-conserve av-bypass av-oversize-passed av-oversize-blocked ips-pkg-update ips-fail-open faz-disconnect faz wc-ap-up wc-ap-down fswctl-session-up fswctl-session-down load-balance-real-server-down per-cpu-high dhcp pool-usage ippool interface ospf-nbr-state-change ospf-virtnbr-state-change bfd",
    "mib-view": "",
    "security-level": "no-auth-no-priv",
    "auth-proto": "sha",
    "priv-proto": "aes",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "name": "string",  # SNMP user name.
    "status": "option",  # Enable/disable this SNMP user.
    "trap-status": "option",  # Enable/disable traps for this SNMP user.
    "trap-lport": "integer",  # SNMPv3 local trap port (default = 162).
    "trap-rport": "integer",  # SNMPv3 trap remote port (default = 162).
    "queries": "option",  # Enable/disable SNMP queries for this user.
    "query-port": "integer",  # SNMPv3 query port (default = 161).
    "notify-hosts": "ipv4-address",  # SNMP managers to send notifications (traps) to.
    "notify-hosts6": "ipv6-address",  # IPv6 SNMP managers to send notifications (traps) to.
    "source-ip": "ipv4-address",  # Source IP for SNMP trap.
    "source-ipv6": "ipv6-address",  # Source IPv6 for SNMP trap.
    "ha-direct": "option",  # Enable/disable direct management of HA cluster members.
    "events": "option",  # SNMP notifications (traps) to send.
    "mib-view": "string",  # SNMP access control MIB view.
    "vdoms": "string",  # SNMP access control VDOMs.
    "security-level": "option",  # Security level for message authentication and encryption.
    "auth-proto": "option",  # Authentication protocol.
    "auth-pwd": "password",  # Password for authentication protocol.
    "priv-proto": "option",  # Privacy (encryption) protocol.
    "priv-pwd": "password",  # Password for privacy (encryption) protocol.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "SNMP user name.",
    "status": "Enable/disable this SNMP user.",
    "trap-status": "Enable/disable traps for this SNMP user.",
    "trap-lport": "SNMPv3 local trap port (default = 162).",
    "trap-rport": "SNMPv3 trap remote port (default = 162).",
    "queries": "Enable/disable SNMP queries for this user.",
    "query-port": "SNMPv3 query port (default = 161).",
    "notify-hosts": "SNMP managers to send notifications (traps) to.",
    "notify-hosts6": "IPv6 SNMP managers to send notifications (traps) to.",
    "source-ip": "Source IP for SNMP trap.",
    "source-ipv6": "Source IPv6 for SNMP trap.",
    "ha-direct": "Enable/disable direct management of HA cluster members.",
    "events": "SNMP notifications (traps) to send.",
    "mib-view": "SNMP access control MIB view.",
    "vdoms": "SNMP access control VDOMs.",
    "security-level": "Security level for message authentication and encryption.",
    "auth-proto": "Authentication protocol.",
    "auth-pwd": "Password for authentication protocol.",
    "priv-proto": "Privacy (encryption) protocol.",
    "priv-pwd": "Password for privacy (encryption) protocol.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 32},
    "trap-lport": {"type": "integer", "min": 1, "max": 65535},
    "trap-rport": {"type": "integer", "min": 1, "max": 65535},
    "query-port": {"type": "integer", "min": 1, "max": 65535},
    "mib-view": {"type": "string", "max_length": 32},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
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
VALID_BODY_TRAP_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_QUERIES = [
    "enable",
    "disable",
]
VALID_BODY_HA_DIRECT = [
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
VALID_BODY_SECURITY_LEVEL = [
    "no-auth-no-priv",
    "auth-no-priv",
    "auth-priv",
]
VALID_BODY_AUTH_PROTO = [
    "md5",
    "sha",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
]
VALID_BODY_PRIV_PROTO = [
    "aes",
    "des",
    "aes256",
    "aes256cisco",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_snmp_user_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/snmp/user."""
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


def validate_system_snmp_user_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/snmp/user object."""
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
    if "trap-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-status",
            payload["trap-status"],
            VALID_BODY_TRAP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "queries" in payload:
        is_valid, error = _validate_enum_field(
            "queries",
            payload["queries"],
            VALID_BODY_QUERIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-direct" in payload:
        is_valid, error = _validate_enum_field(
            "ha-direct",
            payload["ha-direct"],
            VALID_BODY_HA_DIRECT,
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
    if "security-level" in payload:
        is_valid, error = _validate_enum_field(
            "security-level",
            payload["security-level"],
            VALID_BODY_SECURITY_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-proto" in payload:
        is_valid, error = _validate_enum_field(
            "auth-proto",
            payload["auth-proto"],
            VALID_BODY_AUTH_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priv-proto" in payload:
        is_valid, error = _validate_enum_field(
            "priv-proto",
            payload["priv-proto"],
            VALID_BODY_PRIV_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_snmp_user_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/snmp/user."""
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
    if "trap-status" in payload:
        is_valid, error = _validate_enum_field(
            "trap-status",
            payload["trap-status"],
            VALID_BODY_TRAP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "queries" in payload:
        is_valid, error = _validate_enum_field(
            "queries",
            payload["queries"],
            VALID_BODY_QUERIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-direct" in payload:
        is_valid, error = _validate_enum_field(
            "ha-direct",
            payload["ha-direct"],
            VALID_BODY_HA_DIRECT,
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
    if "security-level" in payload:
        is_valid, error = _validate_enum_field(
            "security-level",
            payload["security-level"],
            VALID_BODY_SECURITY_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-proto" in payload:
        is_valid, error = _validate_enum_field(
            "auth-proto",
            payload["auth-proto"],
            VALID_BODY_AUTH_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priv-proto" in payload:
        is_valid, error = _validate_enum_field(
            "priv-proto",
            payload["priv-proto"],
            VALID_BODY_PRIV_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
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
    "endpoint": "system/snmp/user",
    "category": "cmdb",
    "api_path": "system.snmp/user",
    "mkey": "name",
    "mkey_type": "string",
    "help": "SNMP user configuration.",
    "total_fields": 23,
    "required_fields_count": 4,
    "fields_with_defaults_count": 20,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
