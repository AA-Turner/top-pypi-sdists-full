"""Validation helpers for user/fsso - Auto-generated"""

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
    "name",  # Name.
    "server",  # Domain name or IP address of the first FSSO collector agent.
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "type": "default",
    "server": "",
    "port": 8000,
    "server2": "",
    "port2": 8000,
    "server3": "",
    "port3": 8000,
    "server4": "",
    "port4": 8000,
    "server5": "",
    "port5": 8000,
    "logon-timeout": 5,
    "ldap-server": "",
    "group-poll-interval": 0,
    "ldap-poll": "disable",
    "ldap-poll-interval": 180,
    "ldap-poll-filter": "(objectCategory=group)",
    "user-info-server": "",
    "ssl": "disable",
    "sni": "",
    "ssl-server-host-ip-check": "disable",
    "ssl-trusted-cert": "",
    "source-ip": "0.0.0.0",
    "source-ip6": "::",
    "interface-select-method": "auto",
    "interface": "",
    "vrf-select": 0,
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
    "name": "string",  # Name.
    "type": "option",  # Server type.
    "server": "string",  # Domain name or IP address of the first FSSO collector agent.
    "port": "integer",  # Port of the first FSSO collector agent.
    "password": "password",  # Password of the first FSSO collector agent.
    "server2": "string",  # Domain name or IP address of the second FSSO collector agent.
    "port2": "integer",  # Port of the second FSSO collector agent.
    "password2": "password",  # Password of the second FSSO collector agent.
    "server3": "string",  # Domain name or IP address of the third FSSO collector agent.
    "port3": "integer",  # Port of the third FSSO collector agent.
    "password3": "password",  # Password of the third FSSO collector agent.
    "server4": "string",  # Domain name or IP address of the fourth FSSO collector agent.
    "port4": "integer",  # Port of the fourth FSSO collector agent.
    "password4": "password",  # Password of the fourth FSSO collector agent.
    "server5": "string",  # Domain name or IP address of the fifth FSSO collector agent.
    "port5": "integer",  # Port of the fifth FSSO collector agent.
    "password5": "password",  # Password of the fifth FSSO collector agent.
    "logon-timeout": "integer",  # Interval in minutes to keep logons after FSSO server down.
    "ldap-server": "string",  # LDAP server to get group information.
    "group-poll-interval": "integer",  # Interval in minutes within to fetch groups from FSSO server, or unset to disable
    "ldap-poll": "option",  # Enable/disable automatic fetching of groups from LDAP server.
    "ldap-poll-interval": "integer",  # Interval in minutes within to fetch groups from LDAP server.
    "ldap-poll-filter": "string",  # Filter used to fetch groups.
    "user-info-server": "string",  # LDAP server to get user information.
    "ssl": "option",  # Enable/disable use of SSL.
    "sni": "string",  # Server Name Indication.
    "ssl-server-host-ip-check": "option",  # Enable/disable server host/IP verification.
    "ssl-trusted-cert": "string",  # Trusted server certificate or CA certificate.
    "source-ip": "ipv4-address",  # Source IP for communications to FSSO agent.
    "source-ip6": "ipv6-address",  # IPv6 source for communications to FSSO agent.
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "type": "Server type.",
    "server": "Domain name or IP address of the first FSSO collector agent.",
    "port": "Port of the first FSSO collector agent.",
    "password": "Password of the first FSSO collector agent.",
    "server2": "Domain name or IP address of the second FSSO collector agent.",
    "port2": "Port of the second FSSO collector agent.",
    "password2": "Password of the second FSSO collector agent.",
    "server3": "Domain name or IP address of the third FSSO collector agent.",
    "port3": "Port of the third FSSO collector agent.",
    "password3": "Password of the third FSSO collector agent.",
    "server4": "Domain name or IP address of the fourth FSSO collector agent.",
    "port4": "Port of the fourth FSSO collector agent.",
    "password4": "Password of the fourth FSSO collector agent.",
    "server5": "Domain name or IP address of the fifth FSSO collector agent.",
    "port5": "Port of the fifth FSSO collector agent.",
    "password5": "Password of the fifth FSSO collector agent.",
    "logon-timeout": "Interval in minutes to keep logons after FSSO server down.",
    "ldap-server": "LDAP server to get group information.",
    "group-poll-interval": "Interval in minutes within to fetch groups from FSSO server, or unset to disable.",
    "ldap-poll": "Enable/disable automatic fetching of groups from LDAP server.",
    "ldap-poll-interval": "Interval in minutes within to fetch groups from LDAP server.",
    "ldap-poll-filter": "Filter used to fetch groups.",
    "user-info-server": "LDAP server to get user information.",
    "ssl": "Enable/disable use of SSL.",
    "sni": "Server Name Indication.",
    "ssl-server-host-ip-check": "Enable/disable server host/IP verification.",
    "ssl-trusted-cert": "Trusted server certificate or CA certificate.",
    "source-ip": "Source IP for communications to FSSO agent.",
    "source-ip6": "IPv6 source for communications to FSSO agent.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "server": {"type": "string", "max_length": 63},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "server2": {"type": "string", "max_length": 63},
    "port2": {"type": "integer", "min": 1, "max": 65535},
    "server3": {"type": "string", "max_length": 63},
    "port3": {"type": "integer", "min": 1, "max": 65535},
    "server4": {"type": "string", "max_length": 63},
    "port4": {"type": "integer", "min": 1, "max": 65535},
    "server5": {"type": "string", "max_length": 63},
    "port5": {"type": "integer", "min": 1, "max": 65535},
    "logon-timeout": {"type": "integer", "min": 1, "max": 2880},
    "ldap-server": {"type": "string", "max_length": 35},
    "group-poll-interval": {"type": "integer", "min": 1, "max": 2880},
    "ldap-poll-interval": {"type": "integer", "min": 1, "max": 2880},
    "ldap-poll-filter": {"type": "string", "max_length": 2047},
    "user-info-server": {"type": "string", "max_length": 35},
    "sni": {"type": "string", "max_length": 255},
    "ssl-trusted-cert": {"type": "string", "max_length": 79},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "default",
    "fortinac",
]
VALID_BODY_LDAP_POLL = [
    "enable",
    "disable",
]
VALID_BODY_SSL = [
    "enable",
    "disable",
]
VALID_BODY_SSL_SERVER_HOST_IP_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_fsso_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/fsso."""
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


def validate_user_fsso_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/fsso object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldap-poll" in payload:
        is_valid, error = _validate_enum_field(
            "ldap-poll",
            payload["ldap-poll"],
            VALID_BODY_LDAP_POLL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl" in payload:
        is_valid, error = _validate_enum_field(
            "ssl",
            payload["ssl"],
            VALID_BODY_SSL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-host-ip-check" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-host-ip-check",
            payload["ssl-server-host-ip-check"],
            VALID_BODY_SSL_SERVER_HOST_IP_CHECK,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_fsso_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/fsso."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldap-poll" in payload:
        is_valid, error = _validate_enum_field(
            "ldap-poll",
            payload["ldap-poll"],
            VALID_BODY_LDAP_POLL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl" in payload:
        is_valid, error = _validate_enum_field(
            "ssl",
            payload["ssl"],
            VALID_BODY_SSL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-host-ip-check" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-host-ip-check",
            payload["ssl-server-host-ip-check"],
            VALID_BODY_SSL_SERVER_HOST_IP_CHECK,
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
    "endpoint": "user/fsso",
    "category": "cmdb",
    "api_path": "user/fsso",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Fortinet Single Sign On (FSSO) agents.",
    "total_fields": 33,
    "required_fields_count": 3,
    "fields_with_defaults_count": 28,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
