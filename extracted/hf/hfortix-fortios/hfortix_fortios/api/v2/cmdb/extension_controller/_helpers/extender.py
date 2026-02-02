"""Validation helpers for extension_controller/extender - Auto-generated"""

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
    "name",  # FortiExtender entry name.
    "id",  # FortiExtender serial number.
    "extension-type",  # Extension type for this FortiExtender.
    "login-password",  # Set the managed extender's administrator password.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "id": "",
    "authorized": "discovered",
    "ext-name": "",
    "description": "",
    "vdom": 1,
    "device-id": 1026,
    "extension-type": "",
    "profile": "",
    "override-allowaccess": "disable",
    "allowaccess": "",
    "override-login-password-change": "disable",
    "login-password-change": "no",
    "override-enforce-bandwidth": "disable",
    "enforce-bandwidth": "disable",
    "bandwidth-limit": 1024,
    "firmware-provision-latest": "disable",
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
    "name": "string",  # FortiExtender entry name.
    "id": "string",  # FortiExtender serial number.
    "authorized": "option",  # FortiExtender Administration (enable or disable).
    "ext-name": "string",  # FortiExtender name.
    "description": "string",  # Description.
    "vdom": "integer",  # VDOM.
    "device-id": "integer",  # Device ID.
    "extension-type": "option",  # Extension type for this FortiExtender.
    "profile": "string",  # FortiExtender profile configuration.
    "override-allowaccess": "option",  # Enable to override the extender profile management access co
    "allowaccess": "option",  # Control management access to the managed extender. Separate 
    "override-login-password-change": "option",  # Enable to override the extender profile login-password (admi
    "login-password-change": "option",  # Change or reset the administrator password of a managed exte
    "login-password": "password",  # Set the managed extender's administrator password.
    "override-enforce-bandwidth": "option",  # Enable to override the extender profile enforce-bandwidth se
    "enforce-bandwidth": "option",  # Enable/disable enforcement of bandwidth on LAN extension int
    "bandwidth-limit": "integer",  # FortiExtender LAN extension bandwidth limit (Mbps).
    "wan-extension": "string",  # FortiExtender wan extension configuration.
    "firmware-provision-latest": "option",  # Enable/disable one-time automatic provisioning of the latest
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "FortiExtender entry name.",
    "id": "FortiExtender serial number.",
    "authorized": "FortiExtender Administration (enable or disable).",
    "ext-name": "FortiExtender name.",
    "description": "Description.",
    "vdom": "VDOM.",
    "device-id": "Device ID.",
    "extension-type": "Extension type for this FortiExtender.",
    "profile": "FortiExtender profile configuration.",
    "override-allowaccess": "Enable to override the extender profile management access configuration.",
    "allowaccess": "Control management access to the managed extender. Separate entries with a space.",
    "override-login-password-change": "Enable to override the extender profile login-password (administrator password) setting.",
    "login-password-change": "Change or reset the administrator password of a managed extender (yes, default, or no, default = no).",
    "login-password": "Set the managed extender's administrator password.",
    "override-enforce-bandwidth": "Enable to override the extender profile enforce-bandwidth setting.",
    "enforce-bandwidth": "Enable/disable enforcement of bandwidth on LAN extension interface.",
    "bandwidth-limit": "FortiExtender LAN extension bandwidth limit (Mbps).",
    "wan-extension": "FortiExtender wan extension configuration.",
    "firmware-provision-latest": "Enable/disable one-time automatic provisioning of the latest firmware version.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 19},
    "id": {"type": "string", "max_length": 19},
    "ext-name": {"type": "string", "max_length": 31},
    "description": {"type": "string", "max_length": 255},
    "vdom": {"type": "integer", "min": 0, "max": 4294967295},
    "device-id": {"type": "integer", "min": 0, "max": 4294967295},
    "profile": {"type": "string", "max_length": 31},
    "bandwidth-limit": {"type": "integer", "min": 1, "max": 16776000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "wan-extension": {
        "modem1-extension": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem2-extension": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem1-pdn1-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem1-pdn2-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem1-pdn3-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem1-pdn4-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem2-pdn1-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem2-pdn2-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem2-pdn3-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
        "modem2-pdn4-interface": {
            "type": "string",
            "help": "FortiExtender interface name.",
            "default": "",
            "max_length": 31,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_AUTHORIZED = [
    "discovered",
    "disable",
    "enable",
]
VALID_BODY_EXTENSION_TYPE = [
    "wan-extension",
    "lan-extension",
]
VALID_BODY_OVERRIDE_ALLOWACCESS = [
    "enable",
    "disable",
]
VALID_BODY_ALLOWACCESS = [
    "ping",
    "telnet",
    "http",
    "https",
    "ssh",
    "snmp",
]
VALID_BODY_OVERRIDE_LOGIN_PASSWORD_CHANGE = [
    "enable",
    "disable",
]
VALID_BODY_LOGIN_PASSWORD_CHANGE = [
    "yes",
    "default",
    "no",
]
VALID_BODY_OVERRIDE_ENFORCE_BANDWIDTH = [
    "enable",
    "disable",
]
VALID_BODY_ENFORCE_BANDWIDTH = [
    "enable",
    "disable",
]
VALID_BODY_FIRMWARE_PROVISION_LATEST = [
    "disable",
    "once",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_extension_controller_extender_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for extension_controller/extender."""
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


def validate_extension_controller_extender_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new extension_controller/extender object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "authorized" in payload:
        is_valid, error = _validate_enum_field(
            "authorized",
            payload["authorized"],
            VALID_BODY_AUTHORIZED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension-type" in payload:
        is_valid, error = _validate_enum_field(
            "extension-type",
            payload["extension-type"],
            VALID_BODY_EXTENSION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "override-allowaccess",
            payload["override-allowaccess"],
            VALID_BODY_OVERRIDE_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "override-login-password-change",
            payload["override-login-password-change"],
            VALID_BODY_OVERRIDE_LOGIN_PASSWORD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-password-change",
            payload["login-password-change"],
            VALID_BODY_LOGIN_PASSWORD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-enforce-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "override-enforce-bandwidth",
            payload["override-enforce-bandwidth"],
            VALID_BODY_OVERRIDE_ENFORCE_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-bandwidth",
            payload["enforce-bandwidth"],
            VALID_BODY_ENFORCE_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-latest" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-latest",
            payload["firmware-provision-latest"],
            VALID_BODY_FIRMWARE_PROVISION_LATEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_extension_controller_extender_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update extension_controller/extender."""
    # Validate enum values using central function
    if "authorized" in payload:
        is_valid, error = _validate_enum_field(
            "authorized",
            payload["authorized"],
            VALID_BODY_AUTHORIZED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension-type" in payload:
        is_valid, error = _validate_enum_field(
            "extension-type",
            payload["extension-type"],
            VALID_BODY_EXTENSION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "override-allowaccess",
            payload["override-allowaccess"],
            VALID_BODY_OVERRIDE_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "override-login-password-change",
            payload["override-login-password-change"],
            VALID_BODY_OVERRIDE_LOGIN_PASSWORD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-password-change",
            payload["login-password-change"],
            VALID_BODY_LOGIN_PASSWORD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-enforce-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "override-enforce-bandwidth",
            payload["override-enforce-bandwidth"],
            VALID_BODY_OVERRIDE_ENFORCE_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-bandwidth",
            payload["enforce-bandwidth"],
            VALID_BODY_ENFORCE_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-latest" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-latest",
            payload["firmware-provision-latest"],
            VALID_BODY_FIRMWARE_PROVISION_LATEST,
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
    "endpoint": "extension_controller/extender",
    "category": "cmdb",
    "api_path": "extension-controller/extender",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Extender controller configuration.",
    "total_fields": 19,
    "required_fields_count": 4,
    "fields_with_defaults_count": 17,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
