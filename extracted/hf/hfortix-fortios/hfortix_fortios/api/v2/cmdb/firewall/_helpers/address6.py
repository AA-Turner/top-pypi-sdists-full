"""Validation helpers for firewall/address6 - Auto-generated"""

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
    "template",  # IPv6 address template.
    "filter",  # Match criteria filter.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "type": "ipprefix",
    "route-tag": 0,
    "sdn": "",
    "ip6": "::/0",
    "wildcard": ":: ::",
    "start-ip": "::",
    "end-ip": "::",
    "fqdn": "",
    "country": "",
    "cache-ttl": 0,
    "color": 0,
    "template": "",
    "host-type": "any",
    "host": "::",
    "tenant": "",
    "epg-name": "",
    "sdn-tag": "",
    "sdn-addr-type": "private",
    "passive-fqdn-learning": "enable",
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
    "name": "string",  # Address name.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "type": "option",  # Type of IPv6 address object (default = ipprefix).
    "route-tag": "integer",  # route-tag address.
    "macaddr": "string",  # Multiple MAC address ranges.
    "sdn": "string",  # SDN.
    "ip6": "ipv6-network",  # IPv6 address prefix (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:x
    "wildcard": "ipv6-wildcard",  # IPv6 address and wildcard netmask.
    "start-ip": "ipv6-address",  # First IP address (inclusive) in the range for the address (f
    "end-ip": "ipv6-address",  # Final IP address (inclusive) in the range for the address (f
    "fqdn": "string",  # Fully qualified domain name.
    "country": "string",  # IPv6 addresses associated to a specific country.
    "cache-ttl": "integer",  # Minimal TTL of individual IPv6 addresses in FQDN cache.
    "color": "integer",  # Integer value to determine the color of the icon in the GUI 
    "obj-id": "var-string",  # Object ID for NSX.
    "tagging": "string",  # Config object tagging.
    "comment": "var-string",  # Comment.
    "template": "string",  # IPv6 address template.
    "subnet-segment": "string",  # IPv6 subnet segments.
    "host-type": "option",  # Host type.
    "host": "ipv6-address",  # Host Address.
    "tenant": "string",  # Tenant.
    "epg-name": "string",  # Endpoint group name.
    "sdn-tag": "string",  # SDN Tag.
    "filter": "var-string",  # Match criteria filter.
    "list": "string",  # IP address list.
    "sdn-addr-type": "option",  # Type of addresses to collect.
    "passive-fqdn-learning": "option",  # Enable/disable passive learning of FQDNs.  When enabled, the
    "fabric-object": "option",  # Security Fabric global object setting.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Address name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "type": "Type of IPv6 address object (default = ipprefix).",
    "route-tag": "route-tag address.",
    "macaddr": "Multiple MAC address ranges.",
    "sdn": "SDN.",
    "ip6": "IPv6 address prefix (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx).",
    "wildcard": "IPv6 address and wildcard netmask.",
    "start-ip": "First IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).",
    "end-ip": "Final IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).",
    "fqdn": "Fully qualified domain name.",
    "country": "IPv6 addresses associated to a specific country.",
    "cache-ttl": "Minimal TTL of individual IPv6 addresses in FQDN cache.",
    "color": "Integer value to determine the color of the icon in the GUI (range 1 to 32, default = 0, which sets the value to 1).",
    "obj-id": "Object ID for NSX.",
    "tagging": "Config object tagging.",
    "comment": "Comment.",
    "template": "IPv6 address template.",
    "subnet-segment": "IPv6 subnet segments.",
    "host-type": "Host type.",
    "host": "Host Address.",
    "tenant": "Tenant.",
    "epg-name": "Endpoint group name.",
    "sdn-tag": "SDN Tag.",
    "filter": "Match criteria filter.",
    "list": "IP address list.",
    "sdn-addr-type": "Type of addresses to collect.",
    "passive-fqdn-learning": "Enable/disable passive learning of FQDNs.  When enabled, the FortiGate learns, trusts, and saves FQDNs from endpoint DNS queries (default = enable).",
    "fabric-object": "Security Fabric global object setting.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "route-tag": {"type": "integer", "min": 1, "max": 4294967295},
    "sdn": {"type": "string", "max_length": 35},
    "fqdn": {"type": "string", "max_length": 255},
    "country": {"type": "string", "max_length": 2},
    "cache-ttl": {"type": "integer", "min": 0, "max": 86400},
    "color": {"type": "integer", "min": 0, "max": 32},
    "template": {"type": "string", "max_length": 63},
    "tenant": {"type": "string", "max_length": 35},
    "epg-name": {"type": "string", "max_length": 255},
    "sdn-tag": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "macaddr": {
        "macaddr": {
            "type": "string",
            "help": "MAC address ranges <start>[-<end>] separated by space.",
            "required": True,
            "default": "",
            "max_length": 127,
        },
    },
    "tagging": {
        "name": {
            "type": "string",
            "help": "Tagging entry name.",
            "default": "",
            "max_length": 63,
        },
        "category": {
            "type": "string",
            "help": "Tag category.",
            "default": "",
            "max_length": 63,
        },
        "tags": {
            "type": "string",
            "help": "Tags.",
        },
    },
    "subnet-segment": {
        "name": {
            "type": "string",
            "help": "Name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "type": {
            "type": "option",
            "help": "Subnet segment type.",
            "required": True,
            "default": "any",
            "options": ["any", "specific"],
        },
        "value": {
            "type": "string",
            "help": "Subnet segment value.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
    "list": {
        "ip": {
            "type": "string",
            "help": "IP.",
            "required": True,
            "default": "",
            "max_length": 89,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "ipprefix",
    "iprange",
    "fqdn",
    "geography",
    "dynamic",
    "template",
    "mac",
    "route-tag",
    "wildcard",
]
VALID_BODY_HOST_TYPE = [
    "any",
    "specific",
]
VALID_BODY_SDN_ADDR_TYPE = [
    "private",
    "public",
    "all",
]
VALID_BODY_PASSIVE_FQDN_LEARNING = [
    "disable",
    "enable",
]
VALID_BODY_FABRIC_OBJECT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_address6_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/address6."""
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


def validate_firewall_address6_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/address6 object."""
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
    if "host-type" in payload:
        is_valid, error = _validate_enum_field(
            "host-type",
            payload["host-type"],
            VALID_BODY_HOST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdn-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "sdn-addr-type",
            payload["sdn-addr-type"],
            VALID_BODY_SDN_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "passive-fqdn-learning" in payload:
        is_valid, error = _validate_enum_field(
            "passive-fqdn-learning",
            payload["passive-fqdn-learning"],
            VALID_BODY_PASSIVE_FQDN_LEARNING,
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


def validate_firewall_address6_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/address6."""
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
    if "host-type" in payload:
        is_valid, error = _validate_enum_field(
            "host-type",
            payload["host-type"],
            VALID_BODY_HOST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdn-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "sdn-addr-type",
            payload["sdn-addr-type"],
            VALID_BODY_SDN_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "passive-fqdn-learning" in payload:
        is_valid, error = _validate_enum_field(
            "passive-fqdn-learning",
            payload["passive-fqdn-learning"],
            VALID_BODY_PASSIVE_FQDN_LEARNING,
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
    "endpoint": "firewall/address6",
    "category": "cmdb",
    "api_path": "firewall/address6",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure IPv6 firewall addresses.",
    "total_fields": 29,
    "required_fields_count": 2,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
