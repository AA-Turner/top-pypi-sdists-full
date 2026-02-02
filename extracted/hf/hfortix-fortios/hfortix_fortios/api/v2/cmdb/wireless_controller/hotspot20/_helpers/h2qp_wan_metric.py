"""Validation helpers for wireless_controller/hotspot20/h2qp_wan_metric - Auto-generated"""

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
    "link-status": "up",
    "symmetric-wan-link": "asymmetric",
    "link-at-capacity": "disable",
    "uplink-speed": 2400,
    "downlink-speed": 2400,
    "uplink-load": 0,
    "downlink-load": 0,
    "load-measurement-duration": 0,
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
    "name": "string",  # WAN metric name.
    "link-status": "option",  # Link status.
    "symmetric-wan-link": "option",  # WAN link symmetry.
    "link-at-capacity": "option",  # Link at capacity.
    "uplink-speed": "integer",  # Uplink speed (in kilobits/s).
    "downlink-speed": "integer",  # Downlink speed (in kilobits/s).
    "uplink-load": "integer",  # Uplink load.
    "downlink-load": "integer",  # Downlink load.
    "load-measurement-duration": "integer",  # Load measurement duration (in tenths of a second).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WAN metric name.",
    "link-status": "Link status.",
    "symmetric-wan-link": "WAN link symmetry.",
    "link-at-capacity": "Link at capacity.",
    "uplink-speed": "Uplink speed (in kilobits/s).",
    "downlink-speed": "Downlink speed (in kilobits/s).",
    "uplink-load": "Uplink load.",
    "downlink-load": "Downlink load.",
    "load-measurement-duration": "Load measurement duration (in tenths of a second).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "uplink-speed": {"type": "integer", "min": 0, "max": 4294967295},
    "downlink-speed": {"type": "integer", "min": 0, "max": 4294967295},
    "uplink-load": {"type": "integer", "min": 0, "max": 255},
    "downlink-load": {"type": "integer", "min": 0, "max": 255},
    "load-measurement-duration": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_LINK_STATUS = [
    "up",
    "down",
    "in-test",
]
VALID_BODY_SYMMETRIC_WAN_LINK = [
    "symmetric",
    "asymmetric",
]
VALID_BODY_LINK_AT_CAPACITY = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_hotspot20_h2qp_wan_metric_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/hotspot20/h2qp_wan_metric."""
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


def validate_wireless_controller_hotspot20_h2qp_wan_metric_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/hotspot20/h2qp_wan_metric object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "link-status" in payload:
        is_valid, error = _validate_enum_field(
            "link-status",
            payload["link-status"],
            VALID_BODY_LINK_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "symmetric-wan-link" in payload:
        is_valid, error = _validate_enum_field(
            "symmetric-wan-link",
            payload["symmetric-wan-link"],
            VALID_BODY_SYMMETRIC_WAN_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-at-capacity" in payload:
        is_valid, error = _validate_enum_field(
            "link-at-capacity",
            payload["link-at-capacity"],
            VALID_BODY_LINK_AT_CAPACITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_hotspot20_h2qp_wan_metric_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/hotspot20/h2qp_wan_metric."""
    # Validate enum values using central function
    if "link-status" in payload:
        is_valid, error = _validate_enum_field(
            "link-status",
            payload["link-status"],
            VALID_BODY_LINK_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "symmetric-wan-link" in payload:
        is_valid, error = _validate_enum_field(
            "symmetric-wan-link",
            payload["symmetric-wan-link"],
            VALID_BODY_SYMMETRIC_WAN_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-at-capacity" in payload:
        is_valid, error = _validate_enum_field(
            "link-at-capacity",
            payload["link-at-capacity"],
            VALID_BODY_LINK_AT_CAPACITY,
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
    "endpoint": "wireless_controller/hotspot20/h2qp_wan_metric",
    "category": "cmdb",
    "api_path": "wireless-controller.hotspot20/h2qp-wan-metric",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure WAN metrics.",
    "total_fields": 9,
    "required_fields_count": 0,
    "fields_with_defaults_count": 9,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
