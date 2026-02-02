"""Validation helpers for system/link_monitor - Auto-generated"""

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
    "server",  # IP address of the server(s) to be monitored.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "addr-mode": "ipv4",
    "srcintf": "",
    "server-config": "default",
    "server-type": "static",
    "protocol": "ping",
    "port": 0,
    "gateway-ip": "0.0.0.0",
    "gateway-ip6": "::",
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "http-get": "/",
    "http-agent": "Chrome/ Safari/",
    "http-match": "",
    "interval": 500,
    "probe-timeout": 500,
    "failtime": 5,
    "recoverytime": 5,
    "probe-count": 30,
    "security-mode": "none",
    "packet-size": 124,
    "ha-priority": 1,
    "fail-weight": 0,
    "update-cascade-interface": "enable",
    "update-static-route": "enable",
    "update-policy-route": "enable",
    "status": "enable",
    "diffservcode": "",
    "class-id": 0,
    "service-detection": "disable",
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
    "name": "string",  # Link monitor name.
    "addr-mode": "option",  # Address mode (IPv4 or IPv6).
    "srcintf": "string",  # Interface that receives the traffic to be monitored.
    "server-config": "option",  # Mode of server configuration.
    "server-type": "option",  # Server type (static or dynamic).
    "server": "string",  # IP address of the server(s) to be monitored.
    "protocol": "option",  # Protocols used to monitor the server.
    "port": "integer",  # Port number of the traffic to be used to monitor the server.
    "gateway-ip": "ipv4-address-any",  # Gateway IP address used to probe the server.
    "gateway-ip6": "ipv6-address",  # Gateway IPv6 address used to probe the server.
    "route": "string",  # Subnet to monitor.
    "source-ip": "ipv4-address-any",  # Source IP address used in packet to the server.
    "source-ip6": "ipv6-address",  # Source IPv6 address used in packet to the server.
    "http-get": "string",  # If you are monitoring an HTML server you can send an HTTP-GE
    "http-agent": "string",  # String in the http-agent field in the HTTP header.
    "http-match": "string",  # String that you expect to see in the HTTP-GET requests of th
    "interval": "integer",  # Detection interval in milliseconds (20 - 3600 * 1000 msec, d
    "probe-timeout": "integer",  # Time to wait before a probe packet is considered lost (20 - 
    "failtime": "integer",  # Number of retry attempts before the server is considered dow
    "recoverytime": "integer",  # Number of successful responses received before server is con
    "probe-count": "integer",  # Number of most recent probes that should be used to calculat
    "security-mode": "option",  # Twamp controller security mode.
    "password": "password",  # TWAMP controller password in authentication mode.
    "packet-size": "integer",  # Packet size of a TWAMP test session (124/158 - 1024).
    "ha-priority": "integer",  # HA election priority (1 - 50).
    "fail-weight": "integer",  # Threshold weight to trigger link failure alert.
    "update-cascade-interface": "option",  # Enable/disable update cascade interface.
    "update-static-route": "option",  # Enable/disable updating the static route.
    "update-policy-route": "option",  # Enable/disable updating the policy route.
    "status": "option",  # Enable/disable this link monitor.
    "diffservcode": "user",  # Differentiated services code point (DSCP) in the IP header o
    "class-id": "integer",  # Traffic class ID.
    "service-detection": "option",  # Only use monitor to read quality values. If enabled, static 
    "server-list": "string",  # Servers for link-monitor to monitor.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Link monitor name.",
    "addr-mode": "Address mode (IPv4 or IPv6).",
    "srcintf": "Interface that receives the traffic to be monitored.",
    "server-config": "Mode of server configuration.",
    "server-type": "Server type (static or dynamic).",
    "server": "IP address of the server(s) to be monitored.",
    "protocol": "Protocols used to monitor the server.",
    "port": "Port number of the traffic to be used to monitor the server.",
    "gateway-ip": "Gateway IP address used to probe the server.",
    "gateway-ip6": "Gateway IPv6 address used to probe the server.",
    "route": "Subnet to monitor.",
    "source-ip": "Source IP address used in packet to the server.",
    "source-ip6": "Source IPv6 address used in packet to the server.",
    "http-get": "If you are monitoring an HTML server you can send an HTTP-GET request with a custom string. Use this option to define the string.",
    "http-agent": "String in the http-agent field in the HTTP header.",
    "http-match": "String that you expect to see in the HTTP-GET requests of the traffic to be monitored.",
    "interval": "Detection interval in milliseconds (20 - 3600 * 1000 msec, default = 500).",
    "probe-timeout": "Time to wait before a probe packet is considered lost (20 - 5000 msec, default = 500).",
    "failtime": "Number of retry attempts before the server is considered down (1 - 3600, default = 5).",
    "recoverytime": "Number of successful responses received before server is considered recovered (1 - 3600, default = 5).",
    "probe-count": "Number of most recent probes that should be used to calculate latency and jitter (5 - 30, default = 30).",
    "security-mode": "Twamp controller security mode.",
    "password": "TWAMP controller password in authentication mode.",
    "packet-size": "Packet size of a TWAMP test session (124/158 - 1024).",
    "ha-priority": "HA election priority (1 - 50).",
    "fail-weight": "Threshold weight to trigger link failure alert.",
    "update-cascade-interface": "Enable/disable update cascade interface.",
    "update-static-route": "Enable/disable updating the static route.",
    "update-policy-route": "Enable/disable updating the policy route.",
    "status": "Enable/disable this link monitor.",
    "diffservcode": "Differentiated services code point (DSCP) in the IP header of the probe packet.",
    "class-id": "Traffic class ID.",
    "service-detection": "Only use monitor to read quality values. If enabled, static routes and cascade interfaces will not be updated.",
    "server-list": "Servers for link-monitor to monitor.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "srcintf": {"type": "string", "max_length": 15},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "http-get": {"type": "string", "max_length": 1024},
    "http-agent": {"type": "string", "max_length": 1024},
    "http-match": {"type": "string", "max_length": 1024},
    "interval": {"type": "integer", "min": 20, "max": 3600000},
    "probe-timeout": {"type": "integer", "min": 20, "max": 5000},
    "failtime": {"type": "integer", "min": 1, "max": 3600},
    "recoverytime": {"type": "integer", "min": 1, "max": 3600},
    "probe-count": {"type": "integer", "min": 5, "max": 30},
    "packet-size": {"type": "integer", "min": 0, "max": 65535},
    "ha-priority": {"type": "integer", "min": 1, "max": 50},
    "fail-weight": {"type": "integer", "min": 0, "max": 255},
    "class-id": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server": {
        "address": {
            "type": "string",
            "help": "Server address.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "route": {
        "subnet": {
            "type": "string",
            "help": "IP and netmask (x.x.x.x/y).",
            "default": "",
            "max_length": 79,
        },
    },
    "server-list": {
        "id": {
            "type": "integer",
            "help": "Server ID.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 32,
        },
        "dst": {
            "type": "string",
            "help": "IP address of the server to be monitored.",
            "required": True,
            "default": "",
            "max_length": 64,
        },
        "protocol": {
            "type": "option",
            "help": "Protocols used to monitor the server.",
            "default": "ping",
            "options": ["ping", "tcp-echo", "udp-echo", "http", "https", "twamp"],
        },
        "port": {
            "type": "integer",
            "help": "Port number of the traffic to be used to monitor the server.",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "weight": {
            "type": "integer",
            "help": "Weight of the monitor to this dst (0 - 255).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ADDR_MODE = [
    "ipv4",
    "ipv6",
]
VALID_BODY_SERVER_CONFIG = [
    "default",
    "individual",
]
VALID_BODY_SERVER_TYPE = [
    "static",
    "dynamic",
]
VALID_BODY_PROTOCOL = [
    "ping",
    "tcp-echo",
    "udp-echo",
    "http",
    "https",
    "twamp",
]
VALID_BODY_SECURITY_MODE = [
    "none",
    "authentication",
]
VALID_BODY_UPDATE_CASCADE_INTERFACE = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_STATIC_ROUTE = [
    "enable",
    "disable",
]
VALID_BODY_UPDATE_POLICY_ROUTE = [
    "enable",
    "disable",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SERVICE_DETECTION = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_link_monitor_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/link_monitor."""
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


def validate_system_link_monitor_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/link_monitor object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "addr-mode" in payload:
        is_valid, error = _validate_enum_field(
            "addr-mode",
            payload["addr-mode"],
            VALID_BODY_ADDR_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-config" in payload:
        is_valid, error = _validate_enum_field(
            "server-config",
            payload["server-config"],
            VALID_BODY_SERVER_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-cascade-interface" in payload:
        is_valid, error = _validate_enum_field(
            "update-cascade-interface",
            payload["update-cascade-interface"],
            VALID_BODY_UPDATE_CASCADE_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-static-route" in payload:
        is_valid, error = _validate_enum_field(
            "update-static-route",
            payload["update-static-route"],
            VALID_BODY_UPDATE_STATIC_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-policy-route" in payload:
        is_valid, error = _validate_enum_field(
            "update-policy-route",
            payload["update-policy-route"],
            VALID_BODY_UPDATE_POLICY_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-detection" in payload:
        is_valid, error = _validate_enum_field(
            "service-detection",
            payload["service-detection"],
            VALID_BODY_SERVICE_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_link_monitor_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/link_monitor."""
    # Validate enum values using central function
    if "addr-mode" in payload:
        is_valid, error = _validate_enum_field(
            "addr-mode",
            payload["addr-mode"],
            VALID_BODY_ADDR_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-config" in payload:
        is_valid, error = _validate_enum_field(
            "server-config",
            payload["server-config"],
            VALID_BODY_SERVER_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-cascade-interface" in payload:
        is_valid, error = _validate_enum_field(
            "update-cascade-interface",
            payload["update-cascade-interface"],
            VALID_BODY_UPDATE_CASCADE_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-static-route" in payload:
        is_valid, error = _validate_enum_field(
            "update-static-route",
            payload["update-static-route"],
            VALID_BODY_UPDATE_STATIC_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-policy-route" in payload:
        is_valid, error = _validate_enum_field(
            "update-policy-route",
            payload["update-policy-route"],
            VALID_BODY_UPDATE_POLICY_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-detection" in payload:
        is_valid, error = _validate_enum_field(
            "service-detection",
            payload["service-detection"],
            VALID_BODY_SERVICE_DETECTION,
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
    "endpoint": "system/link_monitor",
    "category": "cmdb",
    "api_path": "system/link-monitor",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Link Health Monitor.",
    "total_fields": 34,
    "required_fields_count": 1,
    "fields_with_defaults_count": 30,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
