"""Validation helpers for dlp/profile - Auto-generated"""

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
    "name",  # Name of the DLP profile.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "feature-set": "flow",
    "replacemsg-group": "",
    "dlp-log": "enable",
    "extended-log": "disable",
    "nac-quar-log": "disable",
    "full-archive-proto": "",
    "summary-proto": "",
    "fortidata-error-action": "block",
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
    "name": "string",  # Name of the DLP profile.
    "comment": "var-string",  # Comment.
    "feature-set": "option",  # Flow/proxy feature set.
    "replacemsg-group": "string",  # Replacement message group used by this DLP profile.
    "rule": "string",  # Set up DLP rules for this profile.
    "dlp-log": "option",  # Enable/disable DLP logging.
    "extended-log": "option",  # Enable/disable extended logging for data loss prevention.
    "nac-quar-log": "option",  # Enable/disable NAC quarantine logging.
    "full-archive-proto": "option",  # Protocols to always content archive.
    "summary-proto": "option",  # Protocols to always log summary.
    "fortidata-error-action": "option",  # Action to take if FortiData query fails.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name of the DLP profile.",
    "comment": "Comment.",
    "feature-set": "Flow/proxy feature set.",
    "replacemsg-group": "Replacement message group used by this DLP profile.",
    "rule": "Set up DLP rules for this profile.",
    "dlp-log": "Enable/disable DLP logging.",
    "extended-log": "Enable/disable extended logging for data loss prevention.",
    "nac-quar-log": "Enable/disable NAC quarantine logging.",
    "full-archive-proto": "Protocols to always content archive.",
    "summary-proto": "Protocols to always log summary.",
    "fortidata-error-action": "Action to take if FortiData query fails.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "rule": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "Filter name.",
            "default": "",
            "max_length": 35,
        },
        "severity": {
            "type": "option",
            "help": "Select the severity or threat level that matches this filter.",
            "default": "medium",
            "options": ["info", "low", "medium", "high", "critical"],
        },
        "type": {
            "type": "option",
            "help": "Select whether to check the content of messages (an email message) or files (downloaded files or email attachments).",
            "default": "file",
            "options": ["file", "message"],
        },
        "proto": {
            "type": "option",
            "help": "Check messages or files over one or more of these protocols.",
            "default": "",
            "options": ["smtp", "pop3", "imap", "http-get", "http-post", "ftp", "nntp", "mapi", "ssh", "cifs"],
        },
        "filter-by": {
            "type": "option",
            "help": "Select the type of content to match.",
            "default": "none",
            "options": ["sensor", "label", "fingerprint", "encrypted", "none"],
        },
        "file-size": {
            "type": "integer",
            "help": "Match files greater than or equal to this size (KB).",
            "default": 0,
            "min_value": 0,
            "max_value": 4193280,
        },
        "sensitivity": {
            "type": "string",
            "help": "Select a DLP file pattern sensitivity to match.",
            "required": True,
        },
        "match-percentage": {
            "type": "integer",
            "help": "Percentage of fingerprints in the fingerprint databases designated with the selected sensitivity to match.",
            "default": 10,
            "min_value": 1,
            "max_value": 100,
        },
        "file-type": {
            "type": "integer",
            "help": "Select the number of a DLP file pattern table to match.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "sensor": {
            "type": "string",
            "help": "Select DLP sensors.",
            "required": True,
        },
        "label": {
            "type": "string",
            "help": "Select DLP label.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "archive": {
            "type": "option",
            "help": "Enable/disable DLP archiving.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "action": {
            "type": "option",
            "help": "Action to take with content that this DLP profile matches.",
            "default": "allow",
            "options": ["allow", "log-only", "block", "quarantine-ip"],
        },
        "expiry": {
            "type": "user",
            "help": "Quarantine duration in days, hours, minutes (format = dddhhmm).",
            "default": "5m",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FEATURE_SET = [
    "flow",
    "proxy",
]
VALID_BODY_DLP_LOG = [
    "enable",
    "disable",
]
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_BODY_NAC_QUAR_LOG = [
    "enable",
    "disable",
]
VALID_BODY_FULL_ARCHIVE_PROTO = [
    "smtp",
    "pop3",
    "imap",
    "http-get",
    "http-post",
    "ftp",
    "nntp",
    "mapi",
    "ssh",
    "cifs",
]
VALID_BODY_SUMMARY_PROTO = [
    "smtp",
    "pop3",
    "imap",
    "http-get",
    "http-post",
    "ftp",
    "nntp",
    "mapi",
    "ssh",
    "cifs",
]
VALID_BODY_FORTIDATA_ERROR_ACTION = [
    "log-only",
    "block",
    "ignore",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_dlp_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for dlp/profile."""
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


def validate_dlp_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new dlp/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-log" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-log",
            payload["dlp-log"],
            VALID_BODY_DLP_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nac-quar-log" in payload:
        is_valid, error = _validate_enum_field(
            "nac-quar-log",
            payload["nac-quar-log"],
            VALID_BODY_NAC_QUAR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "full-archive-proto" in payload:
        is_valid, error = _validate_enum_field(
            "full-archive-proto",
            payload["full-archive-proto"],
            VALID_BODY_FULL_ARCHIVE_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "summary-proto" in payload:
        is_valid, error = _validate_enum_field(
            "summary-proto",
            payload["summary-proto"],
            VALID_BODY_SUMMARY_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortidata-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortidata-error-action",
            payload["fortidata-error-action"],
            VALID_BODY_FORTIDATA_ERROR_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_dlp_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update dlp/profile."""
    # Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-log" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-log",
            payload["dlp-log"],
            VALID_BODY_DLP_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nac-quar-log" in payload:
        is_valid, error = _validate_enum_field(
            "nac-quar-log",
            payload["nac-quar-log"],
            VALID_BODY_NAC_QUAR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "full-archive-proto" in payload:
        is_valid, error = _validate_enum_field(
            "full-archive-proto",
            payload["full-archive-proto"],
            VALID_BODY_FULL_ARCHIVE_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "summary-proto" in payload:
        is_valid, error = _validate_enum_field(
            "summary-proto",
            payload["summary-proto"],
            VALID_BODY_SUMMARY_PROTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortidata-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortidata-error-action",
            payload["fortidata-error-action"],
            VALID_BODY_FORTIDATA_ERROR_ACTION,
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
    "endpoint": "dlp/profile",
    "category": "cmdb",
    "api_path": "dlp/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure DLP profiles.",
    "total_fields": 11,
    "required_fields_count": 1,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
