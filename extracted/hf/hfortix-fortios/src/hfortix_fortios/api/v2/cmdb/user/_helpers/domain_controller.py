"""Validation helpers for user/domain_controller - Auto-generated"""

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
    "hostname",  # Hostname of the server to connect to.
    "username",  # User name to sign in with. Must have proper permissions for service.
    "password",  # Password for specified username.
    "interface",  # Specify outgoing interface to reach server.
    "adlds-dn",  # AD LDS distinguished name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "ad-mode": "none",
    "hostname": "",
    "username": "",
    "ip-address": "0.0.0.0",
    "ip6": "::",
    "port": 445,
    "source-ip-address": "0.0.0.0",
    "source-ip6": "::",
    "source-port": 0,
    "interface-select-method": "auto",
    "interface": "",
    "domain-name": "",
    "replication-port": 0,
    "change-detection": "disable",
    "change-detection-period": 60,
    "dns-srv-lookup": "disable",
    "adlds-dn": "",
    "adlds-ip-address": "0.0.0.0",
    "adlds-ip6": "::",
    "adlds-port": 389,
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
    "name": "string",  # Domain controller entry name.
    "ad-mode": "option",  # Set Active Directory mode.
    "hostname": "string",  # Hostname of the server to connect to.
    "username": "string",  # User name to sign in with. Must have proper permissions for service.
    "password": "password",  # Password for specified username.
    "ip-address": "ipv4-address",  # Domain controller IPv4 address.
    "ip6": "ipv6-address",  # Domain controller IPv6 address.
    "port": "integer",  # Port to be used for communication with the domain controller (default = 445).
    "source-ip-address": "ipv4-address",  # FortiGate IPv4 address to be used for communication with the domain controller.
    "source-ip6": "ipv6-address",  # FortiGate IPv6 address to be used for communication with the domain controller.
    "source-port": "integer",  # Source port to be used for communication with the domain controller.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "extra-server": "string",  # Extra servers.
    "domain-name": "string",  # Domain DNS name.
    "replication-port": "integer",  # Port to be used for communication with the domain controller for replication ser
    "ldap-server": "string",  # LDAP server name(s).
    "change-detection": "option",  # Enable/disable detection of a configuration change in the Active Directory serve
    "change-detection-period": "integer",  # Minutes to detect a configuration change in the Active Directory server (5 - 100
    "dns-srv-lookup": "option",  # Enable/disable DNS service lookup.
    "adlds-dn": "string",  # AD LDS distinguished name.
    "adlds-ip-address": "ipv4-address",  # AD LDS IPv4 address.
    "adlds-ip6": "ipv6-address",  # AD LDS IPv6 address.
    "adlds-port": "integer",  # Port number of AD LDS service (default = 389).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Domain controller entry name.",
    "ad-mode": "Set Active Directory mode.",
    "hostname": "Hostname of the server to connect to.",
    "username": "User name to sign in with. Must have proper permissions for service.",
    "password": "Password for specified username.",
    "ip-address": "Domain controller IPv4 address.",
    "ip6": "Domain controller IPv6 address.",
    "port": "Port to be used for communication with the domain controller (default = 445).",
    "source-ip-address": "FortiGate IPv4 address to be used for communication with the domain controller.",
    "source-ip6": "FortiGate IPv6 address to be used for communication with the domain controller.",
    "source-port": "Source port to be used for communication with the domain controller.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "extra-server": "Extra servers.",
    "domain-name": "Domain DNS name.",
    "replication-port": "Port to be used for communication with the domain controller for replication service. Port number 0 indicates automatic discovery.",
    "ldap-server": "LDAP server name(s).",
    "change-detection": "Enable/disable detection of a configuration change in the Active Directory server.",
    "change-detection-period": "Minutes to detect a configuration change in the Active Directory server (5 - 10080 minutes (7 days), default = 60).",
    "dns-srv-lookup": "Enable/disable DNS service lookup.",
    "adlds-dn": "AD LDS distinguished name.",
    "adlds-ip-address": "AD LDS IPv4 address.",
    "adlds-ip6": "AD LDS IPv6 address.",
    "adlds-port": "Port number of AD LDS service (default = 389).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "hostname": {"type": "string", "max_length": 255},
    "username": {"type": "string", "max_length": 64},
    "port": {"type": "integer", "min": 0, "max": 65535},
    "source-port": {"type": "integer", "min": 0, "max": 65535},
    "interface": {"type": "string", "max_length": 15},
    "domain-name": {"type": "string", "max_length": 255},
    "replication-port": {"type": "integer", "min": 0, "max": 65535},
    "change-detection-period": {"type": "integer", "min": 5, "max": 10080},
    "adlds-dn": {"type": "string", "max_length": 255},
    "adlds-port": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "extra-server": {
        "id": {
            "type": "integer",
            "help": "Server ID.",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 100,
        },
        "ip-address": {
            "type": "ipv4-address",
            "help": "Domain controller IP address.",
            "required": True,
            "default": "0.0.0.0",
        },
        "port": {
            "type": "integer",
            "help": "Port to be used for communication with the domain controller (default = 445).",
            "default": 445,
            "min_value": 0,
            "max_value": 65535,
        },
        "source-ip-address": {
            "type": "ipv4-address",
            "help": "FortiGate IPv4 address to be used for communication with the domain controller.",
            "required": True,
            "default": "0.0.0.0",
        },
        "source-port": {
            "type": "integer",
            "help": "Source port to be used for communication with the domain controller.",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
    },
    "ldap-server": {
        "name": {
            "type": "string",
            "help": "LDAP server name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_AD_MODE = [
    "none",
    "ds",
    "lds",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_CHANGE_DETECTION = [
    "enable",
    "disable",
]
VALID_BODY_DNS_SRV_LOOKUP = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_domain_controller_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/domain_controller."""
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


def validate_user_domain_controller_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/domain_controller object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "ad-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ad-mode",
            payload["ad-mode"],
            VALID_BODY_AD_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "change-detection" in payload:
        is_valid, error = _validate_enum_field(
            "change-detection",
            payload["change-detection"],
            VALID_BODY_CHANGE_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-srv-lookup" in payload:
        is_valid, error = _validate_enum_field(
            "dns-srv-lookup",
            payload["dns-srv-lookup"],
            VALID_BODY_DNS_SRV_LOOKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_domain_controller_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/domain_controller."""
    # Validate enum values using central function
    if "ad-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ad-mode",
            payload["ad-mode"],
            VALID_BODY_AD_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "change-detection" in payload:
        is_valid, error = _validate_enum_field(
            "change-detection",
            payload["change-detection"],
            VALID_BODY_CHANGE_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-srv-lookup" in payload:
        is_valid, error = _validate_enum_field(
            "dns-srv-lookup",
            payload["dns-srv-lookup"],
            VALID_BODY_DNS_SRV_LOOKUP,
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
    "endpoint": "user/domain_controller",
    "category": "cmdb",
    "api_path": "user/domain-controller",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure domain controller entries.",
    "total_fields": 24,
    "required_fields_count": 5,
    "fields_with_defaults_count": 21,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
