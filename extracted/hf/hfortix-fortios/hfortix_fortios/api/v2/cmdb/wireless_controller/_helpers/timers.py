"""Validation helpers for wireless_controller/timers - Auto-generated"""

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
    "echo-interval": 30,
    "nat-session-keep-alive": 0,
    "discovery-interval": 5,
    "client-idle-timeout": 300,
    "client-idle-rehome-timeout": 20,
    "auth-timeout": 5,
    "rogue-ap-log": 0,
    "fake-ap-log": 1,
    "sta-offline-cleanup": 300,
    "sta-offline-ip2mac-cleanup": 300,
    "sta-cap-cleanup": 0,
    "rogue-ap-cleanup": 0,
    "rogue-sta-cleanup": 0,
    "wids-entry-cleanup": 0,
    "ble-device-cleanup": 60,
    "sta-stats-interval": 10,
    "vap-stats-interval": 15,
    "radio-stats-interval": 15,
    "sta-capability-interval": 30,
    "sta-locate-timer": 1800,
    "ipsec-intf-cleanup": 120,
    "ble-scan-report-intv": 30,
    "drma-interval": 60,
    "ap-reboot-wait-interval1": 0,
    "ap-reboot-wait-time": "",
    "ap-reboot-wait-interval2": 0,
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
    "echo-interval": "integer",  # Time between echo requests sent by the managed WTP, AP, or F
    "nat-session-keep-alive": "integer",  # Maximal time in seconds between control requests sent by the
    "discovery-interval": "integer",  # Time between discovery requests (2 - 180 sec, default = 5).
    "client-idle-timeout": "integer",  # Time after which a client is considered idle and times out (
    "client-idle-rehome-timeout": "integer",  # Time after which a client is considered idle and disconnecte
    "auth-timeout": "integer",  # Time after which a client is considered failed in RADIUS aut
    "rogue-ap-log": "integer",  # Time between logging rogue AP messages if periodic rogue AP 
    "fake-ap-log": "integer",  # Time between recording logs about fake APs if periodic fake 
    "sta-offline-cleanup": "integer",  # Time period in seconds to keep station offline data after it
    "sta-offline-ip2mac-cleanup": "integer",  # Time period in seconds to keep station offline Ip2mac data a
    "sta-cap-cleanup": "integer",  # Time period in minutes to keep station capability data after
    "rogue-ap-cleanup": "integer",  # Time period in minutes to keep rogue AP after it is gone (de
    "rogue-sta-cleanup": "integer",  # Time period in minutes to keep rogue station after it is gon
    "wids-entry-cleanup": "integer",  # Time period in minutes to keep wids entry after it is gone (
    "ble-device-cleanup": "integer",  # Time period in minutes to keep BLE device after it is gone (
    "sta-stats-interval": "integer",  # Time between running client (station) reports (1 - 255 sec, 
    "vap-stats-interval": "integer",  # Time between running Virtual Access Point (VAP) reports (1 -
    "radio-stats-interval": "integer",  # Time between running radio reports (1 - 255 sec, default = 1
    "sta-capability-interval": "integer",  # Time between running station capability reports (1 - 255 sec
    "sta-locate-timer": "integer",  # Time between running client presence flushes to remove clien
    "ipsec-intf-cleanup": "integer",  # Time period to keep IPsec VPN interfaces up after WTP sessio
    "ble-scan-report-intv": "integer",  # Time between running Bluetooth Low Energy (BLE) reports (10 
    "drma-interval": "integer",  # Dynamic radio mode assignment (DRMA) schedule interval in mi
    "ap-reboot-wait-interval1": "integer",  # Time in minutes to wait before AP reboots when there is no c
    "ap-reboot-wait-time": "string",  # Time to reboot the AP when there is no controller detected a
    "ap-reboot-wait-interval2": "integer",  # Time in minutes to wait before AP reboots when there is no c
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "echo-interval": "Time between echo requests sent by the managed WTP, AP, or FortiAP (1 - 255 sec, default = 30).",
    "nat-session-keep-alive": "Maximal time in seconds between control requests sent by the managed WTP, AP, or FortiAP (0 - 255 sec, default = 0).",
    "discovery-interval": "Time between discovery requests (2 - 180 sec, default = 5).",
    "client-idle-timeout": "Time after which a client is considered idle and times out (20 - 3600 sec, default = 300, 0 for no timeout).",
    "client-idle-rehome-timeout": "Time after which a client is considered idle and disconnected from the home controller (2 - 3600 sec, default = 20, 0 for no timeout).",
    "auth-timeout": "Time after which a client is considered failed in RADIUS authentication and times out (5 - 30 sec, default = 5).",
    "rogue-ap-log": "Time between logging rogue AP messages if periodic rogue AP logging is configured (0 - 1440 min, default = 0).",
    "fake-ap-log": "Time between recording logs about fake APs if periodic fake AP logging is configured (1 - 1440 min, default = 1).",
    "sta-offline-cleanup": "Time period in seconds to keep station offline data after it is gone (default = 300).",
    "sta-offline-ip2mac-cleanup": "Time period in seconds to keep station offline Ip2mac data after it is gone (default = 300).",
    "sta-cap-cleanup": "Time period in minutes to keep station capability data after it is gone (default = 0).",
    "rogue-ap-cleanup": "Time period in minutes to keep rogue AP after it is gone (default = 0).",
    "rogue-sta-cleanup": "Time period in minutes to keep rogue station after it is gone (default = 0).",
    "wids-entry-cleanup": "Time period in minutes to keep wids entry after it is gone (default = 0).",
    "ble-device-cleanup": "Time period in minutes to keep BLE device after it is gone (default = 60).",
    "sta-stats-interval": "Time between running client (station) reports (1 - 255 sec, default = 10).",
    "vap-stats-interval": "Time between running Virtual Access Point (VAP) reports (1 - 255 sec, default = 15).",
    "radio-stats-interval": "Time between running radio reports (1 - 255 sec, default = 15).",
    "sta-capability-interval": "Time between running station capability reports (1 - 255 sec, default = 30).",
    "sta-locate-timer": "Time between running client presence flushes to remove clients that are listed but no longer present (0 - 86400 sec, default = 1800).",
    "ipsec-intf-cleanup": "Time period to keep IPsec VPN interfaces up after WTP sessions are disconnected (30 - 3600 sec, default = 120).",
    "ble-scan-report-intv": "Time between running Bluetooth Low Energy (BLE) reports (10 - 3600 sec, default = 30).",
    "drma-interval": "Dynamic radio mode assignment (DRMA) schedule interval in minutes (1 - 1440, default = 60).",
    "ap-reboot-wait-interval1": "Time in minutes to wait before AP reboots when there is no controller detected (5 - 65535, default = 0, 0 for no reboot).",
    "ap-reboot-wait-time": "Time to reboot the AP when there is no controller detected and standalone SSIDs are pushed to the AP in the previous session, format hh:mm.",
    "ap-reboot-wait-interval2": "Time in minutes to wait before AP reboots when there is no controller detected and standalone SSIDs are pushed to the AP in the previous session (5 - 65535, default = 0, 0 for no reboot).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "echo-interval": {"type": "integer", "min": 1, "max": 255},
    "nat-session-keep-alive": {"type": "integer", "min": 0, "max": 255},
    "discovery-interval": {"type": "integer", "min": 2, "max": 180},
    "client-idle-timeout": {"type": "integer", "min": 20, "max": 3600},
    "client-idle-rehome-timeout": {"type": "integer", "min": 2, "max": 3600},
    "auth-timeout": {"type": "integer", "min": 5, "max": 30},
    "rogue-ap-log": {"type": "integer", "min": 0, "max": 1440},
    "fake-ap-log": {"type": "integer", "min": 1, "max": 1440},
    "sta-offline-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "sta-offline-ip2mac-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "sta-cap-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "rogue-ap-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "rogue-sta-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "wids-entry-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "ble-device-cleanup": {"type": "integer", "min": 0, "max": 4294967295},
    "sta-stats-interval": {"type": "integer", "min": 1, "max": 255},
    "vap-stats-interval": {"type": "integer", "min": 1, "max": 255},
    "radio-stats-interval": {"type": "integer", "min": 1, "max": 255},
    "sta-capability-interval": {"type": "integer", "min": 1, "max": 255},
    "sta-locate-timer": {"type": "integer", "min": 0, "max": 86400},
    "ipsec-intf-cleanup": {"type": "integer", "min": 30, "max": 3600},
    "ble-scan-report-intv": {"type": "integer", "min": 10, "max": 3600},
    "drma-interval": {"type": "integer", "min": 1, "max": 1440},
    "ap-reboot-wait-interval1": {"type": "integer", "min": 5, "max": 65535},
    "ap-reboot-wait-time": {"type": "string", "max_length": 7},
    "ap-reboot-wait-interval2": {"type": "integer", "min": 5, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_timers_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/timers."""
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


def validate_wireless_controller_timers_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/timers object."""
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


def validate_wireless_controller_timers_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/timers."""
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
    "endpoint": "wireless_controller/timers",
    "category": "cmdb",
    "api_path": "wireless-controller/timers",
    "help": "Configure CAPWAP timers.",
    "total_fields": 26,
    "required_fields_count": 0,
    "fields_with_defaults_count": 26,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
