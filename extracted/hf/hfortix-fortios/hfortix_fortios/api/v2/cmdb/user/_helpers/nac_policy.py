"""Validation helpers for user/nac_policy - Auto-generated"""

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
    "description": "",
    "category": "device",
    "status": "enable",
    "match-type": "dynamic",
    "match-period": 0,
    "match-remove": "default",
    "mac": "",
    "hw-vendor": "",
    "type": "",
    "family": "",
    "os": "",
    "hw-version": "",
    "sw-version": "",
    "host": "",
    "user": "",
    "src": "",
    "user-group": "",
    "ems-tag": "",
    "fortivoice-tag": "",
    "switch-fortilink": "",
    "switch-mac-policy": "",
    "firewall-address": "",
    "ssid-policy": "",
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
    "name": "string",  # NAC policy name.
    "description": "string",  # Description for the NAC policy matching pattern.
    "category": "option",  # Category of NAC policy.
    "status": "option",  # Enable/disable NAC policy.
    "match-type": "option",  # Match and retain the devices based on the type.
    "match-period": "integer",  # Number of days the matched devices will be retained (0 - alw
    "match-remove": "option",  # Options to remove the matched override devices.
    "mac": "string",  # NAC policy matching MAC address.
    "hw-vendor": "string",  # NAC policy matching hardware vendor.
    "type": "string",  # NAC policy matching type.
    "family": "string",  # NAC policy matching family.
    "os": "string",  # NAC policy matching operating system.
    "hw-version": "string",  # NAC policy matching hardware version.
    "sw-version": "string",  # NAC policy matching software version.
    "host": "string",  # NAC policy matching host.
    "user": "string",  # NAC policy matching user.
    "src": "string",  # NAC policy matching source.
    "user-group": "string",  # NAC policy matching user group.
    "ems-tag": "string",  # NAC policy matching EMS tag.
    "fortivoice-tag": "string",  # NAC policy matching FortiVoice tag.
    "severity": "string",  # NAC policy matching devices vulnerability severity lists.
    "switch-fortilink": "string",  # FortiLink interface for which this NAC policy belongs to.
    "switch-group": "string",  # List of managed FortiSwitch groups on which NAC policy can b
    "switch-mac-policy": "string",  # Switch MAC policy action to be applied on the matched NAC po
    "firewall-address": "string",  # Dynamic firewall address to associate MAC which match this p
    "ssid-policy": "string",  # SSID policy to be applied on the matched NAC policy.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "NAC policy name.",
    "description": "Description for the NAC policy matching pattern.",
    "category": "Category of NAC policy.",
    "status": "Enable/disable NAC policy.",
    "match-type": "Match and retain the devices based on the type.",
    "match-period": "Number of days the matched devices will be retained (0 - always retain)",
    "match-remove": "Options to remove the matched override devices.",
    "mac": "NAC policy matching MAC address.",
    "hw-vendor": "NAC policy matching hardware vendor.",
    "type": "NAC policy matching type.",
    "family": "NAC policy matching family.",
    "os": "NAC policy matching operating system.",
    "hw-version": "NAC policy matching hardware version.",
    "sw-version": "NAC policy matching software version.",
    "host": "NAC policy matching host.",
    "user": "NAC policy matching user.",
    "src": "NAC policy matching source.",
    "user-group": "NAC policy matching user group.",
    "ems-tag": "NAC policy matching EMS tag.",
    "fortivoice-tag": "NAC policy matching FortiVoice tag.",
    "severity": "NAC policy matching devices vulnerability severity lists.",
    "switch-fortilink": "FortiLink interface for which this NAC policy belongs to.",
    "switch-group": "List of managed FortiSwitch groups on which NAC policy can be applied.",
    "switch-mac-policy": "Switch MAC policy action to be applied on the matched NAC policy.",
    "firewall-address": "Dynamic firewall address to associate MAC which match this policy.",
    "ssid-policy": "SSID policy to be applied on the matched NAC policy.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "description": {"type": "string", "max_length": 63},
    "match-period": {"type": "integer", "min": 0, "max": 120},
    "mac": {"type": "string", "max_length": 17},
    "hw-vendor": {"type": "string", "max_length": 15},
    "type": {"type": "string", "max_length": 15},
    "family": {"type": "string", "max_length": 31},
    "os": {"type": "string", "max_length": 31},
    "hw-version": {"type": "string", "max_length": 15},
    "sw-version": {"type": "string", "max_length": 15},
    "host": {"type": "string", "max_length": 64},
    "user": {"type": "string", "max_length": 64},
    "src": {"type": "string", "max_length": 15},
    "user-group": {"type": "string", "max_length": 35},
    "ems-tag": {"type": "string", "max_length": 79},
    "fortivoice-tag": {"type": "string", "max_length": 79},
    "switch-fortilink": {"type": "string", "max_length": 15},
    "switch-mac-policy": {"type": "string", "max_length": 63},
    "firewall-address": {"type": "string", "max_length": 79},
    "ssid-policy": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "severity": {
        "severity-num": {
            "type": "integer",
            "help": "Enter multiple severity levels, where 0 = Info, 1 = Low, ..., 4 = Critical",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4,
        },
    },
    "switch-group": {
        "name": {
            "type": "string",
            "help": "Managed FortiSwitch group name from available options.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_CATEGORY = [
    "device",
    "firewall-user",
    "ems-tag",
    "fortivoice-tag",
    "vulnerability",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MATCH_TYPE = [
    "dynamic",
    "override",
]
VALID_BODY_MATCH_REMOVE = [
    "default",
    "link-down",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_nac_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/nac_policy."""
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


def validate_user_nac_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/nac_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "category" in payload:
        is_valid, error = _validate_enum_field(
            "category",
            payload["category"],
            VALID_BODY_CATEGORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-type" in payload:
        is_valid, error = _validate_enum_field(
            "match-type",
            payload["match-type"],
            VALID_BODY_MATCH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-remove" in payload:
        is_valid, error = _validate_enum_field(
            "match-remove",
            payload["match-remove"],
            VALID_BODY_MATCH_REMOVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_nac_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/nac_policy."""
    # Validate enum values using central function
    if "category" in payload:
        is_valid, error = _validate_enum_field(
            "category",
            payload["category"],
            VALID_BODY_CATEGORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-type" in payload:
        is_valid, error = _validate_enum_field(
            "match-type",
            payload["match-type"],
            VALID_BODY_MATCH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-remove" in payload:
        is_valid, error = _validate_enum_field(
            "match-remove",
            payload["match-remove"],
            VALID_BODY_MATCH_REMOVE,
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
    "endpoint": "user/nac_policy",
    "category": "cmdb",
    "api_path": "user/nac-policy",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure NAC policy matching pattern to identify matching NAC devices.",
    "total_fields": 26,
    "required_fields_count": 0,
    "fields_with_defaults_count": 24,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
