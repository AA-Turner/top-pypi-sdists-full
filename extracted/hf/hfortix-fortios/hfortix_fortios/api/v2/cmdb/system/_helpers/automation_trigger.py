"""Validation helpers for system/automation_trigger - Auto-generated"""

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
    "stitch-name",  # Triggering stitch name.
    "faz-event-name",  # FortiAnalyzer event handler name.
    "serial",  # Fabric connector serial number.
    "fabric-event-name",  # Fabric connector event handler name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "trigger-type": "event-based",
    "event-type": "ioc",
    "license-type": "forticare-support",
    "report-type": "posture",
    "stitch-name": "",
    "trigger-frequency": "daily",
    "trigger-weekday": "",
    "trigger-day": 1,
    "trigger-hour": 0,
    "trigger-minute": 0,
    "trigger-datetime": "0000-00-00 00:00:00",
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
    "name": "string",  # Name.
    "description": "var-string",  # Description.
    "trigger-type": "option",  # Trigger type.
    "event-type": "option",  # Event type.
    "vdom": "string",  # Virtual domain(s) that this trigger is valid for.
    "license-type": "option",  # License type.
    "report-type": "option",  # Security Rating report.
    "stitch-name": "string",  # Triggering stitch name.
    "logid": "string",  # Log IDs to trigger event.
    "trigger-frequency": "option",  # Scheduled trigger frequency (default = daily).
    "trigger-weekday": "option",  # Day of week for trigger.
    "trigger-day": "integer",  # Day within a month to trigger.
    "trigger-hour": "integer",  # Hour of the day on which to trigger (0 - 23, default = 1).
    "trigger-minute": "integer",  # Minute of the hour on which to trigger (0 - 59, default = 0)
    "trigger-datetime": "datetime",  # Trigger date and time (YYYY-MM-DD HH:MM:SS).
    "fields": "string",  # Customized trigger field settings.
    "faz-event-name": "var-string",  # FortiAnalyzer event handler name.
    "faz-event-severity": "var-string",  # FortiAnalyzer event severity.
    "faz-event-tags": "var-string",  # FortiAnalyzer event tags.
    "serial": "var-string",  # Fabric connector serial number.
    "fabric-event-name": "var-string",  # Fabric connector event handler name.
    "fabric-event-severity": "var-string",  # Fabric connector event severity.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "description": "Description.",
    "trigger-type": "Trigger type.",
    "event-type": "Event type.",
    "vdom": "Virtual domain(s) that this trigger is valid for.",
    "license-type": "License type.",
    "report-type": "Security Rating report.",
    "stitch-name": "Triggering stitch name.",
    "logid": "Log IDs to trigger event.",
    "trigger-frequency": "Scheduled trigger frequency (default = daily).",
    "trigger-weekday": "Day of week for trigger.",
    "trigger-day": "Day within a month to trigger.",
    "trigger-hour": "Hour of the day on which to trigger (0 - 23, default = 1).",
    "trigger-minute": "Minute of the hour on which to trigger (0 - 59, default = 0).",
    "trigger-datetime": "Trigger date and time (YYYY-MM-DD HH:MM:SS).",
    "fields": "Customized trigger field settings.",
    "faz-event-name": "FortiAnalyzer event handler name.",
    "faz-event-severity": "FortiAnalyzer event severity.",
    "faz-event-tags": "FortiAnalyzer event tags.",
    "serial": "Fabric connector serial number.",
    "fabric-event-name": "Fabric connector event handler name.",
    "fabric-event-severity": "Fabric connector event severity.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "stitch-name": {"type": "string", "max_length": 35},
    "trigger-day": {"type": "integer", "min": 1, "max": 31},
    "trigger-hour": {"type": "integer", "min": 0, "max": 23},
    "trigger-minute": {"type": "integer", "min": 0, "max": 59},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "vdom": {
        "name": {
            "type": "string",
            "help": "Virtual domain name.",
            "default": "",
            "max_length": 79,
        },
    },
    "logid": {
        "id": {
            "type": "integer",
            "help": "Log ID.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
    },
    "fields": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "Name.",
            "default": "",
            "max_length": 35,
        },
        "value": {
            "type": "var-string",
            "help": "Value.",
            "max_length": 63,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TRIGGER_TYPE = [
    "event-based",
    "scheduled",
]
VALID_BODY_EVENT_TYPE = [
    "ioc",
    "event-log",
    "reboot",
    "low-memory",
    "high-cpu",
    "license-near-expiry",
    "local-cert-near-expiry",
    "ha-failover",
    "config-change",
    "security-rating-summary",
    "virus-ips-db-updated",
    "faz-event",
    "incoming-webhook",
    "fabric-event",
    "ips-logs",
    "anomaly-logs",
    "virus-logs",
    "ssh-logs",
    "webfilter-violation",
    "traffic-violation",
    "stitch",
]
VALID_BODY_LICENSE_TYPE = [
    "forticare-support",
    "fortiguard-webfilter",
    "fortiguard-antispam",
    "fortiguard-antivirus",
    "fortiguard-ips",
    "fortiguard-management",
    "forticloud",
    "any",
]
VALID_BODY_REPORT_TYPE = [
    "posture",
    "coverage",
    "optimization",
    "any",
]
VALID_BODY_TRIGGER_FREQUENCY = [
    "hourly",
    "daily",
    "weekly",
    "monthly",
    "once",
]
VALID_BODY_TRIGGER_WEEKDAY = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_automation_trigger_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/automation_trigger."""
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


def validate_system_automation_trigger_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/automation_trigger object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "trigger-type" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-type",
            payload["trigger-type"],
            VALID_BODY_TRIGGER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "event-type" in payload:
        is_valid, error = _validate_enum_field(
            "event-type",
            payload["event-type"],
            VALID_BODY_EVENT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "license-type" in payload:
        is_valid, error = _validate_enum_field(
            "license-type",
            payload["license-type"],
            VALID_BODY_LICENSE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "report-type" in payload:
        is_valid, error = _validate_enum_field(
            "report-type",
            payload["report-type"],
            VALID_BODY_REPORT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trigger-frequency" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-frequency",
            payload["trigger-frequency"],
            VALID_BODY_TRIGGER_FREQUENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trigger-weekday" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-weekday",
            payload["trigger-weekday"],
            VALID_BODY_TRIGGER_WEEKDAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_automation_trigger_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/automation_trigger."""
    # Validate enum values using central function
    if "trigger-type" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-type",
            payload["trigger-type"],
            VALID_BODY_TRIGGER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "event-type" in payload:
        is_valid, error = _validate_enum_field(
            "event-type",
            payload["event-type"],
            VALID_BODY_EVENT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "license-type" in payload:
        is_valid, error = _validate_enum_field(
            "license-type",
            payload["license-type"],
            VALID_BODY_LICENSE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "report-type" in payload:
        is_valid, error = _validate_enum_field(
            "report-type",
            payload["report-type"],
            VALID_BODY_REPORT_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trigger-frequency" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-frequency",
            payload["trigger-frequency"],
            VALID_BODY_TRIGGER_FREQUENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trigger-weekday" in payload:
        is_valid, error = _validate_enum_field(
            "trigger-weekday",
            payload["trigger-weekday"],
            VALID_BODY_TRIGGER_WEEKDAY,
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
    "endpoint": "system/automation_trigger",
    "category": "cmdb",
    "api_path": "system/automation-trigger",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Trigger for automation stitches.",
    "total_fields": 22,
    "required_fields_count": 4,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
