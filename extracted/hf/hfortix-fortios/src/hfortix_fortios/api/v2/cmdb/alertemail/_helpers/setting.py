"""Validation helpers for alertemail/setting - Auto-generated"""

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
    "username": "",
    "mailto1": "",
    "mailto2": "",
    "mailto3": "",
    "filter-mode": "category",
    "email-interval": 5,
    "IPS-logs": "disable",
    "firewall-authentication-failure-logs": "disable",
    "HA-logs": "disable",
    "IPsec-errors-logs": "disable",
    "FDS-update-logs": "disable",
    "PPP-errors-logs": "disable",
    "sslvpn-authentication-errors-logs": "disable",
    "antivirus-logs": "disable",
    "webfilter-logs": "disable",
    "configuration-changes-logs": "disable",
    "violation-traffic-logs": "disable",
    "admin-login-logs": "disable",
    "FDS-license-expiring-warning": "disable",
    "log-disk-usage-warning": "disable",
    "fortiguard-log-quota-warning": "disable",
    "amc-interface-bypass-mode": "disable",
    "FIPS-CC-errors": "disable",
    "FSSO-disconnect-logs": "disable",
    "ssh-logs": "disable",
    "local-disk-usage": 75,
    "emergency-interval": 1,
    "alert-interval": 2,
    "critical-interval": 3,
    "error-interval": 5,
    "warning-interval": 10,
    "notification-interval": 20,
    "information-interval": 30,
    "debug-interval": 60,
    "severity": "alert",
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
    "username": "string",  # Name that appears in the From: field of alert emails (max. 63 characters).
    "mailto1": "string",  # Email address to send alert email to (usually a system administrator) (max. 63 c
    "mailto2": "string",  # Optional second email address to send alert email to (max. 63 characters).
    "mailto3": "string",  # Optional third email address to send alert email to (max. 63 characters).
    "filter-mode": "option",  # How to filter log messages that are sent to alert emails.
    "email-interval": "integer",  # Interval between sending alert emails (1 - 99999 min, default = 5).
    "IPS-logs": "option",  # Enable/disable IPS logs in alert email.
    "firewall-authentication-failure-logs": "option",  # Enable/disable firewall authentication failure logs in alert email.
    "HA-logs": "option",  # Enable/disable HA logs in alert email.
    "IPsec-errors-logs": "option",  # Enable/disable IPsec error logs in alert email.
    "FDS-update-logs": "option",  # Enable/disable FortiGuard update logs in alert email.
    "PPP-errors-logs": "option",  # Enable/disable PPP error logs in alert email.
    "sslvpn-authentication-errors-logs": "option",  # Enable/disable Agentless VPN authentication error logs in alert email.
    "antivirus-logs": "option",  # Enable/disable antivirus logs in alert email.
    "webfilter-logs": "option",  # Enable/disable web filter logs in alert email.
    "configuration-changes-logs": "option",  # Enable/disable configuration change logs in alert email.
    "violation-traffic-logs": "option",  # Enable/disable violation traffic logs in alert email.
    "admin-login-logs": "option",  # Enable/disable administrator login/logout logs in alert email.
    "FDS-license-expiring-warning": "option",  # Enable/disable FortiGuard license expiration warnings in alert email.
    "log-disk-usage-warning": "option",  # Enable/disable disk usage warnings in alert email.
    "fortiguard-log-quota-warning": "option",  # Enable/disable FortiCloud log quota warnings in alert email.
    "amc-interface-bypass-mode": "option",  # Enable/disable Fortinet Advanced Mezzanine Card (AMC) interface bypass mode logs
    "FIPS-CC-errors": "option",  # Enable/disable FIPS and Common Criteria error logs in alert email.
    "FSSO-disconnect-logs": "option",  # Enable/disable logging of FSSO collector agent disconnect.
    "ssh-logs": "option",  # Enable/disable SSH logs in alert email.
    "local-disk-usage": "integer",  # Disk usage percentage at which to send alert email (1 - 99 percent, default = 75
    "emergency-interval": "integer",  # Emergency alert interval in minutes.
    "alert-interval": "integer",  # Alert alert interval in minutes.
    "critical-interval": "integer",  # Critical alert interval in minutes.
    "error-interval": "integer",  # Error alert interval in minutes.
    "warning-interval": "integer",  # Warning alert interval in minutes.
    "notification-interval": "integer",  # Notification alert interval in minutes.
    "information-interval": "integer",  # Information alert interval in minutes.
    "debug-interval": "integer",  # Debug alert interval in minutes.
    "severity": "option",  # Lowest severity level to log.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "username": "Name that appears in the From: field of alert emails (max. 63 characters).",
    "mailto1": "Email address to send alert email to (usually a system administrator) (max. 63 characters).",
    "mailto2": "Optional second email address to send alert email to (max. 63 characters).",
    "mailto3": "Optional third email address to send alert email to (max. 63 characters).",
    "filter-mode": "How to filter log messages that are sent to alert emails.",
    "email-interval": "Interval between sending alert emails (1 - 99999 min, default = 5).",
    "IPS-logs": "Enable/disable IPS logs in alert email.",
    "firewall-authentication-failure-logs": "Enable/disable firewall authentication failure logs in alert email.",
    "HA-logs": "Enable/disable HA logs in alert email.",
    "IPsec-errors-logs": "Enable/disable IPsec error logs in alert email.",
    "FDS-update-logs": "Enable/disable FortiGuard update logs in alert email.",
    "PPP-errors-logs": "Enable/disable PPP error logs in alert email.",
    "sslvpn-authentication-errors-logs": "Enable/disable Agentless VPN authentication error logs in alert email.",
    "antivirus-logs": "Enable/disable antivirus logs in alert email.",
    "webfilter-logs": "Enable/disable web filter logs in alert email.",
    "configuration-changes-logs": "Enable/disable configuration change logs in alert email.",
    "violation-traffic-logs": "Enable/disable violation traffic logs in alert email.",
    "admin-login-logs": "Enable/disable administrator login/logout logs in alert email.",
    "FDS-license-expiring-warning": "Enable/disable FortiGuard license expiration warnings in alert email.",
    "log-disk-usage-warning": "Enable/disable disk usage warnings in alert email.",
    "fortiguard-log-quota-warning": "Enable/disable FortiCloud log quota warnings in alert email.",
    "amc-interface-bypass-mode": "Enable/disable Fortinet Advanced Mezzanine Card (AMC) interface bypass mode logs in alert email.",
    "FIPS-CC-errors": "Enable/disable FIPS and Common Criteria error logs in alert email.",
    "FSSO-disconnect-logs": "Enable/disable logging of FSSO collector agent disconnect.",
    "ssh-logs": "Enable/disable SSH logs in alert email.",
    "local-disk-usage": "Disk usage percentage at which to send alert email (1 - 99 percent, default = 75).",
    "emergency-interval": "Emergency alert interval in minutes.",
    "alert-interval": "Alert alert interval in minutes.",
    "critical-interval": "Critical alert interval in minutes.",
    "error-interval": "Error alert interval in minutes.",
    "warning-interval": "Warning alert interval in minutes.",
    "notification-interval": "Notification alert interval in minutes.",
    "information-interval": "Information alert interval in minutes.",
    "debug-interval": "Debug alert interval in minutes.",
    "severity": "Lowest severity level to log.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "username": {"type": "string", "max_length": 63},
    "mailto1": {"type": "string", "max_length": 63},
    "mailto2": {"type": "string", "max_length": 63},
    "mailto3": {"type": "string", "max_length": 63},
    "email-interval": {"type": "integer", "min": 1, "max": 99999},
    "local-disk-usage": {"type": "integer", "min": 1, "max": 99},
    "emergency-interval": {"type": "integer", "min": 1, "max": 99999},
    "alert-interval": {"type": "integer", "min": 1, "max": 99999},
    "critical-interval": {"type": "integer", "min": 1, "max": 99999},
    "error-interval": {"type": "integer", "min": 1, "max": 99999},
    "warning-interval": {"type": "integer", "min": 1, "max": 99999},
    "notification-interval": {"type": "integer", "min": 1, "max": 99999},
    "information-interval": {"type": "integer", "min": 1, "max": 99999},
    "debug-interval": {"type": "integer", "min": 1, "max": 99999},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_FILTER_MODE = [
    "category",
    "threshold",
]
VALID_BODY_IPS_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_FIREWALL_AUTHENTICATION_FAILURE_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_HA_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_IPSEC_ERRORS_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_FDS_UPDATE_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_PPP_ERRORS_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_SSLVPN_AUTHENTICATION_ERRORS_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_ANTIVIRUS_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_WEBFILTER_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_CONFIGURATION_CHANGES_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_VIOLATION_TRAFFIC_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_LOGIN_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_FDS_LICENSE_EXPIRING_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_LOG_DISK_USAGE_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_FORTIGUARD_LOG_QUOTA_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_AMC_INTERFACE_BYPASS_MODE = [
    "enable",
    "disable",
]
VALID_BODY_FIPS_CC_ERRORS = [
    "enable",
    "disable",
]
VALID_BODY_FSSO_DISCONNECT_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_SSH_LOGS = [
    "enable",
    "disable",
]
VALID_BODY_SEVERITY = [
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_alertemail_setting_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for alertemail/setting."""
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


def validate_alertemail_setting_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new alertemail/setting object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "filter-mode" in payload:
        is_valid, error = _validate_enum_field(
            "filter-mode",
            payload["filter-mode"],
            VALID_BODY_FILTER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "IPS-logs" in payload:
        is_valid, error = _validate_enum_field(
            "IPS-logs",
            payload["IPS-logs"],
            VALID_BODY_IPS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firewall-authentication-failure-logs" in payload:
        is_valid, error = _validate_enum_field(
            "firewall-authentication-failure-logs",
            payload["firewall-authentication-failure-logs"],
            VALID_BODY_FIREWALL_AUTHENTICATION_FAILURE_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "HA-logs" in payload:
        is_valid, error = _validate_enum_field(
            "HA-logs",
            payload["HA-logs"],
            VALID_BODY_HA_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "IPsec-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "IPsec-errors-logs",
            payload["IPsec-errors-logs"],
            VALID_BODY_IPSEC_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FDS-update-logs" in payload:
        is_valid, error = _validate_enum_field(
            "FDS-update-logs",
            payload["FDS-update-logs"],
            VALID_BODY_FDS_UPDATE_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "PPP-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "PPP-errors-logs",
            payload["PPP-errors-logs"],
            VALID_BODY_PPP_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sslvpn-authentication-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "sslvpn-authentication-errors-logs",
            payload["sslvpn-authentication-errors-logs"],
            VALID_BODY_SSLVPN_AUTHENTICATION_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antivirus-logs" in payload:
        is_valid, error = _validate_enum_field(
            "antivirus-logs",
            payload["antivirus-logs"],
            VALID_BODY_ANTIVIRUS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-logs" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-logs",
            payload["webfilter-logs"],
            VALID_BODY_WEBFILTER_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "configuration-changes-logs" in payload:
        is_valid, error = _validate_enum_field(
            "configuration-changes-logs",
            payload["configuration-changes-logs"],
            VALID_BODY_CONFIGURATION_CHANGES_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "violation-traffic-logs" in payload:
        is_valid, error = _validate_enum_field(
            "violation-traffic-logs",
            payload["violation-traffic-logs"],
            VALID_BODY_VIOLATION_TRAFFIC_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-login-logs" in payload:
        is_valid, error = _validate_enum_field(
            "admin-login-logs",
            payload["admin-login-logs"],
            VALID_BODY_ADMIN_LOGIN_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FDS-license-expiring-warning" in payload:
        is_valid, error = _validate_enum_field(
            "FDS-license-expiring-warning",
            payload["FDS-license-expiring-warning"],
            VALID_BODY_FDS_LICENSE_EXPIRING_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-disk-usage-warning" in payload:
        is_valid, error = _validate_enum_field(
            "log-disk-usage-warning",
            payload["log-disk-usage-warning"],
            VALID_BODY_LOG_DISK_USAGE_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiguard-log-quota-warning" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-log-quota-warning",
            payload["fortiguard-log-quota-warning"],
            VALID_BODY_FORTIGUARD_LOG_QUOTA_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "amc-interface-bypass-mode" in payload:
        is_valid, error = _validate_enum_field(
            "amc-interface-bypass-mode",
            payload["amc-interface-bypass-mode"],
            VALID_BODY_AMC_INTERFACE_BYPASS_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FIPS-CC-errors" in payload:
        is_valid, error = _validate_enum_field(
            "FIPS-CC-errors",
            payload["FIPS-CC-errors"],
            VALID_BODY_FIPS_CC_ERRORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FSSO-disconnect-logs" in payload:
        is_valid, error = _validate_enum_field(
            "FSSO-disconnect-logs",
            payload["FSSO-disconnect-logs"],
            VALID_BODY_FSSO_DISCONNECT_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-logs" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-logs",
            payload["ssh-logs"],
            VALID_BODY_SSH_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "severity" in payload:
        is_valid, error = _validate_enum_field(
            "severity",
            payload["severity"],
            VALID_BODY_SEVERITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_alertemail_setting_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update alertemail/setting."""
    # Validate enum values using central function
    if "filter-mode" in payload:
        is_valid, error = _validate_enum_field(
            "filter-mode",
            payload["filter-mode"],
            VALID_BODY_FILTER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "IPS-logs" in payload:
        is_valid, error = _validate_enum_field(
            "IPS-logs",
            payload["IPS-logs"],
            VALID_BODY_IPS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firewall-authentication-failure-logs" in payload:
        is_valid, error = _validate_enum_field(
            "firewall-authentication-failure-logs",
            payload["firewall-authentication-failure-logs"],
            VALID_BODY_FIREWALL_AUTHENTICATION_FAILURE_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "HA-logs" in payload:
        is_valid, error = _validate_enum_field(
            "HA-logs",
            payload["HA-logs"],
            VALID_BODY_HA_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "IPsec-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "IPsec-errors-logs",
            payload["IPsec-errors-logs"],
            VALID_BODY_IPSEC_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FDS-update-logs" in payload:
        is_valid, error = _validate_enum_field(
            "FDS-update-logs",
            payload["FDS-update-logs"],
            VALID_BODY_FDS_UPDATE_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "PPP-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "PPP-errors-logs",
            payload["PPP-errors-logs"],
            VALID_BODY_PPP_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sslvpn-authentication-errors-logs" in payload:
        is_valid, error = _validate_enum_field(
            "sslvpn-authentication-errors-logs",
            payload["sslvpn-authentication-errors-logs"],
            VALID_BODY_SSLVPN_AUTHENTICATION_ERRORS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "antivirus-logs" in payload:
        is_valid, error = _validate_enum_field(
            "antivirus-logs",
            payload["antivirus-logs"],
            VALID_BODY_ANTIVIRUS_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webfilter-logs" in payload:
        is_valid, error = _validate_enum_field(
            "webfilter-logs",
            payload["webfilter-logs"],
            VALID_BODY_WEBFILTER_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "configuration-changes-logs" in payload:
        is_valid, error = _validate_enum_field(
            "configuration-changes-logs",
            payload["configuration-changes-logs"],
            VALID_BODY_CONFIGURATION_CHANGES_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "violation-traffic-logs" in payload:
        is_valid, error = _validate_enum_field(
            "violation-traffic-logs",
            payload["violation-traffic-logs"],
            VALID_BODY_VIOLATION_TRAFFIC_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-login-logs" in payload:
        is_valid, error = _validate_enum_field(
            "admin-login-logs",
            payload["admin-login-logs"],
            VALID_BODY_ADMIN_LOGIN_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FDS-license-expiring-warning" in payload:
        is_valid, error = _validate_enum_field(
            "FDS-license-expiring-warning",
            payload["FDS-license-expiring-warning"],
            VALID_BODY_FDS_LICENSE_EXPIRING_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-disk-usage-warning" in payload:
        is_valid, error = _validate_enum_field(
            "log-disk-usage-warning",
            payload["log-disk-usage-warning"],
            VALID_BODY_LOG_DISK_USAGE_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiguard-log-quota-warning" in payload:
        is_valid, error = _validate_enum_field(
            "fortiguard-log-quota-warning",
            payload["fortiguard-log-quota-warning"],
            VALID_BODY_FORTIGUARD_LOG_QUOTA_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "amc-interface-bypass-mode" in payload:
        is_valid, error = _validate_enum_field(
            "amc-interface-bypass-mode",
            payload["amc-interface-bypass-mode"],
            VALID_BODY_AMC_INTERFACE_BYPASS_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FIPS-CC-errors" in payload:
        is_valid, error = _validate_enum_field(
            "FIPS-CC-errors",
            payload["FIPS-CC-errors"],
            VALID_BODY_FIPS_CC_ERRORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "FSSO-disconnect-logs" in payload:
        is_valid, error = _validate_enum_field(
            "FSSO-disconnect-logs",
            payload["FSSO-disconnect-logs"],
            VALID_BODY_FSSO_DISCONNECT_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-logs" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-logs",
            payload["ssh-logs"],
            VALID_BODY_SSH_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "severity" in payload:
        is_valid, error = _validate_enum_field(
            "severity",
            payload["severity"],
            VALID_BODY_SEVERITY,
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
    "endpoint": "alertemail/setting",
    "category": "cmdb",
    "api_path": "alertemail/setting",
    "help": "Configure alert email settings.",
    "total_fields": 35,
    "required_fields_count": 0,
    "fields_with_defaults_count": 35,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
