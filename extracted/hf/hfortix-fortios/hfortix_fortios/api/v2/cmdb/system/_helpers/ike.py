"""Validation helpers for system/ike - Auto-generated"""

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
    "embryonic-limit": 10000,
    "dh-multiprocess": "enable",
    "dh-worker-count": 0,
    "dh-mode": "software",
    "dh-keypair-cache": "enable",
    "dh-keypair-count": 100,
    "dh-keypair-throttle": "enable",
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
    "embryonic-limit": "integer",  # Maximum number of IPsec tunnels to negotiate simultaneously.
    "dh-multiprocess": "option",  # Enable/disable multiprocess Diffie-Hellman daemon for IKE.
    "dh-worker-count": "integer",  # Number of Diffie-Hellman workers to start.
    "dh-mode": "option",  # Use software (CPU) or hardware (CPX) to perform Diffie-Hellm
    "dh-keypair-cache": "option",  # Enable/disable Diffie-Hellman key pair cache.
    "dh-keypair-count": "integer",  # Number of key pairs to pre-generate for each Diffie-Hellman 
    "dh-keypair-throttle": "option",  # Enable/disable Diffie-Hellman key pair cache CPU throttling.
    "dh-group-1": "string",  # Diffie-Hellman group 1 (MODP-768).
    "dh-group-2": "string",  # Diffie-Hellman group 2 (MODP-1024).
    "dh-group-5": "string",  # Diffie-Hellman group 5 (MODP-1536).
    "dh-group-14": "string",  # Diffie-Hellman group 14 (MODP-2048).
    "dh-group-15": "string",  # Diffie-Hellman group 15 (MODP-3072).
    "dh-group-16": "string",  # Diffie-Hellman group 16 (MODP-4096).
    "dh-group-17": "string",  # Diffie-Hellman group 17 (MODP-6144).
    "dh-group-18": "string",  # Diffie-Hellman group 18 (MODP-8192).
    "dh-group-19": "string",  # Diffie-Hellman group 19 (EC-P256).
    "dh-group-20": "string",  # Diffie-Hellman group 20 (EC-P384).
    "dh-group-21": "string",  # Diffie-Hellman group 21 (EC-P521).
    "dh-group-27": "string",  # Diffie-Hellman group 27 (EC-P224BP).
    "dh-group-28": "string",  # Diffie-Hellman group 28 (EC-P256BP).
    "dh-group-29": "string",  # Diffie-Hellman group 29 (EC-P384BP).
    "dh-group-30": "string",  # Diffie-Hellman group 30 (EC-P512BP).
    "dh-group-31": "string",  # Diffie-Hellman group 31 (EC-X25519).
    "dh-group-32": "string",  # Diffie-Hellman group 32 (EC-X448).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "embryonic-limit": "Maximum number of IPsec tunnels to negotiate simultaneously.",
    "dh-multiprocess": "Enable/disable multiprocess Diffie-Hellman daemon for IKE.",
    "dh-worker-count": "Number of Diffie-Hellman workers to start.",
    "dh-mode": "Use software (CPU) or hardware (CPX) to perform Diffie-Hellman calculations.",
    "dh-keypair-cache": "Enable/disable Diffie-Hellman key pair cache.",
    "dh-keypair-count": "Number of key pairs to pre-generate for each Diffie-Hellman group (per-worker).",
    "dh-keypair-throttle": "Enable/disable Diffie-Hellman key pair cache CPU throttling.",
    "dh-group-1": "Diffie-Hellman group 1 (MODP-768).",
    "dh-group-2": "Diffie-Hellman group 2 (MODP-1024).",
    "dh-group-5": "Diffie-Hellman group 5 (MODP-1536).",
    "dh-group-14": "Diffie-Hellman group 14 (MODP-2048).",
    "dh-group-15": "Diffie-Hellman group 15 (MODP-3072).",
    "dh-group-16": "Diffie-Hellman group 16 (MODP-4096).",
    "dh-group-17": "Diffie-Hellman group 17 (MODP-6144).",
    "dh-group-18": "Diffie-Hellman group 18 (MODP-8192).",
    "dh-group-19": "Diffie-Hellman group 19 (EC-P256).",
    "dh-group-20": "Diffie-Hellman group 20 (EC-P384).",
    "dh-group-21": "Diffie-Hellman group 21 (EC-P521).",
    "dh-group-27": "Diffie-Hellman group 27 (EC-P224BP).",
    "dh-group-28": "Diffie-Hellman group 28 (EC-P256BP).",
    "dh-group-29": "Diffie-Hellman group 29 (EC-P384BP).",
    "dh-group-30": "Diffie-Hellman group 30 (EC-P512BP).",
    "dh-group-31": "Diffie-Hellman group 31 (EC-X25519).",
    "dh-group-32": "Diffie-Hellman group 32 (EC-X448).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "embryonic-limit": {"type": "integer", "min": 50, "max": 20000},
    "dh-worker-count": {"type": "integer", "min": 1, "max": 2},
    "dh-keypair-count": {"type": "integer", "min": 0, "max": 50000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "dh-group-1": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-2": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-5": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-14": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-15": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-16": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-17": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-18": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-19": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-20": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-21": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-27": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-28": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-29": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-30": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-31": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
    "dh-group-32": {
        "mode": {
            "type": "option",
            "help": "Use software (CPU) or hardware (CPX) to perform calculations for this Diffie-Hellman group.",
            "default": "global",
            "options": ["software", "hardware", "global"],
        },
        "keypair-cache": {
            "type": "option",
            "help": "Configure custom key pair cache size for this Diffie-Hellman group.",
            "default": "global",
            "options": ["global", "custom"],
        },
        "keypair-count": {
            "type": "integer",
            "help": "Number of key pairs to pre-generate for this Diffie-Hellman group (per-worker).",
            "default": 0,
            "min_value": 0,
            "max_value": 50000,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_DH_MULTIPROCESS = [
    "enable",
    "disable",
]
VALID_BODY_DH_MODE = [
    "software",
    "hardware",
]
VALID_BODY_DH_KEYPAIR_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_DH_KEYPAIR_THROTTLE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ike_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ike."""
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


def validate_system_ike_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ike object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "dh-multiprocess" in payload:
        is_valid, error = _validate_enum_field(
            "dh-multiprocess",
            payload["dh-multiprocess"],
            VALID_BODY_DH_MULTIPROCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-mode" in payload:
        is_valid, error = _validate_enum_field(
            "dh-mode",
            payload["dh-mode"],
            VALID_BODY_DH_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-keypair-cache" in payload:
        is_valid, error = _validate_enum_field(
            "dh-keypair-cache",
            payload["dh-keypair-cache"],
            VALID_BODY_DH_KEYPAIR_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-keypair-throttle" in payload:
        is_valid, error = _validate_enum_field(
            "dh-keypair-throttle",
            payload["dh-keypair-throttle"],
            VALID_BODY_DH_KEYPAIR_THROTTLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ike_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ike."""
    # Validate enum values using central function
    if "dh-multiprocess" in payload:
        is_valid, error = _validate_enum_field(
            "dh-multiprocess",
            payload["dh-multiprocess"],
            VALID_BODY_DH_MULTIPROCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-mode" in payload:
        is_valid, error = _validate_enum_field(
            "dh-mode",
            payload["dh-mode"],
            VALID_BODY_DH_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-keypair-cache" in payload:
        is_valid, error = _validate_enum_field(
            "dh-keypair-cache",
            payload["dh-keypair-cache"],
            VALID_BODY_DH_KEYPAIR_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-keypair-throttle" in payload:
        is_valid, error = _validate_enum_field(
            "dh-keypair-throttle",
            payload["dh-keypair-throttle"],
            VALID_BODY_DH_KEYPAIR_THROTTLE,
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
    "endpoint": "system/ike",
    "category": "cmdb",
    "api_path": "system/ike",
    "help": "Configure IKE global attributes.",
    "total_fields": 24,
    "required_fields_count": 0,
    "fields_with_defaults_count": 7,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
