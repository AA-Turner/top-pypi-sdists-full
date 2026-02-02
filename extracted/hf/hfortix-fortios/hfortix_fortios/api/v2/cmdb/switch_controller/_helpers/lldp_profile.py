"""Validation helpers for switch_controller/lldp_profile - Auto-generated"""

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
    "med-tlvs": "",
    "802.1-tlvs": "",
    "802.3-tlvs": "",
    "auto-isl": "enable",
    "auto-isl-hello-timer": 3,
    "auto-isl-receive-timeout": 60,
    "auto-isl-port-group": 0,
    "auto-mclag-icl": "disable",
    "auto-isl-auth": "legacy",
    "auto-isl-auth-user": "",
    "auto-isl-auth-identity": "",
    "auto-isl-auth-reauth": 3600,
    "auto-isl-auth-encrypt": "none",
    "auto-isl-auth-macsec-profile": "",
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
    "name": "string",  # Profile name.
    "med-tlvs": "option",  # Transmitted LLDP-MED TLVs (type-length-value descriptions).
    "802.1-tlvs": "option",  # Transmitted IEEE 802.1 TLVs.
    "802.3-tlvs": "option",  # Transmitted IEEE 802.3 TLVs.
    "auto-isl": "option",  # Enable/disable auto inter-switch LAG.
    "auto-isl-hello-timer": "integer",  # Auto inter-switch LAG hello timer duration (1 - 30 sec, defa
    "auto-isl-receive-timeout": "integer",  # Auto inter-switch LAG timeout if no response is received (3 
    "auto-isl-port-group": "integer",  # Auto inter-switch LAG port group ID (0 - 9).
    "auto-mclag-icl": "option",  # Enable/disable MCLAG inter chassis link.
    "auto-isl-auth": "option",  # Auto inter-switch LAG authentication mode.
    "auto-isl-auth-user": "string",  # Auto inter-switch LAG authentication user certificate.
    "auto-isl-auth-identity": "string",  # Auto inter-switch LAG authentication identity.
    "auto-isl-auth-reauth": "integer",  # Auto inter-switch LAG authentication reauth period in second
    "auto-isl-auth-encrypt": "option",  # Auto inter-switch LAG encryption mode.
    "auto-isl-auth-macsec-profile": "string",  # Auto inter-switch LAG macsec profile for encryption.
    "med-network-policy": "string",  # Configuration method to edit Media Endpoint Discovery (MED) 
    "med-location-service": "string",  # Configuration method to edit Media Endpoint Discovery (MED) 
    "custom-tlvs": "string",  # Configuration method to edit custom TLV entries.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "med-tlvs": "Transmitted LLDP-MED TLVs (type-length-value descriptions).",
    "802.1-tlvs": "Transmitted IEEE 802.1 TLVs.",
    "802.3-tlvs": "Transmitted IEEE 802.3 TLVs.",
    "auto-isl": "Enable/disable auto inter-switch LAG.",
    "auto-isl-hello-timer": "Auto inter-switch LAG hello timer duration (1 - 30 sec, default = 3).",
    "auto-isl-receive-timeout": "Auto inter-switch LAG timeout if no response is received (3 - 90 sec, default = 9).",
    "auto-isl-port-group": "Auto inter-switch LAG port group ID (0 - 9).",
    "auto-mclag-icl": "Enable/disable MCLAG inter chassis link.",
    "auto-isl-auth": "Auto inter-switch LAG authentication mode.",
    "auto-isl-auth-user": "Auto inter-switch LAG authentication user certificate.",
    "auto-isl-auth-identity": "Auto inter-switch LAG authentication identity.",
    "auto-isl-auth-reauth": "Auto inter-switch LAG authentication reauth period in seconds(10 - 3600, default = 3600).",
    "auto-isl-auth-encrypt": "Auto inter-switch LAG encryption mode.",
    "auto-isl-auth-macsec-profile": "Auto inter-switch LAG macsec profile for encryption.",
    "med-network-policy": "Configuration method to edit Media Endpoint Discovery (MED) network policy type-length-value (TLV) categories.",
    "med-location-service": "Configuration method to edit Media Endpoint Discovery (MED) location service type-length-value (TLV) categories.",
    "custom-tlvs": "Configuration method to edit custom TLV entries.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 63},
    "auto-isl-hello-timer": {"type": "integer", "min": 1, "max": 30},
    "auto-isl-receive-timeout": {"type": "integer", "min": 0, "max": 90},
    "auto-isl-port-group": {"type": "integer", "min": 0, "max": 9},
    "auto-isl-auth-user": {"type": "string", "max_length": 63},
    "auto-isl-auth-identity": {"type": "string", "max_length": 63},
    "auto-isl-auth-reauth": {"type": "integer", "min": 180, "max": 3600},
    "auto-isl-auth-macsec-profile": {"type": "string", "max_length": 63},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "med-network-policy": {
        "name": {
            "type": "string",
            "help": "Policy type name.",
            "default": "",
            "max_length": 63,
        },
        "status": {
            "type": "option",
            "help": "Enable or disable this TLV.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "vlan-intf": {
            "type": "string",
            "help": "VLAN interface to advertise; if configured on port.",
            "default": "",
            "max_length": 15,
        },
        "assign-vlan": {
            "type": "option",
            "help": "Enable/disable VLAN assignment when this profile is applied on managed FortiSwitch port.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "priority": {
            "type": "integer",
            "help": "Advertised Layer 2 priority (0 - 7; from lowest to highest priority).",
            "default": 0,
            "min_value": 0,
            "max_value": 7,
        },
        "dscp": {
            "type": "integer",
            "help": "Advertised Differentiated Services Code Point (DSCP) value, a packet header value indicating the level of service requested for traffic, such as high priority or best effort delivery.",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
    },
    "med-location-service": {
        "name": {
            "type": "string",
            "help": "Location service type name.",
            "default": "",
            "max_length": 63,
        },
        "status": {
            "type": "option",
            "help": "Enable or disable this TLV.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "sys-location-id": {
            "type": "string",
            "help": "Location service ID.",
            "default": "",
            "max_length": 63,
        },
    },
    "custom-tlvs": {
        "name": {
            "type": "string",
            "help": "TLV name (not sent).",
            "default": "",
            "max_length": 63,
        },
        "oui": {
            "type": "user",
            "help": "Organizationally unique identifier (OUI), a 3-byte hexadecimal number, for this TLV.",
            "required": True,
            "default": "000000",
        },
        "subtype": {
            "type": "integer",
            "help": "Organizationally defined subtype (0 - 255).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "information-string": {
            "type": "user",
            "help": "Organizationally defined information string (0 - 507 hexadecimal bytes).",
            "default": "",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MED_TLVS = [
    "inventory-management",
    "network-policy",
    "power-management",
    "location-identification",
]
VALID_BODY_802_1_TLVS = [
    "port-vlan-id",
]
VALID_BODY_802_3_TLVS = [
    "max-frame-size",
    "power-negotiation",
]
VALID_BODY_AUTO_ISL = [
    "disable",
    "enable",
]
VALID_BODY_AUTO_MCLAG_ICL = [
    "disable",
    "enable",
]
VALID_BODY_AUTO_ISL_AUTH = [
    "legacy",
    "strict",
    "relax",
]
VALID_BODY_AUTO_ISL_AUTH_ENCRYPT = [
    "none",
    "mixed",
    "must",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_lldp_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/lldp_profile."""
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


def validate_switch_controller_lldp_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/lldp_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "med-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "med-tlvs",
            payload["med-tlvs"],
            VALID_BODY_MED_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "802.1-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "802.1-tlvs",
            payload["802.1-tlvs"],
            VALID_BODY_802_1_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "802.3-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "802.3-tlvs",
            payload["802.3-tlvs"],
            VALID_BODY_802_3_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl",
            payload["auto-isl"],
            VALID_BODY_AUTO_ISL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-mclag-icl" in payload:
        is_valid, error = _validate_enum_field(
            "auto-mclag-icl",
            payload["auto-mclag-icl"],
            VALID_BODY_AUTO_MCLAG_ICL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl-auth" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl-auth",
            payload["auto-isl-auth"],
            VALID_BODY_AUTO_ISL_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl-auth-encrypt" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl-auth-encrypt",
            payload["auto-isl-auth-encrypt"],
            VALID_BODY_AUTO_ISL_AUTH_ENCRYPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_lldp_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/lldp_profile."""
    # Validate enum values using central function
    if "med-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "med-tlvs",
            payload["med-tlvs"],
            VALID_BODY_MED_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "802.1-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "802.1-tlvs",
            payload["802.1-tlvs"],
            VALID_BODY_802_1_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "802.3-tlvs" in payload:
        is_valid, error = _validate_enum_field(
            "802.3-tlvs",
            payload["802.3-tlvs"],
            VALID_BODY_802_3_TLVS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl",
            payload["auto-isl"],
            VALID_BODY_AUTO_ISL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-mclag-icl" in payload:
        is_valid, error = _validate_enum_field(
            "auto-mclag-icl",
            payload["auto-mclag-icl"],
            VALID_BODY_AUTO_MCLAG_ICL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl-auth" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl-auth",
            payload["auto-isl-auth"],
            VALID_BODY_AUTO_ISL_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-isl-auth-encrypt" in payload:
        is_valid, error = _validate_enum_field(
            "auto-isl-auth-encrypt",
            payload["auto-isl-auth-encrypt"],
            VALID_BODY_AUTO_ISL_AUTH_ENCRYPT,
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
    "endpoint": "switch_controller/lldp_profile",
    "category": "cmdb",
    "api_path": "switch-controller/lldp-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure FortiSwitch LLDP profiles.",
    "total_fields": 18,
    "required_fields_count": 0,
    "fields_with_defaults_count": 15,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
