"""Validation helpers for switch_controller/security_policy/x802_1x - Auto-generated"""

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
    "user-group",  # Name of user-group to assign to this MAC Authentication Bypass (MAB) policy.
    "guest-vlan-id",  # Guest VLAN name.
    "auth-fail-vlan-id",  # VLAN ID on which authentication failed.
    "authserver-timeout-vlanid",  # Authentication server timeout VLAN name.
    "authserver-timeout-tagged-vlanid",  # Tagged VLAN name for which the timeout option is applied to (only one VLAN ID).
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "security-mode": "802.1X",
    "mac-auth-bypass": "disable",
    "auth-order": "mab-dot1x",
    "auth-priority": "legacy",
    "open-auth": "disable",
    "eap-passthru": "enable",
    "eap-auto-untagged-vlans": "enable",
    "guest-vlan": "disable",
    "guest-vlan-id": "",
    "guest-auth-delay": 30,
    "auth-fail-vlan": "disable",
    "auth-fail-vlan-id": "",
    "framevid-apply": "enable",
    "radius-timeout-overwrite": "disable",
    "policy-type": "802.1X",
    "authserver-timeout-period": 3,
    "authserver-timeout-vlan": "disable",
    "authserver-timeout-vlanid": "",
    "authserver-timeout-tagged": "disable",
    "authserver-timeout-tagged-vlanid": "",
    "dacl": "disable",
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
    "name": "string",  # Policy name.
    "security-mode": "option",  # Port or MAC based 802.1X security mode.
    "user-group": "string",  # Name of user-group to assign to this MAC Authentication Bypass (MAB) policy.
    "mac-auth-bypass": "option",  # Enable/disable MAB for this policy.
    "auth-order": "option",  # Configure authentication order.
    "auth-priority": "option",  # Configure authentication priority.
    "open-auth": "option",  # Enable/disable open authentication for this policy.
    "eap-passthru": "option",  # Enable/disable EAP pass-through mode, allowing protocols (such as LLDP) to pass 
    "eap-auto-untagged-vlans": "option",  # Enable/disable automatic inclusion of untagged VLANs.
    "guest-vlan": "option",  # Enable the guest VLAN feature to allow limited access to non-802.1X-compliant cl
    "guest-vlan-id": "string",  # Guest VLAN name.
    "guest-auth-delay": "integer",  # Guest authentication delay (1 - 900  sec, default = 30).
    "auth-fail-vlan": "option",  # Enable to allow limited access to clients that cannot authenticate.
    "auth-fail-vlan-id": "string",  # VLAN ID on which authentication failed.
    "framevid-apply": "option",  # Enable/disable the capability to apply the EAP/MAB frame VLAN to the port native
    "radius-timeout-overwrite": "option",  # Enable to override the global RADIUS session timeout.
    "policy-type": "option",  # Policy type.
    "authserver-timeout-period": "integer",  # Authentication server timeout period (3 - 15 sec, default = 3).
    "authserver-timeout-vlan": "option",  # Enable/disable the authentication server timeout VLAN to allow limited access wh
    "authserver-timeout-vlanid": "string",  # Authentication server timeout VLAN name.
    "authserver-timeout-tagged": "option",  # Configure timeout option for the tagged VLAN which allows limited access when th
    "authserver-timeout-tagged-vlanid": "string",  # Tagged VLAN name for which the timeout option is applied to (only one VLAN ID).
    "dacl": "option",  # Enable/disable dynamic access control list on this interface.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Policy name.",
    "security-mode": "Port or MAC based 802.1X security mode.",
    "user-group": "Name of user-group to assign to this MAC Authentication Bypass (MAB) policy.",
    "mac-auth-bypass": "Enable/disable MAB for this policy.",
    "auth-order": "Configure authentication order.",
    "auth-priority": "Configure authentication priority.",
    "open-auth": "Enable/disable open authentication for this policy.",
    "eap-passthru": "Enable/disable EAP pass-through mode, allowing protocols (such as LLDP) to pass through ports for more flexible authentication.",
    "eap-auto-untagged-vlans": "Enable/disable automatic inclusion of untagged VLANs.",
    "guest-vlan": "Enable the guest VLAN feature to allow limited access to non-802.1X-compliant clients.",
    "guest-vlan-id": "Guest VLAN name.",
    "guest-auth-delay": "Guest authentication delay (1 - 900  sec, default = 30).",
    "auth-fail-vlan": "Enable to allow limited access to clients that cannot authenticate.",
    "auth-fail-vlan-id": "VLAN ID on which authentication failed.",
    "framevid-apply": "Enable/disable the capability to apply the EAP/MAB frame VLAN to the port native VLAN.",
    "radius-timeout-overwrite": "Enable to override the global RADIUS session timeout.",
    "policy-type": "Policy type.",
    "authserver-timeout-period": "Authentication server timeout period (3 - 15 sec, default = 3).",
    "authserver-timeout-vlan": "Enable/disable the authentication server timeout VLAN to allow limited access when RADIUS is unavailable.",
    "authserver-timeout-vlanid": "Authentication server timeout VLAN name.",
    "authserver-timeout-tagged": "Configure timeout option for the tagged VLAN which allows limited access when the authentication server is unavailable.",
    "authserver-timeout-tagged-vlanid": "Tagged VLAN name for which the timeout option is applied to (only one VLAN ID).",
    "dacl": "Enable/disable dynamic access control list on this interface.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 31},
    "guest-vlan-id": {"type": "string", "max_length": 15},
    "guest-auth-delay": {"type": "integer", "min": 1, "max": 900},
    "auth-fail-vlan-id": {"type": "string", "max_length": 15},
    "authserver-timeout-period": {"type": "integer", "min": 3, "max": 15},
    "authserver-timeout-vlanid": {"type": "string", "max_length": 15},
    "authserver-timeout-tagged-vlanid": {"type": "string", "max_length": 15},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "user-group": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SECURITY_MODE = [
    "802.1X",
    "802.1X-mac-based",
]
VALID_BODY_MAC_AUTH_BYPASS = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_ORDER = [
    "dot1x-mab",
    "mab-dot1x",
    "mab",
]
VALID_BODY_AUTH_PRIORITY = [
    "legacy",
    "dot1x-mab",
    "mab-dot1x",
]
VALID_BODY_OPEN_AUTH = [
    "disable",
    "enable",
]
VALID_BODY_EAP_PASSTHRU = [
    "disable",
    "enable",
]
VALID_BODY_EAP_AUTO_UNTAGGED_VLANS = [
    "disable",
    "enable",
]
VALID_BODY_GUEST_VLAN = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_FAIL_VLAN = [
    "disable",
    "enable",
]
VALID_BODY_FRAMEVID_APPLY = [
    "disable",
    "enable",
]
VALID_BODY_RADIUS_TIMEOUT_OVERWRITE = [
    "disable",
    "enable",
]
VALID_BODY_POLICY_TYPE = [
    "802.1X",
]
VALID_BODY_AUTHSERVER_TIMEOUT_VLAN = [
    "disable",
    "enable",
]
VALID_BODY_AUTHSERVER_TIMEOUT_TAGGED = [
    "disable",
    "lldp-voice",
    "static",
]
VALID_BODY_DACL = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_security_policy_x802_1x_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/security_policy/x802_1x."""
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


def validate_switch_controller_security_policy_x802_1x_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/security_policy/x802_1x object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "mac-auth-bypass",
            payload["mac-auth-bypass"],
            VALID_BODY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-order" in payload:
        is_valid, error = _validate_enum_field(
            "auth-order",
            payload["auth-order"],
            VALID_BODY_AUTH_ORDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-priority" in payload:
        is_valid, error = _validate_enum_field(
            "auth-priority",
            payload["auth-priority"],
            VALID_BODY_AUTH_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "open-auth" in payload:
        is_valid, error = _validate_enum_field(
            "open-auth",
            payload["open-auth"],
            VALID_BODY_OPEN_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-passthru" in payload:
        is_valid, error = _validate_enum_field(
            "eap-passthru",
            payload["eap-passthru"],
            VALID_BODY_EAP_PASSTHRU,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-auto-untagged-vlans" in payload:
        is_valid, error = _validate_enum_field(
            "eap-auto-untagged-vlans",
            payload["eap-auto-untagged-vlans"],
            VALID_BODY_EAP_AUTO_UNTAGGED_VLANS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "guest-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "guest-vlan",
            payload["guest-vlan"],
            VALID_BODY_GUEST_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-fail-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "auth-fail-vlan",
            payload["auth-fail-vlan"],
            VALID_BODY_AUTH_FAIL_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "framevid-apply" in payload:
        is_valid, error = _validate_enum_field(
            "framevid-apply",
            payload["framevid-apply"],
            VALID_BODY_FRAMEVID_APPLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-timeout-overwrite" in payload:
        is_valid, error = _validate_enum_field(
            "radius-timeout-overwrite",
            payload["radius-timeout-overwrite"],
            VALID_BODY_RADIUS_TIMEOUT_OVERWRITE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-type" in payload:
        is_valid, error = _validate_enum_field(
            "policy-type",
            payload["policy-type"],
            VALID_BODY_POLICY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authserver-timeout-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "authserver-timeout-vlan",
            payload["authserver-timeout-vlan"],
            VALID_BODY_AUTHSERVER_TIMEOUT_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authserver-timeout-tagged" in payload:
        is_valid, error = _validate_enum_field(
            "authserver-timeout-tagged",
            payload["authserver-timeout-tagged"],
            VALID_BODY_AUTHSERVER_TIMEOUT_TAGGED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dacl" in payload:
        is_valid, error = _validate_enum_field(
            "dacl",
            payload["dacl"],
            VALID_BODY_DACL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_security_policy_x802_1x_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/security_policy/x802_1x."""
    # Validate enum values using central function
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "mac-auth-bypass",
            payload["mac-auth-bypass"],
            VALID_BODY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-order" in payload:
        is_valid, error = _validate_enum_field(
            "auth-order",
            payload["auth-order"],
            VALID_BODY_AUTH_ORDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-priority" in payload:
        is_valid, error = _validate_enum_field(
            "auth-priority",
            payload["auth-priority"],
            VALID_BODY_AUTH_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "open-auth" in payload:
        is_valid, error = _validate_enum_field(
            "open-auth",
            payload["open-auth"],
            VALID_BODY_OPEN_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-passthru" in payload:
        is_valid, error = _validate_enum_field(
            "eap-passthru",
            payload["eap-passthru"],
            VALID_BODY_EAP_PASSTHRU,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-auto-untagged-vlans" in payload:
        is_valid, error = _validate_enum_field(
            "eap-auto-untagged-vlans",
            payload["eap-auto-untagged-vlans"],
            VALID_BODY_EAP_AUTO_UNTAGGED_VLANS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "guest-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "guest-vlan",
            payload["guest-vlan"],
            VALID_BODY_GUEST_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-fail-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "auth-fail-vlan",
            payload["auth-fail-vlan"],
            VALID_BODY_AUTH_FAIL_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "framevid-apply" in payload:
        is_valid, error = _validate_enum_field(
            "framevid-apply",
            payload["framevid-apply"],
            VALID_BODY_FRAMEVID_APPLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-timeout-overwrite" in payload:
        is_valid, error = _validate_enum_field(
            "radius-timeout-overwrite",
            payload["radius-timeout-overwrite"],
            VALID_BODY_RADIUS_TIMEOUT_OVERWRITE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-type" in payload:
        is_valid, error = _validate_enum_field(
            "policy-type",
            payload["policy-type"],
            VALID_BODY_POLICY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authserver-timeout-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "authserver-timeout-vlan",
            payload["authserver-timeout-vlan"],
            VALID_BODY_AUTHSERVER_TIMEOUT_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authserver-timeout-tagged" in payload:
        is_valid, error = _validate_enum_field(
            "authserver-timeout-tagged",
            payload["authserver-timeout-tagged"],
            VALID_BODY_AUTHSERVER_TIMEOUT_TAGGED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dacl" in payload:
        is_valid, error = _validate_enum_field(
            "dacl",
            payload["dacl"],
            VALID_BODY_DACL,
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
    "endpoint": "switch_controller/security_policy/x802_1x",
    "category": "cmdb",
    "api_path": "switch-controller.security-policy/802-1X",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure 802.1x MAC Authentication Bypass (MAB) policies.",
    "total_fields": 23,
    "required_fields_count": 5,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
