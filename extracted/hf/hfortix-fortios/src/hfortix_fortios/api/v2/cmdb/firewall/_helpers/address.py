"""Validation helpers for firewall/address - Auto-generated"""

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
    "interface",  # Name of interface whose IP address is to be used.
    "filter",  # Match criteria filter.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "subnet": "0.0.0.0 0.0.0.0",
    "type": "ipmask",
    "route-tag": 0,
    "sub-type": "sdn",
    "clearpass-spt": "unknown",
    "start-ip": "0.0.0.0",
    "end-ip": "0.0.0.0",
    "fqdn": "",
    "country": "",
    "wildcard-fqdn": "",
    "cache-ttl": 0,
    "wildcard": "0.0.0.0 0.0.0.0",
    "sdn": "",
    "interface": "",
    "tenant": "",
    "organization": "",
    "epg-name": "",
    "subnet-name": "",
    "sdn-tag": "",
    "policy-group": "",
    "obj-tag": "",
    "obj-type": "ip",
    "tag-detection-level": "",
    "tag-type": "",
    "hw-vendor": "",
    "hw-model": "",
    "os": "",
    "sw-version": "",
    "associated-interface": "",
    "color": 0,
    "sdn-addr-type": "private",
    "node-ip-only": "disable",
    "allow-routing": "disable",
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
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "subnet": "ipv4-classnet-any",  # IP address and subnet mask of address.
    "type": "option",  # Type of address.
    "route-tag": "integer",  # route-tag address.
    "sub-type": "option",  # Sub-type of address.
    "clearpass-spt": "option",  # SPT (System Posture Token) value.
    "macaddr": "string",  # Multiple MAC address ranges.
    "start-ip": "ipv4-address-any",  # First IP address (inclusive) in the range for the address.
    "end-ip": "ipv4-address-any",  # Final IP address (inclusive) in the range for the address.
    "fqdn": "string",  # Fully Qualified Domain Name address.
    "country": "string",  # IP addresses associated to a specific country.
    "wildcard-fqdn": "string",  # Fully Qualified Domain Name with wildcard characters.
    "cache-ttl": "integer",  # Defines the minimal TTL of individual IP addresses in FQDN cache measured in sec
    "wildcard": "ipv4-classnet-any",  # IP address and wildcard netmask.
    "sdn": "string",  # SDN.
    "fsso-group": "string",  # FSSO group(s).
    "sso-attribute-value": "string",  # RADIUS attributes value.
    "interface": "string",  # Name of interface whose IP address is to be used.
    "tenant": "string",  # Tenant.
    "organization": "string",  # Organization domain name (Syntax: organization/domain).
    "epg-name": "string",  # Endpoint group name.
    "subnet-name": "string",  # Subnet name.
    "sdn-tag": "string",  # SDN Tag.
    "policy-group": "string",  # Policy group name.
    "obj-tag": "string",  # Tag of dynamic address object.
    "obj-type": "option",  # Object type.
    "tag-detection-level": "string",  # Tag detection level of dynamic address object.
    "tag-type": "string",  # Tag type of dynamic address object.
    "hw-vendor": "string",  # Dynamic address matching hardware vendor.
    "hw-model": "string",  # Dynamic address matching hardware model.
    "os": "string",  # Dynamic address matching operating system.
    "sw-version": "string",  # Dynamic address matching software version.
    "comment": "var-string",  # Comment.
    "associated-interface": "string",  # Network interface associated with address.
    "color": "integer",  # Color of icon on the GUI.
    "filter": "var-string",  # Match criteria filter.
    "sdn-addr-type": "option",  # Type of addresses to collect.
    "node-ip-only": "option",  # Enable/disable collection of node addresses only in Kubernetes.
    "obj-id": "var-string",  # Object ID for NSX.
    "list": "string",  # IP address list.
    "tagging": "string",  # Config object tagging.
    "allow-routing": "option",  # Enable/disable use of this address in routing configurations.
    "passive-fqdn-learning": "option",  # Enable/disable passive learning of FQDNs.  When enabled, the FortiGate learns, t
    "fabric-object": "option",  # Security Fabric global object setting.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Address name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "subnet": "IP address and subnet mask of address.",
    "type": "Type of address.",
    "route-tag": "route-tag address.",
    "sub-type": "Sub-type of address.",
    "clearpass-spt": "SPT (System Posture Token) value.",
    "macaddr": "Multiple MAC address ranges.",
    "start-ip": "First IP address (inclusive) in the range for the address.",
    "end-ip": "Final IP address (inclusive) in the range for the address.",
    "fqdn": "Fully Qualified Domain Name address.",
    "country": "IP addresses associated to a specific country.",
    "wildcard-fqdn": "Fully Qualified Domain Name with wildcard characters.",
    "cache-ttl": "Defines the minimal TTL of individual IP addresses in FQDN cache measured in seconds.",
    "wildcard": "IP address and wildcard netmask.",
    "sdn": "SDN.",
    "fsso-group": "FSSO group(s).",
    "sso-attribute-value": "RADIUS attributes value.",
    "interface": "Name of interface whose IP address is to be used.",
    "tenant": "Tenant.",
    "organization": "Organization domain name (Syntax: organization/domain).",
    "epg-name": "Endpoint group name.",
    "subnet-name": "Subnet name.",
    "sdn-tag": "SDN Tag.",
    "policy-group": "Policy group name.",
    "obj-tag": "Tag of dynamic address object.",
    "obj-type": "Object type.",
    "tag-detection-level": "Tag detection level of dynamic address object.",
    "tag-type": "Tag type of dynamic address object.",
    "hw-vendor": "Dynamic address matching hardware vendor.",
    "hw-model": "Dynamic address matching hardware model.",
    "os": "Dynamic address matching operating system.",
    "sw-version": "Dynamic address matching software version.",
    "comment": "Comment.",
    "associated-interface": "Network interface associated with address.",
    "color": "Color of icon on the GUI.",
    "filter": "Match criteria filter.",
    "sdn-addr-type": "Type of addresses to collect.",
    "node-ip-only": "Enable/disable collection of node addresses only in Kubernetes.",
    "obj-id": "Object ID for NSX.",
    "list": "IP address list.",
    "tagging": "Config object tagging.",
    "allow-routing": "Enable/disable use of this address in routing configurations.",
    "passive-fqdn-learning": "Enable/disable passive learning of FQDNs.  When enabled, the FortiGate learns, trusts, and saves FQDNs from endpoint DNS queries (default = enable).",
    "fabric-object": "Security Fabric global object setting.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "route-tag": {"type": "integer", "min": 1, "max": 4294967295},
    "fqdn": {"type": "string", "max_length": 255},
    "country": {"type": "string", "max_length": 2},
    "wildcard-fqdn": {"type": "string", "max_length": 255},
    "cache-ttl": {"type": "integer", "min": 0, "max": 86400},
    "sdn": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 35},
    "tenant": {"type": "string", "max_length": 35},
    "organization": {"type": "string", "max_length": 35},
    "epg-name": {"type": "string", "max_length": 255},
    "subnet-name": {"type": "string", "max_length": 255},
    "sdn-tag": {"type": "string", "max_length": 15},
    "policy-group": {"type": "string", "max_length": 15},
    "obj-tag": {"type": "string", "max_length": 255},
    "tag-detection-level": {"type": "string", "max_length": 15},
    "tag-type": {"type": "string", "max_length": 63},
    "hw-vendor": {"type": "string", "max_length": 35},
    "hw-model": {"type": "string", "max_length": 35},
    "os": {"type": "string", "max_length": 35},
    "sw-version": {"type": "string", "max_length": 35},
    "associated-interface": {"type": "string", "max_length": 35},
    "color": {"type": "integer", "min": 0, "max": 32},
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
    "fsso-group": {
        "name": {
            "type": "string",
            "help": "FSSO group name.",
            "default": "",
            "max_length": 511,
        },
    },
    "sso-attribute-value": {
        "name": {
            "type": "string",
            "help": "RADIUS attribute value.",
            "default": "",
            "max_length": 511,
        },
    },
    "list": {
        "ip": {
            "type": "string",
            "help": "IP.",
            "required": True,
            "default": "",
            "max_length": 35,
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
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "ipmask",
    "iprange",
    "fqdn",
    "geography",
    "wildcard",
    "dynamic",
    "interface-subnet",
    "mac",
    "route-tag",
]
VALID_BODY_SUB_TYPE = [
    "sdn",
    "clearpass-spt",
    "fsso",
    "rsso",
    "ems-tag",
    "fortivoice-tag",
    "fortinac-tag",
    "swc-tag",
    "device-identification",
    "external-resource",
    "obsolete",
]
VALID_BODY_CLEARPASS_SPT = [
    "unknown",
    "healthy",
    "quarantine",
    "checkup",
    "transient",
    "infected",
]
VALID_BODY_OBJ_TYPE = [
    "ip",
    "mac",
]
VALID_BODY_SDN_ADDR_TYPE = [
    "private",
    "public",
    "all",
]
VALID_BODY_NODE_IP_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_ROUTING = [
    "enable",
    "disable",
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


def validate_firewall_address_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/address."""
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


def validate_firewall_address_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/address object."""
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
    if "sub-type" in payload:
        is_valid, error = _validate_enum_field(
            "sub-type",
            payload["sub-type"],
            VALID_BODY_SUB_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clearpass-spt" in payload:
        is_valid, error = _validate_enum_field(
            "clearpass-spt",
            payload["clearpass-spt"],
            VALID_BODY_CLEARPASS_SPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obj-type" in payload:
        is_valid, error = _validate_enum_field(
            "obj-type",
            payload["obj-type"],
            VALID_BODY_OBJ_TYPE,
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
    if "node-ip-only" in payload:
        is_valid, error = _validate_enum_field(
            "node-ip-only",
            payload["node-ip-only"],
            VALID_BODY_NODE_IP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-routing" in payload:
        is_valid, error = _validate_enum_field(
            "allow-routing",
            payload["allow-routing"],
            VALID_BODY_ALLOW_ROUTING,
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


def validate_firewall_address_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/address."""
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
    if "sub-type" in payload:
        is_valid, error = _validate_enum_field(
            "sub-type",
            payload["sub-type"],
            VALID_BODY_SUB_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clearpass-spt" in payload:
        is_valid, error = _validate_enum_field(
            "clearpass-spt",
            payload["clearpass-spt"],
            VALID_BODY_CLEARPASS_SPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "obj-type" in payload:
        is_valid, error = _validate_enum_field(
            "obj-type",
            payload["obj-type"],
            VALID_BODY_OBJ_TYPE,
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
    if "node-ip-only" in payload:
        is_valid, error = _validate_enum_field(
            "node-ip-only",
            payload["node-ip-only"],
            VALID_BODY_NODE_IP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-routing" in payload:
        is_valid, error = _validate_enum_field(
            "allow-routing",
            payload["allow-routing"],
            VALID_BODY_ALLOW_ROUTING,
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
    "endpoint": "firewall/address",
    "category": "cmdb",
    "api_path": "firewall/address",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure IPv4 addresses.",
    "total_fields": 45,
    "required_fields_count": 2,
    "fields_with_defaults_count": 37,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
