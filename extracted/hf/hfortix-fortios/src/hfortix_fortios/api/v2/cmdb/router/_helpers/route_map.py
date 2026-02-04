"""Validation helpers for router/route_map - Auto-generated"""

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
    "name",  # Name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "comments": "",
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
    "name": "string",  # Name.
    "comments": "string",  # Optional comments.
    "rule": "string",  # Rule.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "comments": "Optional comments.",
    "rule": "Rule.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comments": {"type": "string", "max_length": 127},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "rule": {
        "id": {
            "type": "integer",
            "help": "Rule ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "action": {
            "type": "option",
            "help": "Action.",
            "default": "permit",
            "options": ["permit", "deny"],
        },
        "match-as-path": {
            "type": "string",
            "help": "Match BGP AS path list.",
            "default": "",
            "max_length": 35,
        },
        "match-community": {
            "type": "string",
            "help": "Match BGP community list.",
            "default": "",
            "max_length": 35,
        },
        "match-extcommunity": {
            "type": "string",
            "help": "Match BGP extended community list.",
            "default": "",
            "max_length": 35,
        },
        "match-community-exact": {
            "type": "option",
            "help": "Enable/disable exact matching of communities.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "match-extcommunity-exact": {
            "type": "option",
            "help": "Enable/disable exact matching of extended communities.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "match-origin": {
            "type": "option",
            "help": "Match BGP origin code.",
            "default": "none",
            "options": ["none", "egp", "igp", "incomplete"],
        },
        "match-interface": {
            "type": "string",
            "help": "Match interface configuration.",
            "default": "",
            "max_length": 15,
        },
        "match-ip-address": {
            "type": "string",
            "help": "Match IP address permitted by access-list or prefix-list.",
            "default": "",
            "max_length": 35,
        },
        "match-ip6-address": {
            "type": "string",
            "help": "Match IPv6 address permitted by access-list6 or prefix-list6.",
            "default": "",
            "max_length": 35,
        },
        "match-ip-nexthop": {
            "type": "string",
            "help": "Match next hop IP address passed by access-list or prefix-list.",
            "default": "",
            "max_length": 35,
        },
        "match-ip6-nexthop": {
            "type": "string",
            "help": "Match next hop IPv6 address passed by access-list6 or prefix-list6.",
            "default": "",
            "max_length": 35,
        },
        "match-metric": {
            "type": "integer",
            "help": "Match metric for redistribute routes.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "match-route-type": {
            "type": "option",
            "help": "Match route type.",
            "default": "",
            "options": ["external-type1", "external-type2", "none"],
        },
        "match-tag": {
            "type": "integer",
            "help": "Match tag.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "match-vrf": {
            "type": "integer",
            "help": "Match VRF ID.",
            "default": "",
            "min_value": 0,
            "max_value": 511,
        },
        "match-suppress": {
            "type": "option",
            "help": "Enable/disable matching of suppressed original neighbor.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "set-aggregator-as": {
            "type": "integer",
            "help": "BGP aggregator AS.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-aggregator-ip": {
            "type": "ipv4-address-any",
            "help": "BGP aggregator IP.",
            "required": True,
            "default": "0.0.0.0",
        },
        "set-aspath-action": {
            "type": "option",
            "help": "Specify preferred action of set-aspath.",
            "default": "prepend",
            "options": ["prepend", "replace"],
        },
        "set-aspath": {
            "type": "string",
            "help": "Prepend BGP AS path attribute.",
        },
        "set-atomic-aggregate": {
            "type": "option",
            "help": "Enable/disable BGP atomic aggregate attribute.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "set-community-delete": {
            "type": "string",
            "help": "Delete communities matching community list.",
            "default": "",
            "max_length": 35,
        },
        "set-community": {
            "type": "string",
            "help": "BGP community attribute.",
        },
        "set-community-additive": {
            "type": "option",
            "help": "Enable/disable adding set-community to existing community.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "set-dampening-reachability-half-life": {
            "type": "integer",
            "help": "Reachability half-life time for the penalty (1 - 45 min, 0 = unset).",
            "default": 0,
            "min_value": 0,
            "max_value": 45,
        },
        "set-dampening-reuse": {
            "type": "integer",
            "help": "Value to start reusing a route (1 - 20000, 0 = unset).",
            "default": 0,
            "min_value": 0,
            "max_value": 20000,
        },
        "set-dampening-suppress": {
            "type": "integer",
            "help": "Value to start suppressing a route (1 - 20000, 0 = unset).",
            "default": 0,
            "min_value": 0,
            "max_value": 20000,
        },
        "set-dampening-max-suppress": {
            "type": "integer",
            "help": "Maximum duration to suppress a route (1 - 255 min, 0 = unset).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "set-dampening-unreachability-half-life": {
            "type": "integer",
            "help": "Unreachability Half-life time for the penalty (1 - 45 min, 0 = unset).",
            "default": 0,
            "min_value": 0,
            "max_value": 45,
        },
        "set-extcommunity-rt": {
            "type": "string",
            "help": "Route Target extended community.",
        },
        "set-extcommunity-soo": {
            "type": "string",
            "help": "Site-of-Origin extended community.",
        },
        "set-ip-nexthop": {
            "type": "ipv4-address",
            "help": "IP address of next hop.",
            "default": "",
        },
        "set-ip-prefsrc": {
            "type": "ipv4-address",
            "help": "IP address of preferred source.",
            "default": "",
        },
        "set-vpnv4-nexthop": {
            "type": "ipv4-address",
            "help": "IP address of VPNv4 next-hop.",
            "default": "",
        },
        "set-ip6-nexthop": {
            "type": "ipv6-address",
            "help": "IPv6 global address of next hop.",
            "default": "",
        },
        "set-ip6-nexthop-local": {
            "type": "ipv6-address",
            "help": "IPv6 local address of next hop.",
            "default": "",
        },
        "set-vpnv6-nexthop": {
            "type": "ipv6-address",
            "help": "IPv6 global address of VPNv6 next-hop.",
            "default": "",
        },
        "set-vpnv6-nexthop-local": {
            "type": "ipv6-address",
            "help": "IPv6 link-local address of VPNv6 next-hop.",
            "default": "",
        },
        "set-local-preference": {
            "type": "integer",
            "help": "BGP local preference path attribute.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-metric": {
            "type": "integer",
            "help": "Metric value.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-metric-type": {
            "type": "option",
            "help": "Metric type.",
            "default": "",
            "options": ["external-type1", "external-type2", "none"],
        },
        "set-originator-id": {
            "type": "ipv4-address-any",
            "help": "BGP originator ID attribute.",
            "default": "",
        },
        "set-origin": {
            "type": "option",
            "help": "BGP origin code.",
            "default": "none",
            "options": ["none", "egp", "igp", "incomplete"],
        },
        "set-tag": {
            "type": "integer",
            "help": "Tag value.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-weight": {
            "type": "integer",
            "help": "BGP weight for routing table.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-route-tag": {
            "type": "integer",
            "help": "Route tag for routing table.",
            "default": "",
            "min_value": 0,
            "max_value": 4294967295,
        },
        "set-priority": {
            "type": "integer",
            "help": "Priority for routing table.",
            "default": "",
            "min_value": 1,
            "max_value": 65535,
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_route_map_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/route_map."""
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


def validate_router_route_map_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/route_map object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_router_route_map_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/route_map."""
    # Validate enum values using central function

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
    "endpoint": "router/route_map",
    "category": "cmdb",
    "api_path": "router/route-map",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure route maps.",
    "total_fields": 3,
    "required_fields_count": 1,
    "fields_with_defaults_count": 2,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
