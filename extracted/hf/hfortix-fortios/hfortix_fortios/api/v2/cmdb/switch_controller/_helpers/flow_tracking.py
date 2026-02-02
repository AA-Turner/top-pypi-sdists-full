"""Validation helpers for switch_controller/flow_tracking - Auto-generated"""

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
    "sample-mode": "perimeter",
    "sample-rate": 512,
    "format": "netflow9",
    "level": "ip",
    "max-export-pkt-size": 512,
    "template-export-period": 5,
    "timeout-general": 3600,
    "timeout-icmp": 300,
    "timeout-max": 604800,
    "timeout-tcp": 3600,
    "timeout-tcp-fin": 300,
    "timeout-tcp-rst": 120,
    "timeout-udp": 300,
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
    "sample-mode": "option",  # Configure sample mode for the flow tracking.
    "sample-rate": "integer",  # Configure sample rate for the perimeter and device-ingress s
    "format": "option",  # Configure flow tracking protocol.
    "collectors": "string",  # Configure collectors for the flow.
    "level": "option",  # Configure flow tracking level.
    "max-export-pkt-size": "integer",  # Configure flow max export packet size (512-9216, default=512
    "template-export-period": "integer",  # Configure template export period (1-60, default=5 minutes).
    "timeout-general": "integer",  # Configure flow session general timeout (60-604800, default=3
    "timeout-icmp": "integer",  # Configure flow session ICMP timeout (60-604800, default=300 
    "timeout-max": "integer",  # Configure flow session max timeout (60-604800, default=60480
    "timeout-tcp": "integer",  # Configure flow session TCP timeout (60-604800, default=3600 
    "timeout-tcp-fin": "integer",  # Configure flow session TCP FIN timeout (60-604800, default=3
    "timeout-tcp-rst": "integer",  # Configure flow session TCP RST timeout (60-604800, default=1
    "timeout-udp": "integer",  # Configure flow session UDP timeout (60-604800, default=300 s
    "aggregates": "string",  # Configure aggregates in which all traffic sessions matching 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "sample-mode": "Configure sample mode for the flow tracking.",
    "sample-rate": "Configure sample rate for the perimeter and device-ingress sampling(0 - 99999).",
    "format": "Configure flow tracking protocol.",
    "collectors": "Configure collectors for the flow.",
    "level": "Configure flow tracking level.",
    "max-export-pkt-size": "Configure flow max export packet size (512-9216, default=512 bytes).",
    "template-export-period": "Configure template export period (1-60, default=5 minutes).",
    "timeout-general": "Configure flow session general timeout (60-604800, default=3600 seconds).",
    "timeout-icmp": "Configure flow session ICMP timeout (60-604800, default=300 seconds).",
    "timeout-max": "Configure flow session max timeout (60-604800, default=604800 seconds).",
    "timeout-tcp": "Configure flow session TCP timeout (60-604800, default=3600 seconds).",
    "timeout-tcp-fin": "Configure flow session TCP FIN timeout (60-604800, default=300 seconds).",
    "timeout-tcp-rst": "Configure flow session TCP RST timeout (60-604800, default=120 seconds).",
    "timeout-udp": "Configure flow session UDP timeout (60-604800, default=300 seconds).",
    "aggregates": "Configure aggregates in which all traffic sessions matching the IP Address will be grouped into the same flow.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "sample-rate": {"type": "integer", "min": 0, "max": 99999},
    "max-export-pkt-size": {"type": "integer", "min": 512, "max": 9216},
    "template-export-period": {"type": "integer", "min": 1, "max": 60},
    "timeout-general": {"type": "integer", "min": 60, "max": 604800},
    "timeout-icmp": {"type": "integer", "min": 60, "max": 604800},
    "timeout-max": {"type": "integer", "min": 60, "max": 604800},
    "timeout-tcp": {"type": "integer", "min": 60, "max": 604800},
    "timeout-tcp-fin": {"type": "integer", "min": 60, "max": 604800},
    "timeout-tcp-rst": {"type": "integer", "min": 60, "max": 604800},
    "timeout-udp": {"type": "integer", "min": 60, "max": 604800},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "collectors": {
        "name": {
            "type": "string",
            "help": "Collector name.",
            "default": "",
            "max_length": 63,
        },
        "ip": {
            "type": "ipv4-address-any",
            "help": "Collector IP address.",
            "default": "0.0.0.0",
        },
        "port": {
            "type": "integer",
            "help": "Collector port number(0-65535, default:0, netflow:2055, ipfix:4739).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "transport": {
            "type": "option",
            "help": "Collector L4 transport protocol for exporting packets.",
            "default": "udp",
            "options": ["udp", "tcp", "sctp"],
        },
    },
    "aggregates": {
        "id": {
            "type": "integer",
            "help": "Aggregate id.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip": {
            "type": "ipv4-classnet",
            "help": "IP address to group all matching traffic sessions to a flow.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SAMPLE_MODE = [
    "local",
    "perimeter",
    "device-ingress",
]
VALID_BODY_FORMAT = [
    "netflow1",
    "netflow5",
    "netflow9",
    "ipfix",
]
VALID_BODY_LEVEL = [
    "vlan",
    "ip",
    "port",
    "proto",
    "mac",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_flow_tracking_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/flow_tracking."""
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


def validate_switch_controller_flow_tracking_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/flow_tracking object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "sample-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sample-mode",
            payload["sample-mode"],
            VALID_BODY_SAMPLE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "format" in payload:
        is_valid, error = _validate_enum_field(
            "format",
            payload["format"],
            VALID_BODY_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "level" in payload:
        is_valid, error = _validate_enum_field(
            "level",
            payload["level"],
            VALID_BODY_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_flow_tracking_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/flow_tracking."""
    # Validate enum values using central function
    if "sample-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sample-mode",
            payload["sample-mode"],
            VALID_BODY_SAMPLE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "format" in payload:
        is_valid, error = _validate_enum_field(
            "format",
            payload["format"],
            VALID_BODY_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "level" in payload:
        is_valid, error = _validate_enum_field(
            "level",
            payload["level"],
            VALID_BODY_LEVEL,
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
    "endpoint": "switch_controller/flow_tracking",
    "category": "cmdb",
    "api_path": "switch-controller/flow-tracking",
    "help": "Configure FortiSwitch flow tracking and export via ipfix/netflow.",
    "total_fields": 15,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
