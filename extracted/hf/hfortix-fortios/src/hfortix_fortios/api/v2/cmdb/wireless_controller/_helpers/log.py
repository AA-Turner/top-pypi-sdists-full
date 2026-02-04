"""Validation helpers for wireless_controller/log - Auto-generated"""

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
    "status": "enable",
    "addrgrp-log": "notification",
    "ble-log": "notification",
    "clb-log": "notification",
    "dhcp-starv-log": "notification",
    "led-sched-log": "notification",
    "radio-event-log": "notification",
    "rogue-event-log": "notification",
    "sta-event-log": "notification",
    "sta-locate-log": "notification",
    "wids-log": "notification",
    "wtp-event-log": "notification",
    "wtp-fips-event-log": "notification",
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
    "status": "option",  # Enable/disable wireless event logging.
    "addrgrp-log": "option",  # Lowest severity level to log address group message.
    "ble-log": "option",  # Lowest severity level to log BLE detection message.
    "clb-log": "option",  # Lowest severity level to log client load balancing message.
    "dhcp-starv-log": "option",  # Lowest severity level to log DHCP starvation event message.
    "led-sched-log": "option",  # Lowest severity level to log LED schedule event message.
    "radio-event-log": "option",  # Lowest severity level to log radio event message.
    "rogue-event-log": "option",  # Lowest severity level to log rogue AP event message.
    "sta-event-log": "option",  # Lowest severity level to log station event message.
    "sta-locate-log": "option",  # Lowest severity level to log station locate message.
    "wids-log": "option",  # Lowest severity level to log WIDS message.
    "wtp-event-log": "option",  # Lowest severity level to log WTP event message.
    "wtp-fips-event-log": "option",  # Lowest severity level to log FAP fips event message.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable wireless event logging.",
    "addrgrp-log": "Lowest severity level to log address group message.",
    "ble-log": "Lowest severity level to log BLE detection message.",
    "clb-log": "Lowest severity level to log client load balancing message.",
    "dhcp-starv-log": "Lowest severity level to log DHCP starvation event message.",
    "led-sched-log": "Lowest severity level to log LED schedule event message.",
    "radio-event-log": "Lowest severity level to log radio event message.",
    "rogue-event-log": "Lowest severity level to log rogue AP event message.",
    "sta-event-log": "Lowest severity level to log station event message.",
    "sta-locate-log": "Lowest severity level to log station locate message.",
    "wids-log": "Lowest severity level to log WIDS message.",
    "wtp-event-log": "Lowest severity level to log WTP event message.",
    "wtp-fips-event-log": "Lowest severity level to log FAP fips event message.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ADDRGRP_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_BLE_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_CLB_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_DHCP_STARV_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_LED_SCHED_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_RADIO_EVENT_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_ROGUE_EVENT_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_STA_EVENT_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_STA_LOCATE_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_WIDS_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_WTP_EVENT_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_BODY_WTP_FIPS_EVENT_LOG = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_log_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/log."""
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


def validate_wireless_controller_log_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/log object."""
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
    if "addrgrp-log" in payload:
        is_valid, error = _validate_enum_field(
            "addrgrp-log",
            payload["addrgrp-log"],
            VALID_BODY_ADDRGRP_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ble-log" in payload:
        is_valid, error = _validate_enum_field(
            "ble-log",
            payload["ble-log"],
            VALID_BODY_BLE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clb-log" in payload:
        is_valid, error = _validate_enum_field(
            "clb-log",
            payload["clb-log"],
            VALID_BODY_CLB_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-starv-log" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-starv-log",
            payload["dhcp-starv-log"],
            VALID_BODY_DHCP_STARV_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "led-sched-log" in payload:
        is_valid, error = _validate_enum_field(
            "led-sched-log",
            payload["led-sched-log"],
            VALID_BODY_LED_SCHED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radio-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "radio-event-log",
            payload["radio-event-log"],
            VALID_BODY_RADIO_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rogue-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "rogue-event-log",
            payload["rogue-event-log"],
            VALID_BODY_ROGUE_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sta-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "sta-event-log",
            payload["sta-event-log"],
            VALID_BODY_STA_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sta-locate-log" in payload:
        is_valid, error = _validate_enum_field(
            "sta-locate-log",
            payload["sta-locate-log"],
            VALID_BODY_STA_LOCATE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wids-log" in payload:
        is_valid, error = _validate_enum_field(
            "wids-log",
            payload["wids-log"],
            VALID_BODY_WIDS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-event-log",
            payload["wtp-event-log"],
            VALID_BODY_WTP_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-fips-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-fips-event-log",
            payload["wtp-fips-event-log"],
            VALID_BODY_WTP_FIPS_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_log_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/log."""
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
    if "addrgrp-log" in payload:
        is_valid, error = _validate_enum_field(
            "addrgrp-log",
            payload["addrgrp-log"],
            VALID_BODY_ADDRGRP_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ble-log" in payload:
        is_valid, error = _validate_enum_field(
            "ble-log",
            payload["ble-log"],
            VALID_BODY_BLE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clb-log" in payload:
        is_valid, error = _validate_enum_field(
            "clb-log",
            payload["clb-log"],
            VALID_BODY_CLB_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-starv-log" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-starv-log",
            payload["dhcp-starv-log"],
            VALID_BODY_DHCP_STARV_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "led-sched-log" in payload:
        is_valid, error = _validate_enum_field(
            "led-sched-log",
            payload["led-sched-log"],
            VALID_BODY_LED_SCHED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radio-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "radio-event-log",
            payload["radio-event-log"],
            VALID_BODY_RADIO_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rogue-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "rogue-event-log",
            payload["rogue-event-log"],
            VALID_BODY_ROGUE_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sta-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "sta-event-log",
            payload["sta-event-log"],
            VALID_BODY_STA_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sta-locate-log" in payload:
        is_valid, error = _validate_enum_field(
            "sta-locate-log",
            payload["sta-locate-log"],
            VALID_BODY_STA_LOCATE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wids-log" in payload:
        is_valid, error = _validate_enum_field(
            "wids-log",
            payload["wids-log"],
            VALID_BODY_WIDS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-event-log",
            payload["wtp-event-log"],
            VALID_BODY_WTP_EVENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wtp-fips-event-log" in payload:
        is_valid, error = _validate_enum_field(
            "wtp-fips-event-log",
            payload["wtp-fips-event-log"],
            VALID_BODY_WTP_FIPS_EVENT_LOG,
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
    "endpoint": "wireless_controller/log",
    "category": "cmdb",
    "api_path": "wireless-controller/log",
    "help": "Configure wireless controller event log filters.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
