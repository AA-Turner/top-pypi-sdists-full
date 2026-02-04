"""Validation helpers for firewall/proxy_address - Auto-generated"""

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
    "host",  # Address object for the host.
    "application",  # SaaS application.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "type": "url",
    "host": "",
    "host-regex": "",
    "path": "",
    "query": "",
    "referrer": "disable",
    "method": "",
    "ua": "",
    "ua-min-ver": "",
    "ua-max-ver": "",
    "header-name": "",
    "header": "",
    "case-sensitivity": "disable",
    "color": 0,
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
    "name": "string",  # Address name.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "type": "option",  # Proxy address type.
    "host": "string",  # Address object for the host.
    "host-regex": "string",  # Host name as a regular expression.
    "path": "string",  # URL path as a regular expression.
    "query": "string",  # Match the query part of the URL as a regular expression.
    "referrer": "option",  # Enable/disable use of referrer field in the HTTP header to match the address.
    "category": "string",  # FortiGuard category ID.
    "method": "option",  # HTTP request methods to be used.
    "ua": "option",  # Names of browsers to be used as user agent.
    "ua-min-ver": "string",  # Minimum version of the user agent specified in dotted notation. For example, use
    "ua-max-ver": "string",  # Maximum version of the user agent specified in dotted notation. For example, use
    "header-name": "string",  # Name of HTTP header.
    "header": "string",  # HTTP header name as a regular expression.
    "case-sensitivity": "option",  # Enable to make the pattern case sensitive.
    "header-group": "string",  # HTTP header group.
    "color": "integer",  # Integer value to determine the color of the icon in the GUI (1 - 32, default = 0
    "tagging": "string",  # Config object tagging.
    "comment": "var-string",  # Optional comments.
    "application": "string",  # SaaS application.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Address name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "type": "Proxy address type.",
    "host": "Address object for the host.",
    "host-regex": "Host name as a regular expression.",
    "path": "URL path as a regular expression.",
    "query": "Match the query part of the URL as a regular expression.",
    "referrer": "Enable/disable use of referrer field in the HTTP header to match the address.",
    "category": "FortiGuard category ID.",
    "method": "HTTP request methods to be used.",
    "ua": "Names of browsers to be used as user agent.",
    "ua-min-ver": "Minimum version of the user agent specified in dotted notation. For example, use 90.0.1 with the ua field set to \"chrome\" to require Google Chrome's minimum version must be 90.0.1.",
    "ua-max-ver": "Maximum version of the user agent specified in dotted notation. For example, use 120 with the ua field set to \"chrome\" to require Google Chrome's maximum version must be 120.",
    "header-name": "Name of HTTP header.",
    "header": "HTTP header name as a regular expression.",
    "case-sensitivity": "Enable to make the pattern case sensitive.",
    "header-group": "HTTP header group.",
    "color": "Integer value to determine the color of the icon in the GUI (1 - 32, default = 0, which sets value to 1).",
    "tagging": "Config object tagging.",
    "comment": "Optional comments.",
    "application": "SaaS application.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "host": {"type": "string", "max_length": 79},
    "host-regex": {"type": "string", "max_length": 255},
    "path": {"type": "string", "max_length": 255},
    "query": {"type": "string", "max_length": 255},
    "ua-min-ver": {"type": "string", "max_length": 63},
    "ua-max-ver": {"type": "string", "max_length": 63},
    "header-name": {"type": "string", "max_length": 79},
    "header": {"type": "string", "max_length": 255},
    "color": {"type": "integer", "min": 0, "max": 32},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "category": {
        "id": {
            "type": "integer",
            "help": "FortiGuard category ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "header-group": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "header-name": {
            "type": "string",
            "help": "HTTP header.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "header": {
            "type": "string",
            "help": "HTTP header regular expression.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
        "case-sensitivity": {
            "type": "option",
            "help": "Case sensitivity in pattern.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "tagging": {
        "name": {
            "type": "string",
            "help": "Tagging entry name.",
            "default": "",
            "max_length": 63,
        },
        "category": {
            "type": "string",
            "help": "Tag category.",
            "default": "",
            "max_length": 63,
        },
        "tags": {
            "type": "string",
            "help": "Tags.",
        },
    },
    "application": {
        "name": {
            "type": "string",
            "help": "SaaS application name.",
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "host-regex",
    "url",
    "category",
    "method",
    "ua",
    "header",
    "src-advanced",
    "dst-advanced",
    "saas",
]
VALID_BODY_REFERRER = [
    "enable",
    "disable",
]
VALID_BODY_METHOD = [
    "get",
    "post",
    "put",
    "head",
    "connect",
    "trace",
    "options",
    "delete",
    "update",
    "patch",
    "other",
]
VALID_BODY_UA = [
    "chrome",
    "ms",
    "firefox",
    "safari",
    "ie",
    "edge",
    "other",
]
VALID_BODY_CASE_SENSITIVITY = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_proxy_address_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/proxy_address."""
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


def validate_firewall_proxy_address_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/proxy_address object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "referrer" in payload:
        is_valid, error = _validate_enum_field(
            "referrer",
            payload["referrer"],
            VALID_BODY_REFERRER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ua" in payload:
        is_valid, error = _validate_enum_field(
            "ua",
            payload["ua"],
            VALID_BODY_UA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "case-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "case-sensitivity",
            payload["case-sensitivity"],
            VALID_BODY_CASE_SENSITIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_proxy_address_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/proxy_address."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "referrer" in payload:
        is_valid, error = _validate_enum_field(
            "referrer",
            payload["referrer"],
            VALID_BODY_REFERRER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ua" in payload:
        is_valid, error = _validate_enum_field(
            "ua",
            payload["ua"],
            VALID_BODY_UA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "case-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "case-sensitivity",
            payload["case-sensitivity"],
            VALID_BODY_CASE_SENSITIVITY,
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
    "endpoint": "firewall/proxy_address",
    "category": "cmdb",
    "api_path": "firewall/proxy-address",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure web proxy address.",
    "total_fields": 21,
    "required_fields_count": 2,
    "fields_with_defaults_count": 16,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
