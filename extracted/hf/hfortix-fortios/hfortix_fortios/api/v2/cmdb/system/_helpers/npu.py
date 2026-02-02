"""Validation helpers for system/npu - Auto-generated"""

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
    "dedicated-management-cpu": "option",  # Enable to dedicate one CPU for GUI and CLI connections when 
    "dedicated-management-affinity": "string",  # Affinity setting for management daemons (hexadecimal value u
    "capwap-offload": "option",  # Enable/disable offloading managed FortiAP and FortiLink CAPW
    "ipsec-mtu-override": "option",  # Enable/disable NP6 IPsec MTU override.   
disable:Disable NP
    "ipsec-ordering": "option",  # Enable/disable IPsec ordering.   
disable:Disable IPsec orde
    "ipsec-enc-subengine-mask": "string",  # IPsec encryption subengine mask (0x1 - 0x0f, default 0x0f).
    "ipsec-dec-subengine-mask": "string",  # IPsec decryption subengine mask (0x1 - 0x0f, default 0x0f).
    "priority-protocol": "table",  # Configure NPU priority protocol.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "dedicated-management-cpu": "Enable to dedicate one CPU for GUI and CLI connections when NPs are busy.    enable:Enable dedication of CPU #0 for management tasks.    disable:Disable dedication of CPU #0 for management tasks.",
    "dedicated-management-affinity": "Affinity setting for management daemons (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "capwap-offload": "Enable/disable offloading managed FortiAP and FortiLink CAPWAP sessions.    enable:Enable CAPWAP offload.    disable:Disable CAPWAP offload.",
    "ipsec-mtu-override": "Enable/disable NP6 IPsec MTU override.    disable:Disable NP6 IPsec MTU override.    enable:Enable NP6 IPsec MTU override.",
    "ipsec-ordering": "Enable/disable IPsec ordering.    disable:Disable IPsec ordering.    enable:Enable IPsec ordering.",
    "ipsec-enc-subengine-mask": "IPsec encryption subengine mask (0x1 - 0x0f, default 0x0f).",
    "ipsec-dec-subengine-mask": "IPsec decryption subengine mask (0x1 - 0x0f, default 0x0f).",
    "priority-protocol": "Configure NPU priority protocol.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "priority-protocol": {
        "bgp": {
            "type": "option",
            "help": "Enable/disable NPU BGP priority protocol.    enable:Enable NPU BGP priority protocol.    disable:Disable NPU BGP priority protocol.",
            "options": ["enable", "disable"],
        },
        "slbc": {
            "type": "option",
            "help": "Enable/disable NPU SLBC priority protocol.    enable:Enable NPU SLBC priority protocol.    disable:Disable NPU SLBC priority protocol.",
            "options": ["enable", "disable"],
        },
        "bfd": {
            "type": "option",
            "help": "Enable/disable NPU BFD priority protocol.    enable:Enable NPU BFD priority protocol.    disable:Disable NPU BFD priority protocol.",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_DEDICATED_MANAGEMENT_CPU = [
    "enable",
    "disable",
]
VALID_BODY_CAPWAP_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_IPSEC_MTU_OVERRIDE = [
    "disable",
    "enable",
]
VALID_BODY_IPSEC_ORDERING = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_npu_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/npu."""
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


def validate_system_npu_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/npu object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "dedicated-management-cpu" in payload:
        is_valid, error = _validate_enum_field(
            "dedicated-management-cpu",
            payload["dedicated-management-cpu"],
            VALID_BODY_DEDICATED_MANAGEMENT_CPU,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capwap-offload" in payload:
        is_valid, error = _validate_enum_field(
            "capwap-offload",
            payload["capwap-offload"],
            VALID_BODY_CAPWAP_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-mtu-override" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-mtu-override",
            payload["ipsec-mtu-override"],
            VALID_BODY_IPSEC_MTU_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-ordering" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-ordering",
            payload["ipsec-ordering"],
            VALID_BODY_IPSEC_ORDERING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_npu_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/npu."""
    # Validate enum values using central function
    if "dedicated-management-cpu" in payload:
        is_valid, error = _validate_enum_field(
            "dedicated-management-cpu",
            payload["dedicated-management-cpu"],
            VALID_BODY_DEDICATED_MANAGEMENT_CPU,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capwap-offload" in payload:
        is_valid, error = _validate_enum_field(
            "capwap-offload",
            payload["capwap-offload"],
            VALID_BODY_CAPWAP_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-mtu-override" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-mtu-override",
            payload["ipsec-mtu-override"],
            VALID_BODY_IPSEC_MTU_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-ordering" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-ordering",
            payload["ipsec-ordering"],
            VALID_BODY_IPSEC_ORDERING,
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
    "endpoint": "system/npu",
    "category": "cmdb",
    "api_path": "system/npu",
    "help": "Configuration for system/npu",
    "total_fields": 8,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
