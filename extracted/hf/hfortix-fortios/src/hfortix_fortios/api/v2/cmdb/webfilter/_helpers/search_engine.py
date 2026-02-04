"""Validation helpers for webfilter/search_engine - Auto-generated"""

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
    "name",  # Search engine name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "hostname": "",
    "url": "",
    "query": "",
    "safesearch": "disable",
    "charset": "utf-8",
    "safesearch-str": "",
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
    "name": "string",  # Search engine name.
    "hostname": "string",  # Hostname (regular expression).
    "url": "string",  # URL (regular expression).
    "query": "string",  # Code used to prefix a query (must end with an equals character).
    "safesearch": "option",  # Safe search method. You can disable safe search, add the safe search string to U
    "charset": "option",  # Search engine charset.
    "safesearch-str": "string",  # Safe search parameter used in the URL in URL mode. In translate mode, it provide
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Search engine name.",
    "hostname": "Hostname (regular expression).",
    "url": "URL (regular expression).",
    "query": "Code used to prefix a query (must end with an equals character).",
    "safesearch": "Safe search method. You can disable safe search, add the safe search string to URLs, or insert a safe search header.",
    "charset": "Search engine charset.",
    "safesearch-str": "Safe search parameter used in the URL in URL mode. In translate mode, it provides either the regex to translate the URL or the special case to translate the URL.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "hostname": {"type": "string", "max_length": 127},
    "url": {"type": "string", "max_length": 127},
    "query": {"type": "string", "max_length": 15},
    "safesearch-str": {"type": "string", "max_length": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_SAFESEARCH = [
    "disable",
    "url",
    "header",
    "translate",
    "yt-pattern",
    "yt-scan",
    "yt-video",
    "yt-channel",
]
VALID_BODY_CHARSET = [
    "utf-8",
    "gb2312",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_webfilter_search_engine_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for webfilter/search_engine."""
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


def validate_webfilter_search_engine_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new webfilter/search_engine object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "safesearch" in payload:
        is_valid, error = _validate_enum_field(
            "safesearch",
            payload["safesearch"],
            VALID_BODY_SAFESEARCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "charset" in payload:
        is_valid, error = _validate_enum_field(
            "charset",
            payload["charset"],
            VALID_BODY_CHARSET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_webfilter_search_engine_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update webfilter/search_engine."""
    # Validate enum values using central function
    if "safesearch" in payload:
        is_valid, error = _validate_enum_field(
            "safesearch",
            payload["safesearch"],
            VALID_BODY_SAFESEARCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "charset" in payload:
        is_valid, error = _validate_enum_field(
            "charset",
            payload["charset"],
            VALID_BODY_CHARSET,
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
    "endpoint": "webfilter/search_engine",
    "category": "cmdb",
    "api_path": "webfilter/search-engine",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure web filter search engines.",
    "total_fields": 7,
    "required_fields_count": 1,
    "fields_with_defaults_count": 7,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
