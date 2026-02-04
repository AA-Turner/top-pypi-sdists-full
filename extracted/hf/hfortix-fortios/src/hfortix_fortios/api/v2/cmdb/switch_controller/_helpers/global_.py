"""Validation helpers for switch_controller/global_ - Auto-generated"""

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
    "mac-aging-interval": 300,
    "https-image-push": "enable",
    "vlan-all-mode": "defined",
    "vlan-optimization": "configured",
    "vlan-identity": "name",
    "mac-retention-period": 24,
    "default-virtual-switch-vlan": "",
    "dhcp-server-access-list": "disable",
    "dhcp-option82-format": "ascii",
    "dhcp-option82-circuit-id": "intfname vlan mode",
    "dhcp-option82-remote-id": "mac",
    "dhcp-snoop-client-req": "drop-untrusted",
    "dhcp-snoop-client-db-exp": 86400,
    "dhcp-snoop-db-per-port-learn-limit": 64,
    "log-mac-limit-violations": "disable",
    "mac-violation-timer": 0,
    "sn-dns-resolution": "enable",
    "mac-event-logging": "disable",
    "bounce-quarantined-link": "disable",
    "quarantine-mode": "by-vlan",
    "update-user-device": "mac-cache lldp dhcp-snooping l2-db l3-db",
    "fips-enforce": "enable",
    "firmware-provision-on-authorization": "disable",
    "switch-on-deauth": "no-op",
    "firewall-auth-user-hold-period": 5,
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
    "mac-aging-interval": "integer",  # Time after which an inactive MAC is aged out (10 - 1000000 sec, default = 300, 0
    "https-image-push": "option",  # Enable/disable image push to FortiSwitch using HTTPS.
    "vlan-all-mode": "option",  # VLAN configuration mode, user-defined-vlans or all-possible-vlans.
    "vlan-optimization": "option",  # FortiLink VLAN optimization.
    "vlan-identity": "option",  # Identity of the VLAN. Commonly used for RADIUS Tunnel-Private-Group-Id.
    "disable-discovery": "string",  # Prevent this FortiSwitch from discovering.
    "mac-retention-period": "integer",  # Time in hours after which an inactive MAC is removed from client DB (0 = aged ou
    "default-virtual-switch-vlan": "string",  # Default VLAN for ports when added to the virtual-switch.
    "dhcp-server-access-list": "option",  # Enable/disable DHCP snooping server access list.
    "dhcp-option82-format": "option",  # DHCP option-82 format string.
    "dhcp-option82-circuit-id": "option",  # List the parameters to be included to inform about client identification.
    "dhcp-option82-remote-id": "option",  # List the parameters to be included to inform about client identification.
    "dhcp-snoop-client-req": "option",  # Client DHCP packet broadcast mode.
    "dhcp-snoop-client-db-exp": "integer",  # Expiry time for DHCP snooping server database entries (300 - 259200 sec, default
    "dhcp-snoop-db-per-port-learn-limit": "integer",  # Per Interface dhcp-server entries learn limit (0 - 1024, default = 64).
    "log-mac-limit-violations": "option",  # Enable/disable logs for Learning Limit Violations.
    "mac-violation-timer": "integer",  # Set timeout for Learning Limit Violations (0 = disabled).
    "sn-dns-resolution": "option",  # Enable/disable DNS resolution of the FortiSwitch unit's IP address with switch n
    "mac-event-logging": "option",  # Enable/disable MAC address event logging.
    "bounce-quarantined-link": "option",  # Enable/disable bouncing (administratively bring the link down, up) of a switch p
    "quarantine-mode": "option",  # Quarantine mode.
    "update-user-device": "option",  # Control which sources update the device user list.
    "custom-command": "string",  # List of custom commands to be pushed to all FortiSwitches in the VDOM.
    "fips-enforce": "option",  # Enable/disable enforcement of FIPS on managed FortiSwitch devices.
    "firmware-provision-on-authorization": "option",  # Enable/disable automatic provisioning of latest firmware on authorization.
    "switch-on-deauth": "option",  # No-operation/Factory-reset the managed FortiSwitch on deauthorization.
    "firewall-auth-user-hold-period": "integer",  # Time period in minutes to hold firewall authenticated MAC users (5 - 1440, defau
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "mac-aging-interval": "Time after which an inactive MAC is aged out (10 - 1000000 sec, default = 300, 0 = disable).",
    "https-image-push": "Enable/disable image push to FortiSwitch using HTTPS.",
    "vlan-all-mode": "VLAN configuration mode, user-defined-vlans or all-possible-vlans.",
    "vlan-optimization": "FortiLink VLAN optimization.",
    "vlan-identity": "Identity of the VLAN. Commonly used for RADIUS Tunnel-Private-Group-Id.",
    "disable-discovery": "Prevent this FortiSwitch from discovering.",
    "mac-retention-period": "Time in hours after which an inactive MAC is removed from client DB (0 = aged out based on mac-aging-interval).",
    "default-virtual-switch-vlan": "Default VLAN for ports when added to the virtual-switch.",
    "dhcp-server-access-list": "Enable/disable DHCP snooping server access list.",
    "dhcp-option82-format": "DHCP option-82 format string.",
    "dhcp-option82-circuit-id": "List the parameters to be included to inform about client identification.",
    "dhcp-option82-remote-id": "List the parameters to be included to inform about client identification.",
    "dhcp-snoop-client-req": "Client DHCP packet broadcast mode.",
    "dhcp-snoop-client-db-exp": "Expiry time for DHCP snooping server database entries (300 - 259200 sec, default = 86400 sec).",
    "dhcp-snoop-db-per-port-learn-limit": "Per Interface dhcp-server entries learn limit (0 - 1024, default = 64).",
    "log-mac-limit-violations": "Enable/disable logs for Learning Limit Violations.",
    "mac-violation-timer": "Set timeout for Learning Limit Violations (0 = disabled).",
    "sn-dns-resolution": "Enable/disable DNS resolution of the FortiSwitch unit's IP address with switch name.",
    "mac-event-logging": "Enable/disable MAC address event logging.",
    "bounce-quarantined-link": "Enable/disable bouncing (administratively bring the link down, up) of a switch port where a quarantined device was seen last. Helps to re-initiate the DHCP process for a device.",
    "quarantine-mode": "Quarantine mode.",
    "update-user-device": "Control which sources update the device user list.",
    "custom-command": "List of custom commands to be pushed to all FortiSwitches in the VDOM.",
    "fips-enforce": "Enable/disable enforcement of FIPS on managed FortiSwitch devices.",
    "firmware-provision-on-authorization": "Enable/disable automatic provisioning of latest firmware on authorization.",
    "switch-on-deauth": "No-operation/Factory-reset the managed FortiSwitch on deauthorization.",
    "firewall-auth-user-hold-period": "Time period in minutes to hold firewall authenticated MAC users (5 - 1440, default = 5, disable = 0).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "mac-aging-interval": {"type": "integer", "min": 10, "max": 1000000},
    "mac-retention-period": {"type": "integer", "min": 0, "max": 168},
    "default-virtual-switch-vlan": {"type": "string", "max_length": 15},
    "dhcp-snoop-client-db-exp": {"type": "integer", "min": 300, "max": 259200},
    "dhcp-snoop-db-per-port-learn-limit": {"type": "integer", "min": 0, "max": 2048},
    "mac-violation-timer": {"type": "integer", "min": 0, "max": 4294967295},
    "firewall-auth-user-hold-period": {"type": "integer", "min": 5, "max": 1440},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "disable-discovery": {
        "name": {
            "type": "string",
            "help": "FortiSwitch Serial-number.",
            "default": "",
            "max_length": 79,
        },
    },
    "custom-command": {
        "command-entry": {
            "type": "string",
            "help": "List of FortiSwitch commands.",
            "default": "",
            "max_length": 35,
        },
        "command-name": {
            "type": "string",
            "help": "Name of custom command to push to all FortiSwitches in VDOM.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_HTTPS_IMAGE_PUSH = [
    "enable",
    "disable",
]
VALID_BODY_VLAN_ALL_MODE = [
    "all",
    "defined",
]
VALID_BODY_VLAN_OPTIMIZATION = [
    "prune",
    "configured",
    "none",
]
VALID_BODY_VLAN_IDENTITY = [
    "description",
    "name",
]
VALID_BODY_DHCP_SERVER_ACCESS_LIST = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_OPTION82_FORMAT = [
    "ascii",
    "legacy",
]
VALID_BODY_DHCP_OPTION82_CIRCUIT_ID = [
    "intfname",
    "vlan",
    "hostname",
    "mode",
    "description",
]
VALID_BODY_DHCP_OPTION82_REMOTE_ID = [
    "mac",
    "hostname",
    "ip",
]
VALID_BODY_DHCP_SNOOP_CLIENT_REQ = [
    "drop-untrusted",
    "forward-untrusted",
]
VALID_BODY_LOG_MAC_LIMIT_VIOLATIONS = [
    "enable",
    "disable",
]
VALID_BODY_SN_DNS_RESOLUTION = [
    "enable",
    "disable",
]
VALID_BODY_MAC_EVENT_LOGGING = [
    "enable",
    "disable",
]
VALID_BODY_BOUNCE_QUARANTINED_LINK = [
    "disable",
    "enable",
]
VALID_BODY_QUARANTINE_MODE = [
    "by-vlan",
    "by-redirect",
]
VALID_BODY_UPDATE_USER_DEVICE = [
    "mac-cache",
    "lldp",
    "dhcp-snooping",
    "l2-db",
    "l3-db",
]
VALID_BODY_FIPS_ENFORCE = [
    "disable",
    "enable",
]
VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_ON_DEAUTH = [
    "no-op",
    "factory-reset",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_global_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/global_."""
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


def validate_switch_controller_global_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/global_ object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "https-image-push" in payload:
        is_valid, error = _validate_enum_field(
            "https-image-push",
            payload["https-image-push"],
            VALID_BODY_HTTPS_IMAGE_PUSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-all-mode" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-all-mode",
            payload["vlan-all-mode"],
            VALID_BODY_VLAN_ALL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-optimization" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-optimization",
            payload["vlan-optimization"],
            VALID_BODY_VLAN_OPTIMIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-identity" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-identity",
            payload["vlan-identity"],
            VALID_BODY_VLAN_IDENTITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server-access-list" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server-access-list",
            payload["dhcp-server-access-list"],
            VALID_BODY_DHCP_SERVER_ACCESS_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-format" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-format",
            payload["dhcp-option82-format"],
            VALID_BODY_DHCP_OPTION82_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-circuit-id" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-circuit-id",
            payload["dhcp-option82-circuit-id"],
            VALID_BODY_DHCP_OPTION82_CIRCUIT_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-remote-id" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-remote-id",
            payload["dhcp-option82-remote-id"],
            VALID_BODY_DHCP_OPTION82_REMOTE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-snoop-client-req" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-snoop-client-req",
            payload["dhcp-snoop-client-req"],
            VALID_BODY_DHCP_SNOOP_CLIENT_REQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-mac-limit-violations" in payload:
        is_valid, error = _validate_enum_field(
            "log-mac-limit-violations",
            payload["log-mac-limit-violations"],
            VALID_BODY_LOG_MAC_LIMIT_VIOLATIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sn-dns-resolution" in payload:
        is_valid, error = _validate_enum_field(
            "sn-dns-resolution",
            payload["sn-dns-resolution"],
            VALID_BODY_SN_DNS_RESOLUTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-event-logging" in payload:
        is_valid, error = _validate_enum_field(
            "mac-event-logging",
            payload["mac-event-logging"],
            VALID_BODY_MAC_EVENT_LOGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-quarantined-link" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-quarantined-link",
            payload["bounce-quarantined-link"],
            VALID_BODY_BOUNCE_QUARANTINED_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quarantine-mode" in payload:
        is_valid, error = _validate_enum_field(
            "quarantine-mode",
            payload["quarantine-mode"],
            VALID_BODY_QUARANTINE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-user-device" in payload:
        is_valid, error = _validate_enum_field(
            "update-user-device",
            payload["update-user-device"],
            VALID_BODY_UPDATE_USER_DEVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fips-enforce" in payload:
        is_valid, error = _validate_enum_field(
            "fips-enforce",
            payload["fips-enforce"],
            VALID_BODY_FIPS_ENFORCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-on-authorization",
            payload["firmware-provision-on-authorization"],
            VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-on-deauth" in payload:
        is_valid, error = _validate_enum_field(
            "switch-on-deauth",
            payload["switch-on-deauth"],
            VALID_BODY_SWITCH_ON_DEAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_global_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/global_."""
    # Validate enum values using central function
    if "https-image-push" in payload:
        is_valid, error = _validate_enum_field(
            "https-image-push",
            payload["https-image-push"],
            VALID_BODY_HTTPS_IMAGE_PUSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-all-mode" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-all-mode",
            payload["vlan-all-mode"],
            VALID_BODY_VLAN_ALL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-optimization" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-optimization",
            payload["vlan-optimization"],
            VALID_BODY_VLAN_OPTIMIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-identity" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-identity",
            payload["vlan-identity"],
            VALID_BODY_VLAN_IDENTITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server-access-list" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server-access-list",
            payload["dhcp-server-access-list"],
            VALID_BODY_DHCP_SERVER_ACCESS_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-format" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-format",
            payload["dhcp-option82-format"],
            VALID_BODY_DHCP_OPTION82_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-circuit-id" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-circuit-id",
            payload["dhcp-option82-circuit-id"],
            VALID_BODY_DHCP_OPTION82_CIRCUIT_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-remote-id" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-remote-id",
            payload["dhcp-option82-remote-id"],
            VALID_BODY_DHCP_OPTION82_REMOTE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-snoop-client-req" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-snoop-client-req",
            payload["dhcp-snoop-client-req"],
            VALID_BODY_DHCP_SNOOP_CLIENT_REQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-mac-limit-violations" in payload:
        is_valid, error = _validate_enum_field(
            "log-mac-limit-violations",
            payload["log-mac-limit-violations"],
            VALID_BODY_LOG_MAC_LIMIT_VIOLATIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sn-dns-resolution" in payload:
        is_valid, error = _validate_enum_field(
            "sn-dns-resolution",
            payload["sn-dns-resolution"],
            VALID_BODY_SN_DNS_RESOLUTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-event-logging" in payload:
        is_valid, error = _validate_enum_field(
            "mac-event-logging",
            payload["mac-event-logging"],
            VALID_BODY_MAC_EVENT_LOGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-quarantined-link" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-quarantined-link",
            payload["bounce-quarantined-link"],
            VALID_BODY_BOUNCE_QUARANTINED_LINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quarantine-mode" in payload:
        is_valid, error = _validate_enum_field(
            "quarantine-mode",
            payload["quarantine-mode"],
            VALID_BODY_QUARANTINE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "update-user-device" in payload:
        is_valid, error = _validate_enum_field(
            "update-user-device",
            payload["update-user-device"],
            VALID_BODY_UPDATE_USER_DEVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fips-enforce" in payload:
        is_valid, error = _validate_enum_field(
            "fips-enforce",
            payload["fips-enforce"],
            VALID_BODY_FIPS_ENFORCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-on-authorization",
            payload["firmware-provision-on-authorization"],
            VALID_BODY_FIRMWARE_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-on-deauth" in payload:
        is_valid, error = _validate_enum_field(
            "switch-on-deauth",
            payload["switch-on-deauth"],
            VALID_BODY_SWITCH_ON_DEAUTH,
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
    "endpoint": "switch_controller/global_",
    "category": "cmdb",
    "api_path": "switch-controller/global",
    "help": "Configure FortiSwitch global settings.",
    "total_fields": 27,
    "required_fields_count": 0,
    "fields_with_defaults_count": 25,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
