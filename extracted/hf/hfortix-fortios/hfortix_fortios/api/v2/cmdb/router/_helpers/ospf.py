"""Validation helpers for router/ospf - Auto-generated"""

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
    "abr-type": "standard",
    "auto-cost-ref-bandwidth": 1000,
    "distance-external": 110,
    "distance-inter-area": 110,
    "distance-intra-area": 110,
    "database-overflow": "disable",
    "database-overflow-max-lsas": 10000,
    "database-overflow-time-to-recover": 300,
    "default-information-originate": "disable",
    "default-information-metric": 10,
    "default-information-metric-type": "2",
    "default-information-route-map": "",
    "default-metric": 10,
    "distance": 110,
    "lsa-refresh-interval": 5,
    "rfc1583-compatible": "disable",
    "router-id": "0.0.0.0",
    "spf-timers": "",
    "bfd": "disable",
    "log-neighbour-changes": "enable",
    "distribute-list-in": "",
    "distribute-route-map-in": "",
    "restart-mode": "none",
    "restart-period": 120,
    "restart-on-topology-change": "disable",
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
    "abr-type": "option",  # Area border router type.
    "auto-cost-ref-bandwidth": "integer",  # Reference bandwidth in terms of megabits per second.
    "distance-external": "integer",  # Administrative external distance.
    "distance-inter-area": "integer",  # Administrative inter-area distance.
    "distance-intra-area": "integer",  # Administrative intra-area distance.
    "database-overflow": "option",  # Enable/disable database overflow.
    "database-overflow-max-lsas": "integer",  # Database overflow maximum LSAs.
    "database-overflow-time-to-recover": "integer",  # Database overflow time to recover (sec).
    "default-information-originate": "option",  # Enable/disable generation of default route.
    "default-information-metric": "integer",  # Default information metric.
    "default-information-metric-type": "option",  # Default information metric type.
    "default-information-route-map": "string",  # Default information route map.
    "default-metric": "integer",  # Default metric of redistribute routes.
    "distance": "integer",  # Distance of the route.
    "lsa-refresh-interval": "integer",  # The minimal OSPF LSA update time interval
    "rfc1583-compatible": "option",  # Enable/disable RFC1583 compatibility.
    "router-id": "ipv4-address-any",  # Router ID.
    "spf-timers": "user",  # SPF calculation frequency.
    "bfd": "option",  # Bidirectional Forwarding Detection (BFD).
    "log-neighbour-changes": "option",  # Log of OSPF neighbor changes.
    "distribute-list-in": "string",  # Filter incoming routes.
    "distribute-route-map-in": "string",  # Filter incoming external routes by route-map.
    "restart-mode": "option",  # OSPF restart mode (graceful or LLS).
    "restart-period": "integer",  # Graceful restart period.
    "restart-on-topology-change": "option",  # Enable/disable continuing graceful restart upon topology cha
    "area": "string",  # OSPF area configuration.
    "ospf-interface": "string",  # OSPF interface configuration.
    "network": "string",  # OSPF network configuration.
    "neighbor": "string",  # OSPF neighbor configuration are used when OSPF runs on non-b
    "passive-interface": "string",  # Passive interface configuration.
    "summary-address": "string",  # IP address summary configuration.
    "distribute-list": "string",  # Distribute list configuration.
    "redistribute": "string",  # Redistribute configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "abr-type": "Area border router type.",
    "auto-cost-ref-bandwidth": "Reference bandwidth in terms of megabits per second.",
    "distance-external": "Administrative external distance.",
    "distance-inter-area": "Administrative inter-area distance.",
    "distance-intra-area": "Administrative intra-area distance.",
    "database-overflow": "Enable/disable database overflow.",
    "database-overflow-max-lsas": "Database overflow maximum LSAs.",
    "database-overflow-time-to-recover": "Database overflow time to recover (sec).",
    "default-information-originate": "Enable/disable generation of default route.",
    "default-information-metric": "Default information metric.",
    "default-information-metric-type": "Default information metric type.",
    "default-information-route-map": "Default information route map.",
    "default-metric": "Default metric of redistribute routes.",
    "distance": "Distance of the route.",
    "lsa-refresh-interval": "The minimal OSPF LSA update time interval",
    "rfc1583-compatible": "Enable/disable RFC1583 compatibility.",
    "router-id": "Router ID.",
    "spf-timers": "SPF calculation frequency.",
    "bfd": "Bidirectional Forwarding Detection (BFD).",
    "log-neighbour-changes": "Log of OSPF neighbor changes.",
    "distribute-list-in": "Filter incoming routes.",
    "distribute-route-map-in": "Filter incoming external routes by route-map.",
    "restart-mode": "OSPF restart mode (graceful or LLS).",
    "restart-period": "Graceful restart period.",
    "restart-on-topology-change": "Enable/disable continuing graceful restart upon topology change.",
    "area": "OSPF area configuration.",
    "ospf-interface": "OSPF interface configuration.",
    "network": "OSPF network configuration.",
    "neighbor": "OSPF neighbor configuration are used when OSPF runs on non-broadcast media.",
    "passive-interface": "Passive interface configuration.",
    "summary-address": "IP address summary configuration.",
    "distribute-list": "Distribute list configuration.",
    "redistribute": "Redistribute configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "auto-cost-ref-bandwidth": {"type": "integer", "min": 1, "max": 1000000},
    "distance-external": {"type": "integer", "min": 1, "max": 255},
    "distance-inter-area": {"type": "integer", "min": 1, "max": 255},
    "distance-intra-area": {"type": "integer", "min": 1, "max": 255},
    "database-overflow-max-lsas": {"type": "integer", "min": 0, "max": 4294967295},
    "database-overflow-time-to-recover": {"type": "integer", "min": 0, "max": 65535},
    "default-information-metric": {"type": "integer", "min": 1, "max": 16777214},
    "default-information-route-map": {"type": "string", "max_length": 35},
    "default-metric": {"type": "integer", "min": 1, "max": 16777214},
    "distance": {"type": "integer", "min": 1, "max": 255},
    "lsa-refresh-interval": {"type": "integer", "min": 0, "max": 5},
    "distribute-list-in": {"type": "string", "max_length": 35},
    "distribute-route-map-in": {"type": "string", "max_length": 35},
    "restart-period": {"type": "integer", "min": 1, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "area": {
        "id": {
            "type": "ipv4-address-any",
            "help": "Area entry IP address.",
            "default": "0.0.0.0",
        },
        "shortcut": {
            "type": "option",
            "help": "Enable/disable shortcut option.",
            "default": "disable",
            "options": ["disable", "enable", "default"],
        },
        "authentication": {
            "type": "option",
            "help": "Authentication type.",
            "default": "none",
            "options": ["none", "text", "message-digest"],
        },
        "default-cost": {
            "type": "integer",
            "help": "Summary default cost of stub or NSSA area.",
            "default": 10,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "nssa-translator-role": {
            "type": "option",
            "help": "NSSA translator role type.",
            "default": "candidate",
            "options": ["candidate", "never", "always"],
        },
        "stub-type": {
            "type": "option",
            "help": "Stub summary setting.",
            "default": "summary",
            "options": ["no-summary", "summary"],
        },
        "type": {
            "type": "option",
            "help": "Area type setting.",
            "default": "regular",
            "options": ["regular", "nssa", "stub"],
        },
        "nssa-default-information-originate": {
            "type": "option",
            "help": "Redistribute, advertise, or do not originate Type-7 default route into NSSA area.",
            "default": "disable",
            "options": ["enable", "always", "disable"],
        },
        "nssa-default-information-originate-metric": {
            "type": "integer",
            "help": "OSPF default metric.",
            "default": 10,
            "min_value": 0,
            "max_value": 16777214,
        },
        "nssa-default-information-originate-metric-type": {
            "type": "option",
            "help": "OSPF metric type for default routes.",
            "default": "2",
            "options": ["1", "2"],
        },
        "nssa-redistribution": {
            "type": "option",
            "help": "Enable/disable redistribute into NSSA area.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "comments": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
        "range": {
            "type": "string",
            "help": "OSPF area range configuration.",
        },
        "virtual-link": {
            "type": "string",
            "help": "OSPF virtual link configuration.",
        },
        "filter-list": {
            "type": "string",
            "help": "OSPF area filter-list configuration.",
        },
    },
    "ospf-interface": {
        "name": {
            "type": "string",
            "help": "Interface entry name.",
            "default": "",
            "max_length": 35,
        },
        "comments": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
        "interface": {
            "type": "string",
            "help": "Configuration interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "ip": {
            "type": "ipv4-address",
            "help": "IP address.",
            "default": "0.0.0.0",
        },
        "linkdown-fast-failover": {
            "type": "option",
            "help": "Enable/disable fast link failover.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "authentication": {
            "type": "option",
            "help": "Authentication type.",
            "default": "none",
            "options": ["none", "text", "message-digest"],
        },
        "authentication-key": {
            "type": "password",
            "help": "Authentication key.",
            "max_length": 8,
        },
        "keychain": {
            "type": "string",
            "help": "Message-digest key-chain name.",
            "default": "",
            "max_length": 35,
        },
        "prefix-length": {
            "type": "integer",
            "help": "Prefix length.",
            "default": 0,
            "min_value": 0,
            "max_value": 32,
        },
        "retransmit-interval": {
            "type": "integer",
            "help": "Retransmit interval.",
            "default": 5,
            "min_value": 1,
            "max_value": 65535,
        },
        "transmit-delay": {
            "type": "integer",
            "help": "Transmit delay.",
            "default": 1,
            "min_value": 1,
            "max_value": 65535,
        },
        "cost": {
            "type": "integer",
            "help": "Cost of the interface, value range from 0 to 65535, 0 means auto-cost.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "priority": {
            "type": "integer",
            "help": "Priority.",
            "default": 1,
            "min_value": 0,
            "max_value": 255,
        },
        "dead-interval": {
            "type": "integer",
            "help": "Dead interval.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "hello-interval": {
            "type": "integer",
            "help": "Hello interval.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "hello-multiplier": {
            "type": "integer",
            "help": "Number of hello packets within dead interval.",
            "default": 0,
            "min_value": 3,
            "max_value": 10,
        },
        "database-filter-out": {
            "type": "option",
            "help": "Enable/disable control of flooding out LSAs.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mtu": {
            "type": "integer",
            "help": "MTU for database description packets.",
            "default": 0,
            "min_value": 576,
            "max_value": 65535,
        },
        "mtu-ignore": {
            "type": "option",
            "help": "Enable/disable ignore MTU.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "network-type": {
            "type": "option",
            "help": "Network type.",
            "default": "broadcast",
            "options": ["broadcast", "non-broadcast", "point-to-point", "point-to-multipoint", "point-to-multipoint-non-broadcast"],
        },
        "bfd": {
            "type": "option",
            "help": "Bidirectional Forwarding Detection (BFD).",
            "default": "global",
            "options": ["global", "enable", "disable"],
        },
        "status": {
            "type": "option",
            "help": "Enable/disable status.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "resync-timeout": {
            "type": "integer",
            "help": "Graceful restart neighbor resynchronization timeout.",
            "default": 40,
            "min_value": 1,
            "max_value": 3600,
        },
        "md5-keys": {
            "type": "string",
            "help": "MD5 key.",
        },
    },
    "network": {
        "id": {
            "type": "integer",
            "help": "Network entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix": {
            "type": "ipv4-classnet",
            "help": "Prefix.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "area": {
            "type": "ipv4-address-any",
            "help": "Attach the network to area.",
            "required": True,
            "default": "0.0.0.0",
        },
        "comments": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
    },
    "neighbor": {
        "id": {
            "type": "integer",
            "help": "Neighbor entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip": {
            "type": "ipv4-address",
            "help": "Interface IP address of the neighbor.",
            "required": True,
            "default": "0.0.0.0",
        },
        "poll-interval": {
            "type": "integer",
            "help": "Poll interval time in seconds.",
            "default": 10,
            "min_value": 1,
            "max_value": 65535,
        },
        "cost": {
            "type": "integer",
            "help": "Cost of the interface, value range from 0 to 65535, 0 means auto-cost.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "priority": {
            "type": "integer",
            "help": "Priority.",
            "default": 1,
            "min_value": 0,
            "max_value": 255,
        },
    },
    "passive-interface": {
        "name": {
            "type": "string",
            "help": "Passive interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "summary-address": {
        "id": {
            "type": "integer",
            "help": "Summary address entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "prefix": {
            "type": "ipv4-classnet",
            "help": "Prefix.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "tag": {
            "type": "integer",
            "help": "Tag value.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "advertise": {
            "type": "option",
            "help": "Enable/disable advertise status.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
    },
    "distribute-list": {
        "id": {
            "type": "integer",
            "help": "Distribute list entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "access-list": {
            "type": "string",
            "help": "Access list name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "protocol": {
            "type": "option",
            "help": "Protocol type.",
            "required": True,
            "default": "connected",
            "options": ["connected", "static", "rip"],
        },
    },
    "redistribute": {
        "name": {
            "type": "string",
            "help": "Redistribute name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "metric": {
            "type": "integer",
            "help": "Redistribute metric setting.",
            "default": 0,
            "min_value": 0,
            "max_value": 16777214,
        },
        "routemap": {
            "type": "string",
            "help": "Route map name.",
            "default": "",
            "max_length": 35,
        },
        "metric-type": {
            "type": "option",
            "help": "Metric type.",
            "default": "2",
            "options": ["1", "2"],
        },
        "tag": {
            "type": "integer",
            "help": "Tag value.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ABR_TYPE = [
    "cisco",
    "ibm",
    "shortcut",
    "standard",
]
VALID_BODY_DATABASE_OVERFLOW = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULT_INFORMATION_ORIGINATE = [
    "enable",
    "always",
    "disable",
]
VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE = [
    "1",
    "2",
]
VALID_BODY_RFC1583_COMPATIBLE = [
    "enable",
    "disable",
]
VALID_BODY_BFD = [
    "enable",
    "disable",
]
VALID_BODY_LOG_NEIGHBOUR_CHANGES = [
    "enable",
    "disable",
]
VALID_BODY_RESTART_MODE = [
    "none",
    "lls",
    "graceful-restart",
]
VALID_BODY_RESTART_ON_TOPOLOGY_CHANGE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_router_ospf_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/ospf."""
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


def validate_router_ospf_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/ospf object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "abr-type" in payload:
        is_valid, error = _validate_enum_field(
            "abr-type",
            payload["abr-type"],
            VALID_BODY_ABR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database-overflow" in payload:
        is_valid, error = _validate_enum_field(
            "database-overflow",
            payload["database-overflow"],
            VALID_BODY_DATABASE_OVERFLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-information-metric-type" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-metric-type",
            payload["default-information-metric-type"],
            VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rfc1583-compatible" in payload:
        is_valid, error = _validate_enum_field(
            "rfc1583-compatible",
            payload["rfc1583-compatible"],
            VALID_BODY_RFC1583_COMPATIBLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bfd" in payload:
        is_valid, error = _validate_enum_field(
            "bfd",
            payload["bfd"],
            VALID_BODY_BFD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-neighbour-changes" in payload:
        is_valid, error = _validate_enum_field(
            "log-neighbour-changes",
            payload["log-neighbour-changes"],
            VALID_BODY_LOG_NEIGHBOUR_CHANGES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "restart-mode" in payload:
        is_valid, error = _validate_enum_field(
            "restart-mode",
            payload["restart-mode"],
            VALID_BODY_RESTART_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "restart-on-topology-change" in payload:
        is_valid, error = _validate_enum_field(
            "restart-on-topology-change",
            payload["restart-on-topology-change"],
            VALID_BODY_RESTART_ON_TOPOLOGY_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_router_ospf_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/ospf."""
    # Validate enum values using central function
    if "abr-type" in payload:
        is_valid, error = _validate_enum_field(
            "abr-type",
            payload["abr-type"],
            VALID_BODY_ABR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "database-overflow" in payload:
        is_valid, error = _validate_enum_field(
            "database-overflow",
            payload["database-overflow"],
            VALID_BODY_DATABASE_OVERFLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-information-metric-type" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-metric-type",
            payload["default-information-metric-type"],
            VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rfc1583-compatible" in payload:
        is_valid, error = _validate_enum_field(
            "rfc1583-compatible",
            payload["rfc1583-compatible"],
            VALID_BODY_RFC1583_COMPATIBLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bfd" in payload:
        is_valid, error = _validate_enum_field(
            "bfd",
            payload["bfd"],
            VALID_BODY_BFD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-neighbour-changes" in payload:
        is_valid, error = _validate_enum_field(
            "log-neighbour-changes",
            payload["log-neighbour-changes"],
            VALID_BODY_LOG_NEIGHBOUR_CHANGES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "restart-mode" in payload:
        is_valid, error = _validate_enum_field(
            "restart-mode",
            payload["restart-mode"],
            VALID_BODY_RESTART_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "restart-on-topology-change" in payload:
        is_valid, error = _validate_enum_field(
            "restart-on-topology-change",
            payload["restart-on-topology-change"],
            VALID_BODY_RESTART_ON_TOPOLOGY_CHANGE,
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
    "endpoint": "router/ospf",
    "category": "cmdb",
    "api_path": "router/ospf",
    "help": "Configure OSPF.",
    "total_fields": 33,
    "required_fields_count": 0,
    "fields_with_defaults_count": 25,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
