"""Validation helpers for waf/profile - Auto-generated"""

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
    "name": "",
    "external": "disable",
    "extended-log": "disable",
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
    "name": "string",  # WAF Profile name.
    "external": "option",  # Disable/Enable external HTTP Inspection.
    "extended-log": "option",  # Enable/disable extended logging.
    "signature": "string",  # WAF signatures.
    "constraint": "string",  # WAF HTTP protocol restrictions.
    "method": "string",  # Method restriction.
    "address-list": "string",  # Address block and allow lists.
    "url-access": "string",  # URL access list.
    "comment": "var-string",  # Comment.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WAF Profile name.",
    "external": "Disable/Enable external HTTP Inspection.",
    "extended-log": "Enable/disable extended logging.",
    "signature": "WAF signatures.",
    "constraint": "WAF HTTP protocol restrictions.",
    "method": "Method restriction.",
    "address-list": "Address block and allow lists.",
    "url-access": "URL access list.",
    "comment": "Comment.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "signature": {
        "main-class": {
            "type": "string",
            "help": "Main signature class.",
        },
        "disabled-sub-class": {
            "type": "string",
            "help": "Disabled signature subclasses.",
        },
        "disabled-signature": {
            "type": "string",
            "help": "Disabled signatures.",
        },
        "credit-card-detection-threshold": {
            "type": "integer",
            "help": "The minimum number of Credit cards to detect violation.",
            "default": 3,
            "min_value": 0,
            "max_value": 128,
        },
        "custom-signature": {
            "type": "string",
            "help": "Custom signature.",
        },
    },
    "constraint": {
        "header-length": {
            "type": "string",
            "help": "HTTP header length in request.",
        },
        "content-length": {
            "type": "string",
            "help": "HTTP content length in request.",
        },
        "param-length": {
            "type": "string",
            "help": "Maximum length of parameter in URL, HTTP POST request or HTTP body.",
        },
        "line-length": {
            "type": "string",
            "help": "HTTP line length in request.",
        },
        "url-param-length": {
            "type": "string",
            "help": "Maximum length of parameter in URL.",
        },
        "version": {
            "type": "string",
            "help": "Enable/disable HTTP version check.",
        },
        "method": {
            "type": "string",
            "help": "Enable/disable HTTP method check.",
        },
        "hostname": {
            "type": "string",
            "help": "Enable/disable hostname check.",
        },
        "malformed": {
            "type": "string",
            "help": "Enable/disable malformed HTTP request check.",
        },
        "max-cookie": {
            "type": "string",
            "help": "Maximum number of cookies in HTTP request.",
        },
        "max-header-line": {
            "type": "string",
            "help": "Maximum number of HTTP header line.",
        },
        "max-url-param": {
            "type": "string",
            "help": "Maximum number of parameters in URL.",
        },
        "max-range-segment": {
            "type": "string",
            "help": "Maximum number of range segments in HTTP range line.",
        },
        "exception": {
            "type": "string",
            "help": "HTTP constraint exception.",
        },
    },
    "method": {
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "log": {
            "type": "option",
            "help": "Enable/disable logging.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "severity": {
            "type": "option",
            "help": "Severity.",
            "default": "medium",
            "options": ["high", "medium", "low"],
        },
        "default-allowed-methods": {
            "type": "option",
            "help": "Methods.",
            "default": "",
            "options": ["get", "post", "put", "head", "connect", "trace", "options", "delete", "others"],
        },
        "method-policy": {
            "type": "string",
            "help": "HTTP method policy.",
        },
    },
    "address-list": {
        "status": {
            "type": "option",
            "help": "Status.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "blocked-log": {
            "type": "option",
            "help": "Enable/disable logging on blocked addresses.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "severity": {
            "type": "option",
            "help": "Severity.",
            "default": "medium",
            "options": ["high", "medium", "low"],
        },
        "trusted-address": {
            "type": "string",
            "help": "Trusted address.",
        },
        "blocked-address": {
            "type": "string",
            "help": "Blocked address.",
        },
    },
    "url-access": {
        "id": {
            "type": "integer",
            "help": "URL access ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "address": {
            "type": "string",
            "help": "Host address.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "action": {
            "type": "option",
            "help": "Action.",
            "default": "permit",
            "options": ["bypass", "permit", "block"],
        },
        "log": {
            "type": "option",
            "help": "Enable/disable logging.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "severity": {
            "type": "option",
            "help": "Severity.",
            "default": "medium",
            "options": ["high", "medium", "low"],
        },
        "access-pattern": {
            "type": "string",
            "help": "URL access pattern.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_EXTERNAL = [
    "disable",
    "enable",
]
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_waf_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for waf/profile."""
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


def validate_waf_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new waf/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_waf_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update waf/profile."""
    # Validate enum values using central function
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
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
    "endpoint": "waf/profile",
    "category": "cmdb",
    "api_path": "waf/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Web application firewall configuration.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 3,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
