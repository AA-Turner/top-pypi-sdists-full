"""Validation helpers for log/eventfilter - Auto-generated"""

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
    "event": "enable",
    "system": "enable",
    "vpn": "enable",
    "user": "enable",
    "router": "enable",
    "wireless-activity": "enable",
    "wan-opt": "enable",
    "endpoint": "enable",
    "ha": "enable",
    "security-rating": "enable",
    "fortiextender": "enable",
    "connector": "enable",
    "sdwan": "enable",
    "cifs": "enable",
    "switch-controller": "enable",
    "rest-api": "enable",
    "web-svc": "enable",
    "webproxy": "enable",
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
    "event": "option",  # Enable/disable event logging.
    "system": "option",  # Enable/disable system event logging.
    "vpn": "option",  # Enable/disable VPN event logging.
    "user": "option",  # Enable/disable user authentication event logging.
    "router": "option",  # Enable/disable router event logging.
    "wireless-activity": "option",  # Enable/disable wireless event logging.
    "wan-opt": "option",  # Enable/disable WAN optimization event logging.
    "endpoint": "option",  # Enable/disable endpoint event logging.
    "ha": "option",  # Enable/disable ha event logging.
    "security-rating": "option",  # Enable/disable Security Rating result logging.
    "fortiextender": "option",  # Enable/disable FortiExtender logging.
    "connector": "option",  # Enable/disable SDN connector logging.
    "sdwan": "option",  # Enable/disable SD-WAN logging.
    "cifs": "option",  # Enable/disable CIFS logging.
    "switch-controller": "option",  # Enable/disable Switch-Controller logging.
    "rest-api": "option",  # Enable/disable REST API logging.
    "web-svc": "option",  # Enable/disable web-svc performance logging.
    "webproxy": "option",  # Enable/disable web proxy event logging.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "event": "Enable/disable event logging.",
    "system": "Enable/disable system event logging.",
    "vpn": "Enable/disable VPN event logging.",
    "user": "Enable/disable user authentication event logging.",
    "router": "Enable/disable router event logging.",
    "wireless-activity": "Enable/disable wireless event logging.",
    "wan-opt": "Enable/disable WAN optimization event logging.",
    "endpoint": "Enable/disable endpoint event logging.",
    "ha": "Enable/disable ha event logging.",
    "security-rating": "Enable/disable Security Rating result logging.",
    "fortiextender": "Enable/disable FortiExtender logging.",
    "connector": "Enable/disable SDN connector logging.",
    "sdwan": "Enable/disable SD-WAN logging.",
    "cifs": "Enable/disable CIFS logging.",
    "switch-controller": "Enable/disable Switch-Controller logging.",
    "rest-api": "Enable/disable REST API logging.",
    "web-svc": "Enable/disable web-svc performance logging.",
    "webproxy": "Enable/disable web proxy event logging.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_EVENT = [
    "enable",
    "disable",
]
VALID_BODY_SYSTEM = [
    "enable",
    "disable",
]
VALID_BODY_VPN = [
    "enable",
    "disable",
]
VALID_BODY_USER = [
    "enable",
    "disable",
]
VALID_BODY_ROUTER = [
    "enable",
    "disable",
]
VALID_BODY_WIRELESS_ACTIVITY = [
    "enable",
    "disable",
]
VALID_BODY_WAN_OPT = [
    "enable",
    "disable",
]
VALID_BODY_ENDPOINT = [
    "enable",
    "disable",
]
VALID_BODY_HA = [
    "enable",
    "disable",
]
VALID_BODY_SECURITY_RATING = [
    "enable",
    "disable",
]
VALID_BODY_FORTIEXTENDER = [
    "enable",
    "disable",
]
VALID_BODY_CONNECTOR = [
    "enable",
    "disable",
]
VALID_BODY_SDWAN = [
    "enable",
    "disable",
]
VALID_BODY_CIFS = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER = [
    "enable",
    "disable",
]
VALID_BODY_REST_API = [
    "enable",
    "disable",
]
VALID_BODY_WEB_SVC = [
    "enable",
    "disable",
]
VALID_BODY_WEBPROXY = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_log_eventfilter_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for log/eventfilter."""
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


def validate_log_eventfilter_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new log/eventfilter object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "event" in payload:
        is_valid, error = _validate_enum_field(
            "event",
            payload["event"],
            VALID_BODY_EVENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system" in payload:
        is_valid, error = _validate_enum_field(
            "system",
            payload["system"],
            VALID_BODY_SYSTEM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn" in payload:
        is_valid, error = _validate_enum_field(
            "vpn",
            payload["vpn"],
            VALID_BODY_VPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user" in payload:
        is_valid, error = _validate_enum_field(
            "user",
            payload["user"],
            VALID_BODY_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "router" in payload:
        is_valid, error = _validate_enum_field(
            "router",
            payload["router"],
            VALID_BODY_ROUTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-activity" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-activity",
            payload["wireless-activity"],
            VALID_BODY_WIRELESS_ACTIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-opt" in payload:
        is_valid, error = _validate_enum_field(
            "wan-opt",
            payload["wan-opt"],
            VALID_BODY_WAN_OPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "endpoint" in payload:
        is_valid, error = _validate_enum_field(
            "endpoint",
            payload["endpoint"],
            VALID_BODY_ENDPOINT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha" in payload:
        is_valid, error = _validate_enum_field(
            "ha",
            payload["ha"],
            VALID_BODY_HA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-rating" in payload:
        is_valid, error = _validate_enum_field(
            "security-rating",
            payload["security-rating"],
            VALID_BODY_SECURITY_RATING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender",
            payload["fortiextender"],
            VALID_BODY_FORTIEXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "connector" in payload:
        is_valid, error = _validate_enum_field(
            "connector",
            payload["connector"],
            VALID_BODY_CONNECTOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdwan" in payload:
        is_valid, error = _validate_enum_field(
            "sdwan",
            payload["sdwan"],
            VALID_BODY_SDWAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cifs" in payload:
        is_valid, error = _validate_enum_field(
            "cifs",
            payload["cifs"],
            VALID_BODY_CIFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller",
            payload["switch-controller"],
            VALID_BODY_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api",
            payload["rest-api"],
            VALID_BODY_REST_API,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-svc" in payload:
        is_valid, error = _validate_enum_field(
            "web-svc",
            payload["web-svc"],
            VALID_BODY_WEB_SVC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webproxy" in payload:
        is_valid, error = _validate_enum_field(
            "webproxy",
            payload["webproxy"],
            VALID_BODY_WEBPROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_log_eventfilter_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update log/eventfilter."""
    # Validate enum values using central function
    if "event" in payload:
        is_valid, error = _validate_enum_field(
            "event",
            payload["event"],
            VALID_BODY_EVENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system" in payload:
        is_valid, error = _validate_enum_field(
            "system",
            payload["system"],
            VALID_BODY_SYSTEM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn" in payload:
        is_valid, error = _validate_enum_field(
            "vpn",
            payload["vpn"],
            VALID_BODY_VPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user" in payload:
        is_valid, error = _validate_enum_field(
            "user",
            payload["user"],
            VALID_BODY_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "router" in payload:
        is_valid, error = _validate_enum_field(
            "router",
            payload["router"],
            VALID_BODY_ROUTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-activity" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-activity",
            payload["wireless-activity"],
            VALID_BODY_WIRELESS_ACTIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-opt" in payload:
        is_valid, error = _validate_enum_field(
            "wan-opt",
            payload["wan-opt"],
            VALID_BODY_WAN_OPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "endpoint" in payload:
        is_valid, error = _validate_enum_field(
            "endpoint",
            payload["endpoint"],
            VALID_BODY_ENDPOINT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha" in payload:
        is_valid, error = _validate_enum_field(
            "ha",
            payload["ha"],
            VALID_BODY_HA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-rating" in payload:
        is_valid, error = _validate_enum_field(
            "security-rating",
            payload["security-rating"],
            VALID_BODY_SECURITY_RATING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender",
            payload["fortiextender"],
            VALID_BODY_FORTIEXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "connector" in payload:
        is_valid, error = _validate_enum_field(
            "connector",
            payload["connector"],
            VALID_BODY_CONNECTOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sdwan" in payload:
        is_valid, error = _validate_enum_field(
            "sdwan",
            payload["sdwan"],
            VALID_BODY_SDWAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cifs" in payload:
        is_valid, error = _validate_enum_field(
            "cifs",
            payload["cifs"],
            VALID_BODY_CIFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller",
            payload["switch-controller"],
            VALID_BODY_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api",
            payload["rest-api"],
            VALID_BODY_REST_API,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-svc" in payload:
        is_valid, error = _validate_enum_field(
            "web-svc",
            payload["web-svc"],
            VALID_BODY_WEB_SVC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webproxy" in payload:
        is_valid, error = _validate_enum_field(
            "webproxy",
            payload["webproxy"],
            VALID_BODY_WEBPROXY,
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
    "endpoint": "log/eventfilter",
    "category": "cmdb",
    "api_path": "log/eventfilter",
    "help": "Configure log event filters.",
    "total_fields": 18,
    "required_fields_count": 0,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
