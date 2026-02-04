"""Validation helpers for system/ddns - Auto-generated"""

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
    "ddns-server",  # Select a DDNS service provider.
    "monitor-interface",  # Monitored interface.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ddnsid": 0,
    "ddns-server": "",
    "addr-type": "ipv4",
    "server-type": "ipv4",
    "ddns-zone": "",
    "ddns-ttl": 300,
    "ddns-auth": "disable",
    "ddns-keyname": "",
    "ddns-domain": "",
    "ddns-username": "",
    "ddns-sn": "",
    "use-public-ip": "disable",
    "update-interval": 0,
    "clear-text": "disable",
    "ssl-certificate": "Fortinet_Factory",
    "bound-ip": "",
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
    "ddnsid": "integer",  # DDNS ID.
    "ddns-server": "option",  # Select a DDNS service provider.
    "addr-type": "option",  # Address type of interface address in DDNS update.
    "server-type": "option",  # Address type of the DDNS server.
    "ddns-server-addr": "string",  # Generic DDNS server IP/FQDN list.
    "ddns-zone": "string",  # Zone of your domain name (for example, DDNS.com).
    "ddns-ttl": "integer",  # Time-to-live for DDNS packets.
    "ddns-auth": "option",  # Enable/disable TSIG authentication for your DDNS server.
    "ddns-keyname": "string",  # DDNS update key name.
    "ddns-key": "password_aes256",  # DDNS update key (base 64 encoding).
    "ddns-domain": "string",  # Your fully qualified domain name. For example, yourname.ddns.com.
    "ddns-username": "string",  # DDNS user name.
    "ddns-sn": "string",  # DDNS Serial Number.
    "ddns-password": "password",  # DDNS password.
    "use-public-ip": "option",  # Enable/disable use of public IP address.
    "update-interval": "integer",  # DDNS update interval (60 - 2592000 sec, 0 means default).
    "clear-text": "option",  # Enable/disable use of clear text connections.
    "ssl-certificate": "string",  # Name of local certificate for SSL connections.
    "bound-ip": "string",  # Bound IP address.
    "monitor-interface": "string",  # Monitored interface.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ddnsid": "DDNS ID.",
    "ddns-server": "Select a DDNS service provider.",
    "addr-type": "Address type of interface address in DDNS update.",
    "server-type": "Address type of the DDNS server.",
    "ddns-server-addr": "Generic DDNS server IP/FQDN list.",
    "ddns-zone": "Zone of your domain name (for example, DDNS.com).",
    "ddns-ttl": "Time-to-live for DDNS packets.",
    "ddns-auth": "Enable/disable TSIG authentication for your DDNS server.",
    "ddns-keyname": "DDNS update key name.",
    "ddns-key": "DDNS update key (base 64 encoding).",
    "ddns-domain": "Your fully qualified domain name. For example, yourname.ddns.com.",
    "ddns-username": "DDNS user name.",
    "ddns-sn": "DDNS Serial Number.",
    "ddns-password": "DDNS password.",
    "use-public-ip": "Enable/disable use of public IP address.",
    "update-interval": "DDNS update interval (60 - 2592000 sec, 0 means default).",
    "clear-text": "Enable/disable use of clear text connections.",
    "ssl-certificate": "Name of local certificate for SSL connections.",
    "bound-ip": "Bound IP address.",
    "monitor-interface": "Monitored interface.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "ddnsid": {"type": "integer", "min": 0, "max": 4294967295},
    "ddns-zone": {"type": "string", "max_length": 64},
    "ddns-ttl": {"type": "integer", "min": 60, "max": 86400},
    "ddns-keyname": {"type": "string", "max_length": 64},
    "ddns-domain": {"type": "string", "max_length": 64},
    "ddns-username": {"type": "string", "max_length": 64},
    "ddns-sn": {"type": "string", "max_length": 64},
    "update-interval": {"type": "integer", "min": 60, "max": 2592000},
    "ssl-certificate": {"type": "string", "max_length": 35},
    "bound-ip": {"type": "string", "max_length": 46},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ddns-server-addr": {
        "addr": {
            "type": "string",
            "help": "IP address or FQDN of the server.",
            "required": True,
            "default": "",
            "max_length": 256,
        },
    },
    "monitor-interface": {
        "interface-name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_DDNS_SERVER = [
    "dyndns.org",
    "dyns.net",
    "tzo.com",
    "vavic.com",
    "dipdns.net",
    "now.net.cn",
    "dhs.org",
    "easydns.com",
    "genericDDNS",
    "FortiGuardDDNS",
    "noip.com",
]
VALID_BODY_ADDR_TYPE = [
    "ipv4",
    "ipv6",
]
VALID_BODY_SERVER_TYPE = [
    "ipv4",
    "ipv6",
]
VALID_BODY_DDNS_AUTH = [
    "disable",
    "tsig",
]
VALID_BODY_USE_PUBLIC_IP = [
    "disable",
    "enable",
]
VALID_BODY_CLEAR_TEXT = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ddns_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ddns."""
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


def validate_system_ddns_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ddns object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ddns-server" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-server",
            payload["ddns-server"],
            VALID_BODY_DDNS_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
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
    if "ddns-auth" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-auth",
            payload["ddns-auth"],
            VALID_BODY_DDNS_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-public-ip" in payload:
        is_valid, error = _validate_enum_field(
            "use-public-ip",
            payload["use-public-ip"],
            VALID_BODY_USE_PUBLIC_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clear-text" in payload:
        is_valid, error = _validate_enum_field(
            "clear-text",
            payload["clear-text"],
            VALID_BODY_CLEAR_TEXT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ddns_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ddns."""
    # Validate enum values using central function
    if "ddns-server" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-server",
            payload["ddns-server"],
            VALID_BODY_DDNS_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
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
    if "ddns-auth" in payload:
        is_valid, error = _validate_enum_field(
            "ddns-auth",
            payload["ddns-auth"],
            VALID_BODY_DDNS_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-public-ip" in payload:
        is_valid, error = _validate_enum_field(
            "use-public-ip",
            payload["use-public-ip"],
            VALID_BODY_USE_PUBLIC_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clear-text" in payload:
        is_valid, error = _validate_enum_field(
            "clear-text",
            payload["clear-text"],
            VALID_BODY_CLEAR_TEXT,
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
    "endpoint": "system/ddns",
    "category": "cmdb",
    "api_path": "system/ddns",
    "mkey": "ddnsid",
    "mkey_type": "integer",
    "help": "Configure DDNS.",
    "total_fields": 20,
    "required_fields_count": 2,
    "fields_with_defaults_count": 16,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
