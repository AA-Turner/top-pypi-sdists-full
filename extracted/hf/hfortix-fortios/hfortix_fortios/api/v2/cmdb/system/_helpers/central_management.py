"""Validation helpers for system/central_management - Auto-generated"""

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
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "mode": "normal",
    "type": "fortiguard",
    "fortigate-cloud-sso-default-profile": "",
    "schedule-config-restore": "enable",
    "schedule-script-restore": "enable",
    "allow-push-configuration": "enable",
    "allow-push-firmware": "enable",
    "allow-remote-firmware-upgrade": "enable",
    "allow-monitor": "enable",
    "serial-number": "",
    "fmg": "",
    "fmg-source-ip": "0.0.0.0",
    "fmg-source-ip6": "::",
    "local-cert": "",
    "ca-cert": "",
    "vdom": "root",
    "fmg-update-port": "8890",
    "fmg-update-http-header": "disable",
    "include-default-servers": "enable",
    "enc-algorithm": "high",
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
    "mode": "option",  # Central management mode.
    "type": "option",  # Central management type.
    "fortigate-cloud-sso-default-profile": "string",  # Override access profile. Permission is set to read-only with
    "schedule-config-restore": "option",  # Enable/disable allowing the central management server to res
    "schedule-script-restore": "option",  # Enable/disable allowing the central management server to res
    "allow-push-configuration": "option",  # Enable/disable allowing the central management server to pus
    "allow-push-firmware": "option",  # Enable/disable allowing the central management server to pus
    "allow-remote-firmware-upgrade": "option",  # Enable/disable remotely upgrading the firmware on this Forti
    "allow-monitor": "option",  # Enable/disable allowing the central management server to rem
    "serial-number": "user",  # Serial number.
    "fmg": "user",  # IP address or FQDN of the FortiManager.
    "fmg-source-ip": "ipv4-address",  # IPv4 source address that this FortiGate uses when communicat
    "fmg-source-ip6": "ipv6-address",  # IPv6 source address that this FortiGate uses when communicat
    "local-cert": "string",  # Certificate to be used by FGFM protocol.
    "ca-cert": "user",  # CA certificate to be used by FGFM protocol.
    "vdom": "string",  # Virtual domain (VDOM) name to use when communicating with Fo
    "server-list": "string",  # Additional severs that the FortiGate can use for updates (fo
    "fmg-update-port": "option",  # Port used to communicate with FortiManager that is acting as
    "fmg-update-http-header": "option",  # Enable/disable inclusion of HTTP header in update request.
    "include-default-servers": "option",  # Enable/disable inclusion of public FortiGuard servers in the
    "enc-algorithm": "option",  # Encryption strength for communications between the FortiGate
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "vrf-select": "integer",  # VRF ID used for connection to server.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "mode": "Central management mode.",
    "type": "Central management type.",
    "fortigate-cloud-sso-default-profile": "Override access profile. Permission is set to read-only without a FortiGate Cloud Central Management license.",
    "schedule-config-restore": "Enable/disable allowing the central management server to restore the configuration of this FortiGate.",
    "schedule-script-restore": "Enable/disable allowing the central management server to restore the scripts stored on this FortiGate.",
    "allow-push-configuration": "Enable/disable allowing the central management server to push configuration changes to this FortiGate.",
    "allow-push-firmware": "Enable/disable allowing the central management server to push firmware updates to this FortiGate.",
    "allow-remote-firmware-upgrade": "Enable/disable remotely upgrading the firmware on this FortiGate from the central management server.",
    "allow-monitor": "Enable/disable allowing the central management server to remotely monitor this FortiGate unit.",
    "serial-number": "Serial number.",
    "fmg": "IP address or FQDN of the FortiManager.",
    "fmg-source-ip": "IPv4 source address that this FortiGate uses when communicating with FortiManager.",
    "fmg-source-ip6": "IPv6 source address that this FortiGate uses when communicating with FortiManager.",
    "local-cert": "Certificate to be used by FGFM protocol.",
    "ca-cert": "CA certificate to be used by FGFM protocol.",
    "vdom": "Virtual domain (VDOM) name to use when communicating with FortiManager.",
    "server-list": "Additional severs that the FortiGate can use for updates (for AV, IPS, updates) and ratings (for web filter and antispam ratings) servers.",
    "fmg-update-port": "Port used to communicate with FortiManager that is acting as a FortiGuard update server.",
    "fmg-update-http-header": "Enable/disable inclusion of HTTP header in update request.",
    "include-default-servers": "Enable/disable inclusion of public FortiGuard servers in the override server list.",
    "enc-algorithm": "Encryption strength for communications between the FortiGate and central management.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "vrf-select": "VRF ID used for connection to server.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "fortigate-cloud-sso-default-profile": {"type": "string", "max_length": 35},
    "local-cert": {"type": "string", "max_length": 35},
    "vdom": {"type": "string", "max_length": 31},
    "interface": {"type": "string", "max_length": 15},
    "vrf-select": {"type": "integer", "min": 0, "max": 511},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-list": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "server-type": {
            "type": "option",
            "help": "FortiGuard service type.",
            "required": True,
            "default": "",
            "options": ["update", "rating", "vpatch-query", "iot-collect"],
        },
        "addr-type": {
            "type": "option",
            "help": "Indicate whether the FortiGate communicates with the override server using an IPv4 address, an IPv6 address or a FQDN.",
            "default": "ipv4",
            "options": ["ipv4", "ipv6", "fqdn"],
        },
        "server-address": {
            "type": "ipv4-address",
            "help": "IPv4 address of override server.",
            "required": True,
            "default": "0.0.0.0",
        },
        "server-address6": {
            "type": "ipv6-address",
            "help": "IPv6 address of override server.",
            "required": True,
            "default": "::",
        },
        "fqdn": {
            "type": "string",
            "help": "FQDN address of override server.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MODE = [
    "normal",
    "backup",
]
VALID_BODY_TYPE = [
    "fortimanager",
    "fortiguard",
    "none",
]
VALID_BODY_SCHEDULE_CONFIG_RESTORE = [
    "enable",
    "disable",
]
VALID_BODY_SCHEDULE_SCRIPT_RESTORE = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_PUSH_CONFIGURATION = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_PUSH_FIRMWARE = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_REMOTE_FIRMWARE_UPGRADE = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_MONITOR = [
    "enable",
    "disable",
]
VALID_BODY_FMG_UPDATE_PORT = [
    "8890",
    "443",
]
VALID_BODY_FMG_UPDATE_HTTP_HEADER = [
    "enable",
    "disable",
]
VALID_BODY_INCLUDE_DEFAULT_SERVERS = [
    "enable",
    "disable",
]
VALID_BODY_ENC_ALGORITHM = [
    "default",
    "high",
    "low",
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


def validate_system_central_management_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/central_management."""
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


def validate_system_central_management_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/central_management object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule-config-restore" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-config-restore",
            payload["schedule-config-restore"],
            VALID_BODY_SCHEDULE_CONFIG_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule-script-restore" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-script-restore",
            payload["schedule-script-restore"],
            VALID_BODY_SCHEDULE_SCRIPT_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-push-configuration" in payload:
        is_valid, error = _validate_enum_field(
            "allow-push-configuration",
            payload["allow-push-configuration"],
            VALID_BODY_ALLOW_PUSH_CONFIGURATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-push-firmware" in payload:
        is_valid, error = _validate_enum_field(
            "allow-push-firmware",
            payload["allow-push-firmware"],
            VALID_BODY_ALLOW_PUSH_FIRMWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-remote-firmware-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "allow-remote-firmware-upgrade",
            payload["allow-remote-firmware-upgrade"],
            VALID_BODY_ALLOW_REMOTE_FIRMWARE_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-monitor" in payload:
        is_valid, error = _validate_enum_field(
            "allow-monitor",
            payload["allow-monitor"],
            VALID_BODY_ALLOW_MONITOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fmg-update-port" in payload:
        is_valid, error = _validate_enum_field(
            "fmg-update-port",
            payload["fmg-update-port"],
            VALID_BODY_FMG_UPDATE_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fmg-update-http-header" in payload:
        is_valid, error = _validate_enum_field(
            "fmg-update-http-header",
            payload["fmg-update-http-header"],
            VALID_BODY_FMG_UPDATE_HTTP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-default-servers" in payload:
        is_valid, error = _validate_enum_field(
            "include-default-servers",
            payload["include-default-servers"],
            VALID_BODY_INCLUDE_DEFAULT_SERVERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
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


def validate_system_central_management_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/central_management."""
    # Validate enum values using central function
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule-config-restore" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-config-restore",
            payload["schedule-config-restore"],
            VALID_BODY_SCHEDULE_CONFIG_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule-script-restore" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-script-restore",
            payload["schedule-script-restore"],
            VALID_BODY_SCHEDULE_SCRIPT_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-push-configuration" in payload:
        is_valid, error = _validate_enum_field(
            "allow-push-configuration",
            payload["allow-push-configuration"],
            VALID_BODY_ALLOW_PUSH_CONFIGURATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-push-firmware" in payload:
        is_valid, error = _validate_enum_field(
            "allow-push-firmware",
            payload["allow-push-firmware"],
            VALID_BODY_ALLOW_PUSH_FIRMWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-remote-firmware-upgrade" in payload:
        is_valid, error = _validate_enum_field(
            "allow-remote-firmware-upgrade",
            payload["allow-remote-firmware-upgrade"],
            VALID_BODY_ALLOW_REMOTE_FIRMWARE_UPGRADE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-monitor" in payload:
        is_valid, error = _validate_enum_field(
            "allow-monitor",
            payload["allow-monitor"],
            VALID_BODY_ALLOW_MONITOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fmg-update-port" in payload:
        is_valid, error = _validate_enum_field(
            "fmg-update-port",
            payload["fmg-update-port"],
            VALID_BODY_FMG_UPDATE_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fmg-update-http-header" in payload:
        is_valid, error = _validate_enum_field(
            "fmg-update-http-header",
            payload["fmg-update-http-header"],
            VALID_BODY_FMG_UPDATE_HTTP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-default-servers" in payload:
        is_valid, error = _validate_enum_field(
            "include-default-servers",
            payload["include-default-servers"],
            VALID_BODY_INCLUDE_DEFAULT_SERVERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enc-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "enc-algorithm",
            payload["enc-algorithm"],
            VALID_BODY_ENC_ALGORITHM,
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
    "endpoint": "system/central_management",
    "category": "cmdb",
    "api_path": "system/central-management",
    "help": "Configure central management.",
    "total_fields": 24,
    "required_fields_count": 1,
    "fields_with_defaults_count": 23,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
