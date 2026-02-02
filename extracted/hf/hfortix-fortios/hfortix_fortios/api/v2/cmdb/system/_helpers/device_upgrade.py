"""Validation helpers for system/device_upgrade - Auto-generated"""

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
    "known-ha-members",  # Known members of the HA cluster. If a member is missing at upgrade time, the upgrade will be cancelled.
    "serial",  # Serial number of the node to include.
    "time",  # Scheduled upgrade execution time in UTC (hh:mm yyyy/mm/dd UTC).
    "setup-time",  # Upgrade preparation start time in UTC (hh:mm yyyy/mm/dd UTC).
    "upgrade-path",  # Fortinet OS image versions to upgrade through in major-minor-patch format, such as 7-0-4.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "vdom": "",
    "status": "disabled",
    "ha-reboot-controller": "",
    "next-path-index": 0,
    "initial-version": "",
    "starter-admin": "",
    "serial": "",
    "timing": "immediate",
    "maximum-minutes": 15,
    "time": "",
    "setup-time": "",
    "upgrade-path": "",
    "device-type": "fortigate",
    "allow-download": "enable",
    "failure-reason": "none",
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
    "vdom": "string",  # Limit upgrade to this virtual domain (VDOM).
    "status": "option",  # Current status of the upgrade.
    "ha-reboot-controller": "string",  # Serial number of the FortiGate unit that will control the re
    "next-path-index": "integer",  # The index of the next image to upgrade to.
    "known-ha-members": "string",  # Known members of the HA cluster. If a member is missing at u
    "initial-version": "user",  # Firmware version when the upgrade was set up.
    "starter-admin": "string",  # Admin that started the upgrade.
    "serial": "string",  # Serial number of the node to include.
    "timing": "option",  # Run immediately or at a scheduled time.
    "maximum-minutes": "integer",  # Maximum number of minutes to allow for immediate upgrade pre
    "time": "user",  # Scheduled upgrade execution time in UTC (hh:mm yyyy/mm/dd UT
    "setup-time": "user",  # Upgrade preparation start time in UTC (hh:mm yyyy/mm/dd UTC)
    "upgrade-path": "user",  # Fortinet OS image versions to upgrade through in major-minor
    "device-type": "option",  # Fortinet device type.
    "allow-download": "option",  # Enable/disable download firmware images.
    "failure-reason": "option",  # Upgrade failure reason.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "vdom": "Limit upgrade to this virtual domain (VDOM).",
    "status": "Current status of the upgrade.",
    "ha-reboot-controller": "Serial number of the FortiGate unit that will control the reboot process for the federated upgrade of the HA cluster.",
    "next-path-index": "The index of the next image to upgrade to.",
    "known-ha-members": "Known members of the HA cluster. If a member is missing at upgrade time, the upgrade will be cancelled.",
    "initial-version": "Firmware version when the upgrade was set up.",
    "starter-admin": "Admin that started the upgrade.",
    "serial": "Serial number of the node to include.",
    "timing": "Run immediately or at a scheduled time.",
    "maximum-minutes": "Maximum number of minutes to allow for immediate upgrade preparation.",
    "time": "Scheduled upgrade execution time in UTC (hh:mm yyyy/mm/dd UTC).",
    "setup-time": "Upgrade preparation start time in UTC (hh:mm yyyy/mm/dd UTC).",
    "upgrade-path": "Fortinet OS image versions to upgrade through in major-minor-patch format, such as 7-0-4.",
    "device-type": "Fortinet device type.",
    "allow-download": "Enable/disable download firmware images.",
    "failure-reason": "Upgrade failure reason.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "vdom": {"type": "string", "max_length": 31},
    "ha-reboot-controller": {"type": "string", "max_length": 79},
    "next-path-index": {"type": "integer", "min": 0, "max": 10},
    "starter-admin": {"type": "string", "max_length": 64},
    "serial": {"type": "string", "max_length": 79},
    "maximum-minutes": {"type": "integer", "min": 5, "max": 10080},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "known-ha-members": {
        "serial": {
            "type": "string",
            "help": "Serial number of HA member",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disabled",
    "initialized",
    "downloading",
    "device-disconnected",
    "ready",
    "coordinating",
    "staging",
    "final-check",
    "upgrade-devices",
    "cancelled",
    "confirmed",
    "done",
    "failed",
]
VALID_BODY_TIMING = [
    "immediate",
    "scheduled",
]
VALID_BODY_DEVICE_TYPE = [
    "fortigate",
    "fortiswitch",
    "fortiap",
    "fortiextender",
]
VALID_BODY_ALLOW_DOWNLOAD = [
    "enable",
    "disable",
]
VALID_BODY_FAILURE_REASON = [
    "none",
    "internal",
    "timeout",
    "device-type-unsupported",
    "download-failed",
    "device-missing",
    "version-unavailable",
    "staging-failed",
    "reboot-failed",
    "device-not-reconnected",
    "node-not-ready",
    "no-final-confirmation",
    "no-confirmation-query",
    "config-error-log-nonempty",
    "csf-tree-not-supported",
    "firmware-changed",
    "node-failed",
    "image-missing",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_device_upgrade_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/device_upgrade."""
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


def validate_system_device_upgrade_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/device_upgrade object."""
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
    if "timing" in payload:
        is_valid, error = _validate_enum_field(
            "timing",
            payload["timing"],
            VALID_BODY_TIMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-type" in payload:
        is_valid, error = _validate_enum_field(
            "device-type",
            payload["device-type"],
            VALID_BODY_DEVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-download" in payload:
        is_valid, error = _validate_enum_field(
            "allow-download",
            payload["allow-download"],
            VALID_BODY_ALLOW_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "failure-reason" in payload:
        is_valid, error = _validate_enum_field(
            "failure-reason",
            payload["failure-reason"],
            VALID_BODY_FAILURE_REASON,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_device_upgrade_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/device_upgrade."""
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
    if "timing" in payload:
        is_valid, error = _validate_enum_field(
            "timing",
            payload["timing"],
            VALID_BODY_TIMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-type" in payload:
        is_valid, error = _validate_enum_field(
            "device-type",
            payload["device-type"],
            VALID_BODY_DEVICE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-download" in payload:
        is_valid, error = _validate_enum_field(
            "allow-download",
            payload["allow-download"],
            VALID_BODY_ALLOW_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "failure-reason" in payload:
        is_valid, error = _validate_enum_field(
            "failure-reason",
            payload["failure-reason"],
            VALID_BODY_FAILURE_REASON,
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
    "endpoint": "system/device_upgrade",
    "category": "cmdb",
    "api_path": "system/device-upgrade",
    "mkey": "serial",
    "mkey_type": "string",
    "help": "Independent upgrades for managed devices.",
    "total_fields": 16,
    "required_fields_count": 5,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
