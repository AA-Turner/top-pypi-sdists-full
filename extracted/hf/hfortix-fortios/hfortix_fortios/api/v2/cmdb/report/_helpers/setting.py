"""Validation helpers for report/setting - Auto-generated"""

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
    "pdf-report": "enable",
    "fortiview": "enable",
    "report-source": "forward-traffic",
    "web-browsing-threshold": 3,
    "top-n": 1000,
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
    "pdf-report": "option",  # Enable/disable PDF report.
    "fortiview": "option",  # Enable/disable historical FortiView.
    "report-source": "option",  # Report log source.
    "web-browsing-threshold": "integer",  # Web browsing time calculation threshold (3 - 15 min).
    "top-n": "integer",  # Number of items to populate (1000 - 20000).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "pdf-report": "Enable/disable PDF report.",
    "fortiview": "Enable/disable historical FortiView.",
    "report-source": "Report log source.",
    "web-browsing-threshold": "Web browsing time calculation threshold (3 - 15 min).",
    "top-n": "Number of items to populate (1000 - 20000).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "web-browsing-threshold": {"type": "integer", "min": 3, "max": 15},
    "top-n": {"type": "integer", "min": 1000, "max": 20000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_PDF_REPORT = [
    "enable",
    "disable",
]
VALID_BODY_FORTIVIEW = [
    "enable",
    "disable",
]
VALID_BODY_REPORT_SOURCE = [
    "forward-traffic",
    "sniffer-traffic",
    "local-deny-traffic",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_report_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for report/setting."""
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


def validate_report_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new report/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "pdf-report" in payload:
        is_valid, error = _validate_enum_field(
            "pdf-report",
            payload["pdf-report"],
            VALID_BODY_PDF_REPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiview" in payload:
        is_valid, error = _validate_enum_field(
            "fortiview",
            payload["fortiview"],
            VALID_BODY_FORTIVIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "report-source" in payload:
        is_valid, error = _validate_enum_field(
            "report-source",
            payload["report-source"],
            VALID_BODY_REPORT_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_report_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update report/setting."""
    # Validate enum values using central function
    if "pdf-report" in payload:
        is_valid, error = _validate_enum_field(
            "pdf-report",
            payload["pdf-report"],
            VALID_BODY_PDF_REPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiview" in payload:
        is_valid, error = _validate_enum_field(
            "fortiview",
            payload["fortiview"],
            VALID_BODY_FORTIVIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "report-source" in payload:
        is_valid, error = _validate_enum_field(
            "report-source",
            payload["report-source"],
            VALID_BODY_REPORT_SOURCE,
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
    "endpoint": "report/setting",
    "category": "cmdb",
    "api_path": "report/setting",
    "help": "Report setting configuration.",
    "total_fields": 5,
    "required_fields_count": 0,
    "fields_with_defaults_count": 5,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
