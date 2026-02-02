"""Validation helpers for firewall/interface_policy6 - Auto-generated"""

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
    "interface",  # Monitored interface name from available interfaces.
    "srcaddr6",  # IPv6 address object to limit traffic monitoring to network traffic sent from the specified address or range.
    "dstaddr6",  # IPv6 address object to limit traffic monitoring to network traffic sent to the specified address or range.
    "application-list",  # Application list name.
    "ips-sensor",  # IPS sensor name.
    "av-profile",  # Antivirus profile.
    "webfilter-profile",  # Web filter profile.
    "casb-profile",  # CASB profile.
    "emailfilter-profile",  # Email filter profile.
    "dlp-profile",  # DLP profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "policyid": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "status": "enable",
    "logtraffic": "utm",
    "interface": "",
    "application-list-status": "disable",
    "application-list": "",
    "ips-sensor-status": "disable",
    "ips-sensor": "",
    "dsri": "disable",
    "av-profile-status": "disable",
    "av-profile": "",
    "webfilter-profile-status": "disable",
    "webfilter-profile": "",
    "casb-profile-status": "disable",
    "casb-profile": "",
    "emailfilter-profile-status": "disable",
    "emailfilter-profile": "",
    "dlp-profile-status": "disable",
    "dlp-profile": "",
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
    "policyid": "integer",  # Policy ID (0 - 4294967295).
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "status": "option",  # Enable/disable this policy.
    "comments": "var-string",  # Comments.
    "logtraffic": "option",  # Logging type to be used in this policy (Options: all | utm |
    "interface": "string",  # Monitored interface name from available interfaces.
    "srcaddr6": "string",  # IPv6 address object to limit traffic monitoring to network t
    "dstaddr6": "string",  # IPv6 address object to limit traffic monitoring to network t
    "service6": "string",  # Service name.
    "application-list-status": "option",  # Enable/disable application control.
    "application-list": "string",  # Application list name.
    "ips-sensor-status": "option",  # Enable/disable IPS.
    "ips-sensor": "string",  # IPS sensor name.
    "dsri": "option",  # Enable/disable DSRI.
    "av-profile-status": "option",  # Enable/disable antivirus.
    "av-profile": "string",  # Antivirus profile.
    "webfilter-profile-status": "option",  # Enable/disable web filtering.
    "webfilter-profile": "string",  # Web filter profile.
    "casb-profile-status": "option",  # Enable/disable CASB.
    "casb-profile": "string",  # CASB profile.
    "emailfilter-profile-status": "option",  # Enable/disable email filter.
    "emailfilter-profile": "string",  # Email filter profile.
    "dlp-profile-status": "option",  # Enable/disable DLP.
    "dlp-profile": "string",  # DLP profile name.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "policyid": "Policy ID (0 - 4294967295).",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "status": "Enable/disable this policy.",
    "comments": "Comments.",
    "logtraffic": "Logging type to be used in this policy (Options: all | utm | disable, Default: utm).",
    "interface": "Monitored interface name from available interfaces.",
    "srcaddr6": "IPv6 address object to limit traffic monitoring to network traffic sent from the specified address or range.",
    "dstaddr6": "IPv6 address object to limit traffic monitoring to network traffic sent to the specified address or range.",
    "service6": "Service name.",
    "application-list-status": "Enable/disable application control.",
    "application-list": "Application list name.",
    "ips-sensor-status": "Enable/disable IPS.",
    "ips-sensor": "IPS sensor name.",
    "dsri": "Enable/disable DSRI.",
    "av-profile-status": "Enable/disable antivirus.",
    "av-profile": "Antivirus profile.",
    "webfilter-profile-status": "Enable/disable web filtering.",
    "webfilter-profile": "Web filter profile.",
    "casb-profile-status": "Enable/disable CASB.",
    "casb-profile": "CASB profile.",
    "emailfilter-profile-status": "Enable/disable email filter.",
    "emailfilter-profile": "Email filter profile.",
    "dlp-profile-status": "Enable/disable DLP.",
    "dlp-profile": "DLP profile name.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967295},
    "interface": {"type": "string", "max_length": 35},
    "application-list": {"type": "string", "max_length": 47},
    "ips-sensor": {"type": "string", "max_length": 47},
    "av-profile": {"type": "string", "max_length": 47},
    "webfilter-profile": {"type": "string", "max_length": 47},
    "casb-profile": {"type": "string", "max_length": 47},
    "emailfilter-profile": {"type": "string", "max_length": 47},
    "dlp-profile": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "service6": {
        "name": {
            "type": "string",
            "help": "Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_LOGTRAFFIC = [
    "all",
    "utm",
    "disable",
]
VALID_BODY_APPLICATION_LIST_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IPS_SENSOR_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DSRI = [
    "enable",
    "disable",
]
VALID_BODY_AV_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_WEBFILTER_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_CASB_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_EMAILFILTER_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DLP_PROFILE_STATUS = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_interface_policy6_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/interface_policy6."""
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


def validate_firewall_interface_policy6_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/interface_policy6 object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-list-status" in payload:
        is_valid, error = _validate_enum_field(
            "application-list-status",
            payload["application-list-status"],
            VALID_BODY_APPLICATION_LIST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sensor-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sensor-status",
            payload["ips-sensor-status"],
            VALID_BODY_IPS_SENSOR_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "av-profile-status",
            payload["av-profile-status"],
            VALID_BODY_AV_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-profile-status",
            payload["webfilter-profile-status"],
            VALID_BODY_WEBFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "casb-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "casb-profile-status",
            payload["casb-profile-status"],
            VALID_BODY_CASB_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "emailfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "emailfilter-profile-status",
            payload["emailfilter-profile-status"],
            VALID_BODY_EMAILFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-profile-status",
            payload["dlp-profile-status"],
            VALID_BODY_DLP_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_interface_policy6_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/interface_policy6."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-list-status" in payload:
        is_valid, error = _validate_enum_field(
            "application-list-status",
            payload["application-list-status"],
            VALID_BODY_APPLICATION_LIST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sensor-status" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sensor-status",
            payload["ips-sensor-status"],
            VALID_BODY_IPS_SENSOR_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "av-profile-status",
            payload["av-profile-status"],
            VALID_BODY_AV_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-profile-status",
            payload["webfilter-profile-status"],
            VALID_BODY_WEBFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "casb-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "casb-profile-status",
            payload["casb-profile-status"],
            VALID_BODY_CASB_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "emailfilter-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "emailfilter-profile-status",
            payload["emailfilter-profile-status"],
            VALID_BODY_EMAILFILTER_PROFILE_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dlp-profile-status" in payload:
        is_valid, error = _validate_enum_field(
            "dlp-profile-status",
            payload["dlp-profile-status"],
            VALID_BODY_DLP_PROFILE_STATUS,
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
    "endpoint": "firewall/interface_policy6",
    "category": "cmdb",
    "api_path": "firewall/interface-policy6",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure IPv6 interface policies.",
    "total_fields": 24,
    "required_fields_count": 10,
    "fields_with_defaults_count": 20,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
