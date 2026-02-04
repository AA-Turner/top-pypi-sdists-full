"""Validation helpers for ztna/web_portal - Auto-generated"""

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
    "vip": "",
    "host": "",
    "decrypted-traffic-mirror": "",
    "log-blocked-traffic": "enable",
    "auth-portal": "disable",
    "auth-virtual-host": "",
    "vip6": "",
    "auth-rule": "",
    "display-bookmark": "enable",
    "focus-bookmark": "disable",
    "display-status": "enable",
    "display-history": "disable",
    "policy-auth-sso": "enable",
    "heading": "ZTNA Portal",
    "theme": "security-fabric",
    "clipboard": "enable",
    "default-window-width": 1024,
    "default-window-height": 768,
    "cookie-age": 60,
    "forticlient-download": "enable",
    "customize-forticlient-download-url": "disable",
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
    "name": "string",  # ZTNA proxy name.
    "vip": "string",  # Virtual IP name.
    "host": "string",  # Virtual or real host name.
    "decrypted-traffic-mirror": "string",  # Decrypted traffic mirror.
    "log-blocked-traffic": "option",  # Enable/disable logging of blocked traffic.
    "auth-portal": "option",  # Enable/disable authentication portal.
    "auth-virtual-host": "string",  # Virtual host for authentication portal.
    "vip6": "string",  # Virtual IPv6 name.
    "auth-rule": "string",  # Authentication Rule.
    "display-bookmark": "option",  # Enable to display the web portal bookmark widget.
    "focus-bookmark": "option",  # Enable to prioritize the placement of the bookmark section over the quick-connec
    "display-status": "option",  # Enable to display the web portal status widget.
    "display-history": "option",  # Enable to display the web portal user login history widget.
    "policy-auth-sso": "option",  # Enable policy sso authentication.
    "heading": "string",  # Web portal heading message.
    "theme": "option",  # Web portal color scheme.
    "clipboard": "option",  # Enable to support RDP/VPC clipboard functionality.
    "default-window-width": "integer",  # Screen width (range from 0 - 65535, default = 1024).
    "default-window-height": "integer",  # Screen height (range from 0 - 65535, default = 768).
    "cookie-age": "integer",  # Time in minutes that client web browsers should keep a cookie. Default is 60 min
    "forticlient-download": "option",  # Enable/disable download option for FortiClient.
    "customize-forticlient-download-url": "option",  # Enable support of customized download URL for FortiClient.
    "windows-forticlient-download-url": "var-string",  # Download URL for Windows FortiClient.
    "macos-forticlient-download-url": "var-string",  # Download URL for Mac FortiClient.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "ZTNA proxy name.",
    "vip": "Virtual IP name.",
    "host": "Virtual or real host name.",
    "decrypted-traffic-mirror": "Decrypted traffic mirror.",
    "log-blocked-traffic": "Enable/disable logging of blocked traffic.",
    "auth-portal": "Enable/disable authentication portal.",
    "auth-virtual-host": "Virtual host for authentication portal.",
    "vip6": "Virtual IPv6 name.",
    "auth-rule": "Authentication Rule.",
    "display-bookmark": "Enable to display the web portal bookmark widget.",
    "focus-bookmark": "Enable to prioritize the placement of the bookmark section over the quick-connection section in the ztna web-portal.",
    "display-status": "Enable to display the web portal status widget.",
    "display-history": "Enable to display the web portal user login history widget.",
    "policy-auth-sso": "Enable policy sso authentication.",
    "heading": "Web portal heading message.",
    "theme": "Web portal color scheme.",
    "clipboard": "Enable to support RDP/VPC clipboard functionality.",
    "default-window-width": "Screen width (range from 0 - 65535, default = 1024).",
    "default-window-height": "Screen height (range from 0 - 65535, default = 768).",
    "cookie-age": "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.",
    "forticlient-download": "Enable/disable download option for FortiClient.",
    "customize-forticlient-download-url": "Enable support of customized download URL for FortiClient.",
    "windows-forticlient-download-url": "Download URL for Windows FortiClient.",
    "macos-forticlient-download-url": "Download URL for Mac FortiClient.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "vip": {"type": "string", "max_length": 79},
    "host": {"type": "string", "max_length": 79},
    "decrypted-traffic-mirror": {"type": "string", "max_length": 35},
    "auth-virtual-host": {"type": "string", "max_length": 79},
    "vip6": {"type": "string", "max_length": 79},
    "auth-rule": {"type": "string", "max_length": 35},
    "heading": {"type": "string", "max_length": 31},
    "default-window-width": {"type": "integer", "min": 0, "max": 65535},
    "default-window-height": {"type": "integer", "min": 0, "max": 65535},
    "cookie-age": {"type": "integer", "min": 0, "max": 525600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_LOG_BLOCKED_TRAFFIC = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_PORTAL = [
    "disable",
    "enable",
]
VALID_BODY_DISPLAY_BOOKMARK = [
    "enable",
    "disable",
]
VALID_BODY_FOCUS_BOOKMARK = [
    "enable",
    "disable",
]
VALID_BODY_DISPLAY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DISPLAY_HISTORY = [
    "enable",
    "disable",
]
VALID_BODY_POLICY_AUTH_SSO = [
    "enable",
    "disable",
]
VALID_BODY_THEME = [
    "jade",
    "neutrino",
    "mariner",
    "graphite",
    "melongene",
    "jet-stream",
    "security-fabric",
    "dark-matter",
    "onyx",
    "eclipse",
]
VALID_BODY_CLIPBOARD = [
    "enable",
    "disable",
]
VALID_BODY_FORTICLIENT_DOWNLOAD = [
    "enable",
    "disable",
]
VALID_BODY_CUSTOMIZE_FORTICLIENT_DOWNLOAD_URL = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_ztna_web_portal_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for ztna/web_portal."""
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


def validate_ztna_web_portal_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new ztna/web_portal object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "log-blocked-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "log-blocked-traffic",
            payload["log-blocked-traffic"],
            VALID_BODY_LOG_BLOCKED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-portal" in payload:
        is_valid, error = _validate_enum_field(
            "auth-portal",
            payload["auth-portal"],
            VALID_BODY_AUTH_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-bookmark" in payload:
        is_valid, error = _validate_enum_field(
            "display-bookmark",
            payload["display-bookmark"],
            VALID_BODY_DISPLAY_BOOKMARK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "focus-bookmark" in payload:
        is_valid, error = _validate_enum_field(
            "focus-bookmark",
            payload["focus-bookmark"],
            VALID_BODY_FOCUS_BOOKMARK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-status" in payload:
        is_valid, error = _validate_enum_field(
            "display-status",
            payload["display-status"],
            VALID_BODY_DISPLAY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-history" in payload:
        is_valid, error = _validate_enum_field(
            "display-history",
            payload["display-history"],
            VALID_BODY_DISPLAY_HISTORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-auth-sso" in payload:
        is_valid, error = _validate_enum_field(
            "policy-auth-sso",
            payload["policy-auth-sso"],
            VALID_BODY_POLICY_AUTH_SSO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "theme" in payload:
        is_valid, error = _validate_enum_field(
            "theme",
            payload["theme"],
            VALID_BODY_THEME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clipboard" in payload:
        is_valid, error = _validate_enum_field(
            "clipboard",
            payload["clipboard"],
            VALID_BODY_CLIPBOARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticlient-download" in payload:
        is_valid, error = _validate_enum_field(
            "forticlient-download",
            payload["forticlient-download"],
            VALID_BODY_FORTICLIENT_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "customize-forticlient-download-url" in payload:
        is_valid, error = _validate_enum_field(
            "customize-forticlient-download-url",
            payload["customize-forticlient-download-url"],
            VALID_BODY_CUSTOMIZE_FORTICLIENT_DOWNLOAD_URL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_ztna_web_portal_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update ztna/web_portal."""
    # Validate enum values using central function
    if "log-blocked-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "log-blocked-traffic",
            payload["log-blocked-traffic"],
            VALID_BODY_LOG_BLOCKED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-portal" in payload:
        is_valid, error = _validate_enum_field(
            "auth-portal",
            payload["auth-portal"],
            VALID_BODY_AUTH_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-bookmark" in payload:
        is_valid, error = _validate_enum_field(
            "display-bookmark",
            payload["display-bookmark"],
            VALID_BODY_DISPLAY_BOOKMARK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "focus-bookmark" in payload:
        is_valid, error = _validate_enum_field(
            "focus-bookmark",
            payload["focus-bookmark"],
            VALID_BODY_FOCUS_BOOKMARK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-status" in payload:
        is_valid, error = _validate_enum_field(
            "display-status",
            payload["display-status"],
            VALID_BODY_DISPLAY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "display-history" in payload:
        is_valid, error = _validate_enum_field(
            "display-history",
            payload["display-history"],
            VALID_BODY_DISPLAY_HISTORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-auth-sso" in payload:
        is_valid, error = _validate_enum_field(
            "policy-auth-sso",
            payload["policy-auth-sso"],
            VALID_BODY_POLICY_AUTH_SSO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "theme" in payload:
        is_valid, error = _validate_enum_field(
            "theme",
            payload["theme"],
            VALID_BODY_THEME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clipboard" in payload:
        is_valid, error = _validate_enum_field(
            "clipboard",
            payload["clipboard"],
            VALID_BODY_CLIPBOARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticlient-download" in payload:
        is_valid, error = _validate_enum_field(
            "forticlient-download",
            payload["forticlient-download"],
            VALID_BODY_FORTICLIENT_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "customize-forticlient-download-url" in payload:
        is_valid, error = _validate_enum_field(
            "customize-forticlient-download-url",
            payload["customize-forticlient-download-url"],
            VALID_BODY_CUSTOMIZE_FORTICLIENT_DOWNLOAD_URL,
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
    "endpoint": "ztna/web_portal",
    "category": "cmdb",
    "api_path": "ztna/web-portal",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure ztna web-portal.",
    "total_fields": 24,
    "required_fields_count": 0,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
