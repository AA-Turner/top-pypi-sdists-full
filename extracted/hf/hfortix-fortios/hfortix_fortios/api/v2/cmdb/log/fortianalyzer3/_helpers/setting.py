"""Validation helpers for log/fortianalyzer3/setting - Auto-generated"""

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
    "server",  # The remote FortiAnalyzer.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "ips-archive": "enable",
    "server": "",
    "alt-server": "",
    "fallback-to-primary": "enable",
    "certificate-verification": "enable",
    "server-cert-ca": "",
    "preshared-key": "",
    "access-config": "enable",
    "hmac-algorithm": "sha256",
    "enc-algorithm": "high",
    "ssl-min-proto-version": "default",
    "conn-timeout": 10,
    "monitor-keepalive-period": 5,
    "monitor-failure-retry-period": 5,
    "certificate": "",
    "source-ip": "",
    "upload-option": "5-minute",
    "upload-interval": "daily",
    "upload-day": "",
    "upload-time": "",
    "reliable": "disable",
    "priority": "default",
    "max-log-rate": 0,
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
    "status": "option",  # Enable/disable logging to FortiAnalyzer.
    "ips-archive": "option",  # Enable/disable IPS packet archive logging.
    "server": "string",  # The remote FortiAnalyzer.
    "alt-server": "string",  # Alternate FortiAnalyzer.
    "fallback-to-primary": "option",  # Enable/disable this FortiGate unit to fallback to the primar
    "certificate-verification": "option",  # Enable/disable identity verification of FortiAnalyzer by use
    "serial": "string",  # Serial numbers of the FortiAnalyzer.
    "server-cert-ca": "string",  # Mandatory CA on FortiGate in certificate chain of server.
    "preshared-key": "string",  # Preshared-key used for auto-authorization on FortiAnalyzer.
    "access-config": "option",  # Enable/disable FortiAnalyzer access to configuration and dat
    "hmac-algorithm": "option",  # OFTP login hash algorithm.
    "enc-algorithm": "option",  # Configure the level of SSL protection for secure communicati
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (
    "conn-timeout": "integer",  # FortiAnalyzer connection time-out in seconds (for status and
    "monitor-keepalive-period": "integer",  # Time between OFTP keepalives in seconds (for status and log 
    "monitor-failure-retry-period": "integer",  # Time between FortiAnalyzer connection retries in seconds (fo
    "certificate": "string",  # Certificate used to communicate with FortiAnalyzer.
    "source-ip": "string",  # Source IPv4 or IPv6 address used to communicate with FortiAn
    "upload-option": "option",  # Enable/disable logging to hard disk and then uploading to Fo
    "upload-interval": "option",  # Frequency to upload log files to FortiAnalyzer.
    "upload-day": "user",  # Day of week (month) to upload logs.
    "upload-time": "user",  # Time to upload logs (hh:mm).
    "reliable": "option",  # Enable/disable reliable logging to FortiAnalyzer.
    "priority": "option",  # Set log transmission priority.
    "max-log-rate": "integer",  # FortiAnalyzer maximum log rate in MBps (0 = unlimited).
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable logging to FortiAnalyzer.",
    "ips-archive": "Enable/disable IPS packet archive logging.",
    "server": "The remote FortiAnalyzer.",
    "alt-server": "Alternate FortiAnalyzer.",
    "fallback-to-primary": "Enable/disable this FortiGate unit to fallback to the primary FortiAnalyzer when it is available.",
    "certificate-verification": "Enable/disable identity verification of FortiAnalyzer by use of certificate.",
    "serial": "Serial numbers of the FortiAnalyzer.",
    "server-cert-ca": "Mandatory CA on FortiGate in certificate chain of server.",
    "preshared-key": "Preshared-key used for auto-authorization on FortiAnalyzer.",
    "access-config": "Enable/disable FortiAnalyzer access to configuration and data.",
    "hmac-algorithm": "OFTP login hash algorithm.",
    "enc-algorithm": "Configure the level of SSL protection for secure communication with FortiAnalyzer.",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default is to follow system global setting).",
    "conn-timeout": "FortiAnalyzer connection time-out in seconds (for status and log buffer).",
    "monitor-keepalive-period": "Time between OFTP keepalives in seconds (for status and log buffer).",
    "monitor-failure-retry-period": "Time between FortiAnalyzer connection retries in seconds (for status and log buffer).",
    "certificate": "Certificate used to communicate with FortiAnalyzer.",
    "source-ip": "Source IPv4 or IPv6 address used to communicate with FortiAnalyzer.",
    "upload-option": "Enable/disable logging to hard disk and then uploading to FortiAnalyzer.",
    "upload-interval": "Frequency to upload log files to FortiAnalyzer.",
    "upload-day": "Day of week (month) to upload logs.",
    "upload-time": "Time to upload logs (hh:mm).",
    "reliable": "Enable/disable reliable logging to FortiAnalyzer.",
    "priority": "Set log transmission priority.",
    "max-log-rate": "FortiAnalyzer maximum log rate in MBps (0 = unlimited).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "server": {"type": "string", "max_length": 127},
    "alt-server": {"type": "string", "max_length": 127},
    "server-cert-ca": {"type": "string", "max_length": 79},
    "preshared-key": {"type": "string", "max_length": 63},
    "conn-timeout": {"type": "integer", "min": 1, "max": 3600},
    "monitor-keepalive-period": {"type": "integer", "min": 1, "max": 120},
    "monitor-failure-retry-period": {"type": "integer", "min": 1, "max": 86400},
    "certificate": {"type": "string", "max_length": 35},
    "source-ip": {"type": "string", "max_length": 63},
    "max-log-rate": {"type": "integer", "min": 0, "max": 100000},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "serial": {
        "name": {
            "type": "string",
            "help": "Serial Number.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IPS_ARCHIVE = [
    "enable",
    "disable",
]
VALID_BODY_FALLBACK_TO_PRIMARY = [
    "enable",
    "disable",
]
VALID_BODY_CERTIFICATE_VERIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_ACCESS_CONFIG = [
    "enable",
    "disable",
]
VALID_BODY_HMAC_ALGORITHM = [
    "sha256",
]
VALID_BODY_ENC_ALGORITHM = [
    "high-medium",
    "high",
    "low",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "default",
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_UPLOAD_OPTION = [
    "store-and-upload",
    "realtime",
    "1-minute",
    "5-minute",
]
VALID_BODY_UPLOAD_INTERVAL = [
    "daily",
    "weekly",
    "monthly",
]
VALID_BODY_RELIABLE = [
    "enable",
    "disable",
]
VALID_BODY_PRIORITY = [
    "default",
    "low",
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


def validate_log_fortianalyzer3_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/fortianalyzer3/setting."""
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


def validate_log_fortianalyzer3_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/fortianalyzer3/setting object."""
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
    if "ips-archive" in payload:
        is_valid, error = _validate_enum_field(
            "ips-archive",
            payload["ips-archive"],
            VALID_BODY_IPS_ARCHIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fallback-to-primary" in payload:
        is_valid, error = _validate_enum_field(
            "fallback-to-primary",
            payload["fallback-to-primary"],
            VALID_BODY_FALLBACK_TO_PRIMARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "certificate-verification" in payload:
        is_valid, error = _validate_enum_field(
            "certificate-verification",
            payload["certificate-verification"],
            VALID_BODY_CERTIFICATE_VERIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-config" in payload:
        is_valid, error = _validate_enum_field(
            "access-config",
            payload["access-config"],
            VALID_BODY_ACCESS_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hmac-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "hmac-algorithm",
            payload["hmac-algorithm"],
            VALID_BODY_HMAC_ALGORITHM,
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
    if "upload-option" in payload:
        is_valid, error = _validate_enum_field(
            "upload-option",
            payload["upload-option"],
            VALID_BODY_UPLOAD_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-interval" in payload:
        is_valid, error = _validate_enum_field(
            "upload-interval",
            payload["upload-interval"],
            VALID_BODY_UPLOAD_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reliable" in payload:
        is_valid, error = _validate_enum_field(
            "reliable",
            payload["reliable"],
            VALID_BODY_RELIABLE,
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


def validate_log_fortianalyzer3_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/fortianalyzer3/setting."""
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
    if "ips-archive" in payload:
        is_valid, error = _validate_enum_field(
            "ips-archive",
            payload["ips-archive"],
            VALID_BODY_IPS_ARCHIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fallback-to-primary" in payload:
        is_valid, error = _validate_enum_field(
            "fallback-to-primary",
            payload["fallback-to-primary"],
            VALID_BODY_FALLBACK_TO_PRIMARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "certificate-verification" in payload:
        is_valid, error = _validate_enum_field(
            "certificate-verification",
            payload["certificate-verification"],
            VALID_BODY_CERTIFICATE_VERIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "access-config" in payload:
        is_valid, error = _validate_enum_field(
            "access-config",
            payload["access-config"],
            VALID_BODY_ACCESS_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hmac-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "hmac-algorithm",
            payload["hmac-algorithm"],
            VALID_BODY_HMAC_ALGORITHM,
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
    if "upload-option" in payload:
        is_valid, error = _validate_enum_field(
            "upload-option",
            payload["upload-option"],
            VALID_BODY_UPLOAD_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-interval" in payload:
        is_valid, error = _validate_enum_field(
            "upload-interval",
            payload["upload-interval"],
            VALID_BODY_UPLOAD_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reliable" in payload:
        is_valid, error = _validate_enum_field(
            "reliable",
            payload["reliable"],
            VALID_BODY_RELIABLE,
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
    "endpoint": "log/fortianalyzer3/setting",
    "category": "cmdb",
    "api_path": "log.fortianalyzer3/setting",
    "help": "Global FortiAnalyzer settings.",
    "total_fields": 28,
    "required_fields_count": 2,
    "fields_with_defaults_count": 27,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
