"""Validation helpers for system/dns - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "primary": "0.0.0.0",
    "secondary": "0.0.0.0",
    "protocol": "cleartext",
    "ssl-certificate": "Fortinet_Factory",
    "ip6-primary": "::",
    "ip6-secondary": "::",
    "timeout": 5,
    "retry": 2,
    "dns-cache-limit": 5000,
    "dns-cache-ttl": 1800,
    "cache-notfound-responses": "disable",
    "source-ip": "0.0.0.0",
    "source-ip-interface": "",
    "root-servers": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
    "server-select-method": "least-rtt",
    "alt-primary": "0.0.0.0",
    "alt-secondary": "0.0.0.0",
    "log": "disable",
    "fqdn-cache-ttl": 0,
    "fqdn-max-refresh": 3600,
    "fqdn-min-refresh": 60,
    "hostname-ttl": 86400,
    "hostname-limit": 5000,
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
    "primary": "ipv4-address",  # Primary DNS server IP address.
    "secondary": "ipv4-address",  # Secondary DNS server IP address.
    "protocol": "option",  # DNS transport protocols.
    "ssl-certificate": "string",  # Name of local certificate for SSL connections.
    "server-hostname": "string",  # DNS server host name list.
    "domain": "string",  # Search suffix list for hostname lookup.
    "ip6-primary": "ipv6-address",  # Primary DNS server IPv6 address.
    "ip6-secondary": "ipv6-address",  # Secondary DNS server IPv6 address.
    "timeout": "integer",  # DNS query timeout interval in seconds (1 - 10).
    "retry": "integer",  # Number of times to retry (0 - 5).
    "dns-cache-limit": "integer",  # Maximum number of records in the DNS cache.
    "dns-cache-ttl": "integer",  # Duration in seconds that the DNS cache retains information.
    "cache-notfound-responses": "option",  # Enable/disable response from the DNS server when a record is
    "source-ip": "ipv4-address",  # IP address used by the DNS server as its source IP.
    "source-ip-interface": "string",  # IP address of the specified interface as the source IP addre
    "root-servers": "user",  # Configure up to two preferred servers that serve the DNS roo
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
    "server-select-method": "option",  # Specify how configured servers are prioritized.
    "alt-primary": "ipv4-address",  # Alternate primary DNS server. This is not used as a failover
    "alt-secondary": "ipv4-address",  # Alternate secondary DNS server. This is not used as a failov
    "log": "option",  # Local DNS log setting.
    "fqdn-cache-ttl": "integer",  # FQDN cache time to live in seconds (0 - 86400, default = 0).
    "fqdn-max-refresh": "integer",  # FQDN cache maximum refresh time in seconds (3600 - 86400, de
    "fqdn-min-refresh": "integer",  # FQDN cache minimum refresh time in seconds (10 - 3600, defau
    "hostname-ttl": "integer",  # TTL of hostname table entries (60 - 86400).
    "hostname-limit": "integer",  # Limit of the number of hostname table entries (0 - 50000).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "primary": "Primary DNS server IP address.",
    "secondary": "Secondary DNS server IP address.",
    "protocol": "DNS transport protocols.",
    "ssl-certificate": "Name of local certificate for SSL connections.",
    "server-hostname": "DNS server host name list.",
    "domain": "Search suffix list for hostname lookup.",
    "ip6-primary": "Primary DNS server IPv6 address.",
    "ip6-secondary": "Secondary DNS server IPv6 address.",
    "timeout": "DNS query timeout interval in seconds (1 - 10).",
    "retry": "Number of times to retry (0 - 5).",
    "dns-cache-limit": "Maximum number of records in the DNS cache.",
    "dns-cache-ttl": "Duration in seconds that the DNS cache retains information.",
    "cache-notfound-responses": "Enable/disable response from the DNS server when a record is not in cache.",
    "source-ip": "IP address used by the DNS server as its source IP.",
    "source-ip-interface": "IP address of the specified interface as the source IP address.",
    "root-servers": "Configure up to two preferred servers that serve the DNS root zone (default uses all 13 root servers).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
    "server-select-method": "Specify how configured servers are prioritized.",
    "alt-primary": "Alternate primary DNS server. This is not used as a failover DNS server.",
    "alt-secondary": "Alternate secondary DNS server. This is not used as a failover DNS server.",
    "log": "Local DNS log setting.",
    "fqdn-cache-ttl": "FQDN cache time to live in seconds (0 - 86400, default = 0).",
    "fqdn-max-refresh": "FQDN cache maximum refresh time in seconds (3600 - 86400, default = 3600).",
    "fqdn-min-refresh": "FQDN cache minimum refresh time in seconds (10 - 3600, default = 60).",
    "hostname-ttl": "TTL of hostname table entries (60 - 86400).",
    "hostname-limit": "Limit of the number of hostname table entries (0 - 50000).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "ssl-certificate": {"type": "string", "max_length": 35},
    "timeout": {"type": "integer", "min": 1, "max": 10},
    "retry": {"type": "integer", "min": 0, "max": 5},
    "dns-cache-limit": {"type": "integer", "min": 0, "max": 4294967295},
    "dns-cache-ttl": {"type": "integer", "min": 60, "max": 86400},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
    "fqdn-cache-ttl": {"type": "integer", "min": 0, "max": 86400},
    "fqdn-max-refresh": {"type": "integer", "min": 3600, "max": 86400},
    "fqdn-min-refresh": {"type": "integer", "min": 10, "max": 3600},
    "hostname-ttl": {"type": "integer", "min": 60, "max": 86400},
    "hostname-limit": {"type": "integer", "min": 0, "max": 50000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-hostname": {
        "hostname": {
            "type": "string",
            "help": "DNS server host name list separated by space (maximum 4 domains).",
            "required": True,
            "default": "",
            "max_length": 127,
        },
    },
    "domain": {
        "domain": {
            "type": "string",
            "help": "DNS search domain list separated by space (maximum 8 domains).",
            "required": True,
            "default": "",
            "max_length": 127,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_PROTOCOL = [
    "cleartext",
    "dot",
    "doh",
]
VALID_BODY_CACHE_NOTFOUND_RESPONSES = [
    "disable",
    "enable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_SERVER_SELECT_METHOD = [
    "least-rtt",
    "failover",
]
VALID_BODY_LOG = [
    "disable",
    "error",
    "all",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_dns_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/dns."""
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


def validate_system_dns_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/dns object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-notfound-responses" in payload:
        is_valid, error = _validate_enum_field(
            "cache-notfound-responses",
            payload["cache-notfound-responses"],
            VALID_BODY_CACHE_NOTFOUND_RESPONSES,
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
    if "server-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "server-select-method",
            payload["server-select-method"],
            VALID_BODY_SERVER_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_dns_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/dns."""
    # Validate enum values using central function
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-notfound-responses" in payload:
        is_valid, error = _validate_enum_field(
            "cache-notfound-responses",
            payload["cache-notfound-responses"],
            VALID_BODY_CACHE_NOTFOUND_RESPONSES,
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
    if "server-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "server-select-method",
            payload["server-select-method"],
            VALID_BODY_SERVER_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
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
    "endpoint": "system/dns",
    "category": "cmdb",
    "api_path": "system/dns",
    "help": "Configure DNS.",
    "total_fields": 28,
    "required_fields_count": 1,
    "fields_with_defaults_count": 26,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
