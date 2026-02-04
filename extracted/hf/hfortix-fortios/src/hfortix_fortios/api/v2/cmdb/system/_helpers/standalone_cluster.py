"""Validation helpers for system/standalone_cluster - Auto-generated"""

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
    "psksecret",  # Pre-shared secret for session synchronization (ASCII string or hexadecimal encoded with a leading 0x).
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "standalone-group-id": 0,
    "group-member-id": 0,
    "layer2-connection": "unavailable",
    "session-sync-dev": "",
    "encryption": "disable",
    "asymmetric-traffic-control": "cps-preferred",
    "helper-traffic-bounce": "enable",
    "utm-traffic-bounce": "enable",
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
    "standalone-group-id": "integer",  # Cluster group ID (0 - 255). Must be the same for all members.
    "group-member-id": "integer",  # Cluster member ID (0 - 15).
    "layer2-connection": "option",  # Indicate whether layer 2 connections are present among FGSP members.
    "session-sync-dev": "user",  # Offload session-sync process to kernel and sync sessions using connected interfa
    "encryption": "option",  # Enable/disable encryption when synchronizing sessions.
    "psksecret": "password-3",  # Pre-shared secret for session synchronization (ASCII string or hexadecimal encod
    "asymmetric-traffic-control": "option",  # Asymmetric traffic control mode.
    "cluster-peer": "string",  # Configure FortiGate Session Life Support Protocol (FGSP) session synchronization
    "monitor-interface": "string",  # Configure a list of interfaces on which to monitor itself. Monitoring is perform
    "pingsvr-monitor-interface": "string",  # List of pingsvr monitor interface to check for remote IP monitoring.
    "monitor-prefix": "string",  # Configure a list of routing prefixes to monitor.
    "helper-traffic-bounce": "option",  # Enable/disable helper related traffic bounce.
    "utm-traffic-bounce": "option",  # Enable/disable UTM related traffic bounce.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "standalone-group-id": "Cluster group ID (0 - 255). Must be the same for all members.",
    "group-member-id": "Cluster member ID (0 - 15).",
    "layer2-connection": "Indicate whether layer 2 connections are present among FGSP members.",
    "session-sync-dev": "Offload session-sync process to kernel and sync sessions using connected interface(s) directly.",
    "encryption": "Enable/disable encryption when synchronizing sessions.",
    "psksecret": "Pre-shared secret for session synchronization (ASCII string or hexadecimal encoded with a leading 0x).",
    "asymmetric-traffic-control": "Asymmetric traffic control mode.",
    "cluster-peer": "Configure FortiGate Session Life Support Protocol (FGSP) session synchronization.",
    "monitor-interface": "Configure a list of interfaces on which to monitor itself. Monitoring is performed on the status of the interface.",
    "pingsvr-monitor-interface": "List of pingsvr monitor interface to check for remote IP monitoring.",
    "monitor-prefix": "Configure a list of routing prefixes to monitor.",
    "helper-traffic-bounce": "Enable/disable helper related traffic bounce.",
    "utm-traffic-bounce": "Enable/disable UTM related traffic bounce.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "standalone-group-id": {"type": "integer", "min": 0, "max": 255},
    "group-member-id": {"type": "integer", "min": 0, "max": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "cluster-peer": {
        "sync-id": {
            "type": "integer",
            "help": "Sync ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "peervd": {
            "type": "string",
            "help": "VDOM that contains the session synchronization link interface on the peer unit. Usually both peers would have the same peervd.",
            "default": "root",
            "max_length": 31,
        },
        "peerip": {
            "type": "ipv4-address",
            "help": "IP address of the interface on the peer unit that is used for the session synchronization link.",
            "default": "0.0.0.0",
        },
        "syncvd": {
            "type": "string",
            "help": "Sessions from these VDOMs are synchronized using this session synchronization configuration.",
        },
        "down-intfs-before-sess-sync": {
            "type": "string",
            "help": "List of interfaces to be turned down before session synchronization is complete.",
        },
        "hb-interval": {
            "type": "integer",
            "help": "Heartbeat interval (1 - 20 (100*ms). Increase to reduce false positives.",
            "default": 2,
            "min_value": 1,
            "max_value": 20,
        },
        "hb-lost-threshold": {
            "type": "integer",
            "help": "Lost heartbeat threshold (1 - 60). Increase to reduce false positives.",
            "default": 10,
            "min_value": 1,
            "max_value": 60,
        },
        "ipsec-tunnel-sync": {
            "type": "option",
            "help": "Enable/disable IPsec tunnel synchronization.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "secondary-add-ipsec-routes": {
            "type": "option",
            "help": "Enable/disable IKE route announcement on the backup unit.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "session-sync-filter": {
            "type": "string",
            "help": "Add one or more filters if you only want to synchronize some sessions. Use the filter to configure the types of sessions to synchronize.",
        },
    },
    "monitor-interface": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "pingsvr-monitor-interface": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "monitor-prefix": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "vdom": {
            "type": "string",
            "help": "VDOM name.",
            "required": True,
            "default": "",
            "max_length": 31,
        },
        "vrf": {
            "type": "integer",
            "help": "VRF ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 511,
        },
        "prefix": {
            "type": "ipv4-classnet-any",
            "help": "Prefix.",
            "default": "0.0.0.0 0.0.0.0",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_LAYER2_CONNECTION = [
    "available",
    "unavailable",
]
VALID_BODY_ENCRYPTION = [
    "enable",
    "disable",
]
VALID_BODY_ASYMMETRIC_TRAFFIC_CONTROL = [
    "cps-preferred",
    "strict-anti-replay",
]
VALID_BODY_HELPER_TRAFFIC_BOUNCE = [
    "enable",
    "disable",
]
VALID_BODY_UTM_TRAFFIC_BOUNCE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_standalone_cluster_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/standalone_cluster."""
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


def validate_system_standalone_cluster_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/standalone_cluster object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "layer2-connection" in payload:
        is_valid, error = _validate_enum_field(
            "layer2-connection",
            payload["layer2-connection"],
            VALID_BODY_LAYER2_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymmetric-traffic-control" in payload:
        is_valid, error = _validate_enum_field(
            "asymmetric-traffic-control",
            payload["asymmetric-traffic-control"],
            VALID_BODY_ASYMMETRIC_TRAFFIC_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "helper-traffic-bounce" in payload:
        is_valid, error = _validate_enum_field(
            "helper-traffic-bounce",
            payload["helper-traffic-bounce"],
            VALID_BODY_HELPER_TRAFFIC_BOUNCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-traffic-bounce" in payload:
        is_valid, error = _validate_enum_field(
            "utm-traffic-bounce",
            payload["utm-traffic-bounce"],
            VALID_BODY_UTM_TRAFFIC_BOUNCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_standalone_cluster_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/standalone_cluster."""
    # Validate enum values using central function
    if "layer2-connection" in payload:
        is_valid, error = _validate_enum_field(
            "layer2-connection",
            payload["layer2-connection"],
            VALID_BODY_LAYER2_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymmetric-traffic-control" in payload:
        is_valid, error = _validate_enum_field(
            "asymmetric-traffic-control",
            payload["asymmetric-traffic-control"],
            VALID_BODY_ASYMMETRIC_TRAFFIC_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "helper-traffic-bounce" in payload:
        is_valid, error = _validate_enum_field(
            "helper-traffic-bounce",
            payload["helper-traffic-bounce"],
            VALID_BODY_HELPER_TRAFFIC_BOUNCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-traffic-bounce" in payload:
        is_valid, error = _validate_enum_field(
            "utm-traffic-bounce",
            payload["utm-traffic-bounce"],
            VALID_BODY_UTM_TRAFFIC_BOUNCE,
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
    "endpoint": "system/standalone_cluster",
    "category": "cmdb",
    "api_path": "system/standalone-cluster",
    "help": "Configure FortiGate Session Life Support Protocol (FGSP) cluster attributes.",
    "total_fields": 13,
    "required_fields_count": 1,
    "fields_with_defaults_count": 8,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
