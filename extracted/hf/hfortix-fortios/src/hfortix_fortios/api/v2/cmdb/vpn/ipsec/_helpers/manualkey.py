"""Validation helpers for vpn/ipsec/manualkey - Auto-generated"""

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
    "interface",  # Name of the physical, aggregate, or VLAN interface.
    "authkey",  # Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphens.
    "enckey",  # Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.
    "localspi",  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
    "remotespi",  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "interface": "",
    "remote-gw": "0.0.0.0",
    "local-gw": "0.0.0.0",
    "authentication": "null",
    "encryption": "null",
    "authkey": "",
    "enckey": "",
    "localspi": "",
    "remotespi": "",
    "npu-offload": "enable",
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
    "name": "string",  # IPsec tunnel name.
    "interface": "string",  # Name of the physical, aggregate, or VLAN interface.
    "remote-gw": "ipv4-address",  # Peer gateway.
    "local-gw": "ipv4-address-any",  # Local gateway.
    "authentication": "option",  # Authentication algorithm. Must be the same for both ends of the tunnel.
    "encryption": "option",  # Encryption algorithm. Must be the same for both ends of the tunnel.
    "authkey": "user",  # Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphen
    "enckey": "user",  # Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.
    "localspi": "user",  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic stre
    "remotespi": "user",  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic str
    "npu-offload": "option",  # Enable/disable NPU offloading.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "IPsec tunnel name.",
    "interface": "Name of the physical, aggregate, or VLAN interface.",
    "remote-gw": "Peer gateway.",
    "local-gw": "Local gateway.",
    "authentication": "Authentication algorithm. Must be the same for both ends of the tunnel.",
    "encryption": "Encryption algorithm. Must be the same for both ends of the tunnel.",
    "authkey": "Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphens.",
    "enckey": "Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.",
    "localspi": "Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.",
    "remotespi": "Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.",
    "npu-offload": "Enable/disable NPU offloading.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_AUTHENTICATION = [
    "null",
    "md5",
    "sha1",
    "sha256",
    "sha384",
    "sha512",
]
VALID_BODY_ENCRYPTION = [
    "null",
    "des",
    "3des",
    "aes128",
    "aes192",
    "aes256",
    "aria128",
    "aria192",
    "aria256",
    "seed",
]
VALID_BODY_NPU_OFFLOAD = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_ipsec_manualkey_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/ipsec/manualkey."""
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


def validate_vpn_ipsec_manualkey_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/ipsec/manualkey object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offload" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offload",
            payload["npu-offload"],
            VALID_BODY_NPU_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_ipsec_manualkey_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/ipsec/manualkey."""
    # Validate enum values using central function
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offload" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offload",
            payload["npu-offload"],
            VALID_BODY_NPU_OFFLOAD,
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
    "endpoint": "vpn/ipsec/manualkey",
    "category": "cmdb",
    "api_path": "vpn.ipsec/manualkey",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure IPsec manual keys.",
    "total_fields": 11,
    "required_fields_count": 5,
    "fields_with_defaults_count": 11,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
