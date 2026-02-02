"""Validation helpers for web_proxy/profile - Auto-generated"""

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
    "header-client-ip": "pass",
    "header-via-request": "pass",
    "header-via-response": "pass",
    "header-client-cert": "pass",
    "header-x-forwarded-for": "pass",
    "header-x-forwarded-client-cert": "pass",
    "header-front-end-https": "pass",
    "header-x-authenticated-user": "pass",
    "header-x-authenticated-groups": "pass",
    "strip-encoding": "disable",
    "log-header-change": "disable",
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
    "header-client-ip": "option",  # Action to take on the HTTP client-IP header in forwarded req
    "header-via-request": "option",  # Action to take on the HTTP via header in forwarded requests:
    "header-via-response": "option",  # Action to take on the HTTP via header in forwarded responses
    "header-client-cert": "option",  # Action to take on the HTTP Client-Cert/Client-Cert-Chain hea
    "header-x-forwarded-for": "option",  # Action to take on the HTTP x-forwarded-for header in forward
    "header-x-forwarded-client-cert": "option",  # Action to take on the HTTP x-forwarded-client-cert header in
    "header-front-end-https": "option",  # Action to take on the HTTP front-end-HTTPS header in forward
    "header-x-authenticated-user": "option",  # Action to take on the HTTP x-authenticated-user header in fo
    "header-x-authenticated-groups": "option",  # Action to take on the HTTP x-authenticated-groups header in 
    "strip-encoding": "option",  # Enable/disable stripping unsupported encoding from the reque
    "log-header-change": "option",  # Enable/disable logging HTTP header changes.
    "headers": "string",  # Configure HTTP forwarded requests headers.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "header-client-ip": "Action to take on the HTTP client-IP header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-via-request": "Action to take on the HTTP via header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-via-response": "Action to take on the HTTP via header in forwarded responses: forwards (pass), adds, or removes the HTTP header.",
    "header-client-cert": "Action to take on the HTTP Client-Cert/Client-Cert-Chain headers in forwarded responses: forwards (pass), adds, or removes the HTTP header.",
    "header-x-forwarded-for": "Action to take on the HTTP x-forwarded-for header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-x-forwarded-client-cert": "Action to take on the HTTP x-forwarded-client-cert header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-front-end-https": "Action to take on the HTTP front-end-HTTPS header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-x-authenticated-user": "Action to take on the HTTP x-authenticated-user header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "header-x-authenticated-groups": "Action to take on the HTTP x-authenticated-groups header in forwarded requests: forwards (pass), adds, or removes the HTTP header.",
    "strip-encoding": "Enable/disable stripping unsupported encoding from the request header.",
    "log-header-change": "Enable/disable logging HTTP header changes.",
    "headers": "Configure HTTP forwarded requests headers.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "headers": {
        "id": {
            "type": "integer",
            "help": "HTTP forwarded header id.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "HTTP forwarded header name.",
            "default": "",
            "max_length": 79,
        },
        "dstaddr": {
            "type": "string",
            "help": "Destination address and address group names.",
        },
        "dstaddr6": {
            "type": "string",
            "help": "Destination address and address group names (IPv6).",
        },
        "action": {
            "type": "option",
            "help": "Configure adding, removing, or logging of the HTTP header entry in HTTP requests and responses.",
            "default": "add-to-request",
            "options": ["add-to-request", "add-to-response", "remove-from-request", "remove-from-response", "monitor-request", "monitor-response"],
        },
        "content": {
            "type": "string",
            "help": "HTTP header content (max length: 3999 characters).",
            "default": "",
            "max_length": 3999,
        },
        "base64-encoding": {
            "type": "option",
            "help": "Enable/disable use of base64 encoding of HTTP content.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "add-option": {
            "type": "option",
            "help": "Configure options to append content to existing HTTP header or add new HTTP header.",
            "default": "new",
            "options": ["append", "new-on-not-found", "new", "replace", "replace-when-match"],
        },
        "protocol": {
            "type": "option",
            "help": "Configure protocol(s) to take add-option action on (HTTP, HTTPS, or both).",
            "default": "https http",
            "options": ["https", "http"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_HEADER_CLIENT_IP = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_VIA_REQUEST = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_VIA_RESPONSE = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_CLIENT_CERT = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_X_FORWARDED_FOR = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_X_FORWARDED_CLIENT_CERT = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_FRONT_END_HTTPS = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_X_AUTHENTICATED_USER = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_HEADER_X_AUTHENTICATED_GROUPS = [
    "pass",
    "add",
    "remove",
]
VALID_BODY_STRIP_ENCODING = [
    "enable",
    "disable",
]
VALID_BODY_LOG_HEADER_CHANGE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_web_proxy_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for web_proxy/profile."""
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


def validate_web_proxy_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new web_proxy/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "header-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "header-client-ip",
            payload["header-client-ip"],
            VALID_BODY_HEADER_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-via-request" in payload:
        is_valid, error = _validate_enum_field(
            "header-via-request",
            payload["header-via-request"],
            VALID_BODY_HEADER_VIA_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-via-response" in payload:
        is_valid, error = _validate_enum_field(
            "header-via-response",
            payload["header-via-response"],
            VALID_BODY_HEADER_VIA_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "header-client-cert",
            payload["header-client-cert"],
            VALID_BODY_HEADER_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-forwarded-for" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-forwarded-for",
            payload["header-x-forwarded-for"],
            VALID_BODY_HEADER_X_FORWARDED_FOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-forwarded-client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-forwarded-client-cert",
            payload["header-x-forwarded-client-cert"],
            VALID_BODY_HEADER_X_FORWARDED_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-front-end-https" in payload:
        is_valid, error = _validate_enum_field(
            "header-front-end-https",
            payload["header-front-end-https"],
            VALID_BODY_HEADER_FRONT_END_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-authenticated-user" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-authenticated-user",
            payload["header-x-authenticated-user"],
            VALID_BODY_HEADER_X_AUTHENTICATED_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-authenticated-groups" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-authenticated-groups",
            payload["header-x-authenticated-groups"],
            VALID_BODY_HEADER_X_AUTHENTICATED_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strip-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "strip-encoding",
            payload["strip-encoding"],
            VALID_BODY_STRIP_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-header-change" in payload:
        is_valid, error = _validate_enum_field(
            "log-header-change",
            payload["log-header-change"],
            VALID_BODY_LOG_HEADER_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_web_proxy_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update web_proxy/profile."""
    # Validate enum values using central function
    if "header-client-ip" in payload:
        is_valid, error = _validate_enum_field(
            "header-client-ip",
            payload["header-client-ip"],
            VALID_BODY_HEADER_CLIENT_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-via-request" in payload:
        is_valid, error = _validate_enum_field(
            "header-via-request",
            payload["header-via-request"],
            VALID_BODY_HEADER_VIA_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-via-response" in payload:
        is_valid, error = _validate_enum_field(
            "header-via-response",
            payload["header-via-response"],
            VALID_BODY_HEADER_VIA_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "header-client-cert",
            payload["header-client-cert"],
            VALID_BODY_HEADER_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-forwarded-for" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-forwarded-for",
            payload["header-x-forwarded-for"],
            VALID_BODY_HEADER_X_FORWARDED_FOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-forwarded-client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-forwarded-client-cert",
            payload["header-x-forwarded-client-cert"],
            VALID_BODY_HEADER_X_FORWARDED_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-front-end-https" in payload:
        is_valid, error = _validate_enum_field(
            "header-front-end-https",
            payload["header-front-end-https"],
            VALID_BODY_HEADER_FRONT_END_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-authenticated-user" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-authenticated-user",
            payload["header-x-authenticated-user"],
            VALID_BODY_HEADER_X_AUTHENTICATED_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "header-x-authenticated-groups" in payload:
        is_valid, error = _validate_enum_field(
            "header-x-authenticated-groups",
            payload["header-x-authenticated-groups"],
            VALID_BODY_HEADER_X_AUTHENTICATED_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strip-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "strip-encoding",
            payload["strip-encoding"],
            VALID_BODY_STRIP_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-header-change" in payload:
        is_valid, error = _validate_enum_field(
            "log-header-change",
            payload["log-header-change"],
            VALID_BODY_LOG_HEADER_CHANGE,
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
    "endpoint": "web_proxy/profile",
    "category": "cmdb",
    "api_path": "web-proxy/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure web proxy profiles.",
    "total_fields": 13,
    "required_fields_count": 0,
    "fields_with_defaults_count": 12,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
