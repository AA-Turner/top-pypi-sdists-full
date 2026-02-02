"""Validation helpers for extension_controller/extender_profile - Auto-generated"""

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
    "login-password",  # Set the managed extender's administrator password.
    "cellular",  # FortiExtender cellular configuration.
    "lan-extension",  # FortiExtender LAN extension configuration.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "id": 32,
    "model": "FX201E",
    "extension": "wan-extension",
    "allowaccess": "",
    "login-password-change": "no",
    "enforce-bandwidth": "disable",
    "bandwidth-limit": 1024,
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
    "name": "string",  # FortiExtender profile name.
    "id": "integer",  # ID.
    "model": "option",  # Model.
    "extension": "option",  # Extension option.
    "allowaccess": "option",  # Control management access to the managed extender. Separate 
    "login-password-change": "option",  # Change or reset the administrator password of a managed exte
    "login-password": "password",  # Set the managed extender's administrator password.
    "enforce-bandwidth": "option",  # Enable/disable enforcement of bandwidth on LAN extension int
    "bandwidth-limit": "integer",  # FortiExtender LAN extension bandwidth limit (Mbps).
    "cellular": "string",  # FortiExtender cellular configuration.
    "wifi": "string",  # FortiExtender Wi-Fi configuration.
    "lan-extension": "string",  # FortiExtender LAN extension configuration.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "FortiExtender profile name.",
    "id": "ID.",
    "model": "Model.",
    "extension": "Extension option.",
    "allowaccess": "Control management access to the managed extender. Separate entries with a space.",
    "login-password-change": "Change or reset the administrator password of a managed extender (yes, default, or no, default = no).",
    "login-password": "Set the managed extender's administrator password.",
    "enforce-bandwidth": "Enable/disable enforcement of bandwidth on LAN extension interface.",
    "bandwidth-limit": "FortiExtender LAN extension bandwidth limit (Mbps).",
    "cellular": "FortiExtender cellular configuration.",
    "wifi": "FortiExtender Wi-Fi configuration.",
    "lan-extension": "FortiExtender LAN extension configuration.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 31},
    "id": {"type": "integer", "min": 0, "max": 102400000},
    "bandwidth-limit": {"type": "integer", "min": 1, "max": 16776000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "cellular": {
        "dataplan": {
            "type": "string",
            "help": "Dataplan names.",
        },
        "controller-report": {
            "type": "string",
            "help": "FortiExtender controller report configuration.",
        },
        "sms-notification": {
            "type": "string",
            "help": "FortiExtender cellular SMS notification configuration.",
        },
        "modem1": {
            "type": "string",
            "help": "Configuration options for modem 1.",
        },
        "modem2": {
            "type": "string",
            "help": "Configuration options for modem 2.",
        },
    },
    "wifi": {
        "country": {
            "type": "option",
            "help": "Country in which this FEX will operate (default = NA).",
            "default": "--",
            "options": ["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"],
        },
        "radio-1": {
            "type": "string",
            "help": "Radio-1 config for Wi-Fi 2.4GHz",
        },
        "radio-2": {
            "type": "string",
            "help": "Radio-2 config for Wi-Fi 5GHz",
        },
    },
    "lan-extension": {
        "link-loadbalance": {
            "type": "option",
            "help": "LAN extension link load balance strategy.",
            "required": True,
            "default": "activebackup",
            "options": ["activebackup", "loadbalance"],
        },
        "ipsec-tunnel": {
            "type": "string",
            "help": "IPsec tunnel name.",
            "default": "",
            "max_length": 15,
        },
        "backhaul-interface": {
            "type": "string",
            "help": "IPsec phase1 interface.",
            "default": "",
            "max_length": 15,
        },
        "backhaul-ip": {
            "type": "string",
            "help": "IPsec phase1 IPv4/FQDN. Used to specify the external IP/FQDN when the FortiGate unit is behind a NAT device.",
            "default": "",
            "max_length": 63,
        },
        "backhaul": {
            "type": "string",
            "help": "LAN extension backhaul tunnel configuration.",
        },
        "downlinks": {
            "type": "string",
            "help": "Config FortiExtender downlink interface for LAN extension.",
        },
        "traffic-split-services": {
            "type": "string",
            "help": "Config FortiExtender traffic split interface for LAN extension.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MODEL = [
    "FX201E",
    "FX211E",
    "FX200F",
    "FXA11F",
    "FXE11F",
    "FXA21F",
    "FXE21F",
    "FXA22F",
    "FXE22F",
    "FX212F",
    "FX311F",
    "FX312F",
    "FX511F",
    "FXR51G",
    "FXN51G",
    "FXW51G",
    "FVG21F",
    "FVA21F",
    "FVG22F",
    "FVA22F",
    "FX04DA",
    "FG",
    "BS10FW",
    "BS20GW",
    "BS20GN",
    "FVG51G",
    "FXE11G",
    "FX211G",
]
VALID_BODY_EXTENSION = [
    "wan-extension",
    "lan-extension",
]
VALID_BODY_ALLOWACCESS = [
    "ping",
    "telnet",
    "http",
    "https",
    "ssh",
    "snmp",
]
VALID_BODY_LOGIN_PASSWORD_CHANGE = [
    "yes",
    "default",
    "no",
]
VALID_BODY_ENFORCE_BANDWIDTH = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_extension_controller_extender_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for extension_controller/extender_profile."""
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


def validate_extension_controller_extender_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new extension_controller/extender_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "model" in payload:
        is_valid, error = _validate_enum_field(
            "model",
            payload["model"],
            VALID_BODY_MODEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension" in payload:
        is_valid, error = _validate_enum_field(
            "extension",
            payload["extension"],
            VALID_BODY_EXTENSION,
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
    if "login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-password-change",
            payload["login-password-change"],
            VALID_BODY_LOGIN_PASSWORD_CHANGE,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_extension_controller_extender_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update extension_controller/extender_profile."""
    # Validate enum values using central function
    if "model" in payload:
        is_valid, error = _validate_enum_field(
            "model",
            payload["model"],
            VALID_BODY_MODEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension" in payload:
        is_valid, error = _validate_enum_field(
            "extension",
            payload["extension"],
            VALID_BODY_EXTENSION,
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
    if "login-password-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-password-change",
            payload["login-password-change"],
            VALID_BODY_LOGIN_PASSWORD_CHANGE,
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
    "endpoint": "extension_controller/extender_profile",
    "category": "cmdb",
    "api_path": "extension-controller/extender-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "FortiExtender extender profile configuration.",
    "total_fields": 12,
    "required_fields_count": 3,
    "fields_with_defaults_count": 8,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
