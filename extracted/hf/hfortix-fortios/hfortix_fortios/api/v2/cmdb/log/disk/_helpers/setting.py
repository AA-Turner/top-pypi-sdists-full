"""Validation helpers for log/disk/setting - Auto-generated"""

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
    "uploaduser",  # Username required to log into the FTP server to upload disk log files.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "enable",
    "ips-archive": "enable",
    "max-log-file-size": 20,
    "max-policy-packet-capture-size": 100,
    "roll-schedule": "daily",
    "roll-day": "sunday",
    "roll-time": "",
    "diskfull": "overwrite",
    "log-quota": 0,
    "dlp-archive-quota": 0,
    "report-quota": 0,
    "maximum-log-age": 7,
    "upload": "disable",
    "upload-destination": "ftp-server",
    "uploadip": "0.0.0.0",
    "uploadport": 21,
    "source-ip": "0.0.0.0",
    "uploaduser": "",
    "uploaddir": "",
    "uploadtype": "traffic event virus webfilter IPS emailfilter dlp-archive anomaly voip dlp app-ctrl waf gtp dns ssh ssl",
    "uploadsched": "disable",
    "uploadtime": "",
    "upload-delete-files": "enable",
    "upload-ssl-conn": "default",
    "full-first-warning-threshold": 75,
    "full-second-warning-threshold": 90,
    "full-final-warning-threshold": 95,
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
    "status": "option",  # Enable/disable local disk logging.
    "ips-archive": "option",  # Enable/disable IPS packet archiving to the local disk.
    "max-log-file-size": "integer",  # Maximum log file size before rolling (1 - 100 Mbytes).
    "max-policy-packet-capture-size": "integer",  # Maximum size of policy sniffer in MB (0 means unlimited).
    "roll-schedule": "option",  # Frequency to check log file for rolling.
    "roll-day": "option",  # Day of week on which to roll log file.
    "roll-time": "user",  # Time of day to roll the log file (hh:mm).
    "diskfull": "option",  # Action to take when disk is full. The system can overwrite t
    "log-quota": "integer",  # Disk log quota (MB).
    "dlp-archive-quota": "integer",  # DLP archive quota (MB).
    "report-quota": "integer",  # Report db quota (MB).
    "maximum-log-age": "integer",  # Delete log files older than (days).
    "upload": "option",  # Enable/disable uploading log files when they are rolled.
    "upload-destination": "option",  # The type of server to upload log files to. Only FTP is curre
    "uploadip": "ipv4-address",  # IP address of the FTP server to upload log files to.
    "uploadport": "integer",  # TCP port to use for communicating with the FTP server (defau
    "source-ip": "ipv4-address",  # Source IP address to use for uploading disk log files.
    "uploaduser": "string",  # Username required to log into the FTP server to upload disk 
    "uploadpass": "password",  # Password required to log into the FTP server to upload disk 
    "uploaddir": "string",  # The remote directory on the FTP server to upload log files t
    "uploadtype": "option",  # Types of log files to upload. Separate multiple entries with
    "uploadsched": "option",  # Set the schedule for uploading log files to the FTP server (
    "uploadtime": "user",  # Time of day at which log files are uploaded if uploadsched i
    "upload-delete-files": "option",  # Delete log files after uploading (default = enable).
    "upload-ssl-conn": "option",  # Enable/disable encrypted FTPS communication to upload log fi
    "full-first-warning-threshold": "integer",  # Log full first warning threshold as a percent (1 - 98, defau
    "full-second-warning-threshold": "integer",  # Log full second warning threshold as a percent (2 - 99, defa
    "full-final-warning-threshold": "integer",  # Log full final warning threshold as a percent (3 - 100, defa
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable local disk logging.",
    "ips-archive": "Enable/disable IPS packet archiving to the local disk.",
    "max-log-file-size": "Maximum log file size before rolling (1 - 100 Mbytes).",
    "max-policy-packet-capture-size": "Maximum size of policy sniffer in MB (0 means unlimited).",
    "roll-schedule": "Frequency to check log file for rolling.",
    "roll-day": "Day of week on which to roll log file.",
    "roll-time": "Time of day to roll the log file (hh:mm).",
    "diskfull": "Action to take when disk is full. The system can overwrite the oldest log messages or stop logging when the disk is full (default = overwrite).",
    "log-quota": "Disk log quota (MB).",
    "dlp-archive-quota": "DLP archive quota (MB).",
    "report-quota": "Report db quota (MB).",
    "maximum-log-age": "Delete log files older than (days).",
    "upload": "Enable/disable uploading log files when they are rolled.",
    "upload-destination": "The type of server to upload log files to. Only FTP is currently supported.",
    "uploadip": "IP address of the FTP server to upload log files to.",
    "uploadport": "TCP port to use for communicating with the FTP server (default = 21).",
    "source-ip": "Source IP address to use for uploading disk log files.",
    "uploaduser": "Username required to log into the FTP server to upload disk log files.",
    "uploadpass": "Password required to log into the FTP server to upload disk log files.",
    "uploaddir": "The remote directory on the FTP server to upload log files to.",
    "uploadtype": "Types of log files to upload. Separate multiple entries with a space.",
    "uploadsched": "Set the schedule for uploading log files to the FTP server (default = disable = upload when rolling).",
    "uploadtime": "Time of day at which log files are uploaded if uploadsched is enabled (hh:mm or hh).",
    "upload-delete-files": "Delete log files after uploading (default = enable).",
    "upload-ssl-conn": "Enable/disable encrypted FTPS communication to upload log files.",
    "full-first-warning-threshold": "Log full first warning threshold as a percent (1 - 98, default = 75).",
    "full-second-warning-threshold": "Log full second warning threshold as a percent (2 - 99, default = 90).",
    "full-final-warning-threshold": "Log full final warning threshold as a percent (3 - 100, default = 95).",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "max-log-file-size": {"type": "integer", "min": 1, "max": 100},
    "max-policy-packet-capture-size": {"type": "integer", "min": 0, "max": 4294967295},
    "log-quota": {"type": "integer", "min": 0, "max": 4294967295},
    "dlp-archive-quota": {"type": "integer", "min": 0, "max": 4294967295},
    "report-quota": {"type": "integer", "min": 0, "max": 4294967295},
    "maximum-log-age": {"type": "integer", "min": 0, "max": 3650},
    "uploadport": {"type": "integer", "min": 0, "max": 65535},
    "uploaduser": {"type": "string", "max_length": 35},
    "uploaddir": {"type": "string", "max_length": 63},
    "full-first-warning-threshold": {"type": "integer", "min": 1, "max": 98},
    "full-second-warning-threshold": {"type": "integer", "min": 2, "max": 99},
    "full-final-warning-threshold": {"type": "integer", "min": 3, "max": 100},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
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
VALID_BODY_ROLL_SCHEDULE = [
    "daily",
    "weekly",
]
VALID_BODY_ROLL_DAY = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
VALID_BODY_DISKFULL = [
    "overwrite",
    "nolog",
]
VALID_BODY_UPLOAD = [
    "enable",
    "disable",
]
VALID_BODY_UPLOAD_DESTINATION = [
    "ftp-server",
]
VALID_BODY_UPLOADTYPE = [
    "traffic",
    "event",
    "virus",
    "webfilter",
    "IPS",
    "emailfilter",
    "dlp-archive",
    "anomaly",
    "voip",
    "dlp",
    "app-ctrl",
    "waf",
    "gtp",
    "dns",
    "ssh",
    "ssl",
    "file-filter",
    "icap",
    "virtual-patch",
    "debug",
]
VALID_BODY_UPLOADSCHED = [
    "disable",
    "enable",
]
VALID_BODY_UPLOAD_DELETE_FILES = [
    "enable",
    "disable",
]
VALID_BODY_UPLOAD_SSL_CONN = [
    "default",
    "high",
    "low",
    "disable",
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


def validate_log_disk_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/disk/setting."""
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


def validate_log_disk_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/disk/setting object."""
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
    if "roll-schedule" in payload:
        is_valid, error = _validate_enum_field(
            "roll-schedule",
            payload["roll-schedule"],
            VALID_BODY_ROLL_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "roll-day" in payload:
        is_valid, error = _validate_enum_field(
            "roll-day",
            payload["roll-day"],
            VALID_BODY_ROLL_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diskfull" in payload:
        is_valid, error = _validate_enum_field(
            "diskfull",
            payload["diskfull"],
            VALID_BODY_DISKFULL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload" in payload:
        is_valid, error = _validate_enum_field(
            "upload",
            payload["upload"],
            VALID_BODY_UPLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-destination" in payload:
        is_valid, error = _validate_enum_field(
            "upload-destination",
            payload["upload-destination"],
            VALID_BODY_UPLOAD_DESTINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "uploadtype" in payload:
        is_valid, error = _validate_enum_field(
            "uploadtype",
            payload["uploadtype"],
            VALID_BODY_UPLOADTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "uploadsched" in payload:
        is_valid, error = _validate_enum_field(
            "uploadsched",
            payload["uploadsched"],
            VALID_BODY_UPLOADSCHED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-delete-files" in payload:
        is_valid, error = _validate_enum_field(
            "upload-delete-files",
            payload["upload-delete-files"],
            VALID_BODY_UPLOAD_DELETE_FILES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-ssl-conn" in payload:
        is_valid, error = _validate_enum_field(
            "upload-ssl-conn",
            payload["upload-ssl-conn"],
            VALID_BODY_UPLOAD_SSL_CONN,
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


def validate_log_disk_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/disk/setting."""
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
    if "roll-schedule" in payload:
        is_valid, error = _validate_enum_field(
            "roll-schedule",
            payload["roll-schedule"],
            VALID_BODY_ROLL_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "roll-day" in payload:
        is_valid, error = _validate_enum_field(
            "roll-day",
            payload["roll-day"],
            VALID_BODY_ROLL_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diskfull" in payload:
        is_valid, error = _validate_enum_field(
            "diskfull",
            payload["diskfull"],
            VALID_BODY_DISKFULL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload" in payload:
        is_valid, error = _validate_enum_field(
            "upload",
            payload["upload"],
            VALID_BODY_UPLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-destination" in payload:
        is_valid, error = _validate_enum_field(
            "upload-destination",
            payload["upload-destination"],
            VALID_BODY_UPLOAD_DESTINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "uploadtype" in payload:
        is_valid, error = _validate_enum_field(
            "uploadtype",
            payload["uploadtype"],
            VALID_BODY_UPLOADTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "uploadsched" in payload:
        is_valid, error = _validate_enum_field(
            "uploadsched",
            payload["uploadsched"],
            VALID_BODY_UPLOADSCHED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-delete-files" in payload:
        is_valid, error = _validate_enum_field(
            "upload-delete-files",
            payload["upload-delete-files"],
            VALID_BODY_UPLOAD_DELETE_FILES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upload-ssl-conn" in payload:
        is_valid, error = _validate_enum_field(
            "upload-ssl-conn",
            payload["upload-ssl-conn"],
            VALID_BODY_UPLOAD_SSL_CONN,
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
    "endpoint": "log/disk/setting",
    "category": "cmdb",
    "api_path": "log.disk/setting",
    "help": "Settings for local disk logging.",
    "total_fields": 31,
    "required_fields_count": 2,
    "fields_with_defaults_count": 30,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
