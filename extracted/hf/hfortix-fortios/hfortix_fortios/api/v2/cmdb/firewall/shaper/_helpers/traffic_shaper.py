"""Validation helpers for firewall/shaper/traffic_shaper - Auto-generated"""

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
    "guaranteed-bandwidth": 0,
    "maximum-bandwidth": 0,
    "bandwidth-unit": "kbps",
    "priority": "high",
    "per-policy": "disable",
    "diffserv": "disable",
    "diffservcode": "",
    "dscp-marking-method": "static",
    "exceed-bandwidth": 0,
    "exceed-dscp": "",
    "maximum-dscp": "",
    "cos-marking": "disable",
    "cos-marking-method": "static",
    "cos": "",
    "exceed-cos": "",
    "maximum-cos": "",
    "overhead": 0,
    "exceed-class-id": 0,
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
    "name": "string",  # Traffic shaper name.
    "guaranteed-bandwidth": "integer",  # Amount of bandwidth guaranteed for this shaper (0 - 80000000
    "maximum-bandwidth": "integer",  # Upper bandwidth limit enforced by this shaper (0 - 80000000)
    "bandwidth-unit": "option",  # Unit of measurement for guaranteed and maximum bandwidth for
    "priority": "option",  # Higher priority traffic is more likely to be forwarded witho
    "per-policy": "option",  # Enable/disable applying a separate shaper for each policy. F
    "diffserv": "option",  # Enable/disable changing the DiffServ setting applied to traf
    "diffservcode": "user",  # DiffServ setting to be applied to traffic accepted by this s
    "dscp-marking-method": "option",  # Select DSCP marking method.
    "exceed-bandwidth": "integer",  # Exceed bandwidth used for DSCP/VLAN CoS multi-stage marking.
    "exceed-dscp": "user",  # DSCP mark for traffic in guaranteed-bandwidth and exceed-ban
    "maximum-dscp": "user",  # DSCP mark for traffic in exceed-bandwidth and maximum-bandwi
    "cos-marking": "option",  # Enable/disable VLAN CoS marking.
    "cos-marking-method": "option",  # Select VLAN CoS marking method.
    "cos": "user",  # VLAN CoS mark.
    "exceed-cos": "user",  # VLAN CoS mark for traffic in [guaranteed-bandwidth, exceed-b
    "maximum-cos": "user",  # VLAN CoS mark for traffic in [exceed-bandwidth, maximum-band
    "overhead": "integer",  # Per-packet size overhead used in rate computations.
    "exceed-class-id": "integer",  # Class ID for traffic in guaranteed-bandwidth and maximum-ban
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Traffic shaper name.",
    "guaranteed-bandwidth": "Amount of bandwidth guaranteed for this shaper (0 - 80000000). Units depend on the bandwidth-unit setting.",
    "maximum-bandwidth": "Upper bandwidth limit enforced by this shaper (0 - 80000000). 0 means no limit. Units depend on the bandwidth-unit setting.",
    "bandwidth-unit": "Unit of measurement for guaranteed and maximum bandwidth for this shaper (Kbps, Mbps or Gbps).",
    "priority": "Higher priority traffic is more likely to be forwarded without delays and without compromising the guaranteed bandwidth.",
    "per-policy": "Enable/disable applying a separate shaper for each policy. For example, if enabled the guaranteed bandwidth is applied separately for each policy.",
    "diffserv": "Enable/disable changing the DiffServ setting applied to traffic accepted by this shaper.",
    "diffservcode": "DiffServ setting to be applied to traffic accepted by this shaper.",
    "dscp-marking-method": "Select DSCP marking method.",
    "exceed-bandwidth": "Exceed bandwidth used for DSCP/VLAN CoS multi-stage marking. Units depend on the bandwidth-unit setting.",
    "exceed-dscp": "DSCP mark for traffic in guaranteed-bandwidth and exceed-bandwidth.",
    "maximum-dscp": "DSCP mark for traffic in exceed-bandwidth and maximum-bandwidth.",
    "cos-marking": "Enable/disable VLAN CoS marking.",
    "cos-marking-method": "Select VLAN CoS marking method.",
    "cos": "VLAN CoS mark.",
    "exceed-cos": "VLAN CoS mark for traffic in [guaranteed-bandwidth, exceed-bandwidth].",
    "maximum-cos": "VLAN CoS mark for traffic in [exceed-bandwidth, maximum-bandwidth].",
    "overhead": "Per-packet size overhead used in rate computations.",
    "exceed-class-id": "Class ID for traffic in guaranteed-bandwidth and maximum-bandwidth.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "guaranteed-bandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "maximum-bandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "exceed-bandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "overhead": {"type": "integer", "min": 0, "max": 100},
    "exceed-class-id": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_BANDWIDTH_UNIT = [
    "kbps",
    "mbps",
    "gbps",
]
VALID_BODY_PRIORITY = [
    "low",
    "medium",
    "high",
]
VALID_BODY_PER_POLICY = [
    "disable",
    "enable",
]
VALID_BODY_DIFFSERV = [
    "enable",
    "disable",
]
VALID_BODY_DSCP_MARKING_METHOD = [
    "multi-stage",
    "static",
]
VALID_BODY_COS_MARKING = [
    "enable",
    "disable",
]
VALID_BODY_COS_MARKING_METHOD = [
    "multi-stage",
    "static",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_shaper_traffic_shaper_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/shaper/traffic_shaper."""
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


def validate_firewall_shaper_traffic_shaper_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/shaper/traffic_shaper object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "bandwidth-unit" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-unit",
            payload["bandwidth-unit"],
            VALID_BODY_BANDWIDTH_UNIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-policy" in payload:
        is_valid, error = _validate_enum_field(
            "per-policy",
            payload["per-policy"],
            VALID_BODY_PER_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv",
            payload["diffserv"],
            VALID_BODY_DIFFSERV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dscp-marking-method" in payload:
        is_valid, error = _validate_enum_field(
            "dscp-marking-method",
            payload["dscp-marking-method"],
            VALID_BODY_DSCP_MARKING_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cos-marking" in payload:
        is_valid, error = _validate_enum_field(
            "cos-marking",
            payload["cos-marking"],
            VALID_BODY_COS_MARKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cos-marking-method" in payload:
        is_valid, error = _validate_enum_field(
            "cos-marking-method",
            payload["cos-marking-method"],
            VALID_BODY_COS_MARKING_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_shaper_traffic_shaper_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/shaper/traffic_shaper."""
    # Validate enum values using central function
    if "bandwidth-unit" in payload:
        is_valid, error = _validate_enum_field(
            "bandwidth-unit",
            payload["bandwidth-unit"],
            VALID_BODY_BANDWIDTH_UNIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority" in payload:
        is_valid, error = _validate_enum_field(
            "priority",
            payload["priority"],
            VALID_BODY_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-policy" in payload:
        is_valid, error = _validate_enum_field(
            "per-policy",
            payload["per-policy"],
            VALID_BODY_PER_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv",
            payload["diffserv"],
            VALID_BODY_DIFFSERV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dscp-marking-method" in payload:
        is_valid, error = _validate_enum_field(
            "dscp-marking-method",
            payload["dscp-marking-method"],
            VALID_BODY_DSCP_MARKING_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cos-marking" in payload:
        is_valid, error = _validate_enum_field(
            "cos-marking",
            payload["cos-marking"],
            VALID_BODY_COS_MARKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cos-marking-method" in payload:
        is_valid, error = _validate_enum_field(
            "cos-marking-method",
            payload["cos-marking-method"],
            VALID_BODY_COS_MARKING_METHOD,
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
    "endpoint": "firewall/shaper/traffic_shaper",
    "category": "cmdb",
    "api_path": "firewall.shaper/traffic-shaper",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure shared traffic shaper.",
    "total_fields": 19,
    "required_fields_count": 0,
    "fields_with_defaults_count": 19,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
