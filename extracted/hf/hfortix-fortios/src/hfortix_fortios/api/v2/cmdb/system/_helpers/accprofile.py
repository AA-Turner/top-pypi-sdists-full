"""Validation helpers for system/accprofile - Auto-generated"""

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
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "scope": "vdom",
    "secfabgrp": "none",
    "ftviewgrp": "none",
    "authgrp": "none",
    "sysgrp": "none",
    "netgrp": "none",
    "loggrp": "none",
    "fwgrp": "none",
    "vpngrp": "none",
    "utmgrp": "none",
    "wanoptgrp": "none",
    "wifi": "none",
    "admintimeout-override": "disable",
    "admintimeout": 10,
    "cli-diagnose": "disable",
    "cli-get": "disable",
    "cli-show": "disable",
    "cli-exec": "disable",
    "cli-config": "disable",
    "system-execute-ssh": "enable",
    "system-execute-telnet": "enable",
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
    "scope": "option",  # Scope of admin access: global or specific VDOM(s).
    "comments": "var-string",  # Comment.
    "secfabgrp": "option",  # Security Fabric.
    "ftviewgrp": "option",  # FortiView.
    "authgrp": "option",  # Administrator access to Users and Devices.
    "sysgrp": "option",  # System Configuration.
    "netgrp": "option",  # Network Configuration.
    "loggrp": "option",  # Administrator access to Logging and Reporting including viewing log messages.
    "fwgrp": "option",  # Administrator access to the Firewall configuration.
    "vpngrp": "option",  # Administrator access to IPsec, SSL, PPTP, and L2TP VPN.
    "utmgrp": "option",  # Administrator access to Security Profiles.
    "wanoptgrp": "option",  # Administrator access to WAN Opt & Cache.
    "wifi": "option",  # Administrator access to the WiFi controller and Switch controller.
    "netgrp-permission": "string",  # Custom network permission.
    "sysgrp-permission": "string",  # Custom system permission.
    "fwgrp-permission": "string",  # Custom firewall permission.
    "loggrp-permission": "string",  # Custom Log & Report permission.
    "utmgrp-permission": "string",  # Custom Security Profile permissions.
    "secfabgrp-permission": "string",  # Custom Security Fabric permissions.
    "admintimeout-override": "option",  # Enable/disable overriding the global administrator idle timeout.
    "admintimeout": "integer",  # Administrator timeout for this access profile (0 - 480 min, default = 10, 0 mean
    "cli-diagnose": "option",  # Enable/disable permission to run diagnostic commands.
    "cli-get": "option",  # Enable/disable permission to run get commands.
    "cli-show": "option",  # Enable/disable permission to run show commands.
    "cli-exec": "option",  # Enable/disable permission to run execute commands.
    "cli-config": "option",  # Enable/disable permission to run config commands.
    "system-execute-ssh": "option",  # Enable/disable permission to execute SSH commands.
    "system-execute-telnet": "option",  # Enable/disable permission to execute TELNET commands.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "scope": "Scope of admin access: global or specific VDOM(s).",
    "comments": "Comment.",
    "secfabgrp": "Security Fabric.",
    "ftviewgrp": "FortiView.",
    "authgrp": "Administrator access to Users and Devices.",
    "sysgrp": "System Configuration.",
    "netgrp": "Network Configuration.",
    "loggrp": "Administrator access to Logging and Reporting including viewing log messages.",
    "fwgrp": "Administrator access to the Firewall configuration.",
    "vpngrp": "Administrator access to IPsec, SSL, PPTP, and L2TP VPN.",
    "utmgrp": "Administrator access to Security Profiles.",
    "wanoptgrp": "Administrator access to WAN Opt & Cache.",
    "wifi": "Administrator access to the WiFi controller and Switch controller.",
    "netgrp-permission": "Custom network permission.",
    "sysgrp-permission": "Custom system permission.",
    "fwgrp-permission": "Custom firewall permission.",
    "loggrp-permission": "Custom Log & Report permission.",
    "utmgrp-permission": "Custom Security Profile permissions.",
    "secfabgrp-permission": "Custom Security Fabric permissions.",
    "admintimeout-override": "Enable/disable overriding the global administrator idle timeout.",
    "admintimeout": "Administrator timeout for this access profile (0 - 480 min, default = 10, 0 means never timeout).",
    "cli-diagnose": "Enable/disable permission to run diagnostic commands.",
    "cli-get": "Enable/disable permission to run get commands.",
    "cli-show": "Enable/disable permission to run show commands.",
    "cli-exec": "Enable/disable permission to run execute commands.",
    "cli-config": "Enable/disable permission to run config commands.",
    "system-execute-ssh": "Enable/disable permission to execute SSH commands.",
    "system-execute-telnet": "Enable/disable permission to execute TELNET commands.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "admintimeout": {"type": "integer", "min": 1, "max": 480},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "netgrp-permission": {
        "cfg": {
            "type": "option",
            "help": "Network Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "packet-capture": {
            "type": "option",
            "help": "Packet Capture Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "route-cfg": {
            "type": "option",
            "help": "Router Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
    "sysgrp-permission": {
        "admin": {
            "type": "option",
            "help": "Administrator Users.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "upd": {
            "type": "option",
            "help": "FortiGuard Updates.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "cfg": {
            "type": "option",
            "help": "System Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "mnt": {
            "type": "option",
            "help": "Maintenance.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
    "fwgrp-permission": {
        "policy": {
            "type": "option",
            "help": "Policy Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "address": {
            "type": "option",
            "help": "Address Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "service": {
            "type": "option",
            "help": "Service Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "schedule": {
            "type": "option",
            "help": "Schedule Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "others": {
            "type": "option",
            "help": "Other Firewall Configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
    "loggrp-permission": {
        "config": {
            "type": "option",
            "help": "Log & Report configuration.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "data-access": {
            "type": "option",
            "help": "Log & Report Data Access.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "report-access": {
            "type": "option",
            "help": "Log & Report Report Access.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "threat-weight": {
            "type": "option",
            "help": "Log & Report Threat Weight.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
    "utmgrp-permission": {
        "antivirus": {
            "type": "option",
            "help": "Antivirus profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "ips": {
            "type": "option",
            "help": "IPS profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "webfilter": {
            "type": "option",
            "help": "Web Filter profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "emailfilter": {
            "type": "option",
            "help": "Email Filter and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "dlp": {
            "type": "option",
            "help": "DLP profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "file-filter": {
            "type": "option",
            "help": "File-filter profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "application-control": {
            "type": "option",
            "help": "Application Control profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "icap": {
            "type": "option",
            "help": "ICAP profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "voip": {
            "type": "option",
            "help": "VoIP profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "waf": {
            "type": "option",
            "help": "Web Application Firewall profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "dnsfilter": {
            "type": "option",
            "help": "DNS Filter profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "endpoint-control": {
            "type": "option",
            "help": "FortiClient Profiles.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "videofilter": {
            "type": "option",
            "help": "Video filter profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "virtual-patch": {
            "type": "option",
            "help": "Virtual patch profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "casb": {
            "type": "option",
            "help": "Inline CASB filter profile and settings",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "telemetry": {
            "type": "option",
            "help": "Telemetry profile and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
    "secfabgrp-permission": {
        "csfsys": {
            "type": "option",
            "help": "Security Fabric system profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
        "csffoo": {
            "type": "option",
            "help": "Fabric Overlay Orchestrator profiles and settings.",
            "default": "none",
            "options": ["none", "read", "read-write"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SCOPE = [
    "vdom",
    "global",
]
VALID_BODY_SECFABGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_FTVIEWGRP = [
    "none",
    "read",
    "read-write",
]
VALID_BODY_AUTHGRP = [
    "none",
    "read",
    "read-write",
]
VALID_BODY_SYSGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_NETGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_LOGGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_FWGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_VPNGRP = [
    "none",
    "read",
    "read-write",
]
VALID_BODY_UTMGRP = [
    "none",
    "read",
    "read-write",
    "custom",
]
VALID_BODY_WANOPTGRP = [
    "none",
    "read",
    "read-write",
]
VALID_BODY_WIFI = [
    "none",
    "read",
    "read-write",
]
VALID_BODY_ADMINTIMEOUT_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_CLI_DIAGNOSE = [
    "enable",
    "disable",
]
VALID_BODY_CLI_GET = [
    "enable",
    "disable",
]
VALID_BODY_CLI_SHOW = [
    "enable",
    "disable",
]
VALID_BODY_CLI_EXEC = [
    "enable",
    "disable",
]
VALID_BODY_CLI_CONFIG = [
    "enable",
    "disable",
]
VALID_BODY_SYSTEM_EXECUTE_SSH = [
    "enable",
    "disable",
]
VALID_BODY_SYSTEM_EXECUTE_TELNET = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_accprofile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/accprofile."""
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


def validate_system_accprofile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/accprofile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secfabgrp" in payload:
        is_valid, error = _validate_enum_field(
            "secfabgrp",
            payload["secfabgrp"],
            VALID_BODY_SECFABGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftviewgrp" in payload:
        is_valid, error = _validate_enum_field(
            "ftviewgrp",
            payload["ftviewgrp"],
            VALID_BODY_FTVIEWGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authgrp" in payload:
        is_valid, error = _validate_enum_field(
            "authgrp",
            payload["authgrp"],
            VALID_BODY_AUTHGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sysgrp" in payload:
        is_valid, error = _validate_enum_field(
            "sysgrp",
            payload["sysgrp"],
            VALID_BODY_SYSGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netgrp" in payload:
        is_valid, error = _validate_enum_field(
            "netgrp",
            payload["netgrp"],
            VALID_BODY_NETGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "loggrp" in payload:
        is_valid, error = _validate_enum_field(
            "loggrp",
            payload["loggrp"],
            VALID_BODY_LOGGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwgrp" in payload:
        is_valid, error = _validate_enum_field(
            "fwgrp",
            payload["fwgrp"],
            VALID_BODY_FWGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpngrp" in payload:
        is_valid, error = _validate_enum_field(
            "vpngrp",
            payload["vpngrp"],
            VALID_BODY_VPNGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utmgrp" in payload:
        is_valid, error = _validate_enum_field(
            "utmgrp",
            payload["utmgrp"],
            VALID_BODY_UTMGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanoptgrp" in payload:
        is_valid, error = _validate_enum_field(
            "wanoptgrp",
            payload["wanoptgrp"],
            VALID_BODY_WANOPTGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wifi" in payload:
        is_valid, error = _validate_enum_field(
            "wifi",
            payload["wifi"],
            VALID_BODY_WIFI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admintimeout-override" in payload:
        is_valid, error = _validate_enum_field(
            "admintimeout-override",
            payload["admintimeout-override"],
            VALID_BODY_ADMINTIMEOUT_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-diagnose" in payload:
        is_valid, error = _validate_enum_field(
            "cli-diagnose",
            payload["cli-diagnose"],
            VALID_BODY_CLI_DIAGNOSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-get" in payload:
        is_valid, error = _validate_enum_field(
            "cli-get",
            payload["cli-get"],
            VALID_BODY_CLI_GET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-show" in payload:
        is_valid, error = _validate_enum_field(
            "cli-show",
            payload["cli-show"],
            VALID_BODY_CLI_SHOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-exec" in payload:
        is_valid, error = _validate_enum_field(
            "cli-exec",
            payload["cli-exec"],
            VALID_BODY_CLI_EXEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-config" in payload:
        is_valid, error = _validate_enum_field(
            "cli-config",
            payload["cli-config"],
            VALID_BODY_CLI_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-execute-ssh" in payload:
        is_valid, error = _validate_enum_field(
            "system-execute-ssh",
            payload["system-execute-ssh"],
            VALID_BODY_SYSTEM_EXECUTE_SSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-execute-telnet" in payload:
        is_valid, error = _validate_enum_field(
            "system-execute-telnet",
            payload["system-execute-telnet"],
            VALID_BODY_SYSTEM_EXECUTE_TELNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_accprofile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/accprofile."""
    # Validate enum values using central function
    if "scope" in payload:
        is_valid, error = _validate_enum_field(
            "scope",
            payload["scope"],
            VALID_BODY_SCOPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secfabgrp" in payload:
        is_valid, error = _validate_enum_field(
            "secfabgrp",
            payload["secfabgrp"],
            VALID_BODY_SECFABGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ftviewgrp" in payload:
        is_valid, error = _validate_enum_field(
            "ftviewgrp",
            payload["ftviewgrp"],
            VALID_BODY_FTVIEWGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authgrp" in payload:
        is_valid, error = _validate_enum_field(
            "authgrp",
            payload["authgrp"],
            VALID_BODY_AUTHGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sysgrp" in payload:
        is_valid, error = _validate_enum_field(
            "sysgrp",
            payload["sysgrp"],
            VALID_BODY_SYSGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netgrp" in payload:
        is_valid, error = _validate_enum_field(
            "netgrp",
            payload["netgrp"],
            VALID_BODY_NETGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "loggrp" in payload:
        is_valid, error = _validate_enum_field(
            "loggrp",
            payload["loggrp"],
            VALID_BODY_LOGGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fwgrp" in payload:
        is_valid, error = _validate_enum_field(
            "fwgrp",
            payload["fwgrp"],
            VALID_BODY_FWGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpngrp" in payload:
        is_valid, error = _validate_enum_field(
            "vpngrp",
            payload["vpngrp"],
            VALID_BODY_VPNGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utmgrp" in payload:
        is_valid, error = _validate_enum_field(
            "utmgrp",
            payload["utmgrp"],
            VALID_BODY_UTMGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanoptgrp" in payload:
        is_valid, error = _validate_enum_field(
            "wanoptgrp",
            payload["wanoptgrp"],
            VALID_BODY_WANOPTGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wifi" in payload:
        is_valid, error = _validate_enum_field(
            "wifi",
            payload["wifi"],
            VALID_BODY_WIFI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admintimeout-override" in payload:
        is_valid, error = _validate_enum_field(
            "admintimeout-override",
            payload["admintimeout-override"],
            VALID_BODY_ADMINTIMEOUT_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-diagnose" in payload:
        is_valid, error = _validate_enum_field(
            "cli-diagnose",
            payload["cli-diagnose"],
            VALID_BODY_CLI_DIAGNOSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-get" in payload:
        is_valid, error = _validate_enum_field(
            "cli-get",
            payload["cli-get"],
            VALID_BODY_CLI_GET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-show" in payload:
        is_valid, error = _validate_enum_field(
            "cli-show",
            payload["cli-show"],
            VALID_BODY_CLI_SHOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-exec" in payload:
        is_valid, error = _validate_enum_field(
            "cli-exec",
            payload["cli-exec"],
            VALID_BODY_CLI_EXEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-config" in payload:
        is_valid, error = _validate_enum_field(
            "cli-config",
            payload["cli-config"],
            VALID_BODY_CLI_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-execute-ssh" in payload:
        is_valid, error = _validate_enum_field(
            "system-execute-ssh",
            payload["system-execute-ssh"],
            VALID_BODY_SYSTEM_EXECUTE_SSH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-execute-telnet" in payload:
        is_valid, error = _validate_enum_field(
            "system-execute-telnet",
            payload["system-execute-telnet"],
            VALID_BODY_SYSTEM_EXECUTE_TELNET,
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
    "endpoint": "system/accprofile",
    "category": "cmdb",
    "api_path": "system/accprofile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure access profiles for system administrators.",
    "total_fields": 29,
    "required_fields_count": 1,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
