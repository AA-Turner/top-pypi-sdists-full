"""Validation helpers for system/pppoe_interface - Auto-generated"""

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
    "device",  # Name for the physical interface.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "dial-on-demand": "disable",
    "ipv6": "disable",
    "device": "",
    "username": "",
    "pppoe-egress-cos": "cos0",
    "auth-type": "auto",
    "ipunnumbered": "0.0.0.0",
    "pppoe-unnumbered-negotiate": "enable",
    "idle-timeout": 0,
    "multilink": "disable",
    "mrru": 1500,
    "disc-retry-timeout": 1,
    "padt-retry-timeout": 1,
    "service-name": "",
    "ac-name": "",
    "lcp-echo-interval": 5,
    "lcp-max-echo-fails": 3,
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
    "name": "string",  # Name of the PPPoE interface.
    "dial-on-demand": "option",  # Enable/disable dial on demand to dial the PPPoE interface when packets are route
    "ipv6": "option",  # Enable/disable IPv6 Control Protocol (IPv6CP).
    "device": "string",  # Name for the physical interface.
    "username": "string",  # User name.
    "password": "password",  # Enter the password.
    "pppoe-egress-cos": "option",  # CoS in VLAN tag for outgoing PPPoE/PPP packets.
    "auth-type": "option",  # PPP authentication type to use.
    "ipunnumbered": "ipv4-address",  # PPPoE unnumbered IP.
    "pppoe-unnumbered-negotiate": "option",  # Enable/disable PPPoE unnumbered negotiation.
    "idle-timeout": "integer",  # PPPoE auto disconnect after idle timeout (0-4294967295 sec).
    "multilink": "option",  # Enable/disable PPP multilink support.
    "mrru": "integer",  # PPP MRRU (296 - 65535, default = 1500).
    "disc-retry-timeout": "integer",  # PPPoE discovery init timeout value in (0-4294967295 sec).
    "padt-retry-timeout": "integer",  # PPPoE terminate timeout value in (0-4294967295 sec).
    "service-name": "string",  # PPPoE service name.
    "ac-name": "string",  # PPPoE AC name.
    "lcp-echo-interval": "integer",  # Time in seconds between PPPoE Link Control Protocol (LCP) echo requests.
    "lcp-max-echo-fails": "integer",  # Maximum missed LCP echo messages before disconnect.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name of the PPPoE interface.",
    "dial-on-demand": "Enable/disable dial on demand to dial the PPPoE interface when packets are routed to the PPPoE interface.",
    "ipv6": "Enable/disable IPv6 Control Protocol (IPv6CP).",
    "device": "Name for the physical interface.",
    "username": "User name.",
    "password": "Enter the password.",
    "pppoe-egress-cos": "CoS in VLAN tag for outgoing PPPoE/PPP packets.",
    "auth-type": "PPP authentication type to use.",
    "ipunnumbered": "PPPoE unnumbered IP.",
    "pppoe-unnumbered-negotiate": "Enable/disable PPPoE unnumbered negotiation.",
    "idle-timeout": "PPPoE auto disconnect after idle timeout (0-4294967295 sec).",
    "multilink": "Enable/disable PPP multilink support.",
    "mrru": "PPP MRRU (296 - 65535, default = 1500).",
    "disc-retry-timeout": "PPPoE discovery init timeout value in (0-4294967295 sec).",
    "padt-retry-timeout": "PPPoE terminate timeout value in (0-4294967295 sec).",
    "service-name": "PPPoE service name.",
    "ac-name": "PPPoE AC name.",
    "lcp-echo-interval": "Time in seconds between PPPoE Link Control Protocol (LCP) echo requests.",
    "lcp-max-echo-fails": "Maximum missed LCP echo messages before disconnect.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "device": {"type": "string", "max_length": 15},
    "username": {"type": "string", "max_length": 64},
    "idle-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "mrru": {"type": "integer", "min": 296, "max": 65535},
    "disc-retry-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "padt-retry-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "service-name": {"type": "string", "max_length": 63},
    "ac-name": {"type": "string", "max_length": 63},
    "lcp-echo-interval": {"type": "integer", "min": 0, "max": 32767},
    "lcp-max-echo-fails": {"type": "integer", "min": 0, "max": 32767},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_DIAL_ON_DEMAND = [
    "enable",
    "disable",
]
VALID_BODY_IPV6 = [
    "enable",
    "disable",
]
VALID_BODY_PPPOE_EGRESS_COS = [
    "cos0",
    "cos1",
    "cos2",
    "cos3",
    "cos4",
    "cos5",
    "cos6",
    "cos7",
]
VALID_BODY_AUTH_TYPE = [
    "auto",
    "pap",
    "chap",
    "mschapv1",
    "mschapv2",
]
VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE = [
    "enable",
    "disable",
]
VALID_BODY_MULTILINK = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_pppoe_interface_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/pppoe_interface."""
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


def validate_system_pppoe_interface_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/pppoe_interface object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "dial-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "dial-on-demand",
            payload["dial-on-demand"],
            VALID_BODY_DIAL_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6",
            payload["ipv6"],
            VALID_BODY_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-egress-cos" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-egress-cos",
            payload["pppoe-egress-cos"],
            VALID_BODY_PPPOE_EGRESS_COS,
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
    if "pppoe-unnumbered-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-unnumbered-negotiate",
            payload["pppoe-unnumbered-negotiate"],
            VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multilink" in payload:
        is_valid, error = _validate_enum_field(
            "multilink",
            payload["multilink"],
            VALID_BODY_MULTILINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_pppoe_interface_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/pppoe_interface."""
    # Validate enum values using central function
    if "dial-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "dial-on-demand",
            payload["dial-on-demand"],
            VALID_BODY_DIAL_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6",
            payload["ipv6"],
            VALID_BODY_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-egress-cos" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-egress-cos",
            payload["pppoe-egress-cos"],
            VALID_BODY_PPPOE_EGRESS_COS,
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
    if "pppoe-unnumbered-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-unnumbered-negotiate",
            payload["pppoe-unnumbered-negotiate"],
            VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multilink" in payload:
        is_valid, error = _validate_enum_field(
            "multilink",
            payload["multilink"],
            VALID_BODY_MULTILINK,
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
    "endpoint": "system/pppoe_interface",
    "category": "cmdb",
    "api_path": "system/pppoe-interface",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure the PPPoE interfaces.",
    "total_fields": 19,
    "required_fields_count": 1,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
