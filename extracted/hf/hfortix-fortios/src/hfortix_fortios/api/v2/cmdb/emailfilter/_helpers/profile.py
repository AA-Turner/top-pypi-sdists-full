"""Validation helpers for emailfilter/profile - Auto-generated"""

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
    "feature-set": "flow",
    "replacemsg-group": "",
    "spam-log": "enable",
    "spam-log-fortiguard-response": "disable",
    "spam-filtering": "disable",
    "external": "disable",
    "options": "",
    "spam-bword-threshold": 10,
    "spam-bword-table": 0,
    "spam-bal-table": 0,
    "spam-mheader-table": 0,
    "spam-rbl-table": 0,
    "spam-iptrust-table": 0,
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
    "feature-set": "option",  # Flow/proxy feature set.
    "replacemsg-group": "string",  # Replacement message group.
    "spam-log": "option",  # Enable/disable spam logging for email filtering.
    "spam-log-fortiguard-response": "option",  # Enable/disable logging FortiGuard spam response.
    "spam-filtering": "option",  # Enable/disable spam filtering.
    "external": "option",  # Enable/disable external Email inspection.
    "options": "option",  # Options.
    "imap": "string",  # IMAP.
    "pop3": "string",  # POP3.
    "smtp": "string",  # SMTP.
    "mapi": "string",  # MAPI.
    "msn-hotmail": "string",  # MSN Hotmail.
    "yahoo-mail": "string",  # Yahoo! Mail.
    "gmail": "string",  # Gmail.
    "other-webmails": "string",  # Other supported webmails.
    "spam-bword-threshold": "integer",  # Spam banned word threshold.
    "spam-bword-table": "integer",  # Anti-spam banned word table ID.
    "spam-bal-table": "integer",  # Anti-spam block/allow list table ID.
    "spam-mheader-table": "integer",  # Anti-spam MIME header table ID.
    "spam-rbl-table": "integer",  # Anti-spam DNSBL table ID.
    "spam-iptrust-table": "integer",  # Anti-spam IP trust table ID.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Comment.",
    "feature-set": "Flow/proxy feature set.",
    "replacemsg-group": "Replacement message group.",
    "spam-log": "Enable/disable spam logging for email filtering.",
    "spam-log-fortiguard-response": "Enable/disable logging FortiGuard spam response.",
    "spam-filtering": "Enable/disable spam filtering.",
    "external": "Enable/disable external Email inspection.",
    "options": "Options.",
    "imap": "IMAP.",
    "pop3": "POP3.",
    "smtp": "SMTP.",
    "mapi": "MAPI.",
    "msn-hotmail": "MSN Hotmail.",
    "yahoo-mail": "Yahoo! Mail.",
    "gmail": "Gmail.",
    "other-webmails": "Other supported webmails.",
    "spam-bword-threshold": "Spam banned word threshold.",
    "spam-bword-table": "Anti-spam banned word table ID.",
    "spam-bal-table": "Anti-spam block/allow list table ID.",
    "spam-mheader-table": "Anti-spam MIME header table ID.",
    "spam-rbl-table": "Anti-spam DNSBL table ID.",
    "spam-iptrust-table": "Anti-spam IP trust table ID.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
    "spam-bword-threshold": {"type": "integer", "min": 0, "max": 2147483647},
    "spam-bword-table": {"type": "integer", "min": 0, "max": 4294967295},
    "spam-bal-table": {"type": "integer", "min": 0, "max": 4294967295},
    "spam-mheader-table": {"type": "integer", "min": 0, "max": 4294967295},
    "spam-rbl-table": {"type": "integer", "min": 0, "max": 4294967295},
    "spam-iptrust-table": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "imap": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "action": {
            "type": "option",
            "help": "Action for spam email.",
            "default": "tag",
            "options": ["pass", "tag"],
        },
        "tag-type": {
            "type": "option",
            "help": "Tag subject or header for spam email.",
            "default": "subject spaminfo",
            "options": ["subject", "header", "spaminfo"],
        },
        "tag-msg": {
            "type": "string",
            "help": "Subject text or header added to spam email.",
            "default": "Spam",
            "max_length": 63,
        },
    },
    "pop3": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "action": {
            "type": "option",
            "help": "Action for spam email.",
            "default": "tag",
            "options": ["pass", "tag"],
        },
        "tag-type": {
            "type": "option",
            "help": "Tag subject or header for spam email.",
            "default": "subject spaminfo",
            "options": ["subject", "header", "spaminfo"],
        },
        "tag-msg": {
            "type": "string",
            "help": "Subject text or header added to spam email.",
            "default": "Spam",
            "max_length": 63,
        },
    },
    "smtp": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "action": {
            "type": "option",
            "help": "Action for spam email.",
            "default": "discard",
            "options": ["pass", "tag", "discard"],
        },
        "tag-type": {
            "type": "option",
            "help": "Tag subject or header for spam email.",
            "default": "subject spaminfo",
            "options": ["subject", "header", "spaminfo"],
        },
        "tag-msg": {
            "type": "string",
            "help": "Subject text or header added to spam email.",
            "default": "Spam",
            "max_length": 63,
        },
        "hdrip": {
            "type": "option",
            "help": "Enable/disable SMTP email header IP checks for spamfsip, spamrbl, and spambal filters.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "local-override": {
            "type": "option",
            "help": "Enable/disable local filter to override SMTP remote check result.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "mapi": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "action": {
            "type": "option",
            "help": "Action for spam email.",
            "default": "pass",
            "options": ["pass", "discard"],
        },
    },
    "msn-hotmail": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "yahoo-mail": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "gmail": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "other-webmails": {
        "log-all": {
            "type": "option",
            "help": "Enable/disable logging of all email traffic.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FEATURE_SET = [
    "flow",
    "proxy",
]
VALID_BODY_SPAM_LOG = [
    "disable",
    "enable",
]
VALID_BODY_SPAM_LOG_FORTIGUARD_RESPONSE = [
    "disable",
    "enable",
]
VALID_BODY_SPAM_FILTERING = [
    "enable",
    "disable",
]
VALID_BODY_EXTERNAL = [
    "enable",
    "disable",
]
VALID_BODY_OPTIONS = [
    "bannedword",
    "spambal",
    "spamfsip",
    "spamfssubmit",
    "spamfschksum",
    "spamfsurl",
    "spamhelodns",
    "spamraddrdns",
    "spamrbl",
    "spamhdrcheck",
    "spamfsphish",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_emailfilter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for emailfilter/profile."""
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


def validate_emailfilter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new emailfilter/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-log" in payload:
        is_valid, error = _validate_enum_field(
            "spam-log",
            payload["spam-log"],
            VALID_BODY_SPAM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-log-fortiguard-response" in payload:
        is_valid, error = _validate_enum_field(
            "spam-log-fortiguard-response",
            payload["spam-log-fortiguard-response"],
            VALID_BODY_SPAM_LOG_FORTIGUARD_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-filtering" in payload:
        is_valid, error = _validate_enum_field(
            "spam-filtering",
            payload["spam-filtering"],
            VALID_BODY_SPAM_FILTERING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_emailfilter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update emailfilter/profile."""
    # Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-log" in payload:
        is_valid, error = _validate_enum_field(
            "spam-log",
            payload["spam-log"],
            VALID_BODY_SPAM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-log-fortiguard-response" in payload:
        is_valid, error = _validate_enum_field(
            "spam-log-fortiguard-response",
            payload["spam-log-fortiguard-response"],
            VALID_BODY_SPAM_LOG_FORTIGUARD_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spam-filtering" in payload:
        is_valid, error = _validate_enum_field(
            "spam-filtering",
            payload["spam-filtering"],
            VALID_BODY_SPAM_FILTERING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
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
    "endpoint": "emailfilter/profile",
    "category": "cmdb",
    "api_path": "emailfilter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Email Filter profiles.",
    "total_fields": 23,
    "required_fields_count": 1,
    "fields_with_defaults_count": 14,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
