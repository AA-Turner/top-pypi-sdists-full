"""Validation helpers for system/mobile_tunnel - Auto-generated"""

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
    "roaming-interface",  # Select the associated interface name from available options.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "status": "enable",
    "roaming-interface": "",
    "home-agent": "0.0.0.0",
    "home-address": "0.0.0.0",
    "renew-interval": 60,
    "lifetime": 65535,
    "reg-interval": 5,
    "reg-retry": 3,
    "n-mhae-spi": 256,
    "n-mhae-key-type": "ascii",
    "hash-algorithm": "hmac-md5",
    "tunnel-mode": "gre",
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
    "name": "string",  # Tunnel name.
    "status": "option",  # Enable/disable this mobile tunnel.
    "roaming-interface": "string",  # Select the associated interface name from available options.
    "home-agent": "ipv4-address",  # IPv4 address of the NEMO HA (Format: xxx.xxx.xxx.xxx).
    "home-address": "ipv4-address",  # Home IP address (Format: xxx.xxx.xxx.xxx).
    "renew-interval": "integer",  # Time before lifetime expiration to send NMMO HA re-registrat
    "lifetime": "integer",  # NMMO HA registration request lifetime (180 - 65535 sec, defa
    "reg-interval": "integer",  # NMMO HA registration interval (5 - 300, default = 5).
    "reg-retry": "integer",  # Maximum number of NMMO HA registration retries (1 to 30, def
    "n-mhae-spi": "integer",  # NEMO authentication SPI (default: 256).
    "n-mhae-key-type": "option",  # NEMO authentication key type (ASCII or base64).
    "n-mhae-key": "password_aes256",  # NEMO authentication key.
    "hash-algorithm": "option",  # Hash Algorithm (Keyed MD5).
    "tunnel-mode": "option",  # NEMO tunnel mode (GRE tunnel).
    "network": "string",  # NEMO network configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Tunnel name.",
    "status": "Enable/disable this mobile tunnel.",
    "roaming-interface": "Select the associated interface name from available options.",
    "home-agent": "IPv4 address of the NEMO HA (Format: xxx.xxx.xxx.xxx).",
    "home-address": "Home IP address (Format: xxx.xxx.xxx.xxx).",
    "renew-interval": "Time before lifetime expiration to send NMMO HA re-registration (5 - 60, default = 60).",
    "lifetime": "NMMO HA registration request lifetime (180 - 65535 sec, default = 65535).",
    "reg-interval": "NMMO HA registration interval (5 - 300, default = 5).",
    "reg-retry": "Maximum number of NMMO HA registration retries (1 to 30, default = 3).",
    "n-mhae-spi": "NEMO authentication SPI (default: 256).",
    "n-mhae-key-type": "NEMO authentication key type (ASCII or base64).",
    "n-mhae-key": "NEMO authentication key.",
    "hash-algorithm": "Hash Algorithm (Keyed MD5).",
    "tunnel-mode": "NEMO tunnel mode (GRE tunnel).",
    "network": "NEMO network configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "roaming-interface": {"type": "string", "max_length": 15},
    "renew-interval": {"type": "integer", "min": 5, "max": 60},
    "lifetime": {"type": "integer", "min": 180, "max": 65535},
    "reg-interval": {"type": "integer", "min": 5, "max": 300},
    "reg-retry": {"type": "integer", "min": 1, "max": 30},
    "n-mhae-spi": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "network": {
        "id": {
            "type": "integer",
            "help": "Network entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "interface": {
            "type": "string",
            "help": "Select the associated interface name from available options.",
            "default": "",
            "max_length": 15,
        },
        "prefix": {
            "type": "ipv4-classnet",
            "help": "Class IP and Netmask with correction (Format:xxx.xxx.xxx.xxx xxx.xxx.xxx.xxx or xxx.xxx.xxx.xxx/x).",
            "default": "0.0.0.0 0.0.0.0",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_N_MHAE_KEY_TYPE = [
    "ascii",
    "base64",
]
VALID_BODY_HASH_ALGORITHM = [
    "hmac-md5",
]
VALID_BODY_TUNNEL_MODE = [
    "gre",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_mobile_tunnel_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/mobile_tunnel."""
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


def validate_system_mobile_tunnel_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/mobile_tunnel object."""
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
    if "n-mhae-key-type" in payload:
        is_valid, error = _validate_enum_field(
            "n-mhae-key-type",
            payload["n-mhae-key-type"],
            VALID_BODY_N_MHAE_KEY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hash-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "hash-algorithm",
            payload["hash-algorithm"],
            VALID_BODY_HASH_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_mobile_tunnel_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/mobile_tunnel."""
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
    if "n-mhae-key-type" in payload:
        is_valid, error = _validate_enum_field(
            "n-mhae-key-type",
            payload["n-mhae-key-type"],
            VALID_BODY_N_MHAE_KEY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hash-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "hash-algorithm",
            payload["hash-algorithm"],
            VALID_BODY_HASH_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tunnel-mode" in payload:
        is_valid, error = _validate_enum_field(
            "tunnel-mode",
            payload["tunnel-mode"],
            VALID_BODY_TUNNEL_MODE,
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
    "endpoint": "system/mobile_tunnel",
    "category": "cmdb",
    "api_path": "system/mobile-tunnel",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Mobile tunnels, an implementation of Network Mobility (NEMO) extensions for Mobile IPv4 RFC5177.",
    "total_fields": 15,
    "required_fields_count": 1,
    "fields_with_defaults_count": 13,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
