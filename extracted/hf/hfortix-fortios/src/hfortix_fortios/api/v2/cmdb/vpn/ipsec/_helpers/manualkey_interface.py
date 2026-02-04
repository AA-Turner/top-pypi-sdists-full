"""Validation helpers for vpn/ipsec/manualkey_interface - Auto-generated"""

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
    "auth-key",  # Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphens.
    "enc-key",  # Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.
    "local-spi",  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
    "remote-spi",  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "interface": "",
    "ip-version": "4",
    "addr-type": "4",
    "remote-gw": "0.0.0.0",
    "remote-gw6": "::",
    "local-gw": "0.0.0.0",
    "local-gw6": "::",
    "auth-alg": "null",
    "enc-alg": "null",
    "auth-key": "",
    "enc-key": "",
    "local-spi": "",
    "remote-spi": "",
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
    "ip-version": "option",  # IP version to use for VPN interface.
    "addr-type": "option",  # IP version to use for IP packets.
    "remote-gw": "ipv4-address",  # IPv4 address of the remote gateway's external interface.
    "remote-gw6": "ipv6-address",  # Remote IPv6 address of VPN gateway.
    "local-gw": "ipv4-address-any",  # IPv4 address of the local gateway's external interface.
    "local-gw6": "ipv6-address",  # Local IPv6 address of VPN gateway.
    "auth-alg": "option",  # Authentication algorithm. Must be the same for both ends of the tunnel.
    "enc-alg": "option",  # Encryption algorithm. Must be the same for both ends of the tunnel.
    "auth-key": "user",  # Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphen
    "enc-key": "user",  # Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.
    "local-spi": "user",  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic stre
    "remote-spi": "user",  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic str
    "npu-offload": "option",  # Enable/disable offloading IPsec VPN manual key sessions to NPUs.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "IPsec tunnel name.",
    "interface": "Name of the physical, aggregate, or VLAN interface.",
    "ip-version": "IP version to use for VPN interface.",
    "addr-type": "IP version to use for IP packets.",
    "remote-gw": "IPv4 address of the remote gateway's external interface.",
    "remote-gw6": "Remote IPv6 address of VPN gateway.",
    "local-gw": "IPv4 address of the local gateway's external interface.",
    "local-gw6": "Local IPv6 address of VPN gateway.",
    "auth-alg": "Authentication algorithm. Must be the same for both ends of the tunnel.",
    "enc-alg": "Encryption algorithm. Must be the same for both ends of the tunnel.",
    "auth-key": "Hexadecimal authentication key in 16-digit (8-byte) segments separated by hyphens.",
    "enc-key": "Hexadecimal encryption key in 16-digit (8-byte) segments separated by hyphens.",
    "local-spi": "Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.",
    "remote-spi": "Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns between two traffic streams with different encryption rules.",
    "npu-offload": "Enable/disable offloading IPsec VPN manual key sessions to NPUs.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "interface": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_IP_VERSION = [
    "4",
    "6",
]
VALID_BODY_ADDR_TYPE = [
    "4",
    "6",
]
VALID_BODY_AUTH_ALG = [
    "null",
    "md5",
    "sha1",
    "sha256",
    "sha384",
    "sha512",
]
VALID_BODY_ENC_ALG = [
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


def validate_vpn_ipsec_manualkey_interface_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/ipsec/manualkey_interface."""
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


def validate_vpn_ipsec_manualkey_interface_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/ipsec/manualkey_interface object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ip-version" in payload:
        is_valid, error = _validate_enum_field(
            "ip-version",
            payload["ip-version"],
            VALID_BODY_IP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-alg" in payload:
        is_valid, error = _validate_enum_field(
            "auth-alg",
            payload["auth-alg"],
            VALID_BODY_AUTH_ALG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-alg" in payload:
        is_valid, error = _validate_enum_field(
            "enc-alg",
            payload["enc-alg"],
            VALID_BODY_ENC_ALG,
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


def validate_vpn_ipsec_manualkey_interface_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/ipsec/manualkey_interface."""
    # Validate enum values using central function
    if "ip-version" in payload:
        is_valid, error = _validate_enum_field(
            "ip-version",
            payload["ip-version"],
            VALID_BODY_IP_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "addr-type",
            payload["addr-type"],
            VALID_BODY_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-alg" in payload:
        is_valid, error = _validate_enum_field(
            "auth-alg",
            payload["auth-alg"],
            VALID_BODY_AUTH_ALG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-alg" in payload:
        is_valid, error = _validate_enum_field(
            "enc-alg",
            payload["enc-alg"],
            VALID_BODY_ENC_ALG,
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
    "endpoint": "vpn/ipsec/manualkey_interface",
    "category": "cmdb",
    "api_path": "vpn.ipsec/manualkey-interface",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure IPsec manual keys.",
    "total_fields": 15,
    "required_fields_count": 5,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
