"""Validation helpers for wireless_controller/qos_profile - Auto-generated"""

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
    "name": "",
    "comment": "",
    "uplink": 0,
    "downlink": 0,
    "uplink-sta": 0,
    "downlink-sta": 0,
    "burst": "disable",
    "wmm": "enable",
    "wmm-uapsd": "enable",
    "call-admission-control": "disable",
    "call-capacity": 10,
    "bandwidth-admission-control": "disable",
    "bandwidth-capacity": 2000,
    "dscp-wmm-mapping": "disable",
    "wmm-dscp-marking": "disable",
    "wmm-vo-dscp": 48,
    "wmm-vi-dscp": 32,
    "wmm-be-dscp": 0,
    "wmm-bk-dscp": 8,
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
    "name": "string",  # WiFi QoS profile name.
    "comment": "string",  # Comment.
    "uplink": "integer",  # Maximum uplink bandwidth for Virtual Access Points (VAPs) (0
    "downlink": "integer",  # Maximum downlink bandwidth for Virtual Access Points (VAPs) 
    "uplink-sta": "integer",  # Maximum uplink bandwidth for clients (0 - 2097152 Kbps, defa
    "downlink-sta": "integer",  # Maximum downlink bandwidth for clients (0 - 2097152 Kbps, de
    "burst": "option",  # Enable/disable client rate burst.
    "wmm": "option",  # Enable/disable WiFi multi-media (WMM) control.
    "wmm-uapsd": "option",  # Enable/disable WMM Unscheduled Automatic Power Save Delivery
    "call-admission-control": "option",  # Enable/disable WMM call admission control.
    "call-capacity": "integer",  # Maximum number of Voice over WLAN (VoWLAN) phones allowed (0
    "bandwidth-admission-control": "option",  # Enable/disable WMM bandwidth admission control.
    "bandwidth-capacity": "integer",  # Maximum bandwidth capacity allowed (1 - 600000 Kbps, default
    "dscp-wmm-mapping": "option",  # Enable/disable Differentiated Services Code Point (DSCP) map
    "dscp-wmm-vo": "string",  # DSCP mapping for voice access (default = 48 56).
    "dscp-wmm-vi": "string",  # DSCP mapping for video access (default = 32 40).
    "dscp-wmm-be": "string",  # DSCP mapping for best effort access (default = 0 24).
    "dscp-wmm-bk": "string",  # DSCP mapping for background access (default = 8 16).
    "wmm-dscp-marking": "option",  # Enable/disable WMM Differentiated Services Code Point (DSCP)
    "wmm-vo-dscp": "integer",  # DSCP marking for voice access (default = 48).
    "wmm-vi-dscp": "integer",  # DSCP marking for video access (default = 32).
    "wmm-be-dscp": "integer",  # DSCP marking for best effort access (default = 0).
    "wmm-bk-dscp": "integer",  # DSCP marking for background access (default = 8).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WiFi QoS profile name.",
    "comment": "Comment.",
    "uplink": "Maximum uplink bandwidth for Virtual Access Points (VAPs) (0 - 2097152 Kbps, default = 0, 0 means no limit).",
    "downlink": "Maximum downlink bandwidth for Virtual Access Points (VAPs) (0 - 2097152 Kbps, default = 0, 0 means no limit).",
    "uplink-sta": "Maximum uplink bandwidth for clients (0 - 2097152 Kbps, default = 0, 0 means no limit).",
    "downlink-sta": "Maximum downlink bandwidth for clients (0 - 2097152 Kbps, default = 0, 0 means no limit).",
    "burst": "Enable/disable client rate burst.",
    "wmm": "Enable/disable WiFi multi-media (WMM) control.",
    "wmm-uapsd": "Enable/disable WMM Unscheduled Automatic Power Save Delivery (U-APSD) power save mode.",
    "call-admission-control": "Enable/disable WMM call admission control.",
    "call-capacity": "Maximum number of Voice over WLAN (VoWLAN) phones allowed (0 - 60, default = 10).",
    "bandwidth-admission-control": "Enable/disable WMM bandwidth admission control.",
    "bandwidth-capacity": "Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).",
    "dscp-wmm-mapping": "Enable/disable Differentiated Services Code Point (DSCP) mapping.",
    "dscp-wmm-vo": "DSCP mapping for voice access (default = 48 56).",
    "dscp-wmm-vi": "DSCP mapping for video access (default = 32 40).",
    "dscp-wmm-be": "DSCP mapping for best effort access (default = 0 24).",
    "dscp-wmm-bk": "DSCP mapping for background access (default = 8 16).",
    "wmm-dscp-marking": "Enable/disable WMM Differentiated Services Code Point (DSCP) marking.",
    "wmm-vo-dscp": "DSCP marking for voice access (default = 48).",
    "wmm-vi-dscp": "DSCP marking for video access (default = 32).",
    "wmm-be-dscp": "DSCP marking for best effort access (default = 0).",
    "wmm-bk-dscp": "DSCP marking for background access (default = 8).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comment": {"type": "string", "max_length": 63},
    "uplink": {"type": "integer", "min": 0, "max": 2097152},
    "downlink": {"type": "integer", "min": 0, "max": 2097152},
    "uplink-sta": {"type": "integer", "min": 0, "max": 2097152},
    "downlink-sta": {"type": "integer", "min": 0, "max": 2097152},
    "call-capacity": {"type": "integer", "min": 0, "max": 60},
    "bandwidth-capacity": {"type": "integer", "min": 1, "max": 600000},
    "wmm-vo-dscp": {"type": "integer", "min": 0, "max": 63},
    "wmm-vi-dscp": {"type": "integer", "min": 0, "max": 63},
    "wmm-be-dscp": {"type": "integer", "min": 0, "max": 63},
    "wmm-bk-dscp": {"type": "integer", "min": 0, "max": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "dscp-wmm-vo": {
        "id": {
            "type": "integer",
            "help": "DSCP WMM mapping numbers (0 - 63).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "dscp-wmm-vi": {
        "id": {
            "type": "integer",
            "help": "DSCP WMM mapping numbers (0 - 63).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "dscp-wmm-be": {
        "id": {
            "type": "integer",
            "help": "DSCP WMM mapping numbers (0 - 63).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "dscp-wmm-bk": {
        "id": {
            "type": "integer",
            "help": "DSCP WMM mapping numbers (0 - 63).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_BURST = [
    "enable",
    "disable",
]
VALID_BODY_WMM = [
    "enable",
    "disable",
]
VALID_BODY_WMM_UAPSD = [
    "enable",
    "disable",
]
VALID_BODY_CALL_ADMISSION_CONTROL = [
    "enable",
    "disable",
]
VALID_BODY_BANDWIDTH_ADMISSION_CONTROL = [
    "enable",
    "disable",
]
VALID_BODY_DSCP_WMM_MAPPING = [
    "enable",
    "disable",
]
VALID_BODY_WMM_DSCP_MARKING = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_qos_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/qos_profile."""
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


def validate_wireless_controller_qos_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/qos_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "burst" in payload:
        is_valid, error = _validate_enum_field(
            "burst",
            payload["burst"],
            VALID_BODY_BURST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm" in payload:
        is_valid, error = _validate_enum_field(
            "wmm",
            payload["wmm"],
            VALID_BODY_WMM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm-uapsd" in payload:
        is_valid, error = _validate_enum_field(
            "wmm-uapsd",
            payload["wmm-uapsd"],
            VALID_BODY_WMM_UAPSD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "call-admission-control" in payload:
        is_valid, error = _validate_enum_field(
            "call-admission-control",
            payload["call-admission-control"],
            VALID_BODY_CALL_ADMISSION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bandwidth-admission-control" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-admission-control",
            payload["bandwidth-admission-control"],
            VALID_BODY_BANDWIDTH_ADMISSION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dscp-wmm-mapping" in payload:
        is_valid, error = _validate_enum_field(
            "dscp-wmm-mapping",
            payload["dscp-wmm-mapping"],
            VALID_BODY_DSCP_WMM_MAPPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm-dscp-marking" in payload:
        is_valid, error = _validate_enum_field(
            "wmm-dscp-marking",
            payload["wmm-dscp-marking"],
            VALID_BODY_WMM_DSCP_MARKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_qos_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/qos_profile."""
    # Validate enum values using central function
    if "burst" in payload:
        is_valid, error = _validate_enum_field(
            "burst",
            payload["burst"],
            VALID_BODY_BURST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm" in payload:
        is_valid, error = _validate_enum_field(
            "wmm",
            payload["wmm"],
            VALID_BODY_WMM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm-uapsd" in payload:
        is_valid, error = _validate_enum_field(
            "wmm-uapsd",
            payload["wmm-uapsd"],
            VALID_BODY_WMM_UAPSD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "call-admission-control" in payload:
        is_valid, error = _validate_enum_field(
            "call-admission-control",
            payload["call-admission-control"],
            VALID_BODY_CALL_ADMISSION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bandwidth-admission-control" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-admission-control",
            payload["bandwidth-admission-control"],
            VALID_BODY_BANDWIDTH_ADMISSION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dscp-wmm-mapping" in payload:
        is_valid, error = _validate_enum_field(
            "dscp-wmm-mapping",
            payload["dscp-wmm-mapping"],
            VALID_BODY_DSCP_WMM_MAPPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wmm-dscp-marking" in payload:
        is_valid, error = _validate_enum_field(
            "wmm-dscp-marking",
            payload["wmm-dscp-marking"],
            VALID_BODY_WMM_DSCP_MARKING,
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
    "endpoint": "wireless_controller/qos_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/qos-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure WiFi quality of service (QoS) profiles.",
    "total_fields": 23,
    "required_fields_count": 0,
    "fields_with_defaults_count": 19,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
