"""Validation helpers for file_filter/profile - Auto-generated"""

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
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "feature-set": "flow",
    "replacemsg-group": "",
    "log": "enable",
    "extended-log": "disable",
    "scan-archive-contents": "enable",
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
    "name": "string",  # Profile name.
    "comment": "var-string",  # Comment.
    "feature-set": "option",  # Flow/proxy feature set.
    "replacemsg-group": "string",  # Replacement message group.
    "log": "option",  # Enable/disable file-filter logging.
    "extended-log": "option",  # Enable/disable file-filter extended logging.
    "scan-archive-contents": "option",  # Enable/disable archive contents scan.
    "rules": "string",  # File filter rules.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Comment.",
    "feature-set": "Flow/proxy feature set.",
    "replacemsg-group": "Replacement message group.",
    "log": "Enable/disable file-filter logging.",
    "extended-log": "Enable/disable file-filter extended logging.",
    "scan-archive-contents": "Enable/disable archive contents scan.",
    "rules": "File filter rules.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "rules": {
        "name": {
            "type": "string",
            "help": "File-filter rule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "comment": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
        "protocol": {
            "type": "option",
            "help": "Protocols to apply rule to.",
            "default": "http ftp smtp imap pop3 mapi cifs ssh",
            "options": ["http", "ftp", "smtp", "imap", "pop3", "mapi", "cifs", "ssh"],
        },
        "action": {
            "type": "option",
            "help": "Action taken for matched file.",
            "default": "log-only",
            "options": ["log-only", "block"],
        },
        "direction": {
            "type": "option",
            "help": "Traffic direction (HTTP, FTP, SSH, CIFS, and MAPI only).",
            "default": "any",
            "options": ["incoming", "outgoing", "any"],
        },
        "password-protected": {
            "type": "option",
            "help": "Match password-protected files.",
            "default": "any",
            "options": ["yes", "any"],
        },
        "file-type": {
            "type": "string",
            "help": "Select file type.",
            "required": True,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FEATURE_SET = [
    "flow",
    "proxy",
]
VALID_BODY_LOG = [
    "disable",
    "enable",
]
VALID_BODY_EXTENDED_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SCAN_ARCHIVE_CONTENTS = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_file_filter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for file_filter/profile."""
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


def validate_file_filter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new file_filter/profile object."""
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
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
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
    if "scan-archive-contents" in payload:
        is_valid, error = _validate_enum_field(
            "scan-archive-contents",
            payload["scan-archive-contents"],
            VALID_BODY_SCAN_ARCHIVE_CONTENTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_file_filter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update file_filter/profile."""
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
    if "log" in payload:
        is_valid, error = _validate_enum_field(
            "log",
            payload["log"],
            VALID_BODY_LOG,
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
    if "scan-archive-contents" in payload:
        is_valid, error = _validate_enum_field(
            "scan-archive-contents",
            payload["scan-archive-contents"],
            VALID_BODY_SCAN_ARCHIVE_CONTENTS,
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
    "endpoint": "file_filter/profile",
    "category": "cmdb",
    "api_path": "file-filter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure file-filter profiles.",
    "total_fields": 8,
    "required_fields_count": 1,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
