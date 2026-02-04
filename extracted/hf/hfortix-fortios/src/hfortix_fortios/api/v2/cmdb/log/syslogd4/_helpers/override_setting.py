"""Validation helpers for log/syslogd4/override_setting - Auto-generated"""

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
    "server",  # Address of remote syslog server.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "server": "",
    "mode": "udp",
    "use-management-vdom": "disable",
    "port": 514,
    "facility": "local7",
    "source-ip-interface": "",
    "source-ip": "",
    "format": "default",
    "priority": "default",
    "max-log-rate": 0,
    "enc-algorithm": "disable",
    "ssl-min-proto-version": "default",
    "certificate": "",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "status": "option",  # Enable/disable remote syslog logging.
    "server": "string",  # Address of remote syslog server.
    "mode": "option",  # Remote syslog logging over UDP/Reliable TCP.
    "use-management-vdom": "option",  # Enable/disable use of management VDOM as source VDOM for logs sent to syslog ser
    "port": "integer",  # Server listen port.
    "facility": "option",  # Remote syslog facility.
    "source-ip-interface": "string",  # Source interface of syslog.
    "source-ip": "string",  # Source IP address of syslog.
    "format": "option",  # Log format.
    "priority": "option",  # Set log transmission priority.
    "max-log-rate": "integer",  # Syslog maximum log rate in MBps (0 = unlimited).
    "enc-algorithm": "option",  # Enable/disable reliable syslogging with TLS encryption.
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (default is to follow
    "certificate": "string",  # Certificate used to communicate with Syslog server.
    "custom-field-name": "string",  # Custom field name for CEF format logging.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable remote syslog logging.",
    "server": "Address of remote syslog server.",
    "mode": "Remote syslog logging over UDP/Reliable TCP.",
    "use-management-vdom": "Enable/disable use of management VDOM as source VDOM for logs sent to syslog server.",
    "port": "Server listen port.",
    "facility": "Remote syslog facility.",
    "source-ip-interface": "Source interface of syslog.",
    "source-ip": "Source IP address of syslog.",
    "format": "Log format.",
    "priority": "Set log transmission priority.",
    "max-log-rate": "Syslog maximum log rate in MBps (0 = unlimited).",
    "enc-algorithm": "Enable/disable reliable syslogging with TLS encryption.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "certificate": "Certificate used to communicate with Syslog server.",
    "custom-field-name": "Custom field name for CEF format logging.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "server": {"type": "string", "max_length": 127},
    "port": {"type": "integer", "min": 0, "max": 65535},
    "source-ip-interface": {"type": "string", "max_length": 15},
    "source-ip": {"type": "string", "max_length": 63},
    "max-log-rate": {"type": "integer", "min": 0, "max": 100000},
    "certificate": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "custom-field-name": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "name": {
            "type": "string",
            "help": "Field name [A-Za-z0-9_].",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "custom": {
            "type": "string",
            "help": "Field custom name [A-Za-z0-9_].",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MODE = [
    "udp",
    "legacy-reliable",
    "reliable",
]
VALID_BODY_USE_MANAGEMENT_VDOM = [
    "enable",
    "disable",
]
VALID_BODY_FACILITY = [
    "kernel",
    "user",
    "mail",
    "daemon",
    "auth",
    "syslog",
    "lpr",
    "news",
    "uucp",
    "cron",
    "authpriv",
    "ftp",
    "ntp",
    "audit",
    "alert",
    "clock",
    "local0",
    "local1",
    "local2",
    "local3",
    "local4",
    "local5",
    "local6",
    "local7",
]
VALID_BODY_FORMAT = [
    "default",
    "csv",
    "cef",
    "rfc5424",
    "json",
]
VALID_BODY_PRIORITY = [
    "default",
    "low",
]
VALID_BODY_ENC_ALGORITHM = [
    "high-medium",
    "high",
    "low",
    "disable",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_log_syslogd4_override_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/syslogd4/override_setting."""
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


def validate_log_syslogd4_override_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/syslogd4/override_setting object."""
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
    if "use-management-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "use-management-vdom",
            payload["use-management-vdom"],
            VALID_BODY_USE_MANAGEMENT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "facility" in payload:
        is_valid, error = _validate_enum_field(
            "facility",
            payload["facility"],
            VALID_BODY_FACILITY,
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
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_log_syslogd4_override_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/syslogd4/override_setting."""
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
    if "use-management-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "use-management-vdom",
            payload["use-management-vdom"],
            VALID_BODY_USE_MANAGEMENT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "facility" in payload:
        is_valid, error = _validate_enum_field(
            "facility",
            payload["facility"],
            VALID_BODY_FACILITY,
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
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
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
    "endpoint": "log/syslogd4/override_setting",
    "category": "cmdb",
    "api_path": "log.syslogd4/override-setting",
    "help": "Override settings for remote syslog server.",
    "total_fields": 18,
    "required_fields_count": 2,
    "fields_with_defaults_count": 17,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
