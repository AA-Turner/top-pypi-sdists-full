"""Validation helpers for router/multicast - Auto-generated"""

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
    "route-threshold": "",
    "route-limit": 2147483647,
    "multicast-routing": "disable",
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
    "route-threshold": "integer",  # Generate warnings when the number of multicast routes exceeds this number, must 
    "route-limit": "integer",  # Maximum number of multicast routes.
    "multicast-routing": "option",  # Enable/disable IP multicast routing.
    "pim-sm-global": "string",  # PIM sparse-mode global settings.
    "pim-sm-global-vrf": "string",  # per-VRF PIM sparse-mode global settings.
    "interface": "string",  # PIM interfaces.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "route-threshold": "Generate warnings when the number of multicast routes exceeds this number, must not be greater than route-limit.",
    "route-limit": "Maximum number of multicast routes.",
    "multicast-routing": "Enable/disable IP multicast routing.",
    "pim-sm-global": "PIM sparse-mode global settings.",
    "pim-sm-global-vrf": "per-VRF PIM sparse-mode global settings.",
    "interface": "PIM interfaces.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "route-threshold": {"type": "integer", "min": 1, "max": 2147483647},
    "route-limit": {"type": "integer", "min": 1, "max": 2147483647},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "pim-sm-global": {
        "message-interval": {
            "type": "integer",
            "help": "Period of time between sending periodic PIM join/prune messages in seconds (1 - 65535, default = 60).",
            "default": 60,
            "min_value": 1,
            "max_value": 65535,
        },
        "join-prune-holdtime": {
            "type": "integer",
            "help": "Join/prune holdtime (1 - 65535, default = 210).",
            "default": 210,
            "min_value": 1,
            "max_value": 65535,
        },
        "accept-register-list": {
            "type": "string",
            "help": "Sources allowed to register packets with this Rendezvous Point (RP).",
            "default": "",
            "max_length": 35,
        },
        "accept-source-list": {
            "type": "string",
            "help": "Sources allowed to send multicast traffic.",
            "default": "",
            "max_length": 35,
        },
        "bsr-candidate": {
            "type": "option",
            "help": "Enable/disable allowing this router to become a bootstrap router (BSR).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bsr-interface": {
            "type": "string",
            "help": "Interface to advertise as candidate BSR.",
            "default": "",
            "max_length": 15,
        },
        "bsr-priority": {
            "type": "integer",
            "help": "BSR priority (0 - 255, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "bsr-hash": {
            "type": "integer",
            "help": "BSR hash length (0 - 32, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 32,
        },
        "bsr-allow-quick-refresh": {
            "type": "option",
            "help": "Enable/disable accept BSR quick refresh packets from neighbors.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "cisco-crp-prefix": {
            "type": "option",
            "help": "Enable/disable making candidate RP compatible with old Cisco IOS.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "cisco-register-checksum": {
            "type": "option",
            "help": "Checksum entire register packet(for old Cisco IOS compatibility).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "cisco-register-checksum-group": {
            "type": "string",
            "help": "Cisco register checksum only these groups.",
            "default": "",
            "max_length": 35,
        },
        "cisco-ignore-rp-set-priority": {
            "type": "option",
            "help": "Use only hash for RP selection (compatibility with old Cisco IOS).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "register-rp-reachability": {
            "type": "option",
            "help": "Enable/disable check RP is reachable before registering packets.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "register-source": {
            "type": "option",
            "help": "Override source address in register packets.",
            "default": "disable",
            "options": ["disable", "interface", "ip-address"],
        },
        "register-source-interface": {
            "type": "string",
            "help": "Override with primary interface address.",
            "default": "",
            "max_length": 15,
        },
        "register-source-ip": {
            "type": "ipv4-address",
            "help": "Override with local IP address.",
            "default": "0.0.0.0",
        },
        "register-supression": {
            "type": "integer",
            "help": "Period of time to honor register-stop message (1 - 65535 sec, default = 60).",
            "default": 60,
            "min_value": 1,
            "max_value": 65535,
        },
        "null-register-retries": {
            "type": "integer",
            "help": "Maximum retries of null register (1 - 20, default = 1).",
            "default": 1,
            "min_value": 1,
            "max_value": 20,
        },
        "rp-register-keepalive": {
            "type": "integer",
            "help": "Timeout for RP receiving data on (S,G) tree (1 - 65535 sec, default = 185).",
            "default": 185,
            "min_value": 1,
            "max_value": 65535,
        },
        "spt-threshold": {
            "type": "option",
            "help": "Enable/disable switching to source specific trees.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "spt-threshold-group": {
            "type": "string",
            "help": "Groups allowed to switch to source tree.",
            "default": "",
            "max_length": 35,
        },
        "ssm": {
            "type": "option",
            "help": "Enable/disable source specific multicast.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ssm-range": {
            "type": "string",
            "help": "Groups allowed to source specific multicast.",
            "default": "",
            "max_length": 35,
        },
        "register-rate-limit": {
            "type": "integer",
            "help": "Limit of packets/sec per source registered through this RP (0 - 65535, default = 0 which means unlimited).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "pim-use-sdwan": {
            "type": "option",
            "help": "Enable/disable use of SDWAN when checking RPF neighbor and sending of REG packet.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rp-address": {
            "type": "string",
            "help": "Statically configure RP addresses.",
        },
    },
    "pim-sm-global-vrf": {
        "vrf": {
            "type": "integer",
            "help": "VRF ID.",
            "default": 0,
            "min_value": 1,
            "max_value": 511,
        },
        "bsr-candidate": {
            "type": "option",
            "help": "Enable/disable allowing this router to become a bootstrap router (BSR).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bsr-interface": {
            "type": "string",
            "help": "Interface to advertise as candidate BSR.",
            "default": "",
            "max_length": 15,
        },
        "bsr-priority": {
            "type": "integer",
            "help": "BSR priority (0 - 255, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "bsr-hash": {
            "type": "integer",
            "help": "BSR hash length (0 - 32, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 32,
        },
        "bsr-allow-quick-refresh": {
            "type": "option",
            "help": "Enable/disable accept BSR quick refresh packets from neighbors.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "cisco-crp-prefix": {
            "type": "option",
            "help": "Enable/disable making candidate RP compatible with old Cisco IOS.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rp-address": {
            "type": "string",
            "help": "Statically configure RP addresses.",
        },
    },
    "interface": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 15,
        },
        "ttl-threshold": {
            "type": "integer",
            "help": "Minimum TTL of multicast packets that will be forwarded (applied only to new multicast routes) (1 - 255, default = 1).",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "pim-mode": {
            "type": "option",
            "help": "PIM operation mode.",
            "default": "sparse-mode",
            "options": ["sparse-mode", "dense-mode"],
        },
        "passive": {
            "type": "option",
            "help": "Enable/disable listening to IGMP but not participating in PIM.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bfd": {
            "type": "option",
            "help": "Enable/disable Protocol Independent Multicast (PIM) Bidirectional Forwarding Detection (BFD).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "neighbour-filter": {
            "type": "string",
            "help": "Routers acknowledged as neighbor routers.",
            "default": "",
            "max_length": 35,
        },
        "hello-interval": {
            "type": "integer",
            "help": "Interval between sending PIM hello messages (0 - 65535 sec, default = 30).",
            "default": 30,
            "min_value": 1,
            "max_value": 65535,
        },
        "hello-holdtime": {
            "type": "integer",
            "help": "Time before old neighbor information expires (0 - 65535 sec, default = 105).",
            "default": 105,
            "min_value": 1,
            "max_value": 65535,
        },
        "cisco-exclude-genid": {
            "type": "option",
            "help": "Exclude GenID from hello packets (compatibility with old Cisco IOS).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dr-priority": {
            "type": "integer",
            "help": "DR election priority.",
            "default": 1,
            "min_value": 1,
            "max_value": 4294967295,
        },
        "propagation-delay": {
            "type": "integer",
            "help": "Delay flooding packets on this interface (100 - 5000 msec, default = 500).",
            "default": 500,
            "min_value": 100,
            "max_value": 5000,
        },
        "state-refresh-interval": {
            "type": "integer",
            "help": "Interval between sending state-refresh packets (1 - 100 sec, default = 60).",
            "default": 60,
            "min_value": 1,
            "max_value": 100,
        },
        "rp-candidate": {
            "type": "option",
            "help": "Enable/disable compete to become RP in elections.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rp-candidate-group": {
            "type": "string",
            "help": "Multicast groups managed by this RP.",
            "default": "",
            "max_length": 35,
        },
        "rp-candidate-priority": {
            "type": "integer",
            "help": "Router's priority as RP.",
            "default": 192,
            "min_value": 0,
            "max_value": 255,
        },
        "rp-candidate-interval": {
            "type": "integer",
            "help": "RP candidate advertisement interval (1 - 16383 sec, default = 60).",
            "default": 60,
            "min_value": 1,
            "max_value": 16383,
        },
        "multicast-flow": {
            "type": "string",
            "help": "Acceptable source for multicast group.",
            "default": "",
            "max_length": 35,
        },
        "static-group": {
            "type": "string",
            "help": "Statically set multicast groups to forward out.",
            "default": "",
            "max_length": 35,
        },
        "rpf-nbr-fail-back": {
            "type": "option",
            "help": "Enable/disable fail back for RPF neighbor query.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rpf-nbr-fail-back-filter": {
            "type": "string",
            "help": "Filter for fail back RPF neighbors.",
            "default": "",
            "max_length": 35,
        },
        "join-group": {
            "type": "string",
            "help": "Join multicast groups.",
        },
        "igmp": {
            "type": "string",
            "help": "IGMP configuration options.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MULTICAST_ROUTING = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_multicast_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/multicast."""
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


def validate_router_multicast_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/multicast object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "multicast-routing" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-routing",
            payload["multicast-routing"],
            VALID_BODY_MULTICAST_ROUTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_router_multicast_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/multicast."""
    # Validate enum values using central function
    if "multicast-routing" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-routing",
            payload["multicast-routing"],
            VALID_BODY_MULTICAST_ROUTING,
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
    "endpoint": "router/multicast",
    "category": "cmdb",
    "api_path": "router/multicast",
    "help": "Configure router multicast.",
    "total_fields": 6,
    "required_fields_count": 0,
    "fields_with_defaults_count": 3,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
