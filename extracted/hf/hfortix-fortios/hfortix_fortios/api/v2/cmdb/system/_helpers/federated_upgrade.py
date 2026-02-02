"""Validation helpers for system/federated_upgrade - Auto-generated"""

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
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disabled",
    "source": "user",
    "failure-reason": "none",
    "failure-device": "",
    "upgrade-id": 0,
    "next-path-index": 0,
    "ignore-signing-errors": "disable",
    "ha-reboot-controller": "",
    "initial-version": "",
    "starter-admin": "",
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
    "status": "option",  # Current status of the upgrade.
    "source": "option",  # Source that set up the federated upgrade config.
    "failure-reason": "option",  # Reason for upgrade failure.
    "failure-device": "string",  # Serial number of the node to include.
    "upgrade-id": "integer",  # Unique identifier for this upgrade.
    "next-path-index": "integer",  # The index of the next image to upgrade to.
    "ignore-signing-errors": "option",  # Allow/reject use of FortiGate firmware images that are unsig
    "ha-reboot-controller": "string",  # Serial number of the FortiGate unit that will control the re
    "known-ha-members": "string",  # Known members of the HA cluster. If a member is missing at u
    "initial-version": "user",  # Firmware version when the upgrade was set up.
    "starter-admin": "string",  # Admin that started the upgrade.
    "node-list": "string",  # Nodes which will be included in the upgrade.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Current status of the upgrade.",
    "source": "Source that set up the federated upgrade config.",
    "failure-reason": "Reason for upgrade failure.",
    "failure-device": "Serial number of the node to include.",
    "upgrade-id": "Unique identifier for this upgrade.",
    "next-path-index": "The index of the next image to upgrade to.",
    "ignore-signing-errors": "Allow/reject use of FortiGate firmware images that are unsigned.",
    "ha-reboot-controller": "Serial number of the FortiGate unit that will control the reboot process for the federated upgrade of the HA cluster.",
    "known-ha-members": "Known members of the HA cluster. If a member is missing at upgrade time, the upgrade will be cancelled.",
    "initial-version": "Firmware version when the upgrade was set up.",
    "starter-admin": "Admin that started the upgrade.",
    "node-list": "Nodes which will be included in the upgrade.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "failure-device": {"type": "string", "max_length": 79},
    "upgrade-id": {"type": "integer", "min": 0, "max": 4294967295},
    "next-path-index": {"type": "integer", "min": 0, "max": 10},
    "ha-reboot-controller": {"type": "string", "max_length": 79},
    "starter-admin": {"type": "string", "max_length": 64},
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
    "node-list": {
        "serial": {
            "type": "string",
            "help": "Serial number of the node to include.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "timing": {
            "type": "option",
            "help": "Run immediately or at a scheduled time.",
            "required": True,
            "default": "immediate",
            "options": ["immediate", "scheduled"],
        },
        "maximum-minutes": {
            "type": "integer",
            "help": "Maximum number of minutes to allow for immediate upgrade preparation.",
            "required": True,
            "default": 15,
            "min_value": 5,
            "max_value": 10080,
        },
        "time": {
            "type": "user",
            "help": "Scheduled upgrade execution time in UTC (hh:mm yyyy/mm/dd UTC).",
            "required": True,
            "default": "",
        },
        "setup-time": {
            "type": "user",
            "help": "Upgrade preparation start time in UTC (hh:mm yyyy/mm/dd UTC).",
            "required": True,
            "default": "",
        },
        "upgrade-path": {
            "type": "user",
            "help": "Fortinet OS image versions to upgrade through in major-minor-patch format, such as 7-0-4.",
            "required": True,
            "default": "",
        },
        "device-type": {
            "type": "option",
            "help": "Fortinet device type.",
            "required": True,
            "default": "fortigate",
            "options": ["fortigate", "fortiswitch", "fortiap", "fortiextender"],
        },
        "allow-download": {
            "type": "option",
            "help": "Enable/disable download firmware images.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "coordinating-fortigate": {
            "type": "string",
            "help": "Serial number of the FortiGate unit that controls this device.",
            "default": "",
            "max_length": 79,
        },
        "failure-reason": {
            "type": "option",
            "help": "Upgrade failure reason.",
            "default": "none",
            "options": ["none", "internal", "timeout", "device-type-unsupported", "download-failed", "device-missing", "version-unavailable", "staging-failed", "reboot-failed", "device-not-reconnected", "node-not-ready", "no-final-confirmation", "no-confirmation-query", "config-error-log-nonempty", "csf-tree-not-supported", "firmware-changed", "node-failed", "image-missing"],
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
VALID_BODY_SOURCE = [
    "user",
    "auto-firmware-upgrade",
    "forced-upgrade",
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
VALID_BODY_IGNORE_SIGNING_ERRORS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_federated_upgrade_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/federated_upgrade."""
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


def validate_system_federated_upgrade_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/federated_upgrade object."""
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
    if "source" in payload:
        is_valid, error = _validate_enum_field(
            "source",
            payload["source"],
            VALID_BODY_SOURCE,
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
    if "ignore-signing-errors" in payload:
        is_valid, error = _validate_enum_field(
            "ignore-signing-errors",
            payload["ignore-signing-errors"],
            VALID_BODY_IGNORE_SIGNING_ERRORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_federated_upgrade_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/federated_upgrade."""
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
    if "source" in payload:
        is_valid, error = _validate_enum_field(
            "source",
            payload["source"],
            VALID_BODY_SOURCE,
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
    if "ignore-signing-errors" in payload:
        is_valid, error = _validate_enum_field(
            "ignore-signing-errors",
            payload["ignore-signing-errors"],
            VALID_BODY_IGNORE_SIGNING_ERRORS,
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
    "endpoint": "system/federated_upgrade",
    "category": "cmdb",
    "api_path": "system/federated-upgrade",
    "help": "Coordinate federated upgrades within the Security Fabric.",
    "total_fields": 12,
    "required_fields_count": 1,
    "fields_with_defaults_count": 10,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
