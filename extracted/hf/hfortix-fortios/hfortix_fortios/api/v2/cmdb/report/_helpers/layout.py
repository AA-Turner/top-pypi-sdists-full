"""Validation helpers for report/layout - Auto-generated"""

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
    "style-theme",  # Report style theme.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "title": "",
    "subtitle": "",
    "description": "",
    "style-theme": "",
    "options": "include-table-of-content auto-numbering-heading view-chart-as-heading",
    "format": "pdf",
    "schedule-type": "daily",
    "day": "sunday",
    "time": "",
    "cutoff-option": "run-time",
    "cutoff-time": "",
    "email-send": "disable",
    "email-recipients": "",
    "max-pdf-report": 31,
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
    "name": "string",  # Report layout name.
    "title": "string",  # Report title.
    "subtitle": "string",  # Report subtitle.
    "description": "string",  # Description.
    "style-theme": "string",  # Report style theme.
    "options": "option",  # Report layout options.
    "format": "option",  # Report format.
    "schedule-type": "option",  # Report schedule type.
    "day": "option",  # Schedule days of week to generate report.
    "time": "user",  # Schedule time to generate report (format = hh:mm).
    "cutoff-option": "option",  # Cutoff-option is either run-time or custom.
    "cutoff-time": "user",  # Custom cutoff time to generate report (format = hh:mm).
    "email-send": "option",  # Enable/disable sending emails after reports are generated.
    "email-recipients": "string",  # Email recipients for generated reports.
    "max-pdf-report": "integer",  # Maximum number of PDF reports to keep at one time (oldest re
    "page": "string",  # Configure report page.
    "body-item": "string",  # Configure report body item.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Report layout name.",
    "title": "Report title.",
    "subtitle": "Report subtitle.",
    "description": "Description.",
    "style-theme": "Report style theme.",
    "options": "Report layout options.",
    "format": "Report format.",
    "schedule-type": "Report schedule type.",
    "day": "Schedule days of week to generate report.",
    "time": "Schedule time to generate report (format = hh:mm).",
    "cutoff-option": "Cutoff-option is either run-time or custom.",
    "cutoff-time": "Custom cutoff time to generate report (format = hh:mm).",
    "email-send": "Enable/disable sending emails after reports are generated.",
    "email-recipients": "Email recipients for generated reports.",
    "max-pdf-report": "Maximum number of PDF reports to keep at one time (oldest report is overwritten).",
    "page": "Configure report page.",
    "body-item": "Configure report body item.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "title": {"type": "string", "max_length": 127},
    "subtitle": {"type": "string", "max_length": 127},
    "description": {"type": "string", "max_length": 127},
    "style-theme": {"type": "string", "max_length": 35},
    "email-recipients": {"type": "string", "max_length": 511},
    "max-pdf-report": {"type": "integer", "min": 1, "max": 365},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "page": {
        "paper": {
            "type": "option",
            "help": "Report page paper.",
            "default": "a4",
            "options": ["a4", "letter"],
        },
        "column-break-before": {
            "type": "option",
            "help": "Report page auto column break before heading.",
            "default": "",
            "options": ["heading1", "heading2", "heading3"],
        },
        "page-break-before": {
            "type": "option",
            "help": "Report page auto page break before heading.",
            "default": "",
            "options": ["heading1", "heading2", "heading3"],
        },
        "options": {
            "type": "option",
            "help": "Report page options.",
            "default": "",
            "options": ["header-on-first-page", "footer-on-first-page"],
        },
        "header": {
            "type": "string",
            "help": "Configure report page header.",
        },
        "footer": {
            "type": "string",
            "help": "Configure report page footer.",
        },
    },
    "body-item": {
        "id": {
            "type": "integer",
            "help": "Report item ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "description": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 63,
        },
        "type": {
            "type": "option",
            "help": "Report item type.",
            "default": "text",
            "options": ["text", "image", "chart", "misc"],
        },
        "style": {
            "type": "string",
            "help": "Report item style.",
            "default": "",
            "max_length": 71,
        },
        "top-n": {
            "type": "integer",
            "help": "Value of top.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "parameters": {
            "type": "string",
            "help": "Parameters.",
        },
        "text-component": {
            "type": "option",
            "help": "Report item text component.",
            "default": "text",
            "options": ["text", "heading1", "heading2", "heading3"],
        },
        "content": {
            "type": "string",
            "help": "Report item text content.",
            "default": "",
            "max_length": 511,
        },
        "img-src": {
            "type": "string",
            "help": "Report item image file name.",
            "default": "",
            "max_length": 127,
        },
        "chart": {
            "type": "string",
            "help": "Report item chart name.",
            "default": "",
            "max_length": 71,
        },
        "chart-options": {
            "type": "option",
            "help": "Report chart options.",
            "default": "include-no-data hide-title show-caption",
            "options": ["include-no-data", "hide-title", "show-caption"],
        },
        "misc-component": {
            "type": "option",
            "help": "Report item miscellaneous component.",
            "default": "hline",
            "options": ["hline", "page-break", "column-break", "section-start"],
        },
        "title": {
            "type": "string",
            "help": "Report section title.",
            "default": "",
            "max_length": 511,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_OPTIONS = [
    "include-table-of-content",
    "auto-numbering-heading",
    "view-chart-as-heading",
    "show-html-navbar-before-heading",
    "dummy-option",
]
VALID_BODY_FORMAT = [
    "pdf",
]
VALID_BODY_SCHEDULE_TYPE = [
    "demand",
    "daily",
    "weekly",
]
VALID_BODY_DAY = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
VALID_BODY_CUTOFF_OPTION = [
    "run-time",
    "custom",
]
VALID_BODY_EMAIL_SEND = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_report_layout_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for report/layout."""
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


def validate_report_layout_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new report/layout object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
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
    if "schedule-type" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-type",
            payload["schedule-type"],
            VALID_BODY_SCHEDULE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "day" in payload:
        is_valid, error = _validate_enum_field(
            "day",
            payload["day"],
            VALID_BODY_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cutoff-option" in payload:
        is_valid, error = _validate_enum_field(
            "cutoff-option",
            payload["cutoff-option"],
            VALID_BODY_CUTOFF_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-send" in payload:
        is_valid, error = _validate_enum_field(
            "email-send",
            payload["email-send"],
            VALID_BODY_EMAIL_SEND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_report_layout_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update report/layout."""
    # Validate enum values using central function
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
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
    if "schedule-type" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-type",
            payload["schedule-type"],
            VALID_BODY_SCHEDULE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "day" in payload:
        is_valid, error = _validate_enum_field(
            "day",
            payload["day"],
            VALID_BODY_DAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cutoff-option" in payload:
        is_valid, error = _validate_enum_field(
            "cutoff-option",
            payload["cutoff-option"],
            VALID_BODY_CUTOFF_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-send" in payload:
        is_valid, error = _validate_enum_field(
            "email-send",
            payload["email-send"],
            VALID_BODY_EMAIL_SEND,
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
    "endpoint": "report/layout",
    "category": "cmdb",
    "api_path": "report/layout",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Report layout configuration.",
    "total_fields": 17,
    "required_fields_count": 1,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
