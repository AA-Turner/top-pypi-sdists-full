"""Validation helpers for webfilter/urlfilter - Auto-generated"""

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
    "name",  # Name of URL filter list.
    "entries",  # URL filter entries.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "id": 0,
    "name": "",
    "one-arm-ips-urlfilter": "disable",
    "ip-addr-block": "disable",
    "ip4-mapped-ip6": "disable",
    "include-subdomains": "enable",
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
    "id": "integer",  # ID.
    "name": "string",  # Name of URL filter list.
    "comment": "var-string",  # Optional comments.
    "one-arm-ips-urlfilter": "option",  # Enable/disable DNS resolver for one-arm IPS URL filter opera
    "ip-addr-block": "option",  # Enable/disable blocking URLs when the hostname appears as an
    "ip4-mapped-ip6": "option",  # Enable/disable matching of IPv4 mapped IPv6 URLs.
    "include-subdomains": "option",  # Enable/disable matching subdomains. Applies only to simple t
    "entries": "string",  # URL filter entries.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "id": "ID.",
    "name": "Name of URL filter list.",
    "comment": "Optional comments.",
    "one-arm-ips-urlfilter": "Enable/disable DNS resolver for one-arm IPS URL filter operation.",
    "ip-addr-block": "Enable/disable blocking URLs when the hostname appears as an IP address.",
    "ip4-mapped-ip6": "Enable/disable matching of IPv4 mapped IPv6 URLs.",
    "include-subdomains": "Enable/disable matching subdomains. Applies only to simple type (default = enable).",
    "entries": "URL filter entries.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "id": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "entries": {
        "id": {
            "type": "integer",
            "help": "Id.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "url": {
            "type": "string",
            "help": "URL to be filtered.",
            "default": "",
            "max_length": 511,
        },
        "type": {
            "type": "option",
            "help": "Filter type (simple, regex, or wildcard).",
            "default": "simple",
            "options": ["simple", "regex", "wildcard"],
        },
        "action": {
            "type": "option",
            "help": "Action to take for URL filter matches.",
            "default": "exempt",
            "options": ["exempt", "block", "allow", "monitor"],
        },
        "antiphish-action": {
            "type": "option",
            "help": "Action to take for AntiPhishing matches.",
            "default": "block",
            "options": ["block", "log"],
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this URL filter.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "exempt": {
            "type": "option",
            "help": "If action is set to exempt, select the security profile operations that exempt URLs skip. Separate multiple options with a space.",
            "default": "av web-content activex-java-cookie dlp fortiguard range-block antiphish all",
            "options": ["av", "web-content", "activex-java-cookie", "dlp", "fortiguard", "range-block", "pass", "antiphish", "all"],
        },
        "web-proxy-profile": {
            "type": "string",
            "help": "Web proxy profile.",
            "default": "",
            "max_length": 63,
        },
        "referrer-host": {
            "type": "string",
            "help": "Referrer host name.",
            "default": "",
            "max_length": 255,
        },
        "dns-address-family": {
            "type": "option",
            "help": "Resolve IPv4 address, IPv6 address, or both from DNS server.",
            "default": "ipv4",
            "options": ["ipv4", "ipv6", "both"],
        },
        "comment": {
            "type": "var-string",
            "help": "Comment.",
            "max_length": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ONE_ARM_IPS_URLFILTER = [
    "enable",
    "disable",
]
VALID_BODY_IP_ADDR_BLOCK = [
    "enable",
    "disable",
]
VALID_BODY_IP4_MAPPED_IP6 = [
    "enable",
    "disable",
]
VALID_BODY_INCLUDE_SUBDOMAINS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_webfilter_urlfilter_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for webfilter/urlfilter."""
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


def validate_webfilter_urlfilter_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new webfilter/urlfilter object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "one-arm-ips-urlfilter" in payload:
        is_valid, error = _validate_enum_field(
            "one-arm-ips-urlfilter",
            payload["one-arm-ips-urlfilter"],
            VALID_BODY_ONE_ARM_IPS_URLFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-addr-block" in payload:
        is_valid, error = _validate_enum_field(
            "ip-addr-block",
            payload["ip-addr-block"],
            VALID_BODY_IP_ADDR_BLOCK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip4-mapped-ip6" in payload:
        is_valid, error = _validate_enum_field(
            "ip4-mapped-ip6",
            payload["ip4-mapped-ip6"],
            VALID_BODY_IP4_MAPPED_IP6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "include-subdomains",
            payload["include-subdomains"],
            VALID_BODY_INCLUDE_SUBDOMAINS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_webfilter_urlfilter_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update webfilter/urlfilter."""
    # Validate enum values using central function
    if "one-arm-ips-urlfilter" in payload:
        is_valid, error = _validate_enum_field(
            "one-arm-ips-urlfilter",
            payload["one-arm-ips-urlfilter"],
            VALID_BODY_ONE_ARM_IPS_URLFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-addr-block" in payload:
        is_valid, error = _validate_enum_field(
            "ip-addr-block",
            payload["ip-addr-block"],
            VALID_BODY_IP_ADDR_BLOCK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip4-mapped-ip6" in payload:
        is_valid, error = _validate_enum_field(
            "ip4-mapped-ip6",
            payload["ip4-mapped-ip6"],
            VALID_BODY_IP4_MAPPED_IP6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "include-subdomains",
            payload["include-subdomains"],
            VALID_BODY_INCLUDE_SUBDOMAINS,
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
    "endpoint": "webfilter/urlfilter",
    "category": "cmdb",
    "api_path": "webfilter/urlfilter",
    "mkey": "id",
    "mkey_type": "integer",
    "help": "Configure URL filter lists.",
    "total_fields": 8,
    "required_fields_count": 2,
    "fields_with_defaults_count": 6,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
