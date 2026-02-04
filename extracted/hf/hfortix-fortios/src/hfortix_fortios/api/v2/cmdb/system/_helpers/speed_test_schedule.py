"""Validation helpers for system/speed_test_schedule - Auto-generated"""

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
    "schedules",  # Schedules for the interface.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "interface": "",
    "status": "enable",
    "diffserv": "",
    "server-name": "",
    "mode": "Auto",
    "dynamic-server": "disable",
    "ctrl-port": 5200,
    "server-port": 5201,
    "update-shaper": "disable",
    "update-inbandwidth": "disable",
    "update-outbandwidth": "disable",
    "update-interface-shaping": "disable",
    "update-inbandwidth-maximum": 0,
    "update-inbandwidth-minimum": 0,
    "update-outbandwidth-maximum": 0,
    "update-outbandwidth-minimum": 0,
    "expected-inbandwidth-minimum": 0,
    "expected-inbandwidth-maximum": 0,
    "expected-outbandwidth-minimum": 0,
    "expected-outbandwidth-maximum": 0,
    "retries": 5,
    "retry-pause": 300,
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
    "interface": "string",  # Interface name.
    "status": "option",  # Enable/disable scheduled speed test.
    "diffserv": "user",  # DSCP used for speed test.
    "server-name": "string",  # Speed test server name in system.speed-test-server list or leave it as empty to 
    "mode": "option",  # Protocol Auto(default), TCP or UDP used for speed test.
    "schedules": "string",  # Schedules for the interface.
    "dynamic-server": "option",  # Enable/disable dynamic server option.
    "ctrl-port": "integer",  # Port of the controller to get access token.
    "server-port": "integer",  # Port of the server to run speed test.
    "update-shaper": "option",  # Set egress shaper based on the test result.
    "update-inbandwidth": "option",  # Enable/disable bypassing interface's inbound bandwidth setting.
    "update-outbandwidth": "option",  # Enable/disable bypassing interface's outbound bandwidth setting.
    "update-interface-shaping": "option",  # Enable/disable using the speedtest results as reference for interface shaping (o
    "update-inbandwidth-maximum": "integer",  # Maximum downloading bandwidth (kbps) to be used in a speed test.
    "update-inbandwidth-minimum": "integer",  # Minimum downloading bandwidth (kbps) to be considered effective.
    "update-outbandwidth-maximum": "integer",  # Maximum uploading bandwidth (kbps) to be used in a speed test.
    "update-outbandwidth-minimum": "integer",  # Minimum uploading bandwidth (kbps) to be considered effective.
    "expected-inbandwidth-minimum": "integer",  # Set the minimum inbandwidth threshold for applying speedtest results on shaping-
    "expected-inbandwidth-maximum": "integer",  # Set the maximum inbandwidth threshold for applying speedtest results on shaping-
    "expected-outbandwidth-minimum": "integer",  # Set the minimum outbandwidth threshold for applying speedtest results on shaping
    "expected-outbandwidth-maximum": "integer",  # Set the maximum outbandwidth threshold for applying speedtest results on shaping
    "retries": "integer",  # Maximum number of times the FortiGate unit will attempt to contact the same serv
    "retry-pause": "integer",  # Number of seconds the FortiGate pauses between successive speed tests before try
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "interface": "Interface name.",
    "status": "Enable/disable scheduled speed test.",
    "diffserv": "DSCP used for speed test.",
    "server-name": "Speed test server name in system.speed-test-server list or leave it as empty to choose default server \"FTNT_Auto\".",
    "mode": "Protocol Auto(default), TCP or UDP used for speed test.",
    "schedules": "Schedules for the interface.",
    "dynamic-server": "Enable/disable dynamic server option.",
    "ctrl-port": "Port of the controller to get access token.",
    "server-port": "Port of the server to run speed test.",
    "update-shaper": "Set egress shaper based on the test result.",
    "update-inbandwidth": "Enable/disable bypassing interface's inbound bandwidth setting.",
    "update-outbandwidth": "Enable/disable bypassing interface's outbound bandwidth setting.",
    "update-interface-shaping": "Enable/disable using the speedtest results as reference for interface shaping (overriding configured in/outbandwidth).",
    "update-inbandwidth-maximum": "Maximum downloading bandwidth (kbps) to be used in a speed test.",
    "update-inbandwidth-minimum": "Minimum downloading bandwidth (kbps) to be considered effective.",
    "update-outbandwidth-maximum": "Maximum uploading bandwidth (kbps) to be used in a speed test.",
    "update-outbandwidth-minimum": "Minimum uploading bandwidth (kbps) to be considered effective.",
    "expected-inbandwidth-minimum": "Set the minimum inbandwidth threshold for applying speedtest results on shaping-profile.",
    "expected-inbandwidth-maximum": "Set the maximum inbandwidth threshold for applying speedtest results on shaping-profile.",
    "expected-outbandwidth-minimum": "Set the minimum outbandwidth threshold for applying speedtest results on shaping-profile.",
    "expected-outbandwidth-maximum": "Set the maximum outbandwidth threshold for applying speedtest results on shaping-profile.",
    "retries": "Maximum number of times the FortiGate unit will attempt to contact the same server before considering the speed test has failed (1 - 10, default = 5).",
    "retry-pause": "Number of seconds the FortiGate pauses between successive speed tests before trying a different server (60 - 3600, default = 300).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "interface": {"type": "string", "max_length": 35},
    "server-name": {"type": "string", "max_length": 35},
    "ctrl-port": {"type": "integer", "min": 1, "max": 65535},
    "server-port": {"type": "integer", "min": 1, "max": 65535},
    "update-inbandwidth-maximum": {"type": "integer", "min": 0, "max": 16776000},
    "update-inbandwidth-minimum": {"type": "integer", "min": 0, "max": 16776000},
    "update-outbandwidth-maximum": {"type": "integer", "min": 0, "max": 16776000},
    "update-outbandwidth-minimum": {"type": "integer", "min": 0, "max": 16776000},
    "expected-inbandwidth-minimum": {"type": "integer", "min": 0, "max": 16776000},
    "expected-inbandwidth-maximum": {"type": "integer", "min": 0, "max": 16776000},
    "expected-outbandwidth-minimum": {"type": "integer", "min": 0, "max": 16776000},
    "expected-outbandwidth-maximum": {"type": "integer", "min": 0, "max": 16776000},
    "retries": {"type": "integer", "min": 1, "max": 10},
    "retry-pause": {"type": "integer", "min": 60, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "schedules": {
        "name": {
            "type": "string",
            "help": "Name of a firewall recurring schedule.",
            "required": True,
            "default": "",
            "max_length": 31,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_MODE = [
    "UDP",
    "TCP",
    "Auto",
]
VALID_BODY_DYNAMIC_SERVER = [
    "disable",
    "enable",
]
VALID_BODY_UPDATE_SHAPER = [
    "disable",
    "local",
    "remote",
    "both",
]
VALID_BODY_UPDATE_INBANDWIDTH = [
    "disable",
    "enable",
]
VALID_BODY_UPDATE_OUTBANDWIDTH = [
    "disable",
    "enable",
]
VALID_BODY_UPDATE_INTERFACE_SHAPING = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_speed_test_schedule_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/speed_test_schedule."""
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


def validate_system_speed_test_schedule_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/speed_test_schedule object."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-server" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-server",
            payload["dynamic-server"],
            VALID_BODY_DYNAMIC_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-shaper" in payload:
        is_valid, error = _validate_enum_field(
            "update-shaper",
            payload["update-shaper"],
            VALID_BODY_UPDATE_SHAPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-inbandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "update-inbandwidth",
            payload["update-inbandwidth"],
            VALID_BODY_UPDATE_INBANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-outbandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "update-outbandwidth",
            payload["update-outbandwidth"],
            VALID_BODY_UPDATE_OUTBANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-interface-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "update-interface-shaping",
            payload["update-interface-shaping"],
            VALID_BODY_UPDATE_INTERFACE_SHAPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_speed_test_schedule_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/speed_test_schedule."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-server" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-server",
            payload["dynamic-server"],
            VALID_BODY_DYNAMIC_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-shaper" in payload:
        is_valid, error = _validate_enum_field(
            "update-shaper",
            payload["update-shaper"],
            VALID_BODY_UPDATE_SHAPER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-inbandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "update-inbandwidth",
            payload["update-inbandwidth"],
            VALID_BODY_UPDATE_INBANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-outbandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "update-outbandwidth",
            payload["update-outbandwidth"],
            VALID_BODY_UPDATE_OUTBANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-interface-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "update-interface-shaping",
            payload["update-interface-shaping"],
            VALID_BODY_UPDATE_INTERFACE_SHAPING,
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
    "endpoint": "system/speed_test_schedule",
    "category": "cmdb",
    "api_path": "system/speed-test-schedule",
    "mkey": "interface",
    "mkey_type": "string",
    "help": "Speed test schedule for each interface.",
    "total_fields": 23,
    "required_fields_count": 1,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
