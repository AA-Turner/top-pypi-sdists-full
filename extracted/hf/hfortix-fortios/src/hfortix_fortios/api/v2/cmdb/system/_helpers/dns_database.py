"""Validation helpers for system/dns_database - Auto-generated"""

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
    "name",  # Zone name.
    "domain",  # Domain name.
    "dns-entry",  # DNS entry.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "status": "enable",
    "domain": "",
    "allow-transfer": "",
    "type": "primary",
    "view": "shadow",
    "ip-primary": "0.0.0.0",
    "primary-name": "dns",
    "contact": "host",
    "ttl": 86400,
    "authoritative": "enable",
    "forwarder": "",
    "forwarder6": "::",
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "source-ip-interface": "",
    "rr-max": 16384,
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
    "name": "string",  # Zone name.
    "status": "option",  # Enable/disable this DNS zone.
    "domain": "string",  # Domain name.
    "allow-transfer": "user",  # DNS zone transfer IP address list.
    "type": "option",  # Zone type (primary to manage entries directly, secondary to import entries from 
    "view": "option",  # Zone view (public to serve public clients, shadow to serve internal clients).
    "ip-primary": "ipv4-address-any",  # IP address of primary DNS server. Entries in this primary DNS server and importe
    "primary-name": "string",  # Domain name of the default DNS server for this zone.
    "contact": "string",  # Email address of the administrator for this zone. You can specify only the usern
    "ttl": "integer",  # Default time-to-live value for the entries of this DNS zone (0 - 2147483647 sec,
    "authoritative": "option",  # Enable/disable authoritative zone.
    "forwarder": "user",  # DNS zone forwarder IP address list.
    "forwarder6": "ipv6-address",  # Forwarder IPv6 address.
    "source-ip": "ipv4-address",  # Source IP for forwarding to DNS server.
    "source-ip6": "ipv6-address",  # IPv6 source IP address for forwarding to DNS server.
    "source-ip-interface": "string",  # IP address of the specified interface as the source IP address.
    "rr-max": "integer",  # Maximum number of resource records (10 - 65536, 0 means infinite).
    "dns-entry": "string",  # DNS entry.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Zone name.",
    "status": "Enable/disable this DNS zone.",
    "domain": "Domain name.",
    "allow-transfer": "DNS zone transfer IP address list.",
    "type": "Zone type (primary to manage entries directly, secondary to import entries from other zones).",
    "view": "Zone view (public to serve public clients, shadow to serve internal clients).",
    "ip-primary": "IP address of primary DNS server. Entries in this primary DNS server and imported into the DNS zone.",
    "primary-name": "Domain name of the default DNS server for this zone.",
    "contact": "Email address of the administrator for this zone. You can specify only the username, such as admin or the full email address, such as admin@test.com When using only a username, the domain of the email will be this zone.",
    "ttl": "Default time-to-live value for the entries of this DNS zone (0 - 2147483647 sec, default = 86400).",
    "authoritative": "Enable/disable authoritative zone.",
    "forwarder": "DNS zone forwarder IP address list.",
    "forwarder6": "Forwarder IPv6 address.",
    "source-ip": "Source IP for forwarding to DNS server.",
    "source-ip6": "IPv6 source IP address for forwarding to DNS server.",
    "source-ip-interface": "IP address of the specified interface as the source IP address.",
    "rr-max": "Maximum number of resource records (10 - 65536, 0 means infinite).",
    "dns-entry": "DNS entry.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "domain": {"type": "string", "max_length": 255},
    "primary-name": {"type": "string", "max_length": 255},
    "contact": {"type": "string", "max_length": 255},
    "ttl": {"type": "integer", "min": 0, "max": 2147483647},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "rr-max": {"type": "integer", "min": 10, "max": 65536},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "dns-entry": {
        "id": {
            "type": "integer",
            "help": "DNS entry ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable resource record status.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "type": {
            "type": "option",
            "help": "Resource record type.",
            "required": True,
            "default": "A",
            "options": ["A", "NS", "CNAME", "MX", "AAAA", "PTR", "PTR_V6"],
        },
        "ttl": {
            "type": "integer",
            "help": "Time-to-live for this entry (0 to 2147483647 sec, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 2147483647,
        },
        "preference": {
            "type": "integer",
            "help": "DNS entry preference (0 - 65535, highest preference = 0, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 65535,
        },
        "ip": {
            "type": "ipv4-address-any",
            "help": "IPv4 address of the host.",
            "default": "0.0.0.0",
        },
        "ipv6": {
            "type": "ipv6-address",
            "help": "IPv6 address of the host.",
            "default": "::",
        },
        "hostname": {
            "type": "string",
            "help": "Name of the host.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
        "canonical-name": {
            "type": "string",
            "help": "Canonical name of the host.",
            "default": "",
            "max_length": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_TYPE = [
    "primary",
    "secondary",
]
VALID_BODY_VIEW = [
    "shadow",
    "public",
    "shadow-ztna",
    "proxy",
]
VALID_BODY_AUTHORITATIVE = [
    "enable",
    "disable",
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


def validate_system_dns_database_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/dns_database."""
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


def validate_system_dns_database_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/dns_database object."""
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
    if "view" in payload:
        is_valid, error = _validate_enum_field(
            "view",
            payload["view"],
            VALID_BODY_VIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authoritative" in payload:
        is_valid, error = _validate_enum_field(
            "authoritative",
            payload["authoritative"],
            VALID_BODY_AUTHORITATIVE,
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


def validate_system_dns_database_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/dns_database."""
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
    if "view" in payload:
        is_valid, error = _validate_enum_field(
            "view",
            payload["view"],
            VALID_BODY_VIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authoritative" in payload:
        is_valid, error = _validate_enum_field(
            "authoritative",
            payload["authoritative"],
            VALID_BODY_AUTHORITATIVE,
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
    "endpoint": "system/dns_database",
    "category": "cmdb",
    "api_path": "system/dns-database",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure DNS databases.",
    "total_fields": 21,
    "required_fields_count": 4,
    "fields_with_defaults_count": 20,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
