"""Validation helpers for extension_controller/dataplan - Auto-generated"""

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
    "slot",  # SIM slot configuration.
    "iccid",  # ICCID configuration.
    "carrier",  # Carrier configuration.
    "username",  # Username.
    "password",  # Password.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "modem-id": "all",
    "type": "generic",
    "slot": "",
    "iccid": "",
    "carrier": "",
    "apn": "",
    "auth-type": "none",
    "username": "",
    "pdn": "ipv4-only",
    "signal-threshold": 100,
    "signal-period": 3600,
    "capacity": 0,
    "monthly-fee": 0,
    "billing-date": 1,
    "overage": "disable",
    "preferred-subnet": 0,
    "private-network": "disable",
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
    "name": "string",  # FortiExtender data plan name.
    "modem-id": "option",  # Dataplan's modem specifics, if any.
    "type": "option",  # Type preferences configuration.
    "slot": "option",  # SIM slot configuration.
    "iccid": "string",  # ICCID configuration.
    "carrier": "string",  # Carrier configuration.
    "apn": "string",  # APN configuration.
    "auth-type": "option",  # Authentication type.
    "username": "string",  # Username.
    "password": "password",  # Password.
    "pdn": "option",  # PDN type.
    "signal-threshold": "integer",  # Signal threshold. Specify the range between 50 - 100, where 
    "signal-period": "integer",  # Signal period (600 to 18000 seconds).
    "capacity": "integer",  # Capacity in MB (0 - 102400000).
    "monthly-fee": "integer",  # Monthly fee of dataplan (0 - 100000, in local currency).
    "billing-date": "integer",  # Billing day of the month (1 - 31).
    "overage": "option",  # Enable/disable dataplan overage detection.
    "preferred-subnet": "integer",  # Preferred subnet mask (0 - 32).
    "private-network": "option",  # Enable/disable dataplan private network support.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "FortiExtender data plan name.",
    "modem-id": "Dataplan's modem specifics, if any.",
    "type": "Type preferences configuration.",
    "slot": "SIM slot configuration.",
    "iccid": "ICCID configuration.",
    "carrier": "Carrier configuration.",
    "apn": "APN configuration.",
    "auth-type": "Authentication type.",
    "username": "Username.",
    "password": "Password.",
    "pdn": "PDN type.",
    "signal-threshold": "Signal threshold. Specify the range between 50 - 100, where 50/100 means -50/-100 dBm.",
    "signal-period": "Signal period (600 to 18000 seconds).",
    "capacity": "Capacity in MB (0 - 102400000).",
    "monthly-fee": "Monthly fee of dataplan (0 - 100000, in local currency).",
    "billing-date": "Billing day of the month (1 - 31).",
    "overage": "Enable/disable dataplan overage detection.",
    "preferred-subnet": "Preferred subnet mask (0 - 32).",
    "private-network": "Enable/disable dataplan private network support.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 31},
    "iccid": {"type": "string", "max_length": 31},
    "carrier": {"type": "string", "max_length": 31},
    "apn": {"type": "string", "max_length": 63},
    "username": {"type": "string", "max_length": 127},
    "signal-threshold": {"type": "integer", "min": 50, "max": 100},
    "signal-period": {"type": "integer", "min": 600, "max": 18000},
    "capacity": {"type": "integer", "min": 0, "max": 102400000},
    "monthly-fee": {"type": "integer", "min": 0, "max": 1000000},
    "billing-date": {"type": "integer", "min": 1, "max": 31},
    "preferred-subnet": {"type": "integer", "min": 0, "max": 32},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_MODEM_ID = [
    "modem1",
    "modem2",
    "all",
]
VALID_BODY_TYPE = [
    "carrier",
    "slot",
    "iccid",
    "generic",
]
VALID_BODY_SLOT = [
    "sim1",
    "sim2",
]
VALID_BODY_AUTH_TYPE = [
    "none",
    "pap",
    "chap",
]
VALID_BODY_PDN = [
    "ipv4-only",
    "ipv6-only",
    "ipv4-ipv6",
]
VALID_BODY_OVERAGE = [
    "disable",
    "enable",
]
VALID_BODY_PRIVATE_NETWORK = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_extension_controller_dataplan_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for extension_controller/dataplan."""
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


def validate_extension_controller_dataplan_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new extension_controller/dataplan object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "modem-id" in payload:
        is_valid, error = _validate_enum_field(
            "modem-id",
            payload["modem-id"],
            VALID_BODY_MODEM_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "slot" in payload:
        is_valid, error = _validate_enum_field(
            "slot",
            payload["slot"],
            VALID_BODY_SLOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pdn" in payload:
        is_valid, error = _validate_enum_field(
            "pdn",
            payload["pdn"],
            VALID_BODY_PDN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overage" in payload:
        is_valid, error = _validate_enum_field(
            "overage",
            payload["overage"],
            VALID_BODY_OVERAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-network" in payload:
        is_valid, error = _validate_enum_field(
            "private-network",
            payload["private-network"],
            VALID_BODY_PRIVATE_NETWORK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_extension_controller_dataplan_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update extension_controller/dataplan."""
    # Validate enum values using central function
    if "modem-id" in payload:
        is_valid, error = _validate_enum_field(
            "modem-id",
            payload["modem-id"],
            VALID_BODY_MODEM_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "slot" in payload:
        is_valid, error = _validate_enum_field(
            "slot",
            payload["slot"],
            VALID_BODY_SLOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pdn" in payload:
        is_valid, error = _validate_enum_field(
            "pdn",
            payload["pdn"],
            VALID_BODY_PDN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overage" in payload:
        is_valid, error = _validate_enum_field(
            "overage",
            payload["overage"],
            VALID_BODY_OVERAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-network" in payload:
        is_valid, error = _validate_enum_field(
            "private-network",
            payload["private-network"],
            VALID_BODY_PRIVATE_NETWORK,
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
    "endpoint": "extension_controller/dataplan",
    "category": "cmdb",
    "api_path": "extension-controller/dataplan",
    "mkey": "name",
    "mkey_type": "string",
    "help": "FortiExtender dataplan configuration.",
    "total_fields": 19,
    "required_fields_count": 5,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
