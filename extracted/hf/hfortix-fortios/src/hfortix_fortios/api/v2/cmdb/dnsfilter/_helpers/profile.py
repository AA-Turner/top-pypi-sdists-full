"""Validation helpers for dnsfilter/profile - Auto-generated"""

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
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "log-all-domain": "disable",
    "sdns-ftgd-err-log": "enable",
    "sdns-domain-log": "enable",
    "block-action": "redirect",
    "redirect-portal": "0.0.0.0",
    "redirect-portal6": "::",
    "block-botnet": "disable",
    "safe-search": "disable",
    "youtube-restrict": "strict",
    "strip-ech": "enable",
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
    "comment": "var-string",  # Comment.
    "domain-filter": "string",  # Domain filter settings.
    "ftgd-dns": "string",  # FortiGuard DNS Filter settings.
    "log-all-domain": "option",  # Enable/disable logging of all domains visited (detailed DNS logging).
    "sdns-ftgd-err-log": "option",  # Enable/disable FortiGuard SDNS rating error logging.
    "sdns-domain-log": "option",  # Enable/disable domain filtering and botnet domain logging.
    "block-action": "option",  # Action to take for blocked domains.
    "redirect-portal": "ipv4-address",  # IPv4 address of the SDNS redirect portal.
    "redirect-portal6": "ipv6-address",  # IPv6 address of the SDNS redirect portal.
    "block-botnet": "option",  # Enable/disable blocking botnet C&C DNS lookups.
    "safe-search": "option",  # Enable/disable Google, Bing, YouTube, Qwant, DuckDuckGo safe search.
    "youtube-restrict": "option",  # Set safe search for YouTube restriction level.
    "external-ip-blocklist": "string",  # One or more external IP block lists.
    "dns-translation": "string",  # DNS translation settings.
    "transparent-dns-database": "string",  # Transparent DNS database zones.
    "strip-ech": "option",  # Enable/disable removal of the encrypted client hello service parameter from supp
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Comment.",
    "domain-filter": "Domain filter settings.",
    "ftgd-dns": "FortiGuard DNS Filter settings.",
    "log-all-domain": "Enable/disable logging of all domains visited (detailed DNS logging).",
    "sdns-ftgd-err-log": "Enable/disable FortiGuard SDNS rating error logging.",
    "sdns-domain-log": "Enable/disable domain filtering and botnet domain logging.",
    "block-action": "Action to take for blocked domains.",
    "redirect-portal": "IPv4 address of the SDNS redirect portal.",
    "redirect-portal6": "IPv6 address of the SDNS redirect portal.",
    "block-botnet": "Enable/disable blocking botnet C&C DNS lookups.",
    "safe-search": "Enable/disable Google, Bing, YouTube, Qwant, DuckDuckGo safe search.",
    "youtube-restrict": "Set safe search for YouTube restriction level.",
    "external-ip-blocklist": "One or more external IP block lists.",
    "dns-translation": "DNS translation settings.",
    "transparent-dns-database": "Transparent DNS database zones.",
    "strip-ech": "Enable/disable removal of the encrypted client hello service parameter from supporting DNS RRs.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "domain-filter": {
        "domain-filter-table": {
            "type": "integer",
            "help": "DNS domain filter table ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "ftgd-dns": {
        "options": {
            "type": "option",
            "help": "FortiGuard DNS filter options.",
            "default": "",
            "options": ["error-allow", "ftgd-disable"],
        },
        "filters": {
            "type": "string",
            "help": "FortiGuard DNS domain filters.",
        },
    },
    "external-ip-blocklist": {
        "name": {
            "type": "string",
            "help": "External domain block list name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dns-translation": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "addr-type": {
            "type": "option",
            "help": "DNS translation type (IPv4 or IPv6).",
            "required": True,
            "default": "ipv4",
            "options": ["ipv4", "ipv6"],
        },
        "src": {
            "type": "ipv4-address",
            "help": "IPv4 address or subnet on the internal network to compare with the resolved address in DNS query replies. If the resolved address matches, the resolved address is substituted with dst.",
            "default": "0.0.0.0",
        },
        "dst": {
            "type": "ipv4-address",
            "help": "IPv4 address or subnet on the external network to substitute for the resolved address in DNS query replies. Can be single IP address or subnet on the external network, but number of addresses must equal number of mapped IP addresses in src.",
            "default": "0.0.0.0",
        },
        "netmask": {
            "type": "ipv4-netmask",
            "help": "If src and dst are subnets rather than single IP addresses, enter the netmask for both src and dst.",
            "default": "255.255.255.255",
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this DNS translation entry.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "src6": {
            "type": "ipv6-address",
            "help": "IPv6 address or subnet on the internal network to compare with the resolved address in DNS query replies. If the resolved address matches, the resolved address is substituted with dst6.",
            "default": "::",
        },
        "dst6": {
            "type": "ipv6-address",
            "help": "IPv6 address or subnet on the external network to substitute for the resolved address in DNS query replies. Can be single IP address or subnet on the external network, but number of addresses must equal number of mapped IP addresses in src6.",
            "default": "::",
        },
        "prefix": {
            "type": "integer",
            "help": "If src6 and dst6 are subnets rather than single IP addresses, enter the prefix for both src6 and dst6 (1 - 128, default = 128).",
            "default": 128,
            "min_value": 1,
            "max_value": 128,
        },
    },
    "transparent-dns-database": {
        "name": {
            "type": "string",
            "help": "DNS database zone name.",
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_LOG_ALL_DOMAIN = [
    "enable",
    "disable",
]
VALID_BODY_SDNS_FTGD_ERR_LOG = [
    "enable",
    "disable",
]
VALID_BODY_SDNS_DOMAIN_LOG = [
    "enable",
    "disable",
]
VALID_BODY_BLOCK_ACTION = [
    "block",
    "redirect",
    "block-sevrfail",
]
VALID_BODY_BLOCK_BOTNET = [
    "disable",
    "enable",
]
VALID_BODY_SAFE_SEARCH = [
    "disable",
    "enable",
]
VALID_BODY_YOUTUBE_RESTRICT = [
    "strict",
    "moderate",
    "none",
]
VALID_BODY_STRIP_ECH = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_dnsfilter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for dnsfilter/profile."""
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


def validate_dnsfilter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new dnsfilter/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "log-all-domain" in payload:
        is_valid, error = _validate_enum_field(
            "log-all-domain",
            payload["log-all-domain"],
            VALID_BODY_LOG_ALL_DOMAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-ftgd-err-log" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-ftgd-err-log",
            payload["sdns-ftgd-err-log"],
            VALID_BODY_SDNS_FTGD_ERR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-domain-log" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-domain-log",
            payload["sdns-domain-log"],
            VALID_BODY_SDNS_DOMAIN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-action" in payload:
        is_valid, error = _validate_enum_field(
            "block-action",
            payload["block-action"],
            VALID_BODY_BLOCK_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-botnet" in payload:
        is_valid, error = _validate_enum_field(
            "block-botnet",
            payload["block-botnet"],
            VALID_BODY_BLOCK_BOTNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "safe-search" in payload:
        is_valid, error = _validate_enum_field(
            "safe-search",
            payload["safe-search"],
            VALID_BODY_SAFE_SEARCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "youtube-restrict" in payload:
        is_valid, error = _validate_enum_field(
            "youtube-restrict",
            payload["youtube-restrict"],
            VALID_BODY_YOUTUBE_RESTRICT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strip-ech" in payload:
        is_valid, error = _validate_enum_field(
            "strip-ech",
            payload["strip-ech"],
            VALID_BODY_STRIP_ECH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_dnsfilter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update dnsfilter/profile."""
    # Validate enum values using central function
    if "log-all-domain" in payload:
        is_valid, error = _validate_enum_field(
            "log-all-domain",
            payload["log-all-domain"],
            VALID_BODY_LOG_ALL_DOMAIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-ftgd-err-log" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-ftgd-err-log",
            payload["sdns-ftgd-err-log"],
            VALID_BODY_SDNS_FTGD_ERR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdns-domain-log" in payload:
        is_valid, error = _validate_enum_field(
            "sdns-domain-log",
            payload["sdns-domain-log"],
            VALID_BODY_SDNS_DOMAIN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-action" in payload:
        is_valid, error = _validate_enum_field(
            "block-action",
            payload["block-action"],
            VALID_BODY_BLOCK_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-botnet" in payload:
        is_valid, error = _validate_enum_field(
            "block-botnet",
            payload["block-botnet"],
            VALID_BODY_BLOCK_BOTNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "safe-search" in payload:
        is_valid, error = _validate_enum_field(
            "safe-search",
            payload["safe-search"],
            VALID_BODY_SAFE_SEARCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "youtube-restrict" in payload:
        is_valid, error = _validate_enum_field(
            "youtube-restrict",
            payload["youtube-restrict"],
            VALID_BODY_YOUTUBE_RESTRICT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strip-ech" in payload:
        is_valid, error = _validate_enum_field(
            "strip-ech",
            payload["strip-ech"],
            VALID_BODY_STRIP_ECH,
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
    "endpoint": "dnsfilter/profile",
    "category": "cmdb",
    "api_path": "dnsfilter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure DNS domain filter profile.",
    "total_fields": 17,
    "required_fields_count": 1,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
