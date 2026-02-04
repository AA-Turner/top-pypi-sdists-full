"""Validation helpers for webfilter/fortiguard - Auto-generated"""

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
    "cache-mode": "ttl",
    "cache-prefix-match": "enable",
    "cache-mem-permille": 1,
    "ovrd-auth-port-http": 8008,
    "ovrd-auth-port-https": 8010,
    "ovrd-auth-port-https-flow": 8015,
    "ovrd-auth-port-warning": 8020,
    "ovrd-auth-https": "enable",
    "warn-auth-https": "enable",
    "close-ports": "disable",
    "request-packet-size-limit": 0,
    "embed-image": "enable",
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
    "cache-mode": "option",  # Cache entry expiration mode.
    "cache-prefix-match": "option",  # Enable/disable prefix matching in the cache.
    "cache-mem-permille": "integer",  # Maximum permille of available memory allocated to caching (1 - 150).
    "ovrd-auth-port-http": "integer",  # Port to use for FortiGuard Web Filter HTTP override authentication.
    "ovrd-auth-port-https": "integer",  # Port to use for FortiGuard Web Filter HTTPS override authentication in proxy mod
    "ovrd-auth-port-https-flow": "integer",  # Port to use for FortiGuard Web Filter HTTPS override authentication in flow mode
    "ovrd-auth-port-warning": "integer",  # Port to use for FortiGuard Web Filter Warning override authentication.
    "ovrd-auth-https": "option",  # Enable/disable use of HTTPS for override authentication.
    "warn-auth-https": "option",  # Enable/disable use of HTTPS for warning and authentication.
    "close-ports": "option",  # Close ports used for HTTP/HTTPS override authentication and disable user overrid
    "request-packet-size-limit": "integer",  # Limit size of URL request packets sent to FortiGuard server (0 for default).
    "embed-image": "option",  # Enable/disable embedding images into replacement messages (default = enable).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "cache-mode": "Cache entry expiration mode.",
    "cache-prefix-match": "Enable/disable prefix matching in the cache.",
    "cache-mem-permille": "Maximum permille of available memory allocated to caching (1 - 150).",
    "ovrd-auth-port-http": "Port to use for FortiGuard Web Filter HTTP override authentication.",
    "ovrd-auth-port-https": "Port to use for FortiGuard Web Filter HTTPS override authentication in proxy mode.",
    "ovrd-auth-port-https-flow": "Port to use for FortiGuard Web Filter HTTPS override authentication in flow mode.",
    "ovrd-auth-port-warning": "Port to use for FortiGuard Web Filter Warning override authentication.",
    "ovrd-auth-https": "Enable/disable use of HTTPS for override authentication.",
    "warn-auth-https": "Enable/disable use of HTTPS for warning and authentication.",
    "close-ports": "Close ports used for HTTP/HTTPS override authentication and disable user overrides.",
    "request-packet-size-limit": "Limit size of URL request packets sent to FortiGuard server (0 for default).",
    "embed-image": "Enable/disable embedding images into replacement messages (default = enable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "cache-mem-permille": {"type": "integer", "min": 1, "max": 150},
    "ovrd-auth-port-http": {"type": "integer", "min": 0, "max": 65535},
    "ovrd-auth-port-https": {"type": "integer", "min": 0, "max": 65535},
    "ovrd-auth-port-https-flow": {"type": "integer", "min": 0, "max": 65535},
    "ovrd-auth-port-warning": {"type": "integer", "min": 0, "max": 65535},
    "request-packet-size-limit": {"type": "integer", "min": 576, "max": 10000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_CACHE_MODE = [
    "ttl",
    "db-ver",
]
VALID_BODY_CACHE_PREFIX_MATCH = [
    "enable",
    "disable",
]
VALID_BODY_OVRD_AUTH_HTTPS = [
    "enable",
    "disable",
]
VALID_BODY_WARN_AUTH_HTTPS = [
    "enable",
    "disable",
]
VALID_BODY_CLOSE_PORTS = [
    "enable",
    "disable",
]
VALID_BODY_EMBED_IMAGE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_webfilter_fortiguard_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for webfilter/fortiguard."""
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


def validate_webfilter_fortiguard_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new webfilter/fortiguard object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "cache-mode" in payload:
        is_valid, error = _validate_enum_field(
            "cache-mode",
            payload["cache-mode"],
            VALID_BODY_CACHE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-prefix-match" in payload:
        is_valid, error = _validate_enum_field(
            "cache-prefix-match",
            payload["cache-prefix-match"],
            VALID_BODY_CACHE_PREFIX_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ovrd-auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "ovrd-auth-https",
            payload["ovrd-auth-https"],
            VALID_BODY_OVRD_AUTH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "warn-auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "warn-auth-https",
            payload["warn-auth-https"],
            VALID_BODY_WARN_AUTH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "close-ports" in payload:
        is_valid, error = _validate_enum_field(
            "close-ports",
            payload["close-ports"],
            VALID_BODY_CLOSE_PORTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "embed-image" in payload:
        is_valid, error = _validate_enum_field(
            "embed-image",
            payload["embed-image"],
            VALID_BODY_EMBED_IMAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_webfilter_fortiguard_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update webfilter/fortiguard."""
    # Validate enum values using central function
    if "cache-mode" in payload:
        is_valid, error = _validate_enum_field(
            "cache-mode",
            payload["cache-mode"],
            VALID_BODY_CACHE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cache-prefix-match" in payload:
        is_valid, error = _validate_enum_field(
            "cache-prefix-match",
            payload["cache-prefix-match"],
            VALID_BODY_CACHE_PREFIX_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ovrd-auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "ovrd-auth-https",
            payload["ovrd-auth-https"],
            VALID_BODY_OVRD_AUTH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "warn-auth-https" in payload:
        is_valid, error = _validate_enum_field(
            "warn-auth-https",
            payload["warn-auth-https"],
            VALID_BODY_WARN_AUTH_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "close-ports" in payload:
        is_valid, error = _validate_enum_field(
            "close-ports",
            payload["close-ports"],
            VALID_BODY_CLOSE_PORTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "embed-image" in payload:
        is_valid, error = _validate_enum_field(
            "embed-image",
            payload["embed-image"],
            VALID_BODY_EMBED_IMAGE,
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
    "endpoint": "webfilter/fortiguard",
    "category": "cmdb",
    "api_path": "webfilter/fortiguard",
    "help": "Configure FortiGuard Web Filter service.",
    "total_fields": 12,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
