"""Validation helpers for ztna/web_portal_bookmark - Auto-generated"""

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
    "name": "string",  # Bookmark name.
    "users": "string",  # User name.
    "groups": "string",  # User groups.
    "bookmarks": "string",  # Bookmark table.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Bookmark name.",
    "users": "User name.",
    "groups": "User groups.",
    "bookmarks": "Bookmark table.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "users": {
        "name": {
            "type": "string",
            "help": "User name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "groups": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "bookmarks": {
        "name": {
            "type": "string",
            "help": "Bookmark name.",
            "default": "",
            "max_length": 35,
        },
        "apptype": {
            "type": "option",
            "help": "Application type.",
            "required": True,
            "default": "web",
            "options": ["ftp", "rdp", "sftp", "smb", "ssh", "telnet", "vnc", "web"],
        },
        "url": {
            "type": "var-string",
            "help": "URL parameter.",
            "required": True,
            "max_length": 128,
        },
        "host": {
            "type": "var-string",
            "help": "Host name/IP parameter.",
            "required": True,
            "max_length": 128,
        },
        "folder": {
            "type": "var-string",
            "help": "Network shared file folder parameter.",
            "required": True,
            "max_length": 128,
        },
        "domain": {
            "type": "var-string",
            "help": "Login domain.",
            "max_length": 128,
        },
        "description": {
            "type": "var-string",
            "help": "Description.",
            "max_length": 128,
        },
        "keyboard-layout": {
            "type": "option",
            "help": "Keyboard layout.",
            "default": "en-us",
            "options": ["ar-101", "ar-102", "ar-102-azerty", "can-mul", "cz", "cz-qwerty", "cz-pr", "da", "nl", "de", "de-ch", "de-ibm", "en-uk", "en-uk-ext", "en-us", "en-us-dvorak", "es", "es-var", "fi", "fi-sami", "fr", "fr-apple", "fr-ca", "fr-ch", "fr-be", "hr", "hu", "hu-101", "it", "it-142", "ja", "ja-106", "ko", "la-am", "lt", "lt-ibm", "lt-std", "lav-std", "lav-leg", "mk", "mk-std", "no", "no-sami", "pol-214", "pol-pr", "pt", "pt-br", "pt-br-abnt2", "ru", "ru-mne", "ru-t", "sl", "sv", "sv-sami", "tuk", "tur-f", "tur-q", "zh-sym-sg-us", "zh-sym-us", "zh-tr-hk", "zh-tr-mo", "zh-tr-us"],
        },
        "security": {
            "type": "option",
            "help": "Security mode for RDP connection (default = any).",
            "default": "any",
            "options": ["any", "rdp", "nla", "tls"],
        },
        "send-preconnection-id": {
            "type": "option",
            "help": "Enable/disable sending of preconnection ID.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "preconnection-id": {
            "type": "integer",
            "help": "The numeric ID of the RDP source (0-4294967295).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "preconnection-blob": {
            "type": "var-string",
            "help": "An arbitrary string which identifies the RDP source.",
            "max_length": 511,
        },
        "load-balancing-info": {
            "type": "var-string",
            "help": "The load balancing information or cookie which should be provided to the connection broker.",
            "max_length": 511,
        },
        "restricted-admin": {
            "type": "option",
            "help": "Enable/disable restricted admin mode for RDP.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "port": {
            "type": "integer",
            "help": "Remote port.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "logon-user": {
            "type": "var-string",
            "help": "Logon user.",
            "max_length": 35,
        },
        "logon-password": {
            "type": "password",
            "help": "Logon password.",
            "max_length": 128,
        },
        "color-depth": {
            "type": "option",
            "help": "Color depth per pixel.",
            "default": "16",
            "options": ["32", "16", "8"],
        },
        "sso": {
            "type": "option",
            "help": "Single sign-on.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "width": {
            "type": "integer",
            "help": "Screen width (range from 0 - 65535, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "height": {
            "type": "integer",
            "help": "Screen height (range from 0 - 65535, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "vnc-keyboard-layout": {
            "type": "option",
            "help": "Keyboard layout.",
            "default": "default",
            "options": ["default", "da", "nl", "en-uk", "en-uk-ext", "fi", "fr", "fr-be", "fr-ca-mul", "de", "de-ch", "it", "it-142", "pt", "pt-br-abnt2", "no", "gd", "es", "sv", "us-intl"],
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ztna_web_portal_bookmark_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ztna/web_portal_bookmark."""
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


def validate_ztna_web_portal_bookmark_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ztna/web_portal_bookmark object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ztna_web_portal_bookmark_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ztna/web_portal_bookmark."""
    # Validate enum values using central function

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
    "endpoint": "ztna/web_portal_bookmark",
    "category": "cmdb",
    "api_path": "ztna/web-portal-bookmark",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure ztna web-portal bookmark.",
    "total_fields": 4,
    "required_fields_count": 0,
    "fields_with_defaults_count": 1,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
