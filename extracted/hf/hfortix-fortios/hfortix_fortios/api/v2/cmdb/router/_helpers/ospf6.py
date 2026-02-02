"""Validation helpers for router/ospf6 - Auto-generated"""

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
    "default-information-originate": "disable",
    "log-neighbour-changes": "enable",
    "default-information-metric": 10,
    "default-information-metric-type": "2",
    "default-information-route-map": "",
    "default-metric": 10,
    "router-id": "0.0.0.0",
    "spf-timers": "",
    "bfd": "disable",
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
    "default-information-originate": "option",  # Enable/disable generation of default route.
    "log-neighbour-changes": "option",  # Log OSPFv3 neighbor changes.
    "default-information-metric": "integer",  # Default information metric.
    "default-information-metric-type": "option",  # Default information metric type.
    "default-information-route-map": "string",  # Default information route map.
    "default-metric": "integer",  # Default metric of redistribute routes.
    "router-id": "ipv4-address-any",  # A.B.C.D, in IPv4 address format.
    "spf-timers": "user",  # SPF calculation frequency.
    "bfd": "option",  # Enable/disable Bidirectional Forwarding Detection (BFD).
    "restart-mode": "option",  # OSPFv3 restart mode (graceful or none).
    "restart-period": "integer",  # Graceful restart period in seconds.
    "restart-on-topology-change": "option",  # Enable/disable continuing graceful restart upon topology cha
    "area": "string",  # OSPF6 area configuration.
    "ospf6-interface": "string",  # OSPF6 interface configuration.
    "redistribute": "string",  # Redistribute configuration.
    "passive-interface": "string",  # Passive interface configuration.
    "summary-address": "string",  # IPv6 address summary configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "abr-type": "Area border router type.",
    "auto-cost-ref-bandwidth": "Reference bandwidth in terms of megabits per second.",
    "default-information-originate": "Enable/disable generation of default route.",
    "log-neighbour-changes": "Log OSPFv3 neighbor changes.",
    "default-information-metric": "Default information metric.",
    "default-information-metric-type": "Default information metric type.",
    "default-information-route-map": "Default information route map.",
    "default-metric": "Default metric of redistribute routes.",
    "router-id": "A.B.C.D, in IPv4 address format.",
    "spf-timers": "SPF calculation frequency.",
    "bfd": "Enable/disable Bidirectional Forwarding Detection (BFD).",
    "restart-mode": "OSPFv3 restart mode (graceful or none).",
    "restart-period": "Graceful restart period in seconds.",
    "restart-on-topology-change": "Enable/disable continuing graceful restart upon topology change.",
    "area": "OSPF6 area configuration.",
    "ospf6-interface": "OSPF6 interface configuration.",
    "redistribute": "Redistribute configuration.",
    "passive-interface": "Passive interface configuration.",
    "summary-address": "IPv6 address summary configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "auto-cost-ref-bandwidth": {"type": "integer", "min": 1, "max": 1000000},
    "default-information-metric": {"type": "integer", "min": 1, "max": 16777214},
    "default-information-route-map": {"type": "string", "max_length": 35},
    "default-metric": {"type": "integer", "min": 1, "max": 16777214},
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
        "default-cost": {
            "type": "integer",
            "help": "Summary default cost of stub or NSSA area.",
            "default": 10,
            "min_value": 0,
            "max_value": 16777215,
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
            "help": "Enable/disable originate type 7 default into NSSA area.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "nssa-default-information-originate-metric": {
            "type": "integer",
            "help": "OSPFv3 default metric.",
            "default": 10,
            "min_value": 0,
            "max_value": 16777214,
        },
        "nssa-default-information-originate-metric-type": {
            "type": "option",
            "help": "OSPFv3 metric type for default routes.",
            "default": "2",
            "options": ["1", "2"],
        },
        "nssa-redistribution": {
            "type": "option",
            "help": "Enable/disable redistribute into NSSA area.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "authentication": {
            "type": "option",
            "help": "Authentication mode.",
            "default": "none",
            "options": ["none", "ah", "esp"],
        },
        "key-rollover-interval": {
            "type": "integer",
            "help": "Key roll-over interval.",
            "default": 300,
            "min_value": 300,
            "max_value": 216000,
        },
        "ipsec-auth-alg": {
            "type": "option",
            "help": "Authentication algorithm.",
            "default": "md5",
            "options": ["md5", "sha1", "sha256", "sha384", "sha512"],
        },
        "ipsec-enc-alg": {
            "type": "option",
            "help": "Encryption algorithm.",
            "default": "null",
            "options": ["null", "des", "3des", "aes128", "aes192", "aes256"],
        },
        "ipsec-keys": {
            "type": "string",
            "help": "IPsec authentication and encryption keys.",
        },
        "range": {
            "type": "string",
            "help": "OSPF6 area range configuration.",
        },
        "virtual-link": {
            "type": "string",
            "help": "OSPF6 virtual link configuration.",
        },
    },
    "ospf6-interface": {
        "name": {
            "type": "string",
            "help": "Interface entry name.",
            "default": "",
            "max_length": 35,
        },
        "area-id": {
            "type": "ipv4-address-any",
            "help": "A.B.C.D, in IPv4 address format.",
            "required": True,
            "default": "0.0.0.0",
        },
        "interface": {
            "type": "string",
            "help": "Configuration interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
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
            "min_value": 1,
            "max_value": 65535,
        },
        "hello-interval": {
            "type": "integer",
            "help": "Hello interval.",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable OSPF6 routing on this interface.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "network-type": {
            "type": "option",
            "help": "Network type.",
            "default": "broadcast",
            "options": ["broadcast", "point-to-point", "non-broadcast", "point-to-multipoint", "point-to-multipoint-non-broadcast"],
        },
        "bfd": {
            "type": "option",
            "help": "Enable/disable Bidirectional Forwarding Detection (BFD).",
            "default": "global",
            "options": ["global", "enable", "disable"],
        },
        "mtu": {
            "type": "integer",
            "help": "MTU for OSPFv3 packets.",
            "default": 0,
            "min_value": 576,
            "max_value": 65535,
        },
        "mtu-ignore": {
            "type": "option",
            "help": "Enable/disable ignoring MTU field in DBD packets.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "authentication": {
            "type": "option",
            "help": "Authentication mode.",
            "default": "area",
            "options": ["none", "ah", "esp", "area"],
        },
        "key-rollover-interval": {
            "type": "integer",
            "help": "Key roll-over interval.",
            "default": 300,
            "min_value": 300,
            "max_value": 216000,
        },
        "ipsec-auth-alg": {
            "type": "option",
            "help": "Authentication algorithm.",
            "default": "md5",
            "options": ["md5", "sha1", "sha256", "sha384", "sha512"],
        },
        "ipsec-enc-alg": {
            "type": "option",
            "help": "Encryption algorithm.",
            "default": "null",
            "options": ["null", "des", "3des", "aes128", "aes192", "aes256"],
        },
        "ipsec-keys": {
            "type": "string",
            "help": "IPsec authentication and encryption keys.",
        },
        "neighbor": {
            "type": "string",
            "help": "OSPFv3 neighbors are used when OSPFv3 runs on non-broadcast media.",
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
        "prefix6": {
            "type": "ipv6-network",
            "help": "IPv6 prefix.",
            "required": True,
            "default": "::/0",
        },
        "advertise": {
            "type": "option",
            "help": "Enable/disable advertise status.",
            "default": "enable",
            "options": ["disable", "enable"],
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
    "standard",
]
VALID_BODY_DEFAULT_INFORMATION_ORIGINATE = [
    "enable",
    "always",
    "disable",
]
VALID_BODY_LOG_NEIGHBOUR_CHANGES = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE = [
    "1",
    "2",
]
VALID_BODY_BFD = [
    "enable",
    "disable",
]
VALID_BODY_RESTART_MODE = [
    "none",
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


def validate_router_ospf6_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for router/ospf6."""
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


def validate_router_ospf6_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new router/ospf6 object."""
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
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
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
    if "default-information-metric-type" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-metric-type",
            payload["default-information-metric-type"],
            VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE,
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


def validate_router_ospf6_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update router/ospf6."""
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
    if "default-information-originate" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-originate",
            payload["default-information-originate"],
            VALID_BODY_DEFAULT_INFORMATION_ORIGINATE,
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
    if "default-information-metric-type" in payload:
        is_valid, error = _validate_enum_field(
            "default-information-metric-type",
            payload["default-information-metric-type"],
            VALID_BODY_DEFAULT_INFORMATION_METRIC_TYPE,
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
    "endpoint": "router/ospf6",
    "category": "cmdb",
    "api_path": "router/ospf6",
    "help": "Configure IPv6 OSPF.",
    "total_fields": 19,
    "required_fields_count": 0,
    "fields_with_defaults_count": 14,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
