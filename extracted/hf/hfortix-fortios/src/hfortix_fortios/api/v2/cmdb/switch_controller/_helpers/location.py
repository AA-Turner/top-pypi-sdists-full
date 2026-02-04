"""Validation helpers for switch_controller/location - Auto-generated"""

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
    "name": "string",  # Unique location item name.
    "address-civic": "string",  # Configure location civic address.
    "coordinates": "string",  # Configure location GPS coordinates.
    "elin-number": "string",  # Configure location ELIN number.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Unique location item name.",
    "address-civic": "Configure location civic address.",
    "coordinates": "Configure location GPS coordinates.",
    "elin-number": "Configure location ELIN number.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "address-civic": {
        "additional": {
            "type": "string",
            "help": "Location additional details.",
            "default": "",
            "max_length": 47,
        },
        "additional-code": {
            "type": "string",
            "help": "Location additional code details.",
            "default": "",
            "max_length": 47,
        },
        "block": {
            "type": "string",
            "help": "Location block details.",
            "default": "",
            "max_length": 47,
        },
        "branch-road": {
            "type": "string",
            "help": "Location branch road details.",
            "default": "",
            "max_length": 47,
        },
        "building": {
            "type": "string",
            "help": "Location building details.",
            "default": "",
            "max_length": 47,
        },
        "city": {
            "type": "string",
            "help": "Location city details.",
            "default": "",
            "max_length": 47,
        },
        "city-division": {
            "type": "string",
            "help": "Location city division details.",
            "default": "",
            "max_length": 47,
        },
        "country": {
            "type": "string",
            "help": "The two-letter ISO 3166 country code in capital ASCII letters eg. US, CA, DK, DE.",
            "required": True,
            "default": "",
            "max_length": 47,
        },
        "country-subdivision": {
            "type": "string",
            "help": "National subdivisions (state, canton, region, province, or prefecture).",
            "default": "",
            "max_length": 47,
        },
        "county": {
            "type": "string",
            "help": "County, parish, gun (JP), or district (IN).",
            "default": "",
            "max_length": 47,
        },
        "direction": {
            "type": "string",
            "help": "Leading street direction.",
            "default": "",
            "max_length": 47,
        },
        "floor": {
            "type": "string",
            "help": "Floor.",
            "default": "",
            "max_length": 47,
        },
        "landmark": {
            "type": "string",
            "help": "Landmark or vanity address.",
            "default": "",
            "max_length": 47,
        },
        "language": {
            "type": "string",
            "help": "Language.",
            "default": "",
            "max_length": 47,
        },
        "name": {
            "type": "string",
            "help": "Name (residence and office occupant).",
            "default": "",
            "max_length": 47,
        },
        "number": {
            "type": "string",
            "help": "House number.",
            "default": "",
            "max_length": 47,
        },
        "number-suffix": {
            "type": "string",
            "help": "House number suffix.",
            "default": "",
            "max_length": 47,
        },
        "place-type": {
            "type": "string",
            "help": "Place type.",
            "default": "",
            "max_length": 47,
        },
        "post-office-box": {
            "type": "string",
            "help": "Post office box.",
            "default": "",
            "max_length": 47,
        },
        "postal-community": {
            "type": "string",
            "help": "Postal community name.",
            "default": "",
            "max_length": 47,
        },
        "primary-road": {
            "type": "string",
            "help": "Primary road name.",
            "default": "",
            "max_length": 47,
        },
        "road-section": {
            "type": "string",
            "help": "Road section.",
            "default": "",
            "max_length": 47,
        },
        "room": {
            "type": "string",
            "help": "Room number.",
            "default": "",
            "max_length": 47,
        },
        "script": {
            "type": "string",
            "help": "Script used to present the address information.",
            "default": "",
            "max_length": 47,
        },
        "seat": {
            "type": "string",
            "help": "Seat number.",
            "default": "",
            "max_length": 47,
        },
        "street": {
            "type": "string",
            "help": "Street.",
            "default": "",
            "max_length": 47,
        },
        "street-name-post-mod": {
            "type": "string",
            "help": "Street name post modifier.",
            "default": "",
            "max_length": 47,
        },
        "street-name-pre-mod": {
            "type": "string",
            "help": "Street name pre modifier.",
            "default": "",
            "max_length": 47,
        },
        "street-suffix": {
            "type": "string",
            "help": "Street suffix.",
            "default": "",
            "max_length": 47,
        },
        "sub-branch-road": {
            "type": "string",
            "help": "Sub branch road name.",
            "default": "",
            "max_length": 47,
        },
        "trailing-str-suffix": {
            "type": "string",
            "help": "Trailing street suffix.",
            "default": "",
            "max_length": 47,
        },
        "unit": {
            "type": "string",
            "help": "Unit (apartment, suite).",
            "default": "",
            "max_length": 47,
        },
        "zip": {
            "type": "string",
            "help": "Postal/zip code.",
            "default": "",
            "max_length": 47,
        },
        "parent-key": {
            "type": "string",
            "help": "Parent key name.",
            "default": "",
            "max_length": 63,
        },
    },
    "coordinates": {
        "altitude": {
            "type": "string",
            "help": "Plus or minus floating point number. For example, 117.47.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "altitude-unit": {
            "type": "option",
            "help": "Configure the unit for which the altitude is to (m = meters, f = floors of a building).",
            "required": True,
            "default": "m",
            "options": ["m", "f"],
        },
        "datum": {
            "type": "option",
            "help": "WGS84, NAD83, NAD83/MLLW.",
            "required": True,
            "default": "WGS84",
            "options": ["WGS84", "NAD83", "NAD83/MLLW"],
        },
        "latitude": {
            "type": "string",
            "help": "Floating point starting with +/- or ending with (N or S). For example, +/-16.67 or 16.67N.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "longitude": {
            "type": "string",
            "help": "Floating point starting with +/- or ending with (N or S). For example, +/-26.789 or 26.789E.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "parent-key": {
            "type": "string",
            "help": "Parent key name.",
            "default": "",
            "max_length": 63,
        },
    },
    "elin-number": {
        "elin-num": {
            "type": "string",
            "help": "Configure ELIN callback number.",
            "default": "",
            "max_length": 31,
        },
        "parent-key": {
            "type": "string",
            "help": "Parent key name.",
            "default": "",
            "max_length": 63,
        },
    },
}


# Valid enum values from API documentation
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_location_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/location."""
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


def validate_switch_controller_location_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/location object."""
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


def validate_switch_controller_location_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/location."""
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
    "endpoint": "switch_controller/location",
    "category": "cmdb",
    "api_path": "switch-controller/location",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure FortiSwitch location services.",
    "total_fields": 4,
    "required_fields_count": 0,
    "fields_with_defaults_count": 1,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
