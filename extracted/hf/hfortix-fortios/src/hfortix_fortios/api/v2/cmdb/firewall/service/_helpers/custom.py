"""Validation helpers for firewall/service/custom - Auto-generated"""

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
    "uuid": "00000000-0000-0000-0000-000000000000",
    "proxy": "disable",
    "category": "",
    "protocol": "TCP/UDP/UDP-Lite/SCTP",
    "helper": "auto",
    "iprange": "",
    "fqdn": "",
    "protocol-number": 0,
    "icmptype": "",
    "icmpcode": "",
    "tcp-portrange": "",
    "udp-portrange": "",
    "udplite-portrange": "",
    "sctp-portrange": "",
    "tcp-halfclose-timer": 0,
    "tcp-halfopen-timer": 0,
    "tcp-timewait-timer": 0,
    "tcp-rst-timer": 0,
    "udp-idle-timer": 0,
    "session-ttl": "",
    "check-reset-range": "default",
    "color": 0,
    "app-service-type": "disable",
    "fabric-object": "disable",
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
    "name": "string",  # Custom service name.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "proxy": "option",  # Enable/disable web proxy service.
    "category": "string",  # Service category.
    "protocol": "option",  # Protocol type based on IANA numbers.
    "helper": "option",  # Helper name.
    "iprange": "user",  # Start and end of the IP range associated with service.
    "fqdn": "string",  # Fully qualified domain name.
    "protocol-number": "integer",  # IP protocol number.
    "icmptype": "integer",  # ICMP type.
    "icmpcode": "integer",  # ICMP code.
    "tcp-portrange": "user",  # Multiple TCP port ranges.
    "udp-portrange": "user",  # Multiple UDP port ranges.
    "udplite-portrange": "user",  # Multiple UDP-Lite port ranges.
    "sctp-portrange": "user",  # Multiple SCTP port ranges.
    "tcp-halfclose-timer": "integer",  # Wait time to close a TCP session waiting for an unanswered FIN packet (1 - 86400
    "tcp-halfopen-timer": "integer",  # Wait time to close a TCP session waiting for an unanswered open session packet (
    "tcp-timewait-timer": "integer",  # Set the length of the TCP TIME-WAIT state in seconds (1 - 300 sec, 0 = default).
    "tcp-rst-timer": "integer",  # Set the length of the TCP CLOSE state in seconds (5 - 300 sec, 0 = default).
    "udp-idle-timer": "integer",  # Number of seconds before an idle UDP/UDP-Lite connection times out (0 - 86400 se
    "session-ttl": "user",  # Session TTL (300 - 2764800, 0 = default).
    "check-reset-range": "option",  # Configure the type of ICMP error message verification.
    "comment": "var-string",  # Comment.
    "color": "integer",  # Color of icon on the GUI.
    "app-service-type": "option",  # Application service type.
    "app-category": "string",  # Application category ID.
    "application": "string",  # Application ID.
    "fabric-object": "option",  # Security Fabric global object setting.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Custom service name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "proxy": "Enable/disable web proxy service.",
    "category": "Service category.",
    "protocol": "Protocol type based on IANA numbers.",
    "helper": "Helper name.",
    "iprange": "Start and end of the IP range associated with service.",
    "fqdn": "Fully qualified domain name.",
    "protocol-number": "IP protocol number.",
    "icmptype": "ICMP type.",
    "icmpcode": "ICMP code.",
    "tcp-portrange": "Multiple TCP port ranges.",
    "udp-portrange": "Multiple UDP port ranges.",
    "udplite-portrange": "Multiple UDP-Lite port ranges.",
    "sctp-portrange": "Multiple SCTP port ranges.",
    "tcp-halfclose-timer": "Wait time to close a TCP session waiting for an unanswered FIN packet (1 - 86400 sec, 0 = default).",
    "tcp-halfopen-timer": "Wait time to close a TCP session waiting for an unanswered open session packet (1 - 86400 sec, 0 = default).",
    "tcp-timewait-timer": "Set the length of the TCP TIME-WAIT state in seconds (1 - 300 sec, 0 = default).",
    "tcp-rst-timer": "Set the length of the TCP CLOSE state in seconds (5 - 300 sec, 0 = default).",
    "udp-idle-timer": "Number of seconds before an idle UDP/UDP-Lite connection times out (0 - 86400 sec, 0 = default).",
    "session-ttl": "Session TTL (300 - 2764800, 0 = default).",
    "check-reset-range": "Configure the type of ICMP error message verification.",
    "comment": "Comment.",
    "color": "Color of icon on the GUI.",
    "app-service-type": "Application service type.",
    "app-category": "Application category ID.",
    "application": "Application ID.",
    "fabric-object": "Security Fabric global object setting.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "category": {"type": "string", "max_length": 63},
    "fqdn": {"type": "string", "max_length": 255},
    "protocol-number": {"type": "integer", "min": 0, "max": 254},
    "icmptype": {"type": "integer", "min": 0, "max": 4294967295},
    "icmpcode": {"type": "integer", "min": 0, "max": 255},
    "tcp-halfclose-timer": {"type": "integer", "min": 0, "max": 86400},
    "tcp-halfopen-timer": {"type": "integer", "min": 0, "max": 86400},
    "tcp-timewait-timer": {"type": "integer", "min": 0, "max": 300},
    "tcp-rst-timer": {"type": "integer", "min": 5, "max": 300},
    "udp-idle-timer": {"type": "integer", "min": 0, "max": 86400},
    "color": {"type": "integer", "min": 0, "max": 32},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "app-category": {
        "id": {
            "type": "integer",
            "help": "Application category id.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "application": {
        "id": {
            "type": "integer",
            "help": "Application id.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_PROTOCOL = [
    "TCP/UDP/UDP-Lite/SCTP",
    "ICMP",
    "ICMP6",
    "IP",
    "HTTP",
    "FTP",
    "CONNECT",
    "SOCKS-TCP",
    "SOCKS-UDP",
    "ALL",
]
VALID_BODY_HELPER = [
    "auto",
    "disable",
    "ftp",
    "tftp",
    "ras",
    "h323",
    "tns",
    "mms",
    "sip",
    "pptp",
    "rtsp",
    "dns-udp",
    "dns-tcp",
    "pmap",
    "rsh",
    "dcerpc",
    "mgcp",
]
VALID_BODY_CHECK_RESET_RANGE = [
    "disable",
    "strict",
    "default",
]
VALID_BODY_APP_SERVICE_TYPE = [
    "disable",
    "app-id",
    "app-category",
]
VALID_BODY_FABRIC_OBJECT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_service_custom_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/service/custom."""
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


def validate_firewall_service_custom_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/service/custom object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "proxy" in payload:
        is_valid, error = _validate_enum_field(
            "proxy",
            payload["proxy"],
            VALID_BODY_PROXY,
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
    if "helper" in payload:
        is_valid, error = _validate_enum_field(
            "helper",
            payload["helper"],
            VALID_BODY_HELPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-reset-range" in payload:
        is_valid, error = _validate_enum_field(
            "check-reset-range",
            payload["check-reset-range"],
            VALID_BODY_CHECK_RESET_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-service-type" in payload:
        is_valid, error = _validate_enum_field(
            "app-service-type",
            payload["app-service-type"],
            VALID_BODY_APP_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-object" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-object",
            payload["fabric-object"],
            VALID_BODY_FABRIC_OBJECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_service_custom_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/service/custom."""
    # Validate enum values using central function
    if "proxy" in payload:
        is_valid, error = _validate_enum_field(
            "proxy",
            payload["proxy"],
            VALID_BODY_PROXY,
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
    if "helper" in payload:
        is_valid, error = _validate_enum_field(
            "helper",
            payload["helper"],
            VALID_BODY_HELPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-reset-range" in payload:
        is_valid, error = _validate_enum_field(
            "check-reset-range",
            payload["check-reset-range"],
            VALID_BODY_CHECK_RESET_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-service-type" in payload:
        is_valid, error = _validate_enum_field(
            "app-service-type",
            payload["app-service-type"],
            VALID_BODY_APP_SERVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-object" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-object",
            payload["fabric-object"],
            VALID_BODY_FABRIC_OBJECT,
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
    "endpoint": "firewall/service/custom",
    "category": "cmdb",
    "api_path": "firewall.service/custom",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure custom services.",
    "total_fields": 28,
    "required_fields_count": 0,
    "fields_with_defaults_count": 25,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
